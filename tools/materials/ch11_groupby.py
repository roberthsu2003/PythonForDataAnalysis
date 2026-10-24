"""第 11 章 群組運算：各店 KPI、甜度偏好、尖峰時段、會員客單價、pd.cut 級距、樞紐分析表。"""
from common import order_lines
from nbtools import md, code, setup_cell, font_cell, header, exercises

CHAPTER = '群組資料和群組運算'
NOTEBOOK = '範例_茶語時光_台南人真的愛全糖嗎.ipynb'


def build(out):
    o = order_lines('2024-01-01', '2024-03-31', offset=11)
    o['訂單時間'] = o['訂單時間'].dt.strftime('%Y-%m-%d %H:%M:%S')
    o.drop(columns=['門市代碼', '品項代碼']).to_csv(out / '訂單明細_2024Q1.csv', index=False, encoding='utf-8-sig')

    files = ['訂單明細_2024Q1.csv']
    desc = [('訂單明細_2024Q1.csv', '第一季約 12 萬筆訂單明細：時間、門市、品項、甜度、冰塊、數量、金額、是否會員、付款方式')]

    cells = [
        header(CHAPTER, NOTEBOOK, '🧩 茶語時光：台南人真的愛全糖嗎？',
               '公司內部流傳很多「都市傳說」：台南人特別愛全糖、逢甲店晚上才是戰場、會員比較會花錢……'
               '新來的行銷總監說：「別再用猜的，拿數據來！」你手上有第一季 12 萬筆訂單明細，'
               '只要學會一招 **groupby（分組 → 計算 → 合併）**，就能一一驗證。', desc),
        setup_cell(CHAPTER, files),
        font_cell(),
        md('''
## 任務 1：各店成績單——營收、杯數、訂單數、客單價

**白話說明**：「依 ___ 分組，計算 ___ 的 ___」。注意：一筆訂單有好幾列（好幾個品項），**訂單數要用 `nunique` 數不重複的訂單編號**。
'''),
        code('''
import pandas as pd

orders = pd.read_csv('訂單明細_2024Q1.csv', parse_dates=['訂單時間'])
print(orders.shape)
display(orders.head(3))

kpi = orders.groupby('門市').agg(營收=('金額', 'sum'),            # (新欄名, (原欄位, 計算方式))
                                 杯數=('數量', 'sum'),
                                 訂單數=('訂單編號', 'nunique'))   # 不重複的訂單編號數
kpi['客單價'] = (kpi['營收'] / kpi['訂單數']).round(1)            # 先加總、再相除
display(kpi.sort_values('營收', ascending=False))
'''),
        md('''
## 任務 2：傳說 1——台南人真的愛全糖嗎？

**白話說明**：依「門市 × 甜度」分組加總杯數，再把每家店換算成百分比——**一定要比「比例」**，因為每家店的總杯數不一樣。
'''),
        code('''
sweet = orders.groupby(['門市', '甜度'])['數量'].sum().unstack('甜度')   # 門市 × 甜度 的杯數
sweet = sweet[['正常糖', '少糖', '半糖', '微糖', '無糖']]
sweet_pct = sweet.div(sweet.sum(axis=1), axis=0) * 100               # 每一列除以該店總杯數 → 百分比
display(sweet_pct.round(1))
'''),
        code('''
import matplotlib.pyplot as plt

full_sugar = sweet_pct['正常糖'].sort_values()                       # 各店「正常糖」占比，由小到大
colors = ['#C0392B' if s == '台南成大店' else '#C8A27C' for s in full_sugar.index]   # 台南用紅色凸顯
ax = full_sugar.plot.barh(color=colors, figsize=(8, 3.5), title='各門市點「正常糖」的比例（%）')
for i, v in enumerate(full_sugar):
    ax.text(v + 0.3, i, f'{v:.1f}%', va='center')                     # 在長條旁邊寫上數字
ax.set_xlabel('占該店總杯數 %')
plt.show()
'''),
        md('''
> 💡 **看懂結果**：台南成大店點「正常糖」的比例是其他門市的 **2～3 倍**——傳說是真的！台北信義店（商辦區）則是「無糖」比例最高。
> 行銷建議：台南主打招牌甜飲，信義店可以優先試賣健康無糖新品。
>
> 🤖 **換你問 AI**：「請依門市與甜度分組加總杯數，換算成每家門市的百分比，並找出各門市最受歡迎的甜度。」
'''),
        md('''
## 任務 3：傳說 2——逢甲店晚上才是戰場？找出各店尖峰時段
'''),
        code('''
orders['小時'] = orders['訂單時間'].dt.hour
by_hour = orders.groupby(['門市', '小時'])['訂單編號'].nunique().unstack('門市')   # 小時 × 門市 的訂單數
display(by_hour)
print('\\n各店尖峰時段：')
display(by_hour.idxmax().map(lambda h: f'{h}:00～{h + 1}:00'))       # idxmax：每一欄最大值出現在哪一個小時
'''),
        md('''
> 💡 **看懂結果**：信義店的尖峰在中午 12 點（上班族午休），逢甲店的尖峰在晚上 8 點（夜市人潮）——**同一個品牌，排班表應該完全不同**。
'''),
        md('''
## 任務 4：傳說 3——會員比較會花錢嗎？

**白話說明**：明細是「一列一個品項」，要比較「每筆訂單花多少」，必須**先把同一筆訂單加總**（第一次 groupby），再依會員分組比較（第二次 groupby）。
'''),
        code('''
per_order = orders.groupby(['訂單編號', '會員', '門市'], as_index=False)['金額'].sum()   # 第一次：每筆訂單的總金額
member = per_order.groupby('會員')['金額'].agg([('訂單數', 'count'), ('平均客單價', 'mean'),
                                              ('中位數', 'median'), ('最高', 'max')])     # 第二次：會員 vs. 非會員
display(member.round(1))
'''),
        md('''
> 💡 **看懂結果**：會員的平均客單價明顯高於非會員（約多 25 元），中位數也比較高——**會員比較會花錢是真的**，推廣會員制度值得投資。
'''),
        md('''
## 任務 5：pd.cut——把訂單分成「小額、中額、大額」
'''),
        code('''
per_order['金額級距'] = pd.cut(per_order['金額'], bins=[0, 80, 160, 10_000],
                             labels=['小額(≤80)', '中額(81-160)', '大額(>160)'])
level = pd.crosstab(per_order['門市'], per_order['金額級距'], normalize='index') * 100   # 各店訂單的級距占比 %
display(level.round(1))
'''),
        md('''
> 💡 **看懂結果**：信義店（辦公室團購）與逢甲店（朋友揪團逛夜市）的大額訂單比例最高；台南成大店以學生為主，一半是單杯小額訂單。**滿額優惠要針對信義、逢甲設計，台南則適合第二杯折扣。**
>
> 🤖 **換你問 AI**：「請先把訂單明細依訂單編號加總成每筆訂單金額，再用 pd.cut 分成 ≤80、81–160、>160 三級，計算各門市的級距占比。」
'''),
        md('''
## 任務 6：樞紐分析表——每家店的「招牌飲料」

**白話說明**：每家店賣最多的都是珍珠奶茶（它本來就是全公司最暢銷的），這樣看不出特色。改看「**偏好指數**」＝某品項在這家店的占比 ÷ 全公司的占比，大於 1 代表「這家店的客人特別愛」。
'''),
        code('''
pivot = orders.pivot_table(index='品項', columns='門市', values='數量', aggfunc='sum', margins=True, margins_name='合計')
display(pivot.sort_values('合計', ascending=False))

share = orders.groupby(['門市', '品項'])['數量'].sum()
share = share / share.groupby(level='門市').transform('sum')              # transform：每個品項除以「自己門市」的總杯數 → 店內占比
overall = orders.groupby('品項')['數量'].sum() / orders['數量'].sum()     # 全公司占比
lift = (share / overall).unstack('門市')                                 # 偏好指數 = 店內占比 ÷ 全公司占比（> 1 代表比平均更受歡迎）
display(lift.round(2))
print('\\n偏好指數最高的品項：\\n', lift.idxmax())
print('\\n排除季節性飲料後的各店招牌：\\n', lift.drop(index=['熱可可', '芒果冰沙']).idxmax())
'''),
        md('''
> 💡 **看懂結果**：
> - 偏好指數最高的竟然是季節飲料：台北比較冷 → 熱可可特別好賣；台南、高雄比較熱 → 芒果冰沙特別好賣。**氣候差異會直接反映在菜單上。**
> - 排除季節品後，每家店的招牌就很清楚了：逢甲是黑糖珍珠鮮奶、信義是鮮奶綠、西門是珍珠奶茶、台南是冬瓜檸檬、高雄是多多綠——可以依門市規劃不同的主打商品。
''')
    ] + exercises(
        dict(title='各門市的付款方式占比（%），哪家店最常用現金？',
             hint='付款方式是「一筆訂單」一個，所以先 `drop_duplicates(\'訂單編號\')`；`pd.crosstab(..., normalize=\'index\')` 會把每一列換算成比例。',
             starter='''
one_row = orders.drop_duplicates(___)              # 一筆訂單只留一列
pay = pd.crosstab(one_row['門市'], one_row['付款方式'], normalize=___) * 100
cash_store = pay['現金'].idxmax()
display(pay.round(1))
print('最常用現金：', cash_store)
''',
             check='''
_o = orders.drop_duplicates('訂單編號')
check('pay', pd.crosstab(_o['門市'], _o['付款方式'], normalize='index') * 100)
''',
             solution='''
one_row = orders.drop_duplicates('訂單編號')
pay = pd.crosstab(one_row['門市'], one_row['付款方式'], normalize='index') * 100
cash_store = pay['現金'].idxmax()
display(pay.round(1))
print('最常用現金：', cash_store)
'''),
        dict(title='熱飲在 1～3 月之間有什麼變化？',
             hint='先用 `.dt.month` 做出「月份」欄，再「依月份 × 類別分組，加總數量」，`unstack(\'類別\')` 把類別搬到欄位。',
             starter='''
orders['月份'] = orders['訂單時間'].dt.___
hot_drink = orders.groupby(['月份', ___])['數量'].sum().unstack('類別')['熱飲']
display(hot_drink)
''',
             check='''
check('hot_drink', orders.groupby([orders['訂單時間'].dt.month, '類別'])['數量'].sum().unstack('類別')['熱飲'])
''',
             solution='''
orders['月份'] = orders['訂單時間'].dt.month
hot_drink = orders.groupby(['月份', '類別'])['數量'].sum().unstack('類別')['熱飲']
display(hot_drink)
'''),
        dict(title='哪家店的客人最愛點大杯？',
             hint='`(s == \'大\').mean()` 就是「大杯的比例」，因為 True 會被當成 1、False 當成 0。',
             starter='''
large = orders.groupby(___)['尺寸'].apply(lambda s: (s == '大').mean() * 100)
display(large.round(1).sort_values(ascending=False))
''',
             check='''
check('large', orders.groupby('門市')['尺寸'].apply(lambda s: (s == '大').mean() * 100))
''',
             solution='''
large = orders.groupby('門市')['尺寸'].apply(lambda s: (s == '大').mean() * 100)
display(large.round(1).sort_values(ascending=False))
'''),
    )
    return NOTEBOOK, files, cells
