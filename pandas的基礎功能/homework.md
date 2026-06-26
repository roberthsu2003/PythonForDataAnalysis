# Python 課堂練習設計

## 今日教學重點

整理資料(使用 pandas 讀取 CSV、設定欄位名稱、刪除不需要的列、重設索引、挑選需要的欄位)

---

# 課堂範例回顧(學生剛才已練習)

## 原始程式

```python
import pandas as pd
import numpy as np
dataFrame = pd.read_csv('各鄉鎮市區人口密度.csv')
dataFrame.columns = dataFrame.loc[0]
dataFrame = dataFrame.drop(0)
dataFrame.drop([371, 372, 373, 374, 375], inplace=True)
rowCount, columnCount = dataFrame.shape
dataFrame.index = range(rowCount)
dataFrame1 = dataFrame.reindex(columns=['區域別', '年底人口數', '土地面積'])
```

## 使用的 Python 技術

- `import pandas as pd`、`import numpy as np`
- `pd.read_csv()` 讀取 CSV 檔
- `dataFrame.loc[0]` 取出某一列
- `dataFrame.columns = ...` 重新設定欄位名稱
- `dataFrame.drop(...)` 刪除指定的列(含 `inplace=True`)
- `dataFrame.shape` 取得列數與欄數
- `dataFrame.index = range(...)` 重設索引
- `dataFrame.reindex(columns=[...])` 挑選並重排欄位

## 學習目標

學生可以學會:

- 用 pandas 把一份「原始、含雜訊」的 CSV 整理成乾淨的資料表
- 處理「真正的欄位名稱不在第一列」的情況
- 刪除統計合計列、來源說明列等不需要的資料
- 重設索引並只保留分析需要的欄位

---

# 本次練習題目(全新題目,與課堂範例不同)

> 說明:以下是針對相同教學重點設計的「新題目」,情境與資料和課堂範例不同,但用到的 pandas 整理資料語法一致。

## 題目敘述

學校圖書館提供了一份「各班圖書借閱統計」CSV 檔(`各班圖書借閱統計.csv`)。這份檔案的格式和課堂的人口密度檔很像,有幾個麻煩的地方:

- CSV 第一行的英文代碼(`stat_year`、`class_id`…)會被 pandas 當成欄位名稱讀進來,**真正的中文欄位名稱其實在第 0 列**(`統計年`、`班級`、`學生人數`…)。
- 資料最後有一列是「合計」,以及 4 列說明文字(資料來源、製表日期、備註、僅供教學使用),這些都不是班級資料,需要刪掉。

請寫一支程式,把這份 CSV 整理乾淨,最後只保留「班級」「學生人數」「借閱冊數」三個欄位,並讓索引從 0 開始連續編號。

## 與課堂範例的對應

- 沿用的語法/概念:`read_csv`、用 `loc` 取列當欄位名、`drop` 刪列、`shape` 取列數、`index = range(...)` 重設索引、`reindex(columns=...)` 挑欄位
- 換掉的部分:情境從「人口密度」換成「圖書借閱」;要刪除的列位置不同(合計列 + 說明列);最後保留的欄位換成班級相關欄位

---

# 學生練習:半成品

以下兩種版本皆針對「本次練習題目」,教師可依學生程度選用。

## 版本 A:程式碼半成品(挖空補完)

適合剛接觸本主題的學生:程式架構已給,補完標示處即可。

### 任務說明

請完成以下程式中標示 `# 請完成` 的部分。

```python
import pandas as pd
import numpy as np

# 讀取 CSV 檔
dataFrame = pd.read_csv('各班圖書借閱統計.csv')

# 第 0 列(index 為 0)才是真正的中文欄位名稱,把它設為欄位名
dataFrame.columns = dataFrame.loc[0]

# 刪除第 0 列(已經拿來當欄位名,資料中不需要重複)
dataFrame = dataFrame.drop(0)

# 提示:整理後資料最後面有「合計列」與 4 列說明文字要刪掉
# 先印出 dataFrame 看看那些列的 index 是多少
print(dataFrame)

# 請完成:刪除合計列與 4 列說明文字(用 drop,可加 inplace=True)
# dataFrame.drop([______], inplace=True)


# 取得目前的列數與欄數
rowCount, columnCount = dataFrame.shape

# 請完成:把索引重設為從 0 開始的連續編號
# dataFrame.index = ______


# 請完成:只保留「班級」「學生人數」「借閱冊數」三個欄位
# dataFrame1 = dataFrame.reindex(columns=[______])


print(dataFrame1)
```

學生需要完成:

1. 找出合計列與說明列的 index,用 `drop` 把它們刪掉
2. 用 `range(rowCount)` 重設索引
3. 用 `reindex(columns=[...])` 挑出指定的三個欄位

### 完成後參考程式碼(教師用,勿發給學生)

> 此區塊僅供教師參考核對,是版本 A 補完後的完整正確程式。

```python
import pandas as pd
import numpy as np

# 讀取 CSV 檔
dataFrame = pd.read_csv('各班圖書借閱統計.csv')

# 第 0 列(index 為 0)才是真正的中文欄位名稱,把它設為欄位名
dataFrame.columns = dataFrame.loc[0]

# 刪除第 0 列(已經拿來當欄位名,資料中不需要重複)
dataFrame = dataFrame.drop(0)

# 刪除合計列(index 10)與 4 列說明文字(index 11~14)
dataFrame.drop([10, 11, 12, 13, 14], inplace=True)

# 取得目前的列數與欄數
rowCount, columnCount = dataFrame.shape

# 把索引重設為從 0 開始的連續編號
dataFrame.index = range(rowCount)

# 只保留「班級」「學生人數」「借閱冊數」三個欄位
dataFrame1 = dataFrame.reindex(columns=['班級', '學生人數', '借閱冊數'])

print(dataFrame1)
```

