"""
Unit tests for InsightsService
"""
import pytest
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.insights_service import InsightsService


def test_get_existing_cluster():
    """Test fetching insights for an existing cluster"""
    service = InsightsService()
    insights = service.get_cluster_insights("test-cluster-001")

    assert insights is not None
    assert insights["cluster_id"] == "test-cluster-001"
    assert insights["version"] == "4.15.2"
    assert insights["platform"] == "AWS"
    assert insights["install_type"] == "IPI"


def test_get_nonexistent_cluster():
    """Test fetching insights for a cluster that doesn't exist"""
    service = InsightsService()
    insights = service.get_cluster_insights("nonexistent-cluster")

    assert insights is None


def test_get_all_cluster_ids():
    """Test retrieving all available cluster IDs"""
    service = InsightsService()
    cluster_ids = service.get_all_cluster_ids()

    assert isinstance(cluster_ids, list)
    assert len(cluster_ids) > 0
    assert "test-cluster-001" in cluster_ids


def test_rosa_cluster():
    """Test fetching a ROSA cluster"""
    service = InsightsService()
    insights = service.get_cluster_insights("rosa-cluster-99")

    assert insights is not None
    assert insights["install_type"] == "ROSA"
    assert insights["managed"] is True


def test_degraded_cluster():
    """Test fetching a cluster with alerts"""
    service = InsightsService()
    insights = service.get_cluster_insights("prod-cluster-042")

    assert insights is not None
    assert insights["health_status"] == "Degraded"
    assert len(insights["alerts"]) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
