# 📊 📈 繪圖和視覺展示：一張好圖勝過千行數字，用 Matplotlib 讓老闆秒懂

> [!IMPORTANT]
> **本章節學習核心**：
> 1. **核心觀念**：認識圖表的「畫布（Figure）→ 畫框（Axes）→ 元素（線條、標題、座標軸）」三層結構，並知道 **折線圖、長條圖、直方圖、圓餅圖** 各自適合回答什麼問題。
> 2. **AI 協作能力**：學會用「圖表類型 + X 軸 + Y 軸 + 標題 + 顏色/標註」五個要素，向 AI 精準描述你要的圖，並能要求 AI 修改細節。
> 3. **商業決策產出**：能把營收、成績、市占率等數字轉成一眼就看懂的圖表，看出趨勢、比較高低、掌握比例。

---

> 🚀 **完整互動教學 Notebook**：
> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E7%B9%AA%E5%9C%96%E5%92%8C%E8%A6%96%E8%A6%BA%E5%B1%95%E7%A4%BA/visualization.ipynb) [開啟 visualization.ipynb](./visualization.ipynb)
>
> 📝 **課堂練習**：[subplot 多圖練習](./學生練習2.md)｜[圓餅圖練習](./學生練習3.md)｜[AI 賦能練習](./學生練習4.md)
>
> 🤖 **AI 賦能專案**：[sin / cos 互動繪圖程式](./sin_cos.md)｜[Streamlit 網頁版](./sin_cos_streamlit.md)｜[學生分數分析 student.py](./student.py)（搭配 [考試分數_3年6班.csv](./考試分數_3年6班.csv)）

---

## 📦 學生素材下載

