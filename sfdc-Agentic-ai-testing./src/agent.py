"""
Main Agent Orchestrator
Coordinates event listening, insights fetching, and comment posting
"""
import asyncio
import logging
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import yaml

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.event_listener import EventListener
from src.sfdc_client import SFDCClient
from src.insights_service import InsightsService
from src.comment_generator import CommentGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/agent.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)


class InsightsAgent:
    """Main orchestrator for the SFDC insights automation"""

    def __init__(self, config_path: str = "config/config.yaml"):
        """
        Initialize the agent

        Args:
            config_path: Path to YAML configuration file
        """
        # Load configuration
        self.config = self._load_config(config_path)
        self._load_env()

        # Initialize components
        self.sfdc_client = SFDCClient(
            username=self.sfdc_username,
            password=self.sfdc_password,
            security_token=self.sfdc_security_token,
            domain=self.sfdc_domain,
            api_version=self.config['salesforce']['api_version']
        )

        self.insights_service = InsightsService(
            data_source=self.config['insights']['data_source'],
            data_path=self.config['insights']['mock_data_path']
        )

        self.comment_generator = CommentGenerator(
            api_key=self.gemini_api_key,
            include_support_tips=self.config['agent']['include_support_tips']
        )

        self.event_listener = EventListener(
            username=self.sfdc_username,
            password=self.sfdc_password,
            security_token=self.sfdc_security_token,
            channel=self.config['salesforce']['streaming_channel'],
            domain=self.sfdc_domain
        )

        self.max_retries = self.config['agent']['max_retries']
        self.retry_delay = self.config['agent']['retry_delay_seconds']
        self.comment_prefix = self.config['agent']['comment_prefix']

    def _load_config(self, config_path: str) -> dict:
        """Load YAML configuration"""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.error(f"Config file not found: {config_path}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Invalid YAML in config file: {e}")
            raise

    def _load_env(self):
        """Load environment variables"""
        load_dotenv("config/.env")

        self.sfdc_username = os.getenv("SFDC_USERNAME")
        self.sfdc_password = os.getenv("SFDC_PASSWORD")
        self.sfdc_security_token = os.getenv("SFDC_SECURITY_TOKEN")
        self.sfdc_domain = os.getenv("SFDC_DOMAIN", "test")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")

        # Validate required env vars
        required_vars = [
            "SFDC_USERNAME", "SFDC_PASSWORD", "SFDC_SECURITY_TOKEN", "GEMINI_API_KEY"
        ]
        missing = [var for var in required_vars if not os.getenv(var)]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

    async def handle_case_event(self, event_data: dict):
        """
        Handle incoming case creation event

        Args:
            event_data: Platform Event payload
        """
        case_id = event_data.get('Case_Id__c')
        cluster_id = event_data.get('Cluster_Id__c')

        if not case_id or not cluster_id:
            logger.warning(f"Incomplete event data: {event_data}")
            return

        logger.info(f"Processing case {case_id} with cluster {cluster_id}")

        try:
            # Check if insights already posted (idempotency)
            case_details = self.sfdc_client.get_case_details(case_id)
            if case_details and case_details.get('Auto_Insights_Posted__c'):
                logger.info(f"Insights already posted for case {case_id}, skipping")
                return

            # Fetch cluster insights
            insights = self.insights_service.get_cluster_insights(cluster_id)

            # Generate AI-formatted comment
            comment = self.comment_generator.generate_comment(
                insights,
                comment_prefix=self.comment_prefix
            )

            # Post internal comment with retry logic
            success = await self._post_comment_with_retry(case_id, comment)

            if success:
                # Mark case as processed
                self.sfdc_client.update_case(case_id, {
                    'Auto_Insights_Posted__c': True
                })
                logger.info(f"Successfully processed case {case_id}")
            else:
                logger.error(f"Failed to post comment for case {case_id} after retries")

        except Exception as e:
            logger.error(f"Error processing case {case_id}: {e}", exc_info=True)

    async def _post_comment_with_retry(self, case_id: str, comment: str) -> bool:
        """
        Post comment with retry logic

        Args:
            case_id: Salesforce Case ID
            comment: Comment text

        Returns:
            True if successful, False otherwise
        """
        for attempt in range(self.max_retries):
            try:
                success = self.sfdc_client.post_internal_comment(case_id, comment)
                if success:
                    return True

                logger.warning(f"Attempt {attempt + 1}/{self.max_retries} failed for case {case_id}")

                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay)

            except Exception as e:
                logger.error(f"Exception on attempt {attempt + 1}: {e}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay)

        return False

    async def start(self):
        """Start the agent"""
        logger.info("="*60)
        logger.info("SFDC OpenShift Insights Agent Starting")
        logger.info("="*60)

        # Create logs directory if it doesn't exist
        Path("logs").mkdir(exist_ok=True)

        # Authenticate with Salesforce
        if not self.sfdc_client.authenticate():
            logger.error("Failed to authenticate with Salesforce. Exiting.")
            return

        logger.info("✓ Authenticated with Salesforce")

        # Connect to Streaming API
        if not await self.event_listener.connect():
            logger.error("Failed to connect to Salesforce Streaming API. Exiting.")
            return

        logger.info("✓ Connected to Salesforce Streaming API")
        logger.info(f"✓ Listening for events on {self.event_listener.channel}")
        logger.info("Agent is running. Press Ctrl+C to stop.")
        logger.info("="*60)

        # Start listening for events
        try:
            await self.event_listener.subscribe(self.handle_case_event)
        except KeyboardInterrupt:
            logger.info("Shutting down agent...")
            await self.event_listener.stop()
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)


async def main():
    """Main entry point"""
    try:
        agent = InsightsAgent()
        await agent.start()
    except Exception as e:
        logger.error(f"Failed to start agent: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
