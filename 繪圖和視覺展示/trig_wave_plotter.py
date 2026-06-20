import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import platform

# ==========================================
# 1. 中文字型支援設定 (解決 matplotlib 中文亂碼問題)
# ==========================================
def set_chinese_font():
    """
    根據不同的作業系統，自動設定 matplotlib 的繁體中文字型
    """
    sys_plat = platform.system()
    if sys_plat == 'Windows':
        # Windows 系統使用微軟正黑體
        plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial Unicode MS']
    elif sys_plat == 'Darwin':
        # macOS 系統使用儷黑體、Heiti TC 或 Arial Unicode MS
        plt.rcParams['font.sans-serif'] = ['Heiti TC', 'Arial Unicode MS', 'AppleGothic']
    else:
        # Linux / Unix 系統常規設定
        plt.rcParams['font.sans-serif'] = ['Noto Sans CJK TC', 'Liberation Sans', 'DejaVu Sans']
    
    # 修正負號 '-' 顯示為方塊的問題
    plt.rcParams['axes.unicode_minus'] = False

set_chinese_font()

# ==========================================
# 2. 初始化參數與數據計算
# ==========================================
# 設定 X 軸範圍從 0 到 4π (共 1000 個點，確保曲線平滑)
x = np.linspace(0, 4 * np.pi, 1000)

# 初始參數設定
init_amplitude = 1.0   # 初始振幅 (A)
init_frequency = 1.0   # 初始頻率 (ω)
init_phase = 0.0       # 初始相位 (φ)

# 計算初始波形數據
# 正弦波: y = A * sin(ω * x + φ)
# 餘弦波: y = A * cos(ω * x + φ)
y_sin = init_amplitude * np.sin(init_frequency * x + init_phase)
y_cos = init_amplitude * np.cos(init_frequency * x + init_phase)

# ==========================================
# 3. 建立圖表與版面配置
# ==========================================
# 建立主視窗，並預留下方空間放置滑桿
fig, ax = plt.subplots(figsize=(10, 6.5))
plt.subplots_adjust(bottom=0.3)  # 將圖表向上推，預留 30% 的底部空間給滑桿

# 繪製初始正弦波與餘弦波
# line_sin, 代表正弦曲線，使用實線與藍色
# line_cos, 代表餘弦曲線，使用虛線與紅色
line_sin, = ax.plot(x, y_sin, lw=2, color='#1f77b4', label='正弦波 (y = A * sin(ωx + φ))')
line_cos, = ax.plot(x, y_cos, lw=2, color='#d62728', linestyle='--', label='餘弦波 (y = A * cos(ωx + φ))')

# 設定圖表標題、軸標籤與格線
ax.set_title('互動式正弦與餘弦波形繪圖工具', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('時間 / 位置 (x)', fontsize=12)
ax.set_ylabel('振幅 (y)', fontsize=12)
ax.set_xlim(0, 4 * np.pi)
ax.set_ylim(-6.0, 6.0)  # Y 軸設定稍微大於最大振幅(5.0)，避免波形頂部被切掉
ax.grid(True, linestyle=':', alpha=0.6)

# 設定 X 軸刻度以 π 為單位，方便觀察
x_ticks = np.arange(0, 4.1 * np.pi, np.pi)
x_labels = [f'{int(i)}π' if i > 0 else '0' for i in range(5)]
# 修正 1π 顯示為 π
x_labels[1] = 'π'
ax.set_xticks(x_ticks)
ax.set_xticklabels(x_labels)

# 顯示圖例
ax.legend(loc='upper right', fontsize=10, shadow=True)

# ==========================================
# 4. 建立互動滑桿 (Sliders)
# ==========================================
# 定義滑桿的顏色
ax_color = 'lightgoldenrodyellow'

# 1. 振幅滑桿的位置與屬性 (A)
# [left, bottom, width, height]
ax_amp = plt.axes([0.15, 0.18, 0.7, 0.03], facecolor=ax_color)
slider_amp = Slider(
    ax=ax_amp,
    label='振幅 (Amplitude, A) ',
    valmin=0.1,
    valmax=5.0,
    valinit=init_amplitude,
    valfmt='%1.1f'
)

# 2. 頻率滑桿的位置與屬性 (ω)
ax_freq = plt.axes([0.15, 0.12, 0.7, 0.03], facecolor=ax_color)
slider_freq = Slider(
    ax=ax_freq,
    label='頻率 (Frequency, ω) ',
    valmin=0.1,
    valmax=10.0,
    valinit=init_frequency,
    valfmt='%1.1f'
)

# 3. 相位滑桿的位置與屬性 (φ)
ax_phase = plt.axes([0.15, 0.06, 0.7, 0.03], facecolor=ax_color)
slider_phase = Slider(
    ax=ax_phase,
    label='相位 (Phase, φ) ',
    valmin=0.0,
    valmax=2 * np.pi,
    valinit=init_phase,
    valfmt='%1.2f rad'
)

# ==========================================
# 5. 更新函式與事件綁定
# ==========================================
def update(val):
    """
    當滑桿數值改變時被觸發，重新計算數據並更新圖表
    """
    # 取得當前滑桿的數值
    a = slider_amp.val
    w = slider_freq.val
    phi = slider_phase.val
    
    # 重新計算 sin 與 cos 的 y 值
    new_y_sin = a * np.sin(w * x + phi)
    new_y_cos = a * np.cos(w * x + phi)
    
    # 更新曲線數據
    line_sin.set_ydata(new_y_sin)
    line_cos.set_ydata(new_y_cos)
    
    # 重新繪製視窗
    fig.canvas.draw_idle()

# 將滑桿的數值更動事件綁定到 update 函式上
slider_amp.on_changed(update)
slider_freq.on_changed(update)
slider_phase.on_changed(update)

# ==========================================
# 6. 啟動應用程式
# ==========================================
if __name__ == '__main__':
    # 顯示繪圖視窗
    plt.show()