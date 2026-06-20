# ==========================================
# Homework3 GUI 版本
# pandas + tkinter 資料查詢系統
# ==========================================


# ------------------------------
# import 區域
# ------------------------------

import tkinter as tk
from tkinter import messagebox

import pandas as pd



# ------------------------------
# 資料處理函式
# ------------------------------

def load_data():

    """
    讀取 world.csv

    回傳整理後的 DataFrame
    """

    try:

        dataFrame = pd.read_csv("world.csv")


        # 保留 Homework3 使用的欄位
        dataFrame = dataFrame.reindex(
            columns=[
                '洲名',
                '國家',
                '日期',
                '總確診數',
                '新增確診數',
                '總人口數',
                '解封指數'
            ]
        )


        return dataFrame


    except:

        messagebox.showerror(
            "錯誤",
            "找不到 world.csv\n請確認檔案位置"
        )

        return None




# ------------------------------
# GUI Button 事件
# ------------------------------


def search_country():

    """
    查詢指定國家的所有資料

    Button:
    查詢資料
    """

    country = country_entry.get()


    if country == "":

        messagebox.showwarning(
            "提醒",
            "請輸入國家名稱"
        )

        return



    result = dataFrame.query(
        f'國家=="{country}"'
    )


    show_result(result)




def search_zero():

    """
    查詢新增確診數 = 0

    保留 Homework3 query()
    """

    country = country_entry.get()


    if country == "":

        messagebox.showwarning(
            "提醒",
            "請輸入國家名稱"
        )

        return



    result = dataFrame.query(
        f'國家=="{country}" and 新增確診數==0'
    )


    show_result(result)




def search_max():

    """
    查詢最多新增確診資料
    """

    country = country_entry.get()


    if country == "":

        messagebox.showwarning(
            "提醒",
            "請輸入國家名稱"
        )

        return



    country_data = dataFrame.query(
        f'國家=="{country}"'
    )


    if len(country_data)==0:

        messagebox.showinfo(
            "結果",
            "沒有找到資料"
        )

        return



    max_number = country_data[
        '新增確診數'
    ].max()



    result = dataFrame.query(
        f'國家=="{country}" and 新增確診數=={max_number}'
    )


    show_result(result)




def search_year():

    """
    查詢2022年的資料
    """

    country = country_entry.get()


    if country == "":

        messagebox.showwarning(
            "提醒",
            "請輸入國家名稱"
        )

        return



    result = dataFrame.query(
        f'國家=="{country}" and 日期>="2022-01-01"'
    )


    show_result(result)




def clear_result():

    """
    清除 Text 顯示內容
    """

    result_text.delete(
        "1.0",
        tk.END
    )




# ------------------------------
# 顯示資料
# ------------------------------

def show_result(result):

    """
    將 DataFrame 顯示到 Text
    """

    result_text.delete(
        "1.0",
        tk.END
    )


    if len(result)==0:

        result_text.insert(
            tk.END,
            "沒有資料"
        )

        return



    result_text.insert(
        tk.END,
        result.to_string(index=False)
    )





# ------------------------------
# GUI 建立
# ------------------------------


def create_gui():


    global country_entry
    global result_text



    window = tk.Tk()


    window.title(
        "COVID-19 世界資料查詢系統"
    )


    window.geometry(
        "900x600"
    )



    # ----------------------
    # 第一區 Frame
    # 輸入區
    # ----------------------

    input_frame = tk.Frame(window)

    input_frame.pack(
        pady=10
    )



    tk.Label(
        input_frame,
        text="請輸入國家：",
        font=("Arial",14)
    ).grid(
        row=0,
        column=0
    )



    country_entry = tk.Entry(
        input_frame,
        width=20
    )


    country_entry.grid(
        row=0,
        column=1
    )



    # ----------------------
    # Button區
    # ----------------------


    button_frame = tk.Frame(window)

    button_frame.pack(
        pady=10
    )



    tk.Button(
        button_frame,
        text="查詢資料",
        width=15,
        command=search_country
    ).grid(
        row=0,
        column=0,
        padx=5
    )



    tk.Button(
        button_frame,
        text="新增確診=0",
        width=15,
        command=search_zero
    ).grid(
        row=0,
        column=1,
        padx=5
    )



    tk.Button(
        button_frame,
        text="最高新增確診",
        width=15,
        command=search_max
    ).grid(
        row=0,
        column=2,
        padx=5
    )



    tk.Button(
        button_frame,
        text="查詢2022資料",
        width=15,
        command=search_year
    ).grid(
        row=0,
        column=3,
        padx=5
    )



    tk.Button(
        button_frame,
        text="清除結果",
        width=15,
        command=clear_result
    ).grid(
        row=0,
        column=4,
        padx=5
    )



    # ----------------------
    # 顯示區
    # ----------------------


    result_frame = tk.Frame(window)

    result_frame.pack(
        fill="both",
        expand=True
    )



    result_text = tk.Text(
        result_frame,
        width=100,
        height=25
    )


    result_text.pack(
        padx=10,
        pady=10
    )



    window.mainloop()




# ------------------------------
# main()
# ------------------------------


def main():

    global dataFrame


    dataFrame = load_data()


    if dataFrame is not None:

        create_gui()



# 程式開始

if __name__ == "__main__":

    main()