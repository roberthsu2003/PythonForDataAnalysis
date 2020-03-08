a = 5#全域變數(top_level變數)

def func_one():
    temp = a+1 #區域變數
    print('函式內呼叫:',a)


func_one()
print('函式外呼叫:',a)