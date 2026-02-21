#!/usr/bin/env bash
set -e

# 切換到專案根目錄
cd "$(dirname "$0")/.."

if [ $# -eq 0 ]; then
    echo "用法："
    echo "  单目录模式："
    echo "    ./scripts/start.sh /path/to/target/folder [--remove '字串'] [--dry-run] [--quiet]"
    echo ""
    echo "  配置文件模式："
    echo "    ./scripts/start.sh --config config.yaml [--dry-run] [--quiet]"
    echo ""
    echo "范例："
    echo "  ./scripts/start.sh ~/Downloads --remove '广告字串' --dry-run"
    echo "  ./scripts/start.sh --config config.yaml --dry-run"
    exit 1
fi

if [ "$1" = "--config" ]; then
    # 配置文件模式：透传所有参数给 Python
    uv run python src/main.py --config "$2" "${@:3}"
else
    # 原有单目录模式
    uv run python src/main.py "$@"
fi
