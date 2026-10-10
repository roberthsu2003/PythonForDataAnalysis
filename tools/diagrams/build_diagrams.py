"""產生各章 README「資料長什麼樣子？」的 SVG 圖解，並可替換 README 中的文字圖。

用法（在專案根目錄執行）：
    python tools/diagrams/build_diagrams.py            # 產生全部 SVG 到各章的「圖解」資料夾
"""
from pathlib import Path

from svgkit import C, Canvas, tw

ROOT = Path(__file__).resolve().parents[2]
DIAGRAMS = []          # (章節, README 中第幾個文字圖, 檔名, 標題, 函式)


def diagram(chapter, idx, name, title):
    def deco(fn):
        DIAGRAMS.append((chapter, idx, name, title, fn))
        return fn
    return deco


def mono_box(c, x, y, lines, size=14, line_h=24, fill='#F8FAFC', notes=None, w=None):
    """等寬字的「檔案內容」框；notes = {行號: (說明, 顏色)}。回傳 (寬, 高)。"""
    w = w or max(tw(l, size, mono=True) for l in lines) + 30
    h = len(lines) * line_h + 18
    c.rect(x, y, w, h, fill=fill, stroke=C['line'], rx=8)
    for i, l in enumerate(lines):
        color = C['muted'] if l.lstrip().startswith('#') else C['ink']
        c.text(x + 14, y + 12 + line_h * (i + 0.75), l, size, color, mono=True)
        if notes and i in notes:
            txt, col = notes[i]
            c.note(x + w + 14, y + 12 + line_h * (i + 0.75), txt, col)
    return w, h


# ───────────────────────── 檔案存取 ─────────────────────────
@diagram('檔案存取', 1, 'csv轉二維清單', 'CSV 純文字讀成二維清單')
def d_csv(c):
    c.tag(24, 22, '處理前：students.csv（純文字檔）', 'grey')
    w, h = mono_box(c, 24, 58, ['編號,國文,英文,數學', '01,87,90,56', '02,98,56,78'], size=15, line_h=28)
    c.note(32, 58 + h + 24, '第一列是標題列', C['muted'], icon='▲')
    c.arrow(24 + w + 16, 58 + h / 2, 24 + w + 116, 58 + h / 2, label='csv.reader')
    x2 = 24 + w + 134
    c.tag(x2, 22, '處理後：Python 的二維清單（list）', 'blue')
    mono_box(c, x2, 58, ["[['編號','國文','英文','數學'],", " ['01','87','90','56'],", " ['02','98','56','78']]"],
             size=15, line_h=28, fill=C['blue_l'])
    c.note(x2 + 8, 58 + h + 24, "注意：'87' 有引號——讀進來的全部都是文字，計算前要先轉成數字！", C['red'])


@diagram('檔案存取', 2, 'json巢狀結構', 'JSON 一層一層取出資料')
def d_json(c):
    c.tag(24, 22, '新北市食品工廠清冊.json', 'grey')
    lines = ['{', '  "success": true,', '  "result": {', '    "records": [', '      {"Name_Ins": "鴻輝食品廠", ...},',
             '      {"Name_Ins": "廣達香食品…", ...}', '    ]', '  }', '}']
    w, h = mono_box(c, 24, 58, lines, size=14, line_h=25,
                    notes={1: ('第 1 層：下載狀態', C['muted']), 2: ('第 1 層：結果資料夾', C['amber']),
                           3: ('第 2 層：真正的資料在這裡！', C['red'])})
    c.rect(34, 58 + 12 + 25 * 4 - 2, w - 20, 25 * 2 + 4, fill='none', stroke=C['red'], rx=6, sw=1.8, dash='5 4')
    y = 58 + h + 18
    c.arrow(160, y, 160, y + 50, label="data['result']['records']", mono=True)
    y += 66
    c.tag(24, y, '取出的結果：一筆一個字典的清單', 'blue')
    for i, s in enumerate(['工廠 1', '工廠 2', '工廠 3', '…']):
        c.rect(24 + i * 104, y + 38, 92, 40, fill=C['blue_l'] if s != '…' else 'none', stroke=C['blue'] if s != '…' else 'none', rx=8)
        c.text(70 + i * 104, y + 64, s if s == '…' else '{' + s + '}', 14, C['navy'], 'bold', 'middle')
    c.note(450, y + 64, '一列一筆，可以開始分析了', C['green'])


