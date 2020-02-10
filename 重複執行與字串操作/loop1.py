#!usr/bin/python3

"""
2 - 10所有偶數的總和
"""

sum = 0
i = 2
while(i <= 10):
    sum += i
    print("第",i/2,"次迴圈的i =",i,"總和為", sum);
    i += 2
