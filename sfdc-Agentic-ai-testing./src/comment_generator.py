"""
AI-Powered Comment Generator
Uses Claude API to format cluster insights into support-friendly comments
"""
import logging
from typing import Dict, Optional
from anthropic import Anthropic

logger = logging.getLogger(__name__)


class CommentGenerator:
    """Generate formatted internal comments using Claude API"""

    def __init__(self, api_key: str, include_support_tips: bool = True):
        """
        Initialize comment generator

        Args:
            api_key: Anthropic API key
            include_support_tips: Whether to include AI-generated support tips
        """
        self.client = Anthropic(api_key=api_key)
        self.include_support_tips = include_support_tips

    def generate_comment(self, cluster_insights: Dict, comment_prefix: str = "") -> str:
        """
        Generate formatted comment from cluster insights

        Args:
            cluster_insights: Dictionary containing cluster data
            comment_prefix: Optional prefix for the comment

        Returns:
            Formatted comment string
        """
        if not cluster_insights:
            logger.warning("No cluster insights provided")
            return self._generate_no_data_comment(comment_prefix)

        try:
            # Construct the prompt for Claude
            prompt = self._build_prompt(cluster_insights)

            # Call Claude API with prompt caching
            response = self.client.messages.create(
                model="claude-sonnet-4-5@20250929",
                max_tokens=1024,
                system=[
                    {
                        "type": "text",
                        "text": "You are an expert OpenShift support assistant. Format cluster insights into clear, actionable internal comments for support engineers.",
                        "cache_control": {"type": "ephemeral"}
                    }
                ],
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            comment_body = response.content[0].text

            # Add prefix if provided
            if comment_prefix:
                comment_body = f"{comment_prefix}\n\n{comment_body}"

            logger.info("Successfully generated comment using Claude API")
            return comment_body

        except Exception as e:
            logger.error(f"Error generating comment with Claude API: {e}")
            return self._generate_fallback_comment(cluster_insights, comment_prefix)

    def _build_prompt(self, insights: Dict) -> str:
        """Build the prompt for Claude"""
        support_tips_instruction = ""
        if self.include_support_tips:
            support_tips_instruction = """

Include a **Support Tips** section with 2-3 actionable recommendations based on:
- Cluster version (check for known issues, upgrade path)
- Platform type (AWS/Azure/BareMetal specific considerations)
- Installation type (IPI/UPI/ROSA/ARO/Assisted specific features)
- Health status (especially if degraded or alerts present)
"""

        prompt = f"""Format the following OpenShift cluster insights into a clear internal comment for a support engineer.

Cluster Data:
{self._format_insights_for_prompt(insights)}

Requirements:
1. Use clear markdown formatting with headers and bullet points
2. Start with a **Cluster Overview** section with key details
3. Include a **Current Status** section highlighting health and any alerts
4. Use emojis sparingly for visual clarity (✅ for healthy, ⚠️ for warnings)
5. Keep it concise but informative{support_tips_instruction}

Format the comment professionally and make it easy to scan quickly."""

        return prompt

    def _format_insights_for_prompt(self, insights: Dict) -> str:
        """Format insights dictionary as readable text for the prompt"""
        lines = []
        for key, value in insights.items():
            if key == "alerts" and isinstance(value, list):
                lines.append(f"- {key}: {len(value)} alert(s)")
                for alert in value:
                    lines.append(f"  - {alert.get('severity', 'info')}: {alert.get('message', 'N/A')}")
            else:
                lines.append(f"- {key}: {value}")
        return "\n".join(lines)

    def _generate_fallback_comment(self, insights: Dict, prefix: str = "") -> str:
        """Generate a simple formatted comment without AI (fallback)"""
        health_emoji = "✅" if insights.get("health_status") == "Healthy" else "⚠️"

        lines = []
        if prefix:
            lines.append(prefix)
            lines.append("")

        lines.extend([
            "**OpenShift Cluster Overview**",
            "",
            f"**Cluster ID:** {insights.get('cluster_id', 'N/A')}",
            f"**Version:** {insights.get('version', 'N/A')}",
            f"**Platform:** {insights.get('platform', 'N/A')}",
            f"**Installation Type:** {insights.get('install_type', 'N/A')}",
            f"**Region:** {insights.get('region', 'N/A')}",
            f"**Node Count:** {insights.get('node_count', 'N/A')} ({insights.get('control_plane_nodes', 'N/A')} control, {insights.get('worker_nodes', 'N/A')} workers)",
            f"**Health Status:** {health_emoji} {insights.get('health_status', 'Unknown')}",
            "",
        ])

        # Add alerts if present
        alerts = insights.get('alerts', [])
        if alerts:
            lines.append("**Active Alerts:**")
            for alert in alerts:
                lines.append(f"- {alert.get('severity', 'info').upper()}: {alert.get('message', 'N/A')}")
            lines.append("")

        lines.append(f"*Last Updated: {insights.get('last_updated', 'N/A')}*")

        return "\n".join(lines)

    def _generate_no_data_comment(self, prefix: str = "") -> str:
        """Generate comment when no cluster data is available"""
        lines = []
        if prefix:
            lines.append(prefix)
            lines.append("")

        lines.extend([
            "**OpenShift Cluster Insights**",
            "",
            "⚠️ No cluster insights data found for this cluster ID.",
            "",
            "Please verify:",
            "- The cluster ID is correct",
            "- The cluster is registered in the insights system",
            "- The cluster has sent recent telemetry data"
        ])

        return "\n".join(lines)


# Standalone test
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    import json

    load_dotenv("config/.env")

    logging.basicConfig(level=logging.INFO)

    # Sample cluster data
    test_insights = {
        "cluster_id": "test-cluster-001",
        "version": "4.15.2",
        "platform": "AWS",
        "install_type": "IPI",
        "region": "us-east-1",
        "node_count": 5,
        "control_plane_nodes": 3,
        "worker_nodes": 2,
        "health_status": "Healthy",
        "alerts": [],
        "last_updated": "2026-06-01T10:00:00Z"
    }

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("✗ ANTHROPIC_API_KEY not found in .env file")
        print("Testing fallback comment generation...")
        generator = CommentGenerator(api_key="dummy")
        comment = generator._generate_fallback_comment(
            test_insights,
            "🔍 OpenShift Cluster Insights - Auto-Generated"
        )
        print("\n" + "="*60)
        print(comment)
        print("="*60)
    else:
        generator = CommentGenerator(api_key=api_key, include_support_tips=True)
        print("Generating AI-powered comment...")
        comment = generator.generate_comment(
            test_insights,
            "🔍 OpenShift Cluster Insights - Auto-Generated"
        )
        print("\n" + "="*60)
        print(comment)
        print("="*60)