# ───────────────────────── 繪圖和視覺展示 ─────────────────────────
@diagram('繪圖和視覺展示', 1, '圖表組成元素', 'Matplotlib 圖表的組成：Figure、Axes 與元素')
def d_fig(c):
    c.rect(24, 24, 800, 400, fill='#FAFAF9', stroke=C['brown'], rx=12, sw=2)
    c.tag(40, 36, 'Figure（整張畫布）', 'brown')
    c.rect(60, 78, 480, 326, fill=C['bg'], stroke=C['blue'], rx=10, sw=2)
    c.tag(76, 90, 'Axes（畫框）', 'blue')
    c.text(300, 140, 'Fruit Sales', 17, C['ink'], 'bold', 'middle')
    ox, oy, k = 140, 345, 150 / 9000                  # 座標原點與「每 1 元幾像素」
    c.line(ox, oy, 510, oy, C['ink'], 1.5)
    c.line(ox, 175, ox, oy, C['ink'], 1.5)
    for v in (3000, 6000, 9000):
        yy = oy - v * k
        c.line(ox - 5, yy, ox, yy, C['ink'])
        c.text(ox - 9, yy + 5, v, 12, C['muted'], anchor='end')
    for i, (name, a, b) in enumerate([('apple', 3000, 4000), ('banana', 6000, 7000), ('orange', 4000, 8500)]):
        bx = 175 + i * 110
        c.rect(bx, oy - a * k, 30, a * k, fill=C['brown'], stroke='none', rx=2)
        c.rect(bx + 34, oy - b * k, 30, b * k, fill='#D6B48C', stroke='none', rx=2)
        c.text(bx + 32, oy + 22, name, 13, C['ink'], anchor='middle')
    c.rect(400, 160, 14, 14, fill=C['brown'], stroke='none', rx=2)
    c.text(420, 172, '2024', 12)
    c.rect(460, 160, 14, 14, fill='#D6B48C', stroke='none', rx=2)
    c.text(480, 172, '2025', 12)
    for (bx, by), n in [((375, 135), '1'), ((432, 145), '2'), ((86, 250), '3'), ((222, 262), '4'), ((300, 392), '5')]:
        c.badge(bx, by, n)
    items = [('標題', 'set_title()'), ('圖例', 'legend()'), ('Y 軸刻度', 'set_yticks()'),
             ('資料（長條）', 'bar()'), ('X 軸標籤', 'set_xticks()')]
    for i, (name, fn) in enumerate(items):
        y = 125 + i * 48
        c.badge(575, y, str(i + 1))
        c.text(596, y + 5, name, 15, C['ink'], 'bold')
        c.text(700, y + 5, fn, 13, C['blue'], mono=True)
    c.text(565, 385, '一張 Figure 可以放好幾個 Axes', 13, C['muted'])


@diagram('繪圖和視覺展示', 2, '數字對應座標軸', '兩串數字畫成折線圖')
def d_line(c):
    c.tag(24, 22, '處理前：兩串數字', 'grey')
    c.text(24, 86, 'X（日期） = [1,  2,  3,  4,  5]', 15, mono=True)
    c.text(24, 120, 'Y（營收） = [12, 22, 25, 20, 18]', 15, mono=True)
    c.note(24, 160, '兩串的筆數必須一樣多', C['red'])
    c.arrow(330, 100, 420, 100, label='plt.plot(X, Y)', mono=True)
    c.tag(440, 22, '處理後：折線圖', 'blue')
    ox, oy, sx, sy = 480, 250, 52, 7
    c.line(ox, oy, ox + 290, oy, C['ink'], 1.5)
    c.line(ox, 60, ox, oy, C['ink'], 1.5)
    xs, ys = [1, 2, 3, 4, 5], [12, 22, 25, 20, 18]
    pts = [(ox + x * sx, oy - (y - 5) * sy) for x, y in zip(xs, ys)]
    c.el.append('<polyline points="' + ' '.join(f'{x:.0f},{y:.0f}' for x, y in pts) +
                f'" fill="none" stroke="{C["blue"]}" stroke-width="2.5"/>')
    for (px, py), x, y in zip(pts, xs, ys):
        c.circle(px, py, 5, C['blue'])
        c.text(px, py - 12, y, 12, C['navy'], 'bold', 'middle')
        c.text(px, oy + 20, x, 12, C['muted'], anchor='middle')
    c.text(ox + 300, oy + 5, 'X', 13, C['muted'])
    c.text(ox - 6, 55, 'Y', 13, C['muted'], anchor='end')


# ───────────────────────── NumPy ─────────────────────────
@diagram('Numpy建立與計算', 1, 'reshape重排', 'reshape：一維陣列重排成 3 列 × 4 欄')
def d_reshape(c):
    c.tag(24, 22, '處理前：一維陣列（12 個數字排成一長條）', 'grey')
    c.code(370, 20, 'shape = (12,)')
    for i in range(12):
        c.rect(24 + i * 46, 62, 42, 42, fill=C['brown_l'], stroke=C['brown'], rx=6)
        c.text(45 + i * 46, 89, i, 16, C['brown'], 'bold', 'middle')
    c.arrow(160, 120, 160, 180, label='reshape((3, 4))：重新排成 3 列 × 4 欄', mono=False)
    c.tag(24, 196, '處理後：二維陣列（像一張 Excel 表）', 'blue')
    c.code(330, 194, 'shape = (3, 4)')
    for j in range(4):
        c.text(110 + j * 56, 254, f'欄{j}', 13, C['muted'], 'bold', 'middle')
    for i in range(3):
        c.text(56, 290 + i * 50, f'列{i}', 13, C['muted'], 'bold', 'end')
        for j in range(4):
            c.rect(86 + j * 56, 266 + i * 50, 48, 42, fill=C['blue_l'], stroke=C['blue'], rx=6)
            c.text(110 + j * 56, 293 + i * 50, i * 4 + j, 16, C['navy'], 'bold', 'middle')
    c.note(330, 300, '總數不變：12 = 3 × 4', C['green'])
    c.note(330, 330, '形狀對不上（例如 5 × 3）就會出錯', C['red'])


