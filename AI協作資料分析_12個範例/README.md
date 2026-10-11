# AI 協作資料分析｜十二個範例

這條課程路線為不熟悉程式的學生設計。學生以自然語言提出需求，AI 建立並執行程式；學生負責看懂資料、決定處理方式、解讀結果與驗收。每例先用 ipynb 一步步完成分析，再把同一套邏輯做成可重複執行的報表或 Streamlit 應用。

教材提供 **12 份範例 README、逐步 prompt，以及每例固定的偽資料與資料卡**。沒有預先代寫 `.py`、`.ipynb` 或報表；這些成果要由學生下命令，讓 AI 在學生自己的專案中產生。學生只要先建好環境（第 0 步），依序完成十二個範例，就能走完資料分析的完整流程：讀取 → 清理 → 整理 → 分析 → 視覺化 → 溝通。

## 十二個範例

| 編號 | 範例／資料夾 | 資料 | 核心觀念 | 交付成果 |
| :--- | :--- | :--- | :--- | :--- |
| 01 | [班級段考成績](./01_class_scores/README.md) | 45 位學生 × 5 科 | NumPy 陣列、向量化、缺值統計、相關 | Excel 成績報表 |
| 02 | [便利商店一週銷售](./02_store_sales/README.md) | 175 筆 | DataFrame 選取、排序、新增欄位、篩選 | Excel 銷售摘要 |
| 03 | [圖書館借閱紀錄](./03_library_files/README.md) | Excel＋Big5 CSV＋JSON | 多種格式、編碼、資料型態、合併 | 整合 Excel 與 CSV |
| 04 | [社區活動問卷大掃除](./04_survey_cleaning/README.md) | 320 列髒資料 | 重複、缺值、格式統一、異常值、多選題 | 清理腳本與清理報告 |
| 05 | [連鎖書店季報](./05_bookstore_merge/README.md) | 3 個月訂單＋門市＋商品 | concat、merge、鍵值檢查 | Excel 季報 |
| 06 | [縣市用電](./06_power_reshape/README.md) | 22 縣市 × 24 個月 | melt、pivot_table、stack | Streamlit 用電查詢 |
| 07 | [健身房會員](./07_gym_groupby/README.md) | 3,000 筆入場 | groupby、agg、transform、分組排名 | Streamlit 分店儀表板 |
| 08 | [外送訂單時間](./08_delivery_time/README.md) | 2,500 筆（UTC） | datetime、時區、resample、rolling | Streamlit 時段熱度 |
| 09 | [六城市氣象](./09_weather_charts/README.md) | 6 城市 × 12 個月 | Matplotlib 五種基本圖、子圖、存檔 | 圖表與 HTML 報告 |
| 10 | [台北租屋行情](./10_rent_seaborn/README.md) | 800 筆物件 | Seaborn 分布／比較／關係、離群值 | Streamlit 租屋探索器 |
| 11 | [業務週報](./11_sales_kpi_style/README.md) | 15 人 × 13 週 | Styler 格式化、條件標色、輸出 | HTML 週報與 Excel |
| 12 | [共享單車綜合專題](./12_bike_capstone/README.md) | 6,020 筆＋站點＋天氣 | 完整流程：提問到溝通 | Streamlit 儀表板與報告 |

01～05 打好基礎（NumPy、pandas、檔案、清理、合併），06～08 練習整理與分析（重塑、分組、時間），09～11 學會呈現（圖表、表格），12 把全部串起來。

## 第 0 步｜建立環境

十二例共用同一個學生專案與同一個虛擬環境，只需要建立一次。建議使用 Python 3.12。

### 方法一：使用 uv（推薦）

