

# Python 課堂練習設計

## 今日教學重點

使用 `query()` 搜尋資料(條件篩選、`and` 多條件、`@變數`、與 `max()` 等聚合搭配)

---

# 課堂範例回顧(學生剛才已練習)

## 原始程式

```python
import pandas as pd
dataFrame = pd.read_csv('world.csv')
allDataFrame = dataFrame.reindex(columns=['洲名','國家','日期','總確診數','新增確診數','總人口數','解封指數'])
taiwan = allDataFrame.query('國家=="台灣"')
taiwan1 = allDataFrame.query('國家=="台灣" and 新增確診數>=10000')
max = allDataFrame.query('國家=="台灣"')['新增確診數'].max()
allDataFrame.query('新增確診數==@max')
allDataFrame.query('國家=="台灣" and 日期>="2022-01-01"')
```

## 使用的 Python 技術

- `pd.read_csv()` 讀檔
- `query()` 單一條件篩選
- `query()` 用 `and` 串接多條件
- 數值比較(`>=`、`==`)
- 字串條件(`日期>="2022-01-01"`)
- `max()` 聚合
- `@變數` 在 query 中引用 Python 變數

## 學習目標

學生可以學會:

- 用 `query()` 寫出單一與多重條件
- 在 query 中比較數值與比較字串(日期)
- 把聚合結果存成變數,再用 `@` 帶回 query 篩選

---

# 本次練習題目(全新題目,與課堂範例不同)

> 說明:換成「世界城市天氣紀錄」資料,情境與欄位不同,但 `query()` 的用法完全一致。

## 題目敘述

附檔 `weather.csv` 記錄 10 個城市在 2024 年 1~6 月的天氣,欄位有:`洲名`、`城市`、`月份`、`平均氣溫`、`降雨量`、`濕度`。請用 `query()` 完成下列查詢:

1. 篩選出「台北」的所有紀錄。
2. 篩選出「台北」且「降雨量大於等於 100」的紀錄。
3. 找出「台北」降雨量的最大值,並用 `@` 把這個值帶回 query,查出是哪一個月份下最多雨。
4. 篩選出「亞洲」且「月份大於等於 2024-04」的紀錄。

## 與課堂範例的對應

- 沿用的語法/概念:`read_csv`、`query` 單條件與 `and` 多條件、數值比較、字串(月份)比較、`max()`、`@變數`。
- 換掉的部分:資料從疫情換成天氣;`國家→城市`、`日期→月份`、`新增確診數→降雨量`。

---

# 學生練習:半成品

以下兩種版本皆針對「本次練習題目」,教師可依學生程度選用。

## 版本 A:程式碼半成品(挖空補完)

適合剛接觸本主題的學生:程式架構已給,補完標示處即可。

### 任務說明

請完成以下程式中標示 `# 請完成` 的部分。

```python
import pandas as pd

# 讀取天氣資料
dataFrame = pd.read_csv('weather.csv')

# (1) 篩選出「台北」的所有紀錄
taipei = dataFrame.query('______')   # 請完成:城市等於台北
print(taipei)

# (2) 篩選出「台北」且「降雨量 >= 100」的紀錄
taipei_rain = dataFrame.query('______')   # 請完成:兩個條件用 and 串接
print(taipei_rain)

# (3) 找出台北降雨量的最大值,再用 @ 帶回 query
max_rain = dataFrame.query('城市=="台北"')['______'].______   # 請完成:取降雨量的最大值
result = dataFrame.query('城市=="台北" and ______')           # 請完成:降雨量 == @max_rain
print(result)

# (4) 篩選「亞洲」且「月份 >= 2024-04」
asia = dataFrame.query('______')   # 請完成:洲名等於亞洲 且 月份大於等於 2024-04
print(asia)
```

學生需要完成:

1. 寫出單一條件與 `and` 多條件的 query 字串。
2. 用 `['降雨量'].max()` 取最大值並存進變數。
3. 在 query 中用 `@max_rain` 帶回變數,並寫出字串(月份)比較條件。

### 完成後參考程式碼(教師用,勿發給學生)

> 此區塊僅供教師參考核對,是版本 A 補完後的完整正確程式。

