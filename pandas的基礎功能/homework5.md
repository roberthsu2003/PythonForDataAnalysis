## 業務員季度業績 

```text
請幫我用 Python 的 Streamlit 寫一支可以執行的網頁應用程式,主題是「業務員季度業績統計儀表板」。

【資料來源】
1. 使用 numpy 的 np.random.randint 產生 30 位業務員、4 個季度(第一季、第二季、第三季、第四季)的隨機業績資料,範圍 10~100(單位:萬元)。
2. 用 pandas 建立 DataFrame,index 為業務員編號 1~30(index.name 設為「業務員編號」),欄位名稱為四個季度(columns.name 設為「季度」)。
3. 為了讓每次重新整理不會一直變動,請用 @st.cache_data 把產生資料的函式包起來。

【統計需求(務必使用 DataFrame.apply())】
1. 定義一個函式 cal(s),回傳一個 pd.Series,內容包含:總業績、平均業績、最高業績。
2. 用 sales_pd.apply(cal) 對每一個季度(每一欄)計算上述統計,得到一個統計結果 DataFrame。

【網頁畫面需求】
1. 標題用 st.title 顯示「業務員季度業績統計儀表板」。
2. 用 st.dataframe 顯示原始業績資料表。
3. 用 st.subheader 加上 st.dataframe 顯示 apply() 算出的統計結果表(總業績/平均業績/最高業績)。
4. 圖表整合:
   - 用 st.bar_chart 畫出「各季度總業績」的長條圖。
   - 用 st.line_chart 畫出「各季度平均業績」的折線圖。
5. 加一個 st.selectbox 讓使用者選擇某一個季度,選擇後用 st.metric 顯示該季度的總業績、平均業績、最高業績三個數字。

【其他要求】
1. 程式要完整、可直接執行,所有 import 都要寫出來。
2. 在程式碼中加上中文註解,說明每一段在做什麼。
3. 最後請另外用文字告訴我:要先安裝哪些套件(pip install ...),以及用什麼指令啟動(streamlit run 檔名.py)。
```
