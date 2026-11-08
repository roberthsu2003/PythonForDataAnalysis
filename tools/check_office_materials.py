"""從交付的 Excel 與 Notebook 執行每個參考解法，不連網、不改教材。"""
import contextlib
import io
import json
import os
import shutil
import tempfile
from pathlib import Path

os.environ.setdefault('MPLBACKEND', 'Agg')
os.environ.setdefault('MPLCONFIGDIR', '/tmp/office-matplotlib')
from openpyxl import load_workbook
from build_office_materials import CASES, DEST


def verify():
    original = Path.cwd()
    with tempfile.TemporaryDirectory(prefix='office-check-') as work:
        work = Path(work)
        try:
            os.chdir(work)
            for c in CASES:
                source = DEST / f"{c['name']}.xlsx"
                shutil.copy2(source, work / source.name)
                wb = load_workbook(source, data_only=True, read_only=True)
                assert wb.sheetnames == [s['name'] for s in c['sheets']]
                for s in c['sheets']:
                    actual = [list(r) for r in wb[s['name']].iter_rows(values_only=True)]
                    assert actual == [s['headers']] + s['rows'], c['name']
                wb.close()
                nb = json.loads((DEST / f"{c['name']}.ipynb").read_text())
                scope = {'__name__': '__main__'}
                with contextlib.redirect_stdout(io.StringIO()):
                    for cell in nb['cells']:
                        if cell['cell_type'] == 'code' and not cell['source'].startswith('%pip'):
                            exec(compile(cell['source'], str(source), 'exec'), scope)
                print(f"通過：{c['name']}")
        finally:
            os.chdir(original)
    print('12 份 Excel 原始值與所有參考解法、驗收斷言均通過。')


if __name__ == '__main__':
    verify()