```python
import pandas as pd

dataFrame = pd.read_csv('weather.csv')

taipei = dataFrame.query('城市=="台北"')
print(taipei)

taipei_rain = dataFrame.query('城市=="台北" and 降雨量>=100')
print(taipei_rain)

max_rain = dataFrame.query('城市=="台北"')['降雨量'].max()
result = dataFrame.query('城市=="台北" and 降雨量==@max_rain')
print(result)

asia = dataFrame.query('洲名=="亞洲" and 月份>="2024-04"')
print(asia)
```

## 版本 B:純註解半成品(依註解寫程式)

適合已熟悉本主題、要訓練獨立寫程式的學生:只有註解,沒有程式碼,請依註解逐行寫出完整程式。

### 任務說明

請依照下方每一行註解的說明,寫出對應的 Python 程式碼。

```python
# 匯入 pandas,慣用別名 pd


# 讀取 weather.csv,存成 dataFrame


# (1) 用 query 篩選出城市等於「台北」的紀錄,存成 taipei,並印出


# (2) 用 query 篩選出城市等於「台北」且降雨量大於等於 100 的紀錄,存成 taipei_rain,並印出


# (3) 先用 query 取出台北的資料,再取出「降雨量」欄位的最大值,存成 max_rain


# (3) 用 query 篩選城市等於台北、且降雨量等於 max_rain(用 @max_rain),存成 result,並印出


# (4) 用 query 篩選洲名等於「亞洲」且月份大於等於 "2024-04",存成 asia,並印出

```

學生需要依序完成每個步驟的程式碼。

### 完成後參考程式碼(教師用,勿發給學生)

> 此區塊僅供教師參考核對,是依版本 B 註解逐步寫出的完整正確程式。

```python
# 匯入 pandas,慣用別名 pd
import pandas as pd

# 讀取 weather.csv,存成 dataFrame
dataFrame = pd.read_csv('weather.csv')

# (1) 用 query 篩選出城市等於「台北」的紀錄,存成 taipei,並印出
taipei = dataFrame.query('城市=="台北"')
print(taipei)

# (2) 用 query 篩選出城市等於「台北」且降雨量大於等於 100 的紀錄,存成 taipei_rain,並印出
taipei_rain = dataFrame.query('城市=="台北" and 降雨量>=100')
print(taipei_rain)

# (3) 先用 query 取出台北的資料,再取出「降雨量」欄位的最大值,存成 max_rain
max_rain = dataFrame.query('城市=="台北"')['降雨量'].max()

# (3) 用 query 篩選城市等於台北、且降雨量等於 max_rain(用 @max_rain),存成 result,並印出
result = dataFrame.query('城市=="台北" and 降雨量==@max_rain')
print(result)

# (4) 用 query 篩選洲名等於「亞洲」且月份大於等於 "2024-04",存成 asia,並印出
asia = dataFrame.query('洲名=="亞洲" and 月份>="2024-04"')
print(asia)
```

---

# 延伸挑戰題

## 題目

讓使用者用 `input()` 輸入任一個城市名稱,程式自動查出該城市「平均氣溫最高」的那一個月份,並印出該月的氣溫、降雨量與濕度。若使用者輸入的城市不存在,要印出「查無此城市」。

## 提示

可以思考:

- 如何把 `input()` 取得的字串安全地放進 query?(用 `@變數`)
- 先用 query 篩出該城市,再用 `['平均氣溫'].max()` 找最高溫。
- 篩選後若 DataFrame 是空的(`len(df)==0` 或 `df.empty`),代表查無此城市。

---

# 思考問題

1. `query('城市=="台北" and 降雨量>=100')` 中,如果把 `and` 改成 `or`,結果會有什麼不同?為什麼?
2. 為什麼第 (3) 題要先把 `max()` 存成 `max_rain` 變數,再用 `@max_rain` 帶回 query?不存變數能不能直接寫?
3. 月份是文字(像 `"2024-04"`),為什麼還能用 `>=` 比較大小?換成別種日期寫法(例如 `2024/4`)還比得出來嗎?

---

# 建議查詢方向

學生可以搜尋:

1. 搜尋「pandas query 多條件 and or 寫法」
2. 搜尋「pandas query @ 引用外部變數」
3. 搜尋「pandas 取某欄位最大值 max」

---

# 教師備課備註

本練習主要訓練:

- `query()` 的單條件、多條件與 `@變數` 用法,搭配 `max()` 聚合

