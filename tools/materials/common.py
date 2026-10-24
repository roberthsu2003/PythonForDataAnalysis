"""茶語時光（虛構手搖飲連鎖品牌）共用模擬模型。

所有章節的學生素材都由這裡的門市、菜單、氣溫與事件模型產生，
資料為模擬資料，事件日期參考 2023、2024 年台灣實際的節日與颱風假。
"""
import numpy as np
import pandas as pd

SEED = 2024

STORES = pd.DataFrame([
    # 門市代碼, 門市, 縣市, 開幕日, 座位數, 月租金, 每日基本杯數, 特色
    ('S01', '台北信義店', '台北市', '2019-03-15', 12, 180000, 330, '商辦區，平日午後最忙'),
    ('S02', '台北西門店', '台北市', '2018-07-01', 8, 150000, 360, '觀光客多，假日爆量'),
    ('S03', '台中逢甲店', '台中市', '2020-11-20', 6, 90000, 390, '夜市商圈，晚上最旺'),
    ('S04', '台南成大店', '台南市', '2021-09-01', 20, 60000, 280, '學生客群，偏愛全糖'),
    ('S05', '高雄巨蛋店', '高雄市', '2022-05-10', 10, 85000, 300, '演唱會散場人潮'),
], columns=['門市代碼', '門市', '縣市', '開幕日', '座位數', '月租金', '基本杯數', '特色'])

MENU = pd.DataFrame([
    # 品項代碼, 品項, 類別, 中杯價, 成本, 基本權重
    ('001', '珍珠奶茶', '奶茶', 55, 17, 20.0),
    ('002', '四季春青茶', '純茶', 35, 7, 12.6),
    ('003', '鮮奶綠', '鮮奶', 55, 20, 10.4),
    ('004', '冬瓜檸檬', '果茶', 50, 14, 9.3),
    ('005', '多多綠', '果茶', 50, 15, 8.1),
    ('006', '黑糖珍珠鮮奶', '鮮奶', 75, 27, 11.7),
    ('007', '芒果冰沙', '冰沙', 70, 29, 0),   # 權重隨氣溫變化
    ('008', '熱可可', '熱飲', 60, 21, 0),     # 權重隨氣溫變化
    ('009', '檸檬紅茶', '果茶', 40, 11, 9.6),
    ('010', '芋頭鮮奶', '鮮奶', 70, 26, 11.2),  # 2024-04-01 新品上市
], columns=['品項代碼', '品項', '類別', '中杯價', '成本', '權重'])
NEW_ITEM_CODE, NEW_ITEM_DATE = '010', pd.Timestamp('2024-04-01')
LARGE_EXTRA = 10

SWEETNESS = ['正常糖', '少糖', '半糖', '微糖', '無糖']
ICE = ['正常冰', '少冰', '微冰', '去冰', '熱']
PAYMENTS = ['現金', '悠遊卡', 'LINE Pay', '街口支付', '信用卡', 'Apple Pay']
PAY_P = [0.32, 0.14, 0.22, 0.10, 0.12, 0.10]

# 各縣市氣溫：年中值、振幅
CITY_TEMP = {'台北市': (26.0, 7.5), '台中市': (27.5, 5.5), '台南市': (28.3, 4.8), '高雄市': (28.8, 4.0)}

