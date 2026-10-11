"""產生「AI 協作資料分析｜十二個範例」的固定偽資料與資料卡。

執行方式（在 repo 根目錄）：
    uv run --with openpyxl python tools/ai_data12/build_data.py

每例使用固定亂數種子，重跑會得到相同內容；資料卡會記錄筆數、種子與 SHA-256。
"""
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2] / 'AI協作資料分析_12個範例'

SURNAMES = list('陳林黃張李王吳劉蔡楊許鄭謝郭洪曾邱廖賴周徐蘇葉莊呂江何蕭羅高潘簡朱鍾彭游詹胡施沈余趙盧梁顏柯翁魏孫戴')
GIVEN = list('志明怡君家豪雅婷俊傑淑芬建宏佳玲宗翰美惠冠廷詩涵承恩品妤柏翰子晴宇軒欣妤彥廷思妤育誠郁婷')


def names(rng, n):
    """產生 n 個不重複的假名。"""
    out, seen = [], set()
    while len(out) < n:
        name = rng.choice(SURNAMES) + ''.join(rng.choice(GIVEN, 2))
        if name not in seen:
            seen.add(name)
            out.append(name)
    return out


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_csv(df, path, encoding='utf-8-sig'):
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding=encoding)
    return path


def freeze_xlsx(path):
    """把 xlsx 內的建立／修改時間與 zip 時間戳固定，讓重跑得到相同檔案。"""
    import re
    import zipfile
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, data in items:
            if name == 'docProps/core.xml':
                data = re.sub(rb'(<dcterms:(created|modified)[^>]*>)[^<]*', rb'\g<1>2025-01-01T00:00:00Z', data)
            z.writestr(zipfile.ZipInfo(name, date_time=(2025, 1, 1, 0, 0, 0)), data, zipfile.ZIP_DEFLATED)


def data_card(folder, title, seed, files, fields, rules, traps):
    """files: [(Path, 筆數說明)]；fields: {檔名: [(欄位, 型態與意義)]}"""
    lines = [f'# {title}：偽資料卡', '',
             '這是教材原創的完全合成資料，沒有真實人物、店家或交易記錄。'
             '除非另外註明，CSV 以 UTF-8 BOM 編碼提供（Excel 可直接開啟），空欄表示缺失值。', '',
             f'固定亂數種子：`{seed}`', '',
             '| 檔案 | 內容 | SHA-256 |', '| :--- | :--- | :--- |']
    for p, desc in files:
        lines.append(f'| [{p.name}](./{p.name}) | {desc} | `{sha256(p)[:16]}…` |')
    lines += ['', '完整 SHA-256：', '']
    for p, _ in files:
        lines.append(f'- `{p.name}`：`{sha256(p)}`')
    lines += ['', '## 欄位字典', '']
    for fname, cols in fields.items():
        lines += [f'### {fname}', '', '| 欄位 | 型態／單位與意義 |', '| :--- | :--- |']
        lines += [f'| `{c}` | {d} |' for c, d in cols]
        lines.append('')
    lines += ['## 生成規則', '', rules, '', '## 刻意安排的資料狀況', '']
    lines += [f'- {t}' for t in traps]
    lines += ['', '## 使用方式', '',
              '讀取這份固定資料，不因分析結果不漂亮而請 AI 重新產生或修改原始檔；'
              '清理後的結果另存新檔。所有數字必須由 AI 實際執行程式算出，本資料卡不提供預設答案。'
              '生成規則是教師設計的假想情境，不代表真實世界的因果關係。', '']
    (folder / 'data' / 'DATA_CARD.md').write_text('\n'.join(lines), encoding='utf-8')


# ---------------------------------------------------------------- 01 班級成績
def ex01():
    seed = 101
    rng = np.random.default_rng(seed)
    n = 45
    df = pd.DataFrame({'座號': range(1, n + 1), '姓名': names(rng, n)})
    ability = rng.normal(0, 1, n)                       # 學生整體程度，讓各科有正相關
    spec = {'國文': (74, 9), '英文': (70, 13), '數學': (66, 17), '自然': (68, 14), '社會': (72, 10)}
    for subj, (mu, sd) in spec.items():
        score = mu + sd * (0.6 * ability + 0.8 * rng.normal(0, 1, n))
        df[subj] = pd.array(np.clip(np.round(score), 0, 100).astype(int), dtype='Int64')
    df.loc[[11, 30], '數學'] = pd.NA                     # 兩位缺考
    df.loc[30, '英文'] = pd.NA
    folder = ROOT / '01_class_scores'
    p = save_csv(df, folder / 'data' / 'scores.csv')
    data_card(folder, '01 班級段考成績', seed, [(p, f'{n} 位學生、5 科成績')],
              {'scores.csv': [('座號', '整數，1～45'), ('姓名', '假名'),
                              ('國文／英文／數學／自然／社會', '整數分數，0～100；空白代表缺考')]},
              '每位學生有一個「整體程度」潛在值，各科分數＝科目平均＋標準差×（0.6×程度＋0.8×個別雜訊），'
              '四捨五入後限制在 0～100。數學的標準差最大，國文最小。',
              ['座號 12、31 的數學缺考，座號 31 的英文也缺考，練習 `np.nanmean` 與缺值處理。',
               '各科分數彼此正相關，可觀察「某科高分的人其他科是否也高」。'])


