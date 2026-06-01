"""
Salesforce API Client
Handles authentication and operations for posting internal comments
"""
import logging
from typing import Dict, Optional
from simple_salesforce import Salesforce
from simple_salesforce.exceptions import SalesforceError

logger = logging.getLogger(__name__)


class SFDCClient:
    """Salesforce API client for case comment operations"""

    def __init__(
        self,
        username: str,
        password: str,
        security_token: str,
        domain: str = "test",
        api_version: str = "v60.0"
    ):
        """
        Initialize SFDC client

        Args:
            username: Salesforce username
            password: Salesforce password
            security_token: Salesforce security token
            domain: 'test' for sandbox, 'login' for production
            api_version: Salesforce API version
        """
        self.username = username
        self.password = password
        self.security_token = security_token
        self.domain = domain
        self.api_version = api_version
        self.sf = None

    def authenticate(self) -> bool:
        """
        Authenticate with Salesforce

        Returns:
            True if authentication successful, False otherwise
        """
        try:
            self.sf = Salesforce(
                username=self.username,
                password=self.password,
                security_token=self.security_token,
                domain=self.domain,
                version=self.api_version.replace('v', '')
            )
            logger.info(f"Successfully authenticated to Salesforce as {self.username}")
            return True
        except SalesforceError as e:
            logger.error(f"Salesforce authentication failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during authentication: {e}")
            return False

    def get_case_details(self, case_id: str) -> Optional[Dict]:
        """
        Fetch case details from Salesforce

        Args:
            case_id: Salesforce Case ID

        Returns:
            Dictionary with case details or None if error
        """
        if not self.sf:
            logger.error("Not authenticated. Call authenticate() first.")
            return None

        try:
            case = self.sf.Case.get(case_id)
            logger.info(f"Retrieved case details for {case_id}")
            return case
        except SalesforceError as e:
            logger.error(f"Failed to get case {case_id}: {e}")
            return None

    def post_internal_comment(self, case_id: str, comment_body: str) -> bool:
        """
        Post an internal comment to a Salesforce case

        Args:
            case_id: Salesforce Case ID
            comment_body: Comment text to post

        Returns:
            True if successful, False otherwise
        """
        if not self.sf:
            logger.error("Not authenticated. Call authenticate() first.")
            return False

        try:
            # CaseComment fields:
            # - ParentId: Case ID
            # - CommentBody: The comment text
            # - IsPublished: False for internal comments
            result = self.sf.CaseComment.create({
                'ParentId': case_id,
                'CommentBody': comment_body,
                'IsPublished': False  # Internal comment
            })

            if result.get('success'):
                comment_id = result.get('id')
                logger.info(f"Successfully posted internal comment {comment_id} to case {case_id}")
                return True
            else:
                logger.error(f"Failed to create comment: {result}")
                return False

        except SalesforceError as e:
            logger.error(f"Salesforce error posting comment: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error posting comment: {e}")
            return False

    def update_case(self, case_id: str, fields: Dict) -> bool:
        """
        Update case fields in Salesforce

        Args:
            case_id: Salesforce Case ID
            fields: Dictionary of field names and values to update

        Returns:
            True if successful, False otherwise
        """
        if not self.sf:
            logger.error("Not authenticated. Call authenticate() first.")
            return False

        try:
            result = self.sf.Case.update(case_id, fields)
            logger.info(f"Updated case {case_id} with fields: {list(fields.keys())}")
            return True
        except SalesforceError as e:
            logger.error(f"Failed to update case {case_id}: {e}")
            return False


# Standalone test
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    # Load environment variables
    load_dotenv("config/.env")

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Test authentication
    client = SFDCClient(
        username=os.getenv("SFDC_USERNAME"),
        password=os.getenv("SFDC_PASSWORD"),
        security_token=os.getenv("SFDC_SECURITY_TOKEN"),
        domain=os.getenv("SFDC_DOMAIN", "test")
    )

    if client.authenticate():
        print("✓ Authentication successful")

        # Test case details retrieval (replace with actual case ID)
        test_case_id = os.getenv("TEST_CASE_ID")
        if test_case_id:
            case = client.get_case_details(test_case_id)
            if case:
                print(f"✓ Retrieved case: {case.get('CaseNumber')}")
    else:
        print("✗ Authentication failed - check credentials in .env file")
