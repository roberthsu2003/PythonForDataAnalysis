"""第 4 章 NumPy：每日杯數矩陣的整批運算、axis、布林篩選、cumsum、reshape。"""
from common import STORES, daily_sales
from nbtools import md, code, setup_cell, font_cell, header

CHAPTER = 'Numpy建立與計算'
NOTEBOOK = '範例_茶語時光_一年366天的杯數矩陣.ipynb'


def build(out):
    daily = daily_sales('2024-01-01', '2024-12-31')
    cups = daily.pivot(index='日期', columns='門市', values='杯數')[STORES['門市']]
    cups.index = cups.index.strftime('%Y-%m-%d')
    cups.to_csv(out / '每日杯數_2024.csv', encoding='utf-8')

    files = ['每日杯數_2024.csv']
    desc = [('每日杯數_2024.csv', '2024 年 366 天 × 5 家門市的每日杯數')]

    cells = [
        header(CHAPTER, NOTEBOOK, '🧮 茶語時光：一年 366 天的杯數矩陣',
               '總部拿到一張大表：2024 年每一天、每一家門市賣了幾杯。這是 366 列 × 5 欄、共 1,830 個數字。'
               '用 Excel 一格一格拉公式太累，你決定把它裝進 NumPy 陣列，一次算完老闆想知道的所有數字。', desc),
        setup_cell(CHAPTER, files),
        md('''
## 任務 1：把表格裝進「蛋盒」——載入成 NumPy 陣列

**白話說明**：`np.loadtxt` 讀取 CSV 的數字部分；日期和門市名稱另外存起來，等一下用來對照「第幾列是哪一天」。
'''),
        code('''
import numpy as np

with open('每日杯數_2024.csv', encoding='utf-8') as f:
    stores = f.readline().strip().split(',')[1:]          # 第一行是標題：取出 5 家門市名稱

dates = np.loadtxt('每日杯數_2024.csv', delimiter=',', skiprows=1, usecols=0, dtype=str)       # 第 0 欄：日期（文字）
cups = np.loadtxt('每日杯數_2024.csv', delimiter=',', skiprows=1, usecols=range(1, 6), dtype=int)  # 第 1～5 欄：杯數

print('門市：', stores)
print('形狀 shape：', cups.shape)                          # (366, 5)：366 天 × 5 家店
print('前 3 天：\\n', cups[:3])
'''),
        md('''
## 任務 2：整批運算——一行算出所有門市的營收

**老闆的問題**：「平均一杯賣 58 元，每天每家店大概營收多少？如果全面漲價 5 元呢？」

**白話說明**：陣列可以「整盒一起算」，1,830 個數字一次乘完，不需要迴圈。
'''),
        code('''
revenue = cups * 58                                       # 每一格都乘以 58：整張營收表一次算完
revenue_up = cups * (58 + 5)                              # 假設全面漲價 5 元
print('全年營收（萬元）：', round(revenue.sum() / 10000))
print('漲價 5 元後多賺（萬元）：', round((revenue_up - revenue).sum() / 10000), '（假設杯數不變）')
'''),
        md('''
> 💡 **看懂結果**：漲 5 元，一年多出上百萬元——但這是「假設杯數不變」。真實世界漲價可能流失客人，這正是分析師要提醒老闆的地方。
'''),
        md('''
## 任務 3：用 axis 回答兩種問題——「每家店」與「每一天」

**白話說明**：`axis=0` 直著算 → 每一欄（每家店）一個答案；`axis=1` 橫著算 → 每一列（每一天）一個答案。
'''),
        code('''
store_total = cups.sum(axis=0)                            # 直著加：每家店全年總杯數（5 個數字）
for name, total, avg, sd in zip(stores, store_total, cups.mean(axis=0), cups.std(axis=0)):
    print(f'{name}：全年 {total:,} 杯，日平均 {avg:.0f} 杯，標準差 {sd:.0f}')

day_total = cups.sum(axis=1)                              # 橫著加：每天 5 家店合計（366 個數字）
best, worst = day_total.argmax(), day_total.argmin()      # argmax / argmin：最大、最小值「在第幾個位置」
print('\\n全品牌最好的一天：', dates[best], day_total[best], '杯')
print('全品牌最差的一天：', dates[worst], day_total[worst], '杯')
'''),
        md('''
> 💡 **看懂結果**：最差的那天正是 **2024-10-31 康芮颱風**全台停班停課；最好的一天 6/15 則是週六加上高雄巨蛋演唱會。標準差越大的門市，代表生意起伏越大（例如假日爆量的西門店），排班與備料更需要彈性。
>
> 🤖 **換你問 AI**：「我有一個 366×5 的 NumPy 陣列（列是日期、欄是門市），請算出每家門市的總和、平均、標準差，並找出合計最高與最低的日期。」
'''),
        md('''
## 任務 4：布林篩選——哪幾天生意太差，需要促銷？

**老闆的問題**：「每家店一年有幾天低於 250 杯？最慘的是哪些日子？」
'''),
        code('''
low = cups < 250                                          # 每一格判斷是否 < 250，得到 True / False 的陣列
print('各店低於 250 杯的天數：', dict(zip(stores, low.sum(axis=0).tolist())))   # True 當成 1 加總 = 天數

xinyi = cups[:, stores.index('台北信義店')]                # 取出信義店那一欄
label = np.where(xinyi < 250, '需促銷', '正常')            # 像 Excel 的 IF：符合條件標「需促銷」
print('信義店需促銷的日期（前 10 天）：', dates[label == '需促銷'][:10])
'''),
        md('''
> 💡 **看懂結果**：信義店低於 250 杯的日子幾乎都是**週末與冬天**——商辦區週末沒人上班。與其全面促銷，不如規劃「週末限定」活動。
'''),
        md('''
## 任務 5：cumsum 累計——哪一天突破 50 萬杯？

**老闆的問題**：「我們說今年要賣破 50 萬杯，是哪一天達成的？」
'''),
        code('''
running = day_total.cumsum()                              # 累計加總：每一天 = 從 1/1 到這天的總杯數
hit = np.argmax(running >= 500_000)                       # 第一個「累計 ≥ 50 萬」的位置
print('突破 50 萬杯的日期：', dates[hit], '，當天累計', f'{running[hit]:,}', '杯')
print('全年總杯數：', f'{running[-1]:,}')
'''),
        md('''
## 任務 6：reshape——每家店「星期幾」最好賣？

**白話說明**：2024-01-01 剛好是星期一。取前 364 天（剛好 52 週），把一長條 reshape 成「52 週 × 7 天」的表格，再直著平均，就得到星期一到星期日的平均杯數。
'''),
        code('''
weekday = ['一', '二', '三', '四', '五', '六', '日']
for i, name in enumerate(stores):
    weeks = cups[:364, i].reshape(52, 7)                  # 364 天 → 52 列（週）× 7 欄（星期一～日）
    avg = weeks.mean(axis=0)                              # 直著平均：每個星期幾一個數字
    print(f'{name}：最好賣是星期{weekday[avg.argmax()]}（{avg.max():.0f} 杯），最差是星期{weekday[avg.argmin()]}（{avg.min():.0f} 杯）')
'''),
        md('''
> 💡 **看懂結果**：信義店（商辦區）平日最好、週日最差；西門店（觀光區）剛好相反。**同一個品牌，不同門市的排班策略應該完全不同。**
>
> 🤖 **換你問 AI**：「請把一家門市 364 天的杯數 reshape 成 52×7，計算星期一到星期日的平均，並畫成長條圖。」

---

## ✍️ 練習題

1. 算出「台南成大店」全年的中位數與平均數，兩者差多少？
2. 找出「高雄巨蛋店」杯數最高的 3 天（提示：`np.argsort`），對照日期看看是不是演唱會。
3. 用 `np.where` 把 5 家店每天的杯數標記成「爆量」（≥ 700）或「一般」，數一數每家店有幾天爆量。
'''),
        md('## 🔑 參考解答（先自己試試看！）'),
        code('''
# 練習 1
tainan = cups[:, stores.index('台南成大店')]
print('台南成大店 中位數：', np.median(tainan), '平均：', round(tainan.mean(), 1))

# 練習 2
kh = cups[:, stores.index('高雄巨蛋店')]
top3 = np.argsort(kh)[-3:][::-1]                          # 由小到大排序後取最後 3 個，再反轉成由大到小
for i in top3:
    print(dates[i], kh[i], '杯')

# 練習 3
busy = np.where(cups >= 700, '爆量', '一般')
print(dict(zip(stores, (busy == '爆量').sum(axis=0).tolist())))
'''),
    ]
    return NOTEBOOK, files, cells
