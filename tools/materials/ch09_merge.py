"""第 9 章 數據整理：concat 三個月訂單、merge 主檔、找出對不到的代碼、pivot / stack / melt。"""
import pandas as pd

from common import MENU, STORES, LARGE_EXTRA, order_lines, rng
from nbtools import md, code, setup_cell, header, exercises

CHAPTER = '數據整理_連接_合併_重塑'
NOTEBOOK = '範例_茶語時光_三個月訂單合併成季報.ipynb'


def build(out):
    r = rng(90)
    orders = order_lines('2024-01-01', '2024-03-31', offset=9)
    cols = ['訂單編號', '訂單時間', '門市代碼', '品項代碼', '尺寸', '數量']
    popup = orders[(orders['門市代碼'] == 'S01') & (orders['訂單時間'] >= '2024-03-15')].sample(frac=0.25, random_state=4).copy()
    popup['門市代碼'] = 'S06'                                     # 3/15 起的「信義快閃店」，主檔還沒建檔
    popup['訂單編號'] = 'P' + popup['訂單編號'].str[1:]
    orders = pd.concat([orders, popup]).sort_values('訂單時間')
    orders['訂單時間'] = orders['訂單時間'].dt.strftime('%Y-%m-%d %H:%M:%S')
    for m in (1, 2, 3):
        part = orders[orders['訂單時間'].str[5:7] == f'{m:02d}'][cols]
        part.to_csv(out / f'訂單_2024-{m:02d}.csv', index=False, encoding='utf-8-sig')

    item_master = MENU[['品項代碼', '品項', '類別', '中杯價', '成本']].copy()
    item_master.to_csv(out / '品項主檔.csv', index=False, encoding='utf-8-sig')
    STORES[['門市代碼', '門市', '縣市', '開幕日']].to_csv(out / '門市主檔.csv', index=False, encoding='utf-8-sig')

    files = ['訂單_2024-01.csv', '訂單_2024-02.csv', '訂單_2024-03.csv', '品項主檔.csv', '門市主檔.csv']
    desc = [('訂單_2024-01.csv ～ 訂單_2024-03.csv', '第一季三個月的訂單明細（只有代碼，沒有名稱和價格）'),
            ('品項主檔.csv', '品項代碼 → 品項名稱、類別、價格、成本'), ('門市主檔.csv', '門市代碼 → 門市名稱、縣市')]

    cells = [
        header(CHAPTER, NOTEBOOK, '🔗 茶語時光：把三個月的訂單合併成第一季季報',
               'POS 系統每個月匯出一個訂單檔，而且為了省空間，檔案裡只有「門市代碼」和「品項代碼」，沒有名稱、也沒有價格。'
               '老闆要一份第一季季報：「每家店每個月賣了多少錢？哪一類飲料成長最多？」你需要把 3 個月份的檔案**接起來**，'
               '再和品項主檔、門市主檔**配對**，最後**轉成老闆看得懂的報表版面**。', desc),
        setup_cell(CHAPTER, files[:3] + files[3:]),
        md('''
## 任務 1：concat——把三個月的訂單「上下接起來」

**先踩一個陷阱**：直接讀檔，看看「品項代碼」變成什麼？
'''),
        code('''
import pandas as pd

trap = pd.read_csv('訂單_2024-01.csv')
print('沒指定型態時的品項代碼：', trap['品項代碼'].unique()[:5], trap['品項代碼'].dtype)   # 001 變成 1 了！
'''),
        code('''
months = []
for m in ['01', '02', '03']:
    df = pd.read_csv(f'訂單_2024-{m}.csv', dtype={'品項代碼': str})   # 代碼一律當文字讀，保住開頭的 0
    df['月份'] = f'{int(m)}月'                                         # 加上來源月份
    months.append(df)

orders = pd.concat(months, ignore_index=True)                          # 上下接起來，重新編列號
print('各月筆數：', [len(m) for m in months], '→ 合計', len(orders))
display(orders.head())
'''),
        md('''
> 💡 **看懂結果**：沒指定型態時，`001` 被當成數字 `1`，等一下和主檔的 `'001'` 就**配不起來**了。代碼、電話、郵遞區號這類「長得像數字的文字」，讀檔時一定要指定成文字。
'''),
        md('''
## 任務 2：merge——用品項代碼查出名稱與價格（就是 VLOOKUP）
'''),
        code('''
items = pd.read_csv('品項主檔.csv', dtype={'品項代碼': str})
display(items)

full = orders.merge(items, on='品項代碼', how='left', validate='many_to_one')   # 多筆訂單對一個品項；validate 幫你檢查主檔沒有重複
full['單價'] = full['中杯價'] + (full['尺寸'] == '大') * 10                   # 大杯 +10 元
full['金額'] = full['單價'] * full['數量']
full['毛利'] = (full['單價'] - full['成本']) * full['數量']
print('\\n合併前後筆數：', len(orders), '→', len(full), '（how=left 時兩者應該相同）')
display(full[['訂單編號', '品項代碼', '品項', '尺寸', '數量', '單價', '金額']].head())
'''),
        md('''
## 任務 3：配不到的代碼——找出主檔沒建檔的門市

**白話說明**：`indicator=True` 會多一欄 `_merge`，告訴你每一筆是「兩邊都有」還是「只有左邊有」。
'''),
        code('''
stores = pd.read_csv('門市主檔.csv')
full = full.merge(stores, on='門市代碼', how='left', indicator=True)
display(full['_merge'].value_counts())

missing = full[full['_merge'] == 'left_only']
print('\\n主檔裡找不到的門市代碼：', missing['門市代碼'].unique(),
      '｜筆數：', len(missing), '｜金額：', f"{missing['金額'].sum():,}", '元')
print('最早出現的時間：', missing['訂單時間'].min())
'''),
        md('''
> 💡 **看懂結果**：`S06` 是 3/15 開幕的「信義快閃店」，門市主檔還沒建檔。如果用 `how='inner'`，這些營收會**默默消失**在報表裡；用 `how='left'` 加上 `indicator`，才能抓到問題並通知同事補建主檔。
>
> 🤖 **換你問 AI**：「請把訂單明細和門市主檔用門市代碼 merge，以訂單為主，並列出主檔中找不到的門市代碼、筆數與金額。」
'''),
        code('''
full['門市'] = full['門市'].fillna('信義快閃店(S06)')                  # 先補上名稱，避免報表漏掉這筆營收
full = full.drop(columns='_merge')
'''),
        md('''
## 任務 4：pivot_table——做出「門市 × 月份」的季報
'''),
        code('''
report = full.pivot_table(index='門市', columns='月份', values='金額', aggfunc='sum',
                          margins=True, margins_name='合計')[['1月', '2月', '3月', '合計']]   # 加上合計列與合計欄
display((report / 10000).round(1))

growth = (report['3月'] / report['1月'] - 1) * 100
print('\\n3 月 vs. 1 月成長率 %：\\n', growth.drop('合計').round(1).sort_values(ascending=False))
'''),
        md('''
## 任務 5：stack / unstack / melt——同一份數字，換三種版面
'''),
        code('''
by_cat = full.groupby(['類別', '月份'])['數量'].sum()                  # 長表：一列 = 一個類別的一個月
print('▶ 長表（groupby 結果）：\\n', by_cat.head(6))

wide = by_cat.unstack('月份')[['1月', '2月', '3月']]                    # unstack：把月份搬到欄位 → 寬表（人看的）
wide['成長%'] = ((wide['3月'] / wide['1月'] - 1) * 100).round(1)
print('\\n▶ 寬表（類別 × 月份杯數）：\\n', wide.sort_values('成長%', ascending=False))

long = wide.drop(columns='成長%').reset_index().melt(id_vars='類別', var_name='月份', value_name='杯數')   # melt：寬表 → 長表（畫圖、存資料庫用）
print('\\n▶ melt 回長表：\\n', long.head())

with pd.ExcelWriter('第一季季報.xlsx') as w:
    (report / 10000).round(1).to_excel(w, sheet_name='門市x月份(萬元)')
    wide.to_excel(w, sheet_name='類別x月份(杯)')
print('\\n✅ 已輸出 第一季季報.xlsx')
'''),
        md('''
> 💡 **看懂結果**：冰沙類從 1 月到 3 月大幅成長（天氣變暖）、熱飲則是衰退——**季節性**非常明顯。進貨與行銷要跟著季節調整。
>
> 🤖 **換你問 AI**：「請把類別 × 月份的杯數做成寬表，新增 3 月比 1 月的成長率欄，並說明 stack、unstack、melt 的差別。」
''')
    ] + exercises(
        dict(title='不用手動加「月份」欄：用 `concat` 的 `keys` 參數一次搞定',
             hint='`keys=[\'1月\', \'2月\', \'3月\']` 會變成外層索引，`names=[\'月份\', \'原列號\']` 幫兩層索引取名字。',
             starter='''
alt = pd.concat([pd.read_csv(f'訂單_2024-{m}.csv', dtype={'品項代碼': str}) for m in ['01', '02', '03']],
                keys=___, names=['月份', '原列號'])
display(alt.head(3))
print('總筆數：', len(alt))
''',
             check='''
check('alt', pd.concat([pd.read_csv(f'訂單_2024-{m}.csv', dtype={'品項代碼': str}) for m in ['01', '02', '03']],
                       keys=['1月', '2月', '3月'], names=['月份', '原列號']))
''',
             solution='''
alt = pd.concat([pd.read_csv(f'訂單_2024-{m}.csv', dtype={'品項代碼': str}) for m in ['01', '02', '03']],
                keys=['1月', '2月', '3月'], names=['月份', '原列號'])
display(alt.head(3))
print('總筆數：', len(alt))
'''),
        dict(title='做一張「門市 × 類別」的毛利樞紐分析表，哪家店的鮮奶系列最賺？',
             hint='`pivot_table(index=列, columns=欄, values=值, aggfunc=\'sum\')`；再對「鮮奶」那一欄用 `idxmax()`。',
             starter='''
profit = full.pivot_table(index=___, columns=___, values='毛利', aggfunc='sum')
milk_best = profit['鮮奶'].idxmax()
display(profit.round(0))
print('鮮奶系列毛利最高：', milk_best)
''',
             check='''
check('profit', full.pivot_table(index='門市', columns='類別', values='毛利', aggfunc='sum'))
''',
             solution='''
profit = full.pivot_table(index='門市', columns='類別', values='毛利', aggfunc='sum')
milk_best = profit['鮮奶'].idxmax()
display(profit.round(0))
print('鮮奶系列毛利最高：', milk_best)
'''),
        dict(title='寬表轉長表：哪家門市的哪個月，營收最高？',
             hint='先把「合計」列與「合計」欄拿掉，`stack()` 會把月份搬到列，變成 (門市, 月份) 一列一個數字；再用 `idxmax()`。',
             starter='''
s = report.drop(index='合計', columns='合計').___()
best_cell = s.idxmax()                             # (門市, 月份)
print('單月營收最高：', best_cell, f'{s.max():,.0f} 元')
''',
             check='''
check('best_cell', report.drop(index='合計', columns='合計').stack().idxmax())
''',
             solution='''
s = report.drop(index='合計', columns='合計').stack()
best_cell = s.idxmax()
print('單月營收最高：', best_cell, f'{s.max():,.0f} 元')
'''),
    )
    return NOTEBOOK, files, cells
