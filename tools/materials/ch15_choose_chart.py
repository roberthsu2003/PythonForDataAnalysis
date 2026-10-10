"""新章節 看懂資料與選對圖表：認識欄位 → 問對問題 → 選對圖表 → 把圖表交給 AI → 驗證。"""
import shutil
from pathlib import Path
from urllib.parse import quote

from common import daily_sales, order_lines
from nbtools import REPO_BLOB, md, code, setup_cell, font_cell, header, zip_url

CHAPTER = '看懂資料與選對圖表'
NOTEBOOK = '範例_陌生資料挑戰_空氣品質.ipynb'
ROOT = Path(__file__).resolve().parents[2]

# ── 兩本 Notebook 共用的「資料健檢」與「給 AI 的資料說明」工具 ──
HELPER = r'''
# 🩺 資料健檢小工具：自動判斷每一欄的「型態」，並建議適合的分析與圖表（可以複製到任何專案使用）
import pandas as pd

def 認識資料(df):
    rows = []
    for col in df.columns:
        s = df[col]
        name = str(col).lower()
        n_unique = s.nunique(dropna=True)
        as_number = pd.to_numeric(s, errors='coerce')                     # 試著把整欄轉成數字
        number_like = as_number.notna().sum() >= 0.9 * max(s.notna().sum(), 1)
        if any(k in name for k in ['編號', '代碼', 'id', 'code']):
            kind, tip = '識別碼', '只能「數有幾個」，不要加總或平均'
        elif any(k in name for k in ['經度', '緯度', 'longitude', 'latitude', 'lat', 'lng']):
            kind, tip = '地理座標', '畫在地圖上，或用散佈圖看位置'
        elif pd.api.types.is_datetime64_any_dtype(s):
            kind, tip = '時間', '趨勢 → 折線圖（resample、rolling）'
        elif pd.api.types.is_numeric_dtype(s):
            if n_unique <= 7:
                kind, tip = '數值（只有少數幾種）', '可能是評分或等級 → 依順序排的長條圖'
            else:
                kind, tip = '數值', '分布 → 直方圖／盒鬚圖；關係 → 散佈圖；比較 → 分組加總後畫長條圖'
        elif number_like:
            kind, tip = '⚠️ 數字卻存成文字', '先用 pd.to_numeric(..., errors="coerce") 轉成數字'
        elif pd.to_datetime(s, errors='coerce', format='mixed').notna().mean() > 0.9:
            kind, tip = '時間（目前是文字）', '先用 pd.to_datetime 轉換，再看趨勢 → 折線圖'
        elif n_unique <= 30:
            kind, tip = '類別', '比較 → 排序長條圖；組成 → 百分比堆疊長條（5 類以內才用圓餅圖）'
        else:
            kind, tip = '文字／種類很多的類別', '先取前 10 名或分組，再畫圖'
        rows.append({'欄位': col, '判斷型態': kind, '缺值%': round(s.isnull().mean() * 100, 1),
                     '不重複數': n_unique, '範例': '、'.join(s.dropna().astype(str).unique()[:3]), '建議': tip})
    return pd.DataFrame(rows).set_index('欄位')


def 資料說明給AI(df, 資料名稱):
    """產生一段可以直接複製貼給 AI 的資料說明。"""
    report = 認識資料(df)[['判斷型態', '缺值%', '不重複數', '範例']]
    text = (f'【資料名稱】{資料名稱}\n【大小】{df.shape[0]} 列 × {df.shape[1]} 欄\n\n'
            f'【每一欄的型態】\n{report.to_string()}\n\n【前 5 列】\n{df.head().to_string()}\n')
    print(text)
    return text
'''


