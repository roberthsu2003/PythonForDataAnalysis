"""產生學生範例 Notebook 與打包素材的共用工具。"""
import os
import re
import zipfile
from pathlib import Path
from urllib.parse import quote

import nbformat

REPO_RAW = 'https://github.com/roberthsu2003/PythonForDataAnalysis/raw/master/'
REPO_BLOB = 'https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/'


def zip_name(chapter):
    return f'{chapter}_學生素材.zip'


def zip_url(chapter):
    return REPO_RAW + quote(f'{chapter}/{zip_name(chapter)}')


def colab_url(chapter, notebook):
    return REPO_BLOB + quote(f'{chapter}/學生素材/{notebook}')


def md(text):
    return nbformat.v4.new_markdown_cell(text.strip('\n'))


def code(text):
    return nbformat.v4.new_code_cell(text.strip('\n'))


def setup_cell(chapter, files):
    files_repr = ',\n    '.join(repr(f) for f in files)
    return code(f'''
# 📦 準備素材：在 Colab 開啟時，自動下載本章素材壓縮檔並解壓縮
#    （若是在自己電腦解壓縮後開啟，檔案已經在旁邊，會直接使用）
import os, zipfile, urllib.request

FILES = [
    {files_repr},
]
ZIP_URL = '{zip_url(chapter)}'

if not all(os.path.exists(f) for f in FILES):
    urllib.request.urlretrieve(ZIP_URL, 'materials.zip')            # 下載本章素材壓縮檔
    with zipfile.ZipFile('materials.zip') as z:
        for name in z.namelist():
            inner = name.split('/', 1)[1] if '/' in name else name   # 去掉壓縮檔最外層的資料夾名稱
            if inner and not name.endswith('/'):
                os.makedirs(os.path.dirname(inner) or '.', exist_ok=True)
                with z.open(name) as src, open(inner, 'wb') as dst:
                    dst.write(src.read())

print('✅ 素材準備完成：', [f for f in FILES if os.path.exists(f)])
''')


def font_cell():
    return code('''
# --- 設定 Matplotlib 中文字型支援（Mac / Windows / Colab 通用）---
%pip install -q mplfonts

import glob, os
import mplfonts
from matplotlib import font_manager
from mplfonts import use_font

for f in glob.glob(os.path.join(os.path.dirname(mplfonts.__file__), "fonts", "*.[ot]tf")):
    font_manager.fontManager.addfont(f)   # 直接註冊 mplfonts 內附的字型，不改任何檔案
use_font("Noto Sans CJK SC")              # 套用思源黑體，負號也會一起處理
''')


def header(chapter, notebook, title, story, files_desc):
    badge = f'[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({colab_url(chapter, notebook)})'
    rows = '\n'.join(f'| `{f}` | {d} |' for f, d in files_desc)
    return md(f'''
{badge}

# {title}

> 🧋 **情境**：{story}

| 素材檔案 | 內容 |
| --- | --- |
{rows}

> ⚠️ 「茶語時光」是課程虛構的品牌，資料為模擬資料；節日與颱風假的日期參考台灣實際情況，方便你對照生活經驗。
''')


def checker_cell():
    """練習檢查小幫手：在 Colab 會折疊成一行標題，學生只要執行、不用讀懂。"""
    cell = code('''
# @title 🧰 練習檢查小幫手（執行一次就好，不用看懂裡面的程式）
import math
import numpy as np
import pandas as pd


def _same(ans, expected, ordered=False):
    if isinstance(expected, (pd.DataFrame, pd.Series)):
        if type(ans) is not type(expected):
            return False
        try:
            assert_equal = pd.testing.assert_frame_equal if isinstance(expected, pd.DataFrame) else pd.testing.assert_series_equal
            if not ordered:
                ans, expected = ans.sort_index(), expected.sort_index()
            assert_equal(ans, expected, check_names=False, check_dtype=False,
                         check_index_type=False, check_exact=False, rtol=1e-3, atol=0.06,
                         **({'check_column_type': False} if isinstance(expected, pd.DataFrame) else {}))
            return True
        except (AssertionError, TypeError, ValueError):
            return False
    if isinstance(expected, np.ndarray):
        return np.asarray(ans).shape == expected.shape and np.allclose(np.asarray(ans, dtype=float), expected, atol=0.06)
    if isinstance(expected, (int, float, np.number)) and not isinstance(expected, bool):
        try:
            return math.isclose(float(ans), float(expected), rel_tol=1e-3, abs_tol=0.06)
        except (TypeError, ValueError):
            return False
    if isinstance(expected, (list, tuple, set)):
        return list(ans) == list(expected) if not isinstance(expected, set) else set(ans) == expected
    return ans == expected


def check(name, expected, ordered=False):
    """比對學生的變數 name 和正確答案 expected，印出 ✅ 或 ❌；ordered=True 時連排列順序也要一樣。"""
    if name not in globals():
        print(f'⏳ 還找不到變數 {name}：請先把上一格的 ___ 填好並執行')
        return
    ans = globals()[name]
    if _same(ans, expected, ordered):
        print(f'✅ {name} 答對了！')
        return
    print(f'❌ {name} 還不對，再檢查看看：')
    if type(ans) is not type(expected):
        print(f'   型態不同：你的是 {type(ans).__name__}，應該是 {type(expected).__name__}')
    elif hasattr(expected, 'shape') and getattr(ans, 'shape', None) != expected.shape:
        print(f'   大小不同：你的是 {ans.shape}，應該是 {expected.shape}')
    else:
        print('   型態和大小都對了，是數值' + ('或排列順序' if ordered else '') + '不一樣——檢查一下篩選條件或計算方式')


print('🧰 檢查小幫手準備好了：每題寫完後，執行下方的「✅ 檢查」格')
''')
    cell.metadata['cellView'] = 'form'
    return cell


