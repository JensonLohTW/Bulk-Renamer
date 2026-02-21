#!/usr/bin/env bash
set -e

# 切換到專案根目錄
cd "$(dirname "$0")/.."

if [ $# -eq 0 ]; then
    echo "請提供目標目錄作為參數，例如："
    echo "  ./scripts/start.sh /path/to/target/folder"
    exit 1
fi

uv run python src/main.py "$@"
