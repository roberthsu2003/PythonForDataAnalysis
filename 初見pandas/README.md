# 📊 🐼 初見 pandas：把資料變成「會說話的 Excel 表」，分析從這裡起飛

> [!IMPORTANT]
> **本章節學習核心**：
> 1. **核心觀念**：認識 pandas 兩大主角——**Series（一欄有標籤的資料）** 與 **DataFrame（一整張有欄名、有列號的表格）**，並理解「索引（index）」就是每一列的名牌。
> 2. **AI 協作能力**：學會用「欄位名稱」與「列的條件」跟 AI 溝通，例如「新增總分欄」、「只看汐止區的資料」，讓 AI 精準產出表格操作程式。
> 3. **商業決策產出**：能把 CSV / JSON 原始資料轉成表格，快速算出每人總分、各區合計，並找出缺漏資料（NaN）。

---

> 🚀 **完整互動教學 Notebook**：
> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E5%88%9D%E8%A6%8Bpandas/README.ipynb) [開啟 README.ipynb](./README.ipynb)
>
> 🔍 **觀念對照**：[NumPy 與 pandas 的差異範例 lesson12_4.ipynb](./lesson12_4.ipynb)
>
> 📝 **課後練習解答**：[homework1](./homework1.ipynb)（工廠清冊轉 Series）｜[homework2](./homework2.ipynb)（工廠清冊轉 DataFrame）｜[homework3](./homework3.ipynb)（人口密度表）｜[homework4](./homework4.ipynb)（公共自行車 JSON）

---

## 📦 學生素材下載

