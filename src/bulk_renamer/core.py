"""
批次重新命名工具的核心邏輯。
"""
import os
from .stats import RenameStats

class BulkRenamer:
    """處理檔案系統遍歷與重命名的核心類別。"""

    def __init__(
        self,
        target_dir: str,
        text_to_remove: str | list[str],
        dry_run: bool = False,
        recursive: bool = True,
        verbose: bool = True,
    ):
        self.target_dir = os.path.abspath(target_dir)
        # 統一處理為列表以供內部迴圈判斷
        if isinstance(text_to_remove, str):
            self.text_to_remove = [text_to_remove]
        else:
            self.text_to_remove = text_to_remove

        self.dry_run = dry_run
        self.recursive = recursive
        self.verbose = verbose
        self.stats = RenameStats()

    def run(self) -> RenameStats:
        """執行批次重新命名流程並回傳統計狀態"""
        if not os.path.isdir(self.target_dir):
            print(f"錯誤：{self.target_dir} 不是一個有效的目錄")
            self.stats.errors += 1
            self.stats.finish()
            return self.stats

        # 由下往上走訪（bottom-up）避免重新命名祖父目錄而使後續子目錄路徑失效
        # 效能優化：內部迴圈以 os.path.join 結合字串判斷，減少 Path 實例化開銷
        walker = os.walk(self.target_dir, topdown=False)
        if not self.recursive:
            root, dirs, files = next(walker)
            self._process_files(root, files)
            self._process_dirs(root, dirs)
        else:
            for root, dirs, files in walker:
                self._process_files(root, files)
                self._process_dirs(root, dirs)

        self.stats.finish()
        return self.stats

    def _get_new_name(self, original_name: str) -> str | None:
        """比對所有目標字串，回傳替換後的新名稱。若無須替換則回傳 None"""
        new_name = original_name
        modified = False
        for text in self.text_to_remove:
            if text in new_name:
                new_name = new_name.replace(text, "")
                modified = True

        return new_name if modified else None

    def _process_files(self, root: str, files: list[str]) -> None:
        """處理目錄內的所有檔案"""
        for name in files:
            self.stats.total_files_scanned += 1
            new_name = self._get_new_name(name)

            if new_name is not None:
                old_path = os.path.join(root, name)
                new_path = os.path.join(root, new_name)

                if self.verbose:
                    print(f"[檔案] 重新命名:\n  原名: {name}\n  新名: {new_name}")
                if not self.dry_run:
                    if os.path.exists(new_path):
                        if self.verbose:
                            print(f"  -> [錯誤] 檔案已存在: {new_path}")
                        self.stats.errors += 1
                        continue
                    try:
                        os.rename(old_path, new_path)
                        self.stats.files_renamed += 1
                    except Exception as e:
                        if self.verbose:
                            print(f"  -> [錯誤] 重命名失敗: {e}")
                        self.stats.errors += 1
                else:
                    self.stats.files_renamed += 1
            else:
                self.stats.files_skipped += 1

    def _process_dirs(self, root: str, dirs: list[str]) -> None:
        """處理目錄內的所有子目錄"""
        for name in dirs:
            self.stats.total_dirs_scanned += 1
            new_name = self._get_new_name(name)

            if new_name is not None:
                old_path = os.path.join(root, name)
                new_path = os.path.join(root, new_name)

                if self.verbose:
                    print(f"[目錄] 重新命名:\n  原名: {name}\n  新名: {new_name}")
                if not self.dry_run:
                    if os.path.exists(new_path):
                        if self.verbose:
                            print(f"  -> [錯誤] 目錄已存在: {new_path}")
                        self.stats.errors += 1
                        continue
                    try:
                        os.rename(old_path, new_path)
                        self.stats.dirs_renamed += 1
                    except Exception as e:
                        if self.verbose:
                            print(f"  -> [錯誤] 重命名失敗: {e}")
                        self.stats.errors += 1
                else:
                    self.stats.dirs_renamed += 1
            else:
                self.stats.dirs_skipped += 1