@diagram('Numpy建立與計算', 2, 'axis方向', 'axis=0 直著算、axis=1 橫著算')
def d_axis(c):
    w, h, xs, ys = c.table(60, 30, ['國文', '英文', '數學'], [[80, 90, 70], [60, 75, 95]], index=['小明', '小華'],
                           widths=[70, 78, 78, 78], row_h=40, size=16)
    for y, total, name in zip(ys, [240, 230], ['小明', '小華']):
        c.arrow(60 + w + 10, y, 60 + w + 90, y, C['green'])
        c.text(60 + w + 102, y + 6, f'{name}總分 {total}', 15, C['green'], 'bold')
    for x, total in zip(xs[1:], [140, 165, 165]):
        c.arrow(x, 30 + h + 8, x, 30 + h + 58, C['blue'])
        c.rect(x - 32, 30 + h + 64, 64, 34, fill=C['blue_l'], stroke='none', rx=6)
        c.text(x, 30 + h + 87, total, 16, C['navy'], 'bold', 'middle')
    c.tag(xs[-1] + 52, 30 + h + 66, 'axis=0：直著算 → 每一科一個答案', 'blue')
    c.tag(60 + w + 10, 2 + 30 - 24 + 4, 'axis=1：橫著算 → 每一列（每個人）一個答案', 'green')


# ───────────────────────── 初見 pandas ─────────────────────────
@diagram('初見pandas', 1, 'Series結構', 'Series：一欄有名牌的資料')
def d_series(c):
    w, h, xs, ys = c.table(24, 30, ['values（值）'], [[35000], [71000], [16000], [5000]],
                           index=['台北', '桃園', '台中', '高雄'], index_name='index（名牌）', row_h=38, size=16,
                           index_tone='bold')
    c.note(24 + w + 24, ys[0] + 5, "用名牌查詢：pop['桃園'] → 71000", C['blue'])
    c.note(24 + w + 24, ys[2] + 5, '整欄一起運算：pop * 1.05', C['green'])


@diagram('初見pandas', 2, '字典變DataFrame', 'Python 字典轉成 DataFrame 並新增欄位')
def d_df(c):
    c.tag(24, 22, '處理前：Python 字典（每個 key 是一欄）', 'grey')
    mono_box(c, 24, 58, ["{ '縣市': ['台北','台北','新竹'],", "  '年份': [2000, 2001, 2001],", "  '人口': [2.2, 2.5, 1.1] }"], size=14)
    c.arrow(200, 166, 200, 216)
    c.code(216, 178, 'pd.DataFrame(data)')
    c.text(410, 197, '＋ 新增「新開發區」欄', 14, C['green'], 'bold')
    c.tag(24, 230, '處理後：DataFrame（像 Excel 工作表）', 'blue')
    w, h, xs, ys = c.table(60, 268, ['縣市', '年份', '人口', '新開發區'],
                           [['台北', 2000, 2.2, 'False'], ['台北', 2001, 2.5, 'False'], ['新竹', 2001, 1.1, 'True']],
                           index=['0', '1', '2'], row_h=36, size=15,
                           styles={(0, 3): 'green', (1, 3): 'green', (2, 3): 'green'})
    c.note(60 + w + 20, 268 + 23, '← columns（欄名）', C['blue'])
    c.note(60 + w + 20, 268 + 23 + 36 * 3, '新欄位：縣市 == 新竹', C['green'])
    c.note(24, 268 + h + 30, 'index（列名牌）：沒指定時自動從 0 開始編號', C['muted'], icon='▲')


@diagram('初見pandas', 3, '索引對齊', '兩個 Series 依名牌配對相加，配不到就是 NaN')
def d_align(c):
    wa, h, _, _ = c.table(24, 50, ['人口 A'], [[35000], [71000], [5000]], index=['台北', '桃園', '高雄'], row_h=36, size=15,
                          styles={(1, 0): 'amber'})
    c.text(24 + wa + 20, 50 + h / 2 + 8, '+', 26, C['ink'], 'bold', 'middle')
    x2 = 24 + wa + 40
    wb, _, _, _ = c.table(x2, 50, ['人口 B'], [[35000], ['NaN'], [5000]], index=['台北', '花蓮', '高雄'], row_h=36, size=15,
                          styles={(1, 0): 'amber', (1, -1): 'amber'})
    c.text(x2 + wb + 20, 50 + h / 2 + 8, '=', 26, C['ink'], 'bold', 'middle')
    x3 = x2 + wb + 40
    w3, h3, _, ys = c.table(x3, 50, ['A + B'], [[70000], ['NaN'], ['NaN'], [10000]], index=['台北', '桃園', '花蓮', '高雄'],
                            row_h=36, size=15, styles={(1, 0): 'red', (2, 0): 'red'})
    c.note(x3 + w3 + 16, ys[1] + 5, 'B 沒有桃園', C['red'])
    c.note(x3 + w3 + 16, ys[2] + 5, 'A 沒有花蓮', C['red'])
    c.text(24, 50 + h3 + 34, '依「名牌」配對，不是依位置；任一邊缺少名牌，結果就是 NaN（空值）', 14, C['muted'])