def build(out):
    """學生素材：陌生資料挑戰（真實空氣品質資料）＋ 課堂用的茶語時光資料。"""
    shutil.copy(ROOT / 'pandas的檔案存取' / '空氣品質指標.csv', out / '空氣品質指標.csv')

    d = daily_sales('2024-01-01', '2024-12-31')
    d['日期'] = d['日期'].dt.strftime('%Y-%m-%d')
    d[['日期', '門市', '縣市', '最高溫', '降雨量', '杯數', '營收', '事件']].to_csv(out / '茶語時光_每日營收_2024.csv',
                                                                         index=False, encoding='utf-8-sig')
    o = order_lines('2024-07-01', '2024-07-31', offset=15)
    keep = o['訂單編號'].drop_duplicates().sample(4000, random_state=15)               # 抽樣 4,000 筆訂單（保留完整明細）
    o = o[o['訂單編號'].isin(keep)].copy()
    o['訂單時間'] = o['訂單時間'].dt.strftime('%Y-%m-%d %H:%M:%S')
    o.drop(columns=['門市代碼', '品項代碼']).to_csv(out / '茶語時光_訂單抽樣_2024-07.csv', index=False, encoding='utf-8-sig')

    files = ['空氣品質指標.csv']
    desc = [('空氣品質指標.csv', '環境部全台 84 個測站某一小時的空氣品質觀測（真實的政府開放資料，24 個英文欄位）'),
            ('茶語時光_每日營收_2024.csv', '課堂範例用：5 家門市 2024 年每日杯數、營收、氣溫'),
            ('茶語時光_訂單抽樣_2024-07.csv', '課堂範例用：7 月抽樣 4,000 筆訂單明細')]

    cells = [
        header(CHAPTER, NOTEBOOK, '🔍 陌生資料挑戰：第一次看到空氣品質資料，該怎麼分析？',
               '同事丟來一份「空氣品質指標.csv」，說：「主管想知道全台空氣品質狀況，你幫忙看一下。」你打開檔案，'
               '看到 24 個英文欄位：SiteName、AQI、Pollutant、PM2.5、O3_8hr……完全不知道從何下手。'
               '這次你要練習本章的完整流程：**資料健檢 → 請 AI 建議問題 → 畫圖 → 把圖交給 AI 解讀與診斷 → 自己驗證**。', desc),
        md('> ℹ️ 空氣品質資料為環境部公開的真實資料；另兩個「茶語時光」檔案是課堂範例 `README.ipynb` 使用的模擬資料。'),
        setup_cell(CHAPTER, files),
        font_cell(),
        md('''
## 第 1 步：資料健檢——先認識每一欄

執行下面這格，就有一個可以重複使用的「資料健檢」工具。它會自動判斷每一欄是類別、數值、時間或識別碼，並建議適合的圖表。
'''),
        code(HELPER),
        code('''
aqi = pd.read_csv('空氣品質指標.csv')
print('大小：', aqi.shape)
認識資料(aqi)
'''),
        md('''
> 💡 **看懂健檢結果**：
> - `CO`、`WindSpeed`、`WindDirec` 被判斷為「⚠️ 數字卻存成文字」——裡面有非數字的值，計算前要先轉換。
> - `SiteId` 是識別碼，**不能拿來加總或平均**；`Longitude`、`Latitude` 是地理座標。
> - `Pollutant`（主要污染物）有很多缺值——空氣品質「良好」時不會標示主要污染物，**缺值本身也有意義**。
'''),
        md('''
## 第 2 步：把資料說明交給 AI，請它建議「該問什麼問題」

執行下一格，把印出來的文字**整段複製**，連同下面的提示詞一起貼給 ChatGPT、Claude 或 Gemini。
'''),
        code('''
說明 = 資料說明給AI(aqi, '環境部 空氣品質指標（全台測站某一小時的觀測值）')
'''),
        md('''
> **📋 貼給 AI 的提示詞**：
>
> 「你是資深資料分析師。以下是一份資料的欄位說明與前 5 列（貼上上方輸出）。我是非程式背景的初學者，請你：
> 1. 用白話解釋每個英文欄位代表什麼（例如 AQI、PM2.5、O3_8hr），哪些是最重要的欄位。
> 2. 建議 4 個主管可能關心的問題，分別屬於「比較、組成、分布、關係」哪一類。
> 3. 每個問題建議一種圖表，並說明為什麼、以及要避免哪種畫法。
> 4. 提醒我這份資料有哪些陷阱（例如型態錯誤、缺值、只代表某一個時間點）。」
'''),
        md('''
## 第 3 步：照建議畫圖，並存成圖檔準備交給 AI

以下是 4 個常見問題的參考畫法。每張圖都會存到「給AI的圖表」資料夾。
'''),
        code('''
import os
import matplotlib.pyplot as plt
os.makedirs('給AI的圖表', exist_ok=True)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# ① 比較：哪個縣市的平均 AQI 最高？→ 排序長條圖
county = aqi.groupby('County')['AQI'].mean().sort_values()
county.plot.barh(ax=axes[0, 0], color='#8B5E3C')
axes[0, 0].set_title('1. 比較：各縣市平均 AQI（越高越差）')

# ② 組成：各空氣品質等級的測站占比 → 依「好 → 壞」順序的長條圖
order = ['良好', '普通', '對敏感族群不健康', '對所有族群不健康', '非常不健康', '危害']
status = aqi['Status'].value_counts().reindex(order).dropna()
(status / status.sum() * 100).plot.bar(ax=axes[0, 1], color=['#16A34A', '#EAB308', '#F97316'][:len(status)], rot=0)
axes[0, 1].set_title('2. 組成：空氣品質等級的測站占比（%）')

# ③ 分布：AQI 集中在哪裡？→ 直方圖 + 中位數線
aqi['AQI'].plot.hist(ax=axes[1, 0], bins=15, color='#C8A27C', edgecolor='white')
axes[1, 0].axvline(aqi['AQI'].median(), color='red', linestyle='--', label=f"中位數 {aqi['AQI'].median():.0f}")
axes[1, 0].legend()
axes[1, 0].set_title('3. 分布：各測站 AQI')

# ④ 關係：PM2.5 越高，AQI 越高嗎？→ 散佈圖
aqi.plot.scatter(x='PM2.5', y='AQI', ax=axes[1, 1], alpha=0.6)
axes[1, 1].set_title('4. 關係：PM2.5 vs. AQI')

plt.tight_layout()
plt.savefig('給AI的圖表/空氣品質四張圖.png', dpi=150, bbox_inches='tight')
plt.show()
print('✅ 已存成 給AI的圖表/空氣品質四張圖.png')
'''),
        md('''
## 第 4 步：把圖交給 AI——解讀、診斷、改良

**怎麼把圖給 AI？**
- 在 Colab 或 Jupyter 中，**對圖表按右鍵 →「複製圖片」**，直接貼到 AI 的對話框；或
- 從左側檔案區下載 `給AI的圖表/空氣品質四張圖.png`，再上傳給 AI。

**三種問法（建議三種都試試看）**：

> 🔎 **解讀**：「這是全台空氣品質測站某一小時的四張圖（附圖）。請用白話告訴我 3 個最重要的發現，每個發現都要指出是從哪張圖看出來的。」
>
> 🩺 **診斷**：「請以專業資料視覺化的標準檢查這四張圖：有沒有誤導、看不清楚或可以改進的地方？請具體說明要怎麼改。」
>
> 🛠️ **改良**：「請針對你認為最需要改進的那張圖，提供改良後的 matplotlib 程式碼（使用繁體中文標題）。」
'''),
        md('''
## 第 5 步：驗證 AI 說的話——AI 會看錯圖！

AI 從圖片「目測」數字，常常會不精準，甚至把長條看錯。**AI 說出的每個數字，都要用 pandas 核對一次。**
'''),
        code('''
print('▶ 平均 AQI 最高的 3 個縣市：\\n', county.sort_values(ascending=False).head(3).round(1))
print('\\n▶ 各等級測站數：\\n', aqi['Status'].value_counts())
print('\\n▶ AQI 中位數：', aqi['AQI'].median(), '｜最高：', aqi['AQI'].max(), aqi.loc[aqi['AQI'].idxmax(), 'SiteName'])
print('\\n▶ PM2.5 與 AQI 的相關係數：', round(aqi['PM2.5'].corr(aqi['AQI']), 3))
'''),
        md('''
> 🔍 **一個常見的 AI 誤判**：PM2.5 和 AQI 的相關係數只有 0.36 左右，並沒有想像中高。原因是 AQI 取的是「各項污染物分項指標中最差的一項」——有些測站的主要污染物是懸浮微粒（PM10）或二氧化氮（看 `Pollutant` 欄）。如果 AI 斷言「PM2.5 越高，AQI 一定越高」，你就該打個問號。
>
> 💡 **驗收 AI 建議的 3 個問題**：
> 1. AI 說的數字和上面算出來的一樣嗎？
> 2. AI 有沒有提醒你：這份資料**只是某一個小時**的觀測，不能說「某縣市的空氣一直都比較差」？
> 3. AI 建議的改法，套用後真的比較好讀嗎？——**最後做決定的是你，不是 AI。**

---

## ✍️ 延伸挑戰

1. 把 `CO` 轉成數字（`pd.to_numeric(..., errors='coerce')`），再用健檢工具檢查一次，型態判斷有變嗎？
2. 用 `Longitude`、`Latitude` 畫散佈圖，點的顏色用 AQI（`c='AQI'`、`cmap='RdYlGn_r'`），看起來像什麼？把這張圖交給 AI，請它解讀地理上的分布。
3. 回到課堂範例的「茶語時光」資料，用同樣的流程挑一個你自己的問題，畫圖、交給 AI、再驗證。
'''),
        md('## 🔑 延伸挑戰參考程式'),
        code('''
# 延伸 1
aqi['CO'] = pd.to_numeric(aqi['CO'], errors='coerce')
print(認識資料(aqi).loc[['CO'], ['判斷型態', '缺值%']])

# 延伸 2
ax = aqi.plot.scatter(x='Longitude', y='Latitude', c='AQI', cmap='RdYlGn_r', s=60, figsize=(6, 8),
                      title='測站位置與 AQI（越紅越差）')
ax.set_aspect('equal')
plt.savefig('給AI的圖表/測站地圖.png', dpi=150, bbox_inches='tight')
plt.show()
'''),
    ]
    return NOTEBOOK, files, cells


