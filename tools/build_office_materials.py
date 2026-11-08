"""產生第一階段辦公室教材；Excel 由同目錄 build_office_workbooks.mjs 匯出。

python3 tools/build_office_materials.py
node tools/build_office_workbooks.mjs /tmp/office-materials.json
python3 tools/build_office_materials.py --zip-only
"""
import argparse
import json
import textwrap
import zipfile
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / '第一階段_辦公室Excel實戰'
CASES = []


def case(name, level, department, topic, headers, rows, tasks, rule, code, check, extra=None):
    CASES.append(dict(name=name, level=level, department=department, topic=topic,
                      sheets=[dict(name='資料', headers=headers.split('、'), rows=rows)] + (extra or []),
                      tasks=tasks, rule=rule, code=textwrap.dedent(code).strip(), check=check))


case('01_行政_文具領用', 1, '行政', '讀懂工作表與欄位',
     '領用單號、部門、品項、數量',
     [['A001','行政','原子筆',10],['A002','業務','筆記本',6],['A003','人資','原子筆',8],
      ['A004','行政','資料夾',5],['A005','財務','原子筆',4],['A006','業務','資料夾',7]],
     ['列出工作表名稱、欄位與前 3 筆資料。','說明一列代表一筆領用明細，計算資料筆數。',
      '只列出行政部的領用紀錄。'],
     '單號是文字；數量是件數。不同品項先分開看，不把件數解讀為費用。',
     '''
     print('欄位：', list(rows[0]))
     print('前 3 筆：', rows[:3])
     print('筆數：', len(rows))
     selected = [r for r in rows if r['部門'] == '行政']
     print('行政部：', selected)
     assert len(rows) == 6 and len(selected) == 2
     ''', '6 筆資料；行政部 2 筆，數量分別為 10 與 5。')

case('02_人資_教育訓練名單', 1, '人資', '文字條件篩選與計數',
     '員工編號、姓名、部門、課程、完成狀態',
     [['E001','王小安','業務','資訊安全','完成'],['E002','林小晴','人資','資訊安全','未完成'],
      ['E003','陳小宇','財務','資訊安全','完成'],['E004','李小文','行政','資訊安全','未完成'],
      ['E005','張小玲','業務','資訊安全','完成'],['E006','吳小豪','採購','資訊安全','完成']],
     ['列出員工編號與完成狀態。','篩出未完成人員，保留員工編號、姓名與部門。',
      '計算完成人數與完成率。'],
     '每位員工只有一列，完成率＝完成人數 ÷ 全部員工人數；篩選文字要完全相同。',
     '''
     pending = [r for r in rows if r['完成狀態'] == '未完成']
     completed = sum(r['完成狀態'] == '完成' for r in rows)
     print('待完成：', pending)
     print('完成率：', f'{completed / len(rows):.1%}')
     assert completed == 4 and len(pending) == 2
     ''', '完成 4 人、未完成 2 人；完成率 66.7%，待完成為 E002、E004。')

case('03_財務_費用明細', 1, '財務', '數值加總與條件加總',
     '憑證編號、部門、費用類別、金額_元',
     [['F001','行政','文具',1200],['F002','業務','交通',850],['F003','人資','課程',3000],
      ['F004','行政','郵資',450],['F005','業務','交通',650],['F006','財務','文具',900]],
     ['算出全部費用總額。','只加總業務部費用。','找出最大的一筆費用與憑證編號。'],
     '金額單位為新臺幣元，是已登錄費用；本例不處理稅務與核銷資格。',
     '''
     total = sum(r['金額_元'] for r in rows)
     sales = sum(r['金額_元'] for r in rows if r['部門'] == '業務')
     largest = max(rows, key=lambda r: r['金額_元'])
     print('總額：', total, '業務部：', sales, '最大筆：', largest)
     assert total == 7050 and sales == 1500 and largest['憑證編號'] == 'F003'
     ''', '總額 7,050 元；業務部 1,500 元；最大筆 F003，3,000 元。')

