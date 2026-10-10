# 📊 📂 檔案存取：讓程式讀懂 CSV 與 JSON，把散落的資料檔變成可分析的素材

> [!IMPORTANT]
> **本章節學習核心**：
> 1. **核心觀念**：資料分析的第一步永遠是「把檔案打開、讀進來」。你要認得最常見的兩種資料檔：表格型的 **CSV** 與階層型的 **JSON**，並知道「編碼（UTF-8）」為什麼會讓中文變亂碼。
> 2. **AI 協作能力**：學會向 AI 描述「檔案長什麼樣子」（第一列是不是標題、用什麼符號分隔、資料藏在 JSON 的哪一層），讓 AI 一次寫出正確的讀檔程式。
> 3. **商業決策產出**：能把政府開放資料、股票成交資訊、學生成績等原始檔，整理成「一列一筆」的乾淨清單，為後續統計與圖表打好基礎。

---

> 🚀 **完整互動教學 Notebook**：
> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E6%AA%94%E6%A1%88%E5%AD%98%E5%8F%96/README.ipynb) [開啟 README.ipynb](./README.ipynb)
>
> 📝 **延伸範例**：[個股日成交資訊.ipynb](./個股日成交資訊.ipynb)（CSV 轉成不同格式的清單）｜[csvRead.ipynb](./csvRead.ipynb)｜[jsonReader.ipynb](./jsonReader.ipynb)（新北市食品工廠清冊）
>
> 🧰 **專案範例**：[建立學生成績並存成 CSV](./建立2維list_儲存為csv檔/)｜[可選擇存成 CSV 或 Excel](./建立2維list_儲存為csv或xlsx檔/)
>
> ⚠️ 在 Colab 開啟時只會載入 Notebook 本身，若要讀取本資料夾的 `.csv`、`.json` 檔，請先上傳到 Colab 左側的「檔案」區。

---

## 📦 學生素材下載

