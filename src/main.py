#!/usr/bin/env python3
"""
程式進入點。
保留原有的指令用法以確保向後相容。
"""
import sys
import os

# 確保可以直接透過 python src/main.py 執行而不會找不到 package
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bulk_renamer.cli import main

if __name__ == "__main__":
    main()
