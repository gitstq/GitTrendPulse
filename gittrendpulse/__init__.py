"""
GitTrendPulse - AI驱动的GitHub趋势智能分析与洞察引擎

一个轻量级、零依赖的CLI工具，用于智能分析GitHub趋势数据，
提供多维度洞察和AI驱动的项目推荐。

Author: GitTrendPulse Team
Version: 1.0.0
License: MIT
"""

__version__ = "1.0.0"
__author__ = "GitTrendPulse Team"
__license__ = "MIT"

from .core import TrendAnalyzer
from .github_api import GitHubAPI
from .recommender import AIRecommender
from .formatter import OutputFormatter

__all__ = [
    "TrendAnalyzer",
    "GitHubAPI", 
    "AIRecommender",
    "OutputFormatter",
]
