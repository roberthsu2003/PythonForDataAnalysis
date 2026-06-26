# Python 課堂練習設計

## 今日教學重點

`DataFrame.apply()`:對 DataFrame 的每一個欄位(或列)套用自訂函式,並回傳統計結果組成的新 DataFrame。

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
#使用apply(),做統計動作,產生新的DataFrame

def cal1(s):
    return pd.Series([s.min(),s.max(),s.median()],index=['最低分','最高分','中間值'])
scores_pd.apply(cal1)
```

## 使用的 Python 技術

- `import numpy as np` / `import pandas as pd`
- `np.random.randint()` 產生隨機資料
- `pd.DataFrame()` 建立資料表(設定 columns、index)
- `df.index.name` / `df.columns.name`
- 自訂 function 回傳 `pd.Series`
- `df.apply(func)` 對每一欄套用函式

## 學習目標

學生可以學會:

- 用 `apply()` 把一個函式套用到 DataFrame 的每一欄
- 在函式中回傳 `pd.Series`,讓結果自動組成新的 DataFrame
- 自訂統計指標(不只是內建的 `mean`、`sum`)

---

# 本次練習題目(全新題目,與課堂範例不同)

> 說明:以下是針對相同教學重點設計的「新題目」,情境與資料和課堂範例不同,但用到的 Python 語法一致。

## 題目敘述

某公司有 30 位業務員,記錄了他們在「第一季、第二季、第三季、第四季」四個季度的銷售業績(單位:萬元)。請建立一個 DataFrame,列為業務員編號(1~30),欄為四個季度。

接著使用 `apply()`,針對**每一個季度**(每一欄)計算三項統計指標:該季的「總業績」、「平均業績」與「最高業績」,並把結果組成一個新的 DataFrame。

## 與課堂範例的對應

- 沿用的語法/概念:`np.random.randint()`、`pd.DataFrame()`、`index.name` / `columns.name`、自訂 function 回傳 `pd.Series`、`df.apply(func)`
- 換掉的部分:情境由「學生成績單」改為「業務員季度業績」;欄位由 5 個科目改為 4 個季度;統計指標由「最低分/最高分/中間值」改為「總業績/平均業績/最高業績」

---

# 學生練習:半成品

以下兩種版本皆針對「本次練習題目」,教師可依學生程度選用。

## 版本 A:程式碼半成品(挖空補完)

適合剛接觸本主題的學生:程式架構已給,補完標示處即可。

### 任務說明

請完成以下程式中標示 `# 請完成` 的部分。

```python
# 練習:業務員季度業績統計
import numpy as np
import pandas as pd

# 產生 30 位業務員、4 個季度的隨機業績(10~100 萬元)
sales = np.random.randint(10, 101, size=(30, 4))

# 請完成:建立 DataFrame,欄位為四個季度,index 為 1~30
sales_pd = pd.DataFrame(______, columns=______, index=______)

sales_pd.index.name = "業務員編號"
sales_pd.columns.name = "季度"

# 自訂統計函式:回傳總業績、平均業績、最高業績
def cal(s):
    # 請完成:回傳一個 pd.Series,包含 總業績 / 平均業績 / 最高業績
    return pd.Series([______, ______, ______],
                     index=['總業績', '平均業績', '最高業績'])

# 請完成:用 apply() 對每一欄套用 cal 函式
result = sales_pd.______(______)
print(result)
```

學生需要完成:

1. 用 `sales`、欄位名稱串列、`range(1, 31)` 建立 DataFrame
2. 在函式中用 `s.sum()`、`s.mean()`、`s.max()` 回傳三項指標
3. 呼叫 `sales_pd.apply(cal)`

### 完成後參考程式碼(教師用,勿發給學生)

> 此區塊僅供教師參考核對,是版本 A 補完後的完整正確程式。

```python
# 練習:業務員季度業績統計
import numpy as np
import pandas as pd

# 產生 30 位業務員、4 個季度的隨機業績(10~100 萬元)
sales = np.random.randint(10, 101, size=(30, 4))

# 建立 DataFrame,欄位為四個季度,index 為 1~30
sales_pd = pd.DataFrame(sales,
                        columns=['第一季', '第二季', '第三季', '第四季'],
                        index=range(1, 31))

sales_pd.index.name = "業務員編號"
sales_pd.columns.name = "季度"

# 自訂統計函式:回傳總業績、平均業績、最高業績
def cal(s):
    return pd.Series([s.sum(), s.mean(), s.max()],
                     index=['總業績', '平均業績', '最高業績'])

# 用 apply() 對每一欄套用 cal 函式
result = sales_pd.apply(cal)
print(result)
```