case('04_業務_訂單金額', 2, '業務', '新增計算結果與排序',
     '訂單編號、業務員、商品、單價_元、數量',
     [['S001','王小安','鍵盤',800,3],['S002','林小晴','滑鼠',400,5],
      ['S003','王小安','螢幕',5000,2],['S004','林小晴','鍵盤',800,4],['S005','陳小宇','滑鼠',400,2]],
     ['逐列計算訂單金額＝單價 × 數量。','依訂單金額由大到小排序，列出前 3 筆。',
      '計算全部訂單金額，輸出含計算結果的 CSV。'],
     '一列一張單品訂單；單價為本例約定成交價，不另加稅或運費。',
     '''
     result = [dict(r, 訂單金額_元=r['單價_元'] * r['數量']) for r in rows]
     result.sort(key=lambda r: (-r['訂單金額_元'], r['訂單編號']))
     print('前 3 筆：', result[:3])
     print('總額：', sum(r['訂單金額_元'] for r in result))
     save_csv('訂單金額.csv', result)
     assert sum(r['訂單金額_元'] for r in result) == 18400
     assert [r['訂單編號'] for r in result[:3]] == ['S003', 'S004', 'S001']
     ''', '總額 18,400 元；前三名 S003（10,000）、S004（3,200）、S001（2,400）。')

case('05_倉管_庫存補貨', 2, '倉管', '多條件判斷與差額',
     '商品編號、品名、現有庫存、已訂未到、安全庫存',
     [['P001','影印紙',8,0,20],['P002','碳粉',3,5,6],['P003','資料夾',10,0,10],
      ['P004','原子筆',5,2,15],['P005','筆記本',30,0,20]],
     ['先計算可用量＝現有庫存＋已訂未到。','只挑出可用量低於安全庫存的品項。',
      '建議補貨量＝max(安全庫存－可用量, 0)，輸出補貨清單。'],
     '可用量在本例包含已訂未到；等於安全庫存時不補貨，未考慮交期與最小訂購量。',
     '''
     result = []
     for r in rows:
         available = r['現有庫存'] + r['已訂未到']
         needed = max(r['安全庫存'] - available, 0)
         if needed > 0:
             result.append(dict(r, 可用量=available, 建議補貨量=needed))
     print(result)
     save_csv('補貨清單.csv', result)
     assert [(r['商品編號'], r['建議補貨量']) for r in result] == [('P001',12),('P004',8)]
     ''', '只補 P001 12 件、P004 8 件；P002 已有在途量，P003 等於門檻，皆不補。')

case('06_採購_供應商報價', 2, '採購', '同條件比較與最低值',
     '報價編號、供應商、品項、單價_元、訂購數量、運費_元、交期_天',
     [['Q001','甲供應商','A4影印紙',120,20,200,3],['Q002','乙供應商','A4影印紙',115,20,400,2],
      ['Q003','丙供應商','A4影印紙',125,20,0,5],['Q004','丁供應商','A4影印紙',118,20,180,4]],
     ['計算每筆總成本＝單價 × 訂購數量＋運費。','比較全部報價的最低總成本。',
      '加入交期不超過 3 天的條件，再找最低成本。'],
     '品項規格與數量相同，價格視為含稅；交期是教學約定，成本相同時保留所有並列者。',
     '''
     result = [dict(r, 總成本_元=r['單價_元'] * r['訂購數量'] + r['運費_元']) for r in rows]
     lowest = min(r['總成本_元'] for r in result)
     eligible = [r for r in result if r['交期_天'] <= 3]
     fastest_cost = min(r['總成本_元'] for r in eligible)
     print('全體最低：', [r for r in result if r['總成本_元'] == lowest])
     print('交期內最低：', [r for r in eligible if r['總成本_元'] == fastest_cost])
     assert lowest == 2500 and fastest_cost == 2600
     ''', '全體最低丙供應商 2,500 元；交期 ≤ 3 天時，甲供應商 2,600 元。')

case('07_行政_部門月費用', 3, '行政', 'NumPy 二維陣列與 axis',
     '部門、1月費用_元、2月費用_元、3月費用_元',
     [['行政',12000,10000,14000],['人資',8000,12000,10000],['業務',18000,16000,20000]],
     ['只把三個數值欄轉成 NumPy 陣列，說明 shape。','用 axis=1 算各部門季度總額。',
      '用 axis=0 算各月總額，核對兩種加總的總計。'],
     '每列一個部門、每欄一個月份；費用可跨月加總。部門名稱不能放進數值陣列。',
     '''
     import numpy as np
     a = np.array([[r[k] for k in ['1月費用_元','2月費用_元','3月費用_元']] for r in rows], dtype=float)
     print('shape：', a.shape)
     print('各部門：', a.sum(axis=1))
     print('各月：', a.sum(axis=0))
     assert a.shape == (3,3)
     assert a.sum(axis=1).tolist() == [36000,30000,54000]
     assert a.sum(axis=0).tolist() == [38000,38000,44000]
     assert a.sum() == 120000
     ''', 'shape=(3,3)；部門總額 36,000、30,000、54,000；月總額 38,000、38,000、44,000。')