# 事件：日期 → (影響門市或 'ALL', 倍數, 說明)
EVENTS = {
    # 2023 颱風（參考實際停班停課日）
    '2023-07-27': (['S04', 'S05'], 0.35, '杜蘇芮颱風'),
    '2023-09-03': (['S04', 'S05'], 0.40, '海葵颱風'),
    '2023-09-04': (['S04', 'S05'], 0.55, '海葵颱風'),
    '2023-10-05': (['S04', 'S05'], 0.35, '小犬颱風'),
    # 2024 颱風
    '2024-07-24': ('ALL', 0.40, '凱米颱風'),
    '2024-07-25': ('ALL', 0.30, '凱米颱風'),
    '2024-10-02': (['S04', 'S05'], 0.35, '山陀兒颱風'),
    '2024-10-03': (['S03', 'S04', 'S05'], 0.30, '山陀兒颱風'),
    '2024-10-31': ('ALL', 0.30, '康芮颱風'),
    # 節日
    '2023-02-14': ('ALL', 1.35, '情人節'),
    '2024-02-14': ('ALL', 1.40, '情人節'),
    '2023-08-22': ('ALL', 1.25, '七夕'),
    '2024-08-10': ('ALL', 1.30, '七夕'),
    '2023-12-31': ('ALL', 1.30, '跨年'),
    '2024-12-31': ('ALL', 1.35, '跨年'),
    '2024-02-09': ('ALL', 0.55, '除夕'),
    '2024-02-10': ('ALL', 0.70, '春節'),
    '2023-01-21': ('ALL', 0.55, '除夕'),
    '2023-01-22': ('ALL', 0.70, '春節'),
    # 高雄巨蛋演唱會（虛構場次）
    '2024-03-23': (['S05'], 1.9, '巨蛋演唱會'),
    '2024-03-24': (['S05'], 1.8, '巨蛋演唱會'),
    '2024-06-15': (['S05'], 2.0, '巨蛋演唱會'),
    '2024-09-07': (['S05'], 1.9, '巨蛋演唱會'),
    '2024-12-21': (['S05'], 2.1, '巨蛋演唱會'),
    '2023-11-11': (['S05'], 1.8, '巨蛋演唱會'),
    # 行銷活動：新品上市
    '2024-04-01': ('ALL', 1.25, '芋頭鮮奶上市'),
    '2024-04-02': ('ALL', 1.15, '芋頭鮮奶上市'),
}
# 2024 年 6 月每週三「第二杯半價」
for d in pd.date_range('2024-06-01', '2024-06-30'):
    if d.day_of_week == 2:
        EVENTS[d.strftime('%Y-%m-%d')] = ('ALL', 1.45, '第二杯半價')

WEEKDAY = {  # 星期一～日的倍數
    'S01': [1.10, 1.08, 1.08, 1.10, 1.15, 0.80, 0.70],
    'S02': [0.85, 0.82, 0.85, 0.90, 1.05, 1.40, 1.35],
    'S03': [0.88, 0.85, 0.88, 0.92, 1.15, 1.35, 1.20],
    'S04': [1.00, 1.00, 1.00, 1.02, 1.05, 0.95, 0.90],
    'S05': [0.90, 0.88, 0.90, 0.95, 1.10, 1.30, 1.20],
}


def rng(offset=0):
    return np.random.default_rng(SEED + offset)


def weather(start='2023-01-01', end='2024-12-31'):
    """各縣市每日最高溫與降雨量。"""
    r = rng(1)
    days = pd.date_range(start, end)
    rows = []
    for city, (mid, amp) in CITY_TEMP.items():
        doy = days.dayofyear.values
        base = mid + amp * np.sin(2 * np.pi * (doy - 105) / 365)
        temp = base + r.normal(0, 1.6, len(days))
        rain_p = 0.18 + 0.22 * np.clip(np.sin(2 * np.pi * (doy - 100) / 365), 0, None)
        rain = np.where(r.random(len(days)) < rain_p, r.gamma(1.4, 14, len(days)), 0.0)
        for d, t, rn in zip(days, temp, rain):
            rows.append((d, city, round(float(t), 1), round(float(rn), 1)))
    w = pd.DataFrame(rows, columns=['日期', '縣市', '最高溫', '降雨量'])
    # 颱風日：大雨
    for ds, (who, mult, name) in EVENTS.items():
        if '颱風' in name:
            cities = STORES.set_index('門市代碼').loc[STORES['門市代碼'] if who == 'ALL' else who, '縣市'].unique()
            m = (w['日期'] == pd.Timestamp(ds)) & w['縣市'].isin(cities)
            w.loc[m, '降雨量'] = (w.loc[m, '降雨量'] + 180).round(1)
    return w