> [!TIP]
> **🐼 茶語時光：新品上市週的第一份 pandas 報表**
>
> 2024 年 4 月 1 日，新品「芋頭鮮奶」上市！行銷部想知道：新品賣得怎樣？有沒有搶走其他飲料的生意？每杯賺多少？你第一次用 pandas，把菜單、門市資料與兩週的銷量做成表格來回答。
>
> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E5%88%9D%E8%A6%8Bpandas/%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90/%E7%AF%84%E4%BE%8B_%E8%8C%B6%E8%AA%9E%E6%99%82%E5%85%89_%E6%96%B0%E5%93%81%E4%B8%8A%E5%B8%82%E9%80%B1%E7%9A%84%E7%AC%AC%E4%B8%80%E4%BB%BD%E5%A0%B1%E8%A1%A8.ipynb) [開啟範例 Notebook](./學生素材/%E7%AF%84%E4%BE%8B_%E8%8C%B6%E8%AA%9E%E6%99%82%E5%85%89_%E6%96%B0%E5%93%81%E4%B8%8A%E5%B8%82%E9%80%B1%E7%9A%84%E7%AC%AC%E4%B8%80%E4%BB%BD%E5%A0%B1%E8%A1%A8.ipynb)　｜　[⬇️ 下載本章素材 初見pandas_學生素材.zip](https://github.com/roberthsu2003/PythonForDataAnalysis/raw/master/%E5%88%9D%E8%A6%8Bpandas/%E5%88%9D%E8%A6%8Bpandas_%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90.zip)

| 素材檔案 | 內容 |
| --- | --- |
| `菜單.csv` | 10 個品項的價格與成本 |
| `門市.csv` | 5 家門市的基本資料 |
| `兩週品項銷量.json` | 芋頭鮮奶上市前一週與上市當週，全品牌各品項杯數 |
| `信義店日報_新品週.json` | 信義店新品週每天的杯數、營收、來客數 |
| `課程原始資料/` | 本章課堂 Notebook 使用的原始資料檔 |

**使用方式**：下載壓縮檔並解壓縮後，用 Jupyter 或 VS Code 開啟範例 Notebook，從上到下依序執行即可；若直接在 Colab 開啟，第一格程式會自動下載本章素材。範例開頭有「🗺️ 今日任務地圖」，最後的練習區每題都附「半成品程式 → ✅ 自動檢查 → 🔑 折疊解答」，寫完馬上知道自己對不對。

---

## 💡 1. 為什麼需要這個觀念？（生活化比喻）

- **NumPy 陣列像「蛋盒」**：只能放同一種東西、格子只有編號。**pandas DataFrame 像「Excel 工作表」**：每一欄可以放不同型態（姓名是文字、分數是數字、是否及格是 True/False），而且欄有欄名、列有列名。
- **Series 就像「Excel 的一欄」**：左邊是名牌（index），右邊是數值。例如「台北 → 35000、桃園 → 71000」。
- **DataFrame 就像「很多欄排在一起」**：每一欄都是一個 Series，共用同一組列名牌。
- **索引對齊就像「按名牌配對」**：兩個 Series 相加時，pandas 會先找「名牌一樣」的配對再相加，而不是按位置。名牌對不上的，就給你一個空值 `NaN`（Not a Number，代表「這格沒有資料」）。

| **核心概念** | **生活化直觀比喻** | **傳統工程師痛苦點** | **AI 時代你的角色** |
| -------- | ----------- | ------------ | ------------- |
| Series | Excel 的一欄，左邊有名牌 | 分不清 index 和 values | 說「以縣市為索引、人口為值」 |
| DataFrame | 整張 Excel 工作表 | 用 list / dict 組表格容易對錯欄 | 說清楚「欄位有哪些、一列代表什麼」 |
| 索引 index | 每一列的名牌（學號、統編） | 索引重複或排序錯亂 | 指定「用哪一欄當索引」 |
| `loc` 取列 | 按名牌找人 | `loc` / `iloc` / `[]` 搞混 | 說「取出學號 1 的資料」 |
| 新增 / 刪除欄位 | 在 Excel 插入或刪除一欄 | 欄位長度不一致就報錯 | 說「新增總分欄＝五科加總」 |
| `NaN` 缺值 | 表格中的空白格 | 沒發現缺值，平均算錯 | 要求 AI「先列出有缺值的欄位」 |

---

## 📐 2. 資料長什麼樣子？（直觀結構圖解）

**① Series：一欄有名牌的資料**

[![Series：一欄有名牌的資料](./圖解/Series%E7%B5%90%E6%A7%8B.svg)](https://github.com/roberthsu2003/PythonForDataAnalysis/raw/master/%E5%88%9D%E8%A6%8Bpandas/%E5%9C%96%E8%A7%A3/Series%E7%B5%90%E6%A7%8B.svg)<br><sub>🔍 點圖可開啟原尺寸大圖（向量圖，可再用瀏覽器放大）</sub>

**② DataFrame：從 Python 字典變成表格，再加上新欄位**

[![Python 字典轉成 DataFrame 並新增欄位](./圖解/%E5%AD%97%E5%85%B8%E8%AE%8ADataFrame.svg)](https://github.com/roberthsu2003/PythonForDataAnalysis/raw/master/%E5%88%9D%E8%A6%8Bpandas/%E5%9C%96%E8%A7%A3/%E5%AD%97%E5%85%B8%E8%AE%8ADataFrame.svg)<br><sub>🔍 點圖可開啟原尺寸大圖（向量圖，可再用瀏覽器放大）</sub>

**③ 索引對齊：按名牌配對，對不上就是 NaN**

[![兩個 Series 依名牌配對相加，配不到就是 NaN](./圖解/%E7%B4%A2%E5%BC%95%E5%B0%8D%E9%BD%8A.svg)](https://github.com/roberthsu2003/PythonForDataAnalysis/raw/master/%E5%88%9D%E8%A6%8Bpandas/%E5%9C%96%E8%A7%A3/%E7%B4%A2%E5%BC%95%E5%B0%8D%E9%BD%8A.svg)<br><sub>🔍 點圖可開啟原尺寸大圖（向量圖，可再用瀏覽器放大）</sub>

---

## 💻 3. 核心精華操作（複製貼上即可驗證）

> 學生不需要自己寫，但只要讀懂關鍵邏輯即可。

### 🔹 核心技巧 1：Series——有名牌的一欄資料

**商業意義**：各縣市人口、各產品銷量、各科成績這類「名稱 → 數值」的資料，用 Series 存放，可以直接用名稱查詢與篩選。

```python
import pandas as pd                      # 匯入 pandas，習慣簡稱 pd

# 用字典建立 Series：key 變成名牌（index），value 變成值
pop = pd.Series({'台北': 35000, '桃園': 71000, '台中': 16000, '高雄': 5000})
pop.name = '縣市人口'                    # 幫這欄資料取個名字
pop.index.name = '縣市'                  # 幫名牌取個名字

print(pop['桃園'])                       # 用名牌查詢：71000
print(pop[pop > 20000])                  # 篩選人口超過 2 萬的縣市：台北、桃園
print(pop * 1.05)                        # 整欄一起運算：每個縣市都乘以 1.05（假設成長 5%）
```

### 🔹 核心技巧 2：建立 DataFrame 成績單，並新增「總分」、「平均」欄

**商業意義**：這是所有報表的原型——「一列一個對象（學生、員工、門市），一欄一個指標」。加上總分與平均欄，就能排名與比較。

```python
import pandas as pd                      # 匯入 pandas

data = {                                 # 用字典準備資料：每個 key 是一個欄位
    '國文': [85, 72, 90],
    '英文': [78, 88, 65],
    '數學': [92, 60, 80],
}
scores = pd.DataFrame(data, index=['小明', '小華', '小美'])  # 指定每一列的名牌是學生姓名
scores.index.name = '姓名'               # 列名牌的標題

scores['總分'] = scores.sum(axis=1)      # 新增「總分」欄：axis=1 代表每一列（每位學生）橫著加
scores['平均'] = scores[['國文', '英文', '數學']].mean(axis=1).round(1)  # 只用三科算平均，取到小數 1 位
print(scores)                            # 印出整張成績單

print(scores.loc['小華'])                # 用 loc 依名牌取出「小華」那一列
print(scores['數學'].mean())             # 取出「數學」這一欄並算全班平均：77.33...
```

### 🔹 核心技巧 3：條件篩選與欄位改名（以自行車站點為例）

**商業意義**：從上百個站點中「只看某一區」，並把英文代碼欄位改成看得懂的中文，是整理政府開放資料最常見的第一步。

```python
import pandas as pd                      # 匯入 pandas

# 模擬「新北市公共自行車」JSON 中的 records 資料（一筆一個站點）
records = [
    {'sno': '1001', 'sarea': '新店區', 'sna': '大鵬華城',   'tot': '38', 'sbi': '22'},
    {'sno': '1002', 'sarea': '汐止區', 'sna': '汐止火車站', 'tot': '56', 'sbi': '2'},
    {'sno': '1003', 'sarea': '汐止區', 'sna': '汐止區公所', 'tot': '46', 'sbi': '18'},
]
df = pd.DataFrame(records)               # 一行把「清單裡放字典」轉成表格
df.columns = ['編號', '區域', '站名', '全部數量', '可借']   # 把英文代碼欄名改成中文

xizhi = df[df['區域'] == '汐止區']        # 篩選：只留下「區域」等於汐止區的列
print(xizhi)

total = xizhi['全部數量'].astype(int).sum()   # ⚠️ 原始資料是文字，要先 astype(int) 轉成整數才能加總
print('汐止區可停車總數：', total)       # 結果：102
```

### 🔹 核心技巧 4：索引自動對齊與缺值 NaN

**商業意義**：合併兩份名單時（例如今年與去年的各縣市業績），pandas 會「按名稱配對」而不是按順序，避免張冠李戴；配不上的地方會出現 NaN，提醒你資料有缺。

```python
import pandas as pd                      # 匯入 pandas

this_year = pd.Series({'台北': 350, '桃園': 710, '高雄': 50})   # 今年業績
last_year = pd.Series({'高雄': 40, '台北': 300, '花蓮': 20})    # 去年業績（順序不同、縣市也不完全一樣）

growth = this_year - last_year           # 依「縣市名稱」配對相減，而不是依位置
print(growth)                            # 台北 50、高雄 10；桃園與花蓮配不到 → NaN
print(growth.isnull())                   # 檢查哪些是缺值（True 代表缺）
```

---

## 🤖 4. 指揮 AI 的專屬指令手冊（Prompt 實戰專區）

當你在實務工作遇到此類資料時，直接複製以下 Prompt 讓 AI 替你分析：

> **📋 AI 指揮範本（通用版）**：
>
> 「你現在是我的資深 Python 資料分析師。我有一份 **[例如：新北市食品工廠清冊 CSV，欄位有工廠名稱、登記編號、地址、統編、經緯度]**，我想了解 **[例如：以統一編號為索引排序，並找出統編介於 01000070～01001000 的工廠]**。
>
> 請你：
> 1. 使用 **pandas 的 Series / DataFrame** 進行處理，並說明「一列代表什麼、索引是哪一欄」。
> 2. 詳細解釋每一步的處理邏輯，包括欄位改名、篩選條件、型態轉換。
> 3. 產出繁體中文說明的完整程式碼，並標註潛在的資料異常陷阱（例如：數字被存成文字、索引重複、缺值 NaN、檔案最後幾列是說明文字而非資料）。」

**🎯 情境延伸範本**（依需求替換）：

| 你想問的商業問題 | 直接對 AI 說 |
| --- | --- |
| 做一份成績單 | 「請建立 50 位學生 × 5 科的 DataFrame，學號為索引，新增總分與平均欄，並找出平均最高的 5 位。」 |
| 原始資料轉表格 | 「這是一份 JSON，資料在 `result → records` 裡，請轉成 DataFrame，並把英文欄位改成中文。」 |
| 只看某一區 | 「請篩選出『汐止區』的所有站點，並計算全部車位、可借、可還的總數。」 |
| 比較兩年資料 | 「我有今年和去年各縣市的業績 Series，請計算成長量，並列出哪些縣市只出現在其中一年。」 |

> ⚠️ **驗收小撇步**：請 AI 印出 `df.shape`（幾列幾欄）、`df.head()`（前 5 列）與 `df.dtypes`（每欄型態），確認筆數正確、欄名正確、數字欄真的是數字。

> 🕵️ **真實陷阱案例**：本章 [homework3](./homework3.ipynb) 的人口密度 CSV，檔案最後幾列是「資料來源說明」而不是數據；[homework4](./homework4.ipynb) 的自行車 JSON 中，車位數量全部是文字。兩者都必須先清理，才能正確統計。

---

## 🎯 5. 本章檢查清單（自我驗收）

- [ ] 我能理解 **Series（一欄）** 與 **DataFrame（整張表）** 的差異。
- [ ] 我知道 **index（列名牌）** 與 **columns（欄名）** 分別是什麼。
- [ ] 我能看懂 AI 生成程式中 `pd.DataFrame()`、`loc`、`df['欄名']`、`astype()`、`sum(axis=1)` 的用途。
- [ ] 我理解兩個 Series 運算時會「按名牌配對」，配不上的會變成 NaN。
- [ ] 我會請 AI 用 `shape`、`head()`、`dtypes` 幫我檢查資料。
- [ ] 我能複製 Prompt 範本並替換成自己的業務問題。
