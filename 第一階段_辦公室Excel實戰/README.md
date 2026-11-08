# 第一階段：AI 協作辦公室 Excel 實戰

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
| 01 | 1 | 行政 | [讀懂工作表與欄位](./01_行政_文具領用.md) | [Excel](./01_行政_文具領用.xlsx) | [Colab](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E7%AC%AC%E4%B8%80%E9%9A%8E%E6%AE%B5_%E8%BE%A6%E5%85%AC%E5%AE%A4Excel%E5%AF%A6%E6%88%B0/01_%E8%A1%8C%E6%94%BF_%E6%96%87%E5%85%B7%E9%A0%98%E7%94%A8.ipynb) |
| 02 | 1 | 人資 | [文字條件篩選與計數](./02_人資_教育訓練名單.md) | [Excel](./02_人資_教育訓練名單.xlsx) | [Colab](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E7%AC%AC%E4%B8%80%E9%9A%8E%E6%AE%B5_%E8%BE%A6%E5%85%AC%E5%AE%A4Excel%E5%AF%A6%E6%88%B0/02_%E4%BA%BA%E8%B3%87_%E6%95%99%E8%82%B2%E8%A8%93%E7%B7%B4%E5%90%8D%E5%96%AE.ipynb) |
| 03 | 1 | 財務 | [數值加總與條件加總](./03_財務_費用明細.md) | [Excel](./03_財務_費用明細.xlsx) | [Colab](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E7%AC%AC%E4%B8%80%E9%9A%8E%E6%AE%B5_%E8%BE%A6%E5%85%AC%E5%AE%A4Excel%E5%AF%A6%E6%88%B0/03_%E8%B2%A1%E5%8B%99_%E8%B2%BB%E7%94%A8%E6%98%8E%E7%B4%B0.ipynb) |
| 04 | 2 | 業務 | [新增計算結果與排序](./04_業務_訂單金額.md) | [Excel](./04_業務_訂單金額.xlsx) | [Colab](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E7%AC%AC%E4%B8%80%E9%9A%8E%E6%AE%B5_%E8%BE%A6%E5%85%AC%E5%AE%A4Excel%E5%AF%A6%E6%88%B0/04_%E6%A5%AD%E5%8B%99_%E8%A8%82%E5%96%AE%E9%87%91%E9%A1%8D.ipynb) |
| 05 | 2 | 倉管 | [多條件判斷與差額](./05_倉管_庫存補貨.md) | [Excel](./05_倉管_庫存補貨.xlsx) | [Colab](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E7%AC%AC%E4%B8%80%E9%9A%8E%E6%AE%B5_%E8%BE%A6%E5%85%AC%E5%AE%A4Excel%E5%AF%A6%E6%88%B0/05_%E5%80%89%E7%AE%A1_%E5%BA%AB%E5%AD%98%E8%A3%9C%E8%B2%A8.ipynb) |
| 06 | 2 | 採購 | [同條件比較與最低值](./06_採購_供應商報價.md) | [Excel](./06_採購_供應商報價.xlsx) | [Colab](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E7%AC%AC%E4%B8%80%E9%9A%8E%E6%AE%B5_%E8%BE%A6%E5%85%AC%E5%AE%A4Excel%E5%AF%A6%E6%88%B0/06_%E6%8E%A1%E8%B3%BC_%E4%BE%9B%E6%87%89%E5%95%86%E5%A0%B1%E5%83%B9.ipynb) |
| 07 | 3 | 行政 | [NumPy 二維陣列與 axis](./07_行政_部門月費用.md) | [Excel](./07_行政_部門月費用.xlsx) | [Colab](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E7%AC%AC%E4%B8%80%E9%9A%8E%E6%AE%B5_%E8%BE%A6%E5%85%AC%E5%AE%A4Excel%E5%AF%A6%E6%88%B0/07_%E8%A1%8C%E6%94%BF_%E9%83%A8%E9%96%80%E6%9C%88%E8%B2%BB%E7%94%A8.ipynb) |
| 08 | 3 | 人資 | [缺值與平均數](./08_人資_訓練滿意度.md) | [Excel](./08_人資_訓練滿意度.xlsx) | [Colab](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E7%AC%AC%E4%B8%80%E9%9A%8E%E6%AE%B5_%E8%BE%A6%E5%85%AC%E5%AE%A4Excel%E5%AF%A6%E6%88%B0/08_%E4%BA%BA%E8%B3%87_%E8%A8%93%E7%B7%B4%E6%BB%BF%E6%84%8F%E5%BA%A6.ipynb) |
| 09 | 3 | 客服 | [分類統計與平均的分母](./09_客服_案件處理統計.md) | [Excel](./09_客服_案件處理統計.xlsx) | [Colab](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E7%AC%AC%E4%B8%80%E9%9A%8E%E6%AE%B5_%E8%BE%A6%E5%85%AC%E5%AE%A4Excel%E5%AF%A6%E6%88%B0/09_%E5%AE%A2%E6%9C%8D_%E6%A1%88%E4%BB%B6%E8%99%95%E7%90%86%E7%B5%B1%E8%A8%88.ipynb) |
| 10 | 4 | 業務 | [折線圖與月增率](./10_業務_月營收趨勢.md) | [Excel](./10_業務_月營收趨勢.xlsx) | [Colab](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E7%AC%AC%E4%B8%80%E9%9A%8E%E6%AE%B5_%E8%BE%A6%E5%85%AC%E5%AE%A4Excel%E5%AF%A6%E6%88%B0/10_%E6%A5%AD%E5%8B%99_%E6%9C%88%E7%87%9F%E6%94%B6%E8%B6%A8%E5%8B%A2.ipynb) |
| 11 | 4 | 行銷 | [比率與長條圖](./11_行銷_活動成效.md) | [Excel](./11_行銷_活動成效.xlsx) | [Colab](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E7%AC%AC%E4%B8%80%E9%9A%8E%E6%AE%B5_%E8%BE%A6%E5%85%AC%E5%AE%A4Excel%E5%AF%A6%E6%88%B0/11_%E8%A1%8C%E9%8A%B7_%E6%B4%BB%E5%8B%95%E6%88%90%E6%95%88.ipynb) |
| 12 | 4 | 採購／倉管／財務 | [跨工作表核對與明細報表](./12_跨部門_請購驗收核對.md) | [Excel](./12_跨部門_請購驗收核對.xlsx) | [Colab](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E7%AC%AC%E4%B8%80%E9%9A%8E%E6%AE%B5_%E8%BE%A6%E5%85%AC%E5%AE%A4Excel%E5%AF%A6%E6%88%B0/12_%E8%B7%A8%E9%83%A8%E9%96%80_%E8%AB%8B%E8%B3%BC%E9%A9%97%E6%94%B6%E6%A0%B8%E5%B0%8D.ipynb) |

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