def daily_sales(start='2023-01-01', end='2024-12-31'):
    """每日各店杯數與營收（門市層級）。"""
    r = rng(2)
    w = weather(start, end).set_index(['日期', '縣市'])
    days = pd.date_range(start, end)
    rows = []
    for _, s in STORES.iterrows():
        for i, d in enumerate(days):
            t, rain = w.loc[(d, s['縣市'])]
            f = WEEKDAY[s['門市代碼']][d.day_of_week]
            f *= 1 + 0.028 * (t - 26)                      # 越熱越好賣
            f *= 0.82 if rain > 20 else 1.0                 # 大雨少人出門
            f *= 1 + 0.10 * (d - pd.Timestamp('2023-01-01')).days / 365   # 品牌成長
            ev = EVENTS.get(d.strftime('%Y-%m-%d'))
            event = ''
            if ev and (ev[0] == 'ALL' or s['門市代碼'] in ev[0]):
                f *= ev[1]
                event = ev[2]
            cups = max(0, int(round(s['基本杯數'] * f * r.lognormal(0, 0.07))))
            avg_price = 56 + 0.4 * max(0, t - 26) + r.normal(0, 1.2)
            rows.append((d, s['門市代碼'], s['門市'], s['縣市'], t, rain, cups, int(round(cups * avg_price)), event))
    return pd.DataFrame(rows, columns=['日期', '門市代碼', '門市', '縣市', '最高溫', '降雨量', '杯數', '營收', '事件'])


# 各店招牌品項（與「門市資訊.json」的熱銷品項一致）
STORE_ITEM_BOOST = {'S01': {'003': 1.5, '002': 1.4}, 'S02': {'001': 1.35, '007': 1.3}, 'S03': {'006': 1.6},
                    'S04': {'004': 1.5}, 'S05': {'005': 1.5, '010': 1.3}}
# 各店：一筆訂單的品項數分布、大杯比例、付款方式分布
LINES_P = {'S01': [0.50, 0.30, 0.20], 'S02': [0.60, 0.30, 0.10], 'S03': [0.55, 0.32, 0.13],
           'S04': [0.72, 0.22, 0.06], 'S05': [0.60, 0.28, 0.12]}
LARGE_P = {'S01': 0.25, 'S02': 0.33, 'S03': 0.45, 'S04': 0.42, 'S05': 0.35}
STORE_PAY_P = {'S01': [0.16, 0.18, 0.26, 0.08, 0.16, 0.16], 'S02': [0.30, 0.16, 0.22, 0.08, 0.14, 0.10],
               'S03': [0.36, 0.12, 0.22, 0.12, 0.10, 0.08], 'S04': [0.46, 0.10, 0.20, 0.12, 0.08, 0.04],
               'S05': [0.34, 0.12, 0.20, 0.14, 0.12, 0.08]}


def item_weights(temp, date, store_code=None):
    w = MENU.set_index('品項代碼')['權重'].astype(float).copy()
    for c, b in STORE_ITEM_BOOST.get(store_code, {}).items():
        w[c] *= b
    w['007'] = max(0.0, (temp - 25) * 2.2)          # 芒果冰沙：熱才賣
    w['008'] = max(0.0, (22 - temp) * 2.5)          # 熱可可：冷才賣
    if date < NEW_ITEM_DATE:
        w[NEW_ITEM_CODE] = 0.0
    return w / w.sum()


def sweet_probs(store_code):
    if store_code == 'S04':                        # 台南：偏愛全糖
        return [0.42, 0.20, 0.18, 0.12, 0.08]
    if store_code == 'S01':                        # 信義商辦：偏健康
        return [0.12, 0.18, 0.28, 0.20, 0.22]
    return [0.22, 0.22, 0.26, 0.16, 0.14]


HOUR_PROFILE = {   # 10～22 點各小時權重
    'S01': [2, 5, 12, 10, 7, 8, 7, 5, 3, 2, 1, 1, 1],
    'S02': [2, 3, 5, 6, 7, 8, 8, 8, 8, 7, 6, 4, 2],
    'S03': [1, 2, 3, 4, 4, 5, 6, 8, 10, 11, 11, 9, 6],
    'S04': [2, 4, 7, 6, 5, 6, 7, 6, 6, 6, 5, 4, 3],
    'S05': [2, 3, 5, 5, 5, 6, 7, 7, 8, 9, 9, 7, 5],
}

# 時段偏好：午餐前後愛鮮奶（當正餐）、下午茶愛奶茶、晚上愛果茶與純茶（解膩）
SLOT_BOOST = {'午': {'鮮奶': 1.45}, '下午': {'奶茶': 1.45}, '晚': {'果茶': 1.4, '純茶': 1.35}}


def slot_of(hour):
    return '午' if hour <= 13 else '下午' if hour <= 17 else '晚'


