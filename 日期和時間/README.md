# 📊 📅 日期和時間：讓資料「懂得時間」，看出每月趨勢、成長率與長期走勢

> [!IMPORTANT]
> **本章節學習核心**：
> 1. **核心觀念**：把文字日期轉成真正的「時間型態」，並以時間當索引，就能「按年月取資料」、「把每日資料彙總成每月（resample）」、「和上期比較（shift）」、「算移動平均看長期趨勢（rolling）」，還能處理時區與季度。
> 2. **AI 協作能力**：學會用「時間頻率」的語言指揮 AI——「每日 → 每月加總」、「和上個月比的成長率」、「60 日移動平均」、「轉成台北時間」，並提醒 AI 使用新版 pandas 的頻率代碼。
> 3. **商業決策產出**：能把每日營收整理成月報、計算月增率（MoM）、用移動平均過濾股價雜訊、判斷長期趨勢方向。

<!-- ai-bridge:start -->
> [!TIP]
> 🤖 **不寫程式也能先練一次**：本章的技巧，在「零程式碼・AI 協作」的實戰範例裡會用到。
> 可以先在 Colab 指揮 AI 做一遍，再回來看本章，理解程式是怎麼寫的：
>
> - [範例 08 外送訂單](../AI協作資料分析_12個範例/08_delivery_time/README.md)：時區轉換與 rolling 移動平均
> - [範例 12 共享單車](../AI協作資料分析_12個範例/12_bike_capstone/README.md)：日期時間拆解
<!-- ai-bridge:end -->

---

> 🚀 **完整互動教學 Notebook**：
> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E6%97%A5%E6%9C%9F%E5%92%8C%E6%99%82%E9%96%93/README.ipynb) [開啟 README.ipynb](./README.ipynb)
>
> 📈 **範例資料**：[stock_px_2.csv](./stock_px_2.csv)（2003 年起 AAPL、MSFT、XOM 與 S&P 500 的每日收盤價）

---

## 📦 學生素材下載

