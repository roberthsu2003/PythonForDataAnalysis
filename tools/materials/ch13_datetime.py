"""第 13 章 日期和時間：to_datetime、dt、resample、月增率 / 年增率、rolling、異常日偵測、時區轉換。"""
import numpy as np
import pandas as pd

from common import STORES, daily_sales, rng
from nbtools import md, code, setup_cell, font_cell, header, exercises

CHAPTER = '日期和時間'
NOTEBOOK = '範例_茶語時光_兩年營收與外送時區.ipynb'


def build(out):
    r = rng(130)
    d = daily_sales('2023-01-01', '2024-12-31')
    d['日期'] = d['日期'].dt.year.astype(str) + '/' + d['日期'].dt.month.astype(str) + '/' + d['日期'].dt.day.astype(str)
    d[['日期', '門市', '杯數', '營收']].to_csv(out / '每日營收_2023-2024.csv', index=False, encoding='utf-8-sig')

    n = 6000
    day = pd.to_datetime('2024-09-01') + pd.to_timedelta(r.integers(0, 30, n), unit='D')
    slot = r.choice(3, n, p=[0.42, 0.38, 0.20])                     # 午餐、晚餐、宵夜
    hour = np.select([slot == 0, slot == 1], [r.normal(12.2, 0.8, n), r.normal(18.3, 0.9, n)], r.normal(22.2, 0.7, n))
    local = day + pd.to_timedelta(np.clip(hour, 10, 23.9), unit='h')
    utc = (local - pd.Timedelta(hours=8)).strftime('%Y-%m-%dT%H:%M:%SZ')    # 平台用 UTC 儲存
    stores = STORES[STORES['門市代碼'] != 'S04']['門市'].values
    pd.DataFrame({'訂單編號': [f'UB{i:06d}' for i in range(1, n + 1)], '下單時間_UTC': utc,
                  '平台': r.choice(['FoodRun', 'QuickEat'], n, p=[0.6, 0.4]), '門市': r.choice(stores, n),
                  '金額': (r.gamma(2.5, 45, n) + 60).round().astype(int)}) \
        .sort_values('下單時間_UTC').to_csv(out / '外送訂單_UTC_2024-09.csv', index=False, encoding='utf-8-sig')

    files = ['每日營收_2023-2024.csv', '外送訂單_UTC_2024-09.csv']
    desc = [('每日營收_2023-2024.csv', '2023～2024 兩年、5 家門市的每日杯數與營收（日期格式是「2024/1/5」的文字）'),
            ('外送訂單_UTC_2024-09.csv', '9 月外送平台訂單，時間以 UTC（世界標準時間）儲存')]

    cells = [
        header(CHAPTER, NOTEBOOK, '📅 茶語時光：兩年營收趨勢與外送時區之謎',
               '品牌成立滿兩年，董事會想看：「今年比去年成長多少？哪個月最好？颱風到底讓我們少賺多少？」'
               '同時，外送部門抱怨：「平台報表說我們凌晨 4 點最忙，這怎麼可能？」你要用 pandas 的時間工具，一次解開這些問題。', desc),
        setup_cell(CHAPTER, files),
        font_cell(),
        md('''
## 任務 1：文字變日期——星期幾生意最好？

**白話說明**：「2024/1/5」只是文字，要先用 `pd.to_datetime` 轉成真正的日期，才能取出星期幾、月份、季度。
'''),
        code('''
import pandas as pd
import matplotlib.pyplot as plt

daily = pd.read_csv('每日營收_2023-2024.csv')
print('轉換前的型態：', daily['日期'].dtype, daily['日期'].iloc[0])
daily['日期'] = pd.to_datetime(daily['日期'], format='%Y/%m/%d')       # 指定格式：年/月/日
print('轉換後的型態：', daily['日期'].dtype)

daily['星期'] = daily['日期'].dt.day_of_week                             # 0 = 星期一 … 6 = 星期日
week = daily.pivot_table(index='星期', columns='門市', values='杯數', aggfunc='mean').round(0)
week.index = ['一', '二', '三', '四', '五', '六', '日']
display(week)
'''),
        md('''
## 任務 2：每日 → 每月——resample 做月報
'''),
        code('''
wide = daily.pivot(index='日期', columns='門市', values='營收')         # 日期當索引，才能用 resample
monthly = wide.resample('ME').sum()                                     # 'ME'＝每月月底彙總（新版 pandas 寫法，舊版是 'M'）
monthly['全品牌'] = monthly.sum(axis=1)
display((monthly / 10000).round(1).tail(6))

(monthly['全品牌'] / 10000).plot(figsize=(12, 4), marker='o', title='全品牌每月營收（萬元）')
plt.show()
'''),
        md('''
## 任務 3：月增率與年增率——今年到底成長多少？

**白話說明**：
- **月增率（MoM）**：和「上個月」比 → `pct_change()`
- **年增率（YoY）**：和「去年同月」比 → `pct_change(12)`（往前 12 個月）

季節性很強的生意（飲料夏天好賣），**看年增率才公平**——拿 7 月和 6 月比沒有意義，拿今年 7 月和去年 7 月比才有意義。
'''),
        code('''
brand = monthly['全品牌']
growth = pd.DataFrame({'營收(萬)': (brand / 10000).round(1),
                       '月增率%': (brand.pct_change() * 100).round(1),
                       '年增率%': (brand.pct_change(12) * 100).round(1)})
display(growth.loc['2024'])                                              # 只看 2024 年（日期索引可以直接用年份字串篩選）
print('\\n2024 全年營收年成長：', round((brand['2024'].sum() / brand['2023'].sum() - 1) * 100, 1), '%')
'''),
        md('''
> 💡 **看懂結果**：月增率忽正忽負（受季節影響），但年增率每個月都是正的——**品牌真的在成長**。7 月和 10 月的年增率特別低：2024 年 7 月有凱米颱風、10 月有山陀兒與康芮兩個颱風；6 月年增率最高，因為推出了「每週三第二杯半價」活動。
>
> 🤖 **換你問 AI**：「請把每日營收用 resample 彙總成每月，計算月增率與年增率，並說明為什麼季節性產業要看年增率。」
'''),
        md('''
## 任務 4：rolling 移動平均——把「颱風日」自動抓出來

**白話說明**：用前後 15 天的移動平均當作「正常水準」，某天的營收如果低於正常水準的 60%，就標記為異常日。
'''),
        code('''
brand_daily = wide.sum(axis=1)                                          # 全品牌每日營收
normal = brand_daily.rolling(31, center=True, min_periods=10).median() # 前後 15 天的中位數 = 正常水準
ratio = brand_daily / normal
abnormal = ratio[ratio < 0.6]
print('異常低的日子：\\n', abnormal.round(2))

ax = (brand_daily / 10000).plot(figsize=(14, 4), alpha=0.4, label='每日營收')
(normal / 10000).plot(ax=ax, color='black', label='正常水準（31 日移動中位數）')
ax.scatter(abnormal.index, brand_daily[abnormal.index] / 10000, color='red', zorder=3, label='異常日')
ax.legend(); ax.set_title('全品牌每日營收（萬元）')
plt.show()

loss = (normal[abnormal.index] - brand_daily[abnormal.index]).sum()
print('異常日估計少賺：', f'{loss:,.0f}', '元')
'''),
        md('''
> 💡 **看懂結果**：程式自動抓出的 4 個異常日，全部都是全國性的颱風假：凱米（7/24、7/25）、山陀兒（10/3）、康芮（10/31）——**不用人工翻行事曆，數據自己會告訴你哪天出事了**。（只影響南部兩家店的颱風，全品牌合計沒有跌破 60%，所以沒被抓到；想抓得更細，可以改成每家店分開偵測。）把「估計少賺的金額」放進報告，就能說服老闆投保營業中斷險或強化外送。
'''),
        md('''
## 任務 5：外送時區之謎——凌晨 4 點最忙？

**白話說明**：外送平台用 **UTC（世界標準時間）** 記錄時間，台灣是 **UTC+8**。沒有轉換時區，所有時間都差了 8 小時。
'''),
        code('''
delivery = pd.read_csv('外送訂單_UTC_2024-09.csv')
display(delivery.head(3))

delivery['UTC時間'] = pd.to_datetime(delivery['下單時間_UTC'], utc=True)          # 標記為 UTC 時間
delivery['台北時間'] = delivery['UTC時間'].dt.tz_convert('Asia/Taipei')           # 轉換成台北時間

fig, axes = plt.subplots(1, 2, figsize=(14, 4), sharey=True)
delivery['UTC時間'].dt.hour.value_counts().sort_index().plot.bar(ax=axes[0], color='gray', title='錯誤：直接用 UTC，凌晨最忙？')
delivery['台北時間'].dt.hour.value_counts().sort_index().plot.bar(ax=axes[1], color='#8B5E3C', title='正確：轉成台北時間，午餐、晚餐、宵夜')
plt.show()
'''),
        md('''
> 💡 **看懂結果**：轉換時區後，三個高峰清清楚楚：**中午 12 點、晚上 6 點、宵夜 10 點**。外送人力與備料應該照右邊的圖安排，而不是左邊！
>
> 🤖 **換你問 AI**：「這份外送訂單的時間是 UTC（格式如 2024-09-01T04:12:00Z），請轉成台北時間，並畫出每小時訂單數長條圖。」
'''),
        md('''
## 任務 6：季度報表——to_period
'''),
        code('''
quarter = monthly.drop(columns='全品牌').resample('QE').sum()           # 每季彙總（'QE'＝季底）
quarter.index = quarter.index.to_period('Q')                            # 2024-03-31 → 2024Q1，報表更好讀
display((quarter / 10000).round(0))
''')
    ] + exercises(
        dict(title='2024 年營收最高的是哪一週？',
             hint='`resample(\'W\')` 把每天彙總成每週（週日為一週結束）；`[\'2024\']` 可以只取 2024 年。',
             starter='''
weekly = brand_daily.resample(___).sum()
best_week = weekly['2024'].idxmax()
print('營收最高的週（週日為一週結束）：', best_week.date(), f"{weekly['2024'].max():,.0f}")
''',
             check='''
check('best_week', brand_daily.resample('W').sum()['2024'].idxmax())
''',
             solution='''
weekly = brand_daily.resample('W').sum()
best_week = weekly['2024'].idxmax()
print('營收最高的週（週日為一週結束）：', best_week.date(), f"{weekly['2024'].max():,.0f}")
'''),
        dict(title='台南成大店 2024 年每個月的「年增率」，哪個月成長最多？',
             hint='年增率是「和 12 個月前比」：`pct_change(12)`；結果乘以 100 就是百分比。',
             starter='''
tn_growth = monthly['台南成大店'].pct_change(___)['2024'] * 100
display(tn_growth.round(1))
print('成長最多：', tn_growth.idxmax().strftime('%Y-%m'))
''',
             check='''
check('tn_growth', monthly['台南成大店'].pct_change(12)['2024'] * 100)
''',
             solution='''
tn_growth = monthly['台南成大店'].pct_change(12)['2024'] * 100
display(tn_growth.round(1))
print('成長最多：', tn_growth.idxmax().strftime('%Y-%m'))
'''),
        dict(title='外送轉成台北時間後，平日和週末的尖峰時段一樣嗎？',
             hint='`.dt.day_of_week` 中 0 是星期一、5 和 6 是週末；每一組用 `s.dt.hour.value_counts().idxmax()` 找出最多訂單的小時。',
             starter='''
is_weekend = delivery['台北時間'].dt.day_of_week >= ___
peak = delivery.groupby(is_weekend)['台北時間'].apply(lambda s: s.dt.___.value_counts().idxmax())
display(peak.rename(index={False: '平日', True: '週末'}))
''',
             check='''
check('peak', delivery.groupby(delivery['台北時間'].dt.day_of_week >= 5)['台北時間']
                      .apply(lambda s: s.dt.hour.value_counts().idxmax()))
''',
             solution='''
is_weekend = delivery['台北時間'].dt.day_of_week >= 5
peak = delivery.groupby(is_weekend)['台北時間'].apply(lambda s: s.dt.hour.value_counts().idxmax())
display(peak.rename(index={False: '平日', True: '週末'}))
'''),
    )
    return NOTEBOOK, files, cells
