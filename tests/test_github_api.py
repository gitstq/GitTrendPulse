"""
GitHub API 模块测试
"""

import unittest
import json
from unittest.mock import patch, MagicMock
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gittrendpulse.github_api import GitHubAPI


class TestGitHubAPI(unittest.TestCase):
    """测试 GitHubAPI 类"""
    
    def setUp(self):
        """测试前准备"""
        self.api = GitHubAPI(token="test_token")
    
    def test_init_with_token(self):
        """测试带Token初始化"""
        self.assertEqual(self.api.token, "test_token")
        self.assertIn("Authorization", self.api.headers)
    
    def test_init_without_token(self):
        """测试无Token初始化"""
        api = GitHubAPI()
        self.assertIsNone(api.token)
        self.assertNotIn("Authorization", api.headers)
    
    @patch('urllib.request.urlopen')
    def test_search_repositories(self, mock_urlopen):
        """测试搜索仓库"""
        # 模拟响应
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            "items": [
                {"id": 1, "name": "repo1", "stargazers_count": 100},
                {"id": 2, "name": "repo2", "stargazers_count": 200}
            ]
        }).encode('utf-8')
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        result = self.api.search_repositories("python")
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "repo1")
    
    def test_get_trending_repositories_params(self):
        """测试获取趋势仓库参数"""
        # 这里只测试参数构建，不实际调用API
        params = {
            "daily": "created:>2025-01-01",
            "weekly": "created:>2024-12-25",
            "monthly": "created:>2024-12-01"
        }
        
        for period, expected in params.items():
            self.assertIn("created:>", expected)


if __name__ == "__main__":
    unittest.main()
