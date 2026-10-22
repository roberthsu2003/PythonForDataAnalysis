# 📊 📥 pandas 的檔案存取：一行讀進 CSV、Excel、JSON、資料庫，一行存成老闆要的格式

> [!IMPORTANT]
> **本章節學習核心**：
> 1. **核心觀念**：pandas 提供一整組 `read_xxx()` 與 `to_xxx()` 工具，CSV、Excel、JSON、網路 API、SQLite 資料庫都能「一行讀進來、一行存出去」，而且讀檔時就能順便跳過雜訊、指定欄位、標記缺值。
> 2. **AI 協作能力**：學會向 AI 描述「檔案的毛病」（沒有標題列、前幾行是註解、缺值寫成 NA 或 NULL、檔案太大），讓 AI 選對讀檔參數，一次讀乾淨。
> 3. **商業決策產出**：能把政府開放資料（空氣品質、氣象觀測）下載下來、篩出關鍵資訊，並輸出成 Excel 或資料庫，交給同事或系統使用。

<!-- ai-bridge:start -->
> [!TIP]
> 🤖 **不寫程式也能先練一次**：本章的技巧，在「零程式碼・AI 協作」的實戰範例裡會用到。
> 可以先在 Colab 指揮 AI 做一遍，再回來看本章，理解程式是怎麼寫的：
>
> - [範例 03 圖書館借閱](../AI協作資料分析_12個範例/03_library_files/README.md)：讀取 Excel 工作表與 JSON
> - [範例 13 辦公室資料](../AI協作資料分析_12個範例/13_office_chart_basics/README.md)：讀取多個工作表
> - [範例 14 法務部公開統計](../AI協作資料分析_12個範例/14_moj_public_data/README.md)：下載政府開放資料
<!-- ai-bridge:end -->

---

> 🚀 **完整互動教學 Notebook**：
> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/pandas%E7%9A%84%E6%AA%94%E6%A1%88%E5%AD%98%E5%8F%96/README.ipynb) [開啟 README.ipynb](./README.ipynb)
>
> 📝 **課後練習解答**：[homework1：下載空氣品質指標 AQI 並存成 CSV](./download政府資料開放平台_空氣品質指標_csv下載儲存.ipynb)｜[homework2：下載氣象觀測 JSON 並存入 SQLite](./download政府資料平台解決方案_json.ipynb)
>
> ⚠️ 在 Colab 開啟時只會載入 Notebook 本身，若要讀取本資料夾的 `ex1.csv`、`總統.xls` 等檔案，請先上傳到 Colab 左側的「檔案」區。

---

## 📦 學生素材下載