## 版本 B:純註解半成品(依註解寫程式)

適合已熟悉本主題、要訓練獨立寫程式的學生:只有註解,沒有程式碼,請依註解逐行寫出完整程式。

### 任務說明

請依照下方每一行註解的說明,寫出對應的 Python 程式碼。

```python
# 匯入 pandas,取別名 pd

# 匯入 numpy,取別名 np

# 用 read_csv 讀取「各班圖書借閱統計.csv」,存進變數 dataFrame

# 真正的中文欄位名稱在 index 為 0 的那一列,用 loc 取出來,設定成 dataFrame 的欄位名稱

# 用 drop 刪除 index 0(已拿來當欄位名,資料中不需要重複)

# 先 print 出 dataFrame,觀察「合計列」與說明文字各自的 index 是多少

# 用 drop 刪除合計列與 4 列說明文字(可加 inplace=True)

# 用 shape 取得列數與欄數,分別存進 rowCount 與 columnCount

# 把 dataFrame 的 index 重設為 range(rowCount),讓編號從 0 開始連續

# 用 reindex(columns=[...]) 只保留「班級」「學生人數」「借閱冊數」三欄,存進 dataFrame1

# print 出 dataFrame1,確認整理結果
```

學生需要依序完成每個步驟的程式碼。

### 完成後參考程式碼(教師用,勿發給學生)

> 此區塊僅供教師參考核對,是依版本 B 註解逐步寫出的完整正確程式。

```python
# 匯入 pandas,取別名 pd
import pandas as pd

# 匯入 numpy,取別名 np
import numpy as np

# 用 read_csv 讀取「各班圖書借閱統計.csv」,存進變數 dataFrame
dataFrame = pd.read_csv('各班圖書借閱統計.csv')

# 真正的中文欄位名稱在 index 為 0 的那一列,用 loc 取出來,設定成 dataFrame 的欄位名稱
dataFrame.columns = dataFrame.loc[0]

# 用 drop 刪除 index 0(已拿來當欄位名,資料中不需要重複)
dataFrame = dataFrame.drop(0)

# 先 print 出 dataFrame,觀察「合計列」與說明文字各自的 index 是多少
print(dataFrame)

# 用 drop 刪除合計列與 4 列說明文字(可加 inplace=True)
dataFrame.drop([10, 11, 12, 13, 14], inplace=True)

# 用 shape 取得列數與欄數,分別存進 rowCount 與 columnCount
rowCount, columnCount = dataFrame.shape

# 把 dataFrame 的 index 重設為 range(rowCount),讓編號從 0 開始連續
dataFrame.index = range(rowCount)

# 用 reindex(columns=[...]) 只保留「班級」「學生人數」「借閱冊數」三欄,存進 dataFrame1
dataFrame1 = dataFrame.reindex(columns=['班級', '學生人數', '借閱冊數'])

# print 出 dataFrame1,確認整理結果
print(dataFrame1)
```

---

# 延伸挑戰題

## 題目

整理乾淨後(`dataFrame1`),再多做一步分析:

1. 「學生人數」和「借閱冊數」目前是文字型態,請把它們轉成數字。
2. 新增一個欄位「平均每人借閱」=借閱冊數 ÷ 學生人數,四捨五入到小數點 1 位。
3. 找出「平均每人借閱」最高的班級,並把整張表依「平均每人借閱」由高到低排序。

## 提示

可以思考:

- 怎麼把整個欄位從文字轉成整數?(pandas 有 `astype`,或 `pd.to_numeric`)
- 新欄位可以用 `dataFrame1['平均每人借閱'] = ...` 直接算出來
- 排序可以用 `sort_values()`,找最大值可以用 `idxmax()` 或排序後取第一列

---

# 思考問題

1. 課堂範例和這次練習,都要「先把某一列拿來當欄位名,再把那一列刪掉」。如果忘了刪掉那一列,後面的資料會多出什麼問題?
2. 程式裡 `dataFrame.index = range(rowCount)` 這行如果拿掉,直接 `reindex` 挑欄位,結果會差在哪裡?為什麼重設索引很重要?
3. 刪除合計列和說明列時,我們是直接寫死 index 編號(像 `[10, 11, 12, 13, 14]`)。如果之後資料的班級數量變多,這種寫法會有什麼風險?有沒有更穩定的判斷方式?

---

# 建議查詢方向

學生可以搜尋:

1. 搜尋「pandas read_csv 中文欄位 亂碼 encoding」了解讀檔編碼問題
2. 搜尋「pandas drop 刪除指定列 inplace」了解刪列的不同寫法
3. 搜尋「pandas 欄位 文字轉數字 astype to_numeric」為延伸挑戰做準備

---

# 教師備課備註

本練習主要訓練:

- 把含雜訊的原始 CSV 整理成乾淨資料表的完整流程(設定欄位名 → 刪列 → 重設索引 → 挑欄位)
- 觀察 index 再決定要刪哪幾列的習慣

避免加入:

- 尚未教學的內容(如 groupby、merge、繪圖)
- 過度複雜的寫法(維持與課堂範例相同的 pandas 基本操作)

備註:本練習附帶資料檔 `各班圖書借閱統計.csv`,格式刻意做得和課堂的人口密度檔相似(欄位名在第二列、最後有合計與說明列),方便學生套用相同整理步驟。實際發給學生時,請移除「完成後參考程式碼(教師用)」兩個區塊。