# ---------------------------------------------------------------- 02 便利商店一週銷售
def ex02():
    seed = 202
    rng = np.random.default_rng(seed)
    products = [
        ('御飯糰-鮪魚', '鮮食', 35), ('御飯糰-肉鬆', '鮮食', 35), ('大亨堡', '鮮食', 45), ('茶葉蛋', '鮮食', 13),
        ('三明治-火腿', '鮮食', 39), ('涼麵', '鮮食', 55), ('便當-雞腿', '鮮食', 89), ('關東煮-白蘿蔔', '鮮食', 15),
        ('美式咖啡', '飲品', 45), ('拿鐵咖啡', '飲品', 60), ('無糖綠茶', '飲品', 25), ('鮮奶', '飲品', 42),
        ('運動飲料', '飲品', 28), ('可樂', '飲品', 30), ('礦泉水', '飲品', 20), ('豆漿', '飲品', 25),
        ('洋芋片', '零食', 35), ('巧克力', '零食', 45), ('口香糖', '零食', 30), ('餅乾', '零食', 39),
        ('衛生紙', '日用品', 69), ('牙刷', '日用品', 49), ('雨傘', '日用品', 199), ('電池', '日用品', 89),
        ('冰淇淋', '冰品', 55),
    ]
    dates = pd.date_range('2025-03-03', periods=7)        # 週一到週日
    base = rng.uniform(5, 60, len(products))
    rows = []
    for d in dates:
        weekend = d.dayofweek >= 5
        rainy = d.day == 6                                 # 週四下雨
        for (name, cat, price), b in zip(products, base):
            lam = b * (1.3 if weekend and cat in ('零食', '冰品') else 1.0) * (0.75 if weekend and name in ('美式咖啡', '拿鐵咖啡', '三明治-火腿') else 1.0)
            if name == '雨傘':
                lam = 25 if rainy else 1.5
            if name == '冰淇淋' and rainy:
                lam *= 0.4
            rows.append((d.date().isoformat(), name, cat, price, int(rng.poisson(lam))))
    df = pd.DataFrame(rows, columns=['日期', '品項', '類別', '單價', '數量'])
    folder = ROOT / '02_store_sales'
    p = save_csv(df, folder / 'data' / 'store_sales.csv')
    data_card(folder, '02 便利商店一週銷售', seed, [(p, f'7 天 × {len(products)} 個品項＝{len(df)} 筆')],
              {'store_sales.csv': [('日期', '文字，YYYY-MM-DD，2025-03-03（週一）～03-09（週日）'), ('品項', '商品名稱'),
                                   ('類別', '鮮食／飲品／零食／日用品／冰品'), ('單價', '整數／台幣'), ('數量', '整數／件，當日售出數量')]},
              '每個品項有固定的平均銷量，每日數量用卜瓦松分布抽樣。週末零食與冰品銷量 ×1.3，咖啡與三明治 ×0.75；'
              '2025-03-06（週四）設定為雨天：雨傘平均 25 支（平日約 1.5 支），冰淇淋 ×0.4。',
              ['沒有「營業額」欄位，要自己用 單價 × 數量 算出來。',
               '雨天那一天雨傘銷量特別高，可以練習用篩選找出「異常的一天」。'])


# ---------------------------------------------------------------- 03 圖書館多格式檔案
def ex03():
    seed = 303
    rng = np.random.default_rng(seed)
    cats = pd.DataFrame([('000', '總類'), ('100', '哲學類'), ('300', '自然科學類'), ('400', '應用科學類'),
                         ('500', '社會科學類'), ('700', '史地類'), ('800', '語文類'), ('900', '藝術類')],
                        columns=['分類號', '分類名稱'])
    words = list('星河山海風雲光影夢想時間城市旅人森林季節咖啡設計數學程式資料故事歷史哲學藝術音樂')
    n_books = 120
    titles = set()
    while len(titles) < n_books:
        titles.add(''.join(rng.choice(words, rng.integers(2, 4))) + rng.choice(['之書', '筆記', '入門', '的祕密', '簡史', '指南', '']))
    books = pd.DataFrame({
        '書號': [f'B{i:04d}' for i in range(1, n_books + 1)],
        '書名': sorted(titles),
        '作者': names(rng, n_books),
        '分類號': rng.choice(cats['分類號'], n_books, p=[.05, .08, .15, .2, .17, .1, .17, .08]),
        '出版年': rng.integers(1995, 2025, n_books),
    })
    n_mem = 80
    members = [{'會員編號': f'M{i:03d}', '姓名': nm,
                '身分': str(rng.choice(['學生', '教職員', '校友'], p=[.65, .2, .15])),
                '加入日期': (pd.Timestamp('2022-01-01') + pd.Timedelta(days=int(rng.integers(0, 1000)))).date().isoformat()}
               for i, nm in enumerate(names(rng, n_mem), 1)]
    n_loans = 600
    popular = rng.dirichlet(np.ones(n_books) * 0.6)
    borrow = pd.Timestamp('2025-01-02') + pd.to_timedelta(rng.integers(0, 150, n_loans), unit='D')
    days = rng.integers(3, 35, n_loans)
    ret = (borrow + pd.to_timedelta(days, unit='D')).strftime('%Y/%m/%d').to_numpy(dtype=object)
    ret[borrow > pd.Timestamp('2025-05-10')] = ''        # 近期借出者部分尚未歸還
    ret[rng.random(n_loans) < 0.03] = ''
    loans = pd.DataFrame({'借閱編號': [f'L{i:05d}' for i in range(1, n_loans + 1)],
                          '會員編號': rng.choice([m['會員編號'] for m in members], n_loans),
                          '書號': rng.choice(books['書號'], n_loans, p=popular),
                          '借書日': borrow.strftime('%Y/%m/%d'),
                          '還書日': ret})
    loans = loans.sort_values('借閱編號')
    folder = ROOT / '03_library_files'
    d = folder / 'data'
    d.mkdir(parents=True, exist_ok=True)
    xlsx = d / 'books.xlsx'
    with pd.ExcelWriter(xlsx, engine='openpyxl') as w:
        books.to_excel(w, sheet_name='書目', index=False)
        cats.to_excel(w, sheet_name='分類代碼', index=False)
    freeze_xlsx(xlsx)
    pl = save_csv(loans, d / 'loans_big5.csv', encoding='cp950')
    pj = d / 'members.json'
    pj.write_text(json.dumps(members, ensure_ascii=False, indent=2), encoding='utf-8')
    data_card(folder, '03 圖書館借閱紀錄', seed,
              [(xlsx, f'Excel，兩個工作表：書目 {n_books} 本、分類代碼 {len(cats)} 類'),
               (pl, f'**Big5（cp950）編碼** CSV，{n_loans} 筆借閱'),
               (pj, f'JSON 陣列，{n_mem} 位會員')],
              {'books.xlsx／書目': [('書號', 'B0001～B0120'), ('書名', '假書名'), ('作者', '假名'),
                                   ('分類號', '文字，三位數，例如 "300"（要保留前導 0）'), ('出版年', '整數')],
               'books.xlsx／分類代碼': [('分類號', '文字，三位數'), ('分類名稱', '中文分類名稱')],
               'loans_big5.csv': [('借閱編號', 'L00001～'), ('會員編號', '對應 members.json'), ('書號', '對應書目'),
                                  ('借書日', '文字，YYYY/MM/DD'), ('還書日', '文字，YYYY/MM/DD；空白表示尚未歸還')],
               'members.json': [('會員編號', 'M001～M080'), ('姓名', '假名'), ('身分', '學生／教職員／校友'),
                                ('加入日期', '文字，YYYY-MM-DD')]},
              '書目分類依比例抽樣；每本書有不同的熱門程度（Dirichlet 分布），借閱時依熱門程度抽書。'
              '借書日為 2025-01-02 起 150 天內，借期 3～34 天；2025-05-10 之後借出的書全部未還，其餘約 3% 未還。',
              ['借閱檔是 Big5 編碼，直接用 UTF-8 讀會出現亂碼或錯誤，要指定 `encoding="cp950"`。',
               '分類號是 "000"、"100" 這種文字，若被讀成數字會變成 0、100，和分類代碼表就對不起來。',
               'Excel 有兩個工作表，預設只會讀到第一個。',
               '日期是文字，還書日有空白，計算借閱天數前要先轉成日期。'])


