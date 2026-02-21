# Bulk Renamer

Bulk Renamer 是一個高效、安全的批次檔案重新命名工具，使用 Python 開發，支援遞迴遍歷目錄，並提供試運行（Dry Run）模式以及詳細的處理統計報告。

## 核心特徵

* **批量與遞迴處理**：由下往上（bottom-up）走訪目錄，避免重命名父目錄導致子目錄路徑失效。
* **安全性優先**：
  * 提供 `--dry-run` 模式，讓您預先檢視將修改的項目，確認無誤後再執行真實變更。
  * 具備防呆機制，若目標目錄已有相同檔名的檔案，將自動跳過並標示錯誤，避免覆蓋資料。
* **詳細的處理報表**：執行完畢後會輸出清晰的摘要報告，顯示耗時、總掃描數、成功數與跳過數。
* **高效能架構**：減少大量實例化 `Path` 的開銷，直接透過 `os.path.join` 結合字串運算以提升大量檔案處理效能。

## 系統需求

* Python 3.8+
* 依賴管理器: `uv` (建議)

## 安裝與使用

1. 安裝相依套件 (若有需要)：
   ```bash
   uv sync
   ```

2. 執行腳本：
   建議直接透過 `scripts/start.sh` 執行以確保在正確的環境路徑下運作。
   ```bash
   ./scripts/start.sh /path/to/target/folder
   ```

### 指令參數說明

您可以透過**單一目標目錄**或使用**自訂配置檔**兩種方式來執行。

#### 單目錄模式
* `target_dir` (單目錄必選)：要遞迴處理的目標目錄路徑。
* `--remove` (可選)：要從檔名中移除的字串（預設會移除海量資源相關字串）。
* `-n`, `--dry-run` (可選)：試運行模式，不會實際更動檔案，僅作變更預覽。
* `-q`, `--quiet` (可選)：抑制詳細輸出。

**範例**：

執行試運行 (Dry Run)：
```bash
./scripts/start.sh /path/to/target/folder --dry-run
```

自訂移除特定字串：
```bash
./scripts/start.sh /path/to/target/folder --remove "要刪除的文字"
```

#### 配置檔模式
透過撰寫 YAML 配置檔，您可以一次設定多個目錄、不同要移除的字串，甚至定義多組任務。

* `--config` (配置檔必選)：指定 YAML 配置檔的路徑。
* 命令列傳遞的 `--dry-run` 與 `--quiet` 參數優先級高於配置檔內的設定。

**範例**：

1. 建立配置檔 (您可以複製 `config.example.yaml` 來修改)：
   ```bash
   cp config.example.yaml config.yaml
   ```

2. 根據配置檔進行試運行 (確保安全)：
   ```bash
   ./scripts/start.sh --config config.yaml --dry-run
   ```

3. 確認無誤後正式執行：
   ```bash
   ./scripts/start.sh --config config.yaml
   ```

## 開發與測試

專案使用 `scripts/` 下的腳本進行工程管理：

* `check.sh`: 執行靜態型別與語法檢查 (`mypy`, `flake8` 等)。
* `test.sh`: 建立模擬目錄、建立測試檔案並自動驗證 Help、Dry Run 及實際重命名功能的正確性。

```bash
./scripts/test.sh
```

## 專案結構

```
src/
├── bulk_renamer/
│   ├── __init__.py
│   ├── core.py      # 核心重命名邏輯
│   ├── stats.py     # 處理統計資料類別
│   └── cli.py       # 命令列解析與結果輸出
└── main.py          # 程式進入點 (維持指令相容性)
scripts/
├── start.sh         # 包裝主要執行邏輯
├── check.sh         # 執行靜態檢查
└── test.sh          # 執行測試與驗證
```
