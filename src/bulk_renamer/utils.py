"""
系統與輔助工具模組。
包含與作業系統相關的清理或環境檢查工具。
"""
import sys
import subprocess

def clean_macos_metadata(target_dir: str, dry_run: bool) -> None:
    """清理 macOS 產生的 ._ 資源屬性檔案"""
    if sys.platform != "darwin":
        return
        
    if dry_run:
        print("\n[系統清理] (試運行) 將嘗試使用 dot_clean 清除 macOS 的 ._ 隱藏檔案")
        return
        
    print("\n[系統清理] 正在清除 macOS 的 ._ 隱藏檔案...")
    try:
        # dot_clean -m: Always delete dot underbar files
        subprocess.run(
            ["dot_clean", "-m", target_dir], 
            check=True, 
            capture_output=True
        )
        print("[系統清理] 清除完成")
    except FileNotFoundError:
        print("[系統清理] 未找到 dot_clean 指令，略過清理。")
    except subprocess.CalledProcessError as e:
        print(f"[系統清理] 警告：清除隱藏檔案時發生錯誤 ({e})，將略過並繼續執行後續作業。")