# ---------------------------------------------------------------- 04 問卷大掃除
def ex04():
    seed = 404
    rng = np.random.default_rng(seed)
    n = 305
    districts = ['信義區', '大安區', '中山區', '松山區', '內湖區', '士林區']
    acts = ['路跑', '市集', '音樂會', '親子手作', '淨灘']
    rows = []
    for i in range(n):
        t = pd.Timestamp('2025-04-01 08:00') + pd.Timedelta(minutes=int(rng.integers(0, 60 * 24 * 20)))
        fmt = rng.choice(['a', 'b', 'c'], p=[.6, .25, .15])
        time_s = t.strftime('%Y/%m/%d %H:%M') if fmt == 'a' else t.strftime('%Y-%m-%d') if fmt == 'b' else f'{t.month}月{t.day}日'
        name = rng.choice(SURNAMES) + ''.join(rng.choice(GIVEN, 2))
        if rng.random() < .08:
            name = f' {name} '
        g = rng.choice(['男', '女'])
        gender = rng.choice({'男': ['男', '男', '男', 'M', '男生', 'male'], '女': ['女', '女', '女', 'F', '女生', 'female']}[g])
        if rng.random() < .03:
            gender = ''
        age = int(np.clip(rng.normal(38, 13), 15, 80))
        r = rng.random()
        age_s = f'{age}歲' if r < .12 else '' if r < .16 else '999' if r < .18 else str(age)
        phone = f'09{rng.integers(10, 99)}{rng.integers(0, 999999):06d}'
        pf = rng.choice(['a', 'b', 'c', 'd'], p=[.45, .3, .15, .1])
        phone_s = phone if pf == 'a' else f'{phone[:4]}-{phone[4:7]}-{phone[7:]}' if pf == 'b' else '+886' + phone[1:] if pf == 'c' else phone[1:]
        dist = rng.choice(districts)
        dist = rng.choice([dist, dist, dist, dist[:-1], f' {dist}'])
        k = rng.integers(1, 4)
        chosen = list(rng.choice(acts, k, replace=False))
        sep = rng.choice([';', '、', ','])
        sat = int(rng.choice([1, 2, 3, 4, 5], p=[.05, .08, .2, .37, .3]))
        r = rng.random()
        sat_s = f'{sat}分' if r < .07 else ('非常滿意' if sat == 5 else '滿意' if sat == 4 else str(sat)) if r < .12 else '6' if r < .135 else '' if r < .16 else str(sat)
        rows.append((time_s, name, gender, age_s, phone_s, dist, sep.join(chosen), sat_s))
    df = pd.DataFrame(rows, columns=['填答時間', '姓名', '性別', '年齡', '電話', '居住區', '參加活動', '滿意度'])
    dup = df.sample(15, random_state=seed)                 # 重複送出的問卷
    df = pd.concat([df, dup]).sample(frac=1, random_state=seed).reset_index(drop=True)
    folder = ROOT / '04_survey_cleaning'
    p = save_csv(df, folder / 'data' / 'survey_raw.csv')
    data_card(folder, '04 社區活動問卷大掃除', seed, [(p, f'{len(df)} 列原始問卷（含重複送出）')],
              {'survey_raw.csv': [('填答時間', '文字，格式混雜：2025/04/03 14:05、2025-04-03、4月3日'),
                                  ('姓名', '假名，部分前後有空白'), ('性別', '男／女／M／F／男生／female…；少數空白'),
                                  ('年齡', '文字：25、25歲、999、空白'), ('電話', '0912345678、0912-345-678、+886912345678、912345678'),
                                  ('居住區', '台北市六區，部分寫成「信義」或前面有空白'),
                                  ('參加活動', '多選，分隔符號混用 ; 、 ,'), ('滿意度', '1～5，混入「5分」「非常滿意」「滿意」、6 與空白')]},
              f'先產生 {n} 份乾淨問卷，再依比例把欄位改成各種常見的不一致寫法，最後隨機複製 15 份當作重複送出並打亂順序。',
              ['15 筆完全重複的列。', '同一個意思有多種寫法（性別、居住區、滿意度）。',
               '年齡 999 與滿意度 6 是不可能的值。', '電話要統一成 09 開頭 10 碼。',
               '多選欄位要拆開才能統計各活動人數。', '「4月3日」這種寫法沒有年份，要決定如何補上。'])


