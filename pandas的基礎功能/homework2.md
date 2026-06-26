# Python 課堂練習設計

## 今日教學重點

`sum()`、`mean()`、`rand()`(亂數產生)、`sort_values()`,以及搭配 `rank()` 進行排名。

---

# 課堂範例回顧(學生剛才已練習)

## 原始程式

```python
#練習建立學生成績單
import numpy as np
import pandas as pd

scores = np.random.randint(50,101,size=(50,5))
scores_pd = pd.DataFrame(scores,columns=['國文', '英文', '數學', '地理', '歷史'],index=range(1,51))
scores_pd.index.name="學號"
scores_pd.columns.name="科目"
sum_values = scores_pd.sum(axis=1)
avg_values = scores_pd.mean(axis=1)
rank_values = sum_values.rank(method='first',ascending=False)
scores_pd['總分'] = sum_values
scores_pd['平均'] = avg_values
scores_pd['排名'] = rank_values
scores_pd
scores_pd.sort_values(by='排名')
```

## 使用的 Python 技術

- `numpy` 亂數產生 `np.random.randint()`
- `pandas` 建立 `DataFrame`,設定 `columns`、`index`、`index.name`、`columns.name`
- `sum(axis=1)`、`mean(axis=1)` 逐列彙總
- `rank(method='first', ascending=False)` 計算排名
- `sort_values(by=...)` 排序

## 學習目標

學生可以學會:

- 用亂數建立一份表格資料並命名欄列
- 用 `sum`、`mean` 沿著列方向(axis=1)做彙總計算
- 用 `rank` 算出名次,並用 `sort_values` 依某欄排序

---

# 本次練習題目(全新題目,與課堂範例不同)

> 說明:以下是針對相同教學重點設計的「新題目」,情境與資料和課堂範例不同,但用到的 Python 語法一致。

## 題目敘述

某飲料連鎖店要統計 8 家分店在「一週七天」的每日營業額。請用亂數產生 8 家分店、週一到週日共 7 天的營業額(每天介於 8000 到 20000 元之間),建立成 DataFrame。接著算出每家分店的「週總營業額」與「日平均營業額」,並依週總營業額由高到低排出「業績排名」,最後依排名排序印出整張表。

## 與課堂範例的對應

- 沿用的語法/概念:`np.random.randint()` 產生亂數、建立 `DataFrame`、`sum(axis=1)`、`mean(axis=1)`、`rank(ascending=False)`、`sort_values(by=...)`
- 換掉的部分:情境由「學生成績」改為「分店營業額」;欄位由 5 個科目改為 7 天;列由 50 位學生改為 8 家分店;數值範圍與意義不同

---

# 學生練習:半成品

以下兩種版本皆針對「本次練習題目」,教師可依學生程度選用。

## 版本 A:程式碼半成品(挖空補完)

適合剛接觸本主題的學生:程式架構已給,補完標示處即可。

### 任務說明

請完成以下程式中標示 `# 請完成` 的部分。

```python
# 飲料連鎖店一週營業額統計
import numpy as np
import pandas as pd

# 用亂數產生 8 家分店、7 天的營業額,範圍 8000~20000
sales = np.random.randint(8000, 20001, size=(8, 7))

days = ['週一', '週二', '週三', '週四', '週五', '週六', '週日']
sales_pd = pd.DataFrame(sales, columns=days, index=range(1, 9))
sales_pd.index.name = "分店編號"
sales_pd.columns.name = "星期"

# 請完成:算出每家分店的週總營業額(提示:沿著列方向加總 axis=1)
total_values = # 請完成

# 請完成:算出每家分店的日平均營業額
avg_values = # 請完成

# 請完成:依週總營業額由高到低排名(分數高的排第 1)
rank_values = # 請完成

sales_pd['週總額'] = total_values
sales_pd['日平均'] = avg_values
sales_pd['業績排名'] = rank_values

# 請完成:依業績排名排序後印出
print(  # 請完成
)
```

學生需要完成:

1. 用 `sum(axis=1)` 算出週總額
2. 用 `mean(axis=1)` 算出日平均,並用 `rank()` 算排名
3. 用 `sort_values(by='業績排名')` 排序印出

### 完成後參考程式碼(教師用,勿發給學生)

> 此區塊僅供教師參考核對,是版本 A 補完後的完整正確程式。

```python
# 飲料連鎖店一週營業額統計
import numpy as np
import pandas as pd

sales = np.random.randint(8000, 20001, size=(8, 7))

days = ['週一', '週二', '週三', '週四', '週五', '週六', '週日']
sales_pd = pd.DataFrame(sales, columns=days, index=range(1, 9))
sales_pd.index.name = "分店編號"
sales_pd.columns.name = "星期"

total_values = sales_pd.sum(axis=1)
avg_values = sales_pd.mean(axis=1)
rank_values = total_values.rank(method='first', ascending=False)

sales_pd['週總額'] = total_values
sales_pd['日平均'] = avg_values
sales_pd['業績排名'] = rank_values

print(sales_pd.sort_values(by='業績排名'))
```

