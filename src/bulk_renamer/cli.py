"""
命令列介面與輸出控制。
"""
import argparse
import sys
from typing import Sequence, Optional
from .core import BulkRenamer
from .stats import RenameStats


def print_summary(stats: RenameStats, dry_run: bool, label: str = "") -> None:
    """輸出執行統計報告"""
    print("\n" + "=" * 40)
    if dry_run:
        title = f"  試運行總結 (Dry Run){' - ' + label if label else ''}  "
    else:
        title = f"  執行總結報告{' - ' + label if label else ''}  "
    print(title)
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


def run_config_mode(config, cli_args) -> None:
    """以配置文件模式批量执行所有任务"""
    from .utils import clean_macos_metadata

    # CLI 标志覆盖配置文件全局设置
    dry_run = config.dry_run
    verbose = config.verbose
    mac_clean = config.mac_clean
    confirm = config.confirm_before_run

    if cli_args.dry_run:
        dry_run = True
    if cli_args.quiet:
        verbose = False
    if cli_args.no_mac_clean:
        mac_clean = False

    # 打印所有任务预览
    task_count = len(config.tasks)
    print(f"\n将要执行以下 {task_count} 个任务：")
    print("─" * 33)
    for i, task in enumerate(config.tasks, start=1):
        dirs_display = ", ".join(task.directories)
        recursive_str = "是" if task.recursive else "否"
        verbose_str = "是" if verbose else "否"
        print(f"任务 {i}: {task.name}")
        print(f"  目录: {dirs_display}")
        print(f"  移除模式: {task.patterns}")
        print(f"  递归: {recursive_str} | 详细输出: {verbose_str}")
        print("─" * 33)

    if dry_run:
        print("\n--- 注意：现在是在【试运行模式 (Dry Run)】下，文件不会被真实修改 ---\n")

    # 确认提示
    if confirm:
        answer = input("确认执行？[y/N] ").strip().lower()
        if answer != "y":
            print("已取消。")
            sys.exit(0)

    # 逐任务执行
    total_stats_list: list[tuple[str, str, RenameStats]] = []

    for task in config.tasks:
        print(f"\n>>> 开始任务：{task.name}")
        for directory in task.directories:
            print(f"  处理目录：{directory}")
            if mac_clean:
                clean_macos_metadata(directory, dry_run=dry_run)
            renamer = BulkRenamer(
                target_dir=directory,
                text_to_remove=task.patterns,
                dry_run=dry_run,
                recursive=task.recursive,
                verbose=verbose,
            )
            stats = renamer.run()
            total_stats_list.append((task.name, directory, stats))
            print_summary(stats, dry_run, label=f"{task.name} @ {directory}")

    # 合计汇总
    if len(total_stats_list) > 1:
        print("\n" + "=" * 40)
        print("           全部任务合计汇总           ")
        print("=" * 40)
        total_files = sum(s.total_files_scanned for _, _, s in total_stats_list)
        total_dirs = sum(s.total_dirs_scanned for _, _, s in total_stats_list)
        files_renamed = sum(s.files_renamed for _, _, s in total_stats_list)
        dirs_renamed = sum(s.dirs_renamed for _, _, s in total_stats_list)
        errors = sum(s.errors for _, _, s in total_stats_list)
        duration = sum(s.duration for _, _, s in total_stats_list)
        print(f" 总耗时:        {duration:.3f} 秒")
        print(f" 总扫描文件数:  {total_files}")
        print(f" 总扫描目录数:  {total_dirs}")
        print(f" 成功重命名文件:{files_renamed}")
        print(f" 成功重命名目录:{dirs_renamed}")
        if errors > 0:
            print(f" 错误总数:      {errors}")
        print("=" * 40 + "\n")


def main(argv: Optional[Sequence[str]] = None) -> None:
    """處理 CLI 參數解析並且觸發核心邏輯"""
    parser = argparse.ArgumentParser(
        description="批次遞迴重新命名工具 (移除指定字串)"
    )

    parser.add_argument(
        "target_dir",
        type=str,
        nargs="?",
        help="要處理的目標目錄路徑（與 --config 互斥）",
    )

    parser.add_argument(
        "--remove",
        type=str,
        action="append",
        dest="remove",
        metavar="PATTERN",
        help="要從檔名中移除的字串（可多次使用）",
    )

    parser.add_argument(
        "--config",
        type=str,
        metavar="FILE",
        help="YAML 配置文件路徑（與 target_dir 互斥）",
    )

    parser.add_argument(
        "-n", "--dry-run",
        action="store_true",
        help="試運行模式，不會實際更動檔案，但會顯示變更預覽",
    )

    parser.add_argument(
        "--no-mac-clean",
        action="store_true",
        help="停用 macOS 自動清除 ._ 隱藏資源檔案",
    )

    parser.add_argument(
        "--quiet",
        action="store_true",
        help="抑制詳細輸出，僅顯示匯總統計",
    )

    # 若沒有任何參數（sys.argv只有腳本名稱），列印輔助訊息並退出
    if not argv and len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args(argv)

    # 互斥验证
    if args.config and args.target_dir:
        parser.error("--config 與 target_dir 不能同時使用")

    if not args.config and not args.target_dir:
        parser.print_help(sys.stderr)
        sys.exit(1)

    # 配置文件模式
    if args.config:
        from .config import load_config
        try:
            config = load_config(args.config)
        except (FileNotFoundError, ValueError) as e:
            print(f"錯誤：{e}", file=sys.stderr)
            sys.exit(1)
        run_config_mode(config, args)
        return

    # 单目录模式
    if args.dry_run:
        print("\n--- 注意：現在是在【試運行模式 (Dry Run)】下，檔案不會被真實修改 ---\n")

    # 高內聚低耦合：在執行重命名前，作為準備階段清理 OS 垃圾，不侵入核心邏輯
    if not args.no_mac_clean:
        from .utils import clean_macos_metadata
        clean_macos_metadata(args.target_dir, dry_run=args.dry_run)

    # 若未提供 --remove，使用預設字串
    patterns = args.remove if args.remove else ["【海量资源：666root.com微AG110360】"]

    renamer = BulkRenamer(
        target_dir=args.target_dir,
        text_to_remove=patterns,
        dry_run=args.dry_run,
        verbose=not args.quiet,
    )

    stats = renamer.run()

    print_summary(stats, args.dry_run)