# ---------------------------------------------------------------- 05 連鎖書店訂單合併
def ex05():
    seed = 505
    rng = np.random.default_rng(seed)
    stores = pd.DataFrame([('S01', '台北車站店', '台北市'), ('S02', '板橋店', '新北市'), ('S03', '桃園店', '桃園市'),
                           ('S04', '台中店', '台中市'), ('S05', '台南店', '台南市'), ('S06', '高雄店', '高雄市')],
                          columns=['門市代碼', '門市', '縣市'])
    prods = pd.DataFrame([
        ('P001', '原子習慣', '商業理財', 330), ('P002', '被討厭的勇氣', '心理勵志', 300), ('P003', '人類大歷史', '人文史地', 450),
        ('P004', 'Python 資料分析', '電腦資訊', 780), ('P005', '小王子', '文學小說', 200), ('P006', '解憂雜貨店', '文學小說', 350),
        ('P007', '蛤蟆先生去看心理師', '心理勵志', 380), ('P008', '底層邏輯', '商業理財', 420), ('P009', '深度學習入門', '電腦資訊', 580),
        ('P010', '三體', '文學小說', 399), ('P011', '槍炮、病菌與鋼鐵', '人文史地', 520), ('P012', '我的第一本手帳', '生活風格', 280),
    ], columns=['商品編號', '書名', '類別', '售價'])
    folder = ROOT / '05_bookstore_merge'
    d = folder / 'data'
    files = []
    oid = 1
    weights = np.array([1.4, 1.1, .8, 1.0, .7, .6])
    for month, n in [(1, 380), (2, 340), (3, 410)]:
        days = pd.Period(f'2025-{month:02d}').days_in_month
        store = rng.choice(['S01', 'S02', 'S03', 'S04', 'S05', 'S07'], n, p=np.r_[weights[:5], .3] / (weights[:5].sum() + .3))
        df = pd.DataFrame({
            '訂單編號': [f'O{oid + i:05d}' for i in range(n)],
            '日期': [f'2025-{month:02d}-{int(x):02d}' for x in rng.integers(1, days + 1, n)],
            '門市代碼': store,
            '商品編號': rng.choice(list(prods['商品編號']) + ['P013'], n, p=[.1] * 4 + [.05] * 8 + [.2]),
            '數量': rng.choice([1, 1, 1, 2, 2, 3], n),
        }).sort_values(['日期', '訂單編號'])
        oid += n
        if month == 2:                                       # 二月：代碼大小寫與空白不一致
            m = rng.random(n) < .25
            df.loc[m, '門市代碼'] = df.loc[m, '門市代碼'].str.lower() + ' '
        if month == 3:                                       # 三月：欄位名稱改了
            df = df.rename(columns={'數量': '購買數量'})
        files.append((save_csv(df, d / f'orders_2025_{month:02d}.csv'), f'2025 年 {month} 月訂單 {n} 筆'))
    files.append((save_csv(stores, d / 'stores.csv'), f'門市資料 {len(stores)} 家'))
    files.append((save_csv(prods, d / 'products.csv'), f'商品資料 {len(prods)} 項'))
    data_card(folder, '05 連鎖書店季報合併', seed, files,
              {'orders_2025_01～03.csv': [('訂單編號', 'O00001～，三個月連續編號'), ('日期', '文字，YYYY-MM-DD'),
                                          ('門市代碼', 'S01～S07'), ('商品編號', 'P001～P013'),
                                          ('數量（三月檔叫「購買數量」）', '整數／本')],
               'stores.csv': [('門市代碼', 'S01～S06'), ('門市', '門市名稱'), ('縣市', '所在縣市')],
               'products.csv': [('商品編號', 'P001～P012'), ('書名', '書名'), ('類別', '書籍類別'), ('售價', '整數／台幣')]},
              '各門市依權重抽樣訂單，熱門書（P001～P004）出現機率較高。訂單只記錄代碼，門市名稱與售價要透過合併取得。',
              ['二月約 25% 的門市代碼寫成小寫且結尾多一個空白（例如 "s02 "），直接合併會對不上。',
               '三月的數量欄位改名為「購買數量」，直接上下合併會變成「數量」「購買數量」兩個欄位，各自缺少部分月份的值。',
               '訂單中有門市 S07，但門市資料沒有這家店；S06 在門市資料中卻沒有任何訂單。',
               '訂單中有商品 P013，但商品資料沒有這項商品。',
               '要決定用哪一種 merge（inner／left／outer），並說明會不會讓營業額變少。'])


# ---------------------------------------------------------------- 06 縣市用電長寬轉換
def ex06():
    seed = 606
    rng = np.random.default_rng(seed)
    counties = [('基隆市', '北部', 1.2), ('臺北市', '北部', 10.5), ('新北市', '北部', 14.0), ('桃園市', '北部', 13.5),
                ('新竹市', '北部', 4.6), ('新竹縣', '北部', 5.2), ('宜蘭縣', '東部', 1.8), ('苗栗縣', '中部', 3.4),
                ('臺中市', '中部', 15.0), ('彰化縣', '中部', 6.1), ('南投縣', '中部', 1.7), ('雲林縣', '中部', 5.5),
                ('嘉義市', '南部', 1.0), ('嘉義縣', '南部', 2.2), ('臺南市', '南部', 10.8), ('高雄市', '南部', 16.2),
                ('屏東縣', '南部', 2.9), ('花蓮縣', '東部', 1.4), ('臺東縣', '東部', 0.8), ('澎湖縣', '離島', 0.3),
                ('金門縣', '離島', 0.25), ('連江縣', '離島', 0.03)]
    months = pd.period_range('2024-01', '2025-12', freq='M')
    season = {1: .86, 2: .80, 3: .88, 4: .95, 5: 1.05, 6: 1.17, 7: 1.27, 8: 1.28, 9: 1.18, 10: 1.02, 11: .92, 12: .88}
    rows = []
    for name, region, base in counties:
        vals = []
        for m in months:
            growth = 1 + 0.025 * (m.year - 2024)
            vals.append(round(base * 100 * season[m.month] * growth * rng.normal(1, .03), 1))
        rows.append([name, region] + vals)
    df = pd.DataFrame(rows, columns=['縣市', '區域'] + [str(m) for m in months])
    folder = ROOT / '06_power_reshape'
    p = save_csv(df, folder / 'data' / 'power_wide.csv')
    data_card(folder, '06 縣市用電長寬轉換', seed, [(p, f'寬表格：{len(df)} 縣市 × 24 個月')],
              {'power_wide.csv': [('縣市', '22 個縣市'), ('區域', '北部／中部／南部／東部／離島'),
                                  ('2024-01 … 2025-12', '浮點／百萬度，該月用電量；每個月份是一個欄位')]},
              '每個縣市有固定的用電規模，乘上月份季節係數（7、8 月最高約 1.28，2 月最低約 0.80），'
              '2025 年整體成長 2.5%，再加上 ±3% 隨機波動。',
              ['資料是「寬」格式：月份分散在 24 個欄位，無法直接依年份或月份分組，要先 melt 成長格式。',
               '欄位名稱「2024-01」是文字，轉長格式後要拆出年、月或轉成日期。',
               '縣市規模差距很大（連江縣約為新北市的 0.2%），比較季節變化時可考慮改看比例。'])


