![python for data Aanlysis](./card.png)

# Python 資料分析

用 **NumPy、pandas、Matplotlib** 把原始資料變成能做決策的報表與圖表。每一章都搭配 AI 協作的方法：學會怎麼向 AI 描述需求，也學會怎麼驗收 AI 的產出。

> [!TIP]
> **🧋 這門課有一個貫穿全場的主角：「茶語時光」**
>
> 你是虛構手搖飲連鎖品牌「茶語時光」總部新來的資料小幫手。5 家門市、10 款飲料、兩年的營收與訂單——
> 每一章，老闆都會丟給你一個真實會遇到的問題：**台南人真的愛全糖嗎？颱風天少賺多少？哪個店員最會賣？**
> 學完一章，你就用程式回答了一個問題；學完整門課，你就做出一份能交給老闆的完整報告。

## 🚀 第一次上課：3 步驟開始

| 步驟 | 做什麼 | 說明 |
| :---: | --- | --- |
| 1️⃣ | 點下方表格「🧋 本章任務」的連結 | 直接在 **Google Colab** 開啟範例，不用安裝任何東西（需要 Google 帳號） |
| 2️⃣ | 從第一格開始按 `Shift + Enter` | 第一格會自動下載本章資料；跟著「🗺️ 今日任務地圖」一關一關往下做 |
| 3️⃣ | 完成最後的「✍️ 練習區」 | 把 `___` 填好 → 執行 ✅ 檢查格，馬上知道對不對；真的卡住再點開 🔑 解答 |

> 💻 想在自己電腦上跑？到各章 README 下載 `學生素材.zip`，解壓縮後用 Jupyter 或 VS Code 開啟即可（需要 Python 3.11 以上與 `requirements.txt` 裡的套件）。

### 📒 每本範例 Notebook 都長這樣

```text
🧋 情境故事 → 🗺️ 今日任務地圖 → 任務 1、2、3…… → ✍️ 練習區 → 🏆 完成清單
                                  │
                                  ├─ 老闆的問題：這個任務要回答什麼
                                  ├─ 程式碼：每一行都有中文註解
                                  ├─ 💡 看懂結果：數字背後的意義、可以做什麼決策
                                  └─ 🤖 換你問 AI：可以直接複製的提問句
```

## 🧭 學習路徑：階段一～五

### 🧱 階段一｜基礎工具

