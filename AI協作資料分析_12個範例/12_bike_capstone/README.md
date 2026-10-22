# 12｜共享單車綜合專題：從問題到儀表板

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/AI%E5%8D%94%E4%BD%9C%E8%B3%87%E6%96%99%E5%88%86%E6%9E%90_12%E5%80%8B%E7%AF%84%E4%BE%8B/12_bike_capstone/lesson.ipynb) [開啟教材 Notebook](./lesson.ipynb)

你提出需求、看懂結果並驗收；AI 負責寫程式、執行和除錯。先從上方教材 Notebook 的資料下載與讀取起點開始，再依提示詞逐步完成自己的分析與交付成果。

- 任務：完整資料分析流程：提問、清理、合併、分析、視覺化與溝通。
- 交付成果：Streamlit 儀表板與分析報告。
- 學生專案內位置：`12_bike_capstone/`；共用專案根目錄的 `.venv`。
- 本例完成後：能用自己的話說明分析問題、資料處理步驟與一個發現。

## 資料與問題設定

本教材原創偽資料，騎乘紀錄 6,020 筆（含重複）、站點 12 個、每日天氣 91 天；固定 seed=1212。

### 範例檔下載

- [下載 bike_trips.csv](https://raw.githubusercontent.com/roberthsu2003/PythonForDataAnalysis/master/AI%E5%8D%94%E4%BD%9C%E8%B3%87%E6%96%99%E5%88%86%E6%9E%90_12%E5%80%8B%E7%AF%84%E4%BE%8B/12_bike_capstone/data/bike_trips.csv)：儲存到學生專案的 `12_bike_capstone/data/bike_trips.csv`。
- [下載 stations.csv](https://raw.githubusercontent.com/roberthsu2003/PythonForDataAnalysis/master/AI%E5%8D%94%E4%BD%9C%E8%B3%87%E6%96%99%E5%88%86%E6%9E%90_12%E5%80%8B%E7%AF%84%E4%BE%8B/12_bike_capstone/data/stations.csv)：儲存到學生專案的 `12_bike_capstone/data/stations.csv`。
- [下載 weather_daily.csv](https://raw.githubusercontent.com/roberthsu2003/PythonForDataAnalysis/master/AI%E5%8D%94%E4%BD%9C%E8%B3%87%E6%96%99%E5%88%86%E6%9E%90_12%E5%80%8B%E7%AF%84%E4%BE%8B/12_bike_capstone/data/weather_daily.csv)：儲存到學生專案的 `12_bike_capstone/data/weather_daily.csv`。
- [線上閱讀偽資料卡與欄位字典](./data/DATA_CARD.md)：直接在 GitHub 閱讀，不必下載。

若連結顯示文字，使用瀏覽器「另存新檔」並保留原副檔名。使用這份固定資料，不請 AI 重新生成；本例不需要其他範例的資料。

- **分析問題**：由你提出至少三個問題，例如：通勤尖峰在哪裡？下雨影響多大？哪些站需要補車？
- **使用欄位**：三份檔案都要用到；騎乘時間要自己計算。
- **本例重點**：沒有唯一答案。重點是問題清楚、清理決定有紀錄、結論有圖表與數字支持。

## A｜一步一步建立 Notebook

先把本頁網址貼給 AI，再依序貼以下 prompt。一次只貼一段，確認結果後再繼續；AI 無法讀取網址時，貼上本頁內容。

### A0｜讓 AI 認識任務

```text
請閱讀我提供的教材網址，擔任我的資料分析助教。
沿用我已建立的環境，在 12_bike_capstone/ 工作。
依本例設定逐步建立 lesson.ipynb，保留已完成內容。
用繁體中文說明，只做目前步驟；每步問我一個觀念問題。
能執行就直接執行；不能執行時明說，不編造數字。
Matplotlib／Seaborn 圖表的顯示文字全部使用繁體中文。
現在先說明分析問題、資料欄位與預期成果，不開始寫程式。
```

繪圖前，先貼[共用繁體中文繪圖 prompt](../README.md#共用-promptmatplotlib-與-seaborn-繁體中文繪圖)。

### A1｜讀取與觀察資料

觀念連結：[全方面分析](../../全方面分析/README.md)

```text
在同一份 Notebook 讀取本例資料，原始檔只讀不改。
讀取三份資料，列出筆數、欄位、型態與缺值。
幫我把想回答的問題整理成三到五個，並說明每題需要哪些欄位。
先不要分析，等我確認問題。
缺檔時依上方下載連結取得，不換資料或重新生成。
```

### A2｜清理與整理

觀念連結：[資料整理和使用前準備](../../資料整理和使用前準備/README.md)、[數據整理：連接、合併和重塑](../../數據整理_連接_合併_重塑/README.md)

```text
檢查重複、時間填反、騎乘超過一天、還車站空白等問題。
每個問題說明處理方式與影響筆數，記錄在清理紀錄表。
計算騎乘分鐘，合併站點與天氣資料，確認筆數。
每一步顯示處理前後的筆數，說明這樣做的理由。
```

### A3｜分析與計算

觀念連結：[群組資料和群組運算](../../群組資料和群組運算/README.md)、[日期和時間](../../日期和時間/README.md)

```text
依我確認的問題逐一分析，每題先給數字表格。
至少使用一次 groupby、一次時間分析、一次合併後的比較。
比較平日與週末、晴天與雨天的騎乘量差異。
所有數字都要實際執行得到；不要為了結果好看改資料。
```

### A4｜視覺化與解讀

觀念連結：[看懂資料與選對圖表](../../看懂資料與選對圖表/README.md)、[全方面分析](../../全方面分析/README.md)

```text
套用共用字型設定，圖表標題、座標軸、圖例全部繁體中文。
每個問題配一張最適合的圖，說明為什麼選這種圖。
寫出結論、建議與一個資料限制，不誇大因果。
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

### B1｜建立Streamlit 儀表板與分析報告

```text
建立 Streamlit app.py：日期範圍、站點、使用者類型篩選。
顯示關鍵指標、每小時騎乘量、站點排行與天氣比較圖。
另產生 report.md：問題、資料、清理、發現、建議與限制。
使用清理後的資料；介面、圖表與報告用繁體中文。
不在腳本或應用中重新產生資料；提供執行命令。
```

### B2｜驗收

```text
測試三組篩選條件，比對畫面與 Notebook 數字。
確認清理紀錄的筆數和報告一致。
停止後重啟仍可操作；寫 RUN.md 說明啟動方式。
幫我準備三分鐘發表大綱：問題、方法、發現、限制。
寫一份簡短 RUN.md，說明執行方式、輸出與限制。
回報已測試與待確認項目，再問我下方觀念問題。
```

## 觀念確認

1. 你的清理決定中，哪一個最影響結論？
2. 相關和因果有什麼不同？天氣影響騎乘量，能這樣說嗎？
3. 如果要每月更新這份分析，哪些步驟可以自動化？

## 完成檢查

有清楚的分析問題；清理紀錄完整；每個結論都有數字與圖表支持；儀表板與報告一致。

至少展示：一個由 AI 實際執行得到的數字、一張圖表、一個交付成果；說明一項由你下命令、AI 幫你完成並經你檢查的工作。

[回到課程首頁](../README.md)
