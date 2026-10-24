"""第 4 章 NumPy：用環境部真實 AQI 做成「365 天 × 14 測站」矩陣，練習整批運算、axis、nan、布林篩選與 np.where。"""
import pandas as pd

from nbtools import md, code, setup_cell, header, exercises, read_real, latest

CHAPTER = 'Numpy建立與計算'
NOTEBOOK = '範例_你家附近的空氣好嗎_365天AQI矩陣.ipynb'
SOURCES = ['aqi']
SITES = ['基隆', '林森', '中山', '板橋', '桃園', '新竹', '忠明', '斗六', '臺南', '小港', '屏東', '花蓮', '臺東', '金門']


def build(out):
    aqi = pd.read_csv(read_real('aqi'))
    wide = aqi.pivot(index='monitordate', columns='sitename', values='aqi')[SITES]   # 日期 × 測站
    wide.index.name = '日期'
    wide.to_csv(out / '每日AQI_14測站.csv', float_format='%.0f')                     # 缺值留空白

    files = ['每日AQI_14測站.csv']
    desc = [('每日AQI_14測站.csv', f'近一年（{wide.index[0]}～{wide.index[-1]}）14 個測站的每日空氣品質指標 AQI；'
                                  '整理自環境部「日空氣品質指標」，**空白代表那天測站沒有資料**')]

    cells = [
        header(CHAPTER, NOTEBOOK, '🌫️ 你家附近的空氣好嗎？365 天 × 14 個測站的 AQI 矩陣',
               '早上出門前，你會看手機上的空氣品質嗎？環境部全台有 80 多個測站，每天公布空氣品質指標 AQI'
               '（0～50 良好、51～100 普通、101 以上對敏感族群不健康）。你拿到其中 14 個測站、整整一年的資料，'
               '一共 5,000 多個數字。今天要用 **NumPy 一次算完整張表**，回答：**哪裡的空氣最差？什麼季節最糟？**',
               desc, SOURCES),
        setup_cell(CHAPTER, files),
        md('''
## 任務 1：把 CSV 讀成一個 NumPy 矩陣

**白話說明**：NumPy 的陣列就像一張「全部都是數字」的表格。`np.genfromtxt` 讀數字，遇到空白會自動變成 `nan`（Not a Number，代表「沒有資料」）。日期是文字，另外用 `np.loadtxt(..., dtype=str)` 讀。
'''),
        code('''
import numpy as np

with open('每日AQI_14測站.csv', encoding='utf-8') as f:
    sites = f.readline().strip().split(',')[1:]          # 第一行是標題：取出 14 個測站名稱

dates = np.loadtxt('每日AQI_14測站.csv', delimiter=',', skiprows=1, usecols=0, dtype=str)   # 第 0 欄：日期
aqi = np.genfromtxt('每日AQI_14測站.csv', delimiter=',', skip_header=1, usecols=range(1, 15))  # 第 1～14 欄：AQI

print('測站：', sites)
print('矩陣形狀：', aqi.shape, '→', aqi.shape[0], '天 ×', aqi.shape[1], '個測站')
print('日期範圍：', dates[0], '～', dates[-1])
print('前 3 天：\\n', aqi[:3])
'''),
        md('''
## 任務 2：每個測站的年平均——遇到 nan 怎麼辦？

**你想知道**：一整年下來，哪一個測站的空氣最差？

**白話說明**：`axis=0` 是「**直著算**」（每一欄、每個測站一個答案）；`axis=1` 是「**橫著算**」（每一列、每一天一個答案）。
'''),
        code('''
site_mean = aqi.mean(axis=0)                             # 直著算：每個測站的平均
print(dict(zip(sites, site_mean.round(1).tolist())))
'''),
        md('''
> 😱 **怪了！** 「林森」測站的平均是 `nan`？因為它有幾十天沒資料，**只要有一個 `nan`，整個平均就變成 `nan`**。
>
> 解法：用 `np.nanmean`，它會**跳過 nan**，只用有資料的天數算平均。
'''),
        code('''
site_mean = np.nanmean(aqi, axis=0)                      # 跳過 nan 再算平均
missing = np.isnan(aqi).sum(axis=0)                      # 每個測站有幾天沒資料

order = np.argsort(site_mean)[::-1]                      # 由差到好排序（argsort 由小到大，[::-1] 反轉）
for i in order:
    note = f'（{missing[i]} 天沒資料）' if missing[i] else ''
    print(f'{sites[i]:　<4} 平均 AQI {site_mean[i]:5.1f} ' + '█' * int(site_mean[i] / 4) + note)
'''),
        md('''
> 💡 **看懂結果**：空氣最差的是**斗六、小港、金門、屏東**（平均超過 70），最好的是**花蓮、臺東**（只有 40 出頭）——差了快一倍！
> 斗六、小港附近有工業區與重工業；金門離中國沿海很近，常受境外污染影響；花東有中央山脈擋住西半部的污染。**你住的地方，空氣是哪一種？**
>
> 🤖 **換你問 AI**：「我有一個 365 × 14 的 NumPy 陣列，裡面有 nan。請算出每一欄的平均（跳過 nan），並由大到小列出欄位名稱。」
'''),
        md('''
## 任務 3：全台平均最差的是哪一天？

**白話說明**：換成 `axis=1`——「橫著算」，每一天得到一個 14 個測站的平均。再用 `argmax` / `argmin` 找出最大、最小值在**第幾個位置**，拿這個位置去 `dates` 查日期。
'''),
        code('''
day_mean = np.nanmean(aqi, axis=1)                       # 橫著算：每天 14 個測站的平均（365 個數字）

worst, best = day_mean.argmax(), day_mean.argmin()       # 最大、最小值的位置
print(f'😷 最差的一天：{dates[worst]}，平均 AQI {day_mean[worst]:.0f}')
print(f'😊 最好的一天：{dates[best]}，平均 AQI {day_mean[best]:.0f}')
print('那一天各測站：', dict(zip(sites, aqi[worst].tolist())))
'''),
        md('''
## 任務 4：一年之中，有幾天「對敏感族群不健康」？

**你想知道**：有氣喘的同學，一年有幾天出門要特別小心？

**白話說明**：`aqi > 100` 會對**每一格**判斷，得到一張 True / False 的表。True 會被當成 1，所以 `.sum(axis=0)` 就是每個測站「超過 100 的天數」。（`nan > 100` 會是 False，不會被算進去。）
'''),
        code('''
unhealthy = aqi > 100                                    # 365 × 14 的 True / False
bad_days = unhealthy.sum(axis=0)                         # 直著數：每個測站幾天

for i in np.argsort(bad_days)[::-1]:
    print(f'{sites[i]:　<4} {bad_days[i]:3d} 天 ' + '▇' * int(bad_days[i] / 2))
'''),
        md('''
> 💡 **看懂結果**：斗六和金門一年有將近 **70 天**（大約每 5 天就有 1 天）空氣對敏感族群不健康，花蓮、臺東只有 2 天。**同一個台灣，呼吸到的空氣差很多。**
'''),
        md('''
## 任務 5：替每一天貼上標籤——像 Excel 的 IF

**白話說明**：`np.where(條件, 符合時, 不符合時)` 就像 Excel 的 IF；兩層 `np.where` 就能分三級。`np.unique(..., return_counts=True)` 數每一種標籤出現幾次。
'''),
        code('''
zhongshan = aqi[:, sites.index('中山')]                   # 取出台北中山站那一欄
label = np.where(zhongshan <= 50, '良好', np.where(zhongshan <= 100, '普通', '不健康'))

kinds, counts = np.unique(label, return_counts=True)
print('台北中山站一年的空氣：', dict(zip(kinds, counts.tolist())))
print('最近 7 天：', list(zip(dates[-7:], label[-7:])))
'''),
        md('''
## 任務 6：什麼季節空氣最差？

**白話說明**：日期是 `'2026-01-15'` 這樣的文字，取前 7 個字 `'2026-01'` 就是月份。用「布林遮罩」挑出某個月的那幾列，再算平均。
'''),
        code('''
months = np.array([d[5:7] for d in dates])               # '2026-01-15' → '01'

print('月份  全台平均 AQI')
for m in sorted(set(months)):
    mask = months == m                                   # 這個月的那幾天是 True
    v = np.nanmean(aqi[mask])                            # 這幾天 × 14 個測站，全部一起平均
    print(f' {m} 月   {v:5.1f} ' + '█' * int(v / 2))
'''),
        md('''
> 💡 **看懂結果**：**冬天和春天（11 月～隔年 4 月）最差**，平均接近 70；**夏天（6～8 月）最好**，7 月只有 41。
> 原因：冬天吹東北季風，會把境外污染帶來台灣，而且空氣比較不容易擴散；夏天常下午後雷陣雨，把污染物洗掉。**所以冬天出門，更要看一下 AQI。**
'''),
        latest('''
import pandas as pd
url = ('https://data.moenv.gov.tw/api/v2/aqx_p_434?api_key=846e44e1-8cc5-4893-ad87-c79d2d383706'
       '&format=CSV&limit=1000&sort=monitordate%20desc')
recent = pd.read_csv(url)                                  # 最近幾天、全台所有測站的 AQI
recent.head()
''', note='想看最近幾天、全台 80 多個測站的 AQI？把這段貼到新的一格執行（需要網路）：'),
    ] + exercises(
        dict(title='金門的 AQI，中位數和平均數差多少？',
             hint='`aqi[:, 欄號]` 取出一整欄；中位數是 `np.median()`。金門這一欄沒有 nan，可以直接用 `.mean()`。',
             starter='''
kinmen = aqi[:, sites.index(___)]                   # 取出金門那一欄
kinmen_median = np.___(kinmen)                     # 中位數
kinmen_mean = round(kinmen.mean(), 1)
print('中位數：', kinmen_median, '平均：', kinmen_mean)
''',
             check='''
_k = aqi[:, sites.index('金門')]
check('kinmen_median', np.median(_k))
check('kinmen_mean', round(_k.mean(), 1))
''',
             solution='''
kinmen = aqi[:, sites.index('金門')]
kinmen_median = np.median(kinmen)
kinmen_mean = round(kinmen.mean(), 1)
print('中位數：', kinmen_median, '平均：', kinmen_mean)
# 平均比中位數高：少數幾天特別嚴重的污染，把平均往上拉
'''),
        dict(title='斗六空氣最差的 3 天是哪幾天？',
             hint='`np.argsort(陣列)` 回傳「由小到大排序後的位置」，取最後 3 個 `[-3:]` 再反轉 `[::-1]` 就是最大的 3 個。',
             starter='''
douliu = aqi[:, sites.index('斗六')]
top3 = np.___(douliu)[-3:][::-1]                   # AQI 最高 3 天的位置（由大到小）
for i in top3:
    print(dates[i], douliu[i])
''',
             check='''
check('top3', np.argsort(aqi[:, sites.index('斗六')])[-3:][::-1])
''',
             solution='''
douliu = aqi[:, sites.index('斗六')]
top3 = np.argsort(douliu)[-3:][::-1]
for i in top3:
    print(dates[i], douliu[i])
'''),
        dict(title='紅色警戒！每個測站有幾天 AQI ≥ 150？',
             hint='AQI 151 以上是「對所有族群不健康」（紅色）。`(aqi >= 150)` 得到 True/False，`.sum(axis=0)` 直著數，每個測站一個數字。',
             starter='''
red_days = (aqi >= ___).sum(axis=___)
print(dict(zip(sites, red_days.tolist())))
''',
             check='''
check('red_days', (aqi >= 150).sum(axis=0))
''',
             solution='''
red_days = (aqi >= 150).sum(axis=0)
print(dict(zip(sites, red_days.tolist())))
'''),
    )
    return NOTEBOOK, files, cells
