"""產生各章「學生素材」：模擬資料、情境範例 Notebook，並打包成 {章節}_學生素材.zip。

用法（在專案根目錄執行）：
    python tools/build_student_materials.py                     # 全部章節：重新產生資料與 Notebook，並打包
    python tools/build_student_materials.py 檔案存取             # 只產生指定章節
    python tools/build_student_materials.py --zip-only          # 不重新產生，只把現有「學生素材」重新打包
                                                                #（例如執行 Notebook 存入輸出結果之後）

注意：超過 1MB 的模擬資料不放進 git（見 .gitignore），但都包含在 zip 中。
從 git clone 下來後若要使用 --zip-only，請先執行一次完整產生（固定亂數種子，內容不變）。

需要套件：pandas、numpy、nbformat、openpyxl
"""
import importlib
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent / 'materials'))

from nbtools import build_zip, save_notebook  # noqa: E402

# 章節資料夾 → (產生器模組, 要一併放進壓縮檔的課程原始資料)
CHAPTERS = {
    '檔案存取': ('ch02_files', ['個股日成交資訊.csv', '各鄉鎮市區人口密度.csv', '新北市公共自行車租賃系統.json',
                            '新北市食品工廠清冊.csv', '新北市食品工廠清冊.json', 'data.txt', 'data1.txt', 'score.json']),
    '繪圖和視覺展示': ('ch03_plot', ['考試分數_3年6班.csv']),
    'Numpy建立與計算': ('ch04_numpy', []),
    '初見pandas': ('ch05_pandas_intro', ['各鄉鎮市區人口密度.csv', '新北市公共自行車租賃系統.json', '新北市食品工廠清冊.csv']),
    'pandas的基礎功能': ('ch06_pandas_basic', ['各鄉鎮市區人口密度.csv', '上市公司資料.csv', '各班圖書借閱統計.csv', 'weather.csv']),
    'pandas的檔案存取': ('ch07_pandas_io', ['ex1.csv', 'ex2.csv', 'ex3.txt', 'ex4.csv', 'ex5.csv', 'ex6.csv', 'ex7.csv',
                                       'csv_mindex.csv', 'example.json', 'ex1.xlsx', '總統.xls', '個股日成交資訊.csv',
                                       '空氣品質指標.csv']),
    '資料整理和使用前準備': ('ch08_cleaning', ['各鄉鎮市區人口密度.csv']),
    '數據整理_連接_合併_重塑': ('ch09_merge', ['各鄉鎮市區人口密度.csv', '歷年國內主要觀光遊憩據點遊客人數月別統計.csv',
                                        '台鐵車站資訊.csv', 'macrodata.csv']),
    '視覺化表格': ('ch10_style', []),
    '群組資料和群組運算': ('ch11_groupby', ['tips.csv', '各鄉鎮市區人口密度.csv']),
    '直接使用pandas繪制圖表': ('ch12_pandas_plot', ['tips.csv', 'spx.csv']),
    '日期和時間': ('ch13_datetime', ['stock_px_2.csv']),
    '看懂資料與選對圖表': ('ch15_choose_chart', []),
    '全方面分析': ('ch14_capstone', ['每日各站進出站人數2023.csv', '站點2023年進出分析.ipynb']),
}


def readme_text(chapter, notebook, extras):
    lines = [
        f'茶語時光｜{chapter} 學生素材',
        '=' * 40,
        '',
        '【使用方式】',
        f'1. 解壓縮後，用 Jupyter / VS Code 開啟「{notebook}」，從上到下依序執行。',
        '2. 或在 Colab 開啟範例 Notebook，第一格程式會自動下載這個壓縮檔。',
        '3. 資料檔請和 Notebook 放在同一個資料夾。',
        '',
        '【說明】',
        '「茶語時光」是課程虛構的手搖飲品牌，範例資料為模擬資料；',
        '節日與颱風假的日期參考台灣實際情況。',
    ]
    if extras:
        lines += ['', '【課程原始資料】', '「課程原始資料」資料夾內是本章課堂 Notebook 使用的原始檔案：']
        lines += [f'  - {p}' for p in extras]
    return '\r\n'.join(lines) + '\r\n'


def build(chapter):
    module_name, extras = CHAPTERS[chapter]
    chapter_dir = ROOT / chapter
    material_dir = chapter_dir / '學生素材'
    if material_dir.exists():
        shutil.rmtree(material_dir)
    material_dir.mkdir()
    module = importlib.import_module(module_name)
    notebook, files, cells = module.build(material_dir)
    if hasattr(module, 'build_lesson'):              # 有些章節也一併產生課堂 Notebook（README.ipynb）
        module.build_lesson(chapter_dir)
    save_notebook(cells, material_dir / notebook)
    def exists(f):                                   # 素材在「學生素材」或「課程原始資料」（章節資料夾）中
        if f.startswith('課程原始資料/'):
            return f.split('/', 1)[1] in extras and (chapter_dir / f.split('/', 1)[1]).exists()
        return (material_dir / f).exists()
    missing = [f for f in files if not exists(f)]
    assert not missing, f'{chapter} 缺少素材檔：{missing}'
    out = build_zip(chapter_dir, material_dir, extras, readme_text(chapter, notebook, extras))
    print(f'✅ {chapter}: {notebook}，素材 {len(files)} 個，壓縮檔 {out.stat().st_size / 1024:.0f} KB')


def rezip(chapter):
    _, extras = CHAPTERS[chapter]
    chapter_dir = ROOT / chapter
    material_dir = chapter_dir / '學生素材'
    notebook = next(p.name for p in material_dir.glob('*.ipynb'))
    out = build_zip(chapter_dir, material_dir, extras, readme_text(chapter, notebook, extras))
    print(f'📦 {chapter}: 重新打包 {out.stat().st_size / 1024:.0f} KB')


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    for ch in (args or CHAPTERS):
        rezip(ch) if '--zip-only' in sys.argv else build(ch)