# ---------------------------------------------------------------- 07 健身房 groupby
def ex07():
    seed = 707
    rng = np.random.default_rng(seed)
    n_mem = 200
    branches = ['松江店', '公館店', '板橋店', '新莊店']
    mem = pd.DataFrame({
        '會員編號': [f'G{i:03d}' for i in range(1, n_mem + 1)],
        '分店': rng.choice(branches, n_mem, p=[.3, .25, .25, .2]),
        '方案': rng.choice(['月繳', '季繳', '年繳', '單次'], n_mem, p=[.35, .25, .25, .15]),
        '年齡層': rng.choice(['18-24', '25-34', '35-44', '45-54', '55+'], n_mem, p=[.2, .32, .24, .15, .09]),
    })
    freq = {'單次': .4, '月繳': 1.0, '季繳': 1.3, '年繳': 1.6}
    act = rng.gamma(2, 1, n_mem) * mem['方案'].map(freq).to_numpy()
    n = 3000
    who = rng.choice(n_mem, n, p=act / act.sum())
    m = mem.iloc[who].reset_index(drop=True)
    dates = pd.Timestamp('2025-01-01') + pd.to_timedelta(rng.integers(0, 181, n), unit='D')
    age_min = m['年齡層'].map({'18-24': 70, '25-34': 65, '35-44': 60, '45-54': 55, '55+': 50}).to_numpy()
    minutes = np.clip(rng.normal(age_min, 18), 15, 180).round().astype(int)
    spend = np.where(rng.random(n) < .35, rng.choice([60, 80, 120, 350, 600], n, p=[.35, .3, .2, .1, .05]), 0)
    spend = np.where(m['方案'] == '單次', spend + 250, spend)
    df = pd.DataFrame({'紀錄編號': [f'V{i:05d}' for i in range(1, n + 1)], '會員編號': m['會員編號'], '分店': m['分店'],
                       '方案': m['方案'], '年齡層': m['年齡層'], '日期': dates.strftime('%Y-%m-%d'),
                       '運動分鐘': minutes, '消費金額': spend})
    df = df.sort_values(['日期', '紀錄編號']).reset_index(drop=True)
    df['紀錄編號'] = [f'V{i:05d}' for i in range(1, n + 1)]
    folder = ROOT / '07_gym_groupby'
    p = save_csv(df, folder / 'data' / 'gym_visits.csv')
    data_card(folder, '07 健身房會員分析', seed, [(p, f'{n} 筆入場紀錄；會員 G001～G{n_mem:03d} 中實際有入場的 {df["會員編號"].nunique()} 位')],
              {'gym_visits.csv': [('紀錄編號', 'V00001～，依日期排序'), ('會員編號', 'G001～G200'), ('分店', '4 家分店'),
                                  ('方案', '月繳／季繳／年繳／單次'), ('年齡層', '18-24／25-34／35-44／45-54／55+'),
                                  ('日期', '文字，2025-01-01～2025-06-30'), ('運動分鐘', '整數／分鐘，15～180'),
                                  ('消費金額', '整數／台幣；入場以外的加購（飲料、課程），單次方案含 250 元入場費')]},
              '每位會員有固定的分店、方案與年齡層；活躍度＝Gamma 隨機值 × 方案係數（年繳 1.6、季繳 1.3、月繳 1.0、單次 0.4），'
              '依活躍度抽出 3,000 筆入場。年齡越大平均運動時間越短；約 35% 入場有加購。',
              ['同一位會員會出現很多次，「會員數」要用 `nunique`，不能用 `count`。',
               f'會員編號到 G{n_mem:03d}，但有 {n_mem - df["會員編號"].nunique()} 位會員半年內沒有入場，不會出現在資料中。',
               '消費金額多數是 0，平均數和中位數差很多。',
               '單次方案的消費含入場費，直接和其他方案比消費金額要先說明。'])