case('08_人資_訓練滿意度', 3, '人資', '缺值與平均數',
     '回覆編號、部門、課程內容、講師表達、實務幫助',
     [['R001','行政',5,4,5],['R002','業務',4,4,3],['R003','人資',None,5,4],
      ['R004','財務',3,None,4],['R005','採購',4,3,None]],
     ['說明空白與 0 分的差別，列出每題有效回覆數。','用 np.nanmean 算三題平均。',
      '用 np.nanstd 計算母體標準差，說明此處只描述這批回覆。'],
     '評分 1～5 分，空白代表未答；不把缺答補 0；標準差使用 ddof=0。',
     '''
     import numpy as np
     a = np.array([[r[k] if r[k] is not None else np.nan for k in ['課程內容','講師表達','實務幫助']] for r in rows])
     valid = np.sum(~np.isnan(a), axis=0)
     means = np.nanmean(a, axis=0)
     print('有效回覆：', valid, '平均：', means, '標準差：', np.nanstd(a,axis=0))
     assert valid.tolist() == [4,4,4]
     assert np.allclose(means, [4,4,4])
     assert np.allclose(np.nanstd(a,axis=0), [0.70710678]*3)
     ''', '三題各有 4 筆有效回答，平均皆為 4.0，母體標準差皆約 0.7071。')

case('09_客服_案件處理統計', 3, '客服', '分類統計與平均的分母',
     '案件編號、問題類別、狀態、處理分鐘',
     [['C001','配送','已結案',30],['C002','退貨','已結案',50],['C003','配送','處理中',None],
      ['C004','商品','已結案',20],['C005','退貨','已結案',70],['C006','配送','已結案',40]],
     ['按問題類別計算案件數。','只對已結案案件算平均處理分鐘。',
      '計算整體結案率，說明為何未結案不能當作 0 分鐘。'],
     '每列一個案件；未結案的處理分鐘空白；平均耗時的分母只含已結案案件。',
     '''
     from collections import Counter
     import numpy as np
     counts = Counter(r['問題類別'] for r in rows)
     closed = [r for r in rows if r['狀態'] == '已結案']
     mean = np.mean([r['處理分鐘'] for r in closed])
     print('類別件數：', counts, '平均分鐘：', mean, '結案率：', f'{len(closed)/len(rows):.1%}')
     assert dict(counts) == {'配送':3, '退貨':2, '商品':1}
     assert mean == 42 and len(closed) == 5
     ''', '配送 3 件、退貨 2 件、商品 1 件；已結案平均 42 分鐘，結案率 83.3%。')

case('10_業務_月營收趨勢', 4, '業務', '折線圖與月增率',
     '月份、營收_元',
     [['2025-01',100000],['2025-02',120000],['2025-03',90000],['2025-04',150000],
      ['2025-05',160000],['2025-06',180000]],
     ['依月份排序，確認沒有缺月或重複月份。','畫折線圖，標示月份、金額單位與標題。',
      '算 2～6 月月增率，第一個月保留空白。'],
     '月增率＝（本月－上月）÷ 上月；上月若為 0，應標示無法計算；先排序再比較。',
     '''
     import matplotlib.pyplot as plt
     result = sorted(rows, key=lambda r: r['月份'])
     assert [r['月份'] for r in result] == [f'2025-{m:02d}' for m in range(1,7)]
     amounts = [r['營收_元'] for r in result]
     growth = [None] + [(b-a)/a if a != 0 else None for a,b in zip(amounts,amounts[1:])]
     print('月增率：', growth)
     fig, ax = plt.subplots()
     ax.plot([r['月份'] for r in result], amounts, marker='o')
     ax.set(title='Monthly revenue', xlabel='Month', ylabel='Revenue (TWD)')
     fig.tight_layout()
     fig.savefig(OUT / '月營收.png', dpi=150)
     plt.close(fig)
     assert sum(amounts) == 800000 and growth[2] == -0.25
     ''', '半年營收 800,000 元；3 月月增率 −25%；6 月較 5 月增加 12.5%。')

