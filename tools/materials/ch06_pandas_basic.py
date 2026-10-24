"""第 6 章 pandas 基礎功能：用真實電影票房練習 query/loc、排序、排名、apply 分級、describe 與相關係數。"""
from nbtools import md, code, setup_cell, font_cell, header, exercises, copy_real

CHAPTER = 'pandas的基礎功能'
NOTEBOOK = '範例_票房排行榜與爆紅的秘密.ipynb'
SOURCES = ['boxoffice']


def build(out):
    files = [copy_real(out, 'boxoffice')]
    desc = [(files[0], '文化部全國電影票房：2016 年至今 7,000 多部電影的國別、上映日、戲院數、票數與票房金額（JSON）')]

    cells = [
        header(CHAPTER, NOTEBOOK, '🏆 票房排行榜與爆紅的秘密：排序、排名、分級與相關係數',
               '上一章你做出了第一份票房報表。這次電影公司的行銷經理來問你三個問題：'
               '「**每一年的冠軍是誰？**」「**一部電影的票房『通常』有多少——平均數可以相信嗎？**」'
               '「**上映的戲院越多，票房就越高嗎？**」用 pandas 的排序、排名、分級與統計功能，一次回答。',
               desc, SOURCES),
        setup_cell(CHAPTER, files),
        font_cell(),
        md('''
## 任務 1：讀取並整理（複習上一章）

**白話說明**：和上一章一樣：JSON → DataFrame，刪掉沒用的欄位、改中文欄名、去掉票房是 -1 的電影，再新增「年」和「票房(萬)」。
'''),
        code('''
import json
import pandas as pd

with open('全國電影票房_2016至今.json', encoding='utf-8-sig') as f:
    movies = pd.DataFrame(json.load(f)['List'])

movies = (movies.rename(columns={'Country': '國別', 'Name': '片名', 'ReleaseDate': '上映日',
                                 'TheaterCount': '戲院數', 'TotalTickets': '票數', 'TotalAmounts': '票房'})
                [['片名', '國別', '上映日', '戲院數', '票數', '票房']])
movies = movies[movies['票房'] > 0].copy()                            # 去掉 -1（沒有資料）
movies['年'] = movies['上映日'].str[:4].astype(int)
movies['票房(萬)'] = (movies['票房'] / 1e4).round(0)
movies.head()
'''),
        md('''
## 任務 2：用條件找電影——`query` 和 `loc`

**白話說明**：`query('條件')` 用接近口語的方式寫篩選條件；`loc[列條件, 欄位]` 可以同時挑「哪些列」和「哪些欄」。`str.contains('鬼滅')` 找片名裡有「鬼滅」的電影。
'''),
        code('''
display(movies.query('年 == 2025 and 國別 == "韓國"').nlargest(3, '票房'))          # 2025 年最賣座的 3 部韓國片
display(movies.loc[movies['片名'].str.contains('鬼滅'), ['片名', '年', '戲院數', '票房(萬)']])   # 所有「鬼滅」系列
'''),
        md('''
## 任務 3：每一年的冠軍是誰？——排序

**白話說明**：`sort_values` 可以同時依好幾個欄位排序：先依「年」由小到大，同一年再依「票房」由大到小；這時每一年的第一名就排在最前面，`drop_duplicates('年')` 只留每年的第一筆。
'''),
        code('''
champions = (movies[movies['年'] >= 2016]
             .sort_values(['年', '票房'], ascending=[True, False])
             .drop_duplicates('年'))
champions[['年', '片名', '國別', '票房(萬)']]
'''),
        md('''
> 💡 **看懂結果**：11 個年度冠軍裡，美國片拿了 8 次、日本片 2 次（都是鬼滅之刃！）、韓國片 1 次（2016 年的《屍速列車》）。
> 2020 年疫情讓好萊塢大片延期，日本動畫《鬼滅之刃 無限列車篇》趁勢拿下冠軍；2025 年鬼滅再度封王。
'''),
        md('''
## 任務 4：「小兵立大功」——排名看出誰最有粉絲

**白話說明**：`rank(ascending=False)` 算出名次（最大的是第 1 名）。我們幫 2025 年的電影算兩種名次：**票房名次**和**戲院數名次**。如果一部電影只在很少戲院上映，票房名次卻很前面，代表它的觀眾「**很死忠**」。
'''),
        code('''
y2025 = movies[movies['年'] == 2025].copy()
y2025['票房名次'] = y2025['票房'].rank(ascending=False, method='min').astype(int)
y2025['戲院名次'] = y2025['戲院數'].rank(ascending=False, method='min').astype(int)
y2025['名次進步'] = y2025['戲院名次'] - y2025['票房名次']             # 數字越大，越「以小搏大」

y2025.sort_values('名次進步', ascending=False).head(6)[['片名', '國別', '戲院數', '票房(萬)', '戲院名次', '票房名次', '名次進步']]
'''),
        md('''
> 💡 **看懂結果**：以小搏大的冠軍是 **Yorushika 演唱會電影、《BanG Dream! It's MyGO!!!!!》劇場版**這類作品——只在 10 幾家戲院上映，票房名次卻衝進前 150。它們的觀眾是「**為了偶像／動畫一定要去看**」的鐵粉。
> 這就是「**利基市場**」：不用大規模上映，只要找對觀眾。
'''),
        md('''
## 任務 5：替每部電影分級——`apply`

**白話說明**：寫一個函式，輸入票房、回傳等級；`apply` 會把這個函式**套用到每一格**。
'''),
        code('''
def grade(amount):
    if amount >= 5e8:
        return '🔥 現象級（5 億以上）'
    elif amount >= 1e8:
        return '賣座（1～5 億）'
    elif amount >= 1e7:
        return '普通（1,000 萬～1 億）'
    return '小眾（1,000 萬以下）'

movies['等級'] = movies['票房'].apply(grade)
movies['等級'].value_counts()
'''),
        md('''
> 💡 **看懂結果**：7,300 多部電影裡，**破 5 億的只有 14 部**，而將近 87% 的電影票房不到 1,000 萬。電影是一個「**少數贏家拿走大部分**」的產業。
'''),
        md('''
## 任務 6：平均數會騙人！——`describe` 一次看懂分布

**你想知道**：「一部電影的票房『通常』是多少？」
'''),
        code('''
movies['票房(萬)'].describe().round(0)
'''),
        md('''
> 😱 **平均數（mean）是 1,129 萬，中位數（50%）卻只有 50 萬——差了 22 倍！**
>
> 因為少數幾部 5 億、9 億的大片，把平均數往上拉得很高。這時候**中位數**才代表「一般電影」的票房：一半的電影賣不到 50 萬。
> 以後看到「平均薪資」、「平均房價」的新聞，記得多問一句：**中位數是多少？**
'''),
        md('''
## 任務 7：上映戲院越多，票房就越高嗎？——相關係數

**白話說明**：相關係數介於 -1 到 1：越接近 1，代表「一個變大、另一個也跟著變大」越明顯。`corr()` 預設是 Pearson（看直線關係）；`method='spearman'` 看的是「**名次**」的關係，比較不怕極端值。
'''),
        code('''
import matplotlib.pyplot as plt

print('Pearson 相關係數：', round(movies['戲院數'].corr(movies['票房']), 2))
print('Spearman 相關係數（用名次算）：', round(movies['戲院數'].corr(movies['票房'], method='spearman'), 2))

ax = movies.plot.scatter(x='戲院數', y='票房(萬)', alpha=0.25, figsize=(8, 4.5), logy=True,
                         title='上映戲院數 vs. 票房（Y 軸是對數刻度）')
plt.show()
'''),
        md('''
> 💡 **看懂結果**：Spearman 高達 **0.88**——戲院越多，票房「名次」通常越前面，關係非常強；Pearson 只有 0.47，是被少數超級大片的極端值拉低了。
>
> ⚠️ **但是，相關不等於因果！** 是「戲院多 → 票房高」，還是「片商預期會賣 → 才排很多戲院」？資料只能告訴你兩者一起變化，**不能告訴你誰造成誰**。
>
> 🤖 **換你問 AI**：「請計算 DataFrame 中『戲院數』與『票房』的 Pearson 和 Spearman 相關係數，解釋兩者為什麼差很多，並提醒我相關與因果的差別。」
'''),
    ] + exercises(
        dict(title='2024 年最賣座的韓國電影是哪一部？',
             hint='`query(\'年 == 2024 and 國別 == "韓國"\')` 篩出 2024 年的韓國片，再用 `nlargest(1, \'票房\')` 或 `sort_values` 找第一名。',
             starter='''
korea = movies.query('年 == ___ and 國別 == "韓國"')
korea_top = korea.nlargest(1, '票房')['片名'].iloc[0]
print('2024 年最賣座的韓國片：', korea_top)
''',
             check='''
check('korea_top', movies.query('年 == 2024 and 國別 == "韓國"').nlargest(1, '票房')['片名'].iloc[0])
''',
             solution='''
korea = movies.query('年 == 2024 and 國別 == "韓國"')
korea_top = korea.nlargest(1, '票房')['片名'].iloc[0]
print('2024 年最賣座的韓國片：', korea_top)
'''),
        dict(title='2025 年的電影，票房的平均數和中位數各是多少萬？',
             hint='先篩出 2025 年，再對「票房(萬)」用 `.mean()` 和 `.median()`。',
             starter='''
movies_2025 = movies[movies['年'] == ___]
avg_2025 = movies_2025['票房(萬)'].mean()
median_2025 = movies_2025['票房(萬)'].___()
print(f'2025 年：平均 {avg_2025:,.0f} 萬，中位數 {median_2025:,.0f} 萬')
''',
             check='''
check('avg_2025', movies.loc[movies['年'] == 2025, '票房(萬)'].mean())
check('median_2025', movies.loc[movies['年'] == 2025, '票房(萬)'].median())
''',
             solution='''
movies_2025 = movies[movies['年'] == 2025]
avg_2025 = movies_2025['票房(萬)'].mean()
median_2025 = movies_2025['票房(萬)'].median()
print(f'2025 年：平均 {avg_2025:,.0f} 萬，中位數 {median_2025:,.0f} 萬')
'''),
        dict(title='每一年的「國片冠軍」是哪一部？',
             hint='先篩出國片（國別是 `\'中華民國\'`）而且 2016 年以後，接著用任務 3 的招式：依年、票房排序後 `drop_duplicates(\'年\')`。',
             starter='''
tw_champions = (movies[(movies['國別'] == ___) & (movies['年'] >= 2016)]
                .sort_values(['年', '票房'], ascending=[True, ___])
                .drop_duplicates(___))
tw_champions[['年', '片名', '票房(萬)']]
''',
             check='''
check('tw_champions', movies[(movies['國別'] == '中華民國') & (movies['年'] >= 2016)]
                      .sort_values(['年', '票房'], ascending=[True, False]).drop_duplicates('年'))
''',
             solution='''
tw_champions = (movies[(movies['國別'] == '中華民國') & (movies['年'] >= 2016)]
                .sort_values(['年', '票房'], ascending=[True, False])
                .drop_duplicates('年'))
tw_champions[['年', '片名', '票房(萬)']]
'''),
    )
    return NOTEBOOK, files, cells
