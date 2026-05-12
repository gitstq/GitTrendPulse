"""
核心分析模块测试
"""

import unittest
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gittrendpulse.core import TrendAnalyzer
from gittrendpulse.github_api import GitHubAPI


class TestTrendAnalyzer(unittest.TestCase):
    """测试 TrendAnalyzer 类"""
    
    def setUp(self):
        """测试前准备"""
        self.mock_api = MagicMock(spec=GitHubAPI)
        self.analyzer = TrendAnalyzer(self.mock_api)
    
    def test_calculate_health_score_high(self):
        """测试高健康度评分"""
        details = {
            "stargazers_count": 15000,
            "forks_count": 5000,
            "pushed_at": "2025-05-11T00:00:00Z",
            "description": "A great project",
            "homepage": "https://example.com",
            "license": {"name": "MIT License", "spdx_id": "MIT"}
        }
        
        score = self.analyzer._calculate_health_score(details)
        self.assertGreaterEqual(score, 80)
    
    def test_calculate_health_score_low(self):
        """测试低健康度评分"""
        details = {
            "stargazers_count": 10,
            "forks_count": 0,
            "pushed_at": "2024-01-01T00:00:00Z",
            "description": "",
            "homepage": None,
            "license": None
        }
        
        score = self.analyzer._calculate_health_score(details)
        self.assertLess(score, 60)
    
    def test_analyze_trending_patterns_empty(self):
        """测试空列表趋势分析"""
        result = self.analyzer.analyze_trending_patterns([])
        self.assertIn("error", result)
    
    def test_analyze_trending_patterns_with_data(self):
        """测试有数据的趋势分析"""
        repos = [
            {"language": "Python", "topics": ["ai", "ml"], "stargazers_count": 100, "forks_count": 20},
            {"language": "JavaScript", "topics": ["web", "frontend"], "stargazers_count": 200, "forks_count": 40},
            {"language": "Python", "topics": ["data"], "stargazers_count": 150, "forks_count": 30},
        ]
        
        result = self.analyzer.analyze_trending_patterns(repos)
        
        self.assertEqual(result["summary"]["total_repos"], 3)
        self.assertEqual(result["summary"]["total_stars"], 450)
        self.assertTrue(len(result["language_distribution"]) > 0)


if __name__ == "__main__":
    unittest.main()