> [!TIP]
> **📅 茶語時光：兩年營收趨勢與外送時區之謎**
>
> 品牌成立滿兩年，董事會想看：「今年比去年成長多少？哪個月最好？颱風到底讓我們少賺多少？」同時，外送部門抱怨：「平台報表說我們凌晨 4 點最忙，這怎麼可能？」你要用 pandas 的時間工具，一次解開這些問題。
>
> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E6%97%A5%E6%9C%9F%E5%92%8C%E6%99%82%E9%96%93/%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90/%E7%AF%84%E4%BE%8B_%E8%8C%B6%E8%AA%9E%E6%99%82%E5%85%89_%E5%85%A9%E5%B9%B4%E7%87%9F%E6%94%B6%E8%88%87%E5%A4%96%E9%80%81%E6%99%82%E5%8D%80.ipynb) [開啟範例 Notebook](./學生素材/%E7%AF%84%E4%BE%8B_%E8%8C%B6%E8%AA%9E%E6%99%82%E5%85%89_%E5%85%A9%E5%B9%B4%E7%87%9F%E6%94%B6%E8%88%87%E5%A4%96%E9%80%81%E6%99%82%E5%8D%80.ipynb)　｜　[⬇️ 下載本章素材 日期和時間_學生素材.zip](https://github.com/roberthsu2003/PythonForDataAnalysis/raw/master/%E6%97%A5%E6%9C%9F%E5%92%8C%E6%99%82%E9%96%93/%E6%97%A5%E6%9C%9F%E5%92%8C%E6%99%82%E9%96%93_%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90.zip)

| 素材檔案 | 內容 |
| --- | --- |
| `每日營收_2023-2024.csv` | 2023～2024 兩年、5 家門市的每日杯數與營收（日期格式是「2024/1/5」的文字） |
| `外送訂單_UTC_2024-09.csv` | 9 月外送平台訂單，時間以 UTC（世界標準時間）儲存 |
| `課程原始資料/` | 本章課堂 Notebook 使用的原始資料檔 |

**使用方式**：下載壓縮檔並解壓縮後，用 Jupyter 或 VS Code 開啟範例 Notebook，從上到下依序執行即可；若直接在 Colab 開啟，第一格程式會自動下載本章素材。範例最後附有練習題與參考解答。

---

## 💡 1. 為什麼需要這個觀念？（生活化比喻）

- **文字日期 vs. 時間型態，就像「寫在紙上的日期」vs.「行事曆上的日期」**：紙上的 `'2021-01-05'` 只是字，電腦不知道它是星期幾、下個月是哪天；轉成時間型態後，就像放進行事曆，可以算天數、找月底、按月分組。
- **以時間為索引，就像「日記本」**：翻到「2021 年 3 月」就能直接看到那個月的所有紀錄（`ts['2021-03']`）。
- **resample 就像「把日記整理成月報」**：每天的流水帳（高頻率）加總成每月一筆（低頻率）叫 **降頻**；反過來把每月資料展開成每天（需要補值）叫 **升頻**。
- **shift 就像「把上個月的成績單擺在旁邊對照」**：資料往下挪一格，就能和上一期相減或相除，算出成長率。
- **rolling 移動平均就像「看最近 N 天的平均體重」**：單日數字起伏很大，但「最近 60 天平均」能濾掉雜訊，看出真正的趨勢。

| **核心概念** | **生活化直觀比喻** | **傳統工程師痛苦點** | **AI 時代你的角色** |
| -------- | ----------- | ------------ | ------------- |
| `pd.to_datetime` | 紙上日期 → 行事曆日期 | 日期格式五花八門（7/6/2011、民國年） | 告訴 AI「原始日期長什麼樣子」 |
| 時間索引與切片 | 日記本按年月翻頁 | 日期是文字時無法用範圍篩選 | 說「取出 2021 年第一季」 |
| `date_range` / 頻率代碼 | 自動產生行事曆 | 頻率代碼難記且新舊版不同 | 說「每週三」、「每月最後一個工作日」 |
| `resample` | 日記 → 月報（降頻）／月報 → 日記（升頻） | 區間包含左邊還右邊搞不清 | 說「每日加總成每月」、「缺的日子沿用前一天」 |
| `shift` / `pct_change` | 和上期成績單對照 | 自己寫迴圈算成長率易出錯 | 說「計算月增率」 |
| `rolling` | 最近 N 天平均體重 | 前 N−1 天沒有值的原因不懂 | 說「60 日移動平均，資料不足 10 天就不算」 |
| `tz_localize` / `tz_convert` | 標上時區／換算成當地時間 | 跨國資料時間差 8 小時 | 說「原始是 UTC，轉成台北時間」 |
| `Period` 時期 | 「2023 年第 1 季」這種一整段時間 | 會計年度與季度換算 | 說「以 3 月為年度結束的季度」 |

---

## 📐 2. 資料長什麼樣子？（直觀結構圖解）

**① 時間序列：時間當索引**

[![文字日期轉成時間索引](./圖解/%E6%99%82%E9%96%93%E7%95%B6%E7%B4%A2%E5%BC%95.svg)](https://github.com/roberthsu2003/PythonForDataAnalysis/raw/master/%E6%97%A5%E6%9C%9F%E5%92%8C%E6%99%82%E9%96%93/%E5%9C%96%E8%A7%A3/%E6%99%82%E9%96%93%E7%95%B6%E7%B4%A2%E5%BC%95.svg)<br><sub>🔍 點圖可開啟原尺寸大圖（向量圖，可再用瀏覽器放大）</sub>

**② resample 降頻 / shift 成長率 / rolling 移動平均**

[![resample 降頻、shift 計算月增率、rolling 移動平均](./圖解/%E9%99%8D%E9%A0%BB%E8%88%87%E6%9C%88%E5%A2%9E%E7%8E%87.svg)](https://github.com/roberthsu2003/PythonForDataAnalysis/raw/master/%E6%97%A5%E6%9C%9F%E5%92%8C%E6%99%82%E9%96%93/%E5%9C%96%E8%A7%A3/%E9%99%8D%E9%A0%BB%E8%88%87%E6%9C%88%E5%A2%9E%E7%8E%87.svg)<br><sub>🔍 點圖可開啟原尺寸大圖（向量圖，可再用瀏覽器放大）</sub>

---

## 💻 3. 核心精華操作（複製貼上即可驗證）

> 學生不需要自己寫，但只要讀懂關鍵邏輯即可。程式碼使用新版 pandas 頻率代碼（`'ME'` 月底、`'YE'` 年底），Colab 可直接執行。

### 🔹 核心技巧 1：文字轉日期，取出年、月、星期

**商業意義**：訂單日期轉成時間型態後，才能回答「週末業績比平日好嗎？」、「哪個月是旺季？」這類問題。

```python
import pandas as pd                      # 匯入 pandas

orders = pd.DataFrame({'訂單日期': ['2021-01-02', '2021-01-05', '2021-02-13', '2021-03-20'],
                       '金額': [1200, 800, 1500, 2000]})

orders['訂單日期'] = pd.to_datetime(orders['訂單日期'])   # 把文字轉成真正的時間型態
orders['月份'] = orders['訂單日期'].dt.month             # .dt 取出時間的各部分：月份
orders['星期'] = orders['訂單日期'].dt.day_name()        # 星期幾（英文名稱）
orders['是否週末'] = orders['訂單日期'].dt.dayofweek >= 5  # 0=星期一 … 5=星期六、6=星期日
print(orders)

days = pd.Timestamp('2021-03-20') - pd.Timestamp('2021-01-02')   # 兩個日期相減 → 一段時間
print('相隔天數：', days.days)            # 77 天
```

### 🔹 核心技巧 2：時間索引——按年月取資料、每日彙總成每月

**商業意義**：每天一筆的營收、來客數，老闆通常只想看「每月總計」或「每週平均」；用時間索引加 resample，一行搞定月報。

```python
import numpy as np                       # 匯入 NumPy
import pandas as pd                      # 匯入 pandas

np.random.seed(0)                        # 固定亂數
days = pd.date_range('2021-01-01', '2021-06-30', freq='D')        # 產生每天的日期（共 181 天）
daily = pd.Series(np.random.randint(80, 120, len(days)), index=days)   # 每日營收，日期當索引

print(daily['2021-03'].head())           # 直接用「年-月」字串取出 3 月的資料
print(daily['2021-04-01':'2021-04-07'])  # 用日期範圍切出 4 月第一週

monthly = daily.resample('ME').sum()     # 降頻：每日 → 每月加總（'ME' = 月底，新版 pandas 寫法）
print(monthly)
print(daily.resample('W').mean().head()) # 每週平均（以週日為一週結束）
```

### 🔹 核心技巧 3：shift 計算月增率（MoM）

**商業意義**：「這個月比上個月成長了多少？」是每份月報必備的指標。shift 把上期數字挪到同一列，相除就能得到成長率。

```python
import pandas as pd                      # 匯入 pandas

monthly = pd.Series([310, 336, 372, 350, 401, 420],
                    index=pd.date_range('2021-01-31', periods=6, freq='ME'))   # 6 個月的月營收

report = pd.DataFrame({'營收': monthly,
                       '上月營收': monthly.shift(1)})   # shift(1)：資料往下挪一格 → 每列旁邊就是上個月
report['月增率'] = report['營收'] / report['上月營收'] - 1   # 月增率 = 本月 ÷ 上月 − 1
report['月增率(內建)'] = monthly.pct_change()             # pandas 內建的一行寫法，結果相同
print(report.round(3))                   # 第一個月沒有上月可比 → NaN
```

### 🔹 核心技巧 4：rolling 移動平均——濾掉雜訊看長期趨勢

**商業意義**：股價、日營收每天上下震盪，移動平均線能看出「整體是向上還是向下」，也是技術分析中最基本的工具。

```python
import pandas as pd                      # 匯入 pandas
import matplotlib.pyplot as plt          # 匯入繪圖套件

url = ('https://raw.githubusercontent.com/roberthsu2003/PythonForDataAnalysis/master/'
       '%E6%97%A5%E6%9C%9F%E5%92%8C%E6%99%82%E9%96%93/stock_px_2.csv')
px = pd.read_csv(url, parse_dates=True, index_col=0)   # 讀取股價：第一欄日期轉成時間並當索引
aapl = px['AAPL'].resample('B').ffill()  # 統一成「工作日」頻率，沒交易的日子沿用前一天收盤價

fig, ax = plt.subplots(figsize=(10, 4))
aapl.plot(ax=ax, alpha=0.4, label='Daily close')              # 原始每日收盤價（較淡）
aapl.rolling(100).mean().plot(ax=ax, label='100-day MA')       # 100 日移動平均：前 99 天資料不足 → NaN
aapl.rolling(250, min_periods=10).mean().plot(ax=ax, label='250-day MA')  # 250 日均線，至少 10 天資料就開始計算
ax.set_title('AAPL close price & moving averages')
ax.legend()
plt.show()
```

---

## 🤖 4. 指揮 AI 的專屬指令手冊（Prompt 實戰專區）

當你在實務工作遇到此類資料時，直接複製以下 Prompt 讓 AI 替你分析：

> **📋 AI 指揮範本（通用版）**：
>
> 「你現在是我的資深 Python 資料分析師。我有一份 **[例如：門市每日營收 CSV，日期欄格式是 2021/1/5，另有門市、營收欄位]**，我想了解 **[例如：每月營收、月增率，以及 30 日移動平均的趨勢]**。
>
> 請你：
> 1. 使用 **pandas 的 `to_datetime`、時間索引、`resample`、`shift` / `pct_change`、`rolling`** 進行處理，並使用**新版 pandas 的頻率代碼**（月底用 `'ME'`、年底用 `'YE'`、小時用 `'h'`、分鐘用 `'min'`）。
> 2. 詳細解釋每一步的處理邏輯與計算公式（例如月增率 = 本月 ÷ 上月 − 1），並說明 NaN 出現的原因。
> 3. 產出繁體中文說明的完整程式碼，並標註潛在的資料異常陷阱（例如：日期格式不一致、民國年、日月順序顛倒、時區差 8 小時、某些日子沒有資料、日期重複）。」

**🎯 情境延伸範本**（依需求替換）：

| 你想問的商業問題 | 直接對 AI 說 |
| --- | --- |
| 做月報與季報 | 「請把每日營收彙總成每月總和與每季平均，並計算月增率與年增率（YoY）。」 |
| 週末效應 | 「請新增『星期幾』欄位，比較週一到週日的平均營收，畫成長條圖。」 |
| 看長期趨勢 | 「請畫出股價收盤價，並疊上 20 日、60 日、240 日移動平均線，用白話說明目前趨勢。」 |
| 補齊缺漏日期 | 「資料有些日子沒有紀錄，請補齊成每天一筆，缺的日子營收補 0，庫存沿用前一天。」 |
| 跨國時間 | 「這份網站流量紀錄的時間是 UTC，請轉成台北時間後，再統計每小時的流量。」 |

> ⚠️ **驗收小撇步**：請 AI 印出 `df.index.min()`、`df.index.max()` 與 `df.index.is_unique`，確認資料的起訖日期正確、沒有重複的日期；resample 後檢查「月份數量」是否符合預期。

> 🕵️ **真實陷阱案例**：網路上和 AI 常給出 `resample('M')`、`freq='A-DEC'`、`freq='4H'`、`'90T'` 這類舊寫法，在**新版 pandas 會直接報錯**（例如：`'M' is no longer supported for offsets. Please use 'ME' instead.`）。本章 [README.ipynb](./README.ipynb) 已全部改為新寫法（`'ME'`、`'BME'`、`'Y-DEC'`、`'h'`、`'min'`）。請 AI 寫程式時，記得指定「使用新版 pandas 的頻率代碼」。

---

## 🎯 5. 本章檢查清單（自我驗收）

- [ ] 我理解文字日期必須先用 `pd.to_datetime` 轉成時間型態，才能做時間運算。
- [ ] 我能請 AI 用時間索引「按年、按月、按日期範圍」取出資料。
- [ ] 我能分辨 **降頻**（每日 → 每月，要加總或平均）與 **升頻**（每月 → 每日，要補值）。
- [ ] 我能說明 `shift` 如何用來計算月增率，以及第一期為什麼是 NaN。
- [ ] 我理解 `rolling` 移動平均的意義，以及前 N−1 筆為什麼沒有值。
- [ ] 我知道新版 pandas 的頻率代碼（`'ME'`、`'YE'`、`'h'`、`'min'`）和舊版不同。
- [ ] 我能複製 Prompt 範本並替換成自己的業務問題。