> [!TIP]
> **📈 茶語時光：做出老闆最愛的五張圖**
>
> 年終檢討會議就在明天，老闆說：「我不要看密密麻麻的表格，給我幾張圖，一眼就知道今年哪家店最好、什麼最好賣、客人是誰、天氣對生意有沒有影響。」你決定用 Matplotlib 做出五張圖，再組成一頁儀表板。
>
> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E7%B9%AA%E5%9C%96%E5%92%8C%E8%A6%96%E8%A6%BA%E5%B1%95%E7%A4%BA/%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90/%E7%AF%84%E4%BE%8B_%E8%8C%B6%E8%AA%9E%E6%99%82%E5%85%89_%E8%80%81%E9%97%86%E6%9C%80%E6%84%9B%E7%9A%84%E4%BA%94%E5%BC%B5%E5%9C%96.ipynb) [開啟範例 Notebook](./學生素材/%E7%AF%84%E4%BE%8B_%E8%8C%B6%E8%AA%9E%E6%99%82%E5%85%89_%E8%80%81%E9%97%86%E6%9C%80%E6%84%9B%E7%9A%84%E4%BA%94%E5%BC%B5%E5%9C%96.ipynb)　｜　[⬇️ 下載本章素材 繪圖和視覺展示_學生素材.zip](https://github.com/roberthsu2003/PythonForDataAnalysis/raw/master/%E7%B9%AA%E5%9C%96%E5%92%8C%E8%A6%96%E8%A6%BA%E5%B1%95%E7%A4%BA/%E7%B9%AA%E5%9C%96%E5%92%8C%E8%A6%96%E8%A6%BA%E5%B1%95%E7%A4%BA_%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90.zip)

| 素材檔案 | 內容 |
| --- | --- |
| `門市月營收_2024.csv` | 5 家門市 2024 年每月營收（萬元） |
| `品項年銷量_2024.csv` | 10 個品項全年銷量 |
| `西門店每日氣溫與銷量_2024.csv` | 西門店每天的最高溫與芒果冰沙、熱可可杯數 |
| `會員年齡.csv` | 700 位會員的年齡 |
| `甜度偏好_2024.csv` | 一年來各甜度的杯數（抽樣） |
| `課程原始資料/` | 本章課堂 Notebook 使用的原始資料檔 |

**使用方式**：下載壓縮檔並解壓縮後，用 Jupyter 或 VS Code 開啟範例 Notebook，從上到下依序執行即可；若直接在 Colab 開啟，第一格程式會自動下載本章素材。範例最後附有練習題與參考解答。

---

## 💡 1. 為什麼需要這個觀念？（生活化比喻）

- **Matplotlib 就像「畫室」**：`Figure` 是整張**畫布**，`Axes` 是畫布上的**畫框**（一張畫布可以掛好幾個畫框），線條、標題、座標軸則是畫框裡的**顏料與標籤**。
- **選圖表就像「選交通工具」**：去的地方不同，工具就不同。
  - 想看「**隨時間的變化**」→ 折線圖（像看心電圖）
  - 想「**比較各類別大小**」→ 長條圖（像比身高）
  - 想看「**分數集中在哪個區間**」→ 直方圖（像看班上成績分布）
  - 想看「**各部分佔整體多少**」→ 圓餅圖（像切披薩）
- **在 Excel 裡**，你要點選資料、插入圖表、再一個一個調格式；用 Matplotlib，只要「描述清楚」，AI 就能一次產出，而且同樣格式可以套用到 100 份報表。

| **核心概念** | **生活化直觀比喻** | **傳統工程師痛苦點** | **AI 時代你的角色** |
| -------- | ----------- | ------------ | ------------- |
| Figure / Axes | 畫布與畫框 | 搞不清楚 `plt` 和 `ax` 寫法差在哪 | 說「一張圖」或「並排 2 張圖」即可 |
| 折線圖 `plot` | 心電圖：看起伏與趨勢 | 線條樣式代碼 `'r--o'` 難記 | 說「紅色虛線、加圓點」 |
| 長條圖 `bar` / `barh` | 比身高：誰高誰低 | 群組長條要算位移寬度 | 說「三個系列並排比較、標上數值」 |
| 直方圖 `hist` | 成績分布：多數人落在哪 | `bins` 數量不知怎麼設 | 說「分成 10 個區間」 |
| 圓餅圖 `pie` | 切披薩：各佔幾成 | 百分比格式、突出區塊參數多 | 說「顯示百分比、把最大塊拉出來」 |
| 子圖 `subplot` | 一面牆掛多幅畫 | 列、欄、位置編號容易搞混 | 說「上下兩張」或「2×2 四張」 |
| 中文字型 | 畫室缺了中文顏料 | 中文變成方塊 □□□ | 要求 AI「設定繁體中文字型」或改用英文標籤 |

---

## 📐 2. 資料長什麼樣子？（直觀結構圖解）

**① 一張圖表的組成（Figure → Axes → 元素）**

[![Matplotlib 圖表的組成：Figure、Axes 與元素](./圖解/%E5%9C%96%E8%A1%A8%E7%B5%84%E6%88%90%E5%85%83%E7%B4%A0.svg)](https://github.com/roberthsu2003/PythonForDataAnalysis/raw/master/%E7%B9%AA%E5%9C%96%E5%92%8C%E8%A6%96%E8%A6%BA%E5%B1%95%E7%A4%BA/%E5%9C%96%E8%A7%A3/%E5%9C%96%E8%A1%A8%E7%B5%84%E6%88%90%E5%85%83%E7%B4%A0.svg)<br><sub>🔍 點圖可開啟原尺寸大圖（向量圖，可再用瀏覽器放大）</sub>

**② 從數字到圖表：資料怎麼對應到座標軸**

[![兩串數字畫成折線圖](./圖解/%E6%95%B8%E5%AD%97%E5%B0%8D%E6%87%89%E5%BA%A7%E6%A8%99%E8%BB%B8.svg)](https://github.com/roberthsu2003/PythonForDataAnalysis/raw/master/%E7%B9%AA%E5%9C%96%E5%92%8C%E8%A6%96%E8%A6%BA%E5%B1%95%E7%A4%BA/%E5%9C%96%E8%A7%A3/%E6%95%B8%E5%AD%97%E5%B0%8D%E6%87%89%E5%BA%A7%E6%A8%99%E8%BB%B8.svg)<br><sub>🔍 點圖可開啟原尺寸大圖（向量圖，可再用瀏覽器放大）</sub>

> 💡 **記憶口訣**：X 軸放「分類或時間」，Y 軸放「要比較的數字」。兩串資料的**筆數必須一樣多**，否則畫不出來。

---

## 💻 3. 核心精華操作（複製貼上即可驗證）

> 學生不需要自己寫，但只要讀懂關鍵邏輯即可。範例標籤使用英文，避免 Colab 缺少中文字型時顯示成方塊。

### 🔹 核心技巧 1：標準畫圖四步驟（折線圖）

**商業意義**：觀察「每日溫度」、「每月營收」這類隨時間變化的數據，最適合用折線圖看出趨勢與異常高低點。

```python
import matplotlib.pyplot as plt          # 匯入繪圖套件，簡稱 plt

days = [1, 2, 3, 4, 5, 6, 7]             # X 軸：一週的第幾天
store_a = [12, 22, 25, 20, 18, 30, 28]   # Y 軸：A 店每日營收（萬元）
store_b = [15, 14, 18, 22, 25, 24, 27]   # Y 軸：B 店每日營收（萬元）

fig = plt.figure(figsize=(8, 4))         # 步驟 1：建立畫布，寬 8 吋、高 4 吋
ax = fig.add_subplot(1, 1, 1)            # 步驟 2：在畫布上放 1 個畫框（1 列 1 欄的第 1 個）
ax.plot(days, store_a, 'r-o', label='Store A')   # 步驟 3：畫紅色實線＋圓點，命名為 Store A
ax.plot(days, store_b, 'g--', label='Store B')   #          畫綠色虛線，命名為 Store B
ax.set_title('Daily Revenue')            # 加上圖表標題
ax.set_xlabel('Day')                     # X 軸名稱
ax.set_ylabel('Revenue (10k)')           # Y 軸名稱
ax.grid(axis='y')                        # 只加水平格線，方便對照數值
ax.legend()                              # 顯示圖例，分辨兩條線
plt.show()                               # 步驟 4：顯示圖表
```

### 🔹 核心技巧 2：長條圖＋數值標註

**商業意義**：比較各產品、各門市、各業務的業績高低，長條圖最直觀；在長條上標出數字，簡報時聽眾不用再去對座標軸。

```python
import matplotlib.pyplot as plt          # 匯入繪圖套件

fruits = ['apple', 'banana', 'orange', 'tomato', 'guava']   # X 軸：產品類別
sales = [5000, 7000, 3000, 4000, 6000]                       # Y 軸：銷售額

fig, ax = plt.subplots(figsize=(8, 4))   # 一次建立畫布與畫框的簡便寫法
ax.bar(fruits, sales, color='steelblue') # 畫長條圖，指定顏色
for i, v in enumerate(sales):            # 逐一取出「第幾根長條」與「它的數值」
    ax.annotate(str(v), (i, v + 100), ha='center')  # 在長條上方 100 的位置寫數字，水平置中
ax.set_title('Fruit Sales')              # 圖表標題
ax.set_ylim(0, 8000)                     # Y 軸範圍設 0～8000，留空間放數字
plt.show()                               # 顯示圖表
```

### 🔹 核心技巧 3：一張畫布放多張圖（subplot）＋ 直方圖

**商業意義**：簡報時常需要「並排比較」，例如左邊放成績分布、右邊放各科平均；一張圖就能說完一個故事。

```python
import numpy as np                       # 匯入 NumPy 產生範例資料
import matplotlib.pyplot as plt          # 匯入繪圖套件

scores = np.random.randint(40, 101, size=50)    # 隨機產生 50 位學生的分數（40～100 分）
subjects = ['chinese', 'english', 'math']       # 三個科目
averages = [78, 72, 81]                         # 三科平均

fig = plt.figure(figsize=(10, 4))        # 建立一張寬一點的畫布
ax1 = fig.add_subplot(1, 2, 1)           # 1 列 2 欄的第 1 個位置（左邊）
ax1.hist(scores, bins=6, color='orange', edgecolor='black')  # 直方圖：把分數切成 6 個區間，數每區有幾人
ax1.set_title('Score Distribution')      # 左圖標題

ax2 = fig.add_subplot(1, 2, 2)           # 1 列 2 欄的第 2 個位置（右邊）
ax2.barh(subjects, averages, color='teal')       # 水平長條圖：比較各科平均
ax2.set_title('Average by Subject')      # 右圖標題
plt.tight_layout()                       # 自動調整間距，避免兩張圖的文字重疊
plt.show()                               # 顯示圖表
```

### 🔹 核心技巧 4：圓餅圖顯示市占比例

**商業意義**：回答「各品牌佔了市場幾成？」這類「部分佔整體」的問題。注意：類別超過 5～6 個時，圓餅圖會變得難讀，改用長條圖更好。

```python
import matplotlib.pyplot as plt          # 匯入繪圖套件

brands = ['Nokia', 'Samsung', 'Apple', 'Lumia']  # 品牌名稱
share = [20, 30, 45, 10]                          # 各品牌銷量

fig, ax = plt.subplots(figsize=(5, 5))   # 建立正方形畫布，圓餅才不會變橢圓
ax.pie(share,                            # 要畫的數值
       labels=brands,                    # 每一塊的名稱
       autopct='%1.1f%%',                # 自動計算並顯示百分比（小數 1 位）
       explode=[0, 0, 0.1, 0],           # 把第 3 塊（Apple）往外拉出，強調重點
       startangle=90)                    # 從 12 點鐘方向開始畫
ax.set_title('Market Share')             # 圖表標題
plt.show()                               # 顯示圖表
```

---

## 🤖 4. 指揮 AI 的專屬指令手冊（Prompt 實戰專區）

當你在實務工作遇到此類資料時，直接複製以下 Prompt 讓 AI 替你分析：

> **📋 AI 指揮範本（通用版）**：
>
> 「你現在是我的資深 Python 資料分析師。我有一份 **[例如：3 年 6 班學生的語文、數學、英語、物理、化學成績 CSV]**，我想了解 **[例如：每位學生的強弱科目，以及全班各科的分數分布]**。
>
> 請你：
> 1. 使用 **Matplotlib** 繪製 **[圖表類型：折線圖／長條圖／直方圖／圓餅圖]**，X 軸是 **[ ]**、Y 軸是 **[ ]**，標題是 **[ ]**。
> 2. 詳細解釋為什麼選這種圖表，以及每一步的繪圖邏輯（畫布、畫框、座標軸、圖例）。
> 3. 產出繁體中文說明的完整程式碼，**正確設定繁體中文字型**（使用 `mplfonts`：`%pip install -q mplfonts` 後執行 `use_font("Noto Sans CJK TC")`），並標註潛在的陷阱（例如：X 與 Y 筆數不一致、中文變方塊、類別太多導致標籤重疊）。」

**🎯 情境延伸範本**（依需求替換）：

| 你想問的商業問題 | 直接對 AI 說 |
| --- | --- |
| 兩家店的業績走勢 | 「請用折線圖比較 A、B 兩店 30 天營收，A 用紅色實線、B 用藍色虛線，加上圖例與水平格線。」 |
| 多年度產品比較 | 「請畫群組長條圖，X 軸是 5 種產品，每種產品並排顯示 2023、2024、2025 三年的銷售額，長條上標註數字。」 |
| 一頁看完全部 | 「請用 2×2 的子圖，分別畫出營收趨勢、產品占比圓餅圖、客單價直方圖、各區業績長條圖。」 |
| 做成互動工具 | 「請用 numpy + matplotlib 做一個可用滑桿調整振幅與頻率的 sin/cos 波形圖，並改寫成 Streamlit 網頁版。」 |

> ⚠️ **驗收小撇步**：拿到圖表後，檢查四件事——**標題說得出重點嗎？座標軸有名稱與單位嗎？圖例分得出每條線嗎？中文有沒有變成方塊？**

---

## 🎯 5. 本章檢查清單（自我驗收）

- [ ] 我能理解 **Figure（畫布）** 與 **Axes（畫框）** 的差異，知道一張畫布可以放多張圖。
- [ ] 我能根據問題選對圖表：趨勢用折線圖、比較用長條圖、分布用直方圖、比例用圓餅圖。
- [ ] 我能看懂 AI 生成程式中 `plot`、`bar`、`hist`、`pie`、`subplot`、`legend` 的用途。
- [ ] 我知道 X 軸和 Y 軸的資料筆數必須一樣多。
- [ ] 遇到中文變方塊時，我知道要請 AI 設定中文字型。
- [ ] 我能用「圖表類型 + X 軸 + Y 軸 + 標題 + 顏色/標註」五要素描述我要的圖。
- [ ] 我能複製 Prompt 範本並替換成自己的業務問題。
