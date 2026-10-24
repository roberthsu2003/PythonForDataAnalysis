"""第 8 章 資料整理：一份真實世界會長這樣的「髒」會員問卷。"""
import numpy as np
import pandas as pd

from common import STORES, names, rng, sweet_probs
from nbtools import md, code, setup_cell, header, exercises

CHAPTER = '資料整理和使用前準備'
NOTEBOOK = '範例_茶語時光_髒亂的會員問卷大掃除.ipynb'

STORE_VARIANTS = {
    '台北信義店': ['台北信義店', '信義店', '台北信義店 ', '信義', '臺北信義店'],
    '台北西門店': ['台北西門店', '西門店', '西門町店', ' 台北西門店', '臺北西門店'],
    '台中逢甲店': ['台中逢甲店', '逢甲店', '逢甲', '臺中逢甲店'],
    '台南成大店': ['台南成大店', '成大店', '臺南成大店', '台南成大'],
    '高雄巨蛋店': ['高雄巨蛋店', '巨蛋店', '高雄巨蛋'],
}
SWEET_VARIANTS = {'正常糖': ['正常糖', '全糖', '10分', '正常'], '少糖': ['少糖', '7分', '七分糖'],
                  '半糖': ['半糖', '5分', '50%', '五分糖'], '微糖': ['微糖', '3分', '三分糖'], '無糖': ['無糖', '0分', '去糖']}
DRINK_VARIANTS = {'珍珠奶茶': ['珍珠奶茶', '珍奶', '珍珠奶茶 ', '波霸奶茶'], '四季春青茶': ['四季春青茶', '四季春'],
                  '鮮奶綠': ['鮮奶綠', '鮮奶綠茶'], '冬瓜檸檬': ['冬瓜檸檬'], '多多綠': ['多多綠', '養樂多綠'],
                  '黑糖珍珠鮮奶': ['黑糖珍珠鮮奶', '黑糖鮮奶', '黑糖珠珠鮮奶'], '芋頭鮮奶': ['芋頭鮮奶', '芋泥鮮奶']}
CN_NUM = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7}


