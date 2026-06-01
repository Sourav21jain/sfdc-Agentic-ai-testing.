"""
Salesforce Platform Event Listener
Subscribes to Case_Created__e events via Streaming API
"""
import asyncio
import logging
from typing import Callable, Optional
from aiosfstream import SalesforceStreamingClient, ReplayOption

logger = logging.getLogger(__name__)


class EventListener:
    """Async listener for Salesforce Platform Events"""

    def __init__(
        self,
        username: str,
        password: str,
        security_token: str,
        channel: str = "/event/Case_Created__e",
        domain: str = "test",
        replay_option: ReplayOption = ReplayOption.NEW_EVENTS
    ):
        """
        Initialize event listener

        Args:
            username: Salesforce username
            password: Salesforce password
            security_token: Salesforce security token
            channel: Platform Event channel to subscribe to
            domain: 'test' for sandbox, 'login' for production
            replay_option: Replay option for event streaming
        """
        self.username = username
        self.password = password
        self.security_token = security_token
        self.channel = channel
        self.domain = domain
        self.replay_option = replay_option
        self.client: Optional[SalesforceStreamingClient] = None
        self.is_running = False

    async def connect(self) -> bool:
        """
        Connect to Salesforce Streaming API

        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Build Salesforce instance URL
            if self.domain == "test":
                instance_url = "https://test.salesforce.com"
            else:
                instance_url = "https://login.salesforce.com"

            # Create streaming client
            self.client = SalesforceStreamingClient(
                consumer_key=None,  # Using username/password auth
                consumer_secret=None,
                username=self.username,
                password=f"{self.password}{self.security_token}"
            )

            logger.info(f"Connected to Salesforce Streaming API at {instance_url}")
            return True

        except Exception as e:
            logger.error(f"Failed to connect to Salesforce Streaming API: {e}")
            return False

    async def subscribe(self, event_handler: Callable) -> None:
        """
        Subscribe to Platform Events and handle them

        Args:
            event_handler: Async callback function to handle events
                           Should accept (event_data: dict) as parameter
        """
        if not self.client:
            logger.error("Client not connected. Call connect() first.")
            return

        self.is_running = True
        logger.info(f"Subscribing to channel: {self.channel}")

        try:
            async with self.client:
                await self.client.subscribe(self.channel, self.replay_option)

                async for message in self.client:
                    if not self.is_running:
                        break

                    try:
                        # Extract event data
                        event_data = message.get("payload", {})
                        logger.info(f"Received event: {message.get('event', {})}")

                        # Call the event handler
                        await event_handler(event_data)

                    except Exception as e:
                        logger.error(f"Error handling event: {e}")
                        # Continue listening despite handler errors

        except asyncio.CancelledError:
            logger.info("Event listener cancelled")
        except Exception as e:
            logger.error(f"Error in event subscription: {e}")
            # Attempt reconnection after delay
            if self.is_running:
                logger.info("Attempting to reconnect in 10 seconds...")
                await asyncio.sleep(10)
                await self.subscribe(event_handler)

    async def stop(self) -> None:
        """Stop listening for events"""
        self.is_running = False
        if self.client:
            logger.info("Stopping event listener")


# Standalone test
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv("config/.env")

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    async def test_event_handler(event_data: dict):
        """Test handler that prints received events"""
        print("\n" + "="*60)
        print("EVENT RECEIVED:")
        print(f"Case ID: {event_data.get('Case_Id__c')}")
        print(f"Cluster ID: {event_data.get('Cluster_Id__c')}")
        print("="*60 + "\n")

    async def main():
        listener = EventListener(
            username=os.getenv("SFDC_USERNAME"),
            password=os.getenv("SFDC_PASSWORD"),
            security_token=os.getenv("SFDC_SECURITY_TOKEN"),
            domain=os.getenv("SFDC_DOMAIN", "test")
        )

        if await listener.connect():
            print("✓ Connected to Salesforce Streaming API")
            print(f"✓ Listening for events on {listener.channel}")
            print("Press Ctrl+C to stop...")

            try:
                await listener.subscribe(test_event_handler)
            except KeyboardInterrupt:
                print("\nStopping listener...")
                await listener.stop()
        else:
            print("✗ Failed to connect to Salesforce")

    # Run the async main function
    asyncio.run(main())