> [!TIP]
> **📥 茶語時光：搞定五種難搞的資料檔**
>
> 月初結帳日，各部門丟來五種格式的檔案：POS 系統匯出的「髒」CSV、每家店一個工作表的 Excel、外送平台的巢狀 JSON、IT 部門的會員資料庫，還有一個 10 萬筆、用 Excel 打開會卡住的交易檔。你要用 pandas 一一讀進來，最後整理成一份多工作表的 Excel 交給主管。
>
> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/pandas%E7%9A%84%E6%AA%94%E6%A1%88%E5%AD%98%E5%8F%96/%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90/%E7%AF%84%E4%BE%8B_%E8%8C%B6%E8%AA%9E%E6%99%82%E5%85%89_%E4%BA%94%E7%A8%AE%E9%9B%A3%E6%90%9E%E7%9A%84%E8%B3%87%E6%96%99%E6%AA%94.ipynb) [開啟範例 Notebook](./學生素材/%E7%AF%84%E4%BE%8B_%E8%8C%B6%E8%AA%9E%E6%99%82%E5%85%89_%E4%BA%94%E7%A8%AE%E9%9B%A3%E6%90%9E%E7%9A%84%E8%B3%87%E6%96%99%E6%AA%94.ipynb)　｜　[⬇️ 下載本章素材 pandas的檔案存取_學生素材.zip](https://github.com/roberthsu2003/PythonForDataAnalysis/raw/master/pandas%E7%9A%84%E6%AA%94%E6%A1%88%E5%AD%98%E5%8F%96/pandas%E7%9A%84%E6%AA%94%E6%A1%88%E5%AD%98%E5%8F%96_%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90.zip)

| 素材檔案 | 內容 |
| --- | --- |
| `POS匯出_信義店_2024-03.csv` | POS 匯出的日報：有註解行、千分位逗號、`--` 缺值、最後一列是合計 |
| `各店月報_2024.xlsx` | 5 個工作表（每店一張），前兩列是標題 |
| `外送平台訂單_2024-03.json` | 外送平台的巢狀 JSON：一筆訂單裡有多個品項 |
| `會員資料庫.db` | SQLite 資料庫，內有「會員」資料表（800 位） |
| `全年交易紀錄_2024.csv` | 10 萬筆交易紀錄（用來練習分批讀取） |
| `課程原始資料/` | 本章課堂 Notebook 使用的原始資料檔 |

**使用方式**：下載壓縮檔並解壓縮後，用 Jupyter 或 VS Code 開啟範例 Notebook，從上到下依序執行即可；若直接在 Colab 開啟，第一格程式會自動下載本章素材。範例最後附有練習題與參考解答。

---

## 💡 1. 為什麼需要這個觀念？（生活化比喻）

- **上一章用 `csv` / `json` 模組讀檔，就像「手工拆包裹」**：要自己一層一層打開、一筆一筆整理。**pandas 的 `read_csv()` 就像「自動拆箱機」**：丟進去，出來就是整理好的表格。
- **讀檔參數就像「給拆箱機的指示單」**：「前 3 行是廣告傳單，跳過」（`skiprows`）、「這箱沒有標籤，標籤我給你」（`names`）、「寫著 NA 的格子當成空的」（`na_values`）、「只要這四樣東西」（`usecols`）。
- **`chunksize` 就像「分批搬家」**：100 萬筆的大檔案一次搬不動，就每次搬 1000 筆，邊搬邊統計。
- **SQLite 就像「放在單一檔案裡的小型倉庫」**：不需要架設伺服器，一個 `.sqlite` 檔就是一個資料庫，適合存放每天累積的觀測資料。

| **核心概念** | **生活化直觀比喻** | **傳統工程師痛苦點** | **AI 時代你的角色** |
| -------- | ----------- | ------------ | ------------- |
| `read_csv` / `read_excel` / `read_json` | 自動拆箱機 | 每種格式要記不同寫法 | 說「這是 Excel，讀第幾個工作表」 |
| `header` / `names` / `index_col` | 決定哪一行是標籤 | 沒標題列時資料被當成欄名 | 說「沒有標題列，欄名是…」 |
| `skiprows` / `usecols` / `nrows` | 跳過廣告、只拿需要的 | 雜訊列讓整張表格錯位 | 貼前 10 行給 AI 判斷要跳過哪些 |
| `na_values` | 把「NA」「NULL」「-」當空格 | 缺值被當成文字，統計失準 | 告訴 AI 原始檔用什麼代表缺值 |
| `chunksize` | 分批搬家 | 大檔案讀到記憶體爆掉 | 說「檔案很大，請分批處理」 |
| `to_csv` / `to_excel` / `to_json` | 打包出貨 | 輸出多了一欄索引、中文亂碼 | 要求「不要輸出索引、用 UTF-8」 |
| `to_sql` / `read_sql` | 存進倉庫／從倉庫取貨 | SQL 語法與連線設定繁瑣 | 說「存進 SQLite 的某某資料表」 |

---

## 📐 2. 資料長什麼樣子？（直觀結構圖解）

**① 有雜訊的 CSV → 用參數讀成乾淨表格**

[![有雜訊的 CSV 用參數讀成乾淨表格](./圖解/%E8%B7%B3%E9%81%8E%E9%9B%9C%E8%A8%8A%E8%AE%80CSV.svg)](https://github.com/roberthsu2003/PythonForDataAnalysis/raw/master/pandas%E7%9A%84%E6%AA%94%E6%A1%88%E5%AD%98%E5%8F%96/%E5%9C%96%E8%A7%A3/%E8%B7%B3%E9%81%8E%E9%9B%9C%E8%A8%8A%E8%AE%80CSV.svg)<br><sub>🔍 點圖可開啟原尺寸大圖（向量圖，可再用瀏覽器放大）</sub>

**② 資料的進出口：pandas 是中間的轉運站**

[![pandas 是資料的轉運站：read_xxx 讀進、to_xxx 輸出](./圖解/%E8%B3%87%E6%96%99%E9%80%B2%E5%87%BA%E5%8F%A3.svg)](https://github.com/roberthsu2003/PythonForDataAnalysis/raw/master/pandas%E7%9A%84%E6%AA%94%E6%A1%88%E5%AD%98%E5%8F%96/%E5%9C%96%E8%A7%A3/%E8%B3%87%E6%96%99%E9%80%B2%E5%87%BA%E5%8F%A3.svg)<br><sub>🔍 點圖可開啟原尺寸大圖（向量圖，可再用瀏覽器放大）</sub>

---

## 💻 3. 核心精華操作（複製貼上即可驗證）

> 學生不需要自己寫，但只要讀懂關鍵邏輯即可。以下程式碼會自己產生範例檔，在 Colab 直接執行即可。

### 🔹 核心技巧 1：讀取「不乾淨」的 CSV——跳過雜訊、指定缺值

**商業意義**：各系統匯出的報表常常夾帶說明文字、用奇怪符號表示缺值。讀檔時一次處理好，後面的統計才不會出錯。

```python
import pandas as pd                      # 匯入 pandas

raw = """# 本報表由系統自動產生
門市,一月,二月,三月
台北店,120,NA,150
台中店,90,95,-
高雄店,80,85,88
# 資料來源：營業部"""                     # 模擬一份有註解、有缺值的報表
with open('sales.csv', 'w', encoding='utf-8') as f:
    f.write(raw)                         # 先把範例存成檔案

df = pd.read_csv('sales.csv',
                 comment='#',            # 以 # 開頭的行都是註解，直接略過
                 na_values=['NA', '-'],  # 把 'NA' 和 '-' 都視為缺值（NaN）
                 index_col='門市')       # 用「門市」這一欄當作列名牌
print(df)                                # 乾淨的 3 × 3 表格，缺值顯示為 NaN
print(df.isnull().sum())                 # 每個月有幾格缺值：二月 1、三月 1
```

### 🔹 核心技巧 2：只讀需要的欄位與筆數，大檔案分批處理

**商業意義**：證交所、交易紀錄這類動輒數十萬筆的檔案，先「只讀需要的欄」、「先看前幾筆」，必要時「分批統計」，電腦才不會卡住。

```python
import pandas as pd                      # 匯入 pandas
import numpy as np                       # 用來產生範例資料

big = pd.DataFrame({'訂單編號': range(10000),                         # 模擬 1 萬筆訂單
                    '地區': np.random.choice(['北', '中', '南'], 10000),
                    '金額': np.random.randint(100, 5000, 10000),
                    '備註': 'x'})
big.to_csv('orders.csv', index=False)    # 存成 CSV，不輸出索引

print(pd.read_csv('orders.csv', usecols=['地區', '金額'], nrows=5))   # 只讀 2 欄、前 5 筆，快速預覽

total = pd.Series(dtype=float)           # 準備一個空的累計容器
for chunk in pd.read_csv('orders.csv', chunksize=2000):   # 每次只讀 2000 筆
    total = total.add(chunk.groupby('地區')['金額'].sum(), fill_value=0)  # 各地區金額逐批累加
print(total)                             # 北、中、南三區的總金額
```

### 🔹 核心技巧 3：輸出成 Excel、CSV、JSON

**商業意義**：分析完的結果要交給不同的人——主管要 Excel、系統要 JSON、其他分析師要 CSV。一份 DataFrame，一行就能輸出成各種格式。

```python
import pandas as pd                      # 匯入 pandas

aqi = pd.DataFrame({'測站': ['新店', '大寮', '林園', '三重'],     # 模擬空氣品質資料
                    'AQI': [19, 96, 96, 24],
                    'PM2.5': [4, 34, 34, 7]})

worst = aqi[aqi['AQI'] == aqi['AQI'].max()]   # 篩選出 AQI 最高（空氣最差）的測站
print(worst)                             # 大寮、林園並列最差

aqi.to_csv('aqi.csv', index=False, encoding='utf-8-sig')  # utf-8-sig：用 Excel 直接開 CSV 也不會亂碼
aqi.to_excel('aqi.xlsx', index=False, sheet_name='AQI')   # 存成 Excel，指定工作表名稱（需安裝 openpyxl，Colab 已內建）
print(aqi.to_json(orient='records', force_ascii=False))   # 轉成「一筆一個物件」的 JSON，中文不轉碼
```

### 🔹 核心技巧 4：存進 SQLite 資料庫，再用 SQL 取出

**商業意義**：每天下載的氣象或銷售資料，存進資料庫就能長期累積，之後用一句查詢語法撈出需要的部分。

```python
import sqlite3                           # Python 內建的 SQLite 資料庫工具
import pandas as pd                      # 匯入 pandas

weather = pd.DataFrame({'縣市': ['新北市', '南投縣', '臺南市'],   # 模擬氣象觀測資料
                        '區域': ['烏來區', '仁愛鄉', '安平區'],
                        '溫度': [18.6, 6.2, 24.5]})

con = sqlite3.connect('weather.sqlite')  # 連線到資料庫檔案（不存在會自動建立）
weather.to_sql('氣象觀測資料', con, if_exists='replace', index=False)  # 寫入資料表；已存在就整個取代

cold = pd.read_sql('SELECT * FROM 氣象觀測資料 WHERE 溫度 < 20', con)  # 用 SQL 撈出溫度低於 20 度的地區
print(cold)                              # 烏來區 18.6、仁愛鄉 6.2
con.close()                              # 用完記得關閉連線
```

---

## 🤖 4. 指揮 AI 的專屬指令手冊（Prompt 實戰專區）

當你在實務工作遇到此類資料時，直接複製以下 Prompt 讓 AI 替你分析：

> **📋 AI 指揮範本（通用版）**：
>
> 「你現在是我的資深 Python 資料分析師。我有一份 **[例如：環保署空氣品質指標 CSV／中選會總統選舉 Excel／氣象局觀測 JSON]**，我想了解 **[例如：AQI 最好與最差的測站，並把結果存成 Excel 給主管]**。
>
> 以下是檔案的前 10 行：**[貼上內容]**
>
> 請你：
> 1. 使用 **pandas 的 `read_csv` / `read_excel` / `read_json`**，並說明需要哪些參數（例如 `skiprows`、`header`、`na_values`、`usecols`、`sheet_name`）。
> 2. 詳細解釋每一步的處理邏輯，以及為什麼要這樣設定參數。
> 3. 產出繁體中文說明的完整程式碼，並標註潛在的資料異常陷阱（例如：標題列不在第一行、合併儲存格、缺值寫成 NA 或 -、檔案過大、輸出 CSV 用 Excel 開啟變亂碼）。」

**🎯 情境延伸範本**（依需求替換）：

| 你想問的商業問題 | 直接對 AI 說 |
| --- | --- |
| 下載政府開放資料 | 「請用 requests 下載這個 AQI 的 CSV 網址並存檔，再用 pandas 讀取，只保留測站、AQI、PM2.5、發布時間四欄。」 |
| 讀取格式複雜的 Excel | 「這份選舉 Excel 前 2 列是標題說明、有合併儲存格，請讀取『中央』工作表並整理成一縣市一列的表格。」 |
| 處理超大檔案 | 「這個 CSV 有 500 萬筆，請分批讀取，每批 10 萬筆，統計每個商品類別的總銷售額。」 |
| 建立每日資料庫 | 「請把每次下載的氣象 JSON 轉成 DataFrame，附加（append）到 SQLite 的『氣象觀測資料』表，避免重複寫入同一時間的資料。」 |

> ⚠️ **驗收小撇步**：讀檔後請 AI 立刻印出 `df.shape`、`df.head()`、`df.dtypes`、`df.isnull().sum()`，確認「筆數、欄名、型態、缺值」四件事都正確，再往下分析。

> 🕵️ **真實陷阱案例**：本章 [README.ipynb](./README.ipynb) 讀取的 `總統.xls`，前兩列是標題與合併儲存格，直接讀會得到一堆 `Unnamed: 1`、`Unnamed: 2` 欄位。這時就要請 AI 調整 `header` 或 `skiprows`。

---

## 🎯 5. 本章檢查清單（自我驗收）

- [ ] 我知道 CSV、Excel、JSON、SQLite 分別用哪個 `read_xxx()` 讀取、哪個 `to_xxx()` 輸出。
- [ ] 我能說出 `header`、`names`、`skiprows`、`usecols`、`nrows`、`na_values` 各自解決什麼問題。
- [ ] 我知道大檔案可以用 `chunksize` 分批處理。
- [ ] 我知道輸出 CSV 給 Excel 使用時，用 `utf-8-sig` 可避免中文亂碼。
- [ ] 我能看懂 AI 生成程式中 `to_sql`、`read_sql` 的用途。
- [ ] 我會在讀檔後檢查 `shape`、`head()`、`dtypes`、缺值數量。
- [ ] 我能複製 Prompt 範本，貼上檔案前幾行，並替換成自己的業務問題。