case('11_行銷_活動成效', 4, '行銷', '比率與長條圖',
     '活動編號、管道、花費_元、曝光數、點擊數、名單數',
     [['M001','搜尋',12000,100000,3000,120],['M002','社群',9000,150000,4500,90],
      ['M003','電子報',3000,10000,1500,60],['M004','展示',2000,50000,0,0]],
     ['逐列計算點擊率與每筆名單成本。','分母為 0 時保留空白，不能顯示為 0 元。',
      '畫各管道名單數長條圖，算整體每筆名單成本。'],
     '點擊率＝點擊數÷曝光數；每筆名單成本＝花費÷名單數；整體比率用總和相除。',
     '''
     import matplotlib.pyplot as plt
     result = [dict(r, 點擊率=r['點擊數']/r['曝光數'] if r['曝光數'] else None,
                    每筆名單成本=r['花費_元']/r['名單數'] if r['名單數'] else None) for r in rows]
     overall = sum(r['花費_元'] for r in rows) / sum(r['名單數'] for r in rows)
     print(result, '整體每筆名單成本：', overall)
     save_csv('活動成效.csv', result)
     fig, ax = plt.subplots()
     ax.bar([r['活動編號'] for r in rows], [r['名單數'] for r in rows])
     ax.set(title='Campaign leads', xlabel='Campaign ID', ylabel='Leads')
     fig.tight_layout()
     fig.savefig(OUT / '活動名單數.png', dpi=150)
     plt.close(fig)
     assert result[3]['每筆名單成本'] is None
     assert overall == 26000/270
     ''', 'M001、M002、M003 名單成本為 100、100、50 元；M004 空白；整體約 96.30 元。')

case('12_跨部門_請購驗收核對', 4, '採購／倉管／財務', '跨工作表核對與明細報表',
     '請購單號、部門、品項、請購數量、單價_元',
     [['PR001','行政','影印紙',20,120],['PR002','人資','資料夾',30,20],
      ['PR003','業務','筆記本',10,50],['PR004','財務','碳粉',2,1800]],
     ['以請購單號連結「資料」與「驗收」工作表，不能依列位置拼接。',
      '先加總同一請購單的分批驗收數量，保留沒有驗收的請購單。',
      '計算未到量與未到金額，輸出核對報表。'],
     '每張請購單只有一種品項；同單可分批驗收。沒有驗收紀錄才視為收到 0 件；未到金額＝未到量×單價，不代表應付款。',
     '''
     from collections import defaultdict
     receipts = read_rows(wb['驗收'])
     quantity = defaultdict(int)
     request_ids = {r['請購單號'] for r in rows}
     assert len(request_ids) == len(rows), '請購主檔單號重複'
     for r in receipts:
         assert r['請購單號'] in request_ids, '驗收有未知請購單號'
         quantity[r['請購單號']] += r['驗收數量']
     result = []
     for r in rows:
         received = quantity[r['請購單號']]
         assert received <= r['請購數量'], '有超收，需另外查核'
         missing = r['請購數量'] - received
         result.append(dict(r, 已到量=received, 未到量=missing, 未到金額_元=missing*r['單價_元']))
     print(result)
     save_csv('請購驗收核對.csv', result)
     assert [r['未到量'] for r in result] == [0,10,10,0]
     assert sum(r['未到金額_元'] for r in result) == 700
     ''', 'PR001 分批 12＋8＝20 件；PR002 未到 10 件、200 元；PR003 未到 10 件、500 元；合計 700 元。',
     extra=[dict(name='驗收', headers=['驗收單號','請購單號','驗收數量'], rows=[
         ['GR001','PR004',2],['GR002','PR001',12],['GR003','PR002',20],['GR004','PR001',8]])])


def intro_code(c):
    return f'''from pathlib import Path
import csv
from openpyxl import load_workbook

# 本機：把 Notebook 與 Excel 放在同一資料夾。Colab：先上傳本例 Excel。
SOURCE = Path('{c['name']}.xlsx')
if not SOURCE.exists():
    try:
        from google.colab import files
    except ImportError:
        raise FileNotFoundError(f'請將 {{SOURCE.name}} 放到目前工作目錄：{{Path.cwd()}}')
    files.upload()
if not SOURCE.exists():
    raise FileNotFoundError(f'尚未找到 {{SOURCE.name}}，請確認上傳檔名')
OUT = Path('output') / '{c['name']}'
OUT.mkdir(parents=True, exist_ok=True)

def read_rows(sheet):
    data = sheet.iter_rows(values_only=True)
    headers = next(data)
    return [dict(zip(headers, row)) for row in data if any(v is not None for v in row)]

def save_csv(name, records):
    if not records:
        print('沒有符合條件的資料，未輸出 CSV')
        return
    with (OUT / name).open('w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)

# 來源檔只有原始值，沒有需要重算的 Excel 公式。
wb = load_workbook(SOURCE, read_only=True, data_only=True)
print('工作表：', wb.sheetnames)
rows = read_rows(wb['資料'])
print('第一筆：', rows[0])'''


