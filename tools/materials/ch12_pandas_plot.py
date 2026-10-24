"""第 12 章 pandas 直接繪圖：用真實開放資料一行出圖——折線、長條＋標註、堆疊面積、seaborn 箱型圖、熱力圖、散佈圖。"""
from nbtools import md, code, setup_cell, font_cell, header, exercises, copy_real

CHAPTER = '直接使用pandas繪制圖表'
NOTEBOOK = '範例_一行畫出台灣的六個故事.ipynb'
SOURCES = ['youbike', 'boxoffice', 'power_city', 'aqi', 'mrt']


def build(out):
    files = [copy_real(out, k) for k in SOURCES]
    desc = [(files[0], '臺北市 YouBike 每月騎乘次數（Big5）'),
            (files[1], '文化部全國電影票房（JSON）'),
            (files[2], '台電各縣市每月售電量'),
            (files[3], '環境部近一年每日 AQI'),
            (files[4], '臺北捷運 2026 年 3 月各站每小時進出站人次')]

    cells = [
        header(CHAPTER, NOTEBOOK, '🖼️ 一行程式，畫出台灣的六個故事',
               '前面幾章你已經用過 YouBike、電影票房、台電用電、空氣品質、捷運這幾份真實資料。'
               '這一章是「**成果發表會**」：每份資料整理好之後，只要在表格後面加上 `.plot()`，一行就能畫出圖；'
               '再搭配 **seaborn** 畫出統計圖。你要做出六張可以直接放進簡報的圖，每一張講一個台灣的故事。',
               desc, SOURCES),
        setup_cell(CHAPTER, files),
        font_cell(),
        md('''
## 故事 1：YouBike 騎乘量一路往上——`Series.plot()` 折線圖

**白話說明**：DataFrame / Series 後面直接接 `.plot()`，**索引自動變成 X 軸、數值變成 Y 軸**。索引是日期時，X 軸就會是時間軸。
'''),
        code('''
import pandas as pd
import matplotlib.pyplot as plt

bike = pd.read_csv('臺北市YouBike每月使用量.csv', encoding='cp950')
bike['月份'] = pd.to_datetime(bike['西元年'].astype(str) + '-' + bike['月份'].astype(str) + '-01')
rides = bike.set_index('月份')['臺北市YouBike每月使用量（次數）'] / 1e4       # 單位：萬次

ax = rides.plot(figsize=(11, 4), color='#F39C12', linewidth=2.5, title='臺北市 YouBike 每月騎乘次數（萬次）')
ax.set_xlabel('')
plt.show()
'''),
        md('''
## 故事 2：疫情讓電影院少了一半的觀眾——長條圖＋標註

**白話說明**：`plot.bar()` 畫長條；`ax.annotate` 在圖上加說明文字和箭頭，**讓讀者一眼看到重點**。
'''),
        code('''
import json

with open('全國電影票房_2016至今.json', encoding='utf-8-sig') as f:
    movies = pd.DataFrame(json.load(f)['List'])
movies = movies[movies['TotalAmounts'] > 0]
movies['年'] = movies['ReleaseDate'].str[:4].astype(int)

by_year = movies[movies['年'].between(2016, 2025)].groupby('年')['TotalAmounts'].sum() / 1e8   # 億元
colors = ['#C0392B' if y in (2020, 2021) else '#7F8C8D' for y in by_year.index]
ax = by_year.plot.bar(figsize=(10, 4.5), color=colors, title='全台電影票房（依上映年份，億元）', rot=0)
ax.annotate('疫情：電影院\\n關閉、限制座位', xy=(4.5, 55), xytext=(6.5, 95), ha='center',
            arrowprops=dict(arrowstyle='->', color='#C0392B'), color='#C0392B')
ax.set_xlabel('')
plt.show()
'''),
        md('''
> 💡 **看懂結果**：2017～2019 年每年約 100 億，2020、2021 年掉到 50 億左右——**少了一半**；2025 年才回到快 90 億。
'''),
        md('''
## 故事 3：台灣的電都去哪了？——堆疊面積圖

**白話說明**：`plot.area()` 畫**堆疊面積圖**：每一層是一種用電類別，整體高度是總用電，適合看「總量與組成一起變化」。
'''),
        code('''
power = pd.read_csv('台電各縣市用電統計.csv', thousands=',', usecols=range(5)).dropna(subset=['年月'])
power['年'] = (power['年月'] // 100 + 1911).astype(int)
mix = (power[power['年'].between(2016, 2025)]
       .pivot_table(index='年', columns='用電性質', values='售電量(度)', aggfunc='sum') / 1e8)   # 億度
mix = mix[['工業', '住宅', '服務業', '農林漁牧']]

ax = mix.plot.area(figsize=(10, 4.5), colormap='tab20c', alpha=0.9, title='全台售電量組成（億度）')
ax.legend(loc='upper left', ncol=4)
plt.show()
'''),
        md('''
> 💡 **看懂結果**：最下面的**工業**是最大的一層，2016 到 2022 年成長了將近兩成（半導體等產業擴廠），近幾年持平；**住宅**用電則是穩定地慢慢增加（十年多了約 15%），服務業幾乎沒變。
'''),
        md('''
## 故事 4：冬天的空氣比較差——seaborn 箱型圖

**白話說明**：**箱型圖**一次畫出「中位數（中間那條線）、大部分資料的範圍（箱子）、極端值（點）」，最適合比較好幾組資料的**分布**。seaborn 只要指定 `x`、`y`。
'''),
        code('''
import seaborn as sns

aqi = pd.read_csv('日空氣品質指標_近一年.csv', parse_dates=['monitordate'])
aqi['月'] = aqi['monitordate'].dt.month

plt.figure(figsize=(11, 4.5))
sns.boxplot(data=aqi, x='月', y='aqi', color='#AED6F1', fliersize=1.5)
plt.axhline(100, color='#E67E22', linestyle='--', label='100：對敏感族群不健康')
plt.title('全台各測站每日 AQI 的分布（依月份）'); plt.legend()
plt.show()
'''),
        md('''
> 💡 **看懂結果**：7 月的箱子又低又扁——**幾乎全台都是好空氣**；1～4 月、11 月的箱子高、上面的點（極端值）多，**冬春季要特別注意**。
'''),
        md('''
## 故事 5：一週七天的捷運人潮——seaborn 熱力圖

**白話說明**：先整理成「星期 × 時段」的表（平均每天進站人次），`sns.heatmap` 一行畫出熱力圖：越亮的格子越擠。
'''),
        code('''
mrt = pd.read_csv('臺北捷運各站分時進出量_202603.csv', parse_dates=['日期'])
mrt['星期'] = mrt['日期'].dt.day_of_week
per_day = mrt.groupby(['日期', '星期', '時段'], as_index=False)['進站人次'].sum()
table = per_day.pivot_table(index='星期', columns='時段', values='進站人次', aggfunc='mean') / 1e4   # 萬人次
table.index = ['一', '二', '三', '四', '五', '六', '日']

plt.figure(figsize=(13, 4))
sns.heatmap(table, cmap='magma', cbar_kws={'label': '萬人次'})
plt.title('臺北捷運：星期 × 時段的平均進站人次'); plt.ylabel('星期')
plt.show()
'''),
        md('''
> 💡 **看懂結果**：平日的早上 8 點、晚上 6 點是兩條**亮線**——通勤尖峰；週末的亮區往中午、下午移，而且比較分散。**一張圖就是整座城市的作息表。**
'''),
        md('''
## 故事 6：美國片、日本片、國片——seaborn 散佈圖

**白話說明**：`sns.scatterplot` 用 `hue` 依類別上不同顏色。票房差距太大（從幾百元到 9 億），所以 Y 軸用**對數刻度**（`plt.yscale('log')`），小片和大片才能放在同一張圖裡。
'''),
        code('''
top3 = movies[movies['Country'].isin(['美國', '日本', '中華民國']) & (movies['年'] >= 2016)]

plt.figure(figsize=(9, 5))
sns.scatterplot(data=top3, x='TheaterCount', y='TotalAmounts', hue='Country', alpha=0.5, s=20,
                palette={'美國': '#2E86C1', '日本': '#C0392B', '中華民國': '#27AE60'})
plt.yscale('log')
plt.xlabel('上映戲院數'); plt.ylabel('票房（元，對數刻度）'); plt.title('上映戲院數 vs. 票房')
plt.show()
'''),
        md('''
> 💡 **看懂結果**：三個國家都是「戲院越多、票房越高」的右上斜分布。藍色（美國片）集中在右上角——好萊塢大片一上映就是 100 家戲院；綠色（國片）大多在左下，但也有幾部衝上右上角。
'''),
    ] + exercises(
        dict(title='YouBike 每年總騎乘次數，畫成長條圖',
             hint='`rides.resample(\'YE\').sum()` 依年加總，再 `.plot.bar()`。索引是日期，可以用 `.index.year` 改成只顯示年份。',
             starter='''
by_year_bike = rides.resample(___).sum()
by_year_bike.index = by_year_bike.index.year
by_year_bike.plot.___(figsize=(8, 4), color='#F39C12', rot=0, title='臺北市 YouBike 每年騎乘次數（萬次）')
plt.show()
''',
             check='''
_r = rides.resample('YE').sum()
_r.index = _r.index.year
check('by_year_bike', _r)
''',
             solution='''
by_year_bike = rides.resample('YE').sum()
by_year_bike.index = by_year_bike.index.year
by_year_bike.plot.bar(figsize=(8, 4), color='#F39C12', rot=0, title='臺北市 YouBike 每年騎乘次數（萬次）')
plt.show()
'''),
        dict(title='比較三個測站的 AQI 分布：花蓮、中山、斗六',
             hint='先用 `isin([...])` 篩出三個測站，再 `sns.boxplot(data=..., x=\'sitename\', y=\'aqi\')`。',
             starter='''
three = aqi[aqi['sitename'].isin([___, ___, ___])]
plt.figure(figsize=(7, 4))
sns.boxplot(data=three, x=___, y='aqi', order=['花蓮', '中山', '斗六'])
plt.title('三個測站的 AQI 分布')
plt.show()
''',
             solution='''
three = aqi[aqi['sitename'].isin(['花蓮', '中山', '斗六'])]
plt.figure(figsize=(7, 4))
sns.boxplot(data=three, x='sitename', y='aqi', order=['花蓮', '中山', '斗六'])
plt.title('三個測站的 AQI 分布')
plt.show()
'''),
        dict(title='每年上映的國片有幾部？畫成折線圖',
             hint='篩出 `Country == \'中華民國\'` 且 2016～2025 年，用 `groupby(\'年\').size()` 或 `[\'年\'].value_counts().sort_index()` 數每年幾部，再 `.plot()`。',
             starter='''
tw_count = movies[(movies['Country'] == ___) & movies['年'].between(2016, 2025)].groupby('年').size()
tw_count.plot(marker='o', figsize=(8, 4), title='每年上映的國片數量')
plt.show()
''',
             check='''
check('tw_count', movies[(movies['Country'] == '中華民國') & movies['年'].between(2016, 2025)].groupby('年').size())
''',
             solution='''
tw_count = movies[(movies['Country'] == '中華民國') & movies['年'].between(2016, 2025)].groupby('年').size()
tw_count.plot(marker='o', figsize=(8, 4), title='每年上映的國片數量')
plt.show()
'''),
    )
    return NOTEBOOK, files, cells