| 章 | 主題 | 你會學到 | 🧋 本章任務（點了直接開 Colab） |
| :---: | :--- | :--- | :--- |
| 1 | [Python](https://github.com/roberthsu2003/python) | Python 基礎語法（另一個 repo） | — |
| 2 | [檔案存取](./檔案存取/README.md) | 讀取 CSV 與 JSON，認識 UTF-8 編碼與中文亂碼 | [🧋 用 Python 讀懂顧客評論與菜單檔案](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E6%AA%94%E6%A1%88%E5%AD%98%E5%8F%96/%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90/%E7%AF%84%E4%BE%8B_%E8%8C%B6%E8%AA%9E%E6%99%82%E5%85%89_%E9%A1%A7%E5%AE%A2%E8%A9%95%E8%AB%96%E8%88%87%E8%8F%9C%E5%96%AE%E6%AA%94%E6%A1%88.ipynb) |
| 3 | [繪圖和視覺展示](./繪圖和視覺展示/README.md) | Matplotlib 的畫布結構，折線、長條、直方、圓餅圖 | [📈 做出老闆最愛的五張圖](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E7%B9%AA%E5%9C%96%E5%92%8C%E8%A6%96%E8%A6%BA%E5%B1%95%E7%A4%BA/%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90/%E7%AF%84%E4%BE%8B_%E8%8C%B6%E8%AA%9E%E6%99%82%E5%85%89_%E8%80%81%E9%97%86%E6%9C%80%E6%84%9B%E7%9A%84%E4%BA%94%E5%BC%B5%E5%9C%96.ipynb) |
| 4 | [Numpy建立與計算](./Numpy建立與計算/README.md) | 用陣列整批計算總和、平均、最高最低與累計 | [🧮 一年 366 天的杯數矩陣](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/Numpy%E5%BB%BA%E7%AB%8B%E8%88%87%E8%A8%88%E7%AE%97/%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90/%E7%AF%84%E4%BE%8B_%E8%8C%B6%E8%AA%9E%E6%99%82%E5%85%89_%E4%B8%80%E5%B9%B4366%E5%A4%A9%E7%9A%84%E6%9D%AF%E6%95%B8%E7%9F%A9%E9%99%A3.ipynb) |

### 🐼 階段二｜pandas 入門

| 章 | 主題 | 你會學到 | 🧋 本章任務（點了直接開 Colab） |
| :---: | :--- | :--- | :--- |
| 5 | [初見pandas](./初見pandas/README.md) | Series 與 DataFrame，把資料變成「會說話的 Excel 表」 | [🐼 新品上市週的第一份 pandas 報表](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E5%88%9D%E8%A6%8Bpandas/%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90/%E7%AF%84%E4%BE%8B_%E8%8C%B6%E8%AA%9E%E6%99%82%E5%85%89_%E6%96%B0%E5%93%81%E4%B8%8A%E5%B8%82%E9%80%B1%E7%9A%84%E7%AC%AC%E4%B8%80%E4%BB%BD%E5%A0%B1%E8%A1%A8.ipynb) |
| 6 | [pandas的基礎功能](./pandas的基礎功能/README.md) | 選取、排序、排名、批次加工與描述統計 | [🏆 店員排行榜與天氣分析](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/pandas%E7%9A%84%E5%9F%BA%E7%A4%8E%E5%8A%9F%E8%83%BD/%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90/%E7%AF%84%E4%BE%8B_%E8%8C%B6%E8%AA%9E%E6%99%82%E5%85%89_%E5%BA%97%E5%93%A1%E6%8E%92%E8%A1%8C%E6%A6%9C%E8%88%87%E5%A4%A9%E6%B0%A3%E5%88%86%E6%9E%90.ipynb) |
| 7 | [pandas的檔案存取](./pandas的檔案存取/README.md) | 一行讀寫 CSV、Excel、JSON、API 與資料庫 | [📥 搞定五種難搞的資料檔](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/pandas%E7%9A%84%E6%AA%94%E6%A1%88%E5%AD%98%E5%8F%96/%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90/%E7%AF%84%E4%BE%8B_%E8%8C%B6%E8%AA%9E%E6%99%82%E5%85%89_%E4%BA%94%E7%A8%AE%E9%9B%A3%E6%90%9E%E7%9A%84%E8%B3%87%E6%96%99%E6%AA%94.ipynb) |

### 🧹 階段三｜整理資料

| 章 | 主題 | 你會學到 | 🧋 本章任務（點了直接開 Colab） |
| :---: | :--- | :--- | :--- |
| 8 | [資料整理和使用前準備](./資料整理和使用前準備/README.md) | 缺值、重複、異常值、型態轉換與字串處理 | [🧹 髒亂的會員問卷大掃除](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E8%B3%87%E6%96%99%E6%95%B4%E7%90%86%E5%92%8C%E4%BD%BF%E7%94%A8%E5%89%8D%E6%BA%96%E5%82%99/%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90/%E7%AF%84%E4%BE%8B_%E8%8C%B6%E8%AA%9E%E6%99%82%E5%85%89_%E9%AB%92%E4%BA%82%E7%9A%84%E6%9C%83%E5%93%A1%E5%95%8F%E5%8D%B7%E5%A4%A7%E6%8E%83%E9%99%A4.ipynb) |
| 9 | [群組資料和群組運算](./群組資料和群組運算/README.md) | groupby「分組 → 計算 → 合併」與樞紐分析表 | [🧩 台南人真的愛全糖嗎？](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E7%BE%A4%E7%B5%84%E8%B3%87%E6%96%99%E5%92%8C%E7%BE%A4%E7%B5%84%E9%81%8B%E7%AE%97/%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90/%E7%AF%84%E4%BE%8B_%E8%8C%B6%E8%AA%9E%E6%99%82%E5%85%89_%E5%8F%B0%E5%8D%97%E4%BA%BA%E7%9C%9F%E7%9A%84%E6%84%9B%E5%85%A8%E7%B3%96%E5%97%8E.ipynb) |
| 10 | [數據整理：連接、合併和重塑](./數據整理_連接_合併_重塑/README.md) | merge、concat、stack／pivot，把表格拼成報表 | [🔗 把三個月的訂單合併成第一季季報](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E6%95%B8%E6%93%9A%E6%95%B4%E7%90%86_%E9%80%A3%E6%8E%A5_%E5%90%88%E4%BD%B5_%E9%87%8D%E5%A1%91/%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90/%E7%AF%84%E4%BE%8B_%E8%8C%B6%E8%AA%9E%E6%99%82%E5%85%89_%E4%B8%89%E5%80%8B%E6%9C%88%E8%A8%82%E5%96%AE%E5%90%88%E4%BD%B5%E6%88%90%E5%AD%A3%E5%A0%B1.ipynb) |

### 📈 階段四｜分析與呈現

| 章 | 主題 | 你會學到 | 🧋 本章任務（點了直接開 Colab） |
| :---: | :--- | :--- | :--- |
| 11 | [日期和時間](./日期和時間/README.md) | 時間索引、resample、shift、rolling 與時區 | [📅 兩年營收趨勢與外送時區之謎](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E6%97%A5%E6%9C%9F%E5%92%8C%E6%99%82%E9%96%93/%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90/%E7%AF%84%E4%BE%8B_%E8%8C%B6%E8%AA%9E%E6%99%82%E5%85%89_%E5%85%A9%E5%B9%B4%E7%87%9F%E6%94%B6%E8%88%87%E5%A4%96%E9%80%81%E6%99%82%E5%8D%80.ipynb) |
| 12 | [視覺化表格](./視覺化表格/README.md) | 用 Styler 加上千分位、條件標色與資料條 | [🎨 做一份「會發亮」的 KPI 報表](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E8%A6%96%E8%A6%BA%E5%8C%96%E8%A1%A8%E6%A0%BC/%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90/%E7%AF%84%E4%BE%8B_%E8%8C%B6%E8%AA%9E%E6%99%82%E5%85%89_%E6%9C%83%E7%99%BC%E4%BA%AE%E7%9A%84KPI%E9%80%B1%E5%A0%B1.ipynb) |
| 13 | [直接使用pandas繪制圖表](./直接使用pandas繪制圖表/README.md) | 表格一行出圖，再用 seaborn 畫統計圖 | [🖼️ 一行程式畫出年度簡報圖](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E7%9B%B4%E6%8E%A5%E4%BD%BF%E7%94%A8pandas%E7%B9%AA%E5%88%B6%E5%9C%96%E8%A1%A8/%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90/%E7%AF%84%E4%BE%8B_%E8%8C%B6%E8%AA%9E%E6%99%82%E5%85%89_%E4%B8%80%E8%A1%8C%E7%95%AB%E5%87%BA%E5%B9%B4%E5%BA%A6%E7%B0%A1%E5%A0%B1%E5%9C%96.ipynb) |

### 🚀 階段五｜綜合實戰

| 章 | 主題 | 你會學到 | 🧋 本章任務（點了直接開 Colab） |
| :---: | :--- | :--- | :--- |
| 14 | [全方面分析](./全方面分析/README.md) | 用台鐵 2023 年進出站資料走完一次完整分析流程 | [🚆 台鐵 2023——誰是通勤站？誰是觀光站？](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E5%85%A8%E6%96%B9%E9%9D%A2%E5%88%86%E6%9E%90/%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90/%E6%9C%9F%E6%9C%AB%E5%AF%A6%E6%88%B0_%E5%8F%B0%E9%90%B52023%E9%80%9A%E5%8B%A4%E7%AB%99%E8%88%87%E8%A7%80%E5%85%89%E7%AB%99.ipynb) |
| 15 | [資料分析範例](./資料分析範例/README.md) | 政府開放資料、股票、網路紀錄等延伸範例 | 自選延伸練習 |

---

## 🛠️ 延伸加值：互動介面工具

- [**最適合搭配的介面工具比較表**](./最適合搭配的介面工具比較表.md)：評估 Streamlit、Gradio 等現代互動介面工具，將分析結果搭建為互動式 Web 應用與商業儀表板。


