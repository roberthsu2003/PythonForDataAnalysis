"""第 5 章 初見 pandas：Series、DataFrame、新增欄位、篩選、索引對齊與 NaN。"""
import json

import numpy as np

from common import MENU, STORES, daily_sales, item_weights, rng
from nbtools import md, code, setup_cell, header

CHAPTER = '初見pandas'
NOTEBOOK = '範例_茶語時光_新品上市週的第一份報表.ipynb'


def week_items(daily, r, cannibal=1.0):
    """一週各品項杯數；cannibal < 1 表示鮮奶系列被新品分走部分客人。"""
    total = {}
    for _, d in daily.iterrows():
        w = item_weights(d['最高溫'], d['日期'], d['門市代碼'])
        for code_, share in w.items():
            name = MENU.set_index('品項代碼').loc[code_, '品項']
            factor = cannibal if code_ in ('003', '006') else 1.0
            total[name] = total.get(name, 0) + share * factor * d['杯數'] * r.lognormal(0, 0.05)
    return {k: int(round(v)) for k, v in total.items() if v > 0}


def build(out):
    r = rng(50)
    MENU[['品項代碼', '品項', '類別', '中杯價', '成本']].to_csv(out / '菜單.csv', index=False, encoding='utf-8-sig')
    STORES[['門市代碼', '門市', '縣市', '開幕日', '座位數', '月租金', '特色']].to_csv(out / '門市.csv', index=False, encoding='utf-8-sig')

    daily = daily_sales('2024-03-25', '2024-04-07')
    last = daily[daily['日期'] <= '2024-03-31']
    this = daily[daily['日期'] >= '2024-04-01']
    sales = {'上週(3/25-3/31)': week_items(last, r), '本週(4/1-4/7)': week_items(this, r, cannibal=0.82)}
    (out / '兩週品項銷量.json').write_text(json.dumps(sales, ensure_ascii=False, indent=2), encoding='utf-8')

    xinyi = this[this['門市'] == '台北信義店']
    weather = ['晴', '多雲', '晴', '雨', '晴', '多雲', '晴']
    report = [{'日期': d['日期'].strftime('%Y-%m-%d'), '天氣': w, '杯數': int(d['杯數']), '營收': int(d['營收']),
               '來客數': int(d['杯數'] / r.uniform(1.45, 1.65))} for (_, d), w in zip(xinyi.iterrows(), weather)]
    (out / '信義店日報_新品週.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')

    files = ['菜單.csv', '門市.csv', '兩週品項銷量.json', '信義店日報_新品週.json']
    desc = [('菜單.csv', '10 個品項的價格與成本'), ('門市.csv', '5 家門市的基本資料'),
            ('兩週品項銷量.json', '芋頭鮮奶上市前一週與上市當週，全品牌各品項杯數'),
            ('信義店日報_新品週.json', '信義店新品週每天的杯數、營收、來客數')]

    cells = [
        header(CHAPTER, NOTEBOOK, '🐼 茶語時光：新品上市週的第一份 pandas 報表',
               '2024 年 4 月 1 日，新品「芋頭鮮奶」上市！行銷部想知道：新品賣得怎樣？有沒有搶走其他飲料的生意？'
               '每杯賺多少？你第一次用 pandas，把菜單、門市資料與兩週的銷量做成表格來回答。', desc),
        setup_cell(CHAPTER, files),
        md('''
## 任務 1：Series——有名牌的一欄數字

**老闆的問題**：「每杯中杯賣多少錢？超過 60 元的有哪些？如果全面漲 5%，會變多少？」

**白話說明**：Series 像 Excel 的一欄，左邊是名牌（品項），右邊是數值（價格）。
'''),
        code('''
import pandas as pd

menu = pd.read_csv('菜單.csv', dtype={'品項代碼': str})     # 品項代碼當文字讀，才不會把 001 變成 1
price = pd.Series(menu['中杯價'].values, index=menu['品項'], name='中杯價')   # 名牌＝品項，值＝價格
print(price)
print('\\n珍珠奶茶的價格：', price['珍珠奶茶'])               # 用名牌查詢
print('\\n超過 60 元的品項：\\n', price[price > 60])           # 篩選
print('\\n全面漲 5% 後：\\n', (price * 1.05).round())         # 整欄一起運算
'''),
        md('''
## 任務 2：DataFrame——加上毛利欄位，找出「最會賺」的飲料

**白話說明**：DataFrame 就是整張 Excel 表。新增欄位就像在 Excel 插入一欄、填入公式。
'''),
        code('''
menu['毛利'] = menu['中杯價'] - menu['成本']                 # 新增欄位：每杯賺多少
menu['毛利率'] = (menu['毛利'] / menu['中杯價'] * 100).round(1)
print(menu)

print('\\n形狀：', menu.shape)                                # (列數, 欄數)
print('\\n毛利率 > 70% 的品項：')
print(menu[menu['毛利率'] > 70][['品項', '中杯價', '毛利', '毛利率']])
'''),
        md('''
> 💡 **看懂結果**：純茶、果茶的毛利率最高（成本低），鮮奶系列單價高、每杯賺得多但毛利率較低。**促銷要推哪一杯，取決於你要衝「營收」還是衝「利潤率」。**
>
> 🤖 **換你問 AI**：「這是我的菜單 DataFrame（欄位：品項、中杯價、成本），請新增毛利與毛利率欄，並列出毛利率超過 70% 的品項。」
'''),
        md('''
## 任務 3：從 JSON 建立 DataFrame——信義店新品週日報

**白話說明**：「清單裡放字典」（一天一個字典）的 JSON，用 `pd.DataFrame()` 一行就變成表格。
'''),
        code('''
import json

with open('信義店日報_新品週.json', encoding='utf-8') as f:
    records = json.load(f)
print('原始資料第一筆：', records[0])

report = pd.DataFrame(records)                               # 一個字典 → 一列
report = report.set_index('日期')                             # 用日期當列名牌
report['客單價'] = (report['營收'] / report['來客數']).round(1) # 平均每位客人花多少錢
print(report)
print('\\n新品週總營收：', report['營收'].sum(), '元')
print('雨天那天：\\n', report.loc[report['天氣'] == '雨'])
'''),
        md('''
## 任務 4：新品有沒有搶走其他飲料的生意？——索引對齊與 NaN

**老闆的問題**：「芋頭鮮奶上市後，其他飲料有沒有變少？」

**白話說明**：兩個 Series 相減時，pandas 會「按名牌配對」。芋頭鮮奶上週還沒上市、沒有名牌，配不到就會出現 **NaN**（空值）——這正是新品！
'''),
        code('''
with open('兩週品項銷量.json', encoding='utf-8') as f:
    sales = json.load(f)

last_week = pd.Series(sales['上週(3/25-3/31)'])               # 上週：沒有芋頭鮮奶
this_week = pd.Series(sales['本週(4/1-4/7)'])                 # 本週：多了芋頭鮮奶

compare = pd.DataFrame({'上週': last_week, '本週': this_week})  # 依品項名稱自動對齊
compare['變化'] = compare['本週'] - compare['上週']             # 上週沒有的 → NaN
compare['變化率%'] = (compare['變化'] / compare['上週'] * 100).round(1)
print(compare.sort_values('變化'))
print('\\n上週沒有資料（新品）：', list(compare[compare['上週'].isnull()].index))
'''),
        md('''
> 💡 **看懂結果**：
> - 芋頭鮮奶的「變化」是 NaN，因為上週根本還沒賣；熱可可則相反，天氣變熱、本週沒人點。**NaN 不是錯誤，而是在告訴你「這裡沒有資料可以比」**。
> - 同樣是鮮奶系列的「黑糖珍珠鮮奶」、「鮮奶綠」是衰退最多的兩杯——客人很可能改點新品了，這叫「**自我侵蝕**」。新品賣得好，不代表品牌整體多賺了這麼多。
>
> 🤖 **換你問 AI**：「我有上週與本週各品項銷量兩個 Series，請合併成一張比較表，計算變化量與變化率，並說明 NaN 代表什麼。」
'''),
        md('''
## 任務 5：門市資料表——每個座位要負擔多少租金？
'''),
        code('''
stores = pd.read_csv('門市.csv')
stores['每座位月租金'] = (stores['月租金'] / stores['座位數']).round(0)   # 新增欄位
print(stores[['門市', '縣市', '座位數', '月租金', '每座位月租金']].sort_values('每座位月租金', ascending=False))
'''),
        md('''
> 💡 **看懂結果**：台北的門市每個座位的租金是台南的好幾倍——這也是為什麼台北店更重視「外帶」與「翻桌率」。

---

## ✍️ 練習題

1. 用 `menu` 找出「類別」是「鮮奶」的所有品項，並算出它們的平均毛利。
2. 在 `report` 新增一欄「每杯平均價」＝營收 ÷ 杯數，哪一天最高？
3. 在 `compare` 中，用 `fillna(0)` 把上週的 NaN 補成 0，再重新計算芋頭鮮奶的「變化」。
'''),
        md('## 🔑 參考解答（先自己試試看！）'),
        code('''
# 練習 1
milk = menu[menu['類別'] == '鮮奶']
print(milk[['品項', '毛利']], '\\n平均毛利：', milk['毛利'].mean())

# 練習 2
report['每杯平均價'] = (report['營收'] / report['杯數']).round(1)
print(report['每杯平均價'], '\\n最高：', report['每杯平均價'].idxmax())

# 練習 3
compare['上週'] = compare['上週'].fillna(0)
compare['變化'] = compare['本週'] - compare['上週']
print(compare.loc['芋頭鮮奶'])
'''),
    ]
    return NOTEBOOK, files, cells