SURNAMES = list('陳林黃張李王吳劉蔡楊許鄭謝洪郭邱曾廖賴徐周葉蘇莊呂江何蕭羅高')
GIVEN = ['怡君', '雅婷', '家豪', '志明', '淑芬', '冠宇', '宜庭', '俊傑', '佳穎', '承恩', '詩涵', '柏翰',
         '欣怡', '彥廷', '思妤', '宗翰', '心怡', '品妤', '子軒', '昱廷', '芷晴', '建宏', '郁婷', '冠廷',
         '佩珊', '宇翔', '雅雯', '家瑜', '書豪', '筱涵']


def names(n, offset=0):
    r = rng(100 + offset)
    out, seen = [], set()
    while len(out) < n:
        nm = r.choice(SURNAMES) + r.choice(GIVEN)
        if nm not in seen or len(seen) > 800:
            seen.add(nm)
            out.append(nm)
    return out


def order_lines(start='2024-01-01', end='2024-03-31', scale=1.0, offset=0):
    """訂單明細：一列＝一筆訂單中的一個品項。"""
    r = rng(10 + offset)
    daily = daily_sales(start, end)
    menu = MENU.set_index('品項代碼')
    rows = []
    oid = 0
    for _, d in daily.iterrows():
        cups_target = int(d['杯數'] * scale)
        base_w = item_weights(d['最高溫'], d['日期'], d['門市代碼'])
        cat = MENU.set_index('品項代碼').loc[base_w.index, '類別']
        slot_w = {}
        for slot, boost in SLOT_BOOST.items():
            w2 = base_w * cat.map(boost).fillna(1.0).values
            slot_w[slot] = w2 / w2.sum()
        hours = np.array(HOUR_PROFILE[d['門市代碼']], float)
        hours /= hours.sum()
        sp = sweet_probs(d['門市代碼'])
        cups = 0
        while cups < cups_target:
            oid += 1
            hour = 10 + r.choice(13, p=hours)
            ts = d['日期'] + pd.Timedelta(hours=int(hour), minutes=int(r.integers(0, 60)), seconds=int(r.integers(0, 60)))
            member = 'Y' if r.random() < 0.42 else 'N'
            pay = r.choice(PAYMENTS, p=STORE_PAY_P[d['門市代碼']])
            wts = slot_w[slot_of(hour)]
            lines_p = LINES_P[d['門市代碼']]
            if member == 'Y':                                  # 會員比較會一次多點幾杯
                lines_p = [lines_p[0] - 0.12, lines_p[1] + 0.07, lines_p[2] + 0.05]
            for _ in range(1 + r.choice(3, p=lines_p)):
                code = r.choice(wts.index, p=wts.values)
                qty = 1 + r.choice(3, p=[0.70, 0.22, 0.08] if member == 'Y' else [0.80, 0.16, 0.04])
                size = '大' if r.random() < LARGE_P[d['門市代碼']] else '中'
                price = int(menu.loc[code, '中杯價'] + (LARGE_EXTRA if size == '大' else 0))
                if code == '008':
                    ice = '熱'
                elif code == '007':
                    ice = '正常冰'
                else:
                    hot_p = 0.25 if d['最高溫'] < 20 else 0.03
                    ice = r.choice(ICE, p=[(1 - hot_p) * x for x in [0.38, 0.27, 0.15, 0.20]] + [hot_p])
                sweet = r.choice(SWEETNESS, p=sp)
                rows.append((f'T{ts:%y%m%d}{oid:06d}', ts, d['門市代碼'], d['門市'], code, menu.loc[code, '品項'],
                             menu.loc[code, '類別'], size, sweet, ice, int(qty), price, int(qty) * price, member, pay))
                cups += qty
    return pd.DataFrame(rows, columns=['訂單編號', '訂單時間', '門市代碼', '門市', '品項代碼', '品項', '類別', '尺寸',
                                       '甜度', '冰塊', '數量', '單價', '金額', '會員', '付款方式'])


def expected_items(daily):
    """依每日氣溫把杯數分配到各品項。"""
    r = rng(31)
    rows = []
    for _, d in daily.iterrows():
        w = item_weights(d['最高溫'], d['日期'], d['門市代碼'])
        noise = r.lognormal(0, 0.12, len(w))                         # 每天每個品項的自然波動
        rows.append((d['日期'], d['門市'], *(np.round(w.values * noise * d['杯數']).astype(int))))
    return pd.DataFrame(rows, columns=['日期', '門市', *MENU.set_index('品項代碼').loc[w.index, '品項']])