# ───────────────────────── pandas 的基礎功能 ─────────────────────────
@diagram('pandas的基礎功能', 1, 'loc與iloc', 'loc 按名牌、iloc 按位置取資料')
def d_loc(c):
    c.text(30, 74, '位置', 12, C['amber'], 'bold')
    rows = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
    w, h, xs, ys = c.table(70, 50, ['one', 'two', 'three', 'four'], rows, index=['台北', '台中', '台南', '高雄'],
                           index_name='名牌', row_h=36, size=15, styles={(1, 1): 'blue', (1, 2): 'blue', (1, -1): 'blue'})
    for i, y in enumerate(ys):
        c.text(44, y + 5, f'[{i}]', 13, C['amber'], 'bold', 'middle')
    for j, x in enumerate(xs[1:]):
        c.text(x, 40, f'[{j}]', 12, C['amber'], 'bold', 'middle')
    x = 70 + w + 36
    c.code(x, 70, "data.loc['台中', ['two', 'three']]")
    c.text(x + 4, 120, '用名牌（列名、欄名）→ 5, 6', 14, C['blue'], 'bold')
    c.code(x, 150, 'data.iloc[1, [1, 2]]')
    c.text(x + 4, 200, '用位置（第幾列、第幾欄，從 0 開始）→ 5, 6', 14, C['amber'], 'bold')


@diagram('pandas的基礎功能', 2, '排名排序', '成績單：新增總分、排名，再依名次排序')
def d_rank(c):
    c.tag(24, 22, '處理前', 'grey')
    w, h, _, _ = c.table(24, 58, ['國文', '英文', '數學'], [[89, 93, 94], [77, 93, 58], [95, 88, 97]], index=['1', '2', '3'],
                         index_name='學號', row_h=36, size=15)
    c.arrow(24 + w + 16, 58 + h / 2, 24 + w + 126, 58 + h / 2, label='總分 → rank')
    x2 = 24 + w + 144
    c.tag(x2, 22, "處理後：sort_values(by='排名')", 'blue')
    c.table(x2, 58, ['國文', '英文', '數學', '總分', '排名'],
            [[95, 88, 97, 280, '1.0'], [89, 93, 94, 276, '2.0'], [77, 93, 58, 228, '3.0']], index=['3', '1', '2'],
            index_name='學號', row_h=36, size=15,
            styles={(0, 3): 'green', (1, 3): 'green', (2, 3): 'green', (0, 4): 'blue', (1, 4): 'blue', (2, 4): 'blue'})


# ───────────────────────── pandas 的檔案存取 ─────────────────────────
@diagram('pandas的檔案存取', 1, '跳過雜訊讀CSV', '有雜訊的 CSV 用參數讀成乾淨表格')
def d_skiprows(c):
    c.tag(24, 22, '處理前：ex4.csv（原始檔）', 'grey')
    lines = ['# hey!', 'a,b,c,d,message', '# just wanted to make ...', '# who reads CSV files ...', '1,2,3,4,hello',
             '5,6,7,8,world', '9,10,11,12,foo']
    w, h = mono_box(c, 24, 58, lines, size=14, line_h=26,
                    notes={0: ('第 0 行：註解 → 跳過', C['red']), 1: ('第 1 行：標題', C['green']),
                           2: ('第 2 行：註解 → 跳過', C['red']), 3: ('第 3 行：註解 → 跳過', C['red'])})
    y = 58 + h + 20
    c.arrow(140, y, 140, y + 50)
    c.code(160, y + 10, "pd.read_csv('ex4.csv', skiprows=[0, 2, 3])")
    c.tag(24, y + 66, '處理後：DataFrame', 'blue')
    c.table(24, y + 102, ['a', 'b', 'c', 'd', 'message'], [[1, 2, 3, 4, 'hello'], [5, 6, 7, 8, 'world'], [9, 10, 11, 12, 'foo']],
            index=['0', '1', '2'], row_h=34, size=15)


@diagram('pandas的檔案存取', 2, '資料進出口', 'pandas 是資料的轉運站：read_xxx 讀進、to_xxx 輸出')
def d_hub(c):
    ins = ['CSV', 'Excel', 'JSON', 'Web API', 'SQLite']
    outs = [('CSV', 'to_csv'), ('Excel', 'to_excel'), ('JSON', 'to_json'), ('SQLite', 'to_sql')]
    for i, s in enumerate(ins):
        y = 30 + i * 52
        c.rect(24, y, 110, 38, fill=C['head'], stroke=C['line'], rx=8)
        c.text(79, y + 25, s, 15, C['ink'], 'bold', 'middle')
        c.path(f'M134,{y + 19} C190,{y + 19} 190,155 236,155', C['blue'], 1.8)
    c.rect(246, 112, 200, 86, fill=C['blue'], stroke='none', rx=14)
    c.code(250, 70, 'read_xxx()')
    c.code(360, 70, 'to_xxx()')
    c.text(346, 150, 'DataFrame', 20, '#FFFFFF', 'bold', 'middle')
    c.text(346, 178, '篩選、統計、清理', 14, '#DBEAFE', 'normal', 'middle')
    for i, (s, fn) in enumerate(outs):
        y = 56 + i * 52
        c.path(f'M446,155 C500,155 500,{y + 19} 556,{y + 19}', C['green'], 1.8, marker=False)
        c.line(556, y + 19, 566, y + 19, C['green'], 1.8)
        c.rect(570, y, 200, 38, fill=C['green_l'], stroke=C['green'], rx=8)
        c.text(584, y + 25, s, 15, C['green'], 'bold')
        c.text(760, y + 25, fn + '()', 13, C['green'], anchor='end', mono=True)


