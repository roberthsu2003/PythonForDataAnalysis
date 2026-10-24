"""第 2 章 檔案存取：用純 Python 讀寫真實的政府開放資料——Big5 編碼的 CSV、文字檔與 JSON。"""
from nbtools import md, code, setup_cell, header, exercises, copy_real, latest

CHAPTER = '檔案存取'
NOTEBOOK = '範例_YouBike與電影票房_讀懂政府開放資料.ipynb'
SOURCES = ['youbike', 'boxoffice']


def build(out):
    files = [copy_real(out, 'youbike'), copy_real(out, 'boxoffice')]
    desc = [(files[0], '臺北市 YouBike 每月騎乘次數（2020 年 11 月起；**Big5 編碼**，直接打開會亂碼！）'),
            (files[1], '文化部全國電影票房（2016 年至今、7,000 多部電影，JSON 格式）')]

    cells = [
        header(CHAPTER, NOTEBOOK, '🚲 YouBike 與電影票房：用 Python 讀懂真實的政府開放資料',
               '你在市政府實習，主管丟給你兩份從**政府資料開放平台**下載的檔案：一份是臺北市 YouBike 每個月被騎了幾次，'
               '一份是全台灣每一部電影賣了多少票房。第一份一打開就是亂碼，第二份是一大坨 JSON。'
               '今天的任務是：**不用 Excel，只用 Python 內建功能把它們讀懂，回答「YouBike 騎乘量變幾倍了？」和「台灣人最愛看哪部電影？」**',
               desc, SOURCES),
        setup_cell(CHAPTER, files),
        md('''
## 任務 1：打開就是亂碼！先搞定編碼

**你想知道**：政府的 CSV 為什麼常常打開是亂碼？要怎麼救？

**白話說明**：電腦存中文時要選一本「翻譯字典」（編碼）。台灣很多政府系統還在用舊的 **Big5（cp950）**，新系統用 **UTF-8**。用錯字典讀，Python 會直接報錯 `UnicodeDecodeError`。我們用 `try / except`：先試 UTF-8，失敗就換 cp950。
'''),
        code('''
path = '臺北市YouBike每月使用量.csv'

try:
    with open(path, encoding='utf-8') as f:     # 先用 UTF-8 試試看
        text = f.read()
except UnicodeDecodeError as e:
    print('❌ 用 UTF-8 讀失敗：', e)
    with open(path, encoding='cp950') as f:     # 換成 Big5（cp950）
        text = f.read()
    print('✅ 改用 cp950 成功！')

print(text[:200])                               # 印出前 200 個字確認
'''),
        code('''
# 轉存成 UTF-8：之後所有程式都用 UTF-8 讀，再也不會亂碼
with open('YouBike_utf8.csv', 'w', encoding='utf-8', newline='') as f:
    f.write(text)
print('已另存為 YouBike_utf8.csv')
'''),
        md('''
> 💡 **看懂結果**：錯誤訊息說「`0xa5` 這個位元組不是合法的 UTF-8」——這就是 Big5 檔案的典型症狀。以後看到 `UnicodeDecodeError`，第一個念頭就是「換 `cp950` 試試」。
>
> 🤖 **換你問 AI**：「我從政府資料開放平台下載的 CSV 用 UTF-8 打開是亂碼，可能是 Big5。請寫一段 Python 自動嘗試 utf-8、utf-8-sig、cp950，成功後轉存成 UTF-8。」
'''),
        md('''
## 任務 2：YouBike 騎乘量，這幾年變幾倍了？

**你想知道**：每一年總共被騎了幾次？哪一個月最多人騎？

**白話說明**：`csv.DictReader` 會把第一列當欄位名稱，每一列變成一個字典。⚠️ CSV 讀進來的數字都是**文字**，要先用 `int()` 轉成數字才能相加。
'''),
        code('''
import csv

COUNT = '臺北市YouBike每月使用量（次數）'           # 欄位名稱很長，先存成變數

rows = []
with open('YouBike_utf8.csv', encoding='utf-8') as f:
    for row in csv.DictReader(f):                  # 每一列：{'西元年': '2021', '月份': '1', ...}
        row[COUNT] = int(row[COUNT])               # 文字 → 數字
        rows.append(row)

yearly = {}                                        # 用字典累加：{'2021': 27537119, ...}
for r in rows:
    yearly[r['西元年']] = yearly.get(r['西元年'], 0) + r[COUNT]

for year, total in yearly.items():
    months = sum(1 for r in rows if r['西元年'] == year)
    print(f'{year} 年：{total:>12,} 次（{months} 個月的資料）')

best = max(rows, key=lambda r: r[COUNT])           # 找出次數最多的那一列
print(f"\\n🏆 史上最多人騎的月份：{best['西元年']} 年 {best['月份']} 月，{best[COUNT]:,} 次")
'''),
        md('''
> 💡 **看懂結果**：2021 年約 2,750 萬次，2025 年接近 8,000 萬次——**四年變成將近 3 倍**！這段期間正是 YouBike 2.0 全面上路、站點大量增加的時候。
>
> ⚠️ **小心陷阱**：2020 年只有 11、12 兩個月、今年也還沒過完——**資料月份不一樣多，就不能直接比「年總數」**。報告時一定要註明。
>
> 🤖 **換你問 AI**：「這是一份 CSV 的前 5 行（貼上），請用 Python 內建的 csv 模組依年份加總次數，並找出次數最多的月份。」
'''),
        md('''
## 任務 3：把結果寫成文字報告

**你想知道**：主管說「整理成一份文字檔給我，我要貼到週報裡」。

**白話說明**：`open(檔名, 'w')` 是**寫入模式**（檔案存在會被覆蓋）；`f.write()` 不會自動換行，要自己加 `\\n`。
'''),
        code('''
with open('YouBike年度報告.txt', 'w', encoding='utf-8') as f:
    f.write('臺北市 YouBike 年度騎乘次數\\n')
    f.write('=' * 24 + '\\n')
    for year, total in yearly.items():
        f.write(f'{year} 年  {total:>12,} 次\\n')
    f.write('\\n資料來源：政府資料開放平台（臺北市政府交通局）\\n')

print(open('YouBike年度報告.txt', encoding='utf-8').read())
'''),
        latest('''
import urllib.request
url = 'https://data.taipei/api/dataset/d8cefb03-aba2-41ca-9996-d8774313cdc6/resource/8f690548-61bc-4bff-8baa-01d465eb672c/download'
urllib.request.urlretrieve(url, '臺北市YouBike每月使用量.csv')   # 下載後，從任務 1 重新執行即可
'''),
        md('''
## 任務 4：台灣人最愛看哪部電影？——讀取 JSON

**你想知道**：2016 年到現在，票房最高的電影是哪幾部？

**白話說明**：JSON 就像一層一層的資料夾。先用 `json.load` 讀進來，再看最外層有哪些「鍵」，找到真正的資料在哪一層：這份檔案的電影清單在 `data['List']`。

> ⚠️ 這個 JSON 檔開頭有一個看不見的 BOM 標記，所以編碼要用 `utf-8-sig`（多了 `-sig`），不然會報錯。
'''),
        code('''
import json

with open('全國電影票房_2016至今.json', encoding='utf-8-sig') as f:
    data = json.load(f)                            # JSON → Python 的字典與清單

print('最外層的鍵：', list(data.keys()))
movies = data['List']                              # 真正的電影清單
print('電影數量：', len(movies))
print('第一部電影長這樣：', movies[0])
'''),
        code('''
top = sorted(movies, key=lambda m: m['TotalAmounts'], reverse=True)[:10]   # 依總票房由高到低，取前 10

print('🎬 2016 年至今台灣票房前 10 名')
for i, m in enumerate(top, 1):
    print(f"{i:>2}. {m['Name']}（{m['Country']}，{m['ReleaseDate'][:4]}）  {m['TotalAmounts'] / 1e8:.2f} 億元")
'''),
        md('''
> 💡 **看懂結果**：第一名是《復仇者聯盟：終局之戰》（9.1 億），緊追在後的是 2025 年的《鬼滅之刃 無限城篇》。前 10 名幾乎都是美國和日本片——但 2025 年的國片《陽光女子合唱團》也擠進來了！
>
> 🤖 **換你問 AI**：「這是一份 JSON 的前 30 行（貼上），請告訴我電影清單在哪一層，並用 Python 依 TotalAmounts 排序列出前 10 名。」
'''),
        md('''
## 任務 5：把「2025 年賣座前 10 名」存成 JSON，交給做網站的同學

**你想知道**：網站要放一個「年度賣座排行榜」，工程師說給他 JSON 就好。
'''),
        code('''
top2025 = sorted([m for m in movies if m['ReleaseDate'].startswith('2025')],
                 key=lambda m: m['TotalAmounts'], reverse=True)[:10]

result = [{'名次': i, '片名': m['Name'], '國別': m['Country'], '票房(億)': round(m['TotalAmounts'] / 1e8, 2)}
          for i, m in enumerate(top2025, 1)]

with open('2025賣座前10名.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)   # ensure_ascii=False：中文正常顯示；indent=2：排版好讀

print(open('2025賣座前10名.json', encoding='utf-8').read()[:400])
'''),
        md('''
> 💡 **看懂結果**：2025 年前 3 名是日本動畫、國片、美國動畫——三個不同國家的電影輪流稱王。你也可以把年份改成自己出生的那一年看看。
'''),
    ] + exercises(
        dict(title='2023 年，臺北市 YouBike 總共被騎了幾次？',
             hint='任務 2 已經算好 `yearly` 字典了，鍵是**文字**的年份，例如 `yearly[\'2021\']`。',
             starter='''
rides_2023 = yearly[___]
print(f'2023 年：{rides_2023:,} 次')
''',
             check='''
check('rides_2023', sum(r[COUNT] for r in rows if r['西元年'] == '2023'))
''',
             solution='''
rides_2023 = yearly['2023']
print(f'2023 年：{rides_2023:,} 次')
'''),
        dict(title='國片加油！票房破 1 億元的台灣電影有幾部？',
             hint='台灣電影的 `Country` 是 `\'中華民國\'`；1 億可以寫成 `1e8` 或 `100_000_000`。用串列生成式把兩個條件用 `and` 接起來。',
             starter='''
tw_hits = [m for m in movies if m['Country'] == ___ and m['TotalAmounts'] >= ___]
print('破億國片：', len(tw_hits), '部')
for m in sorted(tw_hits, key=lambda m: m['TotalAmounts'], reverse=True)[:5]:
    print(' ', m['Name'], round(m['TotalAmounts'] / 1e8, 2), '億')
''',
             check='''
check('tw_hits', [m for m in movies if m['Country'] == '中華民國' and m['TotalAmounts'] >= 1e8])
''',
             solution='''
tw_hits = [m for m in movies if m['Country'] == '中華民國' and m['TotalAmounts'] >= 1e8]
print('破億國片：', len(tw_hits), '部')
for m in sorted(tw_hits, key=lambda m: m['TotalAmounts'], reverse=True)[:5]:
    print(' ', m['Name'], round(m['TotalAmounts'] / 1e8, 2), '億')
'''),
        dict(title='檔案不存在也不要當機：用 `try / except` 印出友善訊息',
             hint='打開不存在的檔案會丟出 `FileNotFoundError`，把它寫在 `except` 後面。執行後應該只看到「找不到檔案，請確認檔名」。',
             starter='''
try:
    with open('新北市YouBike每月使用量.csv', encoding='utf-8') as f:
        print(f.read())
except ___:                                        # 要攔下哪一種錯誤？
    print('找不到檔案，請確認檔名')
''',
             solution='''
try:
    with open('新北市YouBike每月使用量.csv', encoding='utf-8') as f:
        print(f.read())
except FileNotFoundError:
    print('找不到檔案，請確認檔名')
'''),
    )
    return NOTEBOOK, files, cells
