"""第 7 章 pandas 檔案存取：髒 CSV、多工作表 Excel、巢狀 JSON、SQLite、大檔分批、輸出多工作表。"""
import json
import sqlite3

import numpy as np
import pandas as pd

from common import MENU, PAYMENTS, PAY_P, STORES, daily_sales, names, rng
from nbtools import md, code, setup_cell, header

CHAPTER = 'pandas的檔案存取'
NOTEBOOK = '範例_茶語時光_五種難搞的資料檔.ipynb'


def build(out):
    r = rng(70)
    d = daily_sales('2024-01-01', '2024-12-31')

    # 1) 髒 CSV：POS 匯出
    x = d[(d['門市代碼'] == 'S01') & (d['日期'].dt.month == 3)].copy()
    lines = ['# 茶語時光 POS 系統匯出報表', '# 門市：台北信義店　期間：2024-03-01 ~ 2024-03-31',
             '# 匯出時間：2024-04-01 09:12:33', '日期,來客數,杯數,營收,現金,電子支付,備註']
    tot = [0, 0, 0, 0, 0]
    for _, row in x.iterrows():
        ds = row['日期'].strftime('%Y-%m-%d')
        if ds in ('2024-03-08', '2024-03-19'):
            lines.append(f'{ds},--,--,--,--,--,系統當機未記錄')
            continue
        guests = int(row['杯數'] / r.uniform(1.45, 1.65))
        cash = int(row['營收'] * r.uniform(0.25, 0.4))
        vals = [guests, row['杯數'], row['營收'], cash, row['營收'] - cash]
        tot = [a + b for a, b in zip(tot, vals)]
        note = '白色情人節活動' if ds == '2024-03-14' else ''
        lines.append(ds + ',' + ','.join(f'"{v:,}"' for v in vals) + f',{note}')
    lines.append('合計,' + ','.join(f'"{v:,}"' for v in tot) + ',')
    (out / 'POS匯出_信義店_2024-03.csv').write_text('\n'.join(lines) + '\n', encoding='utf-8-sig')

    # 2) 多工作表 Excel：各店月報
    with pd.ExcelWriter(out / '各店月報_2024.xlsx', engine='openpyxl') as w:
        for _, s in STORES.iterrows():
            m = d[d['門市代碼'] == s['門市代碼']].groupby(d['日期'].dt.month).agg(營收=('營收', 'sum'), 杯數=('杯數', 'sum'))
            m.insert(0, '月份', [f'{i}月' for i in m.index])
            title = pd.DataFrame([[f'茶語時光 {s["門市"]} 2024 年月報', '', ''], ['單位：元／杯', '', '']])
            title.to_excel(w, sheet_name=s['門市'], index=False, header=False)
            m.to_excel(w, sheet_name=s['門市'], index=False, startrow=2)

    # 3) 巢狀 JSON：外送平台訂單
    menu = MENU.set_index('品項代碼')
    orders = []
    ts = pd.date_range('2024-03-01', '2024-03-31 23:00', freq='h')
    for i in range(1, 361):
        s = STORES[STORES['門市代碼'] != 'S04'].sample(1, random_state=int(r.integers(1e9))).iloc[0]   # 台南店沒有外送
        t = ts[int(r.integers(len(ts)))] + pd.Timedelta(minutes=int(r.integers(60)))
        items = []
        for _ in range(int(r.integers(1, 4))):
            c = r.choice(['001', '002', '003', '004', '005', '006', '009'])
            items.append({'品項': menu.loc[c, '品項'], '數量': int(r.integers(1, 4)), '單價': int(menu.loc[c, '中杯價'])})
        orders.append({'訂單編號': f'FR{i:05d}', '下單時間': t.strftime('%Y-%m-%d %H:%M'),
                       '門市': {'代碼': s['門市代碼'], '名稱': s['門市']},
                       '外送員評分': int(r.choice([3, 4, 5], p=[0.1, 0.3, 0.6])), '品項': items})
    data = {'平台': 'FoodRun 外送', '月份': '2024-03', '抽成比例': 0.3, '訂單': orders}
    (out / '外送平台訂單_2024-03.json').write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding='utf-8')

    # 4) SQLite：會員資料庫
    n = 800
    join = pd.to_datetime('2022-06-01') + pd.to_timedelta(r.integers(0, 945, n), unit='D')
    members = pd.DataFrame({
        '會員編號': [f'M{i:05d}' for i in range(1, n + 1)], '姓名': names(n, 7),
        '性別': r.choice(['女', '男'], n, p=[0.62, 0.38]),
        '生日': (pd.to_datetime('1965-01-01') + pd.to_timedelta(r.integers(0, 15000, n), unit='D')).strftime('%Y-%m-%d'),
        '加入日期': join.strftime('%Y-%m-%d'), '常去門市': r.choice(STORES['門市'], n),
        '累積點數': r.gamma(1.6, 180, n).round().astype(int),
    })
    db = out / '會員資料庫.db'
    if db.exists():
        db.unlink()
    with sqlite3.connect(db) as con:
        members.to_sql('會員', con, index=False)

    # 5) 大檔：全年交易紀錄（10 萬筆）
    n = 100_000
    t = pd.to_datetime('2024-01-01 10:00') + pd.to_timedelta(r.integers(0, 366, n), unit='D') \
        + pd.to_timedelta(r.integers(0, 12 * 3600, n), unit='s')
    big = pd.DataFrame({'交易編號': [f'X{i:07d}' for i in range(1, n + 1)], '交易時間': np.sort(t.values),
                        '門市': r.choice(STORES['門市'], n, p=[0.19, 0.21, 0.24, 0.17, 0.19]),
                        '金額': (r.gamma(2.2, 40, n) + 35).round().astype(int),
                        '付款方式': r.choice(PAYMENTS, n, p=PAY_P)})
    big['交易時間'] = pd.to_datetime(big['交易時間']).dt.strftime('%Y-%m-%d %H:%M:%S')
    big.to_csv(out / '全年交易紀錄_2024.csv', index=False, encoding='utf-8')

    files = ['POS匯出_信義店_2024-03.csv', '各店月報_2024.xlsx', '外送平台訂單_2024-03.json', '會員資料庫.db', '全年交易紀錄_2024.csv']
    desc = [('POS匯出_信義店_2024-03.csv', 'POS 匯出的日報：有註解行、千分位逗號、`--` 缺值、最後一列是合計'),
            ('各店月報_2024.xlsx', '5 個工作表（每店一張），前兩列是標題'),
            ('外送平台訂單_2024-03.json', '外送平台的巢狀 JSON：一筆訂單裡有多個品項'),
            ('會員資料庫.db', 'SQLite 資料庫，內有「會員」資料表（800 位）'),
            ('全年交易紀錄_2024.csv', '10 萬筆交易紀錄（用來練習分批讀取）')]

    cells = [
        header(CHAPTER, NOTEBOOK, '📥 茶語時光：搞定五種難搞的資料檔',
               '月初結帳日，各部門丟來五種格式的檔案：POS 系統匯出的「髒」CSV、每家店一個工作表的 Excel、'
               '外送平台的巢狀 JSON、IT 部門的會員資料庫，還有一個 10 萬筆、用 Excel 打開會卡住的交易檔。'
               '你要用 pandas 一一讀進來，最後整理成一份多工作表的 Excel 交給主管。', desc),
        setup_cell(CHAPTER, files),
        md('''
## 任務 1：POS 匯出的「髒」CSV——讀檔時就順便清乾淨

**先用文字方式看看原始檔長什麼樣子**：
'''),
        code('''
print(open('POS匯出_信義店_2024-03.csv', encoding='utf-8-sig').read()[:600])
'''),
        md('''
**問題**：前 3 行是說明、數字有千分位逗號、`--` 代表當機沒記錄、最後一列是「合計」。直接讀會一團亂，我們用參數一次處理：
'''),
        code('''
import pandas as pd

pos = pd.read_csv('POS匯出_信義店_2024-03.csv',
                  encoding='utf-8-sig',     # 檔案開頭有 BOM，用 utf-8-sig 讀
                  comment='#',              # # 開頭的說明行略過
                  thousands=',',            # "28,560" → 28560
                  na_values=['--'],         # -- 視為缺值
                  skipfooter=1,             # 最後一列「合計」不要
                  engine='python',          # 使用 skipfooter 需要 python 引擎
                  parse_dates=['日期'])      # 日期欄轉成時間型態
print(pos.dtypes)
print('\\n缺資料的日子：\\n', pos[pos['營收'].isnull()][['日期', '備註']])
print('\\n3 月營收合計（不含當機日）：', f"{pos['營收'].sum():,.0f}")
'''),
        md('''
> 🤖 **換你問 AI**：「這是 CSV 的前 8 行（貼上），請用 pandas read_csv 讀取，跳過說明行、處理千分位、把 -- 當成缺值、不要讀最後的合計列。」
'''),
        md('''
## 任務 2：每家店一個工作表的 Excel——一次讀完再合併

**白話說明**：`sheet_name=None` 會一次讀進「所有工作表」，得到一個「工作表名稱 → 表格」的字典；`header=2` 表示第 3 列才是欄位名稱。
'''),
        code('''
sheets = pd.read_excel('各店月報_2024.xlsx', sheet_name=None, header=2)   # 所有工作表、第 3 列是標題
print('工作表：', list(sheets.keys()))

yearly = pd.concat(sheets, names=['門市', '列'])                            # 把 5 張表上下合併，工作表名稱變成「門市」欄
yearly = yearly.reset_index(level='門市').reset_index(drop=True)
print(yearly.head())

summary = yearly.pivot_table(index='月份', columns='門市', values='營收', sort=False)   # 月份 × 門市 的營收總表
print((summary / 10000).round(1))
'''),
        md('''
## 任務 3：外送平台的巢狀 JSON——攤平成表格

**白話說明**：一筆訂單裡有好幾個品項（清單包清單）。`pd.json_normalize` 可以「攤平」：每個品項一列，並把訂單編號、門市等外層資訊帶下來。
'''),
        code('''
import json

with open('外送平台訂單_2024-03.json', encoding='utf-8') as f:
    raw = json.load(f)
print('平台：', raw['平台'], '｜抽成：', raw['抽成比例'], '｜訂單數：', len(raw['訂單']))

items = pd.json_normalize(raw['訂單'],
                          record_path='品項',                                  # 要攤開的清單
                          meta=['訂單編號', '下單時間', ['門市', '名稱'], '外送員評分'])   # 一起帶下來的外層欄位
items['小計'] = items['數量'] * items['單價']
print(items.head())

by_store = items.groupby('門市.名稱')['小計'].sum()
print('\\n各店外送營收：\\n', by_store)
print('\\n扣掉 30% 平台抽成，實拿：', f"{by_store.sum() * (1 - raw['抽成比例']):,.0f}", '元')
'''),
        md('''
> 💡 **看懂結果**：外送營收看起來不少，但平台要抽 30%——這就是為什麼很多飲料店的外送價格比店內貴。
>
> 🤖 **換你問 AI**：「這是外送平台 JSON 的前 30 行（貼上），請用 json_normalize 把每個品項攤成一列，並帶上訂單編號與門市名稱。」
'''),
        md('''
## 任務 4：IT 部門的會員資料庫——用 SQL 撈資料
'''),
        code('''
import sqlite3

con = sqlite3.connect('會員資料庫.db')                                       # 連線到資料庫檔案
print(pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", con))  # 資料庫裡有哪些資料表

new_2024 = pd.read_sql("""
    SELECT 常去門市, COUNT(*) AS 新會員數, ROUND(AVG(累積點數), 1) AS 平均點數
    FROM 會員
    WHERE 加入日期 >= '2024-01-01'
    GROUP BY 常去門市
    ORDER BY 新會員數 DESC
""", con)                                                                      # 2024 年加入的新會員，依門市統計
con.close()
print(new_2024)
'''),
        md('''
## 任務 5：10 萬筆大檔——分批讀取不卡頓
'''),
        code('''
print(pd.read_csv('全年交易紀錄_2024.csv', nrows=5))                         # 先偷看前 5 筆

total = pd.Series(dtype=float)
for chunk in pd.read_csv('全年交易紀錄_2024.csv', usecols=['付款方式', '金額'], chunksize=20_000):   # 每次只讀 2 萬筆、2 個欄位
    total = total.add(chunk.groupby('付款方式')['金額'].sum(), fill_value=0)      # 逐批累加
share = (total / total.sum() * 100).round(1).sort_values(ascending=False)
print('\\n各付款方式金額占比 %：\\n', share)
'''),
        md('''
> 💡 **看懂結果**：電子支付（LINE Pay、悠遊卡、街口、信用卡、Apple Pay）加起來已經超過現金——櫃台是不是該加裝感應設備、推出電子支付優惠？
'''),
        md('''
## 任務 6：整理成一份多工作表 Excel 交給主管
'''),
        code('''
with pd.ExcelWriter('三月結帳報告.xlsx') as writer:                           # 一個 Excel 檔、多個工作表
    pos.to_excel(writer, sheet_name='信義店3月日報', index=False)
    (summary / 10000).round(1).to_excel(writer, sheet_name='各店月營收(萬)')
    by_store.to_frame('外送營收').to_excel(writer, sheet_name='外送營收')
    new_2024.to_excel(writer, sheet_name='2024新會員', index=False)
    share.to_frame('占比%').to_excel(writer, sheet_name='付款方式')
print('✅ 已輸出 三月結帳報告.xlsx：', list(pd.read_excel('三月結帳報告.xlsx', sheet_name=None).keys()))

items.to_csv('外送品項明細.csv', index=False, encoding='utf-8-sig')            # utf-8-sig：用 Excel 開也不會亂碼
'''),
        md('''
---

## ✍️ 練習題

1. 從 `各店月報_2024.xlsx` 只讀取「台南成大店」這一個工作表，找出杯數最多的月份。
2. 用 SQL 從資料庫撈出「累積點數前 10 名」的會員姓名與常去門市。
3. 分批讀取交易紀錄，計算「每家門市」的交易筆數。
'''),
        md('## 🔑 參考解答（先自己試試看！）'),
        code('''
# 練習 1
tn = pd.read_excel('各店月報_2024.xlsx', sheet_name='台南成大店', header=2)
print(tn.loc[tn['杯數'].idxmax()])

# 練習 2
con = sqlite3.connect('會員資料庫.db')
print(pd.read_sql('SELECT 姓名, 常去門市, 累積點數 FROM 會員 ORDER BY 累積點數 DESC LIMIT 10', con))
con.close()

# 練習 3
count = pd.Series(dtype=float)
for chunk in pd.read_csv('全年交易紀錄_2024.csv', usecols=['門市'], chunksize=20_000):
    count = count.add(chunk['門市'].value_counts(), fill_value=0)
print(count.astype(int).sort_values(ascending=False))
'''),
    ]
    return NOTEBOOK, files, cells