# ───────────────────────── 資料整理和使用前準備 ─────────────────────────
@diagram('資料整理和使用前準備', 1, '人口密度清理前後', '人口密度 CSV：清理前 vs. 清理後')
def d_clean(c):
    c.tag(24, 22, '處理前：原始檔 376 列，全部都是文字（object）', 'grey')
    rows = [['統計年', '區域別', '年底人口數', '土地面積', '人口密度'], ['106', '新北市板橋區', '551480', '23.1373', '23835'],
            ['…', '…', '…', '…', '…'], ['106', '南沙群島', '… ', '0.5045', '… '], ['NaN', '資料來源說明…', 'NaN', 'NaN', 'NaN']]
    w, h, xs, ys = c.table(24, 58, ['statistic_yyy', 'site_id', 'people_total', 'area', 'population_density'], rows,
                           index=['0', '1', '…', '370', '371'], row_h=34, size=14, ellipsis_row=2,
                           styles={**{(0, j): 'red' for j in range(5)}, (3, 2): 'red', (3, 4): 'red',
                                   **{(4, j): 'red' for j in range(5)}})
    for y, s in [(ys[0], '第二層標題混在資料裡'), (ys[3], '用「… 」代表無資料'), (ys[4], '檔尾說明文字')]:
        c.note(24 + w + 14, y + 5, s, C['red'], icon='✖')
    y = 58 + h + 22
    c.arrow(120, y, 120, y + 48)
    x = 140
    for step in ['rename', 'drop(0)', 'dropna(thresh=4)', "replace('… ', 0)", 'astype']:
        x += c.code(x, y + 8, step, 13) + 8
    c.tag(24, y + 64, '處理後：370 列，數字欄位已轉成數值型態', 'blue')
    c.table(24, y + 100, ['年', '區域', '人口數 (int)', '土地面積 (float)', '人口密度 (float)'],
            [['106', '新北市板橋區', '551480', '23.14', '23835.0'], ['106', '新北市三重區', '387484', '16.32', '23747.0']],
            index=['第1筆', '第2筆'], row_h=34, size=14, styles={(i, j): 'green' for i in range(2) for j in (2, 3, 4)})


# ───────────────────────── 數據整理：連接、合併、重塑 ─────────────────────────
@diagram('數據整理_連接_合併_重塑', 1, 'merge配對', 'merge：用車站代碼把兩張表配對起來')
def d_merge(c):
    c.tag(24, 22, '左表：每日進出站人數', 'grey')
    wl, h, _, _ = c.table(24, 58, ['乘車日', '車站代碼', '進站人數'],
                          [['20220101', '0900', 8645], ['20220101', '0910', 996], ['20220101', '0920', 1369]],
                          row_h=34, size=15, styles={(i, 1): 'amber' for i in range(3)})
    c.text(24 + wl + 30, 58 + h / 2 + 9, '＋', 24, C['ink'], 'bold', 'middle')
    x2 = 24 + wl + 60
    c.tag(x2, 22, '右表：車站基本資料', 'grey')
    c.table(x2, 58, ['車站代碼', '中文站名'], [['0900', '基隆'], ['0910', '三坑'], ['0920', '八堵']], row_h=34, size=15,
            styles={(i, 0): 'amber' for i in range(3)})
    y = 58 + h + 18
    c.arrow(140, y, 140, y + 48)
    c.code(160, y + 10, "pd.merge(左表, 右表, on='車站代碼', how='left')")
    w, h2, _, ys = c.table(24, y + 64, ['乘車日', '車站代碼', '進站人數', '中文站名'],
                           [['20220101', '0900', 8645, '基隆'], ['20220101', '0910', 996, '三坑'], ['20220101', '0920', 1369, '八堵']],
                           row_h=34, size=15, styles={**{(i, 1): 'amber' for i in range(3)}, **{(i, 3): 'green' for i in range(3)}})
    c.note(24 + w + 16, ys[1] + 5, '每一筆紀錄都補上了站名（就像 VLOOKUP）', C['green'])


