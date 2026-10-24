"""第 10 章 視覺化表格：用環境部真實 AQI 做「會變色的空品表」——Styler 格式化、官方等級色、熱力圖、資料條、匯出 Excel。"""
from nbtools import md, code, setup_cell, header, exercises, copy_real

CHAPTER = '視覺化表格'
NOTEBOOK = '範例_會變色的空氣品質週報_Styler.ipynb'
SOURCES = ['aqi']


def build(out):
    files = [copy_real(out, 'aqi')]
    desc = [(files[0], '環境部近一年、全台 80 多個測站的每日 AQI 與 PM2.5 等副指標')]

    cells = [
        header(CHAPTER, NOTEBOOK, '🎨 做一張會變色的空氣品質週報',
               '你看過環境部的空氣品質地圖嗎？綠色代表良好、黃色普通、橘色開始對敏感族群不健康……'
               '同樣的數字，**上了顏色**，一眼就知道哪裡要小心。學校要你做一份「本週空氣品質報表」貼在公布欄，'
               '今天就用 pandas 的 **Styler**，把一堆數字變成一張**跟官方一樣會變色**的表格，最後匯出成 Excel。',
               desc, SOURCES),
        setup_cell(CHAPTER, files),
        md('''
## 任務 1：先做出「素顏」的週報

**白話說明**：挑 12 個測站、最近 7 天，用 `pivot` 排成「測站 × 日期」的表。數字都對，但很難一眼看出重點。
'''),
        code('''
import pandas as pd

aqi = pd.read_csv('日空氣品質指標_近一年.csv', parse_dates=['monitordate'])
sites = ['基隆', '中山', '板橋', '桃園', '新竹', '忠明', '斗六', '臺南', '小港', '屏東', '花蓮', '金門']
last7 = aqi[aqi['monitordate'] > aqi['monitordate'].max() - pd.Timedelta(days=7)]     # 最近 7 天

week = last7[last7['sitename'].isin(sites)].pivot(index='sitename', columns='monitordate', values='aqi')
week = week.reindex(sites)                                            # 依我們指定的順序（北 → 南 → 東 → 離島）
week.columns = week.columns.strftime('%m/%d')
week.index.name = '測站'
week
'''),
        md('''
## 任務 2：套上官方的 AQI 顏色

**白話說明**：`style.map(函式)` 會把**每一格**的值丟進函式，函式回傳一段 CSS（例如 `'background-color: #00e400'`），那一格就會變色。顏色用的是環境部公告的 AQI 等級色。
'''),
        code('''
def aqi_color(v):
    """依環境部 AQI 等級回傳背景色（文字顏色也一起調整，深色底用白字）。"""
    if pd.isna(v):
        return 'background-color: #eeeeee; color: #999999'
    levels = [(50, '#00e400', 'black'), (100, '#ffff00', 'black'), (150, '#ff7e00', 'black'),
              (200, '#ff0000', 'white'), (300, '#8f3f97', 'white')]
    for upper, bg, fg in levels:
        if v <= upper:
            return f'background-color: {bg}; color: {fg}'
    return 'background-color: #7e0023; color: white'

styled = (week.style
          .map(aqi_color)                                             # 每一格依 AQI 上色
          .format('{:.0f}', na_rep='—')                               # 整數顯示；沒資料顯示「—」
          .set_caption('本週空氣品質 AQI（綠＝良好、黃＝普通、橘＝敏感族群不健康、紅＝不健康）'))
styled
'''),
        md('''
> 💡 **看懂結果**：一上色，馬上看出**中南部（斗六、小港、屏東、臺南）黃色、橘色最多**，花蓮、中山大多是綠色；北部偶爾也會冒出一天橘色——那通常是一陣外來的污染。一眼就看出哪裡、哪天要小心。這就是為什麼官方要規定一套顏色——**顏色本身就是資訊**。
'''),
        md('''
## 任務 3：年度成績單——格式化、資料條、標出最好與最差

**白話說明**：
- `format` 設定顯示格式：`'{:.1f}'` 小數一位、`'{:.0%}'` 百分比。
- `bar` 在格子裡畫**資料條**，長短代表大小。
- `highlight_max` / `highlight_min` 標出每一欄的最大、最小值。
'''),
        code('''
year = aqi[aqi['sitename'].isin(sites)].groupby('sitename').agg(
    平均AQI=('aqi', 'mean'),
    最差AQI=('aqi', 'max'),
    良好天數比例=('aqi', lambda s: (s <= 50).mean()),
    不健康天數=('aqi', lambda s: (s > 100).sum()),
).reindex(sites)
year.index.name = '測站'

report = (year.style
          .format({'平均AQI': '{:.1f}', '最差AQI': '{:.0f}', '良好天數比例': '{:.0%}', '不健康天數': '{:.0f} 天'})
          .bar(subset=['不健康天數'], color='#ff7e00', vmin=0)                     # 資料條
          .highlight_max(subset=['平均AQI'], color='#ffcccc')                     # 平均最差：淡紅
          .highlight_min(subset=['平均AQI'], color='#ccffcc')                     # 平均最好：淡綠
          .set_caption('近一年各測站空氣品質成績單'))
report
'''),
        md('''
> 💡 **看懂結果**：資料條讓「不健康天數」的差距一目了然：斗六、金門的橘色長條，是花蓮的好幾十倍。**花蓮一整年有八成以上的天數是「良好」**，斗六、金門只有兩成多。
'''),
        md('''
## 任務 4：熱力圖——一年 12 個月，哪裡、什麼時候最糟？

**白話說明**：`background_gradient` 依數值大小自動上漸層色，就是「熱力圖」。`axis=None` 代表**整張表一起比較**。
'''),
        code('''
aqi['月份'] = aqi['monitordate'].dt.strftime('%Y-%m')
heat = aqi[aqi['sitename'].isin(sites)].pivot_table(index='sitename', columns='月份', values='aqi', aggfunc='mean').reindex(sites)
heat.index.name = '測站'

heat_style = (heat.style
              .background_gradient(cmap='YlOrRd', axis=None)                     # 整張表一起比：越紅越差
              .format('{:.0f}')
              .set_caption('各測站每月平均 AQI 熱力圖'))
heat_style
'''),
        md('''
> 💡 **看懂結果**：熱力圖同時告訴你兩件事——**橫著看**：每個測站都是冬春紅、夏天黃；**直著看**：中南部和金門的紅色最深。一張表抵十張折線圖。
'''),
        md('''
## 任務 5：匯出成 Excel，貼到公布欄

**白話說明**：Styler 可以直接 `to_excel`，**顏色和格式會一起帶過去**（需要 openpyxl 套件）。
'''),
        code('''
with pd.ExcelWriter('空氣品質週報.xlsx') as writer:
    styled.to_excel(writer, sheet_name='本週AQI')
    report.to_excel(writer, sheet_name='年度成績單')
    heat_style.to_excel(writer, sheet_name='月份熱力圖')
print('已匯出 空氣品質週報.xlsx（用 Excel 打開，顏色都還在）')
'''),
    ] + exercises(
        dict(title='在成績單上，把「平均 AQI」超過全部測站平均的格子改成粗體紅字',
             hint='先算出 `year[\'平均AQI\'].mean()`。`report.map(函式, subset=[\'平均AQI\'])` 的函式要回傳 CSS，例如 `\'color: red; font-weight: bold\'`，不符合時回傳 `None`。',
             starter='''
avg = year['平均AQI'].___()
ex1 = report.map(lambda v: 'color: red; font-weight: bold' if v > ___ else None, subset=['平均AQI'])
ex1
''',
             check='''
check('avg', year['平均AQI'].mean())
''',
             solution='''
avg = year['平均AQI'].mean()
ex1 = report.map(lambda v: 'color: red; font-weight: bold' if v > avg else None, subset=['平均AQI'])
ex1
'''),
        dict(title='公布欄版本：隱藏「最差AQI」欄位',
             hint='`.hide(subset=[欄位], axis=\'columns\')` 只是「不顯示」，資料本身還在。',
             starter='''
ex2 = report.hide(subset=[___], axis='columns')
ex2
''',
             solution='''
ex2 = report.hide(subset=['最差AQI'], axis='columns')
ex2
'''),
        dict(title='熱力圖改成 `axis=1`：顏色的意思變成什麼？',
             hint='`axis=None` 是整張表一起比；`axis=1` 是「每一列（每個測站）自己比」——看的是「這個測站哪個月最糟」，就算是空氣很好的花蓮，也會有自己的紅色月份。',
             starter='''
ex3 = heat.style.background_gradient(cmap='YlOrRd', axis=___).format('{:.0f}')
ex3
''',
             solution='''
ex3 = heat.style.background_gradient(cmap='YlOrRd', axis=1).format('{:.0f}')
ex3
# axis=1 → 每個測站各自上色：看的是「對這個測站來說，哪個月最糟」，而不是「哪個測站最糟」
'''),
    )
    return NOTEBOOK, files, cells