先依 [uv 官方說明](https://docs.astral.sh/uv/getting-started/installation/) 安裝 uv，再開終端機執行：

```bash
mkdir 資料分析專案
cd 資料分析專案
uv init --python 3.12
uv add pandas numpy matplotlib seaborn openpyxl jupyter streamlit mplfonts
```

### 方法二：使用 venv＋pip

```bash
mkdir 資料分析專案
cd 資料分析專案
python -m venv .venv
# macOS：source .venv/bin/activate
# Windows：.venv\Scripts\activate
pip install pandas numpy matplotlib seaborn openpyxl jupyter streamlit mplfonts
```

用 VS Code 開啟「資料分析專案」資料夾，建立 Notebook 時選擇專案內的 `.venv` 當作 kernel。

### 環境檢查 prompt

環境建好後，把這段貼給 AI，確認一切正常再開始 01。

```text
請在我的專案根目錄建立 00_env_check.ipynb，使用專案的 .venv。
印出 Python、pandas、numpy、matplotlib、seaborn、openpyxl、streamlit 版本。
依課程首頁「共用繁體中文繪圖 prompt」設定中文字型。
畫一張含負數、繁體中文標題與圖例的折線圖，並存成 PNG。
執行全部儲存格，回報每個套件是否可用、圖片中文與負號是否正常。
缺套件時告訴我安裝命令，不要改用其他套件。
```

## 在 GitHub 閱讀，只下載當次需要的檔案

1. 在 GitHub 開啟當次範例的 README，直接複製 prompt 給 AI，不必下載 README。
2. 在自己的學生專案中，讓 AI 建立該例資料夾，例如 `01_class_scores/`；Notebook、輸出與應用都放在該例內。
3. 點該例「範例檔下載」連結，只儲存本次需要的檔案到 `範例資料夾/data/`。不要下載整個 GitHub repo 或全部十二例資料。
4. 依序貼 A0～A5，再貼 B1～B2。觀念不懂時，打開該段的「觀念連結」閱讀本 repo 的章節。

CSV 連結開啟時若瀏覽器直接顯示文字，使用「另存新檔」並保留 `.csv` 副檔名。資料卡可線上閱讀，不必下載。AI 可讀取教材網址；如果工具無法讀取，貼上當次 README 的內容即可。

## 每例的兩組 prompt 怎麼貼

- **A0～A5：Notebook 路線。** 設定 AI 角色 → 讀取與觀察 → 清理與整理 → 分析與計算 → 視覺化與解讀 → 重新執行與保存。每段停下問一個觀念問題，學生確認結果合理後才貼下一段。
- **B1～B2：交付路線。** 把 Notebook 的邏輯整理成可重複執行的腳本、報表或 Streamlit 應用，再驗收「重跑結果一致、數字和 Notebook 相同」。

AI 要能直接建立真正的 `.ipynb` 與程式檔並執行。若使用只有聊天功能的 AI，請它交付完整檔案，再由學生存到指定位置；沒有執行能力時不可宣稱已執行或測試。每次續接對話，讓 AI 先讀線上教材與本機 Notebook，避免從頭亂改。

### 共用 prompt｜Matplotlib 與 Seaborn 繁體中文繪圖

第一次繪圖前貼給 AI；每個新 Notebook 都要套用，Streamlit 應用與輸出圖表的腳本也沿用同一設定。字型由第 0 步安裝的 `mplfonts` 套件提供，不必另外下載字型檔。

```text
請在 Notebook 第一張圖之前加入以下字型設定儲存格，不要改寫成其他方式：

import glob, os
import mplfonts
from matplotlib import font_manager
from mplfonts import use_font

for f in glob.glob(os.path.join(os.path.dirname(mplfonts.__file__), "fonts", "*.[ot]tf")):
    font_manager.fontManager.addfont(f)   # 直接註冊 mplfonts 內附的字型，不改任何檔案
use_font("Noto Sans CJK SC")              # 套用思源黑體，負號也會一起處理

使用 Seaborn 時改用 sns.set_theme(font="Noto Sans CJK SC")，避免主題覆蓋中文字型。
不要執行 mplfonts init，也不要寫死老師電腦的字型路徑。
Streamlit 應用與輸出圖表的腳本，在程式開頭執行同一段設定。
圖表標題、座標軸、圖例、類別與註解全部使用繁體中文。
用含負數的中文圖測試顯示及存檔；缺字時修正，不改成英文。
```

`Noto Sans CJK SC` 是 mplfonts 內附的思源黑體，可以正常顯示繁體中文。在 Google Colab 使用時，請在這段程式最前面加一行 `%pip install -q mplfonts`。設定依據：[Matplotlib 字型管理](https://matplotlib.org/stable/api/font_manager_api.html)、[Seaborn 主題設定](https://seaborn.pydata.org/generated/seaborn.set_theme.html)。

### AI 出錯時的除錯 prompt

```text
這是我執行目前步驟時的錯誤：
（貼上完整錯誤與步驟）
請說明原因，只修正必要部分並重跑。
保留原資料與已完成內容，回報結果與下一步。
```

### 想把成果改成另一種形式時

完成任一例後可以延伸，例如把 Excel 報表改成 Streamlit 應用，或把應用的數據匯出成 Excel。官方資料：[Streamlit 基本概念](https://docs.streamlit.io/get-started/fundamentals/main-concepts)、[openpyxl](https://openpyxl.readthedocs.io/)。

```text
請把我指定範例的成果改成（Streamlit 應用／Excel 報表／HTML 報告）。
沿用原本 Notebook 的資料處理邏輯與清理後資料，不重新產生資料。
保留原本的成果，新成果另存新檔，提供執行命令。
圖表沿用共用字型，全部顯示繁體中文，並依原範例的 B2 驗收。
```

## 觀念連結如何穿插教學

各段 prompt 的標題下方，連到本 repo 既有章節，學生直接在 GitHub 閱讀。先讀與當前問題相關的段落，再讓 AI 以實際結果回扣觀念。

| 本 repo 章節 | 最適合回看的範例 |
| :--- | :--- |
| [Numpy建立與計算](../Numpy建立與計算/README.md) | 01：陣列、向量化、統計 |
| [初見pandas](../初見pandas/README.md)、[pandas的基礎功能](../pandas的基礎功能/README.md) | 01、02、07、11：DataFrame 操作 |
| [檔案存取](../檔案存取/README.md)、[pandas的檔案存取](../pandas的檔案存取/README.md) | 03、05：格式、編碼 |
| [資料整理和使用前準備](../資料整理和使用前準備/README.md) | 04、10、12：清理、缺值、異常值 |
| [數據整理：連接、合併和重塑](../數據整理_連接_合併_重塑/README.md) | 03、05、06、12：合併與重塑 |
| [群組資料和群組運算](../群組資料和群組運算/README.md) | 04～08、12：分組統計 |
| [日期和時間](../日期和時間/README.md) | 03、08、12：日期、時區、重新取樣 |
| [繪圖和視覺展示](../繪圖和視覺展示/README.md) | 01、09：Matplotlib 基礎 |
| [直接使用pandas繪制圖表](../直接使用pandas繪制圖表/README.md) | 02～07、10、11：快速繪圖 |
| [看懂資料與選對圖表](../看懂資料與選對圖表/README.md) | 06～10、12：選對圖表 |
| [視覺化表格](../視覺化表格/README.md) | 11：表格格式化 |
| [全方面分析](../全方面分析/README.md) | 12：完整專題 |

## 偽資料安排

十二例的資料全部是教材原創的合成資料，每例 `data/DATA_CARD.md` 記錄欄位意義、筆數、固定亂數種子、生成規則、刻意安排的資料狀況與 SHA-256。資料由 [`tools/ai_data12/build_data.py`](../tools/ai_data12/build_data.py) 產生，重跑會得到完全相同的檔案。

- 01～02：乾淨資料，專心學 NumPy 與 pandas 基本操作。
- 03：同一主題的三種檔案格式，其中一份是 Big5 編碼。
- 04：刻意弄髒的問卷，練習完整的清理流程。
- 05：三個月欄位名稱與代碼寫法不一致，且有對不上的鍵。
- 06：寬格式表格，必須重塑才能分析。
- 07～08：有重複會員與 UTC 時間，練習分組與時區。
- 09～11：重點在呈現；10 有輸入錯誤的離群值，11 需要自己計算達成率。
- 12：重複、時間填反、忘記還車與缺值同時出現，需要學生自己決定處理方式。

AI 不因結果不漂亮而重抽資料或修改原始檔；清理結果一律另存。假想情境的分析結果不能直接當成真實世界的結論。

## 教師課前準備與最後驗收

課前在學生使用的 AI 工具與 Python 3.12 環境試跑第 0 步與至少一例的 prompt。本教材只驗證了資料檔與連結，沒有代替學生執行十二例的 Notebook 與應用；套件 API 由 AI 依學生安裝的版本確認。

完成範例後請回答：「我的分析問題是什麼？資料有什麼問題、我怎麼處理？我用什麼數字和圖表支持結論？AI 幫我執行了什麼，我如何確認？」

最後每位學生以 12 的綜合專題（或任選一例）發表三分鐘：問題、資料、處理方式、發現與一個限制。評量重點為觀念與驗收，不考手寫 Python 語法。完成本課程代表能指揮 AI 完成並檢查一份資料分析；後續可回到本 repo 各章節深化 NumPy、pandas 與視覺化技巧。

[返回主教材](../README.md)
