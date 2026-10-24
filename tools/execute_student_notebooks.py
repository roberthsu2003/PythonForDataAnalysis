"""執行各章「學生素材」範例 Notebook，把輸出結果存回檔案（學生在 GitHub 上就看得到表格與圖）。

用法（在專案根目錄執行）：
    python tools/execute_student_notebooks.py               # 全部章節：執行並存入輸出
    python tools/execute_student_notebooks.py 初見pandas     # 只執行指定章節
    python tools/execute_student_notebooks.py --verify      # 不存檔：把參考解答填進練習格，確認每個 ✅ 檢查都通過

存檔時，練習區的「半成品」與「✅ 檢查」格不保留輸出，學生打開時看到的是乾淨的空格。
執行完記得重新打包：python tools/build_student_materials.py --zip-only

需要套件：nbclient、nbformat、ipykernel，以及範例用到的 pandas、matplotlib、seaborn、mplfonts 等。
"""
import re
import shutil
import sys
import tempfile
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_student_materials import CHAPTERS  # noqa: E402

SOLUTION = re.compile(r'```python\n(.*?)\n```', re.S)


def is_starter(cell):
    return cell.cell_type == 'code' and cell.source.startswith('# ✏️ 練習')


def is_check(cell):
    return cell.cell_type == 'code' and cell.source.startswith('# @title ✅')


def fill_solutions(nb):
    """把每一題的參考解答（折疊的 markdown）放進前面的半成品格。"""
    starter = None
    for cell in nb.cells:
        if is_starter(cell):
            starter = cell
        elif cell.cell_type == 'markdown' and '🔑' in cell.source and starter is not None:
            starter.source = SOLUTION.search(cell.source).group(1)
            starter = None


def run(chapter, verify):
    material = ROOT / chapter / '學生素材'
    path = next(material.glob('*.ipynb'))
    nb = nbformat.read(path, as_version=4)
    if verify:
        fill_solutions(nb)
    with tempfile.TemporaryDirectory() as tmp:          # 在暫存資料夾執行，Notebook 寫出的檔案不會留在 repo
        work = Path(tmp) / 'work'
        shutil.copytree(material, work)
        for extra in CHAPTERS[chapter][1]:                # 課程原始資料（例如期末實戰用的站點資料）
            if (ROOT / chapter / extra).exists():
                (work / '課程原始資料').mkdir(exist_ok=True)
                shutil.copy(ROOT / chapter / extra, work / '課程原始資料' / extra)
        NotebookClient(nb, timeout=600, kernel_name='python3',
                       resources={'metadata': {'path': str(work)}}).execute()
    if verify:
        results = [''.join(o.get('text', '') for o in c.outputs if o.output_type == 'stream') for c in nb.cells if is_check(c)]
        bad = [r for r in results if '✅' not in r or '❌' in r or '⏳' in r]
        print(f"{'✅' if not bad else '❌'} {chapter}: {len(results)} 個檢查格" + (f'，未通過：{bad}' if bad else ''))
        return not bad
    for cell in nb.cells:
        cell.metadata.pop('execution', None)               # 執行時間戳記：不需要，避免每次重跑都產生差異
        if is_starter(cell) or is_check(cell) or cell.source.startswith('# --- 設定 Matplotlib 中文字型'):
            cell.outputs, cell.execution_count = [], None   # 練習格保持乾淨；字型設定格的安裝訊息對學生沒有意義
    nbformat.write(nb, str(path))
    print(f'💾 {chapter}: 已存入輸出 {path.name}')
    return True


if __name__ == '__main__':
    verify = '--verify' in sys.argv
    chapters = [a for a in sys.argv[1:] if not a.startswith('--')] or list(CHAPTERS)
    ok = all([run(ch, verify) for ch in chapters])
    sys.exit(0 if ok else 1)