> [!TIP]
> **🧋 茶語時光：用 Python 讀懂顧客評論與菜單檔案**
>
> 你是「茶語時光」總部新來的資料小幫手。店長丟給你一堆檔案：一份顧客評論文字檔、一份菜單 CSV、一份門市資訊 JSON，還有一份從舊電腦匯出、打開全是亂碼的會員名單。今天的任務是：**不用 Excel，用 Python 把這些檔案讀懂、整理好、再存成店長要的檔案。**
>
> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/roberthsu2003/PythonForDataAnalysis/blob/master/%E6%AA%94%E6%A1%88%E5%AD%98%E5%8F%96/%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90/%E7%AF%84%E4%BE%8B_%E8%8C%B6%E8%AA%9E%E6%99%82%E5%85%89_%E9%A1%A7%E5%AE%A2%E8%A9%95%E8%AB%96%E8%88%87%E8%8F%9C%E5%96%AE%E6%AA%94%E6%A1%88.ipynb) [開啟範例 Notebook](./學生素材/%E7%AF%84%E4%BE%8B_%E8%8C%B6%E8%AA%9E%E6%99%82%E5%85%89_%E9%A1%A7%E5%AE%A2%E8%A9%95%E8%AB%96%E8%88%87%E8%8F%9C%E5%96%AE%E6%AA%94%E6%A1%88.ipynb)　｜　[⬇️ 下載本章素材 檔案存取_學生素材.zip](https://github.com/roberthsu2003/PythonForDataAnalysis/raw/master/%E6%AA%94%E6%A1%88%E5%AD%98%E5%8F%96/%E6%AA%94%E6%A1%88%E5%AD%98%E5%8F%96_%E5%AD%B8%E7%94%9F%E7%B4%A0%E6%9D%90.zip)

| 素材檔案 | 內容 |
| --- | --- |
| `菜單.csv` | 10 個品項的價格與成本 |
| `門市資訊.json` | 5 家門市的營業時間、外送、熱銷品項（巢狀 JSON） |
| `顧客評論.txt` | 3 月份 120 則顧客評論 |
| `舊系統會員_big5.csv` | 舊 POS 系統匯出的會員檔（Big5 編碼，會亂碼！） |
| `課程原始資料/` | 本章課堂 Notebook 使用的原始資料檔 |

**使用方式**：下載壓縮檔並解壓縮後，用 Jupyter 或 VS Code 開啟範例 Notebook，從上到下依序執行即可；若直接在 Colab 開啟，第一格程式會自動下載本章素材。範例最後附有練習題與參考解答。

---

## 💡 1. 為什麼需要這個觀念？（生活化比喻）

- **開檔就像「借閱圖書館的書」**：先 `open()`（借書）、讀完或寫完之後一定要 `close()`（還書）。沒還書，別人（其他程式）就借不到，寫到一半的內容也可能沒存進去。用 `with` 寫法就像「自動還書機」，離開區塊就自動歸還。
- **CSV 就像「純文字版的 Excel」**：每一列一筆資料、欄位之間用逗號隔開。它沒有顏色、沒有公式，而且**所有內容都是文字**——連數字 `87` 讀進來也是字串 `'87'`。
- **JSON 就像「一層一層的資料夾」**：外層資料夾裡有子資料夾，子資料夾裡才是真正的檔案。政府開放資料、網站 API 幾乎都用 JSON，你要知道真正的資料「藏在哪一層」。
- **編碼（UTF-8）就像「翻譯字典」**：存檔用 A 字典、讀檔用 B 字典，中文就會變成亂碼。原則很簡單：**存和讀都指定 `encoding='utf-8'`**。

| **核心概念** | **生活化直觀比喻** | **傳統工程師痛苦點** | **AI 時代你的角色** |
| -------- | ----------- | ------------ | ------------- |
| `open()` / `with` | 借書與自動還書機 | 忘了關檔，資料寫不完整 | 要求 AI「一律用 with 開檔」 |
| 讀寫模式 `r` / `w` / `a` | 只看不改／整本重寫／在最後加頁 | 誤用 `w` 把舊資料整個蓋掉 | 說清楚「覆蓋」還是「附加」 |
| CSV | 純文字版 Excel 表格 | 數字都是字串，計算時報錯 | 提醒 AI「把數字欄位轉成數值」 |
| JSON | 一層一層的資料夾 | 搞不清楚資料在第幾層 | 貼一小段 JSON 給 AI 看結構 |
| 編碼 UTF-8 | 讀寫要用同一本翻譯字典 | 中文變亂碼，不知從何查起 | 指定「UTF-8 讀寫」，亂碼時請 AI 試 `utf-8-sig` 或 `big5` |
| 例外處理 `try/except` | 借書時發現書不見，要有備案 | 程式一遇到缺檔就整個當掉 | 要求 AI「找不到檔案時給清楚提示」 |

---

## 📐 2. 資料長什麼樣子？（直觀結構圖解）

**① CSV：純文字 → 二維清單（一列一筆）**

![CSV 純文字讀成二維清單](./圖解/csv%E8%BD%89%E4%BA%8C%E7%B6%AD%E6%B8%85%E5%96%AE.svg)

**② JSON：一層一層的資料夾 → 取出真正的資料清單**

![JSON 一層一層取出資料](./圖解/json%E5%B7%A2%E7%8B%80%E7%B5%90%E6%A7%8B.svg)

---

## 💻 3. 核心精華操作（複製貼上即可驗證）

> 學生不需要自己寫，但只要讀懂關鍵邏輯即可。以下程式碼會自己產生範例檔，在 Colab 直接執行即可。

### 🔹 核心技巧 1：用 `with` 安全地寫入與讀取文字檔

**商業意義**：會議紀錄、系統日誌、問卷文字回覆都是文字檔。用 `with` 開檔，就不用擔心忘記關檔造成資料遺失。

```python
text = '''python與中文
1. 我們來試試看中文儲存能力。
2. 犇這個字必須是 utf-8 編碼才存得下來。'''   # 準備要寫入的多行文字

# 'w' = 寫入模式（檔案已存在會被整個覆蓋）；encoding 指定 UTF-8 避免中文亂碼
with open('data.txt', 'w', encoding='utf-8') as file:
    file.write(text)                          # 把文字寫進檔案；離開 with 區塊會自動關檔

# 'r' = 讀取模式；同樣要用 UTF-8 讀，才不會出現亂碼
with open('data.txt', 'r', encoding='utf-8') as file:
    for line in file:                         # 一次讀一行，適合大型檔案
        print(line.strip())                   # strip() 去掉每行頭尾的空白與換行符號
```

### 🔹 核心技巧 2：寫入與讀取 CSV 表格

**商業意義**：CSV 是各系統（ERP、POS、資料庫、Excel）之間交換資料的「共通語言」，會讀寫 CSV，就能接收幾乎所有系統匯出的報表。

```python
import csv                                    # 匯入 Python 內建的 CSV 工具

# 寫入：newline='' 可避免 Windows 上每列之間多出空白列
with open('students.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)                 # 建立「CSV 寫手」
    writer.writerow(['編號', '國文', '英文', '數學'])   # 第一列：欄位標題
    writer.writerow(['01', 87, 90, 56])       # 第二列：第 1 位學生
    writer.writerow(['02', 98, 56, 78])       # 第三列：第 2 位學生

# 讀取：DictReader 會自動把第一列當成欄位名稱
with open('students.csv', 'r', encoding='utf-8') as file:
    for row in csv.DictReader(file):          # 每一列變成一個「欄位名稱 → 值」的字典
        total = int(row['國文']) + int(row['英文']) + int(row['數學'])  # ⚠️ 讀進來是文字，要先 int() 轉成數字
        print(row['編號'], '總分：', total)    # 結果：01 總分：233、02 總分：232
```

### 🔹 核心技巧 3：Python 資料 ↔ JSON 檔

**商業意義**：網站 API、政府開放資料、App 設定檔幾乎都是 JSON。會存取 JSON，就能把網路上的即時資料接進你的分析流程。

```python
import json                                   # 匯入 Python 內建的 JSON 工具

students = [{'姓名': 'stu1', '國文': 58, '英文': 61},   # 清單裡放字典：一位學生一筆
            {'姓名': 'stu2', '國文': 82, '英文': 62}]

# 存檔：ensure_ascii=False 讓中文以原字儲存，不會變成 姓 這種代碼
with open('students.json', 'w', encoding='utf-8') as file:
    json.dump(students, file, ensure_ascii=False)

# 讀檔：json.load() 把 JSON 檔還原成 Python 的清單與字典
with open('students.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
print(data[1]['姓名'], data[1]['國文'])      # 取第 2 筆的姓名與國文成績：stu2 82
```

### 🔹 核心技巧 4：例外處理——找不到檔案時不要整個當掉

**商業意義**：自動化報表每天要讀的檔案，可能因為上游還沒產出而不存在。加上例外處理，程式會給出清楚的錯誤訊息，而不是一堆看不懂的紅字。

```python
try:                                          # 「試試看」執行下面的程式
    with open('不存在的報表.csv', 'r', encoding='utf-8') as f:
        print(f.read())
except FileNotFoundError:                     # 如果發生「找不到檔案」
    print('找不到檔案，請確認檔名或先上傳檔案')   # 給使用者看得懂的提示
except PermissionError:                       # 如果發生「沒有權限」
    print('你沒有權限存取這個檔案')
```

---

## 🤖 4. 指揮 AI 的專屬指令手冊（Prompt 實戰專區）

當你在實務工作遇到此類資料時，直接複製以下 Prompt 讓 AI 替你分析：

> **📋 AI 指揮範本（通用版）**：
>
> 「你現在是我的資深 Python 資料分析師。我有一份 **[例如：從政府開放資料平台下載的新北市公共自行車 JSON 檔]**，我想了解 **[例如：新店區每個站點的名稱、地址與目前可借車輛數]**。
>
> 以下是檔案的前幾行內容：**[貼上 CSV 前 5 列，或 JSON 的前 20 行]**
>
> 請你：
> 1. 使用 Python 內建的 **`csv` / `json` 模組**，並一律用 `with` 與 `encoding='utf-8'` 開檔。
> 2. 詳細解釋每一步的處理邏輯，特別說明資料藏在 JSON 的哪一層、CSV 的哪一欄。
> 3. 產出繁體中文說明的完整程式碼，並標註潛在的資料異常陷阱（例如：亂碼、數字帶有千分位逗號、缺少欄位、找不到檔案）。」

**🎯 情境延伸範本**（依需求替換）：

| 你想問的商業問題 | 直接對 AI 說 |
| --- | --- |
| 只要報表中的某幾欄 | 「這是證交所的個股日成交資訊 CSV，第一列是標題，請只取出證券代號、名稱、收盤價、漲跌價差四欄，存成新的 CSV。」 |
| 從 JSON 撈出特定資料 | 「這是 JSON 的前 20 行，請告訴我資料清單在哪一層，並列出所有『新店區』的站名與地址。」 |
| 中文變亂碼 | 「我用 UTF-8 讀這個 CSV 出現亂碼，請幫我判斷可能的編碼（utf-8-sig、big5、cp950），並寫出能自動嘗試的讀檔程式。」 |
| 定期下載資料存檔 | 「請寫一段程式，下載這個 API 的 JSON，取出縣市與天氣描述，存成 UTF-8 的 CSV，下載失敗時要顯示提示。」 |

> ⚠️ **驗收小撇步**：拿到結果後，用 Excel 或記事本打開輸出的檔案，確認「中文正常顯示」、「筆數和原始資料一致」、「第一列是標題」。

> 🕵️ **真實陷阱案例**：本章的 [個股日成交資訊](./個股日成交資訊.ipynb) 中，成交股數寫成 `'46,790,503'`——**帶有千分位逗號的文字**，不能直接拿來加總。記得請 AI「先去掉逗號再轉成數字」。

---

## 🎯 5. 本章檢查清單（自我驗收）

- [ ] 我能理解 **讀取模式 `r`**、**覆蓋寫入 `w`** 與 **附加寫入 `a`** 的差異。
- [ ] 我知道為什麼要用 `with` 開檔，以及沒關檔可能造成的問題。
- [ ] 我能分辨 **CSV（表格）** 與 **JSON（一層一層的資料夾）** 的結構差異。
- [ ] 我知道 CSV 讀進來的內容都是文字，計算前要先轉成數字。
- [ ] 遇到中文亂碼時，我知道要從「編碼」下手請 AI 協助。
- [ ] 我能看懂 AI 生成程式中 `csv.reader`、`csv.DictReader`、`json.load`、`json.dump` 的用途。
- [ ] 我能複製 Prompt 範本，貼上檔案前幾行，並替換成自己的業務問題。