@diagram('數據整理_連接_合併_重塑', 2, '長表寬表', 'stack / unstack：長表與寬表互換')
def d_stack(c):
    c.tag(24, 22, '長表（一列一筆紀錄，適合電腦處理）', 'grey')
    w, h, _, _ = c.table(24, 58, ['年別', '縣市別', '月份', '遊客數'],
                         [['2012', '南投縣', '1月', '1,499,117'], ['2012', '南投縣', '2月', '1,746,048'],
                          ['2012', '嘉義市', '1月', '91,527'], ['…', '…', '…', '…']], row_h=34, size=15, ellipsis_row=3,
                         styles={(0, 2): 'amber', (1, 2): 'amber', (2, 2): 'amber'})
    x1, x2 = 24 + w + 20, 24 + w + 170
    c.arrow(x1, 58 + h / 2 - 20, x2, 58 + h / 2 - 20, label="unstack('月份')", mono=True)
    c.arrow(x2, 58 + h / 2 + 24, x1, 58 + h / 2 + 24, C['green'])
    c.text((x1 + x2) / 2, 58 + h / 2 + 50, 'stack()', 13, C['green'], 'bold', 'middle', mono=True)
    c.tag(x2 + 18, 22, '寬表（人看的報表）', 'blue')
    c.table(x2 + 18, 58, ['1月', '2月'], [['1,499,117', '1,746,048'], ['91,527', '…']],
            index=['2012 南投縣', '2012 嘉義市'], index_name='年別 縣市別', row_h=34, size=15, header_tone='blue',
            styles={(1, 1): 'muted'})
    c.text(x2 + 18, 58 + 34 * 3 + 30, '「月份」從列搬到欄位上', 13, C['amber'], 'bold')


# ───────────────────────── 視覺化表格 ─────────────────────────
@diagram('視覺化表格', 1, 'Styler化妝前後', 'Styler：同一份資料，化妝前後的差別')
def d_style(c):
    c.tag(24, 22, '處理前：素顏的 DataFrame', 'grey')
    rows = [[85, 45, 92, '1234567.8'], [58, 88, 60, '987654.3'], [90, 72, 55, '456789.1']]
    w, h, _, _ = c.table(24, 58, ['國文', '英文', '數學', '營收'], rows, index=['小明', '小華', '小美'], row_h=36, size=15)
    c.arrow(24 + w + 16, 58 + h / 2, 24 + w + 106, 58 + h / 2, label='df.style', mono=True)
    x2 = 24 + w + 124
    c.tag(x2, 22, '處理後：Styler 化妝後的報表', 'blue')
    rows2 = [[85, 45, 92, '1,234,568'], [58, 88, 60, '987,654'], [90, 72, 55, '456,789']]
    st = {(0, 1): 'redtext', (1, 0): 'redtext', (2, 2): 'redtext', (2, 0): 'strong', (1, 1): 'strong', (0, 2): 'strong'}
    w2, h2, _, _ = c.table(x2, 58, ['國文', '英文', '數學', '營收'], rows2, index=['小明', '小華', '小美'], row_h=36, size=15, styles=st)
    y = 58 + h2 + 34
    c.note(x2, y, '紅字 = 不及格（自訂規則 map）', C['red'])
    c.note(x2, y + 26, '深藍底 = 每科最高分（highlight_max）', C['navy'])
    c.note(x2, y + 52, '營收 = 千分位、無小數（format）', C['green'])


# ───────────────────────── 群組資料和群組運算 ─────────────────────────
@diagram('群組資料和群組運算', 1, '分組計算合併', 'Split → Apply → Combine：依區域統計車位與故障數')
def d_groupby(c):
    c.tag(24, 22, '原始資料（一列一個站點）', 'grey')
    w, h, _, ys = c.table(24, 58, ['站名', '區域', '數量', '故障'],
                          [['大鵬華城', '新店區', 38, 0], ['裕隆公園', '新店區', 40, 2], ['汐止火車站', '汐止區', 56, 4],
                           ['汐止區公所', '汐止區', 46, 2]], row_h=34, size=15,
                          styles={**{(i, 1): 'blue' for i in (0, 1)}, **{(i, 1): 'amber' for i in (2, 3)}})
    x = 24 + w + 24
    for k, (title, tone) in enumerate([('① Split 分組', 'grey'), ('② Apply 計算', 'grey'), ('③ Combine 合併', 'grey')]):
        c.tag(x + k * 190, 22, title, tone)
    for i, (area, n, tot, bad, fill, stroke) in enumerate([('新店區', 2, 78, 2, C['blue_l'], C['blue']),
                                                            ('汐止區', 2, 102, 6, C['amber_l'], C['amber'])]):
        y = 66 + i * 76
        c.arrow(x - 18, ys[i * 2] + 17, x - 2, y + 26, C['muted'], 1.6)
        c.rect(x, y, 150, 52, fill=fill, stroke=stroke, rx=8)
        c.text(x + 75, y + 32, f'{area}：{n} 站', 15, stroke, 'bold', 'middle')
        c.arrow(x + 154, y + 26, x + 186, y + 26, C['muted'], 1.6)
        c.rect(x + 190, y, 150, 52, fill=fill, stroke=stroke, rx=8)
        c.text(x + 265, y + 22, f'數量加總 {tot}', 14, stroke, 'bold', 'middle')
        c.text(x + 265, y + 42, f'故障加總 {bad}', 14, stroke, 'bold', 'middle')
        c.arrow(x + 344, y + 26, x + 376, y + 26, C['muted'], 1.6)
    c.table(x + 380, 66, ['數量', '故障', '故障率'], [[78, 2, '2.56%'], [102, 6, '5.88%']], index=['新店區', '汐止區'],
            index_name='區域', row_h=40, size=15, index_tone='bold', styles={(0, 2): 'green', (1, 2): 'red'})
    c.note(x, 236, '比率要「先加總、再相除」：故障率 = 故障加總 ÷ 數量加總', C['red'])