## 版本 B:純註解半成品(依註解寫程式)

適合已熟悉本主題、要訓練獨立寫程式的學生:只有註解,沒有程式碼,請依註解逐行寫出完整程式。

### 任務說明

請依照下方每一行註解的說明,寫出對應的 Python 程式碼。

```python
# 步驟 1:匯入 numpy(別名 np)與 pandas(別名 pd)


# 步驟 2:用 np.random.randint 產生 30 列 4 欄、範圍 10~100 的隨機業績資料


# 步驟 3:用 pd.DataFrame 建立資料表,欄位為四個季度,index 為 1~30


# 步驟 4:設定 index.name 為「業務員編號」


# 步驟 5:設定 columns.name 為「季度」


# 步驟 6:定義函式 cal(s),回傳一個 pd.Series,內容為總業績、平均業績、最高業績


# 步驟 7:用 apply() 對每一欄套用 cal 函式,並把結果存到 result


# 步驟 8:印出 result

```

學生需要依序完成每個步驟的程式碼。

### 完成後參考程式碼(教師用,勿發給學生)

> 此區塊僅供教師參考核對,是依版本 B 註解逐步寫出的完整正確程式。

```python
# 步驟 1:匯入 numpy(別名 np)與 pandas(別名 pd)
import numpy as np
import pandas as pd

# 步驟 2:用 np.random.randint 產生 30 列 4 欄、範圍 10~100 的隨機業績資料
sales = np.random.randint(10, 101, size=(30, 4))

# 步驟 3:用 pd.DataFrame 建立資料表,欄位為四個季度,index 為 1~30
sales_pd = pd.DataFrame(sales,
                        columns=['第一季', '第二季', '第三季', '第四季'],
                        index=range(1, 31))

# 步驟 4:設定 index.name 為「業務員編號」
sales_pd.index.name = "業務員編號"

# 步驟 5:設定 columns.name 為「季度」
sales_pd.columns.name = "季度"

# 步驟 6:定義函式 cal(s),回傳一個 pd.Series,內容為總業績、平均業績、最高業績
def cal(s):
    return pd.Series([s.sum(), s.mean(), s.max()],
                     index=['總業績', '平均業績', '最高業績'])

# 步驟 7:用 apply() 對每一欄套用 cal 函式,並把結果存到 result
result = sales_pd.apply(cal)

# 步驟 8:印出 result
print(result)
```

---

# 延伸挑戰題

## 題目

延續上面的業績資料,改成統計**每一位業務員**(每一列)的「全年總業績」與「全年平均業績」,並新增一欄「達標」:若全年總業績超過 200 萬元就標示「達標」,否則標示「未達標」。

## 提示

可以思考:

- `apply()` 加上 `axis=1` 參數,可以改成對「每一列」套用函式
- 函式內可以用 `if...else` 判斷是否達標
- 如何把計算出來的新欄位加回原本的 DataFrame

---

# 思考問題

1. 課堂範例與本練習都用了 `apply(cal)`,函式 `cal` 收到的參數 `s` 到底是「一欄」還是「一列」?如果想改成對每一列計算,要加上什麼參數?
2. 為什麼函式裡要回傳 `pd.Series` 而不是普通的 `list`?回傳 list 結果會有什麼不同?
3. 如果把 `s.mean()` 改成 `round(s.mean(), 1)`,輸出的平均業績會有什麼變化?為什麼有時需要這樣做?

---

# 建議查詢方向

學生可以搜尋:

1. 搜尋「pandas DataFrame apply axis 0 1 差別」,了解 `axis` 參數如何決定套用方向
2. 搜尋「pandas apply 回傳 Series 自動組成 DataFrame」
3. 搜尋「pandas Series sum mean max 統計方法」

---

# 教師備課備註

本練習主要訓練:

- 用 `apply()` 把自訂函式套用到 DataFrame 每一欄
- 在函式中回傳 `pd.Series` 以產生結構化的統計結果
- 將「成績」情境遷移到「業績」情境,確認學生理解概念而非死背範例

避免加入:

- 尚未教學的內容(如 `groupby`、`lambda` 進階用法)
- 過度複雜的寫法