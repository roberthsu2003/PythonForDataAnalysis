"""第 7 章 pandas 檔案存取：真實政府資料的各種格式——Big5＋民國年、千分位＋空欄、巢狀 JSON、多工作表 Excel、SQLite、大檔分批、輸出 Excel。"""
import sqlite3

import pandas as pd

from nbtools import md, code, setup_cell, header, exercises, copy_real, read_real, latest

CHAPTER = 'pandas的檔案存取'
NOTEBOOK = '範例_政府資料的七種難搞格式.ipynb'
SOURCES = ['recycle', 'power_city', 'boxoffice', 'aqi', 'mrt']


def build(out):
    files = [copy_real(out, 'recycle'), copy_real(out, 'power_city'), copy_real(out, 'boxoffice'), copy_real(out, 'mrt')]

    # 多工作表 Excel：把台電縣市用電整理成「一年一張工作表」，第 1 列是標題（機關報表常見的格式）
    city = pd.read_csv(read_real('power_city'), thousands=',').dropna(subset=['年月'])
    city['年'] = (city['年月'] // 100 + 1911).astype(int)
    with pd.ExcelWriter(out / '台電縣市年度用電.xlsx') as w:
        for year in (2023, 2024, 2025):
            t = city[city['年'] == year].pivot_table(index='縣市', columns='用電性質', values='售電量(度)', aggfunc='sum')
            t = (t / 1e8).round(2).reset_index()
            pd.DataFrame([[f'{year} 年各縣市售電量（單位：億度）']]).to_excel(w, sheet_name=f'{year}年', index=False, header=False)
            t.to_excel(w, sheet_name=f'{year}年', index=False, startrow=1)
    files.append('台電縣市年度用電.xlsx')

    # SQLite：把一年份的日 AQI 存成資料庫
    aqi = pd.read_csv(read_real('aqi'))[['sitename', 'monitordate', 'aqi', 'pm25subindex']]
    aqi.columns = ['測站', '日期', 'AQI', 'PM25副指標']
    db = out / '空氣品質.db'
    db.unlink(missing_ok=True)
    with sqlite3.connect(db) as con:
        aqi.to_sql('日空品', con, index=False)
    files.append('空氣品質.db')

    desc = [(files[0], '臺北市各區清潔隊每月資源回收量（**Big5 編碼**，年度是**民國年**）'),
            (files[1], '台電各縣市每月售電量（數字有**千分位逗號**、最後有空白列和多餘的空欄）'),
            (files[2], '文化部全國電影票房（**巢狀 JSON**）'),
            (files[3], '臺北捷運 2026 年 3 月各站每小時進出站人次（約 8 萬列，練習**分批讀取**）'),
            ('台電縣市年度用電.xlsx', '整理自台電縣市用電：一年一張工作表、**第 1 列是報表標題**'),
            ('空氣品質.db', '整理自環境部日 AQI：一年份、80 個測站的 **SQLite 資料庫**')]

    cells = [
        header(CHAPTER, NOTEBOOK, '📥 政府資料的七種難搞格式：用 pandas 一次搞定',
               '你接下市政府的資料整理工作，第一天就收到一個資料夾：Big5 編碼還用民國年的 CSV、數字有逗號的 CSV、'
               '一層包一層的 JSON、一年一張工作表的 Excel、一個 SQLite 資料庫，還有一個大到 Excel 打開會卡住的檔案。'
               '這些都是**政府開放資料的真實樣貌**。今天的任務是：**每一種都用 pandas 一兩行讀進來，最後整理成一份 Excel 交差。**',
               desc, SOURCES),
        setup_cell(CHAPTER, files),
        md('''
## 任務 1：Big5 編碼＋民國年——臺北市哪一區最會做資源回收？

**白話說明**：`encoding='cp950'` 解決亂碼；`年度` 是民國年，**加 1911** 就是西元年。
'''),
        code('''
import pandas as pd

recycle = pd.read_csv('臺北市各區資源回收量.csv', encoding='cp950')   # Big5 檔案要指定 cp950
recycle.columns = ['年度', '月', '行政區代碼', '區隊', '回收量(噸)']       # 原始欄名有全形括號，改成好打的名字
recycle['西元年'] = recycle['年度'] + 1911                                  # 民國 → 西元
display(recycle.head())

y2025 = recycle[recycle['西元年'] == 2025]
y2025.groupby('區隊')['回收量(噸)'].sum().sort_values(ascending=False).round(0)
'''),
        md('''
> 💡 **看懂結果**：2025 年回收量最多的是**大安區**（將近 8,000 噸），最少的是大同區。不過大安區人口本來就多——**要比「誰最會回收」，應該比「每個人」回收多少**。這需要把人口資料合併進來，第 10 章會教。
'''),
        md('''
## 任務 2：千分位逗號＋空欄＋空白列——台電縣市用電

**白話說明**：
- `thousands=','`：把 `"636,471,432"` 讀成數字。
- 檔案最右邊有兩個沒有名字的空欄（`Unnamed: 5`、`Unnamed: 6`），最後還有一列全空白——用 `usecols` 只讀需要的欄，用 `dropna` 去掉空白列。
'''),
        code('''
raw = pd.read_csv('台電各縣市用電統計.csv')
print('不加任何參數讀進來：')
print(raw.dtypes)                                                   # 售電量是 str（文字）！因為有逗號
print('最後兩列：'); display(raw.tail(2))
'''),
        code('''
power = pd.read_csv('台電各縣市用電統計.csv', thousands=',', usecols=range(5))   # 只讀前 5 欄
power = power.dropna(subset=['年月'])                                             # 去掉空白列
power['年月'] = power['年月'].astype(int)
print(power.dtypes)
power.head()
'''),
        md('''
> 🤖 **換你問 AI**：「我的 CSV 數字欄位有千分位逗號，最右邊還有空欄、最後一列是空白。請用 pandas 讀取並清理，讓數字欄位變成數值型態。」
'''),
        md('''
## 任務 3：巢狀 JSON——用 `json_normalize` 攤平

**白話說明**：票房 JSON 的最外層是 `{'Start': ..., 'End': ..., 'List': [電影, 電影, ...]}`。`pd.json_normalize(data, record_path='List', meta=['End'])` 會把 `List` 裡的每部電影攤成一列，再把外層的 `End`（資料截止日）貼到每一列上。
'''),
        code('''
import json

with open('全國電影票房_2016至今.json', encoding='utf-8-sig') as f:
    data = json.load(f)

movies = pd.json_normalize(data, record_path='List', meta=['End'])   # List 攤平成表格，外層的 End 也一起帶進來
print(movies.shape)
movies[['Name', 'Country', 'TotalAmounts', 'End']].head(3)
'''),
        md('''
## 任務 4：一年一張工作表的 Excel

**白話說明**：`sheet_name=None` 一次讀**所有**工作表，得到一個「工作表名稱 → 表格」的字典。這份 Excel 第 1 列是報表標題，真正的欄名在第 2 列，所以 `header=1`。最後用 `pd.concat` 上下接成一張表。
'''),
        code('''
sheets = pd.read_excel('台電縣市年度用電.xlsx', sheet_name=None, header=1)   # 全部工作表；第 2 列才是欄名
print('工作表：', list(sheets.keys()))

yearly = pd.concat(sheets, names=['年度', '列']).reset_index(level='年度').reset_index(drop=True)
display(yearly.head())

yearly.pivot_table(index='縣市', columns='年度', values='住宅').sort_values('2025年', ascending=False).head(6)
'''),
        md('''
> 💡 **看懂結果**：住宅用電最多的是新北市、台中市、高雄市——人口最多的縣市。而且**大多數縣市一年比一年多**（只有高雄 2025 年略降）：家家戶戶的冷氣、電器越來越多。
'''),
        md('''
## 任務 5：SQLite 資料庫——用 SQL 問問題

**白話說明**：`sqlite3.connect` 連線到資料庫檔案，`pd.read_sql(SQL 指令, 連線)` 把查詢結果直接變成 DataFrame。SQL 的 `GROUP BY` 就是 pandas 的 `groupby`。
'''),
        code('''
import sqlite3

con = sqlite3.connect('空氣品質.db')
display(pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", con))   # 資料庫裡有哪些資料表

worst = pd.read_sql("""
    SELECT 測站, ROUND(AVG(AQI), 1) AS 平均AQI, SUM(AQI > 100) AS 不健康天數
    FROM 日空品
    GROUP BY 測站
    ORDER BY 平均AQI DESC
    LIMIT 8
""", con)
worst
'''),
        md('''
## 任務 6：大檔分批讀——捷運哪一站最多人進站？

**白話說明**：遇到幾百萬列的大檔，一次讀進來可能會讓電腦當掉。`chunksize=20_000` 讓 `read_csv` **一次只給你 2 萬列**；每一批各自加總，最後再合起來。
'''),
        code('''
total = pd.Series(dtype=float)
for chunk in pd.read_csv('臺北捷運各站分時進出量_202603.csv', chunksize=20_000):   # 每次 2 萬列
    total = total.add(chunk.groupby('車站')['進站人次'].sum(), fill_value=0)          # 這一批的結果累加上去

top = (total / 1e4).round(1).sort_values(ascending=False).rename('3月進站人次(萬)')
top.head(10)
'''),
        md('''
> 💡 **看懂結果**：2026 年 3 月，**台北車站**一個月有 481 萬人次進站，是第二名西門的兩倍多。仔細看車站名稱，有些前面多了路線代碼（例如 `BL板橋`、`G大坪林`）——這也是真實資料的「小髒」，第 8 章會處理。
'''),
        md('''
## 任務 7：整理好了，輸出成一份 Excel 交給主管

**白話說明**：`pd.ExcelWriter` 可以把好幾張表寫進**同一個 Excel 的不同工作表**。存 CSV 給 Excel 開時，用 `encoding='utf-8-sig'` 才不會亂碼。
'''),
        code('''
with pd.ExcelWriter('資料整理成果.xlsx') as writer:
    y2025.groupby('區隊')['回收量(噸)'].sum().round(0).to_excel(writer, sheet_name='2025各區回收量')
    worst.to_excel(writer, sheet_name='空品最差測站', index=False)
    top.head(20).to_excel(writer, sheet_name='捷運進站前20名')

top.to_csv('捷運進站排行.csv', encoding='utf-8-sig')                  # utf-8-sig：Excel 打開不會亂碼
print('已輸出：資料整理成果.xlsx、捷運進站排行.csv')
print(pd.read_excel('資料整理成果.xlsx', sheet_name=None).keys())
'''),
        latest('''
import pandas as pd
url = ('https://data.moenv.gov.tw/api/v2/aqx_p_432?api_key=b7df779e-71a6-4148-8379-5afbd441d803'
       '&format=JSON&limit=100')
now = pd.read_json(url)                                    # 環境部 API：全台各測站「現在這一小時」的 AQI
now[['sitename', 'county', 'aqi', 'status', 'publishtime']].sort_values('aqi', ascending=False).head(10)
''', note='環境部有提供 API，可以直接抓「這一小時」的空氣品質。把這段貼到新的一格執行（需要網路）：'),
    ] + exercises(
        dict(title='只讀「2024年」這一張工作表，哪個縣市的工業用電最多？',
             hint='`sheet_name=\'2024年\'` 只讀一張；別忘了 `header=1`。再用 `idxmax()` 找出「工業」最大的那一列，取出「縣市」。',
             starter='''
t2024 = pd.read_excel('台電縣市年度用電.xlsx', sheet_name=___, header=___)
industry_top = t2024.loc[t2024['工業'].idxmax(), '縣市']
print('2024 年工業用電最多的縣市：', industry_top)
''',
             check='''
_t = pd.read_excel('台電縣市年度用電.xlsx', sheet_name='2024年', header=1)
check('industry_top', _t.loc[_t['工業'].idxmax(), '縣市'])
''',
             solution='''
t2024 = pd.read_excel('台電縣市年度用電.xlsx', sheet_name='2024年', header=1)
industry_top = t2024.loc[t2024['工業'].idxmax(), '縣市']
print('2024 年工業用電最多的縣市：', industry_top)
'''),
        dict(title='用 SQL 查：金門有幾天 AQI 超過 100？',
             hint='`WHERE 測站 = \'金門\' AND AQI > 100`；`COUNT(*)` 數有幾列。查詢結果是一個表格，用 `.iloc[0, 0]` 取出那個數字。',
             starter='''
sql = "SELECT COUNT(*) FROM 日空品 WHERE 測站 = ___ AND AQI > ___"
kinmen_days = pd.read_sql(sql, con).iloc[0, 0]
print('金門 AQI > 100 的天數：', kinmen_days)
''',
             check='''
check('kinmen_days', pd.read_sql("SELECT COUNT(*) FROM 日空品 WHERE 測站 = '金門' AND AQI > 100", con).iloc[0, 0])
''',
             solution='''
sql = "SELECT COUNT(*) FROM 日空品 WHERE 測站 = '金門' AND AQI > 100"
kinmen_days = pd.read_sql(sql, con).iloc[0, 0]
print('金門 AQI > 100 的天數：', kinmen_days)
'''),
        dict(title='臺北市 2024 年（民國 113 年）總共回收了幾噸？',
             hint='可以用任務 1 做好的「西元年」欄位篩選 2024，也可以直接用民國的「年度」欄位篩選 113。最後對「回收量(噸)」加總。',
             starter='''
total_2024 = recycle.loc[recycle[___] == 2024, '回收量(噸)'].___()
print(f'2024 年臺北市資源回收量：{total_2024:,.0f} 噸')
''',
             check='''
check('total_2024', recycle.loc[recycle['年度'] == 113, '回收量(噸)'].sum())
''',
             solution='''
total_2024 = recycle.loc[recycle['西元年'] == 2024, '回收量(噸)'].sum()
print(f'2024 年臺北市資源回收量：{total_2024:,.0f} 噸')
'''),
    )
    return NOTEBOOK, files, cells
