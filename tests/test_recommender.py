"""
推荐引擎模块测试
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gittrendpulse.recommender import AIRecommender


class TestAIRecommender(unittest.TestCase):
    """测试 AIRecommender 类"""
    
    def setUp(self):
        """测试前准备"""
        self.recommender = AIRecommender()
    
    def test_recommend_projects_empty(self):
        """测试空列表推荐"""
        result = self.recommender.recommend_projects([])
        self.assertEqual(result, [])
    
    def test_recommend_projects_with_data(self):
        """测试有数据的推荐"""
        repos = [
            {
                "full_name": "user/repo1",
                "description": "A machine learning library",
                "stargazers_count": 5000,
                "forks_count": 1000,
                "topics": ["machine-learning", "python"],
                "language": "Python",
                "created_at": "2025-05-01T00:00:00Z",
                "license": {"spdx_id": "MIT"}
            },
            {
                "full_name": "user/repo2",
                "description": "Web framework",
                "stargazers_count": 100,
                "forks_count": 10,
                "topics": ["web", "javascript"],
                "language": "JavaScript",
                "created_at": "2024-01-01T00:00:00Z",
                "license": None
            }
        ]
        
        result = self.recommender.recommend_projects(
            repositories=repos,
            user_interests=["machine-learning", "python"],
            top_n=2
        )
        
        self.assertEqual(len(result), 2)
        # 第一个应该是ML项目，评分更高
        self.assertGreater(result[0]["score"], result[1]["score"])
    
    def test_generate_trend_insights(self):
        """测试生成趋势洞察"""
        trend_data = {
            "summary": {"total_repos": 30, "avg_stars": 1500},
            "language_distribution": [
                {"language": "Python", "percentage": 40},
                {"language": "JavaScript", "percentage": 30}
            ],
            "topic_trends": [
                {"topic": "ai", "count": 15},
                {"topic": "ml", "count": 10}
            ]
        }
        
        insights = self.recommender.generate_trend_insights(trend_data)
        
        self.assertTrue(len(insights) > 0)
        self.assertIn("Python", insights[0])
    
    def test_predict_project_potential(self):
        """测试项目潜力预测"""
        repo_high = {"stargazers_count": 10000, "forks_count": 3000}
        repo_low = {"stargazers_count": 50, "forks_count": 5}
        
        pred_high = self.recommender.predict_project_potential(repo_high)
        pred_low = self.recommender.predict_project_potential(repo_low)
        
        self.assertIn("爆发", pred_high["short_term"]["rating"])
        self.assertIn("早期", pred_low["short_term"]["rating"])


if __name__ == "__main__":
    unittest.main()