# ---------------------------------------------------------------- 08 外送訂單時間
def ex08():
    seed = 808
    rng = np.random.default_rng(seed)
    n = 2500
    days = pd.date_range('2025-05-01', '2025-06-30', freq='D')
    day_w = np.array([1.35 if d.dayofweek >= 5 else 1.0 for d in days])
    day_w[days == pd.Timestamp('2025-05-31')] = 2.0          # 端午節
    day_w *= np.linspace(.95, 1.1, len(days))                # 慢慢成長
    hour_w = np.array([.2, .1, .05, .03, .03, .05, .2, .5, .7, .6, .8, 2.2, 3.0, 1.4, .7, .6, .8, 1.6, 2.8, 2.4, 1.3, .9, .7, .4])
    day = rng.choice(len(days), n, p=day_w / day_w.sum())
    hour = rng.choice(24, n, p=hour_w / hour_w.sum())
    local = days[day] + pd.to_timedelta(hour, unit='h') + pd.to_timedelta(rng.integers(0, 3600, n), unit='s')
    area = rng.choice(['中正區', '大安區', '信義區', '中山區', '內湖區'], n, p=[.2, .25, .2, .2, .15])
    rush = np.isin(hour, [11, 12, 18, 19])
    mins = np.clip(rng.normal(28, 7, n) + rush * 9 + (area == '內湖區') * 6, 12, 90).round()
    t_utc = local.tz_localize('Asia/Taipei').tz_convert('UTC')
    done = t_utc + pd.to_timedelta(mins, unit='min')
    amt = np.clip(rng.gamma(4, 75, n), 80, 2000).round().astype(int)
    df = pd.DataFrame({'訂單編號': '', '下單時間_utc': t_utc.strftime('%Y-%m-%dT%H:%M:%SZ'),
                       '送達時間_utc': done.strftime('%Y-%m-%dT%H:%M:%SZ'), '區域': area, '訂單金額': amt})
    df = df.sort_values('下單時間_utc').reset_index(drop=True)
    df['訂單編號'] = [f'D{i:05d}' for i in range(1, n + 1)]
    folder = ROOT / '08_delivery_time'
    p = save_csv(df, folder / 'data' / 'delivery_orders.csv')
    data_card(folder, '08 外送訂單時間分析', seed, [(p, f'{n} 筆外送訂單，2025-05-01～06-30（台灣時間）')],
              {'delivery_orders.csv': [('訂單編號', 'D00001～，依下單時間排序'),
                                       ('下單時間_utc', '文字，ISO 8601，**UTC 時間**，例如 2025-05-01T03:15:22Z'),
                                       ('送達時間_utc', '文字，ISO 8601，UTC 時間'), ('區域', '台北市五區'),
                                       ('訂單金額', '整數／台幣')]},
              '依台灣時間產生下單時刻：午餐（11～12 點）與晚餐（18～19 點）是高峰，週末 ×1.35，'
              '2025-05-31（端午節）×2，兩個月整體逐漸成長約 15%。尖峰時段送達時間多 9 分鐘，內湖區多 6 分鐘。最後換算成 UTC 存檔。',
              ['時間是 UTC，直接取小時會比台灣時間少 8 小時，午餐高峰會跑到凌晨 3～4 點。',
               '換算成台灣時間後，部分訂單的「日期」也會改變（UTC 16:00 之後是台灣隔天）。',
               '送達分鐘數要用兩個時間相減取得。', '端午節那天訂單特別多，是 rolling 平均會被拉高的原因。'])


# ---------------------------------------------------------------- 09 氣象站月資料
def ex09():
    seed = 909
    rng = np.random.default_rng(seed)
    cities = {'臺北': (16.5, 30.0, [80, 170, 180, 170, 230, 320, 230, 300, 360, 150, 80, 75], 1400),
              '臺中': (16.5, 29.0, [30, 90, 95, 125, 225, 360, 300, 330, 120, 15, 20, 25], 2100),
              '臺南': (18.0, 29.5, [20, 25, 40, 70, 180, 400, 380, 420, 200, 30, 15, 15], 2200),
              '高雄': (19.5, 29.5, [20, 25, 40, 75, 190, 420, 390, 430, 230, 50, 15, 15], 2150),
              '花蓮': (18.0, 28.5, [60, 90, 85, 90, 190, 210, 160, 230, 350, 370, 160, 70], 1650),
              '恆春': (21.5, 28.5, [25, 25, 25, 50, 200, 450, 420, 480, 320, 120, 40, 20], 2300)}
    rows = []
    for city, (tmin, tmax, rain, sun) in cities.items():
        for m in range(1, 13):
            temp = tmin + (tmax - tmin) * (1 - np.cos((m - 1.3) / 12 * 2 * np.pi)) / 2
            r = max(0, rain[m - 1] * rng.normal(1, .2))
            rows.append((city, m, round(temp + rng.normal(0, .4), 1), round(r, 1),
                         round(sun / 12 * (1.25 - r / 900) * rng.normal(1, .06), 1), int(np.clip(r / 14 + rng.normal(0, 1.5), 1, 26))))
    df = pd.DataFrame(rows, columns=['城市', '月份', '平均氣溫', '降雨量', '日照時數', '降雨日數'])
    folder = ROOT / '09_weather_charts'
    p = save_csv(df, folder / 'data' / 'weather_monthly.csv')
    data_card(folder, '09 六城市氣象月資料', seed, [(p, f'6 城市 × 12 個月＝{len(df)} 筆')],
              {'weather_monthly.csv': [('城市', '臺北／臺中／臺南／高雄／花蓮／恆春'), ('月份', '整數 1～12'),
                                       ('平均氣溫', '浮點／°C'), ('降雨量', '浮點／毫米'), ('日照時數', '浮點／小時'),
                                       ('降雨日數', '整數／天')]},
              '各城市以「最冷月、最熱月」氣溫畫出餘弦形狀的年循環，降雨量依照台灣各地典型的季節型態'
              '（西部夏雨、花蓮秋雨）乘上 ±20% 波動；雨多的月份日照較少。數值為教學用近似，不是中央氣象署觀測值。',
              ['資料是長格式，每個城市 12 列，畫多條折線時要依城市分開或先 pivot。',
               '降雨量與日照時數單位不同，畫在同一張圖要用雙 Y 軸或分開畫。',
               '月份是數字，座標軸要顯示成「1月、2月…」。'])


