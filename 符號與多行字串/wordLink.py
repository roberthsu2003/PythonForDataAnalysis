#!usr/bin/python3

"""
字串文字接龍
"""
outstr=""
print('失敗就會退出遊戲!')
inputstr = input('請輸入一個接龍字串:')#python
while(True):
    outstr += inputstr #outstr = python
    print("上一個字串是:",outstr)
    keyin = (input("請輸入-"+inputstr[-1]+"-開始的字串:"))
    if(keyin[0]!=inputstr[-1]):
                     print("遊戲失敗")
                     break
    elif(keyin[0]==inputstr[-1]):
             inputstr ="-"+keyin 