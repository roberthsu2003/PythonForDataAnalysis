"""第 2 章 檔案存取：純 Python 讀寫 TXT、CSV、JSON 與編碼問題。"""
import csv
import json

from common import MENU, STORES, LARGE_EXTRA, rng
from nbtools import md, code, setup_cell, header

CHAPTER = '檔案存取'
NOTEBOOK = '範例_茶語時光_顧客評論與菜單檔案.ipynb'

GOOD = ['珍珠QQ的，甜度剛好', '店員很親切，還記得我的甜度', '鮮奶很濃，值得這個價錢', '出餐很快，下班買剛好',
        '芋頭鮮奶料超多，會回購', '冬瓜檸檬很解渴', '四季春很香，無糖也好喝', '外送送到還是冰的', '黑糖珍珠鮮奶是我的最愛']
MID = ['味道普通，價格有點高', '排隊排很久，但飲料還可以', '冰塊有點多', '珍珠今天偏硬', '假日人太多，座位不夠']
BAD = ['半糖還是太甜了', '等了快 30 分鐘才拿到', '飲料灑出來，杯子沒封好', '點無糖卻做成全糖，太甜',
       '店員態度很差', '外送超時一小時，冰塊都融了', '珍珠沒煮熟']


def build(out):
    r = rng(20)
    # 1) 菜單.csv
    with open(out / '菜單.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['品項代碼', '品項', '類別', '中杯價', '大杯價', '成本'])
        for _, m in MENU.iterrows():
            w.writerow([m['品項代碼'], m['品項'], m['類別'], m['中杯價'], m['中杯價'] + LARGE_EXTRA, m['成本']])

    # 2) 門市資訊.json（像 API 回傳的巢狀結構）
    hot = {'S01': ['鮮奶綠', '四季春青茶'], 'S02': ['珍珠奶茶', '芒果冰沙'], 'S03': ['黑糖珍珠鮮奶', '珍珠奶茶'],
           'S04': ['珍珠奶茶', '冬瓜檸檬'], 'S05': ['多多綠', '芋頭鮮奶']}
    stores = []
    for _, s in STORES.iterrows():
        stores.append({
            '門市代碼': s['門市代碼'], '門市': s['門市'], '縣市': s['縣市'], '開幕日': s['開幕日'],
            '營業時間': {'平日': '10:00-22:00', '假日': '10:00-23:00' if s['門市代碼'] in ('S02', 'S03') else '10:00-22:00'},
            '外送': s['門市代碼'] != 'S04',
            '熱銷品項': hot[s['門市代碼']],
        })
    data = {'status': 'success', 'updated': '2024-04-01 09:00', 'result': {'count': len(stores), 'stores': stores}}
    (out / '門市資訊.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

    # 3) 顧客評論.txt：日期|門市|星等|評論
    lines = []
    star_bias = {'S01': 4.3, 'S02': 3.6, 'S03': 4.0, 'S04': 4.4, 'S05': 3.8}
    for i in range(120):
        s = STORES.iloc[r.integers(0, 5)]
        star = int(min(5, max(1, round(r.normal(star_bias[s['門市代碼']], 1.0)))))
        text = r.choice(GOOD if star >= 4 else MID if star == 3 else BAD)
        day = f'2024-03-{1 + i % 31:02d}'
        lines.append(f'{day}|{s["門市"]}|{star}|{text}')
    (out / '顧客評論.txt').write_text('# 茶語時光 2024 年 3 月顧客評論（格式：日期|門市|星等|評論）\n' + '\n'.join(lines) + '\n',
                                    encoding='utf-8')

    # 4) 舊系統會員_big5.csv：用 Big5（cp950）編碼，示範亂碼問題
    names = ['陳怡君', '林家豪', '黃雅婷', '張志明', '李淑芬', '王冠宇', '吳宜庭', '劉俊傑']
    with open(out / '舊系統會員_big5.csv', 'w', newline='', encoding='cp950') as f:
        w = csv.writer(f)
        w.writerow(['會員編號', '姓名', '常去門市', '累積點數'])
        for i, n in enumerate(names, 1):
            w.writerow([f'M{i:04d}', n, STORES.iloc[i % 5]['門市'], int(r.integers(20, 900))])

    files = ['菜單.csv', '門市資訊.json', '顧客評論.txt', '舊系統會員_big5.csv']
    desc = [('菜單.csv', '10 個品項的價格與成本'), ('門市資訊.json', '5 家門市的營業時間、外送、熱銷品項（巢狀 JSON）'),
            ('顧客評論.txt', '3 月份 120 則顧客評論'), ('舊系統會員_big5.csv', '舊 POS 系統匯出的會員檔（Big5 編碼，會亂碼！）')]

    cells = [
        header(CHAPTER, NOTEBOOK, '🧋 茶語時光：用 Python 讀懂顧客評論與菜單檔案',
               '你是「茶語時光」總部新來的資料小幫手。店長丟給你一堆檔案：一份顧客評論文字檔、一份菜單 CSV、'
               '一份門市資訊 JSON，還有一份從舊電腦匯出、打開全是亂碼的會員名單。今天的任務是：**不用 Excel，用 Python 把這些檔案讀懂、整理好、再存成店長要的檔案。**',
               desc),
        setup_cell(CHAPTER, files),
        md('''
## 任務 1：顧客到底滿不滿意？——讀取文字檔

**老闆的問題**：「3 月的評論有幾則？平均幾顆星？有多少人抱怨『太甜』？把一、二星的負評整理給我。」

**白話說明**：用 `with open()` 打開文字檔，一行一行讀進來；每一行用 `|` 切開，就能拿到日期、門市、星等、評論。
'''),
        code('''
reviews = []                                          # 準備一個空清單，裝每一則評論
with open('顧客評論.txt', 'r', encoding='utf-8') as f:  # 用 UTF-8 打開文字檔
    for line in f:                                    # 一次讀一行
        line = line.strip()                           # 去掉頭尾空白與換行
        if not line or line.startswith('#'):          # 空行或 # 開頭的說明行就跳過
            continue
        date, store, star, text = line.split('|')     # 用 | 切成四個欄位
        reviews.append({'日期': date, '門市': store, '星等': int(star), '評論': text})

print('評論總數：', len(reviews))
print('平均星等：', round(sum(r['星等'] for r in reviews) / len(reviews), 2))
print('提到「甜」的評論：', sum('甜' in r['評論'] for r in reviews), '則')
print('第一則評論：', reviews[0])
'''),
        code('''
# 把一、二星的負評寫成新的文字檔，交給店長
bad = [r for r in reviews if r['星等'] <= 2]           # 篩出星等 ≤ 2 的評論
with open('負評整理.txt', 'w', encoding='utf-8') as f:   # 'w' 寫入模式：建立新檔（已存在會覆蓋）
    f.write(f'3 月負評共 {len(bad)} 則\\n')
    for r in bad:
        f.write(f"{r['日期']}  {r['門市']}  {r['星等']}★  {r['評論']}\\n")

print(open('負評整理.txt', encoding='utf-8').read()[:300])   # 印出前 300 個字確認內容
'''),
        md('''
> 💡 **看懂結果**：負評集中在「太甜（甜度做錯）」、「等太久」、「外送超時」、「服務態度」幾類——把負評分類統計，就是店長下週開會的討論重點。
>
> 🤖 **換你問 AI**：「我有一個文字檔，每行格式是『日期|門市|星等|評論』，請用 Python 內建的 open 讀取，統計每家門市的評論數與平均星等，並把 1～2 星的評論另存成文字檔。」
'''),
        md('''
## 任務 2：哪一杯最賺錢？——讀取 CSV 菜單

**老闆的問題**：「每一杯中杯賣出去，扣掉成本可以賺多少？哪一杯最賺？」

**白話說明**：`csv.DictReader` 會把第一列當欄位名稱，每一列變成一個字典。⚠️ CSV 讀進來的數字都是**文字**，要先用 `int()` 轉成數字才能相減。
'''),
        code('''
import csv

menu = []
with open('菜單.csv', 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f):                     # 每一列變成 {'品項': '珍珠奶茶', '中杯價': '55', ...}
        row['毛利'] = int(row['中杯價']) - int(row['成本'])   # 文字轉數字後再相減
        row['毛利率'] = round(row['毛利'] / int(row['中杯價']) * 100, 1)
        menu.append(row)

for m in sorted(menu, key=lambda m: m['毛利'], reverse=True):   # 依毛利由高到低排序
    print(f"{m['品項']:　<6}  售價 {m['中杯價']:>3}  成本 {m['成本']:>3}  毛利 {m['毛利']:>3}  毛利率 {m['毛利率']}%")
'''),
        md('''
> 💡 **看懂結果**：毛利「金額」最高的是高單價的鮮奶系列，但毛利「率」最高的是成本很低的純茶——**賺得多**和**賺得有效率**是兩件事，報告時要說清楚用哪一個指標。
>
> 🤖 **換你問 AI**：「這是菜單 CSV 的前三行：（貼上），請用 csv 模組計算每個品項的毛利與毛利率，並依毛利率排序。」
'''),
        md('''
## 任務 3：哪些門市有外送？——讀取巢狀 JSON

**老闆的問題**：「幫我列出每家店的假日營業時間、有沒有外送，以及熱銷品項。」

**白話說明**：JSON 就像一層一層的資料夾。先找到真正的資料在哪一層：`data['result']['stores']`。
'''),
        code('''
import json

with open('門市資訊.json', 'r', encoding='utf-8') as f:
    data = json.load(f)                               # JSON 檔 → Python 的字典與清單

print('最外層有哪些鍵：', list(data.keys()))
stores = data['result']['stores']                     # 真正的門市清單在 result → stores 這一層

for s in stores:
    delivery = '✅ 有外送' if s['外送'] else '❌ 無外送'
    print(f"{s['門市']}｜假日 {s['營業時間']['假日']}｜{delivery}｜熱銷：{'、'.join(s['熱銷品項'])}")
'''),
        md('''
> 🤖 **換你問 AI**：「這是一份 JSON 的前 20 行（貼上），請告訴我門市資料在哪一層，並用 Python 列出每家門市的假日營業時間。」
'''),
        md('''
## 任務 4：舊系統的會員檔打開全是亂碼！——處理編碼

**老闆的問題**：「舊電腦匯出的會員名單打開都是怪字，救得回來嗎？」

**白話說明**：台灣舊系統常用 **Big5（cp950）** 編碼，新系統用 **UTF-8**。用錯「翻譯字典」就會亂碼或直接報錯。我們用 `try / except`：先試 UTF-8，失敗就改用 cp950。
'''),
        code('''
def read_text_any(path):
    """先用 UTF-8 讀，失敗就改用 Big5（cp950）。"""
    for enc in ['utf-8', 'cp950']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read(), enc
        except UnicodeDecodeError:                    # 解碼失敗：這本字典不對，換下一本
            print(f'用 {enc} 讀取失敗，換下一種編碼…')
    raise ValueError('無法判斷編碼')

text, enc = read_text_any('舊系統會員_big5.csv')
print('成功的編碼：', enc)
print(text)

# 轉存成 UTF-8，之後所有程式都用 UTF-8 讀
with open('會員_utf8.csv', 'w', encoding='utf-8', newline='') as f:
    f.write(text)
print('已另存為 會員_utf8.csv')
'''),
        md('''
> 💡 **看懂結果**：第一次用 UTF-8 讀會失敗，改用 cp950 才成功。轉存成 UTF-8 之後，這份檔案就「修好」了。
>
> 🤖 **換你問 AI**：「我的 CSV 用 UTF-8 打開是亂碼，可能是 Big5 編碼。請寫一段程式自動嘗試 utf-8、utf-8-sig、cp950，成功後轉存成 UTF-8。」
'''),
        md('''
## 任務 5：把整理結果存成 JSON，交給工程師做網站

**老闆的問題**：「官網要顯示每家店的平均評分，工程師說給他 JSON 就好。」
'''),
        code('''
import json

summary = {}
for r in reviews:                                     # 依門市累加星等與評論數
    s = summary.setdefault(r['門市'], {'評論數': 0, '星等總和': 0})
    s['評論數'] += 1
    s['星等總和'] += r['星等']

result = [{'門市': name, '評論數': s['評論數'], '平均星等': round(s['星等總和'] / s['評論數'], 2)}
          for name, s in summary.items()]
result.sort(key=lambda x: x['平均星等'], reverse=True)

with open('門市評分.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)   # ensure_ascii=False：中文正常顯示；indent=2：排版好讀

print(open('門市評分.json', encoding='utf-8').read())
'''),
        md('''
> 💡 **看懂結果**：評分最低的是高雄巨蛋店與台北西門店，剛好都是人潮會突然爆量的門市（演唱會散場、觀光客）。人多時的出餐速度與服務品質，值得優先改善。

---

## ✍️ 練習題

1. 從 `reviews` 找出「台南成大店」的所有評論，並計算它的平均星等。
2. 把菜單中「中杯價 ≥ 60 元」的品項，存成新的 `高價品項.csv`（要有標題列）。
3. 試著打開一個不存在的檔案 `四月評論.txt`，用 `try / except FileNotFoundError` 印出「找不到檔案，請確認檔名」。
'''),
        md('## 🔑 參考解答（先自己試試看！）'),
        code('''
# 練習 1
tainan = [r for r in reviews if r['門市'] == '台南成大店']
print('台南成大店評論數：', len(tainan), '平均星等：', round(sum(r['星等'] for r in tainan) / len(tainan), 2))

# 練習 2
with open('高價品項.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['品項', '中杯價'])
    for m in menu:
        if int(m['中杯價']) >= 60:
            w.writerow([m['品項'], m['中杯價']])
print(open('高價品項.csv', encoding='utf-8').read())

# 練習 3
try:
    with open('四月評論.txt', encoding='utf-8') as f:
        print(f.read())
except FileNotFoundError:
    print('找不到檔案，請確認檔名')
'''),
    ]
    return NOTEBOOK, files, cells
