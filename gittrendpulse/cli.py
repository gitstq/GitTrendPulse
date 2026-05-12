#!/usr/bin/env python3
"""
GitTrendPulse CLI - 主命令行接口
"""

import argparse
import sys
import os
from typing import Optional

from .github_api import GitHubAPI
from .core import TrendAnalyzer
from .recommender import AIRecommender
from .formatter import OutputFormatter


def create_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        prog="gittrendpulse",
        description="🚀 GitTrendPulse - AI驱动的GitHub趋势智能分析与洞察引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  gittrendpulse trending                    # 查看今日趋势
  gittrendpulse trending --language python  # 查看Python趋势
  gittrendpulse health owner/repo           # 分析仓库健康度
  gittrendpulse recommend --interests ai,web # 获取AI推荐
  gittrendpulse emerging                    # 发现新兴项目
  gittrendpulse compare repo1 repo2         # 对比多个仓库

更多信息: https://github.com/gitstq/GitTrendPulse
        """
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )
    
    parser.add_argument(
        "--token",
        help="GitHub Personal Access Token (可选，用于提高API限制)",
        default=os.environ.get("GITHUB_TOKEN")
    )
    
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="禁用颜色输出"
    )
    
    parser.add_argument(
        "--output",
        choices=["table", "json", "markdown"],
        default="table",
        help="输出格式 (默认: table)"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # trending 命令
    trending_parser = subparsers.add_parser(
        "trending",
        help="查看GitHub趋势仓库"
    )
    trending_parser.add_argument(
        "--language",
        help="按编程语言筛选 (如: python, javascript, go)"
    )
    trending_parser.add_argument(
        "--since",
        choices=["daily", "weekly", "monthly"],
        default="weekly",
        help="时间范围 (默认: weekly)"
    )
    trending_parser.add_argument(
        "--limit",
        type=int,
        default=30,
        help="返回结果数量 (默认: 30)"
    )
    
    # health 命令
    health_parser = subparsers.add_parser(
        "health",
        help="分析仓库健康度"
    )
    health_parser.add_argument(
        "repository",
        help="仓库名称 (格式: owner/repo)"
    )
    
    # recommend 命令
    recommend_parser = subparsers.add_parser(
        "recommend",
        help="获取AI智能推荐"
    )
    recommend_parser.add_argument(
        "--interests",
        help="感兴趣的技术领域，逗号分隔 (如: ai,python,web)"
    )
    recommend_parser.add_argument(
        "--language",
        help="按编程语言筛选"
    )
    recommend_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="推荐数量 (默认: 10)"
    )
    
    # emerging 命令
    emerging_parser = subparsers.add_parser(
        "emerging",
        help="发现新兴趋势项目"
    )
    emerging_parser.add_argument(
        "--language",
        help="按编程语言筛选"
    )
    emerging_parser.add_argument(
        "--min-stars",
        type=int,
        default=50,
        help="最小Star数 (默认: 50)"
    )
    
    # compare 命令
    compare_parser = subparsers.add_parser(
        "compare",
        help="对比多个仓库"
    )
    compare_parser.add_argument(
        "repositories",
        nargs="+",
        help="要对比的仓库列表 (格式: owner/repo)"
    )
    
    # analyze 命令
    analyze_parser = subparsers.add_parser(
        "analyze",
        help="分析趋势模式"
    )
    analyze_parser.add_argument(
        "--language",
        help="按编程语言筛选"
    )
    analyze_parser.add_argument(
        "--since",
        choices=["daily", "weekly", "monthly"],
        default="weekly",
        help="时间范围"
    )
    
    # velocity 命令
    velocity_parser = subparsers.add_parser(
        "velocity",
        help="分析仓库增长速率"
    )
    velocity_parser.add_argument(
        "repository",
        help="仓库名称 (格式: owner/repo)"
    )
    
    return parser


def handle_trending(args, api: GitHubAPI, formatter: OutputFormatter) -> int:
    """处理 trending 命令"""
    try:
        repos = api.get_trending_repositories(
            language=args.language,
            since=args.since,
            per_page=args.limit
        )
        
        if args.output == "json":
            print(formatter.format_json(repos))
        elif args.output == "markdown":
            print(formatter.format_markdown({"trending": repos}, "GitHub Trending"))
        else:
            print(formatter.format_trending_table(repos))
        
        return 0
    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        return 1


def handle_health(args, api: GitHubAPI, formatter: OutputFormatter) -> int:
    """处理 health 命令"""
    try:
        parts = args.repository.split("/")
        if len(parts) != 2:
            print("❌ 错误: 仓库名称格式应为 'owner/repo'", file=sys.stderr)
            return 1
        
        owner, repo = parts
        analyzer = TrendAnalyzer(api)
        health = analyzer.analyze_repository_health(owner, repo)
        
        if args.output == "json":
            print(formatter.format_json(health))
        elif args.output == "markdown":
            print(formatter.format_markdown(health, f"Health Report: {owner}/{repo}"))
        else:
            print(formatter.format_health_report(health))
        
        return 0
    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        return 1


def handle_recommend(args, api: GitHubAPI, formatter: OutputFormatter) -> int:
    """处理 recommend 命令"""
    try:
        # 获取趋势仓库作为候选
        repos = api.get_trending_repositories(
            language=args.language,
            since="weekly",
            per_page=50
        )
        
        # 解析兴趣
        interests = None
        if args.interests:
            interests = [i.strip() for i in args.interests.split(",")]
        
        # 生成推荐
        recommender = AIRecommender()
        recommendations = recommender.recommend_projects(
            repositories=repos,
            user_interests=interests,
            top_n=args.limit
        )
        
        if args.output == "json":
            print(formatter.format_json(recommendations))
        elif args.output == "markdown":
            print(formatter.format_markdown({"recommendations": recommendations}, "AI Recommendations"))
        else:
            print(formatter.format_recommendations(recommendations))
        
        return 0
    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        return 1


def handle_emerging(args, api: GitHubAPI, formatter: OutputFormatter) -> int:
    """处理 emerging 命令"""
    try:
        analyzer = TrendAnalyzer(api)
        trends = analyzer.detect_emerging_trends(
            language=args.language,
            min_stars=args.min_stars
        )
        
        if args.output == "json":
            print(formatter.format_json(trends))
        elif args.output == "markdown":
            print(formatter.format_markdown({"emerging_trends": trends}, "Emerging Trends"))
        else:
            print(formatter.format_emerging_trends(trends))
        
        return 0
    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        return 1


def handle_compare(args, api: GitHubAPI, formatter: OutputFormatter) -> int:
    """处理 compare 命令"""
    try:
        repos = []
        for repo_str in args.repositories:
            parts = repo_str.split("/")
            if len(parts) != 2:
                print(f"❌ 错误: 仓库名称 '{repo_str}' 格式应为 'owner/repo'", file=sys.stderr)
                return 1
            repos.append((parts[0], parts[1]))
        
        analyzer = TrendAnalyzer(api)
        comparison = analyzer.compare_repositories(repos)
        
        if args.output == "json":
            print(formatter.format_json(comparison))
        else:
            for result in comparison:
                repo_name = result.get("repository")
                if "error" in result:
                    print(f"\n❌ {repo_name}: {result['error']}")
                else:
                    health = result.get("health", {})
                    score = health.get("health_score", 0)
                    print(f"\n📦 {repo_name} - 健康度: {score}/100")
                    
                    metrics = health.get("metrics", {})
                    print(f"   ⭐ {metrics.get('stars', 0):,} | 🍴 {metrics.get('forks', 0):,}")
        
        return 0
    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        return 1


def handle_analyze(args, api: GitHubAPI, formatter: OutputFormatter) -> int:
    """处理 analyze 命令"""
    try:
        repos = api.get_trending_repositories(
            language=args.language,
            since=args.since,
            per_page=50
        )
        
        analyzer = TrendAnalyzer(api)
        analysis = analyzer.analyze_trending_patterns(repos)
        
        # 添加AI洞察
        recommender = AIRecommender()
        insights = recommender.generate_trend_insights(analysis)
        analysis["insights"] = insights
        
        if args.output == "json":
            print(formatter.format_json(analysis))
        elif args.output == "markdown":
            print(formatter.format_markdown(analysis, "Trend Analysis"))
        else:
            print(formatter.format_trend_analysis(analysis))
            print("\n💡 AI洞察:")
            for insight in insights:
                print(f"   {insight}")
        
        return 0
    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        return 1


def handle_velocity(args, api: GitHubAPI, formatter: OutputFormatter) -> int:
    """处理 velocity 命令"""
    try:
        parts = args.repository.split("/")
        if len(parts) != 2:
            print("❌ 错误: 仓库名称格式应为 'owner/repo'", file=sys.stderr)
            return 1
        
        owner, repo = parts
        analyzer = TrendAnalyzer(api)
        velocity = analyzer.calculate_growth_velocity(owner, repo)
        
        if args.output == "json":
            print(formatter.format_json(velocity))
        else:
            print(f"\n📈 增长速率分析: {owner}/{repo}")
            print(f"   评级: {velocity.get('growth_rating', 'N/A')}")
            
            metrics = velocity.get("growth_metrics", {})
            print(f"   总Stars: {metrics.get('total_stars', 0):,}")
            print(f"   日均增长: {metrics.get('daily_star_growth', 0)} ⭐/天")
            
            projected = velocity.get("projected_30d", {})
            print(f"   30天预测: +{projected.get('stars', 0)} ⭐")
        
        return 0
    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        return 1


def main(args: Optional[list] = None) -> int:
    """主入口函数"""
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    
    if not parsed_args.command:
        parser.print_help()
        return 0
    
    # 初始化组件
    api = GitHubAPI(token=parsed_args.token)
    formatter = OutputFormatter(use_color=not parsed_args.no_color)
    
    # 路由到对应处理函数
    handlers = {
        "trending": handle_trending,
        "health": handle_health,
        "recommend": handle_recommend,
        "emerging": handle_emerging,
        "compare": handle_compare,
        "analyze": handle_analyze,
        "velocity": handle_velocity,
    }
    
    handler = handlers.get(parsed_args.command)
    if handler:
        return handler(parsed_args, api, formatter)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