def md_for(c):
    sheets = '\n'.join(f"- `{s['name']}`：{len(s['rows'])} 筆；欄位：{'、'.join(s['headers'])}。" for s in c['sheets'])
    steps = '\n'.join(f'{i}. {t}' for i, t in enumerate(c['tasks'],1))
    prompt = f"我在{c['department']}部門工作，是 Python 初學者。請讀取 {c['name']}.xlsx。\n" + '\n'.join(c['tasks'])
    prompt += f"\n資料規則：{c['rule']}\n請使用 openpyxl 讀檔"
    prompt += '，搭配 NumPy 計算' if c['level'] == 3 else ''
    prompt += '，搭配 Matplotlib 畫圖' if c['name'].startswith(('10_', '11_')) else ''
    prompt += '。先列出你理解的欄位與處理步驟，再給可在 Colab 執行的程式，每個步驟附中文說明。\n輸出放到 output/，保留來源 Excel；缺值與分母為 0 時請明確處理。'
    return f'''# {c['name']}：{c['topic']}

[回到第一階段案例總覽](./README.md)

難度 {c['level']}/4｜部門：{c['department']}｜[下載 Excel](./{c['name']}.xlsx)｜[參考 Notebook](./{c['name']}.ipynb)

## 情境與資料

主管交給你一份 Excel，希望你完成下面的任務，並能說明結果如何算出來。
本例為固定的教學模擬資料，姓名、單號與金額不對應真實公司。

{sheets}

**計算規則**：{c['rule']}

## 跟著做

{steps}

先在 Excel 人工找出兩筆資料核對，再把下列需求交給 AI。一次完成一個步驟，確認結果後再繼續。

## 可複製的 AI 提問

```text
{prompt}
```

## 驗收答案

{c['check']}

請向 AI 追問：「請用原始資料的兩筆紀錄，逐步解釋你的計算；如果資料新增一列，哪些部分需要修改？」
數字相符後，再用一句話寫出可採取的行動，以及本例資料無法回答的問題。

## 參考程式

本機需安裝 `openpyxl numpy matplotlib`。在 Colab 先執行 `!pip -q install openpyxl numpy matplotlib`，再上傳本例 Excel。
圖表使用英文標題避免環境缺少中文字型，圖中的代碼可回查來源表。

```python
{intro_code(c)}

{c['code']}

wb.close()
```
'''


