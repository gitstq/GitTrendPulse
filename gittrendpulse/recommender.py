"""
AI推荐引擎模块
基于规则和分析数据提供智能项目推荐
"""

import random
from typing import Dict, List, Optional, Any
from datetime import datetime
from collections import defaultdict


class AIRecommender:
    """AI驱动的项目推荐引擎"""
    
    # 技术领域关键词映射
    TECH_DOMAINS = {
        "ai_ml": ["machine-learning", "deep-learning", "ai", "neural-network", "llm", "gpt", "transformer", "pytorch", "tensorflow"],
        "web_dev": ["react", "vue", "angular", "frontend", "backend", "web", "javascript", "typescript", "html", "css"],
        "devops": ["docker", "kubernetes", "ci-cd", "devops", "terraform", "ansible", "deployment"],
        "data": ["data-science", "data-analysis", "pandas", "numpy", "visualization", "database", "sql"],
        "mobile": ["android", "ios", "flutter", "react-native", "mobile", "swift", "kotlin"],
        "security": ["security", "pentest", "vulnerability", "cryptography", "encryption", "auth"],
        "tools": ["cli", "tool", "utility", "automation", "productivity", "workflow"],
    }
    
    def __init__(self):
        """初始化推荐引擎"""
        self.user_preferences = {}
        self.interaction_history = []
    
    def recommend_projects(
        self,
        repositories: List[Dict],
        user_interests: Optional[List[str]] = None,
        top_n: int = 10
    ) -> List[Dict[str, Any]]:
        """
        基于用户兴趣和项目特征推荐项目
        
        Args:
            repositories: 候选项目列表
            user_interests: 用户感兴趣的技术领域
            top_n: 返回推荐数量
            
        Returns:
            推荐项目列表，包含推荐理由
        """
        if not repositories:
            return []
        
        scored_repos = []
        
        for repo in repositories:
            score = 0
            reasons = []
            
            # 基础质量分
            stars = repo.get("stargazers_count", 0)
            forks = repo.get("forks_count", 0)
            
            if stars >= 1000:
                score += 20
                reasons.append("⭐ 高Star数，社区认可度高")
            elif stars >= 100:
                score += 10
            
            # Fork活跃度
            if forks > 0 and stars > 0:
                fork_ratio = forks / stars
                if fork_ratio > 0.2:
                    score += 15
                    reasons.append("🍴 高Fork率，开发者参与活跃")
            
            # 兴趣匹配
            if user_interests:
                match_score, match_reasons = self._calculate_interest_match(repo, user_interests)
                score += match_score
                reasons.extend(match_reasons)
            
            # 增长潜力
            created_at = repo.get("created_at", "")
            if created_at:
                try:
                    from datetime import datetime
                    created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                    age_days = (datetime.now() - created.replace(tzinfo=None)).days
                    
                    if age_days <= 30 and stars >= 100:
                        score += 25
                        reasons.append("🚀 新兴项目，增长潜力巨大")
                    elif age_days <= 90 and stars >= 500:
                        score += 15
                        reasons.append("📈 近期热门，值得关注")
                except:
                    pass
            
            # 文档完善度
            if repo.get("description") and len(repo.get("description", "")) > 50:
                score += 5
                reasons.append("📝 文档描述清晰")
            
            # 开源协议加分
            license_info = repo.get("license")
            if license_info and license_info.get("spdx_id") in ["MIT", "Apache-2.0", "BSD-3-Clause"]:
                score += 5
                reasons.append("⚖️ 友好的开源协议")
            
            scored_repos.append({
                "repository": repo,
                "score": score,
                "reasons": reasons[:3],  # 只保留前3个理由
            })
        
        # 按分数排序
        scored_repos.sort(key=lambda x: x["score"], reverse=True)
        
        return scored_repos[:top_n]
    
    def _calculate_interest_match(
        self, 
        repo: Dict, 
        interests: List[str]
    ) -> tuple:
        """
        计算项目与用户兴趣的匹配度
        
        Args:
            repo: 仓库信息
            interests: 用户兴趣列表
            
        Returns:
            (匹配分数, 匹配理由列表)
        """
        score = 0
        reasons = []
        
        repo_topics = set(t.lower() for t in repo.get("topics", []))
        repo_lang = (repo.get("language") or "").lower()
        repo_desc = (repo.get("description") or "").lower()
        repo_name = (repo.get("name") or "").lower()
        
        for interest in interests:
            interest_lower = interest.lower()
            
            # 检查主题匹配
            if interest_lower in repo_topics:
                score += 15
                reasons.append(f"🏷️ 匹配你的兴趣: {interest}")
            
            # 检查语言匹配
            if interest_lower == repo_lang:
                score += 10
                reasons.append(f"💻 使用你感兴趣的{interest}语言")
            
            # 检查描述匹配
            if interest_lower in repo_desc:
                score += 8
            
            # 检查名称匹配
            if interest_lower in repo_name:
                score += 5
        
        return score, reasons
    
    def generate_trend_insights(self, trend_data: Dict) -> List[str]:
        """
        基于趋势数据生成洞察
        
        Args:
            trend_data: 趋势分析数据
            
        Returns:
            洞察文本列表
        """
        insights = []
        
        # 语言趋势洞察
        lang_dist = trend_data.get("language_distribution", [])
        if lang_dist:
            top_lang = lang_dist[0]
            insights.append(
                f"📊 **语言趋势**: {top_lang['language']} 占据主导地位，"
                f"占比 {top_lang['percentage']}%"
            )
            
            if len(lang_dist) >= 2:
                second_lang = lang_dist[1]
                insights.append(
                    f"🥈 **紧随其后**: {second_lang['language']} 以 {second_lang['percentage']}% 的占比"
                    f"成为第二大热门语言"
                )
        
        # 主题趋势洞察
        topic_trends = trend_data.get("topic_trends", [])
        if topic_trends:
            top_topics = [t["topic"] for t in topic_trends[:3]]
            insights.append(
                f"🔥 **热门主题**: {', '.join(top_topics)} 是当前最受关注的技术方向"
            )
        
        # 整体趋势
        summary = trend_data.get("summary", {})
        total_repos = summary.get("total_repos", 0)
        avg_stars = summary.get("avg_stars", 0)
        
        if avg_stars > 1000:
            insights.append(
                f"⭐ **明星项目**: 平均Star数高达 {avg_stars}，说明本期趋势项目质量极高"
            )
        elif avg_stars > 500:
            insights.append(
                f"✨ **优质项目**: 平均Star数 {avg_stars}，整体质量良好"
            )
        
        return insights
    
    def predict_project_potential(self, repo: Dict) -> Dict[str, Any]:
        """
        预测项目的发展潜力
        
        Args:
            repo: 仓库信息
            
        Returns:
            潜力预测报告
        """
        predictions = {
            "short_term": {"rating": "Unknown", "confidence": 0},
            "medium_term": {"rating": "Unknown", "confidence": 0},
            "long_term": {"rating": "Unknown", "confidence": 0},
        }
        
        stars = repo.get("stargazers_count", 0)
        forks = repo.get("forks_count", 0)
        
        # 基于当前指标预测
        if stars >= 5000:
            predictions["short_term"] = {"rating": "🚀 爆发", "confidence": 90}
            predictions["medium_term"] = {"rating": "📈 持续增长", "confidence": 80}
        elif stars >= 1000:
            predictions["short_term"] = {"rating": "📈 快速增长", "confidence": 75}
            predictions["medium_term"] = {"rating": "📊 稳步发展", "confidence": 65}
        elif stars >= 100:
            predictions["short_term"] = {"rating": "🌱 成长中", "confidence": 60}
            predictions["medium_term"] = {"rating": "📊 待观察", "confidence": 50}
        else:
            predictions["short_term"] = {"rating": "🌱 早期", "confidence": 40}
            predictions["medium_term"] = {"rating": "❓ 不确定", "confidence": 30}
        
        # Fork率影响长期预测
        if stars > 0:
            fork_rate = forks / stars
            if fork_rate > 0.3:
                predictions["long_term"] = {"rating": "🏆 生态潜力", "confidence": 75}
            elif fork_rate > 0.1:
                predictions["long_term"] = {"rating": "📊 稳定发展", "confidence": 60}
            else:
                predictions["long_term"] = {"rating": "📋 工具类", "confidence": 50}
        
        return predictions
    
    def suggest_learning_path(
        self,
        current_skills: List[str],
        target_domain: str
    ) -> List[Dict[str, Any]]:
        """
        基于当前技能和目标领域推荐学习路径
        
        Args:
            current_skills: 当前掌握的技能
            target_domain: 目标技术领域
            
        Returns:
            推荐学习路径
        """
        # 领域技能映射
        domain_skills = {
            "ai_ml": ["Python", "PyTorch", "TensorFlow", "NumPy", "Pandas", "Scikit-learn"],
            "web_dev": ["JavaScript", "TypeScript", "React", "Vue", "Node.js", "HTML/CSS"],
            "devops": ["Docker", "Kubernetes", "Terraform", "CI/CD", "AWS/Azure/GCP"],
            "data": ["SQL", "Python", "Pandas", "Data Visualization", "Statistics"],
            "mobile": ["Swift", "Kotlin", "Flutter", "React Native", "iOS/Android"],
            "security": ["Penetration Testing", "Cryptography", "Network Security", "OWASP"],
        }
        
        target_skills = domain_skills.get(target_domain, [])
        
        # 找出需要学习的技能
        skills_to_learn = [s for s in target_skills if s.lower() not in [c.lower() for c in current_skills]]
        
        # 构建学习路径
        path = []
        for i, skill in enumerate(skills_to_learn[:5], 1):
            path.append({
                "step": i,
                "skill": skill,
                "priority": "High" if i <= 2 else "Medium",
                "resources": [
                    f"GitHub搜索 '{skill} tutorial' 查找优质教程",
                    f"搜索 '{skill} best practices' 学习最佳实践",
                ]
            })
        
        return path