def exercise(no, title, starter, check=None, solution='', hint=None):
    """一題練習：題目（含提示）→ 半成品程式 → ✅ 自動檢查 → 折疊的參考解答。

    starter 用 ___ 標示要填的空格；check 是一段算出正確答案並呼叫 check(變數名稱, 答案) 的程式。
    """
    hint_md = f'\n\n<details><summary>💡 卡住了？點我看提示</summary>\n\n{hint.strip()}\n\n</details>' if hint else ''
    starter_cell = code(f'# ✏️ 練習 {no}：把 ___ 換成正確的程式，再按執行\n{starter.strip()}')
    starter_cell.metadata['tags'] = ['raises-exception']   # 空格還沒填時會出錯，自動檢查時允許這一格出錯
    cells = [md(f'### ✍️ 練習 {no}：{title.strip()}{hint_md}'), starter_cell]
    if check:
        check_cell = code(f'# @title ✅ 執行這格，檢查練習 {no}\n{check.strip()}')
        check_cell.metadata['cellView'] = 'form'
        cells.append(check_cell)
    if solution:
        cells.append(md(f'''<details><summary>🔑 先自己試試看！真的想不出來再點開參考解答</summary>

```python
{solution.strip()}
```

</details>'''))
    return cells


def exercises(*items):
    """練習區：標題 + 檢查小幫手 + 每一題（item 是 exercise() 的參數字典）。"""
    cells = [md('''
---

## ✍️ 換你動手：練習區

每一題都有三格：**① 半成品程式**（把 `___` 換成正確的程式）→ **② ✅ 檢查格**（自動告訴你對不對）→ **③ 🔑 參考解答**（折疊起來，先自己試）。

> 看到 `NameError: name '___' is not defined` 不用緊張，那代表還有空格沒填。
'''), checker_cell()]
    for i, item in enumerate(items, 1):
        cells += exercise(i, **item)
    return cells


def _task_titles(cells):
    titles = []
    for c in cells:
        if c.cell_type == 'markdown':
            m = re.match(r'##\s+(任務\s*\d+|第\s*\d+\s*步|Step\s*\d+)[：:]\s*(.+)', c.source)
            if m:
                titles.append((m.group(1), m.group(2).splitlines()[0].strip()))
    return titles


def finalize(cells):
    """在情境說明後加上「今日任務地圖」，在最後加上「完成清單」，讓學生看得到進度與成果。"""
    titles = _task_titles(cells)
    if not titles:
        return cells
    plan = '\n'.join(f'| ⬜ {label} | {t} |' for label, t in titles)
    roadmap = md(f'''
## 🗺️ 今日任務地圖

| 關卡 | 要回答的問題 |
| --- | --- |
{plan}

**怎麼用這本 Notebook**：從上到下按 `Shift + Enter` 一格一格執行。每個任務都會先講「老闆想知道什麼」，再給程式，最後用 💡 **看懂結果** 告訴你這個數字代表什麼。
''')
    done = '\n'.join(f'- ✅ {label}：{t}' for label, t in titles)
    finale = md(f'''
---

## 🏆 任務完成！今天你用程式做到了這些事

{done}

> 🎯 **帶走一句話**：程式只是工具，真正有價值的是你從資料裡找到的那句「所以我們應該……」。
> 把上面每個 💡 **看懂結果** 用自己的話寫成一句建議，就是一份可以交給老闆的報告。
''')
    first_code = next((i for i, c in enumerate(cells) if c.cell_type == 'code'), 1)
    return cells[:first_code] + [roadmap] + cells[first_code:] + [finale]


def save_notebook(cells, path):
    nb = nbformat.v4.new_notebook()
    nb.cells = cells
    nb.metadata = {
        'kernelspec': {'name': 'python3', 'display_name': 'Python 3', 'language': 'python'},
        'language_info': {'name': 'python'},
        'colab': {'provenance': []},
    }
    nbformat.write(nb, str(path))


def build_zip(chapter_dir, material_dir, extra_files, readme_text):
    """把學生素材資料夾與課程原始資料打包成 {章節}_學生素材.zip。"""
    chapter = chapter_dir.name
    root = f'{chapter}_學生素材'
    out = chapter_dir / zip_name(chapter)
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr(f'{root}/讀我.txt', readme_text)
        for p in sorted(material_dir.rglob('*')):
            if p.is_file() and not p.name.startswith('.') and '.ipynb_checkpoints' not in p.parts:
                z.write(p, f'{root}/{p.relative_to(material_dir).as_posix()}')
        for p in extra_files:
            z.write(chapter_dir / p, f'{root}/課程原始資料/{p}')
    return out
