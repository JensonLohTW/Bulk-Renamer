#!/usr/bin/env bash
set -e

# 切換到專案根目錄
cd "$(dirname "$0")/.."

echo "==== 開始測試 Bulk Renamer ===="

TEST_DIR="test_dir"

# 1. 準備模擬資料
rm -rf "$TEST_DIR"
mkdir -p "$TEST_DIR/a/b"
touch "$TEST_DIR/file1【海量资源：666roo t.com微AG110360】.txt"
touch "$TEST_DIR/a/file2.txt"
mkdir -p "$TEST_DIR/dir1【海量资源：666roo t.com微AG110360】"

# 2. 測試 Help 指令
echo -e "\n---> 測試 Help 指令"
uv run python src/main.py -h || true

# 3. 測試 Dry Run 模式
echo -e "\n---> 測試 Dry Run 模式"
uv run python src/main.py "$TEST_DIR" --dry-run

# 4. 測試實際重命名
echo -e "\n---> 測試實際執行重命名"
uv run python src/main.py "$TEST_DIR"

# 5. 清理
rm -rf "$TEST_DIR"
echo -e "\n==== 測試完成 ===="
