import random
print("random",random.randint(1,100))
print("randint",random.randrange(1,100,2))
min=1
max=100
count=0
target=random.randint(1,100)
print("===========猜數字========")
while True:
    count+=1
    keyin=int(input("猜數字"+str(min)+"~"+str(max)+":"))
    if keyin>=min and keyin<=max:
        if keyin==target:
            print("猜對了，答案是:",target)
            print("你猜了",count,"次")
            break
        elif keyin>target:
            print("再小一點")
            max=keyin-1
        elif keyin<target:
            print("再大一點")
            min=keyin+1
            print("你已經猜了",count,"次")
    else:
            print("輸入提示範圍內的數字")