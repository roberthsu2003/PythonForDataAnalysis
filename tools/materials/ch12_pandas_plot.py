"""第 12 章 pandas 直接繪圖：df.plot、事件標註、堆疊百分比長條、seaborn 統計圖、分布圖。"""
import pandas as pd

from common import daily_sales, order_lines
from nbtools import md, code, setup_cell, font_cell, header, exercises

CHAPTER = '直接使用pandas繪制圖表'
NOTEBOOK = '範例_茶語時光_一行畫出年度簡報圖.ipynb'


def build(out):
    d = daily_sales('2024-01-01', '2024-12-31')
    d['日期'] = d['日期'].dt.strftime('%Y-%m-%d')
    d[['日期', '門市', '最高溫', '杯數', '營收', '事件']].to_csv(out / '每日營收_2024.csv', index=False, encoding='utf-8-sig')

    o = order_lines('2024-07-01', '2024-07-31', offset=12)
    o['訂單時間'] = o['訂單時間'].dt.strftime('%Y-%m-%d %H:%M:%S')
    o.drop(columns=['門市代碼', '品項代碼', '單價']).to_csv(out / '訂單明細_2024-07.csv', index=False, encoding='utf-8-sig')

    files = ['每日營收_2024.csv', '訂單明細_2024-07.csv']
    desc = [('每日營收_2024.csv', '2024 年每天 × 5 家門市的杯數、營收、最高溫與特殊事件（颱風、演唱會、節日、活動）'),
            ('訂單明細_2024-07.csv', '7 月份的訂單明細（約 4 萬筆）')]

    cells = [
        header(CHAPTER, NOTEBOOK, '🖼️ 茶語時光：一行程式畫出年度簡報圖',
               '尾牙前要做年度簡報。上一章你學會用 groupby 算出各種統計，這次老闆要的是「圖」：全年營收走勢、'
               '颱風和演唱會的影響、不同時段客人點什麼、會員是不是比較會花錢。好消息是——**表格整理好之後，pandas 一行就能畫圖**。', desc),
        setup_cell(CHAPTER, files),
        font_cell(),
        md('''
## 圖 1：全年營收走勢——pivot 之後一行 `.plot()`

**白話說明**：把資料整理成「日期 × 門市」的寬表，`.plot()` 會自動把**索引當 X 軸、每一欄畫成一條線**。每日數字太亂，再加上 7 日移動平均讓趨勢更清楚。
'''),
        code('''
import pandas as pd
import matplotlib.pyplot as plt

daily = pd.read_csv('每日營收_2024.csv', parse_dates=['日期'])
wide = daily.pivot(index='日期', columns='門市', values='營收')        # 日期 × 門市 的寬表
display(wide.head(3))

ax = (wide.rolling(7).mean() / 10000).plot(figsize=(12, 5), title='2024 各門市每日營收（7 日移動平均，萬元）')   # 一行畫 5 條線
ax.set_ylabel('萬元')
plt.show()
'''),
        md('''
## 圖 2：把颱風、演唱會標在圖上——讓圖會說故事
'''),
        code('''
total = daily.groupby('日期')['營收'].sum() / 10000                     # 全品牌每日營收（萬元）
events = daily[daily['事件'].notna()].groupby('日期')['事件'].first()    # 有特殊事件的日子

ax = total.plot(figsize=(14, 5), color='gray', alpha=0.7, title='2024 全品牌每日營收與重要事件（萬元）')
ax.set_ylim(0, total.max() * 1.45)                                     # 上方留空間放標註文字

last_seen, k = {}, 0
for date, name in events.items():
    if name not in ('凱米颱風', '康芮颱風', '巨蛋演唱會', '情人節', '七夕', '第二杯半價', '芋頭鮮奶上市', '跨年'):
        continue
    if name in last_seen and (date - last_seen[name]).days < 30:      # 一個月內的同一事件只標第一次
        continue
    last_seen[name] = date
    y = total[date]
    if '颱風' in name:                                                  # 颱風：紅色，文字放在下方
        ax.annotate(name, xy=(date, y), xytext=(date, 0.8), ha='center', fontsize=9, color='red',
                    arrowprops=dict(arrowstyle='->', color='red'))
    else:                                                               # 好事件：綠色，文字高低交錯避免重疊
        k += 1
        ax.annotate(name, xy=(date, y), xytext=(date, total.max() * (1.12 if k % 2 else 1.3)),
                    ha='right' if date.month == 12 and date.day > 25 else 'center',   # 年底的標籤靠右，避免超出圖框
                    fontsize=9, color='green', arrowprops=dict(arrowstyle='->', color='green'))
plt.show()
'''),
        md('''
> 💡 **看懂結果**：凱米、康芮颱風那幾天營收直接腰斬；情人節、七夕、跨年、巨蛋演唱會則是明顯的高峰。6 月每週三的「第二杯半價」讓週三變成一週最好的一天。**把事件標上去，老闆一看就懂「為什麼那天特別高或特別低」。**
>
> 🤖 **換你問 AI**：「請畫出全品牌每日營收折線圖，並在『事件』欄位有值的日期加上箭頭標註，颱風用紅色、節日活動用綠色。」
'''),
        md('''
## 圖 3：不同時段，客人點什麼？——百分比堆疊長條圖
'''),
        code('''
orders = pd.read_csv('訂單明細_2024-07.csv', parse_dates=['訂單時間'])
orders['時段'] = pd.cut(orders['訂單時間'].dt.hour, bins=[9, 13, 17, 23], labels=['午餐前後', '下午茶', '晚上'])
mix = pd.crosstab(orders['時段'], orders['類別'], values=orders['數量'], aggfunc='sum', normalize='index') * 100   # 每個時段各類別占比
display(mix.round(1))

ax = mix.plot.barh(stacked=True, figsize=(10, 4), colormap='tab20c', title='7 月各時段的飲料類別占比（%）')
ax.legend(bbox_to_anchor=(1.01, 1), loc='upper left')                  # 圖例放到右邊
plt.show()
'''),
        md('''
> 💡 **看懂結果**：午餐前後鮮奶系列最受歡迎（很多人拿它當正餐），下午茶時段奶茶比例上升，晚上則是清爽的果茶、純茶比較多。**看板與推播訊息可以依時段換主打。**
'''),
        md('''
## 圖 4：會員真的比較會花錢嗎？——seaborn 統計長條圖

**白話說明**：seaborn 畫平均值長條圖時，會自動加上**誤差線（信賴區間）**，告訴你這個平均有多可靠。
'''),
        code('''
import seaborn as sns

per_order = orders.groupby(['訂單編號', '門市', '會員'], as_index=False)['金額'].sum()   # 先算每筆訂單金額
ax = sns.barplot(data=per_order, x='門市', y='金額', hue='會員', errorbar=('ci', 95))
ax.set_title('各門市客單價：會員(Y) vs. 非會員(N)')
plt.show()
'''),
        md('''
> 💡 **看懂結果**：每家店的會員客單價都比較高，而且誤差線沒有重疊——差異是穩定的，不是碰巧。
'''),
        md('''
## 圖 5：訂單金額的分布——直方圖與盒鬚圖
'''),
        code('''
fig, axes = plt.subplots(1, 2, figsize=(14, 4))
per_order['金額'].plot.hist(bins=40, ax=axes[0], color='#C8A27C', title='每筆訂單金額分布')
per_order.boxplot(column='金額', by='門市', ax=axes[1], grid=False)      # 盒鬚圖：中間的線是中位數，點是極端值
axes[1].set_title('各門市訂單金額（盒鬚圖）')
fig.suptitle('')
plt.tight_layout()
plt.savefig('訂單金額分布.png', dpi=200, bbox_inches='tight')           # 存成簡報用的圖檔
plt.show()
'''),
        md('''
> 💡 **看懂結果**：大部分訂單都是 1～2 杯（100 元左右），但有一條長長的「尾巴」——少數大額團購訂單。平均值會被這些大單拉高，所以報告「典型客人花多少」時，**中位數比平均數更貼近事實**。
''')
    ] + exercises(
        dict(title='台南成大店：杯數和氣溫畫在同一張圖（雙 Y 軸）',
             hint='`ax2 = ax.twinx()` 會建立一個共用 X 軸、右邊有自己 Y 軸的新座標；第二條線畫在 `ax=ax2` 上。',
             starter='''
tn = daily[daily['門市'] == ___].set_index('日期')
ax = tn['杯數'].plot(figsize=(12, 4), color='#8B5E3C', label='杯數')
ax2 = ax.___()                                     # 共用 X 軸、右邊另一個 Y 軸
tn['最高溫'].plot(ax=ax2, color='orange', alpha=0.6, label='最高溫')
ax.set_title('台南成大店：每日杯數與最高溫')
plt.show()
''',
             solution='''
tn = daily[daily['門市'] == '台南成大店'].set_index('日期')
ax = tn['杯數'].plot(figsize=(12, 4), color='#8B5E3C', label='杯數')
ax2 = ax.twinx()
tn['最高溫'].plot(ax=ax2, color='orange', alpha=0.6, label='最高溫')
ax.set_title('台南成大店：每日杯數與最高溫')
plt.show()
'''),
        dict(title='各門市的甜度占比，畫成百分比堆疊長條圖',
             hint='`pd.crosstab(列, 欄, normalize=\'index\')` 先算出占比表；`.plot.barh(stacked=True)` 一行畫出堆疊長條。',
             starter='''
sweet = pd.crosstab(orders['門市'], orders[___], normalize='index')[['正常糖', '少糖', '半糖', '微糖', '無糖']] * 100
sweet.plot.barh(stacked=___, figsize=(10, 4), colormap='copper', title='各門市甜度占比（%）')
plt.show()
''',
             check='''
check('sweet', pd.crosstab(orders['門市'], orders['甜度'], normalize='index')[['正常糖', '少糖', '半糖', '微糖', '無糖']] * 100)
''',
             solution='''
sweet = pd.crosstab(orders['門市'], orders['甜度'], normalize='index')[['正常糖', '少糖', '半糖', '微糖', '無糖']] * 100
sweet.plot.barh(stacked=True, figsize=(10, 4), colormap='copper', title='各門市甜度占比（%）')
plt.show()
'''),
        dict(title='會員 vs. 非會員：訂單金額的分布長得一樣嗎？',
             hint='`sns.histplot(data=表格, x=欄位, hue=分組欄位)` 會用不同顏色畫出每一組的分布。',
             starter='''
sns.histplot(data=per_order, x='金額', hue=___, bins=40, element='step')
plt.title('會員 vs. 非會員訂單金額分布')
plt.show()
''',
             solution='''
sns.histplot(data=per_order, x='金額', hue='會員', bins=40, element='step')
plt.title('會員 vs. 非會員訂單金額分布')
plt.show()
'''),
    )
    return NOTEBOOK, files, cells