# ─────────────────────────── 課堂 Notebook（README.ipynb） ───────────────────────────
def lesson_setup():
    return code(f'''
# 📦 準備資料：優先使用本章「學生素材」資料夾，沒有的話（例如在 Colab）自動下載本章素材壓縮檔
import os, shutil, zipfile, urllib.request

FILES = ['茶語時光_每日營收_2024.csv', '茶語時光_訂單抽樣_2024-07.csv']
ZIP_URL = '{zip_url(CHAPTER)}'

for f in FILES:
    if not os.path.exists(f) and os.path.exists(os.path.join('學生素材', f)):
        shutil.copy(os.path.join('學生素材', f), f)
if not all(os.path.exists(f) for f in FILES):
    urllib.request.urlretrieve(ZIP_URL, 'materials.zip')
    with zipfile.ZipFile('materials.zip') as z:
        for name in z.namelist():
            inner = name.split('/', 1)[1] if '/' in name else name
            if inner in FILES:
                with z.open(name) as src, open(inner, 'wb') as dst:
                    dst.write(src.read())
print('✅ 資料準備完成：', [f for f in FILES if os.path.exists(f)])
''')


def build_lesson(chapter_dir):
    badge = f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({REPO_BLOB}{quote(CHAPTER + '/README.ipynb')})"
    cells = [
        md(f'''
{badge}

# 看懂資料與選對圖表——再把圖表交給 AI

拿到一份陌生資料，最難的不是寫程式，而是**不知道該問什麼、該畫什麼**。本章教你一套固定流程：

1. **認識資料**：每一欄是類別、數值、時間，還是識別碼？
2. **問對問題**：主管的問題，幾乎都屬於「比較、組成、分布、關係、趨勢」五類之一。
3. **選對圖表**：問題類型決定圖表類型。
4. **交給 AI**：畫圖前，請 AI 建議問題；畫圖後，把圖交給 AI 解讀、診斷、改良。
5. **自己驗證**：AI 會看錯圖，數字一定要用 pandas 核對。

> 範例使用課程虛構的手搖飲品牌「茶語時光」模擬資料。
'''),
        lesson_setup(),
        font_cell(),
        md('''
## 1. 認識資料：每一欄是什麼型態？

| 型態 | 例子 | 能做的事 |
| --- | --- | --- |
| 類別 | 門市、品項、付款方式 | 計數、分組比較 |
| 順序類別 | 甜度（無糖→正常糖）、滿意度 1～5 | 計數，而且**要照順序排** |
| 數值 | 金額、杯數、氣溫 | 加總、平均、看分布 |
| 時間 | 日期、訂單時間 | 看趨勢、週期 |
| 識別碼 | 訂單編號、會員編號 | **只能數有幾個，不能加總或平均** |

下面這個小工具會自動幫你判斷，以後遇到任何資料都能用：
'''),
        code(HELPER),
        code('''
daily = pd.read_csv('茶語時光_每日營收_2024.csv', parse_dates=['日期'])
orders = pd.read_csv('茶語時光_訂單抽樣_2024-07.csv', parse_dates=['訂單時間'])
認識資料(orders)
'''),
        md('''
## 2. 畫圖之前，先問 AI：「這份資料可以回答哪些問題？」

把下一格印出的文字複製給 AI，並加上這段提示詞：

> **📋 提示詞**：「你是資深資料分析師。以下是手搖飲店 7 月訂單資料的欄位說明與前 5 列（貼上）。請建議 5 個老闆可能關心的商業問題，分別標示屬於『比較、組成、分布、關係、趨勢』哪一類，並建議每個問題適合的圖表與要避免的畫法。」
'''),
        code('''
說明 = 資料說明給AI(orders, '茶語時光 2024 年 7 月訂單抽樣（一列＝一筆訂單中的一個品項）')
'''),
        md('''
## 3. 五類問題 × 五種圖表

| 問題類型 | 老闆會怎麼問 | 分析方法 | 建議圖表 | 避免 |
| --- | --- | --- | --- | --- |
| **比較** | 哪家店賣最多？ | `groupby().sum()` + 排序 | 排序長條圖 | 沒排序、Y 軸不從 0 開始 |
| **組成** | 各付款方式佔幾成？ | `value_counts(normalize=True)` | 百分比長條；5 類以內才用圓餅 | 10 塊的圓餅圖 |
| **分布** | 客人通常花多少？ | `describe()`、中位數 | 直方圖、盒鬚圖 | 只報平均數 |
| **關係** | 越熱賣越多嗎？ | `corr()` | 散佈圖 | 把相關說成因果 |
| **趨勢** | 營收在成長嗎？ | `resample()`、`rolling()` | 折線圖 | 用折線連接類別 |
'''),
        code('''
import os
import matplotlib.pyplot as plt
os.makedirs('給AI的圖表', exist_ok=True)
per_order = orders.groupby(['訂單編號', '門市', '付款方式'], as_index=False)['金額'].sum()   # 每筆訂單的總金額

fig, axes = plt.subplots(2, 3, figsize=(18, 10))

# 比較：各店全年營收（排序長條圖）
(daily.groupby('門市')['營收'].sum().sort_values() / 10000).plot.barh(ax=axes[0, 0], color='#8B5E3C')
axes[0, 0].set_title('比較：2024 各門市營收（萬元）')

# 組成：付款方式占比（排序的百分比長條圖）
pay = per_order['付款方式'].value_counts(normalize=True).sort_values() * 100
pay.plot.barh(ax=axes[0, 1], color='#C8A27C')
axes[0, 1].set_title('組成：7 月付款方式占比（%）')

# 分布：每筆訂單金額（直方圖 + 平均與中位數）
per_order['金額'].plot.hist(ax=axes[0, 2], bins=30, color='#E8D5B7', edgecolor='white')
axes[0, 2].axvline(per_order['金額'].mean(), color='red', linestyle='--', label=f"平均 {per_order['金額'].mean():.0f}")
axes[0, 2].axvline(per_order['金額'].median(), color='green', linestyle='--', label=f"中位數 {per_order['金額'].median():.0f}")
axes[0, 2].legend()
axes[0, 2].set_title('分布：每筆訂單金額')

# 關係：最高溫 vs. 杯數（散佈圖）
daily.plot.scatter(x='最高溫', y='杯數', ax=axes[1, 0], alpha=0.3)
axes[1, 0].set_title(f"關係：最高溫 vs. 杯數（相關係數 {daily['最高溫'].corr(daily['杯數']):.2f}）")

# 趨勢：全品牌每月營收（折線圖）
(daily.set_index('日期')['營收'].resample('ME').sum() / 10000).plot(ax=axes[1, 1], marker='o')
axes[1, 1].set_title('趨勢：全品牌每月營收（萬元）')

axes[1, 2].axis('off')
axes[1, 2].text(0.05, 0.5, '同一份資料\\n問題不同，圖就不同\\n\\n比較 → 長條\\n組成 → 百分比長條\\n分布 → 直方圖\\n關係 → 散佈圖\\n趨勢 → 折線圖',
                fontsize=16, va='center')
plt.tight_layout()
plt.savefig('給AI的圖表/五類問題五張圖.png', dpi=150, bbox_inches='tight')
plt.show()
'''),
        md('''
> 💡 **看懂結果**：逢甲店營收最高；現金仍是最多人用的付款方式（約三成）；訂單金額的「平均」被少數大單拉高，**中位數**更能代表一般客人；氣溫和杯數呈正相關（約 0.39，因為不同門市的規模混在一起，相關程度被稀釋）；營收夏天最高，7 月因凱米颱風而低於 6 月與 8 月。
'''),
        md('''
## 4. 錯誤示範 vs. 正確示範

同樣的數字，畫錯了就會誤導人。下面四組請先自己判斷哪裡有問題，再把圖交給 AI 問問看。
'''),
        code('''
store_rev = daily.groupby('門市')['營收'].sum() / 10000
items = orders.groupby('品項')['數量'].sum().sort_values(ascending=False)

fig, axes = plt.subplots(4, 2, figsize=(14, 20))

# ① Y 軸被截斷：差距看起來被誇大好幾倍
axes[0, 0].bar(store_rev.index, store_rev.values, color='gray')
axes[0, 0].set_ylim(store_rev.min() * 0.97, store_rev.max() * 1.01)
axes[0, 0].set_title('錯 1：Y 軸不從 0 開始，差距被誇大')
axes[0, 1].bar(store_rev.sort_values(ascending=False).index, store_rev.sort_values(ascending=False).values, color='#8B5E3C')
axes[0, 1].set_title('對 1：Y 軸從 0 開始，並由大到小排序')

# ② 太多塊的圓餅圖
axes[1, 0].pie(items.values, labels=items.index, textprops={'fontsize': 9})
axes[1, 0].set_title('錯 2：10 塊的圓餅圖，很難比較大小')
items.sort_values().plot.barh(ax=axes[1, 1], color='#C8A27C')
axes[1, 1].set_title('對 2：排序的水平長條圖')

# ③ 用折線連接「類別」：門市之間沒有先後順序
axes[2, 0].plot(store_rev.index, store_rev.values, marker='o', color='gray')
axes[2, 0].set_title('錯 3：折線暗示門市之間有「趨勢」')
store_rev.sort_values().plot.barh(ax=axes[2, 1], color='#8B5E3C')
axes[2, 1].set_title('對 3：類別比較用長條圖')

# ④ 只看平均：被少數大單誤導
po = per_order['金額']
axes[3, 0].bar(['平均客單價'], [po.mean()], color='gray', width=0.4)
axes[3, 0].set_title(f'錯 4：只報平均 {po.mean():.0f} 元，看不到全貌')
axes[3, 1].boxplot(po)
axes[3, 1].set_title(f'對 4：盒鬚圖——中位數 {po.median():.0f} 元，上方還有一群大額訂單')

plt.tight_layout()
plt.savefig('給AI的圖表/錯誤與正確示範.png', dpi=150, bbox_inches='tight')
plt.show()
'''),
        md('''
## 5. 把圖表交給 AI：解讀、診斷、改良

**怎麼給？** 對圖表按右鍵 →「複製圖片」，貼到 ChatGPT、Claude 或 Gemini 的對話框；或下載 `給AI的圖表/` 資料夾中的圖片後上傳。

| 用途 | 提示詞範本 |
| --- | --- |
| 🔎 **解讀** | 「這是手搖飲店 2024 年的五張分析圖（附圖）。請用白話列出 3 個最重要的發現，並說明是從哪張圖看出來的，最後給老闆 1 個具體建議。」 |
| 🩺 **診斷** | 「請用資料視覺化的專業標準檢查這張圖：有沒有誤導、難讀、或缺少的元素（標題、單位、排序、Y 軸起點）？請條列並說明怎麼改。」 |
| 🛠️ **改良** | 「請提供改良後的 matplotlib 程式碼，使用繁體中文標題與座標軸名稱。我的資料欄位是：（貼上欄位名稱）。」 |
| 🎯 **選圖** | 「我想讓主管一眼看出『哪一家店營收最高』，這張圓餅圖適合嗎？如果不適合，請推薦更好的圖表並說明理由。」 |

> **AI 回覆範例（示意）**——把「錯 1」那張圖交給 AI 診斷時，好的 AI 回答應該包含：
> - 「Y 軸從約 675 萬開始，而不是從 0 開始，讓台南成大店看起來只有台中逢甲店的一小截；實際上兩者只差約 42%（696 萬 vs. 991 萬）。」
> - 「長條沒有排序，讀者要自己找最高的門市。建議由大到小排序，並在長條上標示數值。」
> - 「標題沒有說明單位（萬元）與期間（2024 年）。」
'''),
        md('''
## 6. 驗證 AI：用 pandas 核對每一個數字

AI 看圖時會「目測」，常常把數字讀錯，甚至把兩根長條看反。**AI 說的每個數字，都要用程式核對；AI 給的建議，要用你的商業常識判斷。**
'''),
        code('''
print('▶ 各門市營收（萬元）：\\n', store_rev.sort_values(ascending=False).round(0))
print('\\n▶ 最高與最低門市差距：', f"{(store_rev.max() / store_rev.min() - 1) * 100:.0f}%")
print('\\n▶ 訂單金額：平均', round(po.mean()), '／中位數', po.median(), '／最大', po.max())
print('\\n▶ 付款方式占比 %：\\n', pay.sort_values(ascending=False).round(1))
'''),
        md('''
## 7. 畫完圖的檢查清單

- [ ] 我先判斷了每一欄的型態，沒有把識別碼拿去加總或平均。
- [ ] 我能說出這張圖在回答哪一類問題（比較、組成、分布、關係、趨勢）。
- [ ] 標題說得出重點，座標軸有名稱與單位。
- [ ] 長條圖的 Y 軸從 0 開始，類別有排序。
- [ ] 比較不同大小的群體時，用的是「比例」而不是「次數」。
- [ ] 我把圖交給 AI 解讀與診斷過，並**用 pandas 核對了 AI 說的數字**。

---

## ✍️ 練習題

1. 「哪個時段最忙？」屬於哪一類問題？用 `orders` 畫出來，並把圖交給 AI 解讀。
2. 「會員和非會員的客單價有差嗎？」該用什麼圖？畫出來後，請 AI 診斷你的圖。
3. 打開學生素材的「陌生資料挑戰」，用空氣品質資料走一次完整流程。
'''),
        md('## 🔑 參考解答（先自己試試看！）'),
        code('''
# 練習 1：比較（或趨勢）——各小時訂單數，用長條圖（小時有順序，依小時排列）
by_hour = orders.groupby(orders['訂單時間'].dt.hour)['訂單編號'].nunique()
ax = by_hour.plot.bar(color='#8B5E3C', rot=0, title='7 月各小時訂單數（抽樣）', figsize=(9, 4))
ax.set_xlabel('小時'); ax.set_ylabel('訂單數')
plt.savefig('給AI的圖表/各小時訂單數.png', dpi=150, bbox_inches='tight')
plt.show()

# 練習 2：比較 + 分布——會員 vs. 非會員的訂單金額，用盒鬚圖
member = orders.groupby(['訂單編號', '會員'], as_index=False)['金額'].sum()
member.boxplot(column='金額', by='會員', grid=False, figsize=(7, 4))
plt.suptitle(''); plt.title('會員(Y) vs. 非會員(N) 每筆訂單金額')
plt.show()
print(member.groupby('會員')['金額'].median())
'''),
    ]
    from nbtools import save_notebook
    save_notebook(cells, chapter_dir / 'README.ipynb')
