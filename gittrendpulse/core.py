"""
核心分析引擎模块
提供GitHub趋势数据的多维度分析功能
"""

import math
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
from collections import defaultdict

from .github_api import GitHubAPI


class TrendAnalyzer:
    """GitHub趋势分析引擎"""
    
    def __init__(self, github_api: GitHubAPI):
        """
        初始化趋势分析器
        
        Args:
            github_api: GitHub API客户端实例
        """
        self.api = github_api
    
    def analyze_repository_health(self, owner: str, repo: str) -> Dict[str, Any]:
        """
        分析仓库健康度
        
        Args:
            owner: 仓库所有者
            repo: 仓库名称
            
        Returns:
            健康度分析报告
        """
        try:
            details = self.api.get_repository_details(owner, repo)
        except Exception as e:
            return {"error": str(e)}
        
        # 基础指标
        stars = details.get("stargazers_count", 0)
        forks = details.get("forks_count", 0)
        open_issues = details.get("open_issues_count", 0)
        watchers = details.get("watchers_count", 0)
        
        # 计算健康度评分 (0-100)
        health_score = self._calculate_health_score(details)
        
        # 活跃度分析
        created_at = datetime.fromisoformat(details.get("created_at", "").replace("Z", "+00:00"))
        updated_at = datetime.fromisoformat(details.get("updated_at", "").replace("Z", "+00:00"))
        pushed_at = datetime.fromisoformat(details.get("pushed_at", "").replace("Z", "+00:00")) if details.get("pushed_at") else None
        
        days_since_update = (datetime.now() - updated_at.replace(tzinfo=None)).days
        days_since_push = (datetime.now() - pushed_at.replace(tzinfo=None)).days if pushed_at else None
        
        # Issue分析
        issue_ratio = open_issues / (stars + 1) * 1000  # 每1000 star的open issue数
        
        return {
            "name": f"{owner}/{repo}",
            "health_score": health_score,
            "metrics": {
                "stars": stars,
                "forks": forks,
                "open_issues": open_issues,
                "watchers": watchers,
                "issue_ratio": round(issue_ratio, 2),
            },
            "activity": {
                "days_since_update": days_since_update,
                "days_since_push": days_since_push,
                "is_active": days_since_push <= 30 if days_since_push else False,
                "is_very_active": days_since_push <= 7 if days_since_push else False,
            },
            "metadata": {
                "description": details.get("description", ""),
                "language": details.get("language", "Unknown"),
                "license": details.get("license", {}).get("name", "No License") if details.get("license") else "No License",
                "topics": details.get("topics", []),
                "homepage": details.get("homepage", ""),
            }
        }
    
    def _calculate_health_score(self, details: Dict) -> int:
        """
        计算仓库健康度评分
        
        Args:
            details: 仓库详细信息
            
        Returns:
            健康度评分 (0-100)
        """
        score = 50  # 基础分
        
        # Star数量评分
        stars = details.get("stargazers_count", 0)
        if stars >= 10000:
            score += 15
        elif stars >= 1000:
            score += 10
        elif stars >= 100:
            score += 5
        
        # Fork活跃度
        forks = details.get("forks_count", 0)
        if forks > 0 and stars > 0:
            fork_ratio = forks / stars
            if fork_ratio > 0.3:
                score += 10
            elif fork_ratio > 0.1:
                score += 5
        
        # 更新活跃度
        pushed_at = details.get("pushed_at")
        if pushed_at:
            pushed_date = datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))
            days_since_push = (datetime.now() - pushed_date.replace(tzinfo=None)).days
            if days_since_push <= 7:
                score += 15
            elif days_since_push <= 30:
                score += 10
            elif days_since_push <= 90:
                score += 5
        
        # 文档完善度
        if details.get("description"):
            score += 5
        if details.get("homepage"):
            score += 5
        
        # 开源协议
        if details.get("license"):
            score += 5
        
        return min(100, max(0, score))
    
    def analyze_trending_patterns(
        self, 
        repositories: List[Dict]
    ) -> Dict[str, Any]:
        """
        分析趋势仓库的模式和特征
        
        Args:
            repositories: 趋势仓库列表
            
        Returns:
            趋势模式分析报告
        """
        if not repositories:
            return {"error": "No repositories to analyze"}
        
        # 语言分布
        language_dist = defaultdict(int)
        topic_dist = defaultdict(int)
        
        total_stars = 0
        total_forks = 0
        
        for repo in repositories:
            lang = repo.get("language") or "Unknown"
            language_dist[lang] += 1
            
            topics = repo.get("topics", [])
            for topic in topics:
                topic_dist[topic] += 1
            
            total_stars += repo.get("stargazers_count", 0)
            total_forks += repo.get("forks_count", 0)
        
        # 计算平均指标
        avg_stars = total_stars / len(repositories) if repositories else 0
        avg_forks = total_forks / len(repositories) if repositories else 0
        
        # 热门语言排序
        top_languages = sorted(
            language_dist.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:10]
        
        # 热门主题排序
        top_topics = sorted(
            topic_dist.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:10]
        
        return {
            "summary": {
                "total_repos": len(repositories),
                "total_stars": total_stars,
                "total_forks": total_forks,
                "avg_stars": round(avg_stars, 1),
                "avg_forks": round(avg_forks, 1),
            },
            "language_distribution": [
                {"language": lang, "count": count, "percentage": round(count/len(repositories)*100, 1)}
                for lang, count in top_languages
            ],
            "topic_trends": [
                {"topic": topic, "count": count}
                for topic, count in top_topics
            ],
        }
    
    def calculate_growth_velocity(
        self, 
        owner: str, 
        repo: str,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        计算仓库增长速率
        
        Args:
            owner: 仓库所有者
            repo: 仓库名称
            days: 分析时间范围(天)
            
        Returns:
            增长速率分析
        """
        try:
            details = self.api.get_repository_details(owner, repo)
        except Exception as e:
            return {"error": str(e)}
        
        created_at = datetime.fromisoformat(details.get("created_at", "").replace("Z", "+00:00"))
        repo_age_days = (datetime.now() - created_at.replace(tzinfo=None)).days
        
        stars = details.get("stargazers_count", 0)
        forks = details.get("forks_count", 0)
        
        # 计算日均增长
        daily_star_growth = stars / max(repo_age_days, 1)
        daily_fork_growth = forks / max(repo_age_days, 1)
        
        # 增长评级
        growth_rating = "🚀 Explosive" if daily_star_growth > 50 else \
                       "🔥 Hot" if daily_star_growth > 10 else \
                       "📈 Steady" if daily_star_growth > 1 else \
                       "🌱 Growing"
        
        return {
            "repository": f"{owner}/{repo}",
            "age_days": repo_age_days,
            "growth_metrics": {
                "total_stars": stars,
                "total_forks": forks,
                "daily_star_growth": round(daily_star_growth, 2),
                "daily_fork_growth": round(daily_fork_growth, 2),
            },
            "growth_rating": growth_rating,
            "projected_30d": {
                "stars": round(daily_star_growth * 30),
                "forks": round(daily_fork_growth * 30),
            }
        }
    
    def compare_repositories(
        self, 
        repos: List[Tuple[str, str]]
    ) -> List[Dict[str, Any]]:
        """
        对比多个仓库的指标
        
        Args:
            repos: 仓库列表，格式为 [(owner, repo), ...]
            
        Returns:
            对比分析结果
        """
        results = []
        
        for owner, repo in repos:
            try:
                health = self.analyze_repository_health(owner, repo)
                velocity = self.calculate_growth_velocity(owner, repo)
                
                results.append({
                    "repository": f"{owner}/{repo}",
                    "health": health,
                    "velocity": velocity,
                })
            except Exception as e:
                results.append({
                    "repository": f"{owner}/{repo}",
                    "error": str(e)
                })
        
        # 按健康度排序
        results.sort(
            key=lambda x: x.get("health", {}).get("health_score", 0), 
            reverse=True
        )
        
        return results
    
    def detect_emerging_trends(
        self,
        language: Optional[str] = None,
        min_stars: int = 50
    ) -> List[Dict[str, Any]]:
        """
        检测新兴趋势项目
        
        Args:
            language: 编程语言筛选
            min_stars: 最小Star数
            
        Returns:
            新兴趋势项目列表
        """
        # 获取最近一周创建的优质项目
        query_parts = [
            f"stars:>{min_stars}",
            "created:>" + (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        ]
        if language:
            query_parts.append(f"language:{language}")
        
        query = " ".join(query_parts)
        
        try:
            repos = self.api.search_repositories(
                query=query,
                sort="stars",
                order="desc",
                per_page=30
            )
        except Exception as e:
            return [{"error": str(e)}]
        
        # 分析每个项目的增长潜力
        emerging = []
        for repo in repos:
            created_at = datetime.fromisoformat(
                repo.get("created_at", "").replace("Z", "+00:00")
            )
            age_hours = (datetime.now() - created_at.replace(tzinfo=None)).total_seconds() / 3600
            stars = repo.get("stargazers_count", 0)
            
            # 计算每小时增长速度
            hourly_growth = stars / max(age_hours, 1)
            
            # 潜力评级
            potential = "🔥 High" if hourly_growth > 10 else \
                       "📈 Medium" if hourly_growth > 1 else \
                       "🌱 Low"
            
            emerging.append({
                "name": repo.get("full_name"),
                "description": repo.get("description", ""),
                "stars": stars,
                "forks": repo.get("forks_count", 0),
                "language": repo.get("language", "Unknown"),
                "age_hours": round(age_hours, 1),
                "hourly_growth": round(hourly_growth, 2),
                "potential": potential,
                "url": repo.get("html_url"),
            })
        
        return sorted(emerging, key=lambda x: x["hourly_growth"], reverse=True)