# ---------------------------------------------------------------- 10 租屋 Seaborn
def ex10():
    seed = 1010
    rng = np.random.default_rng(seed)
    n = 800
    dist = {'大安區': 1.35, '信義區': 1.3, '中山區': 1.15, '松山區': 1.18, '文山區': .85, '北投區': .82}
    d = rng.choice(list(dist), n, p=[.18, .14, .2, .14, .18, .16])
    kind = rng.choice(['套房', '雅房', '整層住家'], n, p=[.5, .15, .35])
    size = np.where(kind == '雅房', rng.uniform(3, 7, n), np.where(kind == '套房', rng.uniform(5, 14, n), rng.uniform(15, 45, n)))
    age = np.clip(rng.gamma(3, 9, n), 0, 60).round()
    floor = rng.integers(1, 16, n)
    elevator = np.where(floor > 5, '有', rng.choice(['有', '無'], n, p=[.35, .65]))
    rent = (1100 * size * np.vectorize(dist.get)(d) * (1 - age / 150) * np.where(kind == '雅房', .8, 1)
            * np.where(elevator == '有', 1.06, 1) * rng.lognormal(0, .12, n) + 2500)
    rent = (np.round(rent / 100) * 100).astype(int)
    df = pd.DataFrame({'物件編號': [f'R{i:04d}' for i in range(1, n + 1)], '行政區': d, '類型': kind,
                       '坪數': size.round(1), '屋齡': age.astype(int), '樓層': floor, '電梯': elevator, '月租金': rent})
    df.loc[[57, 402], '月租金'] = [1, 980000]                 # 輸入錯誤
    df.loc[611, '坪數'] = 0.0
    folder = ROOT / '10_rent_seaborn'
    p = save_csv(df, folder / 'data' / 'rent_listings.csv')
    data_card(folder, '10 台北租屋行情', seed, [(p, f'{n} 筆租屋物件')],
              {'rent_listings.csv': [('物件編號', 'R0001～R0800'), ('行政區', '台北市六區'), ('類型', '套房／雅房／整層住家'),
                                     ('坪數', '浮點／坪'), ('屋齡', '整數／年'), ('樓層', '整數，1～15'),
                                     ('電梯', '有／無'), ('月租金', '整數／台幣')]},
              '月租金 ≈ 1,100 × 坪數 × 行政區係數（大安 1.35～北投 0.82）×（1－屋齡/150）× 類型與電梯係數 × 對數常態雜訊＋2,500，'
              '四捨五入到百元。5 樓以上一定有電梯。',
              ['有 3 筆明顯的輸入錯誤：月租金 1 元、月租金 980,000 元、坪數 0。畫圖前要先找出並決定如何處理。',
               '整層住家的坪數與租金遠大於套房、雅房，混在一起看分布會變成多峰。',
               '要比較「每坪租金」才公平，原始資料沒有這個欄位。'])


# ---------------------------------------------------------------- 11 業務 KPI 表格
def ex11():
    seed = 1111
    rng = np.random.default_rng(seed)
    reps = names(rng, 15)
    team = ['北區'] * 5 + ['中區'] * 5 + ['南區'] * 5
    skill = rng.normal(1, .15, 15)
    skill[3], skill[12] = 1.35, .7                           # 一位明星、一位需要協助
    rows = []
    for i, (rep, t) in enumerate(zip(reps, team)):
        target = int(rng.choice([180, 200, 220])) * 1000
        for w in range(1, 14):
            actual = int(round(target * skill[i] * rng.normal(1, .12) * (1.15 if w in (12, 13) else 1) / 1000) * 1000)
            rows.append((rep, t, w, target, actual, int(rng.poisson(3 * skill[i])), int(rng.poisson(.6))))
    df = pd.DataFrame(rows, columns=['業務', '組別', '週次', '週目標', '週實績', '新客數', '退貨筆數'])
    folder = ROOT / '11_sales_kpi_style'
    p = save_csv(df, folder / 'data' / 'sales_kpi.csv')
    data_card(folder, '11 業務週報 KPI', seed, [(p, f'15 位業務 × 13 週＝{len(df)} 筆')],
              {'sales_kpi.csv': [('業務', '假名'), ('組別', '北區／中區／南區，各 5 人'), ('週次', '整數 1～13（2025 第一季）'),
                                 ('週目標', '整數／台幣，每人固定'), ('週實績', '整數／台幣，千元為單位四捨五入'),
                                 ('新客數', '整數／人'), ('退貨筆數', '整數／筆')]},
              '每位業務有固定週目標（18、20 或 22 萬）與能力係數，週實績＝目標 × 能力 × ±12% 波動，季末兩週（第 12、13 週）×1.15 衝業績。'
              '第 4 位業務能力 1.35（明星），第 13 位 0.7（需要協助）。',
              ['沒有「達成率」欄位，要自己算；每週和整季的達成率算法不同（整季要用加總後相除，不是平均每週達成率）。',
               '金額很大，表格要加千分位與單位，否則難以閱讀。',
               '季末衝業績會讓最後兩週看起來特別好，解讀時要說明。'])


