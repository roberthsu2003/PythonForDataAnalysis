"""第 9 章 數據整理：內政部三年人口 concat、台電用電 merge（台／臺對不上）、validate、pivot / melt。"""
from nbtools import md, code, setup_cell, header, exercises, copy_real, latest

CHAPTER = '數據整理_連接_合併_重塑'
NOTEBOOK = '範例_誰最會用電_人口與用電資料大合併.ipynb'
SOURCES = ['population_112', 'population_113', 'population_114', 'power_city', 'recycle']


def build(out):
    files = [copy_real(out, f'population_{y}') for y in (112, 113, 114)]
    files += [copy_real(out, 'power_city'), copy_real(out, 'recycle')]
    desc = [(files[0], '內政部各鄉鎮市區年底人口與面積：民國 112 年（2023）'),
            (files[1], '同上：民國 113 年（2024）'),
            (files[2], '同上：民國 114 年（2025）'),
            (files[3], '台電各縣市每月售電量（住宅、服務業、工業、農林漁牧）'),
            (files[4], '臺北市各區每月資源回收量（Big5、民國年；練習題用）')]

    cells = [
        header(CHAPTER, NOTEBOOK, '🔗 誰最會用電？把人口與用電資料合併成一張表',
               '新聞說「某某縣市最耗電」，但人多的地方本來就用比較多電，這樣比公平嗎？要回答「**每個人**用多少電」，'
               '需要兩個機關的資料：台電的**各縣市用電**，和內政部的**各縣市人口**。'
               '今天你要把三年的人口檔接起來（concat）、再和用電資料合併（merge）——然後你會發現，'
               '**兩個機關連「臺北市」怎麼寫都不一樣**。',
               desc, SOURCES),
        setup_cell(CHAPTER, files),
        md('''
## 任務 1：三年的人口檔，上下接成一張表——`concat`

**白話說明**：三個 JSON 檔欄位一模一樣，只是年份不同，用 `pd.concat` 上下接起來。內政部的 API 把資料放在 `responseData` 這一層。
'''),
        code('''
import json
import pandas as pd

frames = []
for year in [112, 113, 114]:
    with open(f'各鄉鎮市區人口密度_{year}年.json', encoding='utf-8') as f:
        frames.append(pd.DataFrame(json.load(f)['responseData']))     # 每一年一張表

pop = pd.concat(frames, ignore_index=True)                            # 上下接起來，重新編列號
pop.columns = ['年度', '區域', '人口', '面積', '人口密度']
print(pop.shape)
print(pop.dtypes)                                                     # 全部都是文字！
pop.head()
'''),
        md('''
## 任務 2：數字是文字、還有「…」——轉型態

**白話說明**：API 回傳的數字全部是**文字**，要用 `pd.to_numeric` 轉成數字。但轉換時會出錯——因為**東沙群島、南沙群島的人口寫成「…」**（沒有常住人口統計）。`errors='coerce'` 讓轉不了的變成 `NaN`。
'''),
        code('''
print(pop[~pop['人口'].str.isdigit()])                               # 哪些「人口」不是純數字？

pop['人口'] = pd.to_numeric(pop['人口'], errors='coerce')             # 「…」→ NaN
pop['縣市'] = pop['區域'].str[:3]                                      # 「新北市板橋區」→「新北市」
pop['西元年'] = pop['年度'].astype(int) + 1911

total = pop.groupby('西元年')['人口'].sum()
display(total.to_frame('全台人口').style.format('{:,.0f}'))
print('兩年少了：', f'{total[2023] - total[2025]:,.0f} 人')
'''),
        md('''
> 💡 **看懂結果**：台灣人口從 2023 年底的 2,342 萬，到 2025 年底剩 2,330 萬——**兩年少了 12 萬人**，差不多是整個澎湖縣的人口不見了。少子化正在發生。
'''),
        md('''
## 任務 3：把用電和人口合併——`merge`，然後……對不上！

**白話說明**：`merge` 依照「共同的欄位」把兩張表左右接起來，就像 Excel 的 VLOOKUP。加上 `indicator=True` 會多一欄 `_merge`，告訴你每一列是「兩邊都有」還是「只有一邊有」——**合併後一定要檢查**。
'''),
        code('''
pd.set_option('display.float_format', '{:,.0f}'.format)                 # 大數字加千分位、不用科學記號（5.67e+08 很難讀）

power = pd.read_csv('台電各縣市用電統計.csv', thousands=',', usecols=range(5)).dropna(subset=['年月'])
home2025 = (power[(power['年月'] >= 11401) & (power['年月'] <= 11412) & (power['用電性質'] == '住宅')]
            .groupby('縣市', as_index=False)['售電量(度)'].sum())                 # 2025 年各縣市住宅用電

pop2025 = pop[pop['西元年'] == 2025].groupby('縣市', as_index=False)['人口'].sum()

merged = home2025.merge(pop2025, on='縣市', how='outer', indicator=True)
print(merged['_merge'].value_counts())
merged[merged['_merge'] != 'both'].sort_values('縣市')
'''),
        md('''
> 😱 **只有 18 個縣市對得上！** 仔細看：台電寫「**台**北市、**台**中市、**台**南市、**台**東縣」，內政部寫「**臺**北市、**臺**中市……」。
> 對電腦來說，「台」和「臺」是兩個完全不同的字。另外「東沙群」「南沙群」是人口檔切前三個字時切出來的，它們本來就沒有用電資料。
>
> **這就是真實世界的資料合併**：每個機關有自己的寫法，合併前一定要先統一「鑰匙」。
'''),
        code('''
home2025['縣市'] = home2025['縣市'].str.replace('台', '臺')            # 統一寫法：台 → 臺

merged = home2025.merge(pop2025, on='縣市', how='inner', validate='one_to_one')   # validate：確認兩邊的縣市都不重複
print('合併後的縣市數：', len(merged))
merged['每人住宅用電(度)'] = (merged['售電量(度)'] / merged['人口']).round(0)
merged.sort_values('每人住宅用電(度)', ascending=False)
'''),
        md('''
> 💡 **看懂結果**：每人住宅用電最多的是**臺東縣、連江縣、新竹市、新竹縣**；最少的是**金門縣**。南部縣市不一定比較高——用電還跟家裡的人數、房子大小、電器有關。
>
> 🤖 **換你問 AI**：「我要用『縣市』合併兩張表，但一張寫『台北市』、一張寫『臺北市』。請先統一寫法再合併，並用 indicator=True 檢查有沒有對不到的資料。」
'''),
        md('''
## 任務 4：寬表與長表——`pivot` 和 `melt`

**白話說明**：
- **長表**（一列一個「縣市＋用電類別」）適合存資料、畫圖；
- **寬表**（一列一個縣市，用電類別攤成欄位）適合人看、做比較。

`pivot_table` 把長表變寬表，`melt` 把寬表變回長表。
'''),
        code('''
y2025 = power[(power['年月'] >= 11401) & (power['年月'] <= 11412)].copy()
y2025['縣市'] = y2025['縣市'].str.replace('台', '臺')

wide = y2025.pivot_table(index='縣市', columns='用電性質', values='售電量(度)', aggfunc='sum')   # 長表 → 寬表
wide = wide.join(pop2025.set_index('縣市'))                                               # join：依索引合併
per_person = wide[['住宅', '服務業', '工業', '農林漁牧']].div(wide['人口'], axis=0).round(0)  # 每一欄都除以人口
per_person['合計'] = per_person.sum(axis=1)
per_person.sort_values('合計', ascending=False).head(6)
'''),
        md('''
> 💡 **看懂結果**：算上工業用電，第一名是**新竹縣**——每人一年 2 萬度電，是全台平均（約 9,900 度）的 2 倍多！因為新竹科學園區的晶圓廠就在這裡；第三名臺南市則有南部科學園區。
> **同樣是「每人用電」，只看住宅和看全部，答案完全不同。** 報告時一定要說清楚你算的是哪一種。
'''),
        code('''
long = per_person.drop(columns='合計').reset_index().melt(id_vars='縣市', var_name='用電性質', value_name='每人度數')   # 寬表 → 長表
print(long.shape)
long.head(8)
'''),
        md('''
## 任務 5：哪些縣市人口在增加？——長表轉寬表算成長率
'''),
        code('''
county = pop.pivot_table(index='縣市', columns='西元年', values='人口', aggfunc='sum').dropna()   # 縣市 × 年
county['兩年變化%'] = ((county[2025] / county[2023] - 1) * 100).round(2)
county.sort_values('兩年變化%', ascending=False)
'''),
        md('''
> 💡 **看懂結果**：只有**桃園市、新竹縣、臺中市、新北市**人口在增加（桃園 +1.6%），其他縣市都在減少，**臺北市兩年少了將近 3%**。
> 房價、工作機會、交通——人口會往「住得起、又有工作」的地方移動。
'''),
        latest('''
import pandas as pd, urllib.request, json
year = 115                                                   # 改成想查的民國年（每年年中後才會有前一年的資料）
raw = urllib.request.urlopen(f'https://www.ris.gov.tw/rs-opendata/api/v1/datastore/ODRP048/{year}').read()
pd.DataFrame(json.loads(raw)['responseData']).head()
'''),
    ] + exercises(
        dict(title='2025 年底，全台灣有多少人？',
             hint='任務 2 已經算好 `total`（依西元年加總的人口），用 `total[2025]` 取出來。',
             starter='''
people_2025 = total[___]
print(f'2025 年底全台人口：{people_2025:,.0f} 人')
''',
             check='''
check('people_2025', pop.loc[pop['西元年'] == 2025, '人口'].sum())
''',
             solution='''
people_2025 = total[2025]
print(f'2025 年底全台人口：{people_2025:,.0f} 人')
'''),
        dict(title='臺北市哪一區「每人」資源回收最多？',
             hint='回收資料的「區隊」寫成 `大安區隊`，人口資料的「區域」寫成 `臺北市大安區`。把區隊改成同樣的寫法：`\'臺北市\' + 區隊.str.replace(\'區隊\', \'區\')`，再合併。民國 114 年就是 2025 年。',
             starter='''
recycle = pd.read_csv('臺北市各區資源回收量.csv', encoding='cp950')
recycle.columns = ['年度', '月', '行政區代碼', '區隊', '回收量(噸)']
r2025 = recycle[recycle['年度'] == 114].groupby('區隊', as_index=False)['回收量(噸)'].sum()
r2025['區域'] = '臺北市' + r2025['區隊'].str.replace(___, '區')          # 大安區隊 → 臺北市大安區

per_kg = r2025.merge(pop[pop['西元年'] == 2025], on=___, how='inner')
per_kg['每人回收(公斤)'] = (per_kg['回收量(噸)'] * 1000 / per_kg['人口']).round(1)
best_district = per_kg.loc[per_kg['每人回收(公斤)'].idxmax(), '區域']
display(per_kg[['區域', '回收量(噸)', '人口', '每人回收(公斤)']].sort_values('每人回收(公斤)', ascending=False))
print('每人回收最多：', best_district)
''',
             check='''
_r = pd.read_csv('臺北市各區資源回收量.csv', encoding='cp950')
_r.columns = ['年度', '月', '行政區代碼', '區隊', '回收量(噸)']
_r = _r[_r['年度'] == 114].groupby('區隊', as_index=False)['回收量(噸)'].sum()
_r['區域'] = '臺北市' + _r['區隊'].str.replace('區隊', '區')
_m = _r.merge(pop[pop['西元年'] == 2025], on='區域')
check('best_district', _m.loc[(_m['回收量(噸)'] / _m['人口']).idxmax(), '區域'])
''',
             solution='''
recycle = pd.read_csv('臺北市各區資源回收量.csv', encoding='cp950')
recycle.columns = ['年度', '月', '行政區代碼', '區隊', '回收量(噸)']
r2025 = recycle[recycle['年度'] == 114].groupby('區隊', as_index=False)['回收量(噸)'].sum()
r2025['區域'] = '臺北市' + r2025['區隊'].str.replace('區隊', '區')

per_kg = r2025.merge(pop[pop['西元年'] == 2025], on='區域', how='inner')
per_kg['每人回收(公斤)'] = (per_kg['回收量(噸)'] * 1000 / per_kg['人口']).round(1)
best_district = per_kg.loc[per_kg['每人回收(公斤)'].idxmax(), '區域']
display(per_kg[['區域', '回收量(噸)', '人口', '每人回收(公斤)']].sort_values('每人回收(公斤)', ascending=False))
print('每人回收最多：', best_district)
# 「其他」區隊對不到任何行政區，inner 合併時會被排除——合併後記得檢查少了什麼
'''),
        dict(title='把縣市人口的寬表轉回長表',
             hint='`county` 是「縣市 × 年」的寬表。先 `drop(columns=\'兩年變化%\')`、`reset_index()`，再 `melt(id_vars=\'縣市\', var_name=\'西元年\', value_name=\'人口\')`。',
             starter='''
county_long = (county.drop(columns='兩年變化%').reset_index()
                     .melt(id_vars=___, var_name='西元年', value_name=___))
print(county_long.shape)
county_long.head()
''',
             check='''
check('county_long', county.drop(columns='兩年變化%').reset_index()
                     .melt(id_vars='縣市', var_name='西元年', value_name='人口'))
''',
             solution='''
county_long = (county.drop(columns='兩年變化%').reset_index()
                     .melt(id_vars='縣市', var_name='西元年', value_name='人口'))
print(county_long.shape)
county_long.head()
'''),
    )
    return NOTEBOOK, files, cells
