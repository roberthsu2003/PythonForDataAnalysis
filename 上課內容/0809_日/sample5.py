#!usr/bin/python3

'''
這是一個猜數字遊戲
開發者:robertHsu
'''

from random import randint

min = 1
max = 100
cout = 0
target = randint(min,max)
print("============猜數字遊戲===============")
while True:
    cout += 1
    keyin = int(input("猜數字範圍%d~%d:" % (min, max)))
    if(keyin >= min and keyin <= max):
        if keyin == target:
            print("賓果!猜對了, 答案是:%d" % target)
            print("您猜了%d次" % cout)
            break
        elif keyin > target:
            max = keyin
            print("再小一點")
        elif keyin < target:
            min = keyin;
            print("再大一點")
        print("您猜了%d次\n" % cout)
    else:
        print("請輸入提示範圍內的數字")
print("程式結束")