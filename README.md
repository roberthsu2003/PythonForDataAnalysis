![python for data Aanlysis](./card.png)

# Python 資料分析

用 **NumPy、pandas、Matplotlib** 把原始資料變成能做決策的報表與圖表。每一章都搭配 AI 協作的方法：學會怎麼向 AI 描述需求，也學會怎麼驗收 AI 的產出。

> 🌐 **網頁版**：[roberthsu2003.github.io/PythonForDataAnalysis](https://roberthsu2003.github.io/PythonForDataAnalysis/)（手機、平板也好讀，內容與這裡同步）

> [!TIP]
> **📡 這門課的每一個範例，都是台灣的真實資料**
>
> 全部來自[政府資料開放平台](https://data.gov.tw)：你騎的 YouBike、家裡的電費單、每天呼吸的空氣、擠的捷運、看過的電影、走過的路口。
> 每一章都用一個你真的會好奇的問題開場：**夏天電費為什麼暴增？哪一站最擠？台灣人最愛看哪部電影？死亡車禍最常發生在什麼時候？**
> 真實資料也很「髒」——亂碼、民國年、「台北」和「臺北」對不上——學會處理它們，你就具備了真正的資料分析能力。

## 🚀 第一次上課：3 步驟開始

| 步驟 | 做什麼 | 說明 |
| :---: | --- | --- |
| 1️⃣ | 點下方表格「🎯 本章任務」的連結 | 直接在 **Google Colab** 開啟範例，不用安裝任何東西（需要 Google 帳號） |
| 2️⃣ | 從第一格開始按 `Shift + Enter` | 第一格會自動下載本章資料；跟著「🗺️ 今日任務地圖」一關一關往下做 |
| 3️⃣ | 完成最後的「✍️ 練習區」 | 把 `___` 填好 → 執行 ✅ 檢查格，馬上知道對不對；真的卡住再點開 🔑 解答 |

> 💻 想在自己電腦上跑？到各章 README 下載 `學生素材.zip`，解壓縮後用 Jupyter 或 VS Code 開啟即可（需要 Python 3.11 以上與 `requirements.txt` 裡的套件）。

### 📒 每本範例 Notebook 都長這樣

```text
🎯 情境故事 → 🗺️ 今日任務地圖 → 任務 1、2、3…… → ✍️ 練習區 → 🏆 完成清單
                                  │
                                  ├─ 你想知道：這個任務要回答什麼
                                  ├─ 程式碼：每一行都有中文註解
                                  ├─ 💡 看懂結果：數字背後的意義、可以做什麼決策
                                  └─ 🤖 換你問 AI：可以直接複製的提問句
```

## 🧭 學習路徑：階段一～五

### 🧱 階段一｜基礎工具

| 章 | 主題 | 你會學到 | 🎯 本章任務（點了直接開 Colab） |
| :---: | :--- | :--- | :--- |
| 1 | [Python](https://github.com/roberthsu2003/python) | Python 基礎語法（另一個 repo） | — |
| 2 | [檔案存取](./檔案存取/README.md) | 讀取 CSV 與 JSON，認識 UTF-8 編碼與中文亂碼 | [🚲 YouBike 與電影票房](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E6%AA%94%E6%A1%88%E5%AD%98%E5%8F%96/%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90/%E7%AF%84%E4%BE%8B_YouBike%E8%88%87%E9%9B%BB%E5%BD%B1%E7%A5%A8%E6%88%BF_%E8%AE%80%E6%87%82%E6%94%BF%E5%BA%9C%E9%96%8B%E6%94%BE%E8%B3%87%E6%96%99.ipynb) |
| 3 | [繪圖和視覺展示](./繪圖和視覺展示/README.md) | Matplotlib 的畫布結構，折線、長條、直方、圓餅圖 | [⚡ 夏天電費為什麼暴增？](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E7%B9%AA%E5%9C%96%E5%92%8C%E8%A6%96%E8%A6%BA%E5%B1%95%E7%A4%BA/%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90/%E7%AF%84%E4%BE%8B_%E5%A4%8F%E5%A4%A9%E9%9B%BB%E8%B2%BB%E7%82%BA%E4%BB%80%E9%BA%BC%E6%9A%B4%E5%A2%9E_%E5%8F%B0%E9%9B%BB%E7%94%A8%E9%9B%BB%E4%BA%94%E5%BC%B5%E5%9C%96.ipynb) |
| 4 | [Numpy建立與計算](./Numpy建立與計算/README.md) | 用陣列整批計算總和、平均、最高最低與累計 | [🌫️ 你家附近的空氣好嗎？](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/Numpy%E5%BB%BA%E7%AB%8B%E8%88%87%E8%A8%88%E7%AE%97/%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90/%E7%AF%84%E4%BE%8B_%E4%BD%A0%E5%AE%B6%E9%99%84%E8%BF%91%E7%9A%84%E7%A9%BA%E6%B0%A3%E5%A5%BD%E5%97%8E_365%E5%A4%A9AQI%E7%9F%A9%E9%99%A3.ipynb) |

### 🐼 階段二｜pandas 入門

| 章 | 主題 | 你會學到 | 🎯 本章任務（點了直接開 Colab） |
| :---: | :--- | :--- | :--- |
| 5 | [初見pandas](./初見pandas/README.md) | Series 與 DataFrame，把資料變成「會說話的 Excel 表」 | [🎬 台灣人最愛看什麼電影？](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E5%88%9D%E8%A6%8Bpandas/%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90/%E7%AF%84%E4%BE%8B_%E5%8F%B0%E7%81%A3%E4%BA%BA%E6%9C%80%E6%84%9B%E7%9C%8B%E4%BB%80%E9%BA%BC%E9%9B%BB%E5%BD%B1_%E7%AC%AC%E4%B8%80%E4%BB%BDpandas%E5%A0%B1%E8%A1%A8.ipynb) |
| 6 | [pandas的基礎功能](./pandas的基礎功能/README.md) | 選取、排序、排名、批次加工與描述統計 | [🏆 票房排行榜與爆紅的秘密](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/pandas%E7%9A%84%E5%9F%BA%E7%A4%8E%E5%8A%9F%E8%83%BD/%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90/%E7%AF%84%E4%BE%8B_%E7%A5%A8%E6%88%BF%E6%8E%92%E8%A1%8C%E6%A6%9C%E8%88%87%E7%88%86%E7%B4%85%E7%9A%84%E7%A7%98%E5%AF%86.ipynb) |
| 7 | [pandas的檔案存取](./pandas的檔案存取/README.md) | 一行讀寫 CSV、Excel、JSON、API 與資料庫 | [📥 政府資料的七種難搞格式](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/pandas%E7%9A%84%E6%AA%94%E6%A1%88%E5%AD%98%E5%8F%96/%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90/%E7%AF%84%E4%BE%8B_%E6%94%BF%E5%BA%9C%E8%B3%87%E6%96%99%E7%9A%84%E4%B8%83%E7%A8%AE%E9%9B%A3%E6%90%9E%E6%A0%BC%E5%BC%8F.ipynb) |

### 🧹 階段三｜整理資料

| 章 | 主題 | 你會學到 | 🎯 本章任務（點了直接開 Colab） |
| :---: | :--- | :--- | :--- |
| 8 | [資料整理和使用前準備](./資料整理和使用前準備/README.md) | 缺值、重複、異常值、型態轉換與字串處理 | [🚦 死亡車禍資料大掃除](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E8%B3%87%E6%96%99%E6%95%B4%E7%90%86%E5%92%8C%E4%BD%BF%E7%94%A8%E5%89%8D%E6%BA%96%E5%82%99/%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90/%E7%AF%84%E4%BE%8B_%E6%AD%BB%E4%BA%A1%E8%BB%8A%E7%A6%8D%E8%B3%87%E6%96%99%E5%A4%A7%E6%8E%83%E9%99%A4_A1%E4%BA%A4%E9%80%9A%E4%BA%8B%E6%95%85.ipynb) |
| 9 | [群組資料和群組運算](./群組資料和群組運算/README.md) | groupby「分組 → 計算 → 合併」與樞紐分析表 | [🚇 捷運哪一站最擠？](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E7%BE%A4%E7%B5%84%E8%B3%87%E6%96%99%E5%92%8C%E7%BE%A4%E7%B5%84%E9%81%8B%E7%AE%97/%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90/%E7%AF%84%E4%BE%8B_%E6%8D%B7%E9%81%8B%E5%93%AA%E4%B8%80%E7%AB%99%E6%9C%80%E6%93%A0_%E8%AA%B0%E4%BD%8F%E9%80%99%E8%A3%A1%E8%AA%B0%E5%9C%A8%E9%80%99%E4%B8%8A%E7%8F%AD.ipynb) |
| 10 | [數據整理：連接、合併和重塑](./數據整理_連接_合併_重塑/README.md) | merge、concat、stack／pivot，把表格拼成報表 | [🔗 誰最會用電？](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E6%95%B8%E6%93%9A%E6%95%B4%E7%90%86_%E9%80%A3%E6%8E%A5_%E5%90%88%E4%BD%B5_%E9%87%8D%E5%A1%91/%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90/%E7%AF%84%E4%BE%8B_%E8%AA%B0%E6%9C%80%E6%9C%83%E7%94%A8%E9%9B%BB_%E4%BA%BA%E5%8F%A3%E8%88%87%E7%94%A8%E9%9B%BB%E8%B3%87%E6%96%99%E5%A4%A7%E5%90%88%E4%BD%B5.ipynb) |

### 📈 階段四｜分析與呈現

| 章 | 主題 | 你會學到 | 🎯 本章任務（點了直接開 Colab） |
| :---: | :--- | :--- | :--- |
| 11 | [日期和時間](./日期和時間/README.md) | 時間索引、resample、shift、rolling 與時區 | [📅 電費漲了多少？](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E6%97%A5%E6%9C%9F%E5%92%8C%E6%99%82%E9%96%93/%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90/%E7%AF%84%E4%BE%8B_%E9%9B%BB%E8%B2%BB%E6%BC%B2%E4%BA%86%E5%A4%9A%E5%B0%91_%E7%A9%BA%E6%B1%99%E5%93%AA%E5%A4%A9%E6%9C%80%E5%9A%B4%E9%87%8D_%E6%99%82%E9%96%93%E5%BA%8F%E5%88%97.ipynb) |
| 12 | [視覺化表格](./視覺化表格/README.md) | 用 Styler 加上千分位、條件標色與資料條 | [🎨 做一張會變色的空氣品質週報](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E8%A6%96%E8%A6%BA%E5%8C%96%E8%A1%A8%E6%A0%BC/%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90/%E7%AF%84%E4%BE%8B_%E6%9C%83%E8%AE%8A%E8%89%B2%E7%9A%84%E7%A9%BA%E6%B0%A3%E5%93%81%E8%B3%AA%E9%80%B1%E5%A0%B1_Styler.ipynb) |
| 13 | [直接使用pandas繪制圖表](./直接使用pandas繪制圖表/README.md) | 表格一行出圖，再用 seaborn 畫統計圖 | [🖼️ 一行程式，畫出台灣的六個故事](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E7%9B%B4%E6%8E%A5%E4%BD%BF%E7%94%A8pandas%E7%B9%AA%E5%88%B6%E5%9C%96%E8%A1%A8/%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90/%E7%AF%84%E4%BE%8B_%E4%B8%80%E8%A1%8C%E7%95%AB%E5%87%BA%E5%8F%B0%E7%81%A3%E7%9A%84%E5%85%AD%E5%80%8B%E6%95%85%E4%BA%8B.ipynb) |

### 🚀 階段五｜綜合實戰

| 章 | 主題 | 你會學到 | 🎯 本章任務（點了直接開 Colab） |
| :---: | :--- | :--- | :--- |
| 14 | [全方面分析](./全方面分析/README.md) | 用台鐵 2023 年進出站資料走完一次完整分析流程 | [🚆 台鐵 2023——誰是通勤站？](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E5%85%A8%E6%96%B9%E9%9D%A2%E5%88%86%E6%9E%90/%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90/%E6%9C%9F%E6%9C%AB%E5%AF%A6%E6%88%B0_%E5%8F%B0%E9%90%B52023%E9%80%9A%E5%8B%A4%E7%AB%99%E8%88%87%E8%A7%80%E5%85%89%E7%AB%99.ipynb) |
| 15 | [資料分析範例](./資料分析範例/README.md) | 政府開放資料、股票、網路紀錄等延伸範例 | 自選延伸練習 |

---

## 🛠️ 延伸加值：互動介面工具

- [**最適合搭配的介面工具比較表**](./最適合搭配的介面工具比較表.md)：評估 Streamlit、Gradio 等現代互動介面工具，將分析結果搭建為互動式 Web 應用與商業儀表板。