def build():
    DEST.mkdir(exist_ok=True)
    for c in CASES:
        (DEST / f"{c['name']}.md").write_text(md_for(c), encoding='utf-8')
        cells = [dict(cell_type='markdown', metadata={}, source=f"# {c['name']}\n\n{c['topic']}\n\n任務："+'；'.join(c['tasks'])+f"\n\n規則：{c['rule']}\n\n先人工核對再執行。資料皆為教學模擬值。"),
                 dict(cell_type='code', execution_count=None, metadata={}, outputs=[], source='%pip -q install openpyxl numpy matplotlib'),
                 dict(cell_type='code', execution_count=None, metadata={}, outputs=[], source=intro_code(c)),
                 dict(cell_type='code', execution_count=None, metadata={}, outputs=[], source=c['code']+'\nwb.close()'),
                 dict(cell_type='markdown', metadata={}, source='## 驗收答案\n\n'+c['check'])]
        nb = dict(cells=cells, metadata=dict(kernelspec=dict(display_name='Python 3',language='python',name='python3')), nbformat=4, nbformat_minor=5)
        for i, cell in enumerate(cells):
            cell['id'] = f'office-{i}'
        (DEST / f"{c['name']}.ipynb").write_text(json.dumps(nb, ensure_ascii=False, indent=1)+'\n',encoding='utf-8')
    table = '\n'.join(f"| {i:02d} | {c['level']} | {c['department']} | [{c['topic']}](./{c['name']}.md) | [Excel](./{c['name']}.xlsx) | [Colab](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/{quote(DEST.name+'/'+c['name']+'.ipynb')}) |" for i,c in enumerate(CASES,1))
    (DEST / 'README.md').write_text(f'''# 第一階段：AI 協作辦公室 Excel 實戰

從看懂一張 Excel 開始，逐步學會把需求說清楚、請 AI 產生 Python、核對計算，最後交出清單或圖表。
這 12 例全部使用辦公室常見的 Excel 檔，涵蓋行政、人資、財務、業務、倉管、採購、客服與行銷。
資料是**教學模擬資料**，可重建，適合直接用 Excel 開啟與手算驗收。

[下載全部教材（12 份 Excel＋案例說明＋Notebook）](./辦公室Excel_學生素材.zip)｜[回到課程首頁](../README.md)

## 由淺至深的學習順序

| 層級 | 案例 | 先備能力 | 本次新增的能力 | 過關標準 |
| --- | --- | --- | --- | --- |
| 1 讀懂單一表格 | 01～03 | Python 變數、list、dict、for 與 if 的基本概念 | 讀取 xlsx、看欄位、篩選、加總 | 能說出每列意義，手算核對筆數與總額 |
| 2 產生工作清單 | 04～06 | 完成層級 1 | 乘法、排序、多條件、CSV 輸出 | 說清楚金額與門檻規則，產出清單與原表一致 |
| 3 整批統計 | 07～09 | 完成層級 2 | NumPy、axis、缺值、平均、分類統計 | 分清楚每列每欄及平均數的分母 |
| 4 呈現與核對 | 10～12 | 完成層級 3 | Matplotlib、比率、依單號核對多工作表 | 圖表有標題與單位，跨表不漏單、不重複加總 |

建議先依 01→12 完成，再換成自己部門的同類表格。每次只新增一項主要觀念。
原課程章節可依「檔案存取 → NumPy → 繪圖」搭配閱讀；跨表核對先用字典理解，後續 pandas 章節再學 merge 與 groupby。

## 12 個部門案例

| 順序 | 難度 | 部門 | 學習重點與操作說明 | 素材 | 線上執行 |
| --- | --- | --- | --- | --- | --- |
{table}

## 每一例怎麼上課

1. **先看 Excel**：工作表叫什麼？每列代表什麼？金額、件數、分鐘的單位是什麼？
2. **說清楚任務**：先做案例中的第一個步驟，使用附上的 AI 提問逐步要求程式。
3. **執行與核對**：在 Colab 上傳本例 Excel；本機則把 Notebook 與 Excel 放在同一個工作目錄。卡住時再看參考 Notebook。
4. **驗收與說明**：對照每例的固定答案，再抽兩筆手算。輸出 CSV 用 UTF-8 BOM，方便 Excel 開啟；圖表存成 PNG。
5. **換一個條件**：改部門、門檻或一筆數值，先預測結果，再重跑。不要只用「沒有報錯」判斷成功。

參考 Notebook 已含完整解法與斷言檢查；不會自動下載資料，請先下載並上傳對應 Excel。
所有結果寫到 `output/案例名稱/`，重跑會覆蓋同名輸出，來源 Excel 不變。這一階段以讀 Excel、輸出 CSV 與 PNG 為主，格式化 Excel 報表留到後續章節。

## AI 提問的五個必要資訊

| 要說清楚的資訊 | 辦公室例子 |
| --- | --- |
| 來源與工作表 | 讀取 `05_倉管_庫存補貨.xlsx` 的「資料」工作表 |
| 每列代表什麼 | 每列一個商品；商品編號是文字 |
| 計算規則 | 可用量＝現有庫存＋已訂未到；低於安全庫存才補貨 |
| 例外處理 | 等於門檻不補貨；缺值先列出，不自行當成 0 |
| 交付與驗收 | 輸出補貨清單，人工核對 P001 與 P004 的補貨量 |

## 完成後再進階

完成 01～06，再練習把多個月份檔案批次讀入；完成 07～12，再進入 [pandas 入門](../初見pandas/README.md)。
樞紐分析、多檔合併、資料清理與自動產出格式化 Excel 報表，安排在後續階段。
''', encoding='utf-8')
    Path('/tmp/office-materials.json').write_text(json.dumps(dict(destination=str(DEST),cases=CASES),ensure_ascii=False),encoding='utf-8')
    print('已產生 12 份案例說明與 Notebook；Excel 清單：/tmp/office-materials.json')


def package():
    files = [p for p in DEST.iterdir() if p.suffix in {'.xlsx','.ipynb','.md'}]
    assert len(list(DEST.glob('*.xlsx'))) == 12, '請先產生 12 份 Excel'
    with zipfile.ZipFile(DEST / '辦公室Excel_學生素材.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(files):
            z.write(p,p.name)
    print('教材已打包')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--zip-only',action='store_true')
    args = parser.parse_args()
    if args.zip_only:
        package()
    else:
        build()
