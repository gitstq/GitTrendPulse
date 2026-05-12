#!/usr/bin/env python3
"""
GitTrendPulse - Setup Script
"""

from setuptools import setup, find_packages
import os

# 读取README文件
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

setup(
    name="gittrendpulse",
    version="1.0.0",
    author="GitTrendPulse Team",
    author_email="gittrendpulse@example.com",
    description="🚀 AI驱动的GitHub趋势智能分析与洞察引擎",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/GitTrendPulse",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "gittrendpulse=gittrendpulse.cli:main",
            "gtp=gittrendpulse.cli:main",
        ],
    },
    keywords="github trending ai analysis cli developer-tools",
    project_urls={
        "Bug Reports": "https://github.com/gitstq/GitTrendPulse/issues",
        "Source": "https://github.com/gitstq/GitTrendPulse",
        "Documentation": "https://github.com/gitstq/GitTrendPulse#readme",
    },
)
