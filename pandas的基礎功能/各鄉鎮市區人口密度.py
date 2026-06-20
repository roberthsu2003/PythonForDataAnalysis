import tkinter as tk
from tkinter import ttk
import pandas as pd



# ==================================
# 讀取 CSV 並整理資料
# ==================================

def load_data():

    df = pd.read_csv(
        '各鄉鎮市區人口密度.csv'
    )


    # 第一列當欄位名稱
    df.columns = df.loc[0]


    # 移除第一列
    df = df.drop(0)


    # 移除最後5筆非資料內容
    df = df.iloc[:-5]


    # 重設 index
    df.index = range(len(df))


    # 取需要欄位
    df = df.reindex(
        columns=[
            '區域別',
            '年底人口數',
            '土地面積'
        ]
    )


    # 欄位重新命名
    df = df.rename(
        columns={
            '年底人口數':'人口數'
        }
    )


    # ===========================
    # 轉換數字
    # ===========================

    df['人口數'] = pd.to_numeric(
        df['人口數'],
        errors='coerce'
    )


    df['土地面積'] = pd.to_numeric(
        df['土地面積'],
        errors='coerce'
    )


    # 移除錯誤資料
    df = df.dropna()


    # ===========================
    # 計算人口密度
    # ===========================

    df['人口密度'] = (
        df['人口數']
        /
        df['土地面積']
    )


    return df




# 取得資料

dataFrame = load_data()





# ==================================
# Tkinter GUI
# ==================================

window = tk.Tk()


window.title(
    "台灣鄉鎮市區人口密度查詢系統"
)


window.geometry(
    "900x600"
)





# ==================================
# 上方控制區
# ==================================

topFrame = tk.Frame(window)

topFrame.pack(
    pady=10
)



label = tk.Label(
    topFrame,
    text="輸入區域名稱：",
    font=("Arial",14)
)


label.pack(
    side=tk.LEFT
)




keyword = tk.StringVar()



entry = tk.Entry(
    topFrame,
    textvariable=keyword,
    font=("Arial",14),
    width=20
)


entry.pack(
    side=tk.LEFT,
    padx=10
)






# ==================================
# Treeview 表格
# ==================================


columns = (
    "區域別",
    "人口數",
    "土地面積",
    "人口密度"
)



tree = ttk.Treeview(
    window,
    columns=columns,
    show="headings"
)




for col in columns:


    tree.heading(
        col,
        text=col
    )


    tree.column(
        col,
        width=180,
        anchor="center"
    )



tree.pack(
    expand=True,
    fill="both",
    padx=20,
    pady=10
)





# ==================================
# 顯示資料
# ==================================

def show_data(df):


    # 清空表格

    for item in tree.get_children():

        tree.delete(item)



    # 填入資料

    for _, row in df.iterrows():


        tree.insert(

            "",

            tk.END,

            values=(

                row['區域別'],

                int(row['人口數']),

                row['土地面積'],

                round(
                    row['人口密度'],
                    2
                )

            )

        )





# 初始顯示全部

show_data(dataFrame)






# ==================================
# 查詢功能
# ==================================

def search_data():


    text = keyword.get()



    if text == "":


        result = dataFrame



    else:


        result = dataFrame[
            dataFrame['區域別']
            .astype(str)
            .str.contains(text)
        ]



    show_data(result)





button = tk.Button(

    topFrame,

    text="查詢",

    font=("Arial",14),

    command=search_data

)



button.pack(
    side=tk.LEFT
)







# ==================================
# 啟動程式
# ==================================

window.mainloop()