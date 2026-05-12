"""
GitHub API 客户端模块
提供GitHub Trending和Repository数据的获取功能
"""

import urllib.request
import urllib.error
import json
import ssl
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta


class GitHubAPI:
    """GitHub API 客户端"""
    
    BASE_URL = "https://api.github.com"
    TRENDING_URL = "https://github.com/trending"
    
    def __init__(self, token: Optional[str] = None):
        """
        初始化GitHub API客户端
        
        Args:
            token: GitHub Personal Access Token (可选，用于提高API限制)
        """
        self.token = token
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitTrendPulse/1.0.0"
        }
        if token:
            self.headers["Authorization"] = f"Bearer {token}"
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """
        发送HTTP请求到GitHub API
        
        Args:
            endpoint: API端点路径
            params: 查询参数
            
        Returns:
            API响应的JSON数据
        """
        url = f"{self.BASE_URL}{endpoint}"
        if params:
            query_string = "&".join([f"{k}={v}" for k, v in params.items()])
            url = f"{url}?{query_string}"
        
        req = urllib.request.Request(url, headers=self.headers)
        
        # 创建SSL上下文，处理证书验证
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        try:
            with urllib.request.urlopen(req, context=ssl_context, timeout=30) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            raise Exception(f"GitHub API错误: {e.code} - {error_body}")
        except Exception as e:
            raise Exception(f"请求失败: {str(e)}")
    
    def search_repositories(
        self, 
        query: str, 
        sort: str = "stars", 
        order: str = "desc",
        per_page: int = 30,
        page: int = 1
    ) -> List[Dict]:
        """
        搜索GitHub仓库
        
        Args:
            query: 搜索查询
            sort: 排序方式 (stars, forks, updated)
            order: 排序顺序 (asc, desc)
            per_page: 每页结果数
            page: 页码
            
        Returns:
            仓库列表
        """
        params = {
            "q": query,
            "sort": sort,
            "order": order,
            "per_page": per_page,
            "page": page
        }
        
        response = self._make_request("/search/repositories", params)
        return response.get("items", [])
    
    def get_trending_repositories(
        self, 
        language: Optional[str] = None,
        since: str = "daily",
        per_page: int = 30
    ) -> List[Dict]:
        """
        获取趋势仓库（通过搜索最近创建的优质仓库模拟）
        
        Args:
            language: 编程语言筛选
            since: 时间范围 (daily, weekly, monthly)
            per_page: 返回数量
            
        Returns:
            趋势仓库列表
        """
        # 根据时间范围构建查询
        date_ranges = {
            "daily": "created:>" + (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
            "weekly": "created:>" + (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
            "monthly": "created:>" + (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        }
        
        query_parts = [date_ranges.get(since, date_ranges["weekly"]), "stars:>10"]
        if language:
            query_parts.append(f"language:{language}")
        
        query = " ".join(query_parts)
        
        return self.search_repositories(
            query=query,
            sort="stars",
            order="desc",
            per_page=per_page
        )
    
    def get_repository_details(self, owner: str, repo: str) -> Dict:
        """
        获取仓库详细信息
        
        Args:
            owner: 仓库所有者
            repo: 仓库名称
            
        Returns:
            仓库详细信息
        """
        return self._make_request(f"/repos/{owner}/{repo}")
    
    def get_repository_languages(self, owner: str, repo: str) -> Dict[str, int]:
        """
        获取仓库使用的编程语言
        
        Args:
            owner: 仓库所有者
            repo: 仓库名称
            
        Returns:
            语言及其代码字节数的字典
        """
        return self._make_request(f"/repos/{owner}/{repo}/languages")
    
    def get_repository_commits(
        self, 
        owner: str, 
        repo: str, 
        per_page: int = 100
    ) -> List[Dict]:
        """
        获取仓库最近的提交记录
        
        Args:
            owner: 仓库所有者
            repo: 仓库名称
            per_page: 返回数量
            
        Returns:
            提交记录列表
        """
        params = {"per_page": per_page}
        return self._make_request(f"/repos/{owner}/{repo}/commits", params)
    
    def get_repository_issues(
        self, 
        owner: str, 
        repo: str, 
        state: str = "all",
        per_page: int = 100
    ) -> List[Dict]:
        """
        获取仓库的Issues
        
        Args:
            owner: 仓库所有者
            repo: 仓库名称
            state: Issue状态 (open, closed, all)
            per_page: 返回数量
            
        Returns:
            Issues列表
        """
        params = {"state": state, "per_page": per_page}
        return self._make_request(f"/repos/{owner}/{repo}/issues", params)
    
    def get_rate_limit(self) -> Dict:
        """
        获取当前API速率限制状态
        
        Returns:
            速率限制信息
        """
        return self._make_request("/rate_limit")
    
    def get_user_repositories(
        self, 
        username: str, 
        per_page: int = 100,
        page: int = 1
    ) -> List[Dict]:
        """
        获取用户的所有仓库
        
        Args:
            username: GitHub用户名
            per_page: 每页数量
            page: 页码
            
        Returns:
            仓库列表
        """
        params = {"per_page": per_page, "page": page}
        return self._make_request(f"/users/{username}/repos", params)
