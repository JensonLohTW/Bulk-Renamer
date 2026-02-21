"""
批次重新命名工具的狀態追蹤與統計。
"""
from dataclasses import dataclass, field
import time

@dataclass
class RenameStats:
    start_time: float = field(default_factory=time.time)
    end_time: float = 0.0
    
    total_files_scanned: int = 0
    total_dirs_scanned: int = 0
    
    files_renamed: int = 0
    dirs_renamed: int = 0
    
    files_skipped: int = 0
    dirs_skipped: int = 0
    
    errors: int = 0

    def finish(self) -> None:
        """紀錄結束時間"""
        self.end_time = time.time()
        
    @property
    def duration(self) -> float:
        """計算總耗時(秒)"""
        return (self.end_time or time.time()) - self.start_time