def build(out):
    r = rng(80)
    n = 300
    stores = r.choice(STORES['門市'], n, p=[0.22, 0.2, 0.22, 0.18, 0.18])
    code_of = dict(zip(STORES['門市'], STORES['門市代碼']))
    rows = []
    for i in range(n):
        store = stores[i]
        sweet = r.choice(list(SWEET_VARIANTS), p=sweet_probs(code_of[store]))
        gender = r.choice(['女', '男'], p=[0.6, 0.4])
        age = int(np.clip(r.normal(26 if store == '台南成大店' else 31, 7), 16, 65))
        drink = r.choice(list(DRINK_VARIANTS), p=[0.3, 0.1, 0.1, 0.1, 0.1, 0.15, 0.15])
        per_week = int(np.clip(round(r.gamma(2, 1.2)), 1, 7))
        sat = int(np.clip(round(r.normal({'台北信義店': 4.3, '台北西門店': 3.6, '台中逢甲店': 4.0,
                                         '台南成大店': 4.4, '高雄巨蛋店': 3.8}[store], 0.7)), 1, 5))
        mid = f'M{int(r.integers(1, 9000)):05d}'
        ts = pd.Timestamp('2024-05-01') + pd.Timedelta(minutes=int(r.integers(0, 14 * 24 * 60)))
        rows.append(dict(填答時間=ts, 會員編號=mid, 姓名=None, 性別=gender, 年齡=str(age), Email=f'user{i + 1:03d}@example.com',
                         常去門市=store, 最愛飲品=drink, 甜度=sweet, 每週購買次數=str(per_week), 滿意度=str(sat), 建議=''))
    df = pd.DataFrame(rows)
    df['姓名'] = names(n, 8)

    def mess(col, func, frac):
        idx = r.choice(df.index, int(n * frac), replace=False)
        df.loc[idx, col] = [func(v) for v in df.loc[idx, col]]

    mess('性別', lambda v: r.choice({'女': ['F', 'female', '女生', ' 女'], '男': ['M', 'male', '男生', '男 ']}[v]), 0.25)
    mess('性別', lambda v: '', 0.04)
    mess('年齡', lambda v: r.choice([f'{v}歲', f'{v} ', '二十', '999', '-1', '']), 0.12)
    mess('Email', lambda v: r.choice([v.upper(), f' {v} ', v.replace('@', '＠'), '', 'none']), 0.15)
    mess('常去門市', lambda v: r.choice(STORE_VARIANTS[v][1:]), 0.4)
    mess('最愛飲品', lambda v: r.choice(DRINK_VARIANTS[v]), 0.5)
    mess('甜度', lambda v: r.choice(SWEET_VARIANTS[v]), 0.45)
    mess('每週購買次數', lambda v: r.choice([f'{v}次', '每天', f'{["一", "二", "三", "四", "五", "六", "七"][int(v) - 1]}次', '']), 0.2)
    mess('滿意度', lambda v: r.choice(['0', '99', '']), 0.05)
    tips = ['半糖還是太甜', '希望多一點座位', '珍珠可以再Q一點', '外送太慢', '店員很親切', '希望推出無糖新品', '價格有點貴']
    mess('建議', lambda v: r.choice(tips), 0.35)

    dup_exact = df.sample(12, random_state=1)                              # 重複送出：完全相同的列
    dup_update = df.sample(6, random_state=2).copy()                       # 同一會員改答案再送一次（時間較晚）
    dup_update['填答時間'] = dup_update['填答時間'] + pd.Timedelta(hours=3)
    dup_update['滿意度'] = '5'
    df = pd.concat([df, dup_exact, dup_update]).sample(frac=1, random_state=3).reset_index(drop=True)
    df['填答時間'] = df['填答時間'].dt.strftime('%Y/%m/%d %H:%M')
    df.to_csv(out / '會員問卷_原始.csv', index=False, encoding='utf-8-sig')

    files = ['會員問卷_原始.csv']
    desc = [('會員問卷_原始.csv', '從 Google 表單匯出的 318 份會員問卷，未經任何整理（裡面有很多陷阱！）')]

    cells = [
        header(CHAPTER, NOTEBOOK, '🧹 茶語時光：髒亂的會員問卷大掃除',
               '行銷部用 Google 表單做了會員滿意度問卷，想知道「哪家店滿意度最高？」、「各地區客人喜歡幾分糖？」。'
               '但表單是開放填寫的：有人重複送出、性別寫 F 或 male、年齡寫「二十」或 999、門市寫「信義」或「西門町店」、'
               '甜度有「全糖」、「10分」、「正常」三種寫法……直接分析一定會錯。你的任務是**先把資料洗乾淨，再回答問題**。', desc),
        setup_cell(CHAPTER, files),
        md('''
## 任務 1：健康檢查——先看看資料有多髒

**白話說明**：分析前先做「健康檢查」：多少筆、每欄的型態、缺值、重複，以及類別欄位到底有幾種寫法。
'''),
        code('''
import pandas as pd

raw = pd.read_csv('會員問卷_原始.csv', dtype=str, keep_default_na=False)   # 先全部當文字讀，避免 pandas 自作主張轉型
print('筆數與欄數：', raw.shape)
print('完全重複的列：', raw.duplicated().sum())
print('重複的會員編號：', raw['會員編號'].duplicated().sum())
print('\\n性別有幾種寫法：', raw['性別'].unique())
print('\\n甜度有幾種寫法：', raw['甜度'].nunique(), '→', raw['甜度'].unique())
print('\\n門市有幾種寫法：', raw['常去門市'].nunique())
print('\\n年齡的怪值：', [v for v in raw['年齡'].unique() if not v.isdigit()][:10])
'''),
        md('''
> 💡 **看懂結果**：只有 5 家門市，卻有二十幾種寫法；甜度只有 5 種，卻寫出十幾種。**如果直接用 groupby 統計，「信義店」和「台北信義店」會被當成兩家店！**
>
> 🤖 **換你問 AI**：「請幫我對這份問卷做資料健康檢查：列出每欄的缺值數、重複列數，以及每個類別欄位的所有不同寫法。」
'''),
        md('''
## 任務 2：去除重複——同一個人只算一次

**兩種重複**：① 按了兩次送出（整列一模一樣）；② 同一位會員後來改了答案又送一次——這種要**保留最新的一筆**。
'''),
        code('''
df = raw.drop_duplicates().copy()                                      # ① 刪除完全相同的列
print('刪除完全重複後：', len(raw), '→', len(df))

df['填答時間'] = pd.to_datetime(df['填答時間'], format='%Y/%m/%d %H:%M')
df = df.sort_values('填答時間').drop_duplicates('會員編號', keep='last')   # ② 依時間排序，同一會員只留最後一筆
print('同一會員只留最新一筆後：', len(df))
'''),
        md('''
## 任務 3：統一類別——一家店只能有一種寫法

**白話說明**：先 `str.strip()` 去掉前後空白，再用「對照表」（字典）把各種寫法換成標準名稱。
'''),
        code('''
gender_map = {'女': '女', 'F': '女', 'female': '女', '女生': '女', '男': '男', 'M': '男', 'male': '男', '男生': '男'}
df['性別'] = df['性別'].str.strip().map(gender_map)                     # 對照表裡沒有的（空白）會變成 NaN

store_map = {'信義店': '台北信義店', '信義': '台北信義店', '臺北信義店': '台北信義店',
             '西門店': '台北西門店', '西門町店': '台北西門店', '臺北西門店': '台北西門店',
             '逢甲店': '台中逢甲店', '逢甲': '台中逢甲店', '臺中逢甲店': '台中逢甲店',
             '成大店': '台南成大店', '臺南成大店': '台南成大店', '台南成大': '台南成大店',
             '巨蛋店': '高雄巨蛋店', '高雄巨蛋': '高雄巨蛋店'}
df['常去門市'] = df['常去門市'].str.strip().replace(store_map)          # replace：不在對照表的值保持原樣

sweet_map = {'全糖': '正常糖', '10分': '正常糖', '正常': '正常糖', '7分': '少糖', '七分糖': '少糖',
             '5分': '半糖', '50%': '半糖', '五分糖': '半糖', '3分': '微糖', '三分糖': '微糖', '0分': '無糖', '去糖': '無糖'}
df['甜度'] = df['甜度'].str.strip().replace(sweet_map)

drink_map = {'珍奶': '珍珠奶茶', '波霸奶茶': '珍珠奶茶', '四季春': '四季春青茶', '鮮奶綠茶': '鮮奶綠', '養樂多綠': '多多綠',
             '黑糖鮮奶': '黑糖珍珠鮮奶', '黑糖珠珠鮮奶': '黑糖珍珠鮮奶', '芋泥鮮奶': '芋頭鮮奶'}
df['最愛飲品'] = df['最愛飲品'].str.strip().replace(drink_map)

for col in ['性別', '常去門市', '甜度', '最愛飲品']:
    print(col, '→', sorted(df[col].dropna().unique()))
'''),
        md('''
> 🤖 **換你問 AI**：「門市欄位有這些寫法（貼上 unique() 結果），請幫我建立一個對照表字典，統一成 5 家標準門市名稱。」
'''),
        md('''
## 任務 4：救回數字欄位——年齡、購買次數、滿意度

**白話說明**：
- 年齡：從「25歲」中抽出數字；「二十」、「999」、「-1」這種**不合理的值改成缺值（NaN）**，而不是亂猜。
- 購買次數：「三次」→ 3、「每天」→ 7。
- 滿意度：只接受 1～5，其他（0、99）視為無效。
'''),
        code('''
age = pd.to_numeric(df['年齡'].str.extract(r'(\\d+)')[0], errors='coerce')   # 抽出數字；抽不到的變 NaN
df['年齡'] = age.where(age.between(12, 90))                                   # 不在 12～90 歲之間的視為無效

cn = {'一': '1', '二': '2', '三': '3', '四': '4', '五': '5', '六': '6', '七': '7'}
times = df['每週購買次數'].str.replace('次', '').replace({'每天': '7', **cn})
df['每週購買次數'] = pd.to_numeric(times, errors='coerce')

sat = pd.to_numeric(df['滿意度'], errors='coerce')
df['滿意度'] = sat.where(sat.between(1, 5))

display(df[['年齡', '每週購買次數', '滿意度']].describe().round(2))
print('\\n各欄缺值數：\\n', df[['性別', '年齡', '每週購買次數', '滿意度']].isnull().sum())
'''),
        md('''
## 任務 5：整理 Email——大小寫、空白、全形符號
'''),
        code('''
email = (df['Email'].str.strip()                     # 去前後空白
                    .str.lower()                      # 全部轉小寫
                    .str.replace('＠', '@'))          # 全形＠ → 半形 @
df['Email'] = email.where(email.str.contains(r'^[\\w.]+@[\\w.]+\\.\\w+$'))   # 格式不對的（空白、none）變 NaN
print('有效 Email：', df['Email'].notnull().sum(), '／', len(df))
'''),
        md('''
## 任務 6：洗乾淨了！終於可以回答行銷部的問題
'''),
        code('''
print('▶ 各門市平均滿意度：')
display(df.groupby('常去門市')['滿意度'].agg(['count', 'mean']).round(2).sort_values('mean', ascending=False))

print('\\n▶ 各門市甜度偏好（%）：')
sweet_order = ['正常糖', '少糖', '半糖', '微糖', '無糖']
display((pd.crosstab(df['常去門市'], df['甜度'], normalize='index')[sweet_order] * 100).round(0))

df.to_csv('會員問卷_清理後.csv', index=False, encoding='utf-8-sig')
print('\\n✅ 已存成 會員問卷_清理後.csv，共', len(df), '筆')
'''),
        md('''
> 💡 **看懂結果**：
> - 台南成大店選「正常糖」的比例明顯最高，台北信義店（上班族）選正常糖的比例最低，微糖加無糖超過四成——**「台南人愛甜」在我們的資料裡是真的**。健康系列新品可以先在信義店試賣。
> - 回頭想想：如果沒有統一甜度寫法，「全糖」、「10分」、「正常」會被拆成三組，台南的正常糖比例會被嚴重低估。**洗資料不是雜事，它直接決定結論對不對。**
>
> 🤖 **換你問 AI**：「請把整理後的問卷依門市計算平均滿意度，並做出門市 × 甜度的百分比交叉表，用白話說明各地區的甜度偏好差異。」
''')
    ] + exercises(
        dict(title='年齡缺值不要隨便補：用「各門市年齡的中位數」補上',
             hint='`groupby(\'常去門市\')[\'年齡\'].transform(\'median\')` 會回傳和原表一樣長的欄位，每一列都是「自己門市」的中位數，剛好拿來 `fillna`。',
             starter='''
store_median = df.groupby(___)['年齡'].transform('median')
df['年齡'] = df['年齡'].fillna(___)
print('補值後年齡缺值：', df['年齡'].isnull().sum())
''',
             check='''
check('store_median', df.groupby('常去門市')['年齡'].transform('median'))
''',
             solution='''
store_median = df.groupby('常去門市')['年齡'].transform('median')
df['年齡'] = df['年齡'].fillna(store_median)
print('補值後年齡缺值：', df['年齡'].isnull().sum())
'''),
        dict(title='顧客建議裡，有幾則提到「甜」？幾則提到「外送」？',
             hint='`df[\'建議\'].str.contains(\'甜\')` 會得到 True/False，`.sum()` 就是 True 的數量。',
             starter='''
sweet_n = df['建議'].str.___('甜').sum()
delivery_n = df['建議'].str.contains(___).sum()
print('提到甜：', sweet_n, '則；提到外送：', delivery_n, '則')
''',
             check='''
check('sweet_n', df['建議'].str.contains('甜').sum())
check('delivery_n', df['建議'].str.contains('外送').sum())
''',
             solution='''
sweet_n = df['建議'].str.contains('甜').sum()
delivery_n = df['建議'].str.contains('外送').sum()
print('提到甜：', sweet_n, '則；提到外送：', delivery_n, '則')
'''),
        dict(title='清理前後，「台南成大店」的筆數差多少？為什麼？',
             hint='`(表格[\'欄位\'] == 值).sum()` 可以數出符合的筆數。清理後多了「被統一回來的各種寫法」，少了「重複填答」。',
             starter='''
before = (raw['常去門市'] == ___).sum()             # 清理前，剛好寫成「台南成大店」的筆數
after = (df[___] == '台南成大店').sum()              # 清理後
print('清理前：', before, '清理後：', after)
''',
             check='''
check('before', (raw['常去門市'] == '台南成大店').sum())
check('after', (df['常去門市'] == '台南成大店').sum())
''',
             solution='''
before = (raw['常去門市'] == '台南成大店').sum()
after = (df['常去門市'] == '台南成大店').sum()
print('清理前：', before, '清理後：', after)
# 各種寫法（台南店、成大店……）被統一回來，筆數變多；但重複填答被刪掉，又會少一些
'''),
    )
    return NOTEBOOK, files, cells
