"""第 5 章 初見 pandas：用文化部真實電影票房練習 Series、DataFrame、新增欄位、篩選、索引對齊與 NaN。"""
from nbtools import md, code, setup_cell, header, exercises, copy_real, latest

CHAPTER = '初見pandas'
NOTEBOOK = '範例_台灣人最愛看什麼電影_第一份pandas報表.ipynb'
SOURCES = ['boxoffice']


def build(out):
    files = [copy_real(out, 'boxoffice')]
    desc = [(files[0], '文化部全國電影票房：2016 年至今 7,000 多部電影的國別、上映日、戲院數、票數與票房金額（JSON）')]

    cells = [
        header(CHAPTER, NOTEBOOK, '🎬 台灣人最愛看什麼電影？用 pandas 做第一份票房報表',
               '你在影評社團負責「年度回顧」專題。文化部公開了**全國每一部電影的票房**——從 2016 年到現在，7,000 多部電影。'
               '用 Python 的清單和字典處理這麼多資料太辛苦了，今天換上新武器 **pandas**：'
               '它會把資料變成一張「會說話的 Excel 表」，讓你一行程式就回答「**2025 年最賣座的是誰？國片表現如何？**」',
               desc, SOURCES),
        setup_cell(CHAPTER, files),
        md('''
## 任務 1：Series——一欄有「名牌」的數字

**白話說明**：`Series` 就像 Excel 的**一欄**，但每個值都掛著一個名牌（index）。用名牌取值，比記「第幾個」直覺多了。
'''),
        code('''
import pandas as pd

top5 = pd.Series([8.57, 7.75, 7.57, 5.74, 4.93],                 # 2025 年前 5 名的票房（億元）
                 index=['鬼滅之刃 無限城篇', '陽光女子合唱團', '動物方城市2', 'F1電影', '阿凡達：火與燼'],
                 name='票房(億)')
display(top5)
print('陽光女子合唱團：', top5['陽光女子合唱團'], '億')          # 用名牌取值
print('前 5 名合計：', top5.sum().round(2), '億；平均：', top5.mean().round(2), '億')
print('破 6 億的：', top5[top5 > 6].index.tolist())              # 條件篩選
'''),
        md('''
## 任務 2：DataFrame——把 7,000 多部電影變成一張表

**白話說明**：`DataFrame` 就是一整張表格：每一欄都是一個 Series。JSON 裡的電影清單是「一部電影一個字典」，直接丟給 `pd.DataFrame()` 就變成表格。
'''),
        code('''
import json

with open('全國電影票房_2016至今.json', encoding='utf-8-sig') as f:
    data = json.load(f)

movies = pd.DataFrame(data['List'])                                # 字典的清單 → 表格（一個字典 = 一列）
print('幾列 × 幾欄：', movies.shape)
movies.head()
'''),
        code('''
movies.describe()                                                  # 數字欄位的統計摘要
'''),
        md('''
> 🕵️ **仔細看 `describe()` 的結果**，你會發現兩個「真實資料的怪現象」：
> 1. `TicketChangeRate`（票房變動率）**全部都是 0**——這一欄沒有任何資訊。
> 2. `Tickets` 和 `TotalTickets`、`Amounts` 和 `TotalAmounts` 的數字**一模一樣**——重複了。
> 3. 票數、票房的最小值（min）是 **-1**——票房不可能是負的！這是系統用 -1 代表「沒有資料」。
>
> 真實資料常常有沒用、重複或「假數字」的欄位，**先看懂、再處理**，算出來的結果才可信。
'''),
        code('''
movies = movies.drop(columns=['TicketChangeRate', 'Tickets', 'Amounts', 'Produce'])   # 刪掉沒用、重複、幾乎空白的欄位
movies = movies.rename(columns={'Country': '國別', 'Name': '片名', 'ReleaseDate': '上映日', 'Issue': '發行商',
                                'TheaterCount': '戲院數', 'TotalTickets': '票數', 'TotalAmounts': '票房'})
print('票房是 -1（沒有資料）的電影：', (movies['票房'] < 0).sum(), '部')
movies = movies[movies['票房'] > 0]                                # 只留下有票房資料的電影
print('清理後：', movies.shape)
movies.head()
'''),
        md('''
## 任務 3：新增欄位——讓表格回答更多問題

**白話說明**：`表格['新欄位'] = 計算式`，整欄一次算完，不用寫迴圈。`.str[:4]` 取文字的前 4 個字。
'''),
        code('''
movies['年'] = movies['上映日'].str[:4].astype(int)                # '2025-08-06T00:00:00' → 2025
movies['票房(億)'] = (movies['票房'] / 1e8).round(2)
movies['平均票價'] = (movies['票房'] / movies['票數']).round(0)   # 一張票平均多少錢

movies.sort_values('票房', ascending=False).head(10)[['片名', '國別', '年', '戲院數', '票數', '票房(億)', '平均票價']]
'''),
        md('''
> 💡 **看懂結果**：平均票價大多在 240～330 元之間——這就是你去電影院買一張票的價錢。前 10 名幾乎都在 **90 家以上的戲院**同時上映，大片的「排片優勢」非常明顯。
'''),
        md('''
## 任務 4：篩選——2025 年的國片表現如何？

**白話說明**：`表格[條件]` 只留下符合條件的列；兩個條件用 `&`（而且）連接，**每個條件都要加括號**。
'''),
        code('''
tw2025 = movies[(movies['國別'] == '中華民國') & (movies['年'] == 2025)]          # 國片 而且 2025 年
print('2025 年國片數量：', len(tw2025), '部')
print('2025 年國片總票房：', round(tw2025['票房'].sum() / 1e8, 1), '億')
tw2025.sort_values('票房', ascending=False).head(5)[['片名', '上映日', '戲院數', '票房(億)']]
'''),
        md('''
> 💡 **看懂結果**：2025 年國片前兩名《陽光女子合唱團》、《96分鐘》都破 2 億，前者更衝到 7.75 億、擠進全年第 2 名，是近年國片最好的成績之一。
>
> 🤖 **換你問 AI**：「我有一個電影票房的 DataFrame，欄位有片名、國別、年、票房。請篩選出 2025 年的國片，依票房由高到低列出前 5 名。」
'''),
        md('''
## 任務 5：索引對齊——2024 年和 2025 年，哪些國家的電影變多了？

**白話說明**：`value_counts()` 數出每個國別有幾部電影，結果是一個以「國別」當名牌的 Series。
兩個 Series 相減時，pandas 會**依照名牌自動對齊**，不是依照順序——只出現在一邊的名牌，結果會是 `NaN`（沒有資料）。
'''),
        code('''
count2024 = movies.loc[movies['年'] == 2024, '國別'].value_counts()
count2025 = movies.loc[movies['年'] == 2025, '國別'].value_counts()

compare = pd.DataFrame({'2024年': count2024, '2025年': count2025})   # 依「國別」自動對齊
compare['變化'] = compare['2025年'] - compare['2024年']
compare.sort_values('2025年', ascending=False).head(12)
'''),
        code('''
no_pair = compare[compare['變化'].isna()]                           # 哪些國家出現 NaN？
print('只在其中一年出現的國別：', len(no_pair), '個')
no_pair.head(8)
'''),
        md('''
> 💡 **看懂結果**：有些國家只在其中一年有電影上映，另一年沒有名牌，所以「變化」算不出來，變成 `NaN`。
> 這不是錯誤，而是 pandas 很誠實地告訴你「**這裡沒有資料**」——下一步要決定：把 NaN 當成 0？還是刪掉？（練習 3 會用到）
>
> 🕵️ **再仔細看國別**：同一個地方有兩種寫法（「台灣」和「中華民國」、「中國」和「中國大陸」），合拍片還寫成「中國大陸/法國」。這種「寫法不統一」是真實資料最常見的問題，第 8 章「資料整理」會教你怎麼統一。
'''),
        latest('''
import pandas as pd, urllib.request, json
raw = urllib.request.urlopen('https://boxofficetw.tfai.org.tw/OpenData/statistic/since2016').read()
latest_movies = pd.DataFrame(json.loads(raw.decode('utf-8-sig'))['List'])
latest_movies.sort_values('ReleaseDate', ascending=False).head()     # 最近上映的電影
'''),
    ] + exercises(
        dict(title='日本電影的平均票價是多少？',
             hint='先用 `movies[\'國別\'] == \'日本\'` 篩選，再取出「平均票價」那一欄，最後 `.mean()`。',
             starter='''
japan = movies[movies[___] == '日本']
japan_price = japan['平均票價'].___()
print('日本片平均票價：', round(japan_price), '元，共', len(japan), '部')
''',
             check='''
check('japan_price', movies.loc[movies['國別'] == '日本', '平均票價'].mean())
''',
             solution='''
japan = movies[movies['國別'] == '日本']
japan_price = japan['平均票價'].mean()
print('日本片平均票價：', round(japan_price), '元，共', len(japan), '部')
'''),
        dict(title='哪一部電影「平均每家戲院」賣最多錢？',
             hint='新增一欄「每家戲院票房」= 票房 ÷ 戲院數；`idxmax()` 回傳最大值的列名牌，再用 `movies.loc[名牌, \'片名\']` 查片名。',
             starter='''
movies['每家戲院票房'] = movies['票房'] / movies[___]
best_idx = movies['每家戲院票房'].___()
best_movie = movies.loc[best_idx, '片名']
print('平均每家戲院最會賺：', best_movie, round(movies.loc[best_idx, '每家戲院票房'] / 1e4), '萬元')
''',
             check='''
check('best_movie', movies.loc[(movies['票房'] / movies['戲院數']).idxmax(), '片名'])
''',
             solution='''
movies['每家戲院票房'] = movies['票房'] / movies['戲院數']
best_idx = movies['每家戲院票房'].idxmax()
best_movie = movies.loc[best_idx, '片名']
print('平均每家戲院最會賺：', best_movie, round(movies.loc[best_idx, '每家戲院票房'] / 1e4), '萬元')
'''),
        dict(title='把 NaN 補成 0，重新計算「變化」，找出 2025 年電影變最多的國家',
             hint='某國在某一年沒有電影，代表「0 部」，所以可以用 `fillna(0)` 補 0。補好之後再算一次「變化」，用 `idxmax()` 找最大。',
             starter='''
compare = compare.___(0)                           # 沒有電影 = 0 部
compare['變化'] = compare['2025年'] - compare['2024年']
most_up = compare['變化'].idxmax()
print('2025 年電影數增加最多的國家：', most_up, '，多了', int(compare.loc[most_up, '變化']), '部')
''',
             check='''
_c = pd.DataFrame({'2024年': movies.loc[movies['年'] == 2024, '國別'].value_counts(),
                   '2025年': movies.loc[movies['年'] == 2025, '國別'].value_counts()}).fillna(0)
check('most_up', (_c['2025年'] - _c['2024年']).idxmax())
''',
             solution='''
compare = compare.fillna(0)
compare['變化'] = compare['2025年'] - compare['2024年']
most_up = compare['變化'].idxmax()
print('2025 年電影數增加最多的國家：', most_up, '，多了', int(compare.loc[most_up, '變化']), '部')
'''),
    )
    return NOTEBOOK, files, cells
