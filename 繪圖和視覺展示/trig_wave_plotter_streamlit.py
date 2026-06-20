# 執行方式: streamlit run interactive_wave.py

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# 1. 設定中文字型與負號顯示，確保在 Windows 與 macOS 正常顯示中文
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial Unicode MS', 'Heiti TC', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False  # 解決座標軸負號「-」顯示為方塊的問題

# 2. 設定 Streamlit 網頁基本配置
st.set_page_config(
    page_title="互動式正弦與餘弦波形繪圖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 3. 網頁標題與描述
st.title("📊 互動式正弦 (sin) 與餘弦 (cos) 波形繪圖工具")
st.markdown("""
這是一個使用 **Streamlit** 與 **Matplotlib** 建立的互動式波形繪圖網頁。
您可以透過左側的**側邊欄滑桿**即時調整參數，右側的波形圖將會動態更新！
""")

# 4. 在側邊欄建立互動控制元件 (Streamlit Sliders)
st.sidebar.header("⚙️ 參數設定")

# 振幅 (A)：調整範圍 0.1 至 5.0，預設 1.0
amplitude = st.sidebar.slider(
    "振幅 (Amplitude, A)", 
    min_value=0.1, 
    max_value=5.0, 
    value=1.0, 
    step=0.1
)

# 頻率 (ω)：調整範圍 0.1 至 10.0，預設 1.0
frequency = st.sidebar.slider(
    "頻率 (Frequency, ω)", 
    min_value=0.1, 
    max_value=10.0, 
    value=1.0, 
    step=0.1
)

# 相位偏移 (φ)：調整範圍 0 至 2π，預設 0.0
phase = st.sidebar.slider(
    "相位偏移 (Phase, φ)", 
    min_value=0.0, 
    max_value=float(2 * np.pi), 
    value=0.0, 
    step=0.05,
    format="%.2f rad"
)

# 5. 建立 X 軸數據與計算 Y 軸波形數據
# 範圍從 0 到 4π，生成 1000 個點以確保曲線平滑
x = np.linspace(0, 4 * np.pi, 1000)
y_sin = amplitude * np.sin(frequency * x + phase)
y_cos = amplitude * np.cos(frequency * x + phase)

# 6. 使用 Matplotlib 進行圖表繪製
# 建立一個適合網頁顯示的畫布大小
fig, ax = plt.subplots(figsize=(10, 5.5))

# 繪製正弦與餘弦兩條曲線
ax.plot(x, y_sin, lw=2.5, color='#1f77b4', label='正弦波 (sin)')
ax.plot(x, y_cos, lw=2.5, color='#ff7f0e', linestyle='--', label='餘弦波 (cos)')

# 設定圖表標題、軸標籤與格線
ax.set_title(
    f'波形展示 (A={amplitude}, ω={frequency}, φ={phase:.2f} rad)', 
    fontsize=14, 
    fontweight='bold', 
    pad=15
)
ax.set_xlabel('相位 (弧度 rad)', fontsize=12)
ax.set_ylabel('振幅 (y)', fontsize=12)
ax.grid(True, linestyle=':', alpha=0.6)  # 開啟格線

# 設定 X 軸的刻度顯示為 π 的倍數，方便觀察週期性
x_ticks = np.arange(0, 4.1 * np.pi, np.pi)
x_labels = ['0', 'π', '2π', '3π', '4π']
ax.set_xticks(x_ticks)
ax.set_xticklabels(x_labels)

# 固定 Y 軸範圍，避免調整滑桿時軸尺度不斷縮放，影響視覺體驗
ax.set_ylim(-5.5, 5.5)

# 顯示圖例
ax.legend(loc='upper right', frameon=True, shadow=True, fontsize=10)

# 7. 將 Matplotlib 繪製出的圖表渲染至 Streamlit 頁面中
st.pyplot(fig)

# 8. 顯示數值摘要（額外加分項目：幫助使用者閱讀精準數值）
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="當前振幅 (A)", value=f"{amplitude}")
with col2:
    st.metric(label="當前頻率 (ω)", value=f"{frequency} Hz")
with col3:
    st.metric(label="當前相位 (φ)", value=f"{phase:.3f} rad")