# 📊 🎨 視覺化表格：讓數字自己「亮起來」，報表重點一眼就看到

> [!IMPORTANT]
> **本章節學習核心**：
> 1. **核心觀念**：用 pandas 的 **Styler（表格造型師）** 為 DataFrame 加上千分位、百分比、顏色標記、漸層色與資料條，等同 Excel 的「儲存格格式」與「設定格式化的條件」。
> 2. **AI 協作能力**：學會用「什麼條件 → 什麼顏色」的規則句型（例如「不及格標紅字」、「每欄最高分標深藍底」）指揮 AI 產出格式化表格，並匯出成帶顏色的 Excel。
> 3. **商業決策產出**：能做出主管一眼就看懂的報表——異常值自動標紅、最佳表現自動標亮、數值大小用色階與長條呈現。

---

> 🚀 **完整互動教學 Notebook**：
> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E8%A6%96%E8%A6%BA%E5%8C%96%E8%A1%A8%E6%A0%BC/README.ipynb) [開啟 README.ipynb](./README.ipynb)
>
> ⚠️ **注意**：GitHub 網頁預覽 Notebook 時**不會顯示表格顏色**，請點上方 Colab 徽章開啟執行，才看得到完整效果。

---

## 📦 學生素材下載

> [!TIP]
> **🎨 茶語時光：做一份「會發亮」的 KPI 報表**
>
> 每季的營運會議，區經理都要盯著一張密密麻麻的數字表找問題。老闆說：「能不能讓沒達標的自動變紅、表現最好的自動亮起來？我要一眼就看到重點。」你決定用 pandas 的 Styler 幫表格「化妝」，最後匯出成帶顏色的 Excel。
>
> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E8%A6%96%E8%A6%BA%E5%8C%96%E8%A1%A8%E6%A0%BC/%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90/%E7%AF%84%E4%BE%8B_%E8%8C%B6%E8%AA%9E%E6%99%82%E5%85%89_%E6%9C%83%E7%99%BC%E4%BA%AE%E7%9A%84KPI%E9%80%B1%E5%A0%B1.ipynb) [開啟範例 Notebook](./%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90/%E7%AF%84%E4%BE%8B_%E8%8C%B6%E8%AA%9E%E6%99%82%E5%85%89_%E6%9C%83%E7%99%BC%E4%BA%AE%E7%9A%84KPI%E9%80%B1%E5%A0%B1.ipynb)　｜　[⬇️ 下載本章素材 視覺化表格_學生素材.zip](https://github.com/roberthsu2003/PythonForDataAnalysis/raw/master/%E8%A6%96%E8%A6%BA%E5%8C%96%E8%A1%A8%E6%A0%BC/%E8%A6%96%E8%A6%BA%E5%8C%96%E8%A1%A8%E6%A0%BC_%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90.zip)

| 素材檔案 | 內容 |
| --- | --- |
| `門市KPI_2024Q2.csv` | 第二季各門市的營收目標、實際營收、去年同期、來客數、評分、客訴、新會員 |
| `品項月銷量_2024.csv` | 10 個品項 × 12 個月的杯數 |

**使用方式**：下載壓縮檔並解壓縮後，用 Jupyter 或 VS Code 開啟範例 Notebook，從上到下依序執行即可；若直接在 Colab 開啟，第一格程式會自動下載本章素材。範例開頭有「🗺️ 今日任務地圖」，最後的練習區每題都附「半成品程式 → ✅ 自動檢查 → 🔑 折疊解答」，寫完馬上知道自己對不對。

---

## 💡 1. 為什麼需要這個觀念？（生活化比喻）

- **DataFrame 是「素顏的表格」，Styler 是「化妝師」**：化妝不會改變一個人（資料本身不變），只改變外觀（顯示方式）。所以 `df.style` 之後的表格是用來「看」與「匯出」的，不是拿來再計算的。
- **格式化（format）就像「換衣服」**：同樣是 `1000.23`，可以穿成 `1,000.230`、`$1,000`、`100.0%`。
- **條件標色就像「螢光筆」**：老師改考卷時，把不及格的分數用紅筆圈起來——你只要告訴 AI「什麼條件用什麼顏色」。
- **漸層色與資料條就像「溫度計」**：顏色越深、長條越長，代表數字越大，不用細看數字就能比大小。

| **核心概念** | **生活化直觀比喻** | **傳統工程師痛苦點** | **AI 時代你的角色** |
| -------- | ----------- | ------------ | ------------- |
| `style.format` | 幫數字換衣服（千分位、小數位） | 格式字串 `'{:,.0f}'` 難記 | 說「千分位、不要小數」 |
| `highlight_max` / `min` / `null` | 螢光筆標出最高、最低、空白 | 要指定 axis 方向 | 說「每一欄的最高分」或「每一列」 |
| `map` / `apply` 自訂規則 | 自己定義的批改規則 | 回傳 CSS 字串的寫法陌生 | 用白話說「小於 60 標紅字」 |
| `background_gradient` | 溫度計色階 | 色票名稱（cmap）難選 | 說「綠色越深代表越高」 |
| `bar` | 儲存格內的迷你長條圖 | 正負值對齊設定複雜 | 說「負數往左紅色、正數往右藍色」 |
| `hide` / `concat` | 遮住不需要的欄位／在表尾加總計列 | 欄位不一致無法串接 | 說「隱藏某些欄、最後加總分與平均列」 |
| `to_excel` / `to_html` | 把化好妝的表格寄出去 | 匯出後顏色不見 | 要求「匯出成保留顏色的 Excel」 |

---

## 📐 2. 資料長什麼樣子？（直觀結構圖解）

[![Styler：同一份資料，化妝前後的差別](./圖解/Styler%E5%8C%96%E5%A6%9D%E5%89%8D%E5%BE%8C.svg)](https://github.com/roberthsu2003/PythonForDataAnalysis/raw/master/%E8%A6%96%E8%A6%BA%E5%8C%96%E8%A1%A8%E6%A0%BC/%E5%9C%96%E8%A7%A3/Styler%E5%8C%96%E5%A6%9D%E5%89%8D%E5%BE%8C.svg)<br><sub>🔍 點圖可開啟原尺寸大圖（向量圖，可再用瀏覽器放大）</sub>

> 💡 **記憶口訣**：`df.style` 開頭 → 一路用「.」串接各種化妝步驟 → 最後顯示或匯出。資料本身**從頭到尾都沒被改變**。

---

## 💻 3. 核心精華操作（複製貼上即可驗證）

> 學生不需要自己寫，但只要讀懂關鍵邏輯即可。請在 Colab 或 Jupyter 中執行，才能看到顏色效果（每段最後一行會顯示表格）。

### 🔹 核心技巧 1：數字格式化——千分位、小數位、百分比

**商業意義**：營收 `1234567.891` 對主管來說很難讀，`1,234,568` 一眼就懂；成長率 `0.1234` 顯示成 `12.3%` 才符合商業習慣。

```python
import pandas as pd                      # 匯入 pandas

df = pd.DataFrame({'門市': ['台北', '台中', '高雄'],
                   '營收': [1234567.891, 987654.321, 456789.123],
                   '成長率': [0.1234, -0.0567, 0.0821]})

styled = (df.style
          .format({'營收': '{:,.0f}',     # 營收：千分位、不顯示小數
                   '成長率': '{:.1%}'})   # 成長率：轉成百分比、小數 1 位
          .hide(axis='index')            # 隱藏左側 0、1、2 的列號，讓報表更乾淨
          .set_caption('各門市營收報表'))  # 表格標題
styled                                   # 在 Notebook 中顯示化好妝的表格
```

### 🔹 核心技巧 2：內建螢光筆——標出最高、最低與缺值

**商業意義**：成績單或業績表中，誰最好、誰最差、哪裡漏填，用顏色標出來，比用眼睛逐格比對快得多。

```python
import numpy as np                       # 匯入 NumPy
import pandas as pd                      # 匯入 pandas

scores = pd.DataFrame({'國文': [85, 58, 90], '英文': [45, 88, np.nan], '數學': [92, 60, 55]},
                      index=['小明', '小華', '小美'])

styled = (scores.style
          .highlight_max(axis=0, props='color:white; background-color:darkblue;')  # 每一欄（每科）最高分：深藍底白字
          .highlight_min(axis=0, props='background-color:#ffe6e6;')                # 每一欄最低分：淡紅底
          .highlight_null(color='yellow')                                          # 缺值（沒考試）：黃底
          .format('{:.0f}', na_rep='缺考'))                                        # 整數顯示，缺值顯示「缺考」
styled
```

### 🔹 核心技巧 3：自訂條件標色——不及格標紅字

**商業意義**：每家公司的規則都不同（業績未達 80% 標紅、庫存低於安全量標橘），自訂規則讓表格自動「提醒」你該注意的地方。

```python
import pandas as pd                      # 匯入 pandas

scores = pd.DataFrame({'國文': [85, 58, 90], '英文': [45, 88, 72], '數學': [92, 60, 55]},
                      index=['小明', '小華', '小美'])

def fail_red(v):                         # 自訂規則：一次處理「一個儲存格」的值
    return 'color:red; font-weight:bold;' if v < 60 else None   # 小於 60 回傳紅色粗體的樣式，否則不變

styled = (scores.style
          .map(fail_red)                 # 把規則套用到每一個儲存格（舊版 pandas 寫作 applymap）
          .set_caption('紅字＝不及格'))
styled
```

### 🔹 核心技巧 4：色階、資料條與匯出 Excel

**商業意義**：上百列的數字表，用色階和資料條一眼就看出分布；匯出成 Excel 後，顏色會一起保留，直接寄給同事或主管。

```python
import numpy as np                       # 匯入 NumPy
import pandas as pd                      # 匯入 pandas

np.random.seed(0)                        # 固定亂數，每次結果都一樣
sales = pd.DataFrame(np.random.randint(50, 200, size=(6, 3)),   # 6 個月 × 3 個產品的銷量
                     index=['1月', '2月', '3月', '4月', '5月', '6月'],
                     columns=['產品A', '產品B', '產品C'])

styled = (sales.style
          .background_gradient(subset=['產品A', '產品B'], cmap='Greens')  # 產品 A、B：數字越大綠色越深
          .bar(subset=['產品C'], color='#d65f5f'))                       # 產品 C：儲存格內畫紅色資料條
styled.to_excel('sales_report.xlsx')     # 匯出成保留背景顏色的 Excel（需 openpyxl，Colab 已內建）
styled
```

---

## 🤖 4. 指揮 AI 的專屬指令手冊（Prompt 實戰專區）

當你在實務工作遇到此類資料時，直接複製以下 Prompt 讓 AI 替你分析：

> **📋 AI 指揮範本（通用版）**：
>
> 「你現在是我的資深 Python 資料分析師。我有一份 **[例如：天龍國小各班 3 位學生 × 5 科成績的 DataFrame]**，我想做一份 **[例如：給家長會看的成績報表]**。
>
> 請你：
> 1. 使用 **pandas Styler** 進行格式化，規則如下：**[例如：分數取整數；小於 60 紅色粗體；每科最高分深藍底白字；缺考顯示『缺考』並黃底；表尾加上總分與平均列]**。
> 2. 詳細解釋每一個樣式方法的作用，以及 axis 方向代表「每一欄」還是「每一列」。
> 3. 產出繁體中文說明的完整程式碼，並匯出成保留顏色的 Excel；同時標註潛在陷阱（例如：Styler 物件不能再拿來計算、GitHub 預覽不顯示顏色、舊版 pandas 用 applymap 新版用 map）。」

**🎯 情境延伸範本**（依需求替換）：

| 你想問的商業問題 | 直接對 AI 說 |
| --- | --- |
| 業績達成率報表 | 「請把達成率顯示成百分比，低於 80% 標紅底、超過 120% 標綠底，營收加千分位。」 |
| 找出異常值 | 「請把每一欄中位於前 15%（最高的那些）的數值標黃色，並隱藏不需要的欄位。」 |
| 正負值一目了然 | 「請用資料條呈現每月損益，負數向左紅色、正數向右藍色，0 對齊中間。」 |
| 多班級 Excel | 「請產生 5 個班級的隨機成績，每班一個工作表存進同一個 Excel，並套用不及格紅字的格式。」 |

> ⚠️ **驗收小撇步**：格式化只改變「顯示」，請確認原始 DataFrame 的數值沒有被改掉（例如 `df['營收'].sum()` 結果和格式化前相同）。

---

## 🎯 5. 本章檢查清單（自我驗收）

- [ ] 我理解 Styler 只改變「外觀」，不會改變資料本身。
- [ ] 我能請 AI 用 `format` 加上千分位、百分比、指定小數位數。
- [ ] 我能分辨內建的 `highlight_max`、`highlight_min`、`highlight_null`、`background_gradient`、`bar` 各自的效果。
- [ ] 我能用「什麼條件 → 什麼顏色」的句型描述自訂規則。
- [ ] 我知道 GitHub 上看不到表格顏色，要在 Colab / Jupyter 執行才看得到。
- [ ] 我知道可以把格式化後的表格匯出成保留顏色的 Excel。
- [ ] 我能複製 Prompt 範本並替換成自己的業務問題。
