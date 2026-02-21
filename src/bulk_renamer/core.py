"""
批次重新命名工具的核心邏輯。
"""
import os
from .stats import RenameStats

class BulkRenamer:
    """處理檔案系統遍歷與重命名的核心類別。"""
    
    def __init__(self, target_dir: str, text_to_remove: str, dry_run: bool = False):
        self.target_dir = os.path.abspath(target_dir)
        self.text_to_remove = text_to_remove
        self.dry_run = dry_run
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
        for root, dirs, files in os.walk(self.target_dir, topdown=False):
            self._process_files(root, files)
            self._process_dirs(root, dirs)
            
        self.stats.finish()
        return self.stats

    def _process_files(self, root: str, files: list[str]) -> None:
        """處理目錄內的所有檔案"""
        text = self.text_to_remove
        for name in files:
            self.stats.total_files_scanned += 1
            if text in name:
                new_name = name.replace(text, "")
                old_path = os.path.join(root, name)
                new_path = os.path.join(root, new_name)
                
                print(f"[檔案] 重新命名:\n  原名: {name}\n  新名: {new_name}")
                if not self.dry_run:
                    if os.path.exists(new_path):
                        print(f"  -> [錯誤] 檔案已存在: {new_path}")
                        self.stats.errors += 1
                        continue
                    try:
                        os.rename(old_path, new_path)
                        self.stats.files_renamed += 1
                    except Exception as e:
                        print(f"  -> [錯誤] 重命名失敗: {e}")
                        self.stats.errors += 1
                else:
                    self.stats.files_renamed += 1
            else:
                self.stats.files_skipped += 1

    def _process_dirs(self, root: str, dirs: list[str]) -> None:
        """處理目錄內的所有子目錄"""
        text = self.text_to_remove
        for name in dirs:
            self.stats.total_dirs_scanned += 1
            if text in name:
                new_name = name.replace(text, "")
                old_path = os.path.join(root, name)
                new_path = os.path.join(root, new_name)
                
                print(f"[目錄] 重新命名:\n  原名: {name}\n  新名: {new_name}")
                if not self.dry_run:
                    if os.path.exists(new_path):
                        print(f"  -> [錯誤] 目錄已存在: {new_path}")
                        self.stats.errors += 1
                        continue
                    try:
                        os.rename(old_path, new_path)
                        self.stats.dirs_renamed += 1
                    except Exception as e:
                        print(f"  -> [錯誤] 重命名失敗: {e}")
                        self.stats.errors += 1
                else:
                    self.stats.dirs_renamed += 1
            else:
                self.stats.dirs_skipped += 1
