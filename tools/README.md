# 🛠️ 教材維護工具

各章「學生素材」範例 Notebook、素材壓縮檔與網頁版，都由這個資料夾的程式產生。**請不要直接修改 `.ipynb` 或 `docs/` 裡的 HTML**，改產生器之後重建即可。

## 更新流程（在專案根目錄執行）

| 步驟 | 指令 | 做什麼 |
| :---: | --- | --- |
| 1 | `python tools/fetch_real_data.py` | 從政府資料開放平台下載最新資料，存成快照到 `tools/real_data/`（只更新部分資料：`python tools/fetch_real_data.py aqi mrt`） |
| 2 | `python tools/build_student_materials.py` | 依 `tools/materials/chXX_*.py` 重建各章範例 Notebook，並同步更新章節 README 的素材區與根 README 的任務連結 |
| 3 | `python tools/execute_student_notebooks.py --verify` | 把參考解答填進練習格，確認每一個 ✅ 檢查都通過（不存檔） |
| 4 | `python tools/execute_student_notebooks.py` | 執行範例並存入輸出，學生在 GitHub 上就看得到表格與圖 |
| 5 | `python tools/build_student_materials.py --zip-only` | 把含輸出的範例重新打包成各章 `學生素材.zip` |
| 6 | `python tools/build_site.py` | 從 README 重新產生網頁版（`docs/`），push 後 GitHub Pages 約一分鐘更新 |

只改了某幾章時，步驟 2～5 都可以在後面加章節資料夾名稱，例如 `python tools/build_student_materials.py 日期和時間`。

> [!WARNING]
> **更新資料後，一定要核對「💡 看懂結果」的文字！**
>
> 範例裡的說明是依照目前快照的數字寫的，例如「斗六一年約 70 天空氣不健康」、「2,885 列其實只有 1,127 場車禍」、「台北車站每天 30 多萬人次」。
> 換了新資料，程式照樣跑得動、✅ 檢查也會通過（檢查是拿解答算出的答案比對），**但說明文字裡的數字和結論可能已經不對了**。
>
> 執行 `fetch_real_data.py` 後，終端機會列出用到這些資料的章節。請在步驟 4 之後打開這幾本範例，逐一比對 💡 說明和實際輸出；
> 不一致時，修改對應的 `tools/materials/chXX_*.py`，再從步驟 2 重跑。

## 資料夾說明

| 路徑 | 內容 |
| --- | --- |
| `real_data/` | 政府開放資料快照與 `SOURCES.json`（資料集名稱、提供機關、網址、授權、下載日期） |
| `materials/chXX_*.py` | 每一章範例的產生器：故事、程式、💡 說明、練習題都寫在這裡；檔案開頭的 `SOURCES` 宣告用到哪些資料 |
| `materials/nbtools.py` | 共用工具：情境表頭、資料來源表、練習檢查小幫手、任務地圖 |
| `check_notebooks.py` | 檢查各章課堂 Notebook（`README.ipynb` 等）能否從頭跑到尾 |

## 需要的套件

`pandas`、`numpy`、`matplotlib`、`seaborn`、`mplfonts`、`openpyxl`、`xlrd`、`nbformat`、`nbclient`、`ipykernel`、`markdown-it-py`、`mdit-py-plugins`

所有資料皆依「政府資料開放授權條款－第1版」使用。
