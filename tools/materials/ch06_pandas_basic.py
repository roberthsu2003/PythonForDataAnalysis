"""第 6 章 pandas 基礎功能：loc/iloc/query、排序排名、apply、describe、相關係數。"""
import numpy as np
import pandas as pd

from common import STORES, daily_sales, names, rng
from nbtools import md, code, setup_cell, font_cell, header

CHAPTER = 'pandas的基礎功能'
NOTEBOOK = '範例_茶語時光_店員排行榜與天氣分析.ipynb'


def build(out):
    r = rng(60)
    n = 25
    stores = np.repeat(STORES['門市'].values, 5)
    skill = r.normal(0, 1, n)                                        # 隱藏的「服務能力」
    df = pd.DataFrame({
        '員工編號': [f'E{i:03d}' for i in range(1, n + 1)],
        '姓名': names(n, 6),
        '門市': stores,
        '職位': r.choice(['正職', '兼職'], n, p=[0.45, 0.55]),
    })
    df['出勤天數'] = np.where(df['職位'] == '正職', r.integers(66, 79, n), r.integers(28, 58, n))
    df['銷售杯數'] = (df['出勤天數'] * (95 + 12 * skill + r.normal(0, 8, n))).round().astype(int)
    df['加購率%'] = np.clip(18 + 6 * skill + r.normal(0, 3, n), 3, 45).round(1)
    df['顧客評分'] = np.clip(4.2 + 0.3 * skill + r.normal(0, 0.15, n), 3.0, 5.0).round(2)
    df['客訴數'] = np.clip(np.round(2 - 1.3 * skill + r.normal(0, 0.8, n)), 0, None).astype(int)
    df.to_csv(out / '店員業績_2024Q1.csv', index=False, encoding='utf-8-sig')

    d = daily_sales('2024-01-01', '2024-12-31')
    x = d[d['門市'] == '台北信義店'].copy()
    x['星期'] = x['日期'].dt.dayofweek.map(dict(enumerate('一二三四五六日'))).radd('星期')
    x['日期'] = x['日期'].dt.strftime('%Y-%m-%d')
    x[['日期', '星期', '最高溫', '降雨量', '杯數', '營收']].to_csv(out / '信義店每日天氣與銷量_2024.csv', index=False,
                                                     encoding='utf-8-sig')

    files = ['店員業績_2024Q1.csv', '信義店每日天氣與銷量_2024.csv']
    desc = [('店員業績_2024Q1.csv', '25 位店員第一季的出勤、銷售杯數、加購率、顧客評分、客訴數'),
            ('信義店每日天氣與銷量_2024.csv', '信義店 2024 年每天的氣溫、降雨量、杯數、營收')]

    cells = [
        header(CHAPTER, NOTEBOOK, '🏆 茶語時光：店員排行榜與天氣分析',
               '第一季結束，人資要發績效獎金，請你做一份「店員排行榜」並幫每個人打績效等級；'
               '營運長則想知道：「天氣真的會影響生意嗎？要不要看氣象預報排班？」', desc),
        setup_cell(CHAPTER, files),
        font_cell(),
        md('''
## 任務 1：找人——loc、iloc 與條件篩選

**白話說明**：`loc` 按「名牌」找、`iloc` 按「座位號碼」找；條件篩選就像 Excel 的篩選按鈕；`query` 可以用接近白話的方式寫條件。
'''),
        code('''
import pandas as pd

staff = pd.read_csv('店員業績_2024Q1.csv', index_col='員工編號')   # 員工編號當列名牌
print(staff.head())

print('\\n▶ loc：E005 的姓名與評分\\n', staff.loc['E005', ['姓名', '顧客評分']])
print('\\n▶ iloc：前 3 位、前 3 欄\\n', staff.iloc[:3, :3])
print('\\n▶ 篩選：台中逢甲店的兼職人員\\n', staff[(staff['門市'] == '台中逢甲店') & (staff['職位'] == '兼職')])
print('\\n▶ query：評分 4.5 以上且零客訴\\n', staff.query('顧客評分 >= 4.5 and 客訴數 == 0')[['姓名', '門市', '顧客評分']])
'''),
        md('''
> 🤖 **換你問 AI**：「請從店員業績表中，篩選出評分 4.5 以上、客訴數為 0 的店員，用 query 寫法並說明每個條件。」
'''),
        md('''
## 任務 2：公平的排行榜——先換算「每日杯數」再排名

**老闆的問題**：「誰賣最多杯？」

**白話說明**：正職上班 70 幾天、兼職只有 30～50 天，直接比「總杯數」對兼職不公平。先換算成**平均每天賣幾杯**，再用 `rank` 排名。
'''),
        code('''
staff['每日杯數'] = (staff['銷售杯數'] / staff['出勤天數']).round(1)
staff['總杯數名次'] = staff['銷售杯數'].rank(ascending=False, method='min').astype(int)
staff['每日杯數名次'] = staff['每日杯數'].rank(ascending=False, method='min').astype(int)

board = staff.sort_values('每日杯數名次')[['姓名', '門市', '職位', '出勤天數', '銷售杯數', '總杯數名次', '每日杯數', '每日杯數名次']]
print(board.head(10))
'''),
        md('''
> 💡 **看懂結果**：比較兩種名次——有些兼職人員「總杯數」排名很後面，換成「每日杯數」卻名列前茅。**選錯指標，就會獎勵錯的人。**
'''),
        md('''
## 任務 3：apply——依公司規則自動打績效等級

**人資的規則**：
- **A**：每日杯數 ≥ 100、評分 ≥ 4.3、客訴 ≤ 1
- **C**：評分 < 4.0 或 客訴 ≥ 4
- 其他：**B**

**白話說明**：把規則寫成一個函式，用 `apply(..., axis=1)` 套用到「每一位店員（每一列）」。
'''),
        code('''
def grade(row):                                               # row 是一位店員的所有資料
    if row['每日杯數'] >= 100 and row['顧客評分'] >= 4.3 and row['客訴數'] <= 1:
        return 'A'
    if row['顧客評分'] < 4.0 or row['客訴數'] >= 4:
        return 'C'
    return 'B'

staff['績效等級'] = staff.apply(grade, axis=1)                 # axis=1：對每一列套用
print(staff['績效等級'].value_counts())                       # 各等級人數
print(staff[staff['績效等級'] == 'A'][['姓名', '門市', '每日杯數', '顧客評分', '客訴數']])
'''),
        md('''
> 🤖 **換你問 AI**：「請依照以下規則，用 apply 幫每位店員打 A/B/C 等級：（貼上規則），並統計各等級人數。」
'''),
        md('''
## 任務 4：describe——一眼看完整體狀況，再找出極端值
'''),
        code('''
print(staff[['每日杯數', '加購率%', '顧客評分', '客訴數']].describe().round(2))
print('\\n客訴最多：', staff['客訴數'].idxmax(), staff.loc[staff['客訴數'].idxmax(), '姓名'])
print('加購率最高：', staff['加購率%'].idxmax(), staff.loc[staff['加購率%'].idxmax(), '姓名'])
'''),
        md('''
## 任務 5：天氣真的會影響生意嗎？——相關係數

**白話說明**：相關係數介於 -1～1。越接近 1 → 一起變大；越接近 -1 → 一個變大另一個變小；接近 0 → 沒什麼關係。
'''),
        code('''
weather = pd.read_csv('信義店每日天氣與銷量_2024.csv')
print(weather.head())

print('\\n最高溫 vs 杯數：', round(weather['最高溫'].corr(weather['杯數']), 3))
print('降雨量 vs 杯數：', round(weather['降雨量'].corr(weather['杯數']), 3))

print('\\n店員各指標的相關係數：')
print(staff[['每日杯數', '加購率%', '顧客評分', '客訴數']].corr().round(2))
'''),
        code('''
import matplotlib.pyplot as plt

ax = weather.plot.scatter(x='最高溫', y='杯數', alpha=0.5, figsize=(8, 4), title='信義店：每日最高溫 vs. 杯數')
plt.show()
'''),
        md('''
> 💡 **看懂結果**：
> - 最高溫和杯數是**正相關**——天氣越熱越好賣；降雨量則是**負相關**。營運長可以參考氣象預報調整排班與備料。
> - 店員方面，加購率高的人，顧客評分也比較高、客訴比較少——**很會推薦的店員，通常也是服務好的店員**。
> - ⚠️ 但「相關」不等於「因果」：信義店冬天生意差，除了天冷，也可能是年底商辦區的作息變化。散佈圖中週末的點特別低，就是另一個影響因素（星期幾）。
>
> 🤖 **換你問 AI**：「請計算每日最高溫、降雨量與杯數的相關係數，畫散佈圖，並用白話解釋結果，提醒我相關不等於因果。」

---

## ✍️ 練習題

1. 找出每家門市「每日杯數」最高的店員（提示：先依門市、每日杯數排序，再用 `drop_duplicates('門市')`）。
2. 用 `weather` 計算「星期六、日」與「星期一～五」的平均杯數，信義店是平日好還是假日好？
3. 只看氣溫 30 度以上的日子，最高溫與杯數的相關係數還一樣高嗎？為什麼？
'''),
        md('## 🔑 參考解答（先自己試試看！）'),
        code('''
# 練習 1
best = staff.sort_values(['門市', '每日杯數'], ascending=[True, False]).drop_duplicates('門市')
print(best[['門市', '姓名', '每日杯數']])

# 練習 2
weekend = weather['星期'].isin(['星期六', '星期日'])
print('假日平均：', round(weather.loc[weekend, '杯數'].mean()), '平日平均：', round(weather.loc[~weekend, '杯數'].mean()))

# 練習 3
hot = weather[weather['最高溫'] >= 30]
print('30 度以上：', round(hot['最高溫'].corr(hot['杯數']), 3), '（範圍變窄，星期幾的影響相對變大，相關係數會下降）')
'''),
    ]
    return NOTEBOOK, files, cells
