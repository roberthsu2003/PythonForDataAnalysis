"""
檢查各章 Notebook 能否從頭執行到尾。

用法（在 repo 根目錄）：
    python tools/check_notebooks.py                 # 檢查程式碼篇全部章節
    python tools/check_notebooks.py 初見pandas 日期和時間   # 只檢查指定章節

每一章會先複製到暫存資料夾再執行，Notebook 寫出的檔案不會留在 repo 裡。
需要的套件：nbclient、nbformat、ipykernel，以及各章用到的 pandas、matplotlib 等。
"""
import shutil
import sys
import tempfile
import time
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError, CellTimeoutError, DeadKernelError

ROOT = Path(__file__).resolve().parent.parent
CHAPTERS = ['檔案存取', '繪圖和視覺展示', 'Numpy建立與計算', '初見pandas', 'pandas的基礎功能', 'pandas的檔案存取',
            '資料整理和使用前準備', '數據整理_連接_合併_重塑', '視覺化表格', '群組資料和群組運算',
            '直接使用pandas繪制圖表', '日期和時間', '全方面分析', '資料分析範例']

# 課堂 Notebook 中的 input() 在自動檢查時無法輸入：ipykernel 每格執行前都會把 input 指向
# kernel.raw_input，所以直接改寫它，讓它回傳固定答案
SETUP = ("get_ipython().kernel.raw_input = "
         "lambda prompt='', *args, **kwargs: (print(prompt, '→（自動檢查：輸入 1）'), '1')[1]")


def run_notebook(path: Path, timeout: int) -> tuple:
    """回傳（狀態, 說明）；狀態為 OK、ERROR、TIMEOUT"""
    nb = nbformat.read(path, as_version=4)
    nb.cells.insert(0, nbformat.v4.new_code_cell(SETUP))
    client = NotebookClient(nb, timeout=timeout, kernel_name='python3',
                            resources={'metadata': {'path': str(path.parent)}})
    try:
        client.execute()
        return 'OK', ''
    except CellExecutionError as error:
        # 減 1：扣掉最前面自動加入的設定格，讓編號對應原始 Notebook（從 0 起算）
        cell_no = next((i - 1 for i, c in enumerate(nb.cells) if any(o.get('output_type') == 'error' for o in c.get('outputs', []))), None)
        reason = next((f"{o['ename']}: {o['evalue']}" for c in nb.cells for o in c.get('outputs', [])
                       if o.get('output_type') == 'error'), str(error).splitlines()[-1])
        return 'ERROR', f'第 {cell_no} 格（從 0 起算）｜{reason[:300]}'
    except CellTimeoutError:
        return 'TIMEOUT', f'單格執行超過 {timeout} 秒'
    except DeadKernelError as error:
        return 'ERROR', f'Kernel 中止：{error}'


def main(chapters: list, timeout: int = 180) -> int:
    rows = []
    with tempfile.TemporaryDirectory() as tmp:
        for chapter in chapters:
            work = Path(tmp) / chapter
            shutil.copytree(ROOT / chapter, work, ignore=shutil.ignore_patterns('.ipynb_checkpoints', '__pycache__'))
            for nb_path in sorted(work.rglob('*.ipynb')):
                rel = nb_path.relative_to(Path(tmp))
                start = time.time()
                status, detail = run_notebook(nb_path, timeout)
                rows.append((status, str(rel), f'{time.time() - start:.0f}s', detail))
                mark = {'OK': '✅', 'ERROR': '❌', 'TIMEOUT': '⏱️'}[status]
                print(f'{mark} {rel}（{rows[-1][2]}）{detail}', flush=True)
    ok = sum(r[0] == 'OK' for r in rows)
    print(f'\n共 {len(rows)} 本：✅ {ok}　❌ {len(rows) - ok}')
    return 0 if ok == len(rows) else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:] or CHAPTERS))
