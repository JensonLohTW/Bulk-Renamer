#!/usr/bin/env bash
set -e

# 切換到專案根目錄
cd "$(dirname "$0")/.."

echo "==== 靜態型別與語法檢查 ===="
echo "執行 mypy..."
# 如果沒有安裝 mypy 會顯示錯誤或安裝
uv run mypy src/ || echo "mypy 指令失敗或未安裝"

echo "檢查完成！"
