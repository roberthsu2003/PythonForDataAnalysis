# 05｜連鎖書店季報：三個月訂單合併成一份報表

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/AI%E5%8D%94%E4%BD%9C%E8%B3%87%E6%96%99%E5%88%86%E6%9E%90_12%E5%80%8B%E7%AF%84%E4%BE%8B/05_bookstore_merge/lesson.ipynb) [開啟教材 Notebook](./lesson.ipynb)

你提出需求、看懂結果並驗收；AI 負責寫程式、執行和除錯。先從上方教材 Notebook 的資料下載與讀取起點開始，再依提示詞逐步完成自己的分析與交付成果。

- 任務：concat 上下合併、merge 左右合併與鍵值檢查。
- 交付成果：Excel 季報與對不上清單。
- 學生專案內位置：`05_bookstore_merge/`；共用專案根目錄的 `.venv`。
- 本例完成後：能用自己的話說明分析問題、資料處理步驟與一個發現。

## 資料與問題設定

本教材原創偽資料，三個月訂單共 1,130 筆、門市 6 家、商品 12 項；固定 seed=505。

### 範例檔下載

- [下載 orders_2025_01.csv](https://raw.githubusercontent.com/roberthsu2003/PythonForDataAnalysis/master/AI%E5%8D%94%E4%BD%9C%E8%B3%87%E6%96%99%E5%88%86%E6%9E%90_12%E5%80%8B%E7%AF%84%E4%BE%8B/05_bookstore_merge/data/orders_2025_01.csv)：儲存到學生專案的 `05_bookstore_merge/data/orders_2025_01.csv`。
- [下載 orders_2025_02.csv](https://raw.githubusercontent.com/roberthsu2003/PythonForDataAnalysis/master/AI%E5%8D%94%E4%BD%9C%E8%B3%87%E6%96%99%E5%88%86%E6%9E%90_12%E5%80%8B%E7%AF%84%E4%BE%8B/05_bookstore_merge/data/orders_2025_02.csv)：儲存到學生專案的 `05_bookstore_merge/data/orders_2025_02.csv`。
- [下載 orders_2025_03.csv](https://raw.githubusercontent.com/roberthsu2003/PythonForDataAnalysis/master/AI%E5%8D%94%E4%BD%9C%E8%B3%87%E6%96%99%E5%88%86%E6%9E%90_12%E5%80%8B%E7%AF%84%E4%BE%8B/05_bookstore_merge/data/orders_2025_03.csv)：儲存到學生專案的 `05_bookstore_merge/data/orders_2025_03.csv`。
- [下載 stores.csv](https://raw.githubusercontent.com/roberthsu2003/PythonForDataAnalysis/master/AI%E5%8D%94%E4%BD%9C%E8%B3%87%E6%96%99%E5%88%86%E6%9E%90_12%E5%80%8B%E7%AF%84%E4%BE%8B/05_bookstore_merge/data/stores.csv)：儲存到學生專案的 `05_bookstore_merge/data/stores.csv`。
- [下載 products.csv](https://raw.githubusercontent.com/roberthsu2003/PythonForDataAnalysis/master/AI%E5%8D%94%E4%BD%9C%E8%B3%87%E6%96%99%E5%88%86%E6%9E%90_12%E5%80%8B%E7%AF%84%E4%BE%8B/05_bookstore_merge/data/products.csv)：儲存到學生專案的 `05_bookstore_merge/data/products.csv`。
- [線上閱讀偽資料卡與欄位字典](./data/DATA_CARD.md)：直接在 GitHub 閱讀，不必下載。

若連結顯示文字，使用瀏覽器「另存新檔」並保留原副檔名。使用這份固定資料，不請 AI 重新生成；本例不需要其他範例的資料。

- **分析問題**：第一季各門市、各類別營業額是多少？哪個月最好？
- **使用欄位**：訂單只有代碼，門市名稱與售價要合併門市、商品資料才拿得到。
- **本例重點**：合併前先檢查欄位名稱與鍵值；合併後檢查筆數與對不上的資料。

## A｜一步一步建立 Notebook

先把本頁網址貼給 AI，再依序貼以下 prompt。一次只貼一段，確認結果後再繼續；AI 無法讀取網址時，貼上本頁內容。

### A0｜讓 AI 認識任務

```text
請閱讀我提供的教材網址，擔任我的資料分析助教。
沿用我已建立的環境，在 05_bookstore_merge/ 工作。
依本例設定逐步建立 lesson.ipynb，保留已完成內容。
用繁體中文說明，只做目前步驟；每步問我一個觀念問題。
能執行就直接執行；不能執行時明說，不編造數字。
Matplotlib／Seaborn 圖表的顯示文字全部使用繁體中文。
現在先說明分析問題、資料欄位與預期成果，不開始寫程式。
```

繪圖前，先貼[共用繁體中文繪圖 prompt](../README.md#共用-promptmatplotlib-與-seaborn-繁體中文繪圖)。

### A1｜讀取與觀察資料

觀念連結：[pandas的檔案存取](../../pandas的檔案存取/README.md)

```text
在同一份 Notebook 讀取本例資料，原始檔只讀不改。
讀取三個月訂單與門市、商品資料，列出各檔欄位名稱與筆數。
比較三個月的欄位是否一致，門市代碼有哪些不同寫法。
先不要合併，告訴我你發現的問題。
缺檔時依上方下載連結取得，不換資料或重新生成。
```

### A2｜清理與整理

觀念連結：[數據整理：連接、合併和重塑](../../數據整理_連接_合併_重塑/README.md)

```text
統一欄位名稱與門市代碼寫法後，用 concat 合併三個月，加上「月份」欄。
說明 inner、left、outer 三種 merge 的差別，示範各自的結果筆數。
用 merge 的 indicator 找出對不上的門市與商品，另存一張清單。
選定合併方式並說明理由，確認營業額不會因合併方式而默默變少。
每一步顯示處理前後的筆數，說明這樣做的理由。
```

### A3｜分析與計算

觀念連結：[數據整理：連接、合併和重塑](../../數據整理_連接_合併_重塑/README.md)、[群組資料和群組運算](../../群組資料和群組運算/README.md)

```text
新增營業額＝數量 × 售價，計算各門市、各類別、各月份營業額。
對不上商品的訂單無法算營業額，統計有幾筆、影響多少數量。
找出季度暢銷書前五名。
所有數字都要實際執行得到；不要為了結果好看改資料。
```

### A4｜視覺化與解讀

觀念連結：[直接使用pandas繪制圖表](../../直接使用pandas繪制圖表/README.md)

```text
套用共用字型設定，圖表標題、座標軸、圖例全部繁體中文。
畫各門市每月營業額的分組長條圖。
說明季報重點，以及對不上的資料應該請誰確認。
```

### A5｜重新執行與保存

```text
重啟 kernel，從頭執行 lesson.ipynb，確認沒有錯誤、圖表中文正常。
把整理後的資料存到 output/，原始 data/ 不覆蓋。
另存 notes.md：資料來源、處理步驟、主要數字與三個發現。
回報實際執行結果與還不確定的地方。
```

## B｜做成交付成果

完成 A5 後再貼 B1、B2。

### B1｜建立Excel 季報與對不上清單

```text
建立 build_quarter_report.py，一鍵產生季報。
輸出 output/2025Q1季報.xlsx：門市、類別、月份、暢銷書、對不上清單五個工作表。
金額加千分位；對不上清單要寫出原因。
以腳本所在位置定位檔案。
不在腳本或應用中重新產生資料；提供執行命令。
```

### B2｜驗收

```text
重跑腳本，確認五個工作表都有資料。
確認季報總營業額與 Notebook 一致，三個月筆數加總正確。
模擬少一個月份檔案，確認有清楚提示後還原。
寫一份簡短 RUN.md，說明執行方式、輸出與限制。
回報已測試與待確認項目，再問我下方觀念問題。
```

## 觀念確認

1. concat 和 merge 分別解決什麼問題？
2. left join 和 inner join 的結果為什麼筆數不同？
3. 鍵值對不上時，該刪掉、補上，還是回報？

## 完成檢查

三個月欄位統一後才合併；合併方式有理由；對不上的門市與商品被列出而不是默默消失。

至少展示：一個由 AI 實際執行得到的數字、一張圖表、一個交付成果；說明一項由你下命令、AI 幫你完成並經你檢查的工作。

[回到課程首頁](../README.md)
