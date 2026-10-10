# 📊 🖼️ 直接使用 pandas 繪製圖表：表格算完一行出圖，再用 seaborn 讓統計圖更有說服力

> [!IMPORTANT]
> **本章節學習核心**：
> 1. **核心觀念**：DataFrame 與 Series 內建 `.plot()`，**索引自動變成 X 軸、每一欄自動變成一條線或一組長條**，省去手動整理座標；再搭配 seaborn 一行畫出帶有「誤差範圍」的統計圖，以及在圖上標註重要事件。
> 2. **AI 協作能力**：學會先請 AI「把資料整理成適合畫圖的形狀」（例如交叉表、百分比表），再指定圖表類型與標註，讓分析與視覺化一氣呵成。
> 3. **商業決策產出**：能畫出「各星期用餐人數比例」、「不同時段小費比例比較」、「股價走勢與金融危機事件標註」這類能直接放進簡報的圖表，並存成高解析度圖檔。

---

> 🚀 **完整互動教學 Notebook**：
> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E7%9B%B4%E6%8E%A5%E4%BD%BF%E7%94%A8pandas%E7%B9%AA%E5%88%B6%E5%9C%96%E8%A1%A8/README.ipynb) [開啟 README.ipynb](./README.ipynb)
>
> 📝 **延伸範例**：[test.ipynb：2008 金融海嘯 S&P 500 事件標註圖](./test.ipynb)（使用 [spx.csv](./spx.csv)）

---

## 📦 學生素材下載

