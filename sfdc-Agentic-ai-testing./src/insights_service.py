"""
Mock Insights Service - Simulates Tableau data source
Future: Replace with actual Tableau REST API integration
"""
import json
import logging
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class InsightsService:
    """Service to fetch OpenShift cluster insights data"""

    def __init__(self, data_source: str = "mock", data_path: str = "data/mock_insights.json"):
        """
        Initialize the insights service

        Args:
            data_source: Type of data source ('mock' or 'tableau_api')
            data_path: Path to mock data JSON file
        """
        self.data_source = data_source
        self.data_path = Path(data_path)
        self._data_cache = None

        if data_source == "mock":
            self._load_mock_data()

    def _load_mock_data(self) -> None:
        """Load mock data from JSON file"""
        try:
            with open(self.data_path, 'r') as f:
                self._data_cache = json.load(f)
            logger.info(f"Loaded mock data from {self.data_path}")
        except FileNotFoundError:
            logger.error(f"Mock data file not found: {self.data_path}")
            self._data_cache = {"clusters": {}}
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in mock data file: {e}")
            self._data_cache = {"clusters": {}}

    def get_cluster_insights(self, cluster_id: str) -> Optional[Dict]:
        """
        Fetch cluster insights for a given cluster ID

        Args:
            cluster_id: OpenShift cluster identifier

        Returns:
            Dictionary containing cluster insights or None if not found
        """
        if self.data_source == "mock":
            return self._get_mock_insights(cluster_id)
        elif self.data_source == "tableau_api":
            # Future implementation
            raise NotImplementedError("Tableau API integration not yet implemented")
        else:
            raise ValueError(f"Unknown data source: {self.data_source}")

    def _get_mock_insights(self, cluster_id: str) -> Optional[Dict]:
        """Get insights from mock data"""
        if not self._data_cache:
            self._load_mock_data()

        cluster_data = self._data_cache.get("clusters", {}).get(cluster_id)

        if cluster_data:
            logger.info(f"Found insights for cluster: {cluster_id}")
            return cluster_data
        else:
            logger.warning(f"No insights found for cluster: {cluster_id}")
            return None

    def get_all_cluster_ids(self) -> list:
        """Get list of all available cluster IDs"""
        if not self._data_cache:
            self._load_mock_data()

        return list(self._data_cache.get("clusters", {}).keys())


# Standalone test
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    service = InsightsService()

    # Test with existing cluster
    insights = service.get_cluster_insights("test-cluster-001")
    if insights:
        print(f"✓ Found insights for test-cluster-001:")
        print(json.dumps(insights, indent=2))

    # Test with non-existent cluster
    insights = service.get_cluster_insights("non-existent-cluster")
    if not insights:
        print("✓ Correctly returned None for non-existent cluster")

    # List all clusters
    all_ids = service.get_all_cluster_ids()
    print(f"\n✓ Available cluster IDs: {', '.join(all_ids)}")