## 版本 B:純註解半成品(依註解寫程式)

適合已熟悉本主題、要訓練獨立寫程式的學生:只有註解,沒有程式碼,請依註解逐行寫出完整程式。

### 任務說明

請依照下方每一行註解的說明,寫出對應的 Python 程式碼。

```python
# 匯入 numpy 並取別名 np

# 匯入 pandas 並取別名 pd


# 用亂數產生 8 家分店、7 天的營業額,範圍 8000~20000(size=(8, 7))


# 建立星期欄位名稱的清單:週一到週日


# 用上面的亂數與星期清單建立 DataFrame,index 設為 1~8


# 設定 index 名稱為「分店編號」

# 設定 columns 名稱為「星期」


# 算出每家分店的週總營業額(沿列方向加總 axis=1)


# 算出每家分店的日平均營業額(沿列方向平均 axis=1)


# 依週總營業額由高到低算出排名(ascending=False)


# 把週總額加入 DataFrame 成為新欄位

# 把日平均加入 DataFrame 成為新欄位

# 把業績排名加入 DataFrame 成為新欄位


# 依業績排名排序後印出整張表
```

學生需要依序完成每個步驟的程式碼。

### 完成後參考程式碼(教師用,勿發給學生)

> 此區塊僅供教師參考核對,是依版本 B 註解逐步寫出的完整正確程式。

```python
# 匯入 numpy 並取別名 np
import numpy as np
# 匯入 pandas 並取別名 pd
import pandas as pd

# 用亂數產生 8 家分店、7 天的營業額,範圍 8000~20000(size=(8, 7))
sales = np.random.randint(8000, 20001, size=(8, 7))

# 建立星期欄位名稱的清單:週一到週日
days = ['週一', '週二', '週三', '週四', '週五', '週六', '週日']

# 用上面的亂數與星期清單建立 DataFrame,index 設為 1~8
sales_pd = pd.DataFrame(sales, columns=days, index=range(1, 9))

# 設定 index 名稱為「分店編號」
sales_pd.index.name = "分店編號"
# 設定 columns 名稱為「星期」
sales_pd.columns.name = "星期"

# 算出每家分店的週總營業額(沿列方向加總 axis=1)
total_values = sales_pd.sum(axis=1)
# 算出每家分店的日平均營業額(沿列方向平均 axis=1)
avg_values = sales_pd.mean(axis=1)
# 依週總營業額由高到低算出排名(ascending=False)
rank_values = total_values.rank(method='first', ascending=False)

# 把週總額加入 DataFrame 成為新欄位
sales_pd['週總額'] = total_values
# 把日平均加入 DataFrame 成為新欄位
sales_pd['日平均'] = avg_values
# 把業績排名加入 DataFrame 成為新欄位
sales_pd['業績排名'] = rank_values

# 依業績排名排序後印出整張表
print(sales_pd.sort_values(by='業績排名'))
```

---

# 延伸挑戰題

## 題目

在上面的營業額表完成後,進一步找出:(1) 哪一天(週一到週日)全公司所有分店加總營業額最高?(2) 列出「日平均」最高的前 3 家分店。

## 提示

可以思考:

- 要算「每一天的全公司加總」,加總方向應該是 axis=0 還是 axis=1?
- `sort_values` 排序後,如何只取前幾筆?可查 `head()`
- 找最大值對應的欄位,可查 `idxmax()`

---

# 思考問題

1. `sum(axis=1)` 和 `sum(axis=0)` 算出來的意義有什麼不同?在這題各代表什麼?
2. `rank()` 裡如果把 `ascending=False` 改成 `ascending=True`,排名結果會怎麼變?業績最好的分店會變成第幾名?
3. `sort_values(by='業績排名')` 排序後,原本的 DataFrame `sales_pd` 內容有被改變嗎?如果想真正改變原表要怎麼做?

---

# 建議查詢方向

學生可以搜尋:

1. 搜尋 `pandas sum axis 0 1 差別`
2. 搜尋 `pandas rank method ascending 用法`
3. 搜尋 `pandas sort_values 取前幾筆 head`

---

# 教師備課備註

本練習主要訓練:

- 沿用成績單範例的彙總與排名邏輯,遷移到不同情境(分店營業額),強化 `sum`、`mean`、`rank`、`sort_values` 與亂數建表的綜合運用

避免加入:

- 尚未教學的內容(如 `groupby`、繪圖)
- 過度複雜的寫法