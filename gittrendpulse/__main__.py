#!/usr/bin/env python3
"""
GitTrendPulse - 模块入口
允许通过 python -m gittrendpulse 运行
"""

import sys
from .cli import main

if __name__ == "__main__":
    sys.exit(main())
