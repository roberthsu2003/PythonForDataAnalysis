"""第 8 章 資料整理：警政署真實 A1 交通事故資料——註解列、數字日期時間、文字拆數字、一列一個當事者、異常值。"""
from nbtools import md, code, setup_cell, font_cell, header, exercises, copy_real, latest

CHAPTER = '資料整理和使用前準備'
NOTEBOOK = '範例_死亡車禍資料大掃除_A1交通事故.ipynb'
SOURCES = ['a1']


def build(out):
    files = [copy_real(out, 'a1')]
    desc = [(files[0], '警政署 A1 類交通事故（**有人在 24 小時內死亡**的車禍）：今年 1 月起，每一列是一位當事者，共 51 個欄位')]

    cells = [
        header(CHAPTER, NOTEBOOK, '🚦 死亡車禍資料大掃除：清理警政署 A1 交通事故',
               '台灣每年有上千人死於車禍。警政署公開了每一件「A1 類」（造成死亡）事故的詳細資料：時間、地點、天氣、車種、年齡、肇事原因……'
               '但下載下來你會發現：檔案最後混了說明文字、日期是 `20260101.0`、時間是 `53700.0`、「死亡1;受傷0」擠在同一格，'
               '而且**一場車禍會出現好幾列**。今天的任務是：**把它清理乾淨，再回答「死亡車禍最常發生在什麼時候？為什麼會發生？」**',
               desc, SOURCES),
        md('''
> ⚠️ 這份資料記錄的是真實發生、有人過世的事故。分析它的目的，是找出可以預防的原因——**每一個數字背後，都是一個家庭。**
'''),
        setup_cell(CHAPTER, files),
        font_cell(),
        md('''
## 任務 1：健康檢查——資料最後面怎麼有奇怪的東西？

**白話說明**：拿到資料先做「健康檢查」：幾列幾欄、頭尾長什麼樣子、每一欄是什麼型態。**很多問題藏在檔案的最後幾列。**
'''),
        code('''
import pandas as pd

raw = pd.read_csv('A1類交通事故.csv')
print('幾列 × 幾欄：', raw.shape)
display(raw[['發生年度', '發生月份', '發生日期', '發生時間', '發生地點', '死亡受傷人數']].tail(4))
print(raw[['發生年度', '發生日期', '發生時間']].dtypes)
'''),
        md('''
> 🕵️ **發現問題**：最後兩列不是事故，而是「資料提供日期：…」和「事故類別：A1類」這種**說明文字**！也因為它們，`發生年度` 整欄被當成文字（str）。
>
> 解法：把 `發生年度` 轉成數字，轉不過去的（說明文字）會變成 `NaN`，再把這些列刪掉。
'''),
        code('''
df = raw.copy()
df['發生年度'] = pd.to_numeric(df['發生年度'], errors='coerce')   # 轉不了的 → NaN
print('說明文字列：', df['發生年度'].isna().sum(), '列')
df = df.dropna(subset=['發生年度'])                                  # 刪掉說明文字列
print('清理後：', df.shape)
'''),
        md('''
## 任務 2：日期是 `20260101.0`、時間是 `53700.0`？——型態轉換

**白話說明**：
- 日期：先轉成整數 `20260101`，再用 `pd.to_datetime(..., format='%Y%m%d')` 告訴 pandas 「前 4 碼是年、接著 2 碼月、2 碼日」。
- 時間：`53700` 其實是 **05:37:00**——前面的 0 被吃掉了！用 `zfill(6)` 補回 6 碼 `053700`，再取前 2 碼就是小時。
'''),
        code('''
df['日期'] = pd.to_datetime(df['發生日期'].astype(int).astype(str), format='%Y%m%d')
time_text = df['發生時間'].astype(int).astype(str).str.zfill(6)       # 53700 → '053700'
df['小時'] = time_text.str[:2].astype(int)
df['時間'] = time_text.str[:2] + ':' + time_text.str[2:4]              # '05:37'
df[['發生日期', '發生時間', '日期', '時間', '小時']].head()
'''),
        md('''
## 任務 3：「死亡1;受傷0」——把一格文字拆成兩個數字

**白話說明**：`str.extract` 用「正規表示式」從文字裡抓出想要的部分：`(\\d+)` 代表「一串數字」，括號抓到的東西會變成新的一欄。
'''),
        code('''
nums = df['死亡受傷人數'].str.extract(r'死亡(\\d+);受傷(\\d+)').astype(int)   # 兩個括號 → 兩欄
df['死亡'], df['受傷'] = nums[0], nums[1]
df[['死亡受傷人數', '死亡', '受傷']].drop_duplicates().head()
'''),
        md('''
## 任務 4：2,885 列，但其實沒有 2,885 件車禍！

**白話說明**：仔細看前幾列——同一個時間、同一個地點出現好幾次，因為**一列是一位「當事者」**（駕駛、乘客、行人……）。一場車禍有 3 個當事者，就會有 3 列。
如果直接用列數算「事故數」、直接加總「死亡」，都會**重複計算**！

解法：每場事故只留「當事者順位 = 1」（第一當事者）那一列，就是一場事故一列的「事故表」。
'''),
        code('''
print('列數（當事者人數）：', len(df))
accidents = df[df['當事者順位'] == 1].copy()                         # 一場事故只留第一當事者
print('事故件數：', len(accidents))
print('錯誤算法（直接加總每一列）死亡人數：', df['死亡'].sum())
print('正確算法（每場事故算一次）死亡人數：', accidents['死亡'].sum())
'''),
        md('''
> 💡 **看懂結果**：2,885 列其實只有 **1,127 件**事故；如果不注意，死亡人數會從 1,161 人被算成 3,066 人——多了 2.6 倍！
> 這是真實資料最常見、也最危險的陷阱：**先搞清楚「一列代表什麼」**，再開始算。
>
> 🤖 **換你問 AI**：「這份事故資料一列是一位當事者，同一場事故有多列。請幫我建立一場事故一列的表格，並說明為什麼直接加總會重複計算。」
'''),
        md('''
## 任務 5：年齡 -1 歲？——處理異常值與缺值

**白話說明**：年齡欄裡有 **-1** 和 **0**：-1 是「不明」，0 多半是「不是人」（例如撞到電線桿，當事者是物體）。這些不是真的年齡，要改成 `NaN`，才不會把平均拉低。
'''),
        code('''
age = df['當事者事故發生時年齡']
print('年齡 = -1 的有', (age == -1).sum(), '列；年齡 = 0 的有', (age == 0).sum(), '列')
print('清理前平均年齡：', round(age.mean(), 1))

df['年齡'] = age.where(age.between(1, 100))                           # 1～100 歲以外 → NaN
print('清理後平均年齡：', round(df['年齡'].mean(), 1))

df['車種'] = df['當事者區分-類別-大類別名稱-車種'].fillna('非車輛（物體）')   # 缺值補上說明文字
df['縣市'] = df['處理單位名稱警局層'].str.replace('政府警察局', '').str.replace('警察局', '')   # 臺南市政府警察局 → 臺南市
df[['年齡', '車種', '縣市']].head()
'''),
        md('''
## 任務 6：清乾淨了！死亡車禍最常發生在什麼時候？為什麼？
'''),
        code('''
import matplotlib.pyplot as plt

by_hour = accidents['小時'].value_counts().sort_index()                 # 每個小時幾件事故
ax = by_hour.plot.bar(figsize=(11, 4), color=['#C0392B' if h in (6, 7, 16) else '#95A5A6' for h in by_hour.index],
                      title='A1 死亡車禍：各小時事故件數')
ax.set_xlabel('發生時間（時）'); ax.set_ylabel('件數')
plt.show()
'''),
        code('''
causes = accidents['肇因研判子類別名稱-主要'].value_counts().head(8)
display(causes.to_frame('事故件數'))

vehicle = df['車種'].value_counts(normalize=True).mul(100).round(1).head(6)   # 所有當事者的車種占比 %
display(vehicle.to_frame('占當事者 %'))
'''),
        md('''
> 💡 **看懂結果**：
> - **時間**：清晨 6～8 點與下午 4 點是兩個高峰，正好是**上下班、上下學**的時間。
> - **原因**：第一名是「**恍神、緊張、心不在焉分心駕駛**」，比酒駕還多！很多事故不是技術不好，而是「**沒有專心**」。
> - **車種**：死亡車禍的當事者裡，**機車騎士最多**；還有不少是行人。
>
> 所以，騎車上學時，不看手機、不趕時間、專心看路——數據告訴我們，這真的會救命。
'''),
        latest('''
import pandas as pd
url = ('https://opdadm.moi.gov.tw/api/v1/no-auth/resource/api/dataset/02D40248-7CAA-4354-82EA-E27AB8DCAB39'
       '/resource/67214307-AD41-4FE7-A04F-D8051A0301DB/download')
latest_a1 = pd.read_csv(url)                                # 警政署每隔一段時間更新今年的 A1 事故
latest_a1.shape
'''),
    ] + exercises(
        dict(title='酒駕造成的死亡車禍有幾件？',
             hint='用「事故表」`accidents`（一場一列）來數。主要肇因欄位是 `肇因研判子類別名稱-主要`，酒駕的寫法是 `\'酒醉(後)駕駛\'`。',
             starter='''
drunk = (accidents['肇因研判子類別名稱-主要'] == ___).sum()
print('酒駕死亡車禍：', drunk, '件，占', round(drunk / len(accidents) * 100, 1), '%')
''',
             check='''
_acc = df[df['當事者順位'] == 1]
check('drunk', (_acc['肇因研判子類別名稱-主要'] == '酒醉(後)駕駛').sum())
''',
             solution='''
drunk = (accidents['肇因研判子類別名稱-主要'] == '酒醉(後)駕駛').sum()
print('酒駕死亡車禍：', drunk, '件，占', round(drunk / len(accidents) * 100, 1), '%')
'''),
        dict(title='哪個縣市的死亡車禍件數最多？',
             hint='`accidents` 在任務 4 建立時還沒有「縣市」欄，要從 `df` 重新做一次事故表：`df[df[\'當事者順位\'] == 1]`，再對「縣市」用 `value_counts()`。',
             starter='''
acc_city = df[df['當事者順位'] == ___]['縣市'].___()
display(acc_city.head(5))
''',
             check='''
check('acc_city', df[df['當事者順位'] == 1]['縣市'].value_counts())
''',
             solution='''
acc_city = df[df['當事者順位'] == 1]['縣市'].value_counts()
display(acc_city.head(5))
# 要比較「危險程度」還要除以人口或車輛數，否則人多的縣市一定比較多
'''),
        dict(title='機車騎士的平均年齡是幾歲？',
             hint='篩出 `車種 == \'機車\'` 的當事者，再對清理過的「年齡」欄取平均（`mean()` 會自動跳過 NaN）。',
             starter='''
moto_age = df.loc[df['車種'] == ___, ___].mean()
print('死亡車禍中，機車騎士的平均年齡：', round(moto_age, 1), '歲')
''',
             check='''
check('moto_age', df.loc[df['車種'] == '機車', '年齡'].mean())
''',
             solution='''
moto_age = df.loc[df['車種'] == '機車', '年齡'].mean()
print('死亡車禍中，機車騎士的平均年齡：', round(moto_age, 1), '歲')
'''),
    )
    return NOTEBOOK, files, cells
