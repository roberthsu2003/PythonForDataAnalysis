"""第 11 章 群組運算：臺北捷運真實的各站分時進出量——統一站名、agg、多欄分組、先加總再相除、pd.cut、樞紐分析表。"""
from nbtools import md, code, setup_cell, font_cell, header, exercises, copy_real, latest

CHAPTER = '群組資料和群組運算'
NOTEBOOK = '範例_捷運哪一站最擠_誰住這裡誰在這上班.ipynb'
SOURCES = ['mrt']


def build(out):
    files = [copy_real(out, 'mrt')]
    desc = [(files[0], '臺北捷運 2026 年 3 月，每一站、每一天、每一小時的進站與出站人次（約 8 萬列；由臺北捷運公司的起訖站資料彙總）')]

    cells = [
        header(CHAPTER, NOTEBOOK, '🚇 捷運哪一站最擠？誰住這裡、誰在這裡上班？',
               '每天早上擠捷運的你，有沒有想過：**哪一站最多人？大家都從哪裡出發、去哪裡上班？假日大家又去哪裡玩？**'
               '臺北捷運公開了每一站、每一小時的進出站人次——一個月就有 8 萬列。只要學會一招 '
               '**groupby（分組 → 計算 → 合併）**，就能從這堆數字裡看出整座城市的作息。',
               desc, SOURCES),
        setup_cell(CHAPTER, files),
        font_cell(),
        md('''
## 任務 1：先檢查站名——同一站怎麼有兩個名字？

**白話說明**：分組之前，**分組用的欄位一定要乾淨**，不然同一組會被拆成兩組。我們先數一數每一站有幾列、進站和出站各多少。
'''),
        code('''
import pandas as pd

mrt = pd.read_csv('臺北捷運各站分時進出量_202603.csv', parse_dates=['日期'])
print(mrt.shape, '，車站數：', mrt['車站'].nunique())
display(mrt.head())

check_names = mrt.groupby('車站')[['進站人次', '出站人次']].sum()
check_names[check_names.index.str.contains('板橋|大坪林|景安|頭前庄')]
'''),
        md('''
> 🕵️ **發現問題**：「大坪林」只有進站、出站是 0；出站人次都記在「G大坪林」！板橋也被拆成「BL板橋」和「Y板橋」。
> 這些是**轉乘站**：資料把不同路線的紀錄，用「路線代碼＋站名」分開記。要分析「這一站」有多少人，得先把開頭的英文代碼去掉、合成同一站。
'''),
        code('''
mrt['車站'] = mrt['車站'].str.replace(r'^[A-Z]+', '', regex=True)      # 去掉開頭的英文路線代碼：G大坪林 → 大坪林
mrt = mrt.groupby(['日期', '時段', '車站'], as_index=False)[['進站人次', '出站人次']].sum()   # 同一站的紀錄加起來
mrt['假日'] = mrt['日期'].dt.day_of_week >= 5                           # 星期六、日
print('統一站名後的車站數：', mrt['車站'].nunique())
mrt[mrt['車站'] == '大坪林'].head(3)
'''),
        md('''
## 任務 2：哪一站最擠？——各站成績單

**白話說明**：「依 ___ 分組，計算 ___ 的 ___」。`agg` 可以一次算好幾個統計量，並取中文欄名：`新欄名=('原欄位', '計算方式')`。
'''),
        code('''
days = mrt['日期'].nunique()
station = mrt.groupby('車站').agg(進站=('進站人次', 'sum'), 出站=('出站人次', 'sum'))
station['每日平均進出'] = ((station['進站'] + station['出站']) / days).round(0)
station.sort_values('每日平均進出', ascending=False).head(10)
'''),
        md('''
> 💡 **看懂結果**：台北車站每天平均有 30 多萬人次進出，是第二名的兩倍以上——它同時是捷運兩條線、台鐵、高鐵、機場捷運的交會點。
'''),
        md('''
## 任務 3：平日和假日，大家搭捷運的時間一樣嗎？

**白話說明**：用**兩個欄位**分組：「假日 × 時段」。`unstack` 把「假日」搬到欄位，變成一張「時段 × 平日／假日」的表，方便畫圖比較。因為平日和假日的天數不一樣，要除以天數才是「平均每天」。
'''),
        code('''
import matplotlib.pyplot as plt

n_days = mrt.groupby('假日')['日期'].nunique()                          # 平日幾天、假日幾天
by_hour = mrt.groupby(['假日', '時段'])['進站人次'].sum().unstack('假日') / n_days   # 平均每天、每小時
by_hour.columns = ['平日', '假日']

ax = by_hour.plot(figsize=(10, 4.5), marker='o', color=['#2E86C1', '#E67E22'],
                  title='捷運全線：平均每小時進站人次')
ax.set_xticks(range(0, 24)); ax.set_xlabel('時段（點）'); ax.set_ylabel('人次')
plt.show()
'''),
        md('''
> 💡 **看懂結果**：平日是「**雙峰**」：早上 8 點、傍晚 6 點兩個尖峰——標準的上班上學作息；假日只有一個平緩的「**午後山丘**」，大家睡飽才出門。
'''),
        md('''
## 任務 4：誰住這裡？誰在這裡上班？——先加總，再相除

**白話說明**：平日早上 7～9 點，
- **住宅區**：大家從家裡出發 → **進站多、出站少**。
- **上班區**：大家到公司報到 → **出站多、進站少**。

所以「早上出站 ÷ 進站」越大，越像上班區。⚠️ 比率一定要**先把人次加總，再相除**，不能把每小時的比率直接平均。
'''),
        code('''
morning = mrt[(~mrt['假日']) & (mrt['時段'].between(7, 8))]               # 平日 7:00～8:59
am = morning.groupby('車站')[['進站人次', '出站人次']].sum()               # 先加總
am = am[am.sum(axis=1) > 100_000]                                         # 只看人比較多的站
am['出站÷進站'] = (am['出站人次'] / am['進站人次']).round(2)               # 再相除

print('🏠 最像「住宅區」的站（早上幾乎只有人出發）：')
display(am.sort_values('出站÷進站').head(6))
print('🏢 最像「上班區」的站（早上大家都來這裡）：')
display(am.sort_values('出站÷進站', ascending=False).head(6))
'''),
        md('''
> 💡 **看懂結果**：蘆洲、南勢角這些站，早上進站的人是出站的 10 倍以上——**大家住這裡**；台大醫院、松江南京、善導寺則反過來，出站是進站的好幾倍——**大家在這裡上班、看病**。
> 一個簡單的比率，就畫出了整座城市的「住」與「工作」地圖。
>
> 🤖 **換你問 AI**：「我有捷運各站每小時的進出站人次。請篩選平日早上 7～9 點，依車站加總進站與出站，再計算出站÷進站，找出最像住宅區和最像商辦區的車站。」
'''),
        md('''
## 任務 5：`pd.cut`——把每一站分成「住宅型、混合型、上班型」

**白話說明**：`pd.cut` 把連續的數字切成幾個區間，再貼上標籤。切點自己決定：比率 < 0.5 算住宅型、0.5～2 算混合型、> 2 算上班型。
'''),
        code('''
am['類型'] = pd.cut(am['出站÷進站'], bins=[0, 0.5, 2, 100], labels=['🏠 住宅型', '🔀 混合型', '🏢 上班型'])
am['類型'].value_counts()
'''),
        md('''
## 任務 6：樞紐分析表——假日大家都去哪裡？

**白話說明**：`pivot_table` 就是 Excel 的樞紐分析表：列放「車站」、欄放「假日」、值放「進站人次」、計算方式是「加總」。再除以天數，就能比較「假日平均每天」和「平日平均每天」。
'''),
        code('''
pivot = mrt.pivot_table(index='車站', columns='假日', values='進站人次', aggfunc='sum') / n_days
pivot.columns = ['平日每天', '假日每天']
pivot['假日÷平日'] = (pivot['假日每天'] / pivot['平日每天']).round(2)
pivot[pivot['平日每天'] > 8_000].sort_values('假日÷平日', ascending=False).head(8).round({'平日每天': 0, '假日每天': 0})
'''),
        md('''
> 💡 **看懂結果**：假日人潮暴增的是**大安森林公園**（約 1.6 倍）、**國父紀念館**、**圓山**（花博公園、美術館）——公園、展覽、觀光景點。
> 反過來，假日人最少的多半是商辦區。**同一條捷運，平日載上班族，假日載去玩的人。**
'''),
        latest('''
import pandas as pd
index = pd.read_csv('https://data.taipei/api/dataset/63f31c7e-7fc3-418b-bd82-b95158755b4d/resource/eb481f58-1238-4cff-8caa-fa7bb20cb4f4/download')
index.tail()        # 每個月一個原始檔的下載網址（一個月約 300MB 的起訖站資料，下載前請確認網路與硬碟空間）
''', note='臺北捷運每個月都會公布新的資料。這裡可以查到每個月原始檔的網址：'),
    ] + exercises(
        dict(title='星期幾搭捷運的人最多？',
             hint='先用 `.dt.day_of_week` 做出星期幾（0 = 星期一），再「依星期分組、加總進站人次」，最後除以「每個星期幾各有幾天」才公平。',
             starter='''
mrt['星期'] = mrt['日期'].dt.___
weekday_total = mrt.groupby('星期')['進站人次'].sum()
weekday_days = mrt.groupby('星期')['日期'].nunique()
weekday_avg = weekday_total / weekday_days
display(weekday_avg.round(0))
print('平均每天最多人的是星期', weekday_avg.idxmax() + 1)
''',
             check='''
_wd = mrt['日期'].dt.day_of_week
check('weekday_avg', mrt.groupby(_wd)['進站人次'].sum() / mrt.groupby(_wd)['日期'].nunique())
''',
             solution='''
mrt['星期'] = mrt['日期'].dt.day_of_week
weekday_total = mrt.groupby('星期')['進站人次'].sum()
weekday_days = mrt.groupby('星期')['日期'].nunique()
weekday_avg = weekday_total / weekday_days
display(weekday_avg.round(0))
print('平均每天最多人的是星期', weekday_avg.idxmax() + 1)
'''),
        dict(title='平日的台北車站，哪一個小時最多人出站？',
             hint='先篩出「台北車站」而且「不是假日」，再依「時段」分組加總出站人次，最後 `idxmax()`。',
             starter='''
tpe = mrt[(mrt['車站'] == ___) & (~mrt['假日'])]
tpe_peak = tpe.groupby(___)['出站人次'].sum().idxmax()
print('平日台北車站出站最多的時段：', tpe_peak, '點')
''',
             check='''
_t = mrt[(mrt['車站'] == '台北車站') & (~mrt['假日'])]
check('tpe_peak', _t.groupby('時段')['出站人次'].sum().idxmax())
''',
             solution='''
tpe = mrt[(mrt['車站'] == '台北車站') & (~mrt['假日'])]
tpe_peak = tpe.groupby('時段')['出站人次'].sum().idxmax()
print('平日台北車站出站最多的時段：', tpe_peak, '點')
'''),
        dict(title='每一站「單日進站最多」是哪一天、幾人次？',
             hint='先「依車站、日期分組加總」得到每站每天的進站人次；再「依車站分組」用 `agg([\'max\', \'idxmax\'])` 或分兩步做。這裡用 `max` 就好。',
             starter='''
daily = mrt.groupby(['車站', '日期'])['進站人次'].sum()
busiest = daily.groupby(level=___).max().sort_values(ascending=False)
display(busiest.head(5))
''',
             check='''
check('busiest', mrt.groupby(['車站', '日期'])['進站人次'].sum().groupby(level='車站').max())
''',
             solution='''
daily = mrt.groupby(['車站', '日期'])['進站人次'].sum()
busiest = daily.groupby(level='車站').max().sort_values(ascending=False)
display(busiest.head(5))
'''),
    )
    return NOTEBOOK, files, cells
