"""第 13 章 日期和時間：民國年月轉日期、resample、年增率（pct_change）、rolling 與異常日、dt 屬性、時區轉換——全部用真實資料。"""
from nbtools import md, code, setup_cell, font_cell, header, exercises, copy_real

CHAPTER = '日期和時間'
NOTEBOOK = '範例_電費漲了多少_空汙哪天最嚴重_時間序列.ipynb'
SOURCES = ['power_home', 'aqi', 'mrt']


def build(out):
    files = [copy_real(out, 'power_home'), copy_real(out, 'aqi'), copy_real(out, 'mrt')]
    desc = [(files[0], '台電住宅每戶每月平均用電與電費（日期是**民國年月** `10701`）'),
            (files[1], '環境部近一年、全台 80 多個測站的每日 AQI'),
            (files[2], '臺北捷運 2026 年 3 月各站每小時進出站人次')]

    cells = [
        header(CHAPTER, NOTEBOOK, '📅 電費漲了多少？空汙哪天最嚴重？用時間序列看懂變化',
               '「最近電費好像變貴了？」「這幾天空氣好差！」——這些感覺都跟**時間**有關。'
               '今天你手上有三份帶著時間的真實資料：八年的電費、一年的空氣品質、一個月的捷運人潮。'
               '你要學會把各種奇怪的日期格式（像民國年 `10701`）變成 pandas 看得懂的時間，'
               '再用 **resample、年增率、移動平均** 回答：**電費到底漲了多少？哪幾天的空汙特別嚴重？**',
               desc, SOURCES),
        setup_cell(CHAPTER, files),
        font_cell(),
        md('''
## 任務 1：民國年月 `10701` → 真正的日期

**白話說明**：`10701` 是民國 107 年 1 月。拆成年和月：`10701 // 100 = 107`（加 1911 變西元 2018）、`10701 % 100 = 1`。再用 `pd.to_datetime` 組成日期，並設成**索引**——時間當索引，才能用 resample、依年份篩選。
'''),
        code('''
import pandas as pd
import matplotlib.pyplot as plt

power = pd.read_csv('台電住宅每戶平均用電與電費.csv')
power.columns = ['年月', '度數', '去年同期度數', '電費', '去年同期電費']

power['日期'] = pd.to_datetime(pd.DataFrame({'year': power['年月'] // 100 + 1911,   # 民國 → 西元
                                             'month': power['年月'] % 100,
                                             'day': 1}))
power = power.set_index('日期')
print(power.index.min().date(), '～', power.index.max().date())
power[['年月', '度數', '電費']].tail()
'''),
        md('''
## 任務 2：每戶一年要付多少電費？——`resample`

**白話說明**：`resample('YE')` 把資料「依年」重新分組（YE = Year End，每年年底），再 `.sum()` 加總。就像 groupby，只是分組依據是時間。
'''),
        code('''
yearly = power['電費'].resample('YE').sum()                            # 每年加總
yearly.index = yearly.index.year
display(yearly.to_frame('一年電費(元)'))

ax = yearly.loc[2018:2025].plot.bar(figsize=(9, 4), color='#2E86C1', title='每戶一年的平均電費（元）')
ax.bar_label(ax.containers[0])
plt.show()
'''),
        md('''
> 💡 **看懂結果**：2019 年每戶一年電費約 9,200 元，2025 年將近 **10,850 元**——六年漲了快 18%。2024 年那一跳特別明顯：那年台電調漲了電價。
> （2026 年還沒過完，只有到 9 月的資料，不能直接和其他年比。）
'''),
        md('''
## 任務 3：今年比去年貴多少？——年增率 `pct_change(12)`

**白話說明**：月資料要比「去年同一個月」，才不會被季節影響（夏天本來就比較貴）。`pct_change(12)` 就是「跟 12 筆之前比，變化了百分之幾」。
'''),
        code('''
power['年增率%'] = (power['電費'].pct_change(12) * 100).round(1)
display(power.loc['2026', ['電費', '年增率%']])                        # 日期索引可以直接用年份字串篩選

recent = power['年增率%'].loc['2023':]
recent.index = recent.index.strftime('%Y-%m')                           # 日期 → '2023-01' 文字，長條圖的 X 軸才好讀
ax = recent.plot.bar(figsize=(12, 4), color=recent.gt(0).map({True: '#C0392B', False: '#27AE60'}),
                     title='每月電費年增率（紅＝比去年貴、綠＝比去年便宜）')
plt.show()
'''),
        md('''
> 💡 **看懂結果**：2026 年 4 月以後，每個月的電費都比去年同期**貴 5～10%**。資料本身也附了「去年同期電費」欄位，你可以拿來驗算：`電費 / 去年同期電費 - 1` 應該和 `pct_change(12)` 算出來的一樣。
'''),
        md('''
## 任務 4：空氣品質的「趨勢」與「異常日」——`rolling`

**白話說明**：每天的 AQI 起伏很大，很難看出趨勢。`rolling(7).mean()` 是「**7 日移動平均**」：每一天都改成「包含自己在內的 7 天平均」，線條就變平滑了。
再拿每天的值除以「前後一個月的中位數」，比值特別高的，就是**突然變差的異常日**。
'''),
        code('''
aqi = pd.read_csv('日空氣品質指標_近一年.csv', parse_dates=['monitordate'])
daily = aqi.groupby('monitordate')['aqi'].mean()                        # 每天、全台測站平均

smooth = daily.rolling(7, center=True).mean()                           # 7 日移動平均
normal = daily.rolling(31, center=True, min_periods=10).median()        # 前後 15 天的中位數 = 「平常」水準
abnormal = daily[daily / normal > 1.5]                                  # 比平常高 50% 以上

ax = daily.plot(figsize=(13, 4.5), alpha=0.35, color='gray', label='每日')
smooth.plot(ax=ax, color='#2E86C1', linewidth=2.5, label='7 日移動平均')
ax.scatter(abnormal.index, abnormal.values, color='#C0392B', zorder=5, label='異常日')
ax.axhline(100, color='#E67E22', linestyle='--', linewidth=1)
ax.set_title('全台平均 AQI：一年的變化'); ax.legend()
plt.show()

print('異常日：'); display(abnormal.round(0).to_frame('全台平均 AQI'))
'''),
        md('''
> 💡 **看懂結果**：藍色的移動平均線清楚畫出「**冬春高、夏天低**」的季節變化；紅點是比「平常」高 50% 以上、突然變差的日子：冬天的多半是境外污染隨東北季風移入；夏天偶爾也有，常是天氣穩定、風很小，污染物散不出去的時候。
'''),
        code('''
monthly = daily.resample('ME').mean().round(1)                           # 每月平均（ME = Month End）
monthly.index = monthly.index.strftime('%Y-%m')
monthly.to_frame('全台平均 AQI')
'''),
        md('''
## 任務 5：捷運的日期與時段——`dt` 屬性

**白話說明**：時間欄位後面加 `.dt`，就能取出各種資訊：`.dt.day_of_week`（星期幾，0 = 星期一）、`.dt.day_name()`（英文星期名）、`.dt.hour`（小時）……。這份資料的「日期」和「時段」是分開的，先組成完整的時間。
'''),
        code('''
mrt = pd.read_csv('臺北捷運各站分時進出量_202603.csv', parse_dates=['日期'])
mrt['時間'] = mrt['日期'] + pd.to_timedelta(mrt['時段'], unit='h')         # 日期 + 幾小時 = 完整時間
mrt['星期'] = mrt['時間'].dt.day_of_week

by_weekday = mrt.groupby(mrt['時間'].dt.date)['進站人次'].sum()             # 每天的總進站人次
by_weekday.index = pd.to_datetime(by_weekday.index)
week_avg = by_weekday.groupby(by_weekday.index.day_of_week).mean().round(0)
week_avg.index = ['一', '二', '三', '四', '五', '六', '日']
week_avg.to_frame('平均每天進站人次')
'''),
        md('''
> 💡 **看懂結果**：星期五是一週最多人搭捷運的日子（上班＋週五晚上出門玩），星期日最少。
'''),
        md('''
## 任務 6：時區——國際合作夥伴要 UTC 時間

**白話說明**：電腦裡的時間如果沒有標註時區，就是「不知道是哪裡的時間」。`tz_localize('Asia/Taipei')` 是「**標註**：這是台北時間」；`tz_convert('UTC')` 是「**換算**成 UTC 時間」（台北 = UTC+8）。
'''),
        code('''
peak = mrt.loc[mrt['進站人次'].idxmax(), ['時間', '車站', '進站人次']]
print('整個月單一小時最多人進站：', peak['車站'], peak['時間'], peak['進站人次'], '人次')

t = pd.Series([peak['時間']]).dt.tz_localize('Asia/Taipei')               # 標註：這是台北時間
print('台北時間：', t[0])
print('UTC 時間：', t.dt.tz_convert('UTC')[0])                            # 換算成 UTC（少 8 小時）
print('日本時間：', t.dt.tz_convert('Asia/Tokyo')[0])
'''),
    ] + exercises(
        dict(title='這一年，全台空氣最差的是哪一週？',
             hint='`daily.resample(\'W\')` 把每天的 AQI 依「週」分組（週日為一週結束），`.mean()` 算每週平均，再用 `idxmax()`。',
             starter='''
weekly = daily.resample(___).mean()
worst_week = weekly.idxmax()
print('最差的一週（週日結束）：', worst_week.date(), '平均 AQI', round(weekly.max(), 1))
''',
             check='''
check('worst_week', daily.resample('W').mean().idxmax())
''',
             solution='''
weekly = daily.resample('W').mean()
worst_week = weekly.idxmax()
print('最差的一週（週日結束）：', worst_week.date(), '平均 AQI', round(weekly.max(), 1))
'''),
        dict(title='2018 年以來，電費年增率最高的是哪個月？漲了幾 %？',
             hint='任務 3 已經算好 `power[\'年增率%\']`，用 `idxmax()` 找出最大的日期，`.max()` 取出數值。',
             starter='''
top_month = power['年增率%'].___()
print('年增率最高：', top_month.strftime('%Y-%m'), power['年增率%'].max(), '%')
''',
             check='''
check('top_month', power['電費'].pct_change(12).idxmax())
''',
             solution='''
top_month = power['年增率%'].idxmax()
print('年增率最高：', top_month.strftime('%Y-%m'), power['年增率%'].max(), '%')
'''),
        dict(title='用「去年同期電費」欄位驗算年增率',
             hint='年增率 = 本期 ÷ 去年同期 − 1，再乘以 100。和 `pct_change(12)` 的結果比一比，應該幾乎一樣（只有最前面 12 個月 `pct_change` 算不出來）。',
             starter='''
check_yoy = ((power['電費'] / power[___] - 1) * 100).round(1)
display(pd.DataFrame({'pct_change(12)': power['年增率%'], '用去年同期欄位': check_yoy}).tail(6))
''',
             check='''
check('check_yoy', ((power['電費'] / power['去年同期電費'] - 1) * 100).round(1))
''',
             solution='''
check_yoy = ((power['電費'] / power['去年同期電費'] - 1) * 100).round(1)
display(pd.DataFrame({'pct_change(12)': power['年增率%'], '用去年同期欄位': check_yoy}).tail(6))
'''),
    )
    return NOTEBOOK, files, cells