# ───────────────────────── 直接使用 pandas 繪製圖表 ─────────────────────────
@diagram('直接使用pandas繪制圖表', 1, '交叉表到長條圖', '原始紀錄 → 交叉表 → 百分比表 → 長條圖')
def d_crosstab(c):
    c.tag(24, 22, '① 原始資料（一列一筆帳單）', 'grey')
    w1, h, _, _ = c.table(24, 58, ['day', 'size', 'tip'], [['Sun', 2, '1.01'], ['Sun', 3, '1.66'], ['Sat', 2, '3.50'], ['…', '…', '…']],
                          row_h=32, size=14, ellipsis_row=3)
    c.text(24, 58 + h + 22, '共 244 筆', 13, C['muted'])
    x2 = 24 + w1 + 110
    c.arrow(24 + w1 + 12, 58 + h / 2, x2 - 12, 58 + h / 2, label='crosstab')
    c.tag(x2, 22, '② 交叉表：次數', 'grey')
    w2, _, _, _ = c.table(x2, 58, ['2', '3', '4', '5'], [[16, 1, 1, 0], [53, 18, 13, 1], [39, 15, 18, 3], [48, 4, 5, 1]],
                          index=['Fri', 'Sat', 'Sun', 'Thur'], index_name='day', row_h=32, size=14)
    x3 = x2 + w2 + 110
    c.arrow(x2 + w2 + 12, 58 + h / 2, x3 - 12, 58 + h / 2, label='÷ 每列總數')
    c.tag(x3, 22, '③ 百分比表（每列加總 = 100%）', 'blue')
    w3, h3, _, _ = c.table(x3, 58, ['2', '3', '4', '5'],
                           [['89%', '6%', '6%', '0%'], ['62%', '21%', '15%', '1%'], ['52%', '20%', '24%', '4%'], ['83%', '7%', '9%', '2%']],
                           index=['Fri', 'Sat', 'Sun', 'Thur'], index_name='day', row_h=32, size=14, header_tone='blue')
    y = 58 + h3 + 16
    c.arrow(x3 + w3 / 2, y, x3 + w3 / 2, y + 44, label='.plot.bar()', mono=True)
    data = [[89, 6, 6, 0], [62, 21, 15, 1], [52, 20, 24, 4], [83, 7, 9, 2]]
    colors = [C['brown'], '#C8A27C', '#E8D5B7', '#94A3B8']
    bx, by = x3 + 10, y + 170
    c.line(bx - 6, by, bx + 270, by, C['ink'], 1.2)
    for i, (day, vals) in enumerate(zip(['Fri', 'Sat', 'Sun', 'Thur'], data)):
        for j, v in enumerate(vals):
            c.rect(bx + i * 68 + j * 14, by - v * 1.1, 12, v * 1.1, fill=colors[j], stroke='none', rx=1)
        c.text(bx + i * 68 + 27, by + 18, day, 12, C['muted'], anchor='middle')
    for j, (col, lab) in enumerate(zip(colors, ['2 人', '3 人', '4 人', '5 人'])):
        c.rect(bx + j * 62, by + 32, 12, 12, fill=col, stroke='none', rx=2)
        c.text(bx + j * 62 + 17, by + 43, lab, 12, C['muted'])
    c.text(x3 - 30, y + 110, 'X 軸 = 索引（星期）', 14, C['ink'], 'bold', 'end')
    c.text(x3 - 30, y + 136, '每一欄（用餐人數）= 一種顏色的長條', 14, C['ink'], 'bold', 'end')


# ───────────────────────── 日期和時間 ─────────────────────────
@diagram('日期和時間', 1, '時間當索引', '文字日期轉成時間索引')
def d_dtindex(c):
    c.tag(24, 22, '處理前：日期是一般欄位（文字）', 'grey')
    w, h, _, _ = c.table(24, 58, ['日期', '營收'], [["'2021-01-02'", 120], ["'2021-01-05'", 135], ["'2021-02-09'", 160]],
                         index=['0', '1', '2'], row_h=36, size=15, mono_cols=(0,), styles={(i, 0): 'muted' for i in range(3)})
    c.arrow(24 + w + 16, 58 + h / 2 - 8, 24 + w + 150, 58 + h / 2 - 8, label='to_datetime', mono=True)
    c.text(24 + w + 83, 58 + h / 2 + 22, '+ set_index', 13, C['blue'], 'bold', 'middle', mono=True)
    x2 = 24 + w + 168
    c.tag(x2, 22, '處理後：日期變成時間索引（DatetimeIndex）', 'blue')
    w2, _, _, ys = c.table(x2, 58, ['營收'], [[120], [135], [160]], index=['2021-01-02', '2021-01-05', '2021-02-09'],
                           index_name='日期（索引）', row_h=36, size=15, index_tone='blue', styles={(i, -1): 'blue' for i in range(3)})
    for y, s in zip(ys, ["ts['2021-01'] 取出整個月", '算「星期幾」、「第幾季」', "resample('ME') 彙總成每月"]):
        c.note(x2 + w2 + 16, y + 5, s, C['green'])


