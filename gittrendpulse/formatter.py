"""
输出格式化模块
提供多种格式的结果输出
"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime


class OutputFormatter:
    """输出格式化器"""
    
    # 颜色代码
    COLORS = {
        "reset": "\033[0m",
        "bold": "\033[1m",
        "dim": "\033[2m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "bright_red": "\033[91m",
        "bright_green": "\033[92m",
        "bright_yellow": "\033[93m",
        "bright_blue": "\033[94m",
    }
    
    def __init__(self, use_color: bool = True):
        """
        初始化格式化器
        
        Args:
            use_color: 是否使用颜色输出
        """
        self.use_color = use_color
    
    def _color(self, text: str, color: str) -> str:
        """
        为文本添加颜色
        
        Args:
            text: 文本内容
            color: 颜色名称
            
        Returns:
            带颜色的文本
        """
        if not self.use_color:
            return text
        return f"{self.COLORS.get(color, '')}{text}{self.COLORS['reset']}"
    
    def format_trending_table(self, repositories: List[Dict]) -> str:
        """
        格式化趋势仓库为表格
        
        Args:
            repositories: 仓库列表
            
        Returns:
            格式化的表格字符串
        """
        if not repositories:
            return self._color("暂无数据", "yellow")
        
        lines = []
        lines.append("")
        lines.append(self._color("╔" + "═" * 78 + "╗", "cyan"))
        lines.append(self._color("║" + "📊 GitHub 趋势仓库".center(76) + "║", "cyan"))
        lines.append(self._color("╠" + "═" * 78 + "╣", "cyan"))
        
        header = f"{'排名':<4} {'仓库':<30} {'语言':<12} {'⭐ Stars':<10} {'🍴 Forks':<10}"
        lines.append(self._color("║ " + header + " ║", "bold"))
        lines.append(self._color("╠" + "═" * 78 + "╣", "cyan"))
        
        for i, repo in enumerate(repositories[:20], 1):
            name = repo.get("full_name", "Unknown")[:28]
            lang = (repo.get("language") or "N/A")[:10]
            stars = repo.get("stargazers_count", 0)
            forks = repo.get("forks_count", 0)
            
            # 排名颜色
            rank_color = "bright_yellow" if i <= 3 else "white"
            
            row = f"{self._color(f'#{i}', rank_color):<4} {name:<30} {lang:<12} {stars:<10,} {forks:<10,}"
            lines.append("║ " + row + " ║")
        
        lines.append(self._color("╚" + "═" * 78 + "╝", "cyan"))
        lines.append("")
        
        return "\n".join(lines)
    
    def format_health_report(self, health_data: Dict) -> str:
        """
        格式化健康度报告
        
        Args:
            health_data: 健康度分析数据
            
        Returns:
            格式化的报告字符串
        """
        if "error" in health_data:
            return self._color(f"❌ 错误: {health_data['error']}", "red")
        
        lines = []
        lines.append("")
        lines.append(self._color("╔" + "═" * 58 + "╗", "green"))
        lines.append(self._color("║" + "🏥 仓库健康度报告".center(56) + "║", "green"))
        lines.append(self._color("╠" + "═" * 58 + "╣", "green"))
        
        # 仓库名称
        name = health_data.get("name", "Unknown")
        lines.append(f"║ {self._color('📦 仓库:', 'bold')} {name:<45} ║")
        
        # 健康度评分
        score = health_data.get("health_score", 0)
        score_color = "bright_green" if score >= 80 else "yellow" if score >= 60 else "red"
        score_bar = self._render_progress_bar(score, 50)
        lines.append(f"║ {self._color('💯 健康度:', 'bold')} {self._color(score_bar, score_color)} {score}/100 ║")
        
        lines.append(self._color("╠" + "═" * 58 + "╣", "green"))
        
        # 指标
        metrics = health_data.get("metrics", {})
        lines.append(f"║ {self._color('📈 核心指标', 'bold'):<54} ║")
        lines.append(f"║   ⭐ Stars: {metrics.get('stars', 0):<10,}                                  ║")
        lines.append(f"║   🍴 Forks: {metrics.get('forks', 0):<10,}                                  ║")
        lines.append(f"║   📋 Open Issues: {metrics.get('open_issues', 0):<10,}                          ║")
        lines.append(f"║   👀 Watchers: {metrics.get('watchers', 0):<10,}                            ║")
        
        lines.append(self._color("╠" + "═" * 58 + "╣", "green"))
        
        # 活跃度
        activity = health_data.get("activity", {})
        lines.append(f"║ {self._color('⚡ 活跃度', 'bold'):<54} ║")
        
        is_active = activity.get("is_active", False)
        is_very_active = activity.get("is_very_active", False)
        status = "🔥 非常活跃" if is_very_active else "✅ 活跃" if is_active else "😴 不活跃"
        lines.append(f"║   状态: {status:<47} ║")
        
        days_push = activity.get("days_since_push")
        if days_push is not None:
            lines.append(f"║   上次提交: {days_push} 天前{'':<39} ║")
        
        lines.append(self._color("╚" + "═" * 58 + "╝", "green"))
        lines.append("")
        
        return "\n".join(lines)
    
    def _render_progress_bar(self, value: int, width: int = 20) -> str:
        """
        渲染进度条
        
        Args:
            value: 当前值 (0-100)
            width: 进度条宽度
            
        Returns:
            进度条字符串
        """
        filled = int(value / 100 * width)
        bar = "█" * filled + "░" * (width - filled)
        return bar
    
    def format_recommendations(self, recommendations: List[Dict]) -> str:
        """
        格式化推荐列表
        
        Args:
            recommendations: 推荐项目列表
            
        Returns:
            格式化的推荐字符串
        """
        if not recommendations:
            return self._color("暂无推荐项目", "yellow")
        
        lines = []
        lines.append("")
        lines.append(self._color("╔" + "═" * 78 + "╗", "magenta"))
        lines.append(self._color("║" + "🎯 AI智能推荐".center(76) + "║", "magenta"))
        lines.append(self._color("╚" + "═" * 78 + "╝", "magenta"))
        lines.append("")
        
        for i, rec in enumerate(recommendations[:10], 1):
            repo = rec.get("repository", {})
            score = rec.get("score", 0)
            reasons = rec.get("reasons", [])
            
            name = repo.get("full_name", "Unknown")
            desc = (repo.get("description") or "暂无描述")[:60]
            stars = repo.get("stargazers_count", 0)
            lang = repo.get("language") or "N/A"
            
            # 推荐等级
            if score >= 80:
                badge = self._color("🔥 强烈推荐", "bright_red")
            elif score >= 60:
                badge = self._color("⭐ 推荐", "bright_yellow")
            else:
                badge = self._color("👍 值得一看", "green")
            
            lines.append(self._color(f"┌─ 推荐 #{i} {badge} (评分: {score})", "cyan"))
            lines.append(f"│ 📦 {self._color(name, 'bold')}")
            lines.append(f"│ 📝 {desc}")
            lines.append(f"│ 💻 {lang} | ⭐ {stars:,} Stars")
            
            if reasons:
                lines.append(f"│ 💡 推荐理由:")
                for reason in reasons:
                    lines.append(f"│    • {reason}")
            
            lines.append(self._color("└" + "─" * 76, "cyan"))
            lines.append("")
        
        return "\n".join(lines)
    
    def format_trend_analysis(self, analysis: Dict) -> str:
        """
        格式化趋势分析
        
        Args:
            analysis: 趋势分析数据
            
        Returns:
            格式化的分析字符串
        """
        if "error" in analysis:
            return self._color(f"❌ 错误: {analysis['error']}", "red")
        
        lines = []
        lines.append("")
        lines.append(self._color("╔" + "═" * 58 + "╗", "blue"))
        lines.append(self._color("║" + "📊 趋势分析报告".center(56) + "║", "blue"))
        lines.append(self._color("╚" + "═" * 58 + "╝", "blue"))
        lines.append("")
        
        # 摘要
        summary = analysis.get("summary", {})
        lines.append(self._color("📈 数据摘要", "bold"))
        lines.append(f"   总项目数: {summary.get('total_repos', 0)}")
        lines.append(f"   总Stars: {summary.get('total_stars', 0):,}")
        lines.append(f"   总Forks: {summary.get('total_forks', 0):,}")
        lines.append(f"   平均Stars: {summary.get('avg_stars', 0)}")
        lines.append("")
        
        # 语言分布
        lang_dist = analysis.get("language_distribution", [])
        if lang_dist:
            lines.append(self._color("💻 语言分布 TOP 5", "bold"))
            for lang in lang_dist[:5]:
                bar = self._render_progress_bar(lang.get("percentage", 0), 20)
                lines.append(f"   {lang.get('language', 'N/A'):<12} {bar} {lang.get('percentage', 0)}%")
            lines.append("")
        
        # 主题趋势
        topic_trends = analysis.get("topic_trends", [])
        if topic_trends:
            lines.append(self._color("🔥 热门主题 TOP 5", "bold"))
            for topic in topic_trends[:5]:
                lines.append(f"   #{topic.get('topic', 'N/A')} - {topic.get('count', 0)} 个项目")
            lines.append("")
        
        return "\n".join(lines)
    
    def format_json(self, data: Any) -> str:
        """
        格式化为JSON字符串
        
        Args:
            data: 要格式化的数据
            
        Returns:
            格式化的JSON字符串
        """
        return json.dumps(data, ensure_ascii=False, indent=2)
    
    def format_markdown(self, data: Dict, title: str = "GitTrendPulse Report") -> str:
        """
        格式化为Markdown报告
        
        Args:
            data: 报告数据
            title: 报告标题
            
        Returns:
            Markdown格式的报告
        """
        lines = []
        lines.append(f"# {title}")
        lines.append("")
        lines.append(f"*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        lines.append("")
        
        # 添加数据内容
        lines.append("## 数据详情")
        lines.append("")
        lines.append("```json")
        lines.append(json.dumps(data, ensure_ascii=False, indent=2))
        lines.append("```")
        lines.append("")
        
        lines.append("---")
        lines.append("*Generated by GitTrendPulse*")
        
        return "\n".join(lines)
    
    def format_emerging_trends(self, trends: List[Dict]) -> str:
        """
        格式化新兴趋势
        
        Args:
            trends: 新兴趋势列表
            
        Returns:
            格式化的字符串
        """
        if not trends:
            return self._color("暂无新兴趋势数据", "yellow")
        
        lines = []
        lines.append("")
        lines.append(self._color("╔" + "═" * 78 + "╗", "bright_yellow"))
        lines.append(self._color("║" + "🚀 新兴趋势项目 (近7天)".center(76) + "║", "bright_yellow"))
        lines.append(self._color("╚" + "═" * 78 + "╝", "bright_yellow"))
        lines.append("")
        
        for i, trend in enumerate(trends[:15], 1):
            name = trend.get("name", "Unknown")
            desc = (trend.get("description") or "暂无描述")[:50]
            stars = trend.get("stars", 0)
            growth = trend.get("hourly_growth", 0)
            potential = trend.get("potential", "🌱 Low")
            
            # 潜力颜色
            if "High" in potential:
                pot_color = "bright_red"
            elif "Medium" in potential:
                pot_color = "bright_yellow"
            else:
                pot_color = "green"
            
            lines.append(self._color(f"┌─ #{i} {potential}", pot_color))
            lines.append(f"│ 📦 {self._color(name, 'bold')}")
            lines.append(f"│ 📝 {desc}")
            lines.append(f"│ ⭐ {stars:,} | 📈 {growth}/小时")
            lines.append(self._color("└" + "─" * 76, "bright_yellow"))
            lines.append("")
        
        return "\n".join(lines)
