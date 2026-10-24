"""第 10 章 視覺化表格：Styler 格式化、條件標色、熱力圖、資料條、匯出 Excel。"""
import numpy as np
import pandas as pd

from common import STORES, daily_sales, expected_items, rng
from nbtools import md, code, setup_cell, header, exercises

CHAPTER = '視覺化表格'
NOTEBOOK = '範例_茶語時光_會發亮的KPI週報.ipynb'


def build(out):
    r = rng(100)
    d = daily_sales('2023-01-01', '2024-12-31')
    q2 = d[(d['日期'] >= '2024-04-01') & (d['日期'] <= '2024-06-30')]
    q2_last = d[(d['日期'] >= '2023-04-01') & (d['日期'] <= '2023-06-30')]
    kpi = q2.groupby('門市').agg(實際營收=('營收', 'sum'), 杯數=('杯數', 'sum'))
    kpi['去年同期營收'] = q2_last.groupby('門市')['營收'].sum()
    achieve = {'台北信義店': 0.97, '台北西門店': 0.91, '台中逢甲店': 1.02, '台南成大店': 1.08, '高雄巨蛋店': 0.98}   # 設定的達成率
    kpi['營收目標'] = ((kpi['實際營收'] / pd.Series(achieve) / 10000).round() * 10000).astype(int)
    kpi['來客數'] = (kpi['杯數'] / r.uniform(1.45, 1.6, len(kpi))).round().astype(int)
    kpi = kpi.reindex(STORES['門市'])                                  # 先依門市固定順序排好，再填入下面的清單
    kpi['Google評分'] = [4.5, 3.7, 4.2, 4.6, np.nan]                 # 信義、西門、逢甲、台南、高雄（高雄店 Google 頁面申請中）
    kpi['客訴數'] = [3, 14, 6, 2, 9]
    kpi['新會員數'] = r.integers(80, 260, len(kpi))
    kpi = kpi.reset_index()
    kpi[['門市', '營收目標', '實際營收', '去年同期營收', '來客數', 'Google評分', '客訴數', '新會員數']] \
        .to_csv(out / '門市KPI_2024Q2.csv', index=False, encoding='utf-8-sig')

    y = d[d['日期'].dt.year == 2024]
    items = expected_items(y)
    heat = items.drop(columns=['門市', '日期']).groupby(items['日期'].dt.month).sum().T
    heat.columns = [f'{m}月' for m in heat.columns]
    heat.index.name = '品項'
    heat.to_csv(out / '品項月銷量_2024.csv', encoding='utf-8-sig')

    files = ['門市KPI_2024Q2.csv', '品項月銷量_2024.csv']
    desc = [('門市KPI_2024Q2.csv', '第二季各門市的營收目標、實際營收、去年同期、來客數、評分、客訴、新會員'),
            ('品項月銷量_2024.csv', '10 個品項 × 12 個月的杯數')]

    cells = [
        header(CHAPTER, NOTEBOOK, '🎨 茶語時光：做一份「會發亮」的 KPI 報表',
               '每季的營運會議，區經理都要盯著一張密密麻麻的數字表找問題。老闆說：「能不能讓沒達標的自動變紅、'
               '表現最好的自動亮起來？我要一眼就看到重點。」你決定用 pandas 的 Styler 幫表格「化妝」，最後匯出成帶顏色的 Excel。', desc),
        setup_cell(CHAPTER, files),
        md('''
## 任務 1：先算出關鍵指標，再幫數字「換衣服」

**白話說明**：Styler 只改「外觀」，不改資料。千分位、百分比、小數位數，都用 `format` 設定。
'''),
        code('''
import pandas as pd

kpi = pd.read_csv('門市KPI_2024Q2.csv', index_col='門市')
kpi['達成率'] = kpi['實際營收'] / kpi['營收目標']                    # 實際 ÷ 目標
kpi['年成長率'] = kpi['實際營收'] / kpi['去年同期營收'] - 1          # 和去年同期比
kpi['客單價'] = kpi['實際營收'] / kpi['來客數']
display(kpi.round(3))                                                  # 素顏的表格：很難一眼看出重點

styled = kpi.style.format({
    '營收目標': '{:,.0f}', '實際營收': '{:,.0f}', '去年同期營收': '{:,.0f}', '來客數': '{:,}',
    '達成率': '{:.1%}', '年成長率': '{:+.1%}', '客單價': '{:.0f}', 'Google評分': '{:.1f}',
}, na_rep='尚無資料').set_caption('2024 第二季門市 KPI')
styled
'''),
        md('''
## 任務 2：內建螢光筆——最好、最差、缺資料
'''),
        code('''
styled2 = (styled
           .highlight_max(subset=['達成率', '年成長率', 'Google評分', '新會員數'], props='background-color:#c6efce; font-weight:bold;')  # 每欄最好：綠底
           .highlight_min(subset=['達成率', '年成長率', 'Google評分'], props='background-color:#ffc7ce;')                               # 每欄最差：紅底
           .highlight_null(color='#ffeb9c'))                                                                                          # 缺資料：黃底
styled2
'''),
        md('''
## 任務 3：自訂規則——沒達標變紅、客訴太多變紅字

**公司的規則**：達成率 < 95% 紅底白字；≥ 105% 綠底；客訴 ≥ 10 件紅色粗體。
'''),
        code('''
def rate_color(v):                                                    # 一次處理一格「達成率」
    if v < 0.95:
        return 'background-color:#c00000; color:white; font-weight:bold;'
    if v >= 1.05:
        return 'background-color:#00b050; color:white;'
    return None

def complaint_color(v):
    return 'color:#c00000; font-weight:bold;' if v >= 10 else None

styled3 = (styled
           .map(rate_color, subset=['達成率'])                         # 套用到「達成率」欄（舊版 pandas 寫作 applymap）
           .map(complaint_color, subset=['客訴數'])
           .bar(subset=['年成長率'], align=0, color=['#ff9999', '#99cc99'], vmin=-0.2, vmax=0.3))   # 成長率資料條：負紅正綠，0 對齊
styled3
'''),
        md('''
> 💡 **看懂結果**：西門店**達成率最低、客訴最多、評分也最低**——三個警訊同時亮起，下季要優先改善；台南成大店則是全面亮綠燈。
> 有了顏色，區經理不用一格一格看數字，**三秒鐘就找到問題門市**。
>
> 🤖 **換你問 AI**：「請用 pandas Styler 格式化這份 KPI 表：達成率顯示百分比，低於 95% 紅底白字、高於 105% 綠底；客訴 ≥ 10 紅字；成長率用資料條呈現。」
'''),
        md('''
## 任務 4：熱力圖——一眼看出每個品項的旺季

**白話說明**：`background_gradient` 讓數字越大顏色越深，一張表就能看出「季節性」。`axis=1` 代表**每個品項自己比較**（每一列各自上色）。
'''),
        code('''
heat = pd.read_csv('品項月銷量_2024.csv', index_col='品項')
heat_style = (heat.style
              .background_gradient(cmap='YlOrBr', axis=1)              # 每一列（每個品項）各自由淺到深
              .format('{:,}')
              .set_caption('2024 各品項每月杯數（顏色越深＝該品項的旺季）'))
heat_style
'''),
        md('''
> 💡 **看懂結果**：芒果冰沙的深色集中在 6～9 月，熱可可只有 1～2 月、12 月有顏色；芋頭鮮奶 1～3 月是空白（還沒上市）。**採購與行銷檔期就照著這張表排。**
'''),
        md('''
## 任務 5：匯出成「帶顏色」的 Excel，直接寄給區經理
'''),
        code('''
with pd.ExcelWriter('2024Q2_KPI報表.xlsx') as writer:
    styled3.to_excel(writer, sheet_name='門市KPI')                      # 顏色、粗體會一起保留
    heat_style.to_excel(writer, sheet_name='品項季節性')
print('✅ 已輸出 2024Q2_KPI報表.xlsx（用 Excel 打開就能看到顏色）')
print('原始資料沒有被改變：實際營收合計 =', f"{kpi['實際營收'].sum():,}")
''')
    ] + exercises(
        dict(title='「客單價」高於全公司平均的格子，標成淡藍底',
             hint='`styled.map(函式, subset=[\'客單價\'])` 會把每一格的值丟進函式；函式回傳 CSS 字串（例如 `\'background-color:#ddebf7;\'`）就會上色，回傳 `None` 就不變。',
             starter='''
avg = kpi['客單價'].___()
ex1 = styled.map(lambda v: 'background-color:#ddebf7;' if v > ___ else None, subset=['客單價'])
ex1
''',
             check='''
check('avg', kpi['客單價'].mean())
''',
             solution='''
avg = kpi['客單價'].mean()
ex1 = styled.map(lambda v: 'background-color:#ddebf7;' if v > avg else None, subset=['客單價'])
ex1
'''),
        dict(title='給老闆看的版本：隱藏「去年同期營收」與「營收目標」兩欄',
             hint='`.hide(subset=[欄位, 欄位], axis=\'columns\')`，只是「不顯示」，資料本身還在。',
             starter='''
ex2 = styled.hide(subset=[___, ___], axis='columns')
ex2
''',
             solution='''
ex2 = styled.hide(subset=['去年同期營收', '營收目標'], axis='columns')
ex2
'''),
        dict(title='熱力圖改成 `axis=0`：顏色的意思變成什麼？',
             hint='`axis=1` 是「每一列（品項）自己比」；`axis=0` 是「每一欄（月份）自己比」——看的是「這個月誰賣最好」。',
             starter='''
ex3 = heat.style.background_gradient(cmap='YlOrBr', axis=___).format('{:,}')
ex3
''',
             solution='''
ex3 = heat.style.background_gradient(cmap='YlOrBr', axis=0).format('{:,}')
ex3
# axis=0 → 每個月份（每一欄）各自上色，看的是「這個月誰賣最好」，而不是「這個品項哪個月最好」
'''),
    )
    return NOTEBOOK, files, cells
