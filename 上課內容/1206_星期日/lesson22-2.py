from tkinter import *
import csv

def main(w):
    gui(w)
    w.mainloop()

def gui(w):
    global scrollbar, mylist, message
    w.title("收集資料")
    # w.geometry('500x300')
    topFrame = Frame(w,bd=1,relief=GROOVE)
    topFrame.config(bg="#dddddd")
    Button(topFrame, text="空氣品質指標",font=('Verdans',13,'bold'),command=aqi).pack(ipadx=25, ipady=10, side=LEFT, expand=YES)
    Button(topFrame, text="確定2",font=('Verdans',13,'bold')).pack(ipadx=25, ipady=10, side=LEFT, expand=YES)
    Button(topFrame, text="確定3",font=('Verdans',13,'bold')).pack(ipadx=25, ipady=10, side=LEFT, expand=YES)
    topFrame.pack(ipady=20,ipadx=20,pady=20,padx=20)

    bottomFrame = Frame(w,bd=1,relief=GROOVE)
    scrollbar = Scrollbar(bottomFrame)
    scrollbar.pack(side=LEFT)
    mylist = Listbox(bottomFrame,selectmode=SINGLE,yscrollcommand=scrollbar.set)
    #register-選取改變
    mylist.bind('<<ListboxSelect>>', changeSelected)
    mylist.pack(side=LEFT, fill=BOTH)
    message = StringVar()
    Label(bottomFrame,textvariable=message,justify=LEFT).pack(side=LEFT)
    message.set("狀態:")
    bottomFrame.pack(ipady=20,ipadx=20,pady=20,padx=20,expand=YES,fill=X)

def aqi():
    # 下載AQI
    global rows
    with open("空氣品質指標.csv","r",encoding='UTF-8') as file:
        #content = file.read()
        next(file)
        rows=csv.reader(file)
        rows = list(rows)
        for item in rows:
            mylist.insert(END,item[0])


        scrollbar.config(command = mylist.yview)
        file.close()



def changeSelected(event):
    #傳出tuple,第一個是選取的索引
    selectedIndex= mylist.curselection()[0]
    print(selectedIndex)
    #print(mylist.get(mylist.curselection()))
    siteName = rows[selectedIndex][0]
    country = rows[selectedIndex][1]
    aqi = rows[selectedIndex][2]
    pollutant = rows[selectedIndex][3]
    status = rows[selectedIndex][4]
    print(siteName, country, aqi, pollutant, status)
    message.set("狀態:\n\n 監測站:%s \n 縣市:%s \n AQI:%s \n 浮粒:%s \n 狀態:%s" % (siteName, country, aqi, pollutant, status))


if __name__ == "__main__":
    rows = None
    scrollbar = None
    mylist = None
    message = None
    window = Tk()
    main(window)
#https://docs.google.com/forms/d/e/1FAIpQLSeQmoajuMAlFiqzA_7nSgoGXaSzDNK244BoPczBI82IPV_62A/viewform?usp=sf_link
