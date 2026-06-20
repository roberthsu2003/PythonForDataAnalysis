## sin, cos 函式繪圖應用(Streamlit版)

### 互動式繪圖應用程式 Prompt

學生可以使用以下 Prompt 來請 AI 生成一個整合 `numpy` 與 `matplotlib` 的互動式繪圖應用程式：

```text
請使用 Python 撰寫一個互動式的正弦（sin）與餘弦（cos）波形繪圖應用程式。
要求如下：
1. **核心套件**：使用 `numpy` 進行數值運算，並使用 `matplotlib` 進行繪圖與互動控制。
2. **圖表介面**：
   - 在同一個圖表中同時繪製 y = A * sin(ω * x + φ) 和 y = A * cos(ω * x + φ) 兩條曲線。
   - 包含格線（grid）、圖表標題、X/Y 軸標籤，以及圖例（Legend）以區分 sin 和 cos。
   - X 軸範圍設定為 0 到 4π。
   - **中文字型支援**：圖表的標題、軸標籤和圖例必須使用繁體中文顯示，且程式中必須正確設定 `plt.rcParams['font.sans-serif']`（可設定支援 macOS 的 `'Arial Unicode MS'`、`'Heiti TC'` 或 Windows 的 `'Microsoft JhengHei'` 微軟正黑體），確保中文字元均能正常顯示，不會出現方塊或亂碼。
3. **互動控制（Streamlit Widgets）**：
   - 在圖表上方加入三個滑桿（Slider），讓使用者可以即時調整以下參數：
     - **振幅 (Amplitude, A)**：調整範圍 0.1 至 5.0，預設為 1.0。
     - **頻率 (Frequency, ω)**：調整範圍 0.1 至 10.0，預設為 1.0。
     - **相位偏移 (Phase, φ)**：調整範圍 0 至 2π，預設為 0。
   - 當使用者拖曳滑桿時，波形必須即時更新。
4. **程式碼品質**：
   - 程式碼結構需清晰，並包含繁體中文註解，以利學習。
   - 確保該程式可以直接在終端機運行並顯示獨立的互動視窗。
```

**完成範例**
[[source,python]](trig_wave_plotter_streamlit.py)