@diagram('日期和時間', 2, '降頻與月增率', 'resample 降頻、shift 計算月增率、rolling 移動平均')
def d_resample(c):
    c.tag(24, 22, '① 每日營收（高頻）', 'grey')
    w1, h, _, _ = c.table(24, 58, ['營收'], [[10], [12], ['…'], [9], ['…']], index=['01-01', '01-02', '…', '01-31', '…'],
                          row_h=32, size=14, ellipsis_row=2)
    c.rect(20, 58 + 32 - 2, w1 + 8, 32 * 4 + 4, fill='none', stroke=C['blue'], rx=6, dash='5 4', sw=1.6)
    x2 = 24 + w1 + 230
    c.arrow(24 + w1 + 16, 58 + h / 2, x2 - 14, 58 + h / 2, label="resample('ME').sum()", mono=True)
    c.text(24 + w1 + 16 + (x2 - 30 - w1 - 24) / 2, 58 + h / 2 + 24, '整個月加總成一筆', 12, C['muted'], anchor='middle')
    c.tag(x2, 22, '② 每月營收', 'grey')
    w2, _, _, _ = c.table(x2, 58, ['營收'], [[310], [336], [372]], index=['01-31', '02-28', '03-31'], index_name='月份',
                          row_h=32, size=14)
    x3 = x2 + w2 + 130
    c.arrow(x2 + w2 + 16, 58 + 70, x3 - 14, 58 + 70, label='shift(1)', mono=True)
    c.tag(x3, 22, '③ 對照上月 → 月增率', 'blue')
    c.table(x3, 58, ['營收', '上月', '月增率'], [[310, 'NaN', 'NaN'], [336, 310, '+8.4%'], [372, 336, '+10.7%']],
            index=['01-31', '02-28', '03-31'], index_name='月份', row_h=32, size=14,
            styles={(0, 1): 'muted', (0, 2): 'muted', (1, 2): 'green', (2, 2): 'green', (1, 1): 'amber', (2, 1): 'amber'})
    y = 58 + h + 36
    c.code(24, y, 'rolling(3).mean()')
    c.text(200, y + 20, '每個時間點 = 「自己 + 前 2 個」的平均；前 2 個時間點資料不足，會是 NaN', 14, C['ink'])


# ───────────────────────── 全方面分析 ─────────────────────────
@diagram('全方面分析', 1, '台鐵資料轉換', '台鐵資料：原始欄位轉換成分析用欄位')
def d_tra(c):
    c.tag(24, 22, '原始資料（一列＝某一天、某一站，共 86,609 筆）', 'grey')
    w, h, xs, _ = c.table(24, 58, ['trnOpDate', 'staCode', 'gateInComingCnt', 'gateOutGoingCnt'],
                          [[20230101, 900, 8030, 8241], [20230101, 910, 1017, 1326], ['…', '…', '…', '…']],
                          row_h=34, size=15, ellipsis_row=2, styles={(0, 0): 'amber', (1, 0): 'amber', (0, 1): 'amber', (1, 1): 'amber'})
    c.note(24 + w + 16, 58 + 60, '日期是整數', C['amber'])
    c.note(24 + w + 16, 58 + 90, '代碼不是站名', C['amber'])
    y = 58 + h + 18
    c.arrow(140, y, 140, y + 48)
    c.code(160, y + 10, 'to_datetime ・ 加減運算 ・ dt.dayofweek ・ merge 站名')
    c.tag(24, y + 64, '轉換後（新增分析用欄位）', 'blue')
    w2, h2, _, _ = c.table(24, y + 100, ['日期', '站名', '進站', '出站', '總運量', '淨流量', '星期', '月份'],
                           [['2023-01-01', '基隆', 8030, 8241, 16271, -211, '星期日', 1],
                            ['2023-01-01', '三坑', 1017, 1326, 2343, -309, '星期日', 1]],
                           row_h=34, size=15, styles={**{(i, j): 'green' for i in range(2) for j in (0, 1, 4, 5, 6, 7)}})
    c.text(24, y + 100 + h2 + 30, '總運量 = 進站 + 出站　｜　淨流量 = 進站 − 出站', 14, C['ink'], 'bold')
    c.text(24, y + 100 + h2 + 58, '分析結果：各星期平均運量、每月趨勢、7 日移動平均、運量前 5 名車站（附站名）', 14, C['muted'])


if __name__ == '__main__':
    import sys
    only = sys.argv[1:]
    for chapter, idx, name, title, fn in DIAGRAMS:
        if only and chapter not in only:
            continue
        c = Canvas()
        fn(c)
        out = ROOT / chapter / '圖解' / f'{name}.svg'
        out.parent.mkdir(exist_ok=True)
        out.write_text(c.svg(title), encoding='utf-8')
        print('✅', out.relative_to(ROOT))