> [!TIP]
> **🖼️ 茶語時光：一行程式畫出年度簡報圖**
>
> 尾牙前要做年度簡報。上一章你學會用 groupby 算出各種統計，這次老闆要的是「圖」：全年營收走勢、颱風和演唱會的影響、不同時段客人點什麼、會員是不是比較會花錢。好消息是——**表格整理好之後，pandas 一行就能畫圖**。
>
> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E7%9B%B4%E6%8E%A5%E4%BD%BF%E7%94%A8pandas%E7%B9%AA%E5%88%B6%E5%9C%96%E8%A1%A8/%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90/%E7%AF%84%E4%BE%8B_%E8%8C%B6%E8%AA%9E%E6%99%82%E5%85%89_%E4%B8%80%E8%A1%8C%E7%95%AB%E5%87%BA%E5%B9%B4%E5%BA%A6%E7%B0%A1%E5%A0%B1%E5%9C%96.ipynb) [開啟範例 Notebook](./學生素材/%E7%AF%84%E4%BE%8B_%E8%8C%B6%E8%AA%9E%E6%99%82%E5%85%89_%E4%B8%80%E8%A1%8C%E7%95%AB%E5%87%BA%E5%B9%B4%E5%BA%A6%E7%B0%A1%E5%A0%B1%E5%9C%96.ipynb)　｜　[⬇️ 下載本章素材 直接使用pandas繪制圖表_學生素材.zip](https://github.com/roberthsu2003/PythonForDataAnalysis/raw/master/%E7%9B%B4%E6%8E%A5%E4%BD%BF%E7%94%A8pandas%E7%B9%AA%E5%88%B6%E5%9C%96%E8%A1%A8/%E7%9B%B4%E6%8E%A5%E4%BD%BF%E7%94%A8pandas%E7%B9%AA%E5%88%B6%E5%9C%96%E8%A1%A8_%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90.zip)

| 素材檔案 | 內容 |
| --- | --- |
| `每日營收_2024.csv` | 2024 年每天 × 5 家門市的杯數、營收、最高溫與特殊事件（颱風、演唱會、節日、活動） |
| `訂單明細_2024-07.csv` | 7 月份的訂單明細（約 4 萬筆） |
| `課程原始資料/` | 本章課堂 Notebook 使用的原始資料檔 |

**使用方式**：下載壓縮檔並解壓縮後，用 Jupyter 或 VS Code 開啟範例 Notebook，從上到下依序執行即可；若直接在 Colab 開啟，第一格程式會自動下載本章素材。範例最後附有練習題與參考解答。

---

## 💡 1. 為什麼需要這個觀念？（生活化比喻）

- **用 Matplotlib 畫圖像「從零開始組裝家具」**：要自己拿出 X 座標、Y 座標、一條一條畫線。**用 pandas `.plot()` 像「買組好的家具」**：表格長什麼樣子，圖就長什麼樣子——索引是 X 軸、欄位是每條線。
- **「先整理表格、再畫圖」就像「先備好菜、再擺盤」**：想畫「各星期不同人數用餐的比例」，就先做出「星期 × 人數」的交叉表，再一行 `.plot.bar()`。
- **seaborn 像「附贈統計顧問的畫家」**：畫平均值長條圖時，會自動加上**誤差線（信賴區間）**，提醒你「這個平均值有多可靠」。
- **圖上標註（annotate）像「便利貼」**：在股價圖上貼一張「雷曼兄弟倒閉」的便利貼，聽眾立刻理解那次暴跌的原因。

| **核心概念** | **生活化直觀比喻** | **傳統工程師痛苦點** | **AI 時代你的角色** |
| -------- | ----------- | ------------ | ------------- |
| `df.plot()` / `s.plot()` | 組好的家具：表格即圖表 | 手動拆出 X、Y 資料 | 說「每一欄畫一條線」 |
| `.plot.bar()` / `barh(stacked=True)` | 並排或堆疊的長條 | 堆疊長條要計算累加位置 | 說「堆疊長條圖、水平方向」 |
| `pd.crosstab` | 計次表（劃正字） | 先統計再畫，步驟繁瑣 | 說「先做星期 × 人數的交叉表」 |
| 百分比正規化 `div` | 把次數換成佔比 | 各列總數不同無法直接比較 | 說「每一列換算成百分比」 |
| `sns.barplot` | 附統計顧問的畫家 | 誤差線要自己算 | 說「畫平均值長條圖並顯示信賴區間」 |
| `hist` / `density` | 分數分布、平滑的分布曲線 | 區間數 bins 難拿捏 | 說「切 50 個區間，再疊一條密度曲線」 |
| `annotate` / `savefig` | 便利貼／存成照片 | 箭頭座標與 dpi 設定繁瑣 | 說「在某日期加箭頭標註、存成 300 dpi PNG」 |

---

## 📐 2. 資料長什麼樣子？（直觀結構圖解）

**從原始紀錄 → 交叉表 → 百分比表 → 長條圖**

```text
原始 tips 資料（一列一筆帳單）      交叉表 pd.crosstab(day, size)        百分比表（每列加總 = 100%）
day   size  tip                     size   2    3    4    5              size    2     3     4     5
Sun    2   1.01                     Fri   16    1    1    0              Fri   0.89  0.06  0.06  0.00
Sun    3   1.66        ──►          Sat   53   18   13    1     ──►      Sat   0.62  0.21  0.15  0.01
Sat    2   3.50                     Sun   39   15   18    3              Sun   0.52  0.20  0.24  0.04
...  (244 筆)                       Thur  48    4    5    1              Thur  0.83  0.07  0.09  0.02

                                                                             ▼  .plot.bar()
                                               X 軸 = 索引（星期）、每一欄（人數）= 一組顏色的長條
```

---

## 💻 3. 核心精華操作（複製貼上即可驗證）

> 學生不需要自己寫，但只要讀懂關鍵邏輯即可。資料直接從本 Repo 的 GitHub 讀取，在 Colab 直接執行即可。

### 🔹 核心技巧 1：DataFrame 一行畫折線圖與堆疊長條圖

**商業意義**：多個產品、多家分店的數據放在同一張表裡，一行就能畫出比較圖，不用一條一條手動加。

```python
import numpy as np                       # 匯入 NumPy 產生範例資料
import pandas as pd                      # 匯入 pandas
import matplotlib.pyplot as plt          # 匯入繪圖套件（用來顯示與排版）

np.random.seed(0)                        # 固定亂數，結果可重現
sales = pd.DataFrame(np.random.randint(50, 150, size=(6, 3)),       # 6 個月 × 3 家分店的營收
                     index=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],  # 索引 → 自動成為 X 軸
                     columns=['Store A', 'Store B', 'Store C'])         # 每一欄 → 自動成為一條線

fig, axes = plt.subplots(1, 2, figsize=(12, 4))          # 一張畫布、左右兩個畫框
sales.plot(ax=axes[0], marker='o', title='Monthly Revenue')         # 左圖：折線圖，每家分店一條線
sales.plot.bar(ax=axes[1], stacked=True, title='Stacked Revenue')   # 右圖：堆疊長條，看每月總營收與各店貢獻
plt.tight_layout()                       # 自動調整間距
plt.show()
```

### 🔹 核心技巧 2：交叉表 → 百分比 → 長條圖

**商業意義**：直接比較「次數」會被樣本數誤導（週六客人本來就多），換算成「百分比」才能公平比較各星期的用餐人數結構。

```python
import pandas as pd                      # 匯入 pandas
import matplotlib.pyplot as plt          # 匯入繪圖套件

url = ('https://raw.githubusercontent.com/roberthsu2003/PythonForDataAnalysis/master/'
       '%E7%9B%B4%E6%8E%A5%E4%BD%BF%E7%94%A8pandas%E7%B9%AA%E5%88%B6%E5%9C%96%E8%A1%A8/tips.csv')
tips = pd.read_csv(url)                  # 讀取 tips 餐廳小費資料集

counts = pd.crosstab(tips['day'], tips['size'])   # 交叉表：每個星期 × 每種用餐人數，各有幾筆
counts = counts.loc[:, 2:5]              # 只保留 2～5 人的欄位（1 人與 6 人樣本太少）
pcts = counts.div(counts.sum(axis=1), axis=0)     # 每一列除以該列總數 → 轉成百分比
print(pcts.round(2))

pcts.plot.bar(title='Party size by day (share)')  # 一行畫出分組長條圖
plt.ylabel('Share')                      # Y 軸名稱
plt.show()
```

### 🔹 核心技巧 3：seaborn 統計長條圖（含信賴區間）與分布圖

**商業意義**：比較「午餐 vs. 晚餐」的平均小費比例時，誤差線告訴你差異是否「夠明顯」；直方圖則讓你看出小費比例集中在哪個範圍、有沒有極端值。

```python
import pandas as pd                      # 匯入 pandas
import seaborn as sns                    # 匯入 seaborn 統計繪圖套件
import matplotlib.pyplot as plt          # 匯入繪圖套件

url = ('https://raw.githubusercontent.com/roberthsu2003/PythonForDataAnalysis/master/'
       '%E7%9B%B4%E6%8E%A5%E4%BD%BF%E7%94%A8pandas%E7%B9%AA%E5%88%B6%E5%9C%96%E8%A1%A8/tips.csv')
tips = pd.read_csv(url)                  # 讀取 tips 資料集
tips['tip_pct'] = tips['tip'] / (tips['total_bill'] - tips['tip'])   # 小費比例 = 小費 ÷ 餐費（帳單扣掉小費）

fig, axes = plt.subplots(1, 2, figsize=(12, 4))      # 左右兩張圖
sns.barplot(data=tips, x='tip_pct', y='day', hue='time', orient='h', ax=axes[0])  # 平均小費比例：依星期 × 時段，黑線是信賴區間
axes[0].set_title('Average tip % by day and time')
tips['tip_pct'].plot.hist(bins=50, ax=axes[1], title='Distribution of tip %')    # 直方圖：小費比例的分布
plt.tight_layout()
plt.show()
```

### 🔹 核心技巧 4：在走勢圖上標註重要事件並存檔

**商業意義**：簡報時，一張「標註了事件」的走勢圖勝過十張投影片。例如在營收圖上標出「新品上市」、「疫情爆發」，因果關係一目了然。

```python
from datetime import datetime            # 用來建立日期
import pandas as pd                      # 匯入 pandas
import matplotlib.pyplot as plt          # 匯入繪圖套件

url = ('https://raw.githubusercontent.com/roberthsu2003/PythonForDataAnalysis/master/'
       '%E7%9B%B4%E6%8E%A5%E4%BD%BF%E7%94%A8pandas%E7%B9%AA%E5%88%B6%E5%9C%96%E8%A1%A8/spx.csv')
spx = pd.read_csv(url, index_col=0, parse_dates=True)['SPX']   # 讀取 S&P 500 指數，日期欄當索引並轉成日期格式

fig, ax = plt.subplots(figsize=(10, 5))  # 建立畫布與畫框
spx.loc['2007':'2010'].plot(ax=ax, style='k-')   # 只畫 2007～2010 年的走勢

events = [(datetime(2007, 10, 11), 'Peak of bull market'),   # 要標註的事件：(日期, 說明)
          (datetime(2008, 3, 12), 'Bear Stearns Fails'),
          (datetime(2008, 9, 15), 'Lehman Bankruptcy')]
for date, label in events:
    ax.annotate(label,                                   # 標註文字
                xy=(date, spx.asof(date) + 75),          # 箭頭指向的位置（該日指數上方一點）
                xytext=(date, spx.asof(date) + 225),     # 文字擺放的位置（再更上方）
                arrowprops=dict(facecolor='black', headwidth=4, width=2, headlength=4),
                horizontalalignment='left', verticalalignment='top')
ax.set_title('Important dates in the 2008-2009 financial crisis')
plt.savefig('spx_crisis.png', dpi=300, bbox_inches='tight')  # 存成 300 dpi 高解析度圖檔，裁掉多餘白邊
plt.show()
```

---

## 🤖 4. 指揮 AI 的專屬指令手冊（Prompt 實戰專區）

當你在實務工作遇到此類資料時，直接複製以下 Prompt 讓 AI 替你分析：

> **📋 AI 指揮範本（通用版）**：
>
> 「你現在是我的資深 Python 資料分析師。我有一份 **[例如：餐廳帳單資料，欄位有帳單金額、小費、是否吸菸、星期、時段、用餐人數]**，我想了解 **[例如：各星期的用餐人數結構，以及午餐與晚餐的小費比例差異]**。
>
> 請你：
> 1. 先用 **pandas** 把資料整理成適合畫圖的形狀（例如 crosstab 交叉表、轉成百分比），再用 **`df.plot()` 或 seaborn** 繪製 **[圖表類型]**。
> 2. 詳細解釋每一步的處理邏輯與指標公式，並說明圖中的誤差線、顏色、座標軸代表什麼。
> 3. 產出繁體中文說明的完整程式碼，正確設定繁體中文字型，存成 300 dpi 的 PNG，並標註潛在的陷阱（例如：直接比較次數而非比例、樣本太少的組別、日期沒有轉成日期格式導致 X 軸亂掉）。」

**🎯 情境延伸範本**（依需求替換）：

| 你想問的商業問題 | 直接對 AI 說 |
| --- | --- |
| 產品銷售結構 | 「請做『月份 × 產品類別』的銷售額表，畫成堆疊長條圖，並另畫一張各類別佔比的百分比堆疊圖。」 |
| 兩組平均值比較 | 「請用 seaborn 畫出會員與非會員的平均客單價長條圖（含信賴區間），並用白話解釋差異是否明顯。」 |
| 事件影響說明 | 「請畫出公司股價近 3 年走勢，並在新品發表、財報公布、疫情爆發三個日期加上箭頭標註。」 |
| 一頁儀表板 | 「請用 2×2 子圖：營收折線、品類堆疊長條、客單價直方圖、各區平均長條圖，存成一張 PNG 放進簡報。」 |

> ⚠️ **驗收小撇步**：看到長條圖時先問自己——Y 軸是「次數」還是「比例」？不同組別的樣本數差很多時，**比例才是公平的比較**。

> 🕵️ **真實陷阱案例**：本章的「小費比例」定義為 **小費 ÷（帳單 − 小費）**，而[群組資料和群組運算](../群組資料和群組運算/README.md)一章用的是 **小費 ÷ 帳單**。兩種算法數字不同，跟 AI 溝通時一定要講清楚「公式是什麼」。

---

## 🎯 5. 本章檢查清單（自我驗收）

- [ ] 我知道 DataFrame `.plot()` 會把「索引當 X 軸、每一欄當一個系列」。
- [ ] 我能分辨分組長條圖與堆疊長條圖（`stacked=True`）的用途。
- [ ] 我能請 AI 先用 `crosstab` 統計次數，再換算成百分比畫圖。
- [ ] 我能看懂 seaborn 長條圖上的誤差線代表平均值的可靠程度。
- [ ] 我能請 AI 在走勢圖上用 `annotate` 標註事件，並用 `savefig` 存成高解析度圖檔。
- [ ] 我會先確認指標的計算公式，再請 AI 畫圖。
- [ ] 我能複製 Prompt 範本並替換成自己的業務問題。
