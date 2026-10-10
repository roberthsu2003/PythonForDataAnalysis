"""產生學生範例 Notebook 與打包素材的共用工具。"""
import os
import zipfile
from pathlib import Path
from urllib.parse import quote

import nbformat

REPO_RAW = 'https://github.com/roberthsu2003/PythonForDataAnalysis/raw/master/'
REPO_BLOB = 'https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/'
FONT_URL = REPO_RAW + quote('繪圖和視覺展示/ChineseFont.ttf')


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
    return code(f'''
# 🈶 設定圖表中文字型（避免中文變成方塊）
import os, urllib.request
import matplotlib.pyplot as plt
from matplotlib import font_manager

def setup_chinese_font():
    installed = {{f.name for f in font_manager.fontManager.ttflist}}
    for name in ['Noto Sans CJK TC', 'Microsoft JhengHei', 'PingFang TC', 'Heiti TC', 'Arial Unicode MS']:
        if name in installed:                       # 電腦裡已經有中文字型就直接用
            plt.rcParams['font.sans-serif'] = [name]
            break
    else:                                           # 沒有（例如 Colab）就下載課程提供的字型
        path = 'ChineseFont.ttf'
        if not os.path.exists(path):
            urllib.request.urlretrieve('{FONT_URL}', path)
        font_manager.fontManager.addfont(path)
        plt.rcParams['font.sans-serif'] = [font_manager.FontProperties(fname=path).get_name()]
    plt.rcParams['axes.unicode_minus'] = False      # 負號正常顯示

setup_chinese_font()
print('✅ 中文字型設定完成：', plt.rcParams['font.sans-serif'][0])
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