# ---------------------------------------------------------------- 12 共享單車綜合專題
def ex12():
    seed = 1212
    rng = np.random.default_rng(seed)
    stations = pd.DataFrame([
        ('T01', '捷運市政府站', '信義區', 60, 1.6), ('T02', '台北101', '信義區', 50, 1.3), ('T03', '捷運公館站', '中正區', 55, 1.5),
        ('T04', '臺大校門口', '大安區', 70, 1.7), ('T05', '捷運忠孝復興站', '大安區', 45, 1.2), ('T06', '華山文創園區', '中正區', 40, 1.0),
        ('T07', '捷運中山站', '中山區', 50, 1.3), ('T08', '大稻埕碼頭', '大同區', 35, .9), ('T09', '捷運劍潭站', '士林區', 45, 1.1),
        ('T10', '內湖科學園區', '內湖區', 60, 1.2), ('T11', '捷運南港展覽館站', '南港區', 40, .8), ('T12', '松山文創園區', '信義區', 35, .8),
    ], columns=['站點代碼', '站名', '行政區', '車位數', 'w'])
    days = pd.date_range('2025-04-01', '2025-06-30', freq='D')
    weather = []
    for d in days:
        p_rain = .25 + .25 * (d.month == 6) + .1 * (d.month == 5)
        w = rng.choice(['晴', '多雲', '雨'], p=[(1 - p_rain) * .55, (1 - p_rain) * .45, p_rain])
        hi = 24 + 7 * (d.dayofyear - 91) / 90 + rng.normal(0, 1.6) - (2 if w == '雨' else 0)
        rain = round(float(rng.gamma(2, 9)), 1) if w == '雨' else 0.0
        weather.append((d.date().isoformat(), w, round(hi, 1), rain))
    wdf = pd.DataFrame(weather, columns=['日期', '天氣', '最高溫', '降雨量'])
    dw = np.array([(1.25 if d.dayofweek >= 5 else 1.0) * (.55 if w[1] == '雨' else 1.0) for d, w in zip(days, weather)])
    n = 6000
    di = rng.choice(len(days), n, p=dw / dw.sum())
    weekend = days[di].dayofweek >= 5
    wk = np.array([.1, .05, .02, .02, .03, .1, .5, 1.6, 2.2, .9, .6, .8, 1.0, .8, .7, .9, 1.3, 2.3, 1.9, 1.1, .8, .6, .4, .2])
    we = np.array([.15, .08, .03, .02, .02, .05, .15, .35, .6, .9, 1.3, 1.5, 1.5, 1.5, 1.6, 1.7, 1.7, 1.5, 1.2, 1.0, .8, .6, .4, .25])
    hour = np.where(weekend, rng.choice(24, n, p=we / we.sum()), rng.choice(24, n, p=wk / wk.sum()))
    start = days[di] + pd.to_timedelta(hour, unit='h') + pd.to_timedelta(rng.integers(0, 3600, n), unit='s')
    sw = stations['w'].to_numpy()
    s_from = rng.choice(stations['站點代碼'], n, p=sw / sw.sum())
    s_to = rng.choice(stations['站點代碼'], n, p=sw / sw.sum())
    user = rng.choice(['會員', '單次'], n, p=[.72, .28])
    user = np.where(weekend & (rng.random(n) < .2), '單次', user)
    dur = np.clip(rng.lognormal(np.log(np.where(user == '單次', 26, 14)), .55), 2, 240)
    end = start + pd.to_timedelta(dur.round(1), unit='min')
    df = pd.DataFrame({'騎乘編號': '', '借車站': s_from, '還車站': s_to,
                       '借車時間': start.strftime('%Y-%m-%d %H:%M:%S'), '還車時間': end.strftime('%Y-%m-%d %H:%M:%S'),
                       '使用者類型': user,
                       '年齡層': rng.choice(['18-24', '25-34', '35-44', '45-54', '55+'], n, p=[.3, .33, .19, .12, .06])})
    df = df.sort_values('借車時間').reset_index(drop=True)
    bad = rng.choice(n, 25, replace=False)                   # 還車時間早於借車時間
    df.loc[bad, ['借車時間', '還車時間']] = df.loc[bad, ['還車時間', '借車時間']].to_numpy()
    long_ = rng.choice(np.setdiff1d(np.arange(n), bad), 8, replace=False)   # 忘記還車，超過一天
    df.loc[long_, '還車時間'] = (pd.to_datetime(df.loc[long_, '借車時間']) + pd.Timedelta(days=2, hours=3)).dt.strftime('%Y-%m-%d %H:%M:%S').to_numpy()
    miss = rng.choice(n, 60, replace=False)
    df.loc[miss, '還車站'] = ''
    df = pd.concat([df, df.sample(20, random_state=seed)]).sort_values('借車時間').reset_index(drop=True)
    ids, seen, k = [], {}, 0
    for row in df.itertuples(index=False):                   # 重複列共用同一個騎乘編號
        key = (row.借車站, row.借車時間, row.還車時間)
        if key not in seen:
            k += 1
            seen[key] = f'K{k:05d}'
        ids.append(seen[key])
    df['騎乘編號'] = ids
    folder = ROOT / '12_bike_capstone'
    d = folder / 'data'
    files = [(save_csv(df, d / 'bike_trips.csv'), f'{len(df)} 筆騎乘紀錄（含重複），2025-04-01～06-30'),
             (save_csv(stations.drop(columns='w'), d / 'stations.csv'), f'{len(stations)} 個站點'),
             (save_csv(wdf, d / 'weather_daily.csv'), f'{len(wdf)} 天天氣')]
    data_card(folder, '12 共享單車綜合專題', seed, files,
              {'bike_trips.csv': [('騎乘編號', 'K00001～；重複送出的紀錄編號相同'), ('借車站／還車站', '站點代碼 T01～T12；還車站少數空白'),
                                  ('借車時間／還車時間', '文字，YYYY-MM-DD HH:MM:SS，台灣時間'), ('使用者類型', '會員／單次'),
                                  ('年齡層', '18-24／25-34／35-44／45-54／55+')],
               'stations.csv': [('站點代碼', 'T01～T12'), ('站名', '站點名稱'), ('行政區', '台北市行政區'), ('車位數', '整數')],
               'weather_daily.csv': [('日期', '文字，YYYY-MM-DD'), ('天氣', '晴／多雲／雨'), ('最高溫', '浮點／°C'),
                                     ('降雨量', '浮點／毫米，非雨天為 0')]},
              '每天的騎乘量受星期（週末 ×1.25）與天氣（雨天 ×0.55）影響；平日有 8 點、18 點通勤雙峰，週末是午後單峰。'
              '單次使用者平均騎得較久（約 26 分鐘，會員約 14 分鐘）。站點熱門程度不同，捷運站與臺大校門口最熱門。',
              ['20 筆完全重複的紀錄（以下筆數都是去除重複後的數字）。', '25 筆還車時間早於借車時間（兩個時間被填反）。',
               '8 筆騎乘超過 2 天（忘記還車），會嚴重拉高平均騎乘時間。', '60 筆還車站空白。',
               '天氣在另一個檔案，要用日期合併；借車時間要先取出日期。',
               '這是完整專題：沒有指定唯一答案，學生要自己提出問題、說明清理決定並用圖表回答。'])


if __name__ == '__main__':
    for f in [ex01, ex02, ex03, ex04, ex05, ex06, ex07, ex08, ex09, ex10, ex11, ex12]:
        f()
        print('ok', f.__name__)
