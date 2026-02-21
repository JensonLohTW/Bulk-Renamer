"""
命令列介面與輸出控制。
"""
import argparse
import sys
from typing import Sequence, Optional
from .core import BulkRenamer
from .stats import RenameStats

def print_summary(stats: RenameStats, dry_run: bool) -> None:
    """輸出執行統計報告"""
    print("\n" + "=" * 40)
    if dry_run:
        print("          試運行總結 (Dry Run)          ")
    else:
        print("             執行總結報告             ")
    print("=" * 40)
    
    print(f" 耗時: {stats.duration:.3f} 秒")
    print("-" * 40)
    print(f" 總掃描檔案數: {stats.total_files_scanned}")
    print(f" 總掃描目錄數: {stats.total_dirs_scanned}")
    print("-" * 40)
    
    print(f" 成功重命名檔案: {stats.files_renamed}")
    print(f" 略過檔案:       {stats.files_skipped}")
    print(f" 成功重命名目錄: {stats.dirs_renamed}")
    print(f" 略過目錄:       {stats.dirs_skipped}")
    
    if stats.errors > 0:
        print("-" * 40)
        print(f" 錯誤總數: {stats.errors}")
        
    print("=" * 40 + "\n")

def main(argv: Optional[Sequence[str]] = None) -> None:
    """處理 CLI 參數解析並且觸發核心邏輯"""
    parser = argparse.ArgumentParser(
        description="批次遞迴重新命名工具 (移除指定字串)"
    )
    
    parser.add_argument("target_dir", type=str, help="要處理的目標目錄路徑")
    
    parser.add_argument(
        "--remove", 
        type=str, 
        default="【海量资源：666roo t.com微AG110360】",
        help="要從檔名中移除的字串（預設會移除海量資源相關字串）"
    )
    
    parser.add_argument(
        "-n", "--dry-run",
        action="store_true",
        help="試運行模式，不會實際更動檔案，但會顯示變更預覽"
    )
    
    # 若沒有任何參數（sys.argv只有腳本名稱），列印輔助訊息並退出
    if not argv and len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
        
    args = parser.parse_args(argv)
    
    if args.dry_run:
        print("\n--- 注意：現在是在【試運行模式 (Dry Run)】下，檔案不會被真實修改 ---\n")
    
    renamer = BulkRenamer(
        target_dir=args.target_dir, 
        text_to_remove=args.remove, 
        dry_run=args.dry_run
    )
    
    stats = renamer.run()
    
    print_summary(stats, args.dry_run)
