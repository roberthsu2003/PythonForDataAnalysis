## 迴圈Loop
###  重複執行概念
- 重覆執行可以讓程式中某一區段流程反覆執行
- 重複執行可用 while 及 for 兩種方式設計

### while 迴圈的架構如下:
```python
設定控制迴圈變數的初始值
while 條件分析:
	條件成立下執行迴圈要執行的工作
	調整控制迴圈變數的內容
```

### while 迴圈
- 當 while 迴圈的條件分析成立時，才會進入到迴圈。
- 若 while 迴圈的條件分析不成立，則跳出迴圈。
- 若 while 迴圈內條件分析一開始不成立，則迴圈一次都不執行。

#### while 迴圈:請動手操作，並留意輸出結果
```python
#while1.py


a=6
while a > 0:
	print(a)
	a -= 1 
print("離開後a為",a)

```

#### Question: 請問執行後最後的輸出哪一個是對的?(選擇題)  

```python
a = 15 
while a > 0:
	print(a) 
	a -= 2
```
(1) 0  
(2) 1  
(3) -2  


### 使用while迴圈,重複執行程式區塊
- 有時我們需要做一件事超過一次，這時就需要迴圈程式
- python最簡單的迴圈就是while迴圈,範例如下:

```python
#簡單列印1~5
#這樣的使用等同於c語言的的 for(int count=1;count<=5;count+=1)
#使用時機明確的知道要執行多少次迴圈

>>> count = 1
>>> while count <= 5:
		print(count)
		count += 1 
...
1
2
3
4
5
>>>
```

#### Homework:計算2 - 10所有偶數的總和
```python
#loop1.py
#計算2 - 10所有偶數的總和

第 1.0 次迴圈的i = 2 總和為 2
第 2.0 次迴圈的i = 4 總和為 6
第 3.0 次迴圈的i = 6 總和為 12
第 4.0 次迴圈的i = 8 總和為 20
第 5.0 次迴圈的i = 10 總和為 30
```
[解題](loop1.py)



### 使用break跳出迴圈
- 使用無限迴圈+break的語法

```python
#使用時機,不明確知道要執行幾次迴圈
#配合條件式if,並使用break停止迴圈

>>> while True:
		stuff = input("String to capitalize [type q to quit]: ")
			if stuff == "q":
				break
		print(stuff.capitalize())


String to capitalize [type q to quit]: test
Test
String to capitalize [type q to quit]: hey, it works Hey, it works
String to capitalize [type q to quit]: q
>>>
```

```python
#while1_s.py
#小美是一位教師，請你以while迴圈方式為小美設計一個輸入成績的程式，如果輸入負數表示成績輸入結束，在輸#入成績結束後顯示班上總成績及平均成績。

#顯示===============
請輸入第1位學生的成績:89
請輸入第2位學生的成績:78
請輸入第3位學生的成績:68
請輸入第4位學生的成績:89
全班總成績為:XXX分, 平均為XX.XX分
#=========================================


num = 0
sum = 0
while(True):
    num += 1
    score = int(input('請輸入第'+ str(num) + "學生的成績:"))
    if(score < 0):
        break

    sum += score
print("全班總成績為:", sum, "平均分數為:", "%.2f" % (sum/num))

```

#### Homework:計算固定中的支出，媽媽每天會將家裡的花費記錄下來，並且計算本週的花費總和
```python
Name        : loop2.py
計算固定中的支出，媽媽每天會將家裡的花費記錄下來，並且計算本週的花費總和

顯示:
請輸入星期1 的支出567
請輸入星期2 的支出456
請輸入星期3 的支出567
請輸入星期4 的支出890
請輸入星期5 的支出345
請輸入星期6 的支出534
請輸入星期日 的支出678
本星期的支出為:4037元
```

[解題](loop2.py)

### 使用continue,中止迴圈,跳至下一輪迴圈,重頭執行

```python
>>> while True:
		value = input("Integer, please [q to quit]: ") 
			if value == 'q': # quit
				break
		number = int(value)
			if number % 2 == 0: # an even number
				continue
		print(number, "squared is", number*number)
		
		
Integer, please [q to quit]: 1 1 squared is 1
Integer, please [q to quit]: 2 Integer, please [q to quit]: 3 3 squared is 9
Integer, please [q to quit]: 4 Integer, please [q to quit]: 5 5 squared is 25
Integer, please [q to quit]: q 
>>>

```

```python
#continue.py
#請設計一個程式，讓使用者輸入數值，只有加總正偶數值，不加總正奇數值，如果輸入負數，結束程式。

顯示:========================================
請輸入第1個數值:456
請輸入第2個數值:455
請輸入第3個數值:123
請輸入第4個數值:-1
所有輸入的正偶數的加總是:xxxxxxx
=============================================

num = 0
sum = 0
while(True):
    num += 1
    inputNum = int(input("請輸入第"+ str(num) + "個數值:"))
    if(inputNum < 0):
        break
    elif (inputNum % 2 == 1):
        continue
    else:
        sum += inputNum
print("所有輸入的正偶數的加總是:", sum)
```

```python
#============================================================================
# Name        : guess.py
#猜數字遊戲

===============猜數字遊戲=================:

猜數字範圍1~100:50
再小一點
您猜了 1 次

猜數字範圍1~50:25
再大一點
您猜了 2 次

猜數字範圍25~50:34
再大一點
您猜了 3 次

猜數字範圍34~50:46
再小一點
您猜了 4 次

猜數字範圍34~46:40
賓果!猜對了, 答案是: 40
您猜了 5 次
#====================================

import random
min = 1
max = 100
count = 0
target = random.randint(1, 100)
print("===============猜數字遊戲=================:\n")
while(True):
    count += 1
    keyin = int(input("猜數字範圍{0}~{1}:".format(min, max)))
    if(keyin >=min and keyin <= max):
        if(keyin == target):
            print("賓果!猜對了, 答案是:", target)
            print("您猜了",count,"次")
            break
        elif (keyin > target):
            max = keyin
            print("再小一點")
        elif (keyin < target):
            min = keyin
            print("再大一點")
        print("您猜了",count,"次\n")
    else:
        print("請輸入提示範圍內的數字")
```
### while break else語法:
- 在while迴圈內,如果沒有使用到break跳出迴圈,則迴圈結束後要執行else的程式區塊

```python
>>> numbers = [1, 3, 5]
>>> position = 0
>>> while position < len(numbers):
		number = numbers[position] 
		if number%2==0:
			print('Found even number', number)
			break
		position += 1
	else: # break not called
			print('No even number')
			
No even number found
```

### 無限定次數的迴圈
```python
#============================================================================
# Name        : while2.py
#小明想要存錢買一輛機車,機車每輛30000元，他將每月存的錢輸入，當存款足夠買機車時，就顯示提示訊息告知。
#============================================================================

顯示:
請輸入第1個月份的存款:4567
請輸入第2個月份的存款:3456
請輸入第3個月份的存款:4567
請輸入第4個月份的存款:4567
請輸入第5個月份的存款:4567
請輸入第6個月份的存款:5678
請輸入第7個月份的存款:7890
恭喜! 已經存夠了，存了7個月的總存款為:35292元。
#============================================================================

deposit = 0
num = 0
while(deposit < 30000):
    num += 1
    inputNum = int(input('請輸入第'+str(num)+"個月份的存款:"))
    deposit += inputNum

print("恭喜!已經存夠了，存了",num,"個月的總存款為:",deposit,"元。")
```

## 使用for in迴圈
- 使用時機,讀取所有集合物件元素1次。(list,tuple,string,dictionaries,sets)
- 使用時機,明確指定執行次數。

```python
#使用傳統的方式,讀取list內的每一個元素
>>> rabbits = ['Flopsy', 'Mopsy', 'Cottontail', 'Peter'] 
>>> current = 0
>>> while current < len(rabbits):
		print(rabbits[current])
		current += 1 
...
Flopsy
Mopsy
Cottontail
Peter

#使用更簡潔方式(for..in)
>>> for rabbit in rabbits: 
			print(rabbit)
			
Flopsy
Mopsy
Cottontail
Peter

```


### 字串每次取出一個字元

```python
>>> word = 'cat'
>>> for letter in word:
		print(letter) 
			
c
a
t


```

### 使用for in讀取dictionary,取出的元素是key, 也可以使用dictionary.keys()方法.
- 使用values()方法取出元素的值

```python

>>> accusation = {'room': 'ballroom', 'weapon': 'lead pipe', 'person': 'Col. Mustard'}

>>>>>> for card in accusation: # or, for card in accusation.keys():
		print(card)

room
weapon
person

```

```python
>>> accusation = {'room': 'ballroom', 'weapon': 'lead pipe', 'person': 'Col. Mustard'}
#使用values()方法取出元素的值
>>> for value in accusation.values(): 
		print(value)

ballroom
lead pipe 
Col. Mustard

```

```python
>>> accusation = {'room': 'ballroom', 'weapon': 'lead pipe', 'person': 'Col. Mustard'}
#使用items()方法,取出包含key和value的tuple, 
>>> for item in accusation.items(): 
		print(item)

('room', 'ballroom')
('weapon', 'lead pipe') 
('person', 'Col. Mustard')


```

```python
>>> accusation = {'room': 'ballroom', 'weapon': 'lead pipe', 'person': 'Col. Mustard'}

#使用拆解法直接同時取出key和value
>>> for card, contents in accusation.items():
		print('Card', card, 'has the contents', contents) 

			
Card weapon has the contents lead pipe
Card person has the contents Col. Mustard
Card room has the contents ballroom
```

### 使用range()產生數值串列
- 使用range()產一個範圍的數值list
- range()不會像list,tuple,set,dictionary先佔用大量記憶體空間
- 語法:range(start, stop, step).
- 如果省略start,只有stop,start預設為0
- 如同slice,產生的值並不包含stop
- step預設值為1


```python
>>> for x in range(0,3): 
		print(x)

0
1
2
>>> list( range(0, 3) )
[0, 1, 2]

```

#### Homework:小王班上有五位學生，請您為小王設計一個輸入成績的程式，並且在輸入成績後顯示班上總成績及平均成績。
```python
#range1.py
#小王班上有五位學生，請您為小王設計一個輸入成績的程式，並且在輸入成績後顯示班上總成績及平均成績。

顯示:
請輸入第1位學生的成績:89
請輸入第2位學生的成績:89
請輸入第3位學生的成績:89
請輸入第4位學生的成績:89
請輸入第5位學生的成績:89

全班總成績為: ***分，平均為89分
```
[解題](range1.py)

```python

#如果使用-1,則每次-1
>>> for x in range(2, -1, -1):
		print(x)

2
1
0
>>> list( range(2, -1, -1) ) 
[2, 1, 0]

```

```python

#step為2,則每次加2
>>> list( range(0, 11, 2) )
[0,2,4,6,8,10]
```

#### for 迴圈兩個參數:請留意輸出結果
```python
#for2.py

print("兩個參數") 
for i in range(4,8):
	print(i)
print("離開後i為",i)
```

#### Question: 請問執行後跑出哪些整數?(選擇題)
```python
for x in range(6,10): 
	print(x)
```
(1) 6 7 8 9  
(2) 6 7 8 9 10  
(3) 7 8 9  

#### for 迴圈三個參數 (1):請留意輸出結果
```python
#for3-1.py

print("三個參數") 
for i in range(4,0,-1):
	print(i) 
print("離開後i為",i)
```

#### for 迴圈三個參數 (2):請留意輸出結果
```python
#for3-2.py

print("三個參數") 
for i in range(4,8,2):
	print(i) 
print("離開後i為",i)

```

#### Question: 請問執行後跑出哪些整數?(選擇題)
```python
for x in range(0,8,2) :
	print(x)
```
(1) 0 2 4 6 8  
(2) 0 2 4 6  
(3) 0 2 8  

###  迴圈中斷
- break 與 continue 都是迴圈中斷語法
	- break 代表迴圈中斷後跳出迴圈。
	- continue 代表迴圈中斷後繼續執行迴圈。
#### 迴圈中斷:請留意輸出結果
```python
#break.py

i = ['a', 'b', 'c', 'd'] 
for j in i:
	if j == 'c': 
		break
	print(j)
```

#### 迴圈中斷:請留意輸出結果
```python
#continue.py

i = ['a', 'b', 'c', 'd'] 
for j in i:
	if j == 'c': 
		continue
	print(j)
```

### 巢狀迴圈
```python
#========================================================
# Name        : forNest1.py
#利用2層迴圈列印「井」字，將其排列成直角三角形
#=======================================================

顯示:
#
##
###
####
#####



for i in range(1,6):
    for _ in range(i):
        print("#",end='')
    print()
```

```python
#=======================================================================
# Name        : forNest2.py
#利用2層迴圈列印九九乘法表
#=======================================================================
1*1=1   1*2=2   1*3=3   1*4=4   1*5=5   1*6=6   1*7=7   1*8=8   1*9=9
2*1=2   2*2=4   2*3=6   2*4=8   2*5=10  2*6=12  2*7=14  2*8=16  2*9=18
3*1=3   3*2=6   3*3=9   3*4=12  3*5=15  3*6=18  3*7=21  3*8=24  3*9=27
4*1=4   4*2=8   4*3=12  4*4=16  4*5=20  4*6=24  4*7=28  4*8=32  4*9=36
5*1=5   5*2=10  5*3=15  5*4=20  5*5=25  5*6=30  5*7=35  5*8=40  5*9=45
6*1=6   6*2=12  6*3=18  6*4=24  6*5=30  6*6=36  6*7=42  6*8=48  6*9=54
7*1=7   7*2=14  7*3=21  7*4=28  7*5=35  7*6=42  7*7=49  7*8=56  7*9=63
8*1=8   8*2=16  8*3=24  8*4=32  8*5=40  8*6=48  8*7=56  8*8=64  8*9=72
9*1=9   9*2=18  9*3=27  9*4=36  9*5=45  9*6=54  9*7=63  9*8=72  9*9=81


for i in range(1,10):
    for j in range(1,10):
        print(i, " * ", j, " = ", i*j, end='\t')
    print()
```


### for break else語法
檢查如果沒有使用break跳出迴圈,就執行else區塊

```python
#檢查是否cheeses為空list
>>> cheeses = []
>>> for cheese in cheeses:
		print('This shop has some lovely', cheese)
		break
	else: # no break means no cheese
		print('This is not much of a cheese shop, is it?') 
			
This is not much of a cheese shop, is it?
```

### 使用for in zip()同步平行讀取多個串列物件

```python
>>> days = ['Monday', 'Tuesday', 'Wednesday']
>>> fruits = ['banana', 'orange', 'peach']
>>> drinks = ['coffee', 'tea', 'beer']
>>> desserts = ['tiramisu', 'ice cream', 'pie', 'pudding']
>>> for day, fruit, drink, dessert in zip(days, fruits, drinks, desserts): 
			print(day, ": drink", drink, "- eat", fruit, "- enjoy", dessert)
			
Monday : drink coffee - eat banana - enjoy tiramisu 
Tuesday : drink tea - eat orange - enjoy ice cream 
Wednesday : drink beer - eat peach - enjoy pie

```
```python

#使用zip()組合每個串列內元素成為tuple
>>> english = 'Monday', 'Tuesday', 'Wednesday'
>>> french = 'Lundi', 'Mardi', 'Mercredi'
>>> list( zip(english, french) )
[('Monday', 'Lundi'), ('Tuesday', 'Mardi'), ('Wednesday', 'Mercredi')]

>>> dict( zip(english, french) )
{'Monday': 'Lundi', 'Tuesday': 'Mardi', 'Wednesday': 'Mercredi'}


```

#### Homework:
```python
#various_loop1.py

以for迴圈計算1到100的和
顯示=================
1+2+3+~+100的總合是5050
```
[解題](various_loop1.py)

#### Homework:
```python
*問題 various_loop2.py
以while迴圈計算1到100的和

顯示============
1+2+3+~+100的總合是5050
```
[解題](various_loop1.py)

#### Homework:
```python
*問題 nestedLoop1.py
試寫出下列數字排列的程式 
顯示=================================

55555
4444
333
22
1
```
[解題](nestedLoop1.py)

#### Homework:
```python
*問題 inputLoop.py
設計一個程式，使用者輸入一個M, 再輸入另一個數N,然後程式可以求出M*1 + M*2 + M*3 + M*4 + M*5....... + M*N的值

顯示==========================
輸入M:5
輸入N:4
M*1 + M*2 + M*3 + ......+ M*N = 50
```
[解題](inputLoop.py)

#### Homework:
```python
*問題 commonfactor.py
設計一個程式，可以由鍵盤輸入兩個數值，並求出這2個數值的最大公因數和最小公倍數

顯示======================================
求兩數的最大公因數和最小公倍數
請輸入第一個整數:XXX
請輸入第二個整數:XXX

計算結果:
14 和 35 的最大公因數:7
14 和 35 的最小倍數是:70
```
[解題](commonfactor.py)

##  符號與多行字串
- 一行字串可以用雙引號或者單引號包起來。
- 單引號或雙引號取決於字串的內容是否有相同的符號，若有則使用另
外一個符號作業。
- 如果字串內容有用到單雙引號，但外圍仍用相同符號，請加上跳脫字 元進行轉換。
- 多行字串使用”””三個雙引號或者’’’三個單引號方式包起來。

###  跳脫字元
```python
- 反斜線作為跳脫字元，可用於引用特殊字元。
	- \\ 反斜線
	- \’ 單引號
	- \” 雙引號
	- \n 換行
	- \t 固定間隔
```

```python
>>> 'Snap'
    'Snap'
>>> "Crackle"
    'Crackle'


>>> "'Nay,' said the naysayer."
"'Nay,' said the naysayer."

>>> 'The rare double quote in captivity: ".'
'The rare double quote in captivity: ".'

>>> 'A "two by four" is actually 1 1⁄2" × 3 1⁄2".'
'A "two by four is" actually 1 1⁄2" × 3 1⁄2".'

>>> "'There's the man that shot my paw!' cried the limping hound." 
"'There's the man that shot my paw!' cried the limping hound."

```

#### 單雙引號與跳脫字元:請留意輸出結果
```python
#string0.py

str = 'This is "Python" !' print(str)
str = "This is \"Python\" !" print(str)
str = "test1 \n test2\\test3" print(str)
``` 

```python
#string1.py

str3= """
多行 
字串
"""
str4= '''
多行 
字串
'''
print("字串1:", str3) 
print("字串2:", str4)
```

```python
#多行文字
>>> '''Boom!'''
    'Boom'
>>> """Eek!"""
    'Eek!'
    
>>> poem = '''There was a Young Lady of Norway, ... Who casually sat in a doorway;
... When the door squeezed her flat,
... She exclaimed, "What of that?"
... This courageous Young Lady of Norway.'''



>>> poem2 = '''I do not like thee, Doctor Fell.
... The reason why, I cannot tell.
... But this I know, and know full well:
... I do not like thee, Doctor Fell.
... '''
>>> print(poem2)
I do not like thee, Doctor Fell.
	The reason why, I cannot tell.
	But this I know, and know full well: 
	I do not like thee, Doctor Fell.
>>>
```

```python
>>> print(99, 'bottles', 'would be enough.') 
    99 bottles would be enough.
    
    

>>> ''
    ''
>>> ""
    ''
>>> ''''''
    ''
>>> """"""
    ''
>>>




>>> bottles = 99
>>> base = ''
>>> base += 'current inventory: '
>>> base += str(bottles)
>>> base
    'current inventory: 99'


```

```python
#使用str()轉換為字串型別
>>> str(98.6) 
    '98.6'
>>> str(1.0e4) 
    '10000.0'
>>> str(True)
    'True'

```

```python
#脫溢字元 \
>>> palindrome = 'A man,\nA plan,\nA canal:\nPanama.' 
>>> print(palindrome)
A man,
A plan,
A canal: Panama.



>>> print('\tabc') 
    abc
>>> print('a\tbc') 
    a bc
>>> print('ab\tc') 
    ab c
>>> print('abc\t') 
    abc



>>> testimony = "\"I did nothing!\" he said. \"Not that either! Or the other thing.\""
>>> print(testimony)
"I did nothing!" he said. "Not that either! Or the other thing."
>>> fact = "The world's largest rubber duck was 54'2\" by 65'7\" by 105'" 
>>> print(fact)
The world's largest rubber duck was 54'2" by 65'7" by 105'



>>> speech = 'Today we honor our friend, the backslash: \\.' 
>>> print(speech)
Today we honor our friend, the backslash: \.


```

```python
#使用+運算子
>>> 'Release the kraken! ' + 'At once!'
    'Release the kraken! At once!'




>>> a = 'Duck.' 
    b=a
>>> c = 'Grey Duck!' 
>>>a+b+c 
   'Duck.Duck.Grey Duck!'



>>> print(a, b, c) 
    Duck. Duck. Grey Duck!
    

```

```python
#len()
>>> len(letters)
    26
>>> empty = ""
>>> len(empty)
    0

```

###  索引編號與取值
- 字元依照順序排序:
	- 第一個字索引編號為 0，第二個字索引編號為 1
	- 最後一個字索引編號為 -1，倒數第二個字索引編號為 -2。

###  索引編號與取值
- [n]
	- [ ]內可加入一個整數 n。
	- 代表由字串中取出固定索引欄位 n 的字元。
	- 由左向右存取，編號由 0 開始遞增。
	- 由右向左存取，編號由 -1 開始遞減。
```python
>>> letters = 'abcdefghijklmnopqrstuvwxyz'
>>> letters[0]
    'a'
>>> letters[1]
'b'
>>> letters[-1]
    'z'
>>> letters[-2] 
    'y'
>>> letters[25]
    'z'
>>> letters[5]
    'f'
    
    

>>> letters[100]
Traceback (most recent call last):
File "<stdin>", line 1, in <module> IndexError: string index out of range




>>> name = 'Henny'
>>> name[0] = 'P'
Traceback (most recent call last): File "<stdin>", line 1, in <module>
TypeError: 'str' object does not support item assignment

```

###  索引編號與取值
- [n : m]
	- 在一個範圍內找資料
	- n 與 m 均是一個整數
	- n 代表起始位置，第一個為 0。
	- m 是結束位置，不可以超過這個位置。

### 索引編號與取值:請留意輸出結果
```python
#string3.py
 mystring1="Hello World"
 print(mystring1[0]) 
 print(mystring1[2]) 
 print(mystring1[-1]) 
 print(mystring1[-2]) 
 print(mystring1[2:]) 
 print(mystring1[:3]) 
 print(mystring1[1:4]) 
```

| H | e | l | l | o |  | W | o | r | l | d |
|:--|:--|:--|:--|:--|:--|:--|:--|:--|:--|:--|
| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7| 8 | 9 | 10 |
| -11 | -10 | -9 | -8 | -7 | -6 | -5 | -4 | -3 | -2 | -1 |

```python

#[ start : end : step ]

>>> letters = 'abcdefghijklmnopqrstuvwxyz'
>>> letters[:]
    'abcdefghijklmnopqrstuvwxyz'

>>> letters[20:]
    'uvwxyz'

>>> letters[10:]
    'klmnopqrstuvwxyz'

>>> letters[12:15]
    'mno'

>>> letters[-3:] 
    'xyz'
    
>>> letters[18:-3] 
    'stuvw'
    
>>> letters[-6:-2] 
    'uvwx'
    
>>> letters[::7]
    'ahov'


>>> letters[4:20:3]
    'ehknqt'


>>> letters[19::4]
    'tx'


>>> letters[:21:5]
    'afkpu'


>>> letters[-1::-1] 
    'zyxwvutsrqponmlkjihgfedcba'


>>> letters[::-1] 
    'zyxwvutsrqponmlkjihgfedcba'
```

###  字串取代

- replace 可以將指定的字串進行更換:
	- str.replace(舊字串, 新字串)
- replace 可以指定您要第幾個位置*後*不進行更換:
	- str.replace(舊字串, 新字串,第幾個位置)
	- 位置編號由 0 開始

#### 字串取代:請留意輸出結果
```python
#string4.py
str="This is Python,That is Java;This is SQLite,That is MySQL" 
print("原本的字串:",str)
print( )
print("is 替換為-:"+str.replace("is","-"))
print( )

str="This is Python,That is Java;This is SQLite,That is MySQL"
print("原本的字串:",str)
print( )
print("加上參數值2:"+str.replace("is","-",2))
print( ) 
```

```python
>>> name = 'Henny'
>>> name.replace('H', 'P') 
   'Penny'
>>> 'P' + name[1:] 
    'Penny'
```

###  字串內容搜尋
- 字串可以搜尋特定內容的位置。
- 搜尋的字串位置編號由 0 開始。
- 字串.find(搜尋字串,起始位置,結束位置)
- 搜尋時不包含結束位置。
- 若搜尋不到則回傳 -1。
- 若沒有起始位置，也沒有結束位置，預設由 0 開始。
- 若沒有結束位置，預設到最後一個字。

#### 字串內容搜尋:請留意輸出結果
```python
#string5.py

str1 = "this is Python Tutorial, there"
search1 = "Python" 
print(str1.find(search1))
search2= "not" 
print(str1.find(search2))
search3="t" 
print(str1.find(search3)) 
print(str1.find(search3,4)) print(str1.find(search3,11,20))
```

####  字串插入與切割
- join( ) : 於字串或著字元之間加入指定的文字
	- 指定文字.join(串列)
- split( ) : 將字串進行切割
	- str.split(分割符號)
	- str.split(分割符號,分割次數)

```python
#string6.py

str1 = "-"
str2 = ("a", "b", "c") 
print(str1.join(str2))
str2 = ("abc", “xyz", “123") 
print(str1.join(str2)) 
str3=":".join("Python") 
print(str3)
str4 = "python-java-c++-ruby" 
print(str4.split('-')) 
print(str4.split('-',1))
```

```python
#split()
>>> todos = 'get gloves,get mask,give cat vitamins,call ambulance' 
>>> todos.split(',')
['get gloves', 'get mask', 'give cat vitamins', 'call ambulance']

```

```python
#join()
>>> crypto_list = ['Yeti', 'Bigfoot', 'Loch Ness Monster'] 
>>> crypto_string = ', '.join(crypto_list)
>>> print('Found and signing book deals:', crypto_string) Found and signing book deals: Yeti, Bigfoot, Loch Ness Monster

```

```python
>>> poem = '''All that doth flow we cannot liquid name Or else would fire and water be the same;
But that is liquid which is moist and wet
Fire that property can never get.
Then 'tis not cold that doth the fire put out But 'tis the wet that makes it die, no doubt.'''


>>> poem[:13]
    'All that doth'
    
>>> len(poem)
    250

>>> poem.startswith('All')
True


>>> poem.endswith('That\'s all, folks!')
False


>>> word = 'the' 
>>> poem.find(word) 
    73


>>> poem.rfind(word)
    214
    

>>> poem.count(word)
    3



>>> setup = 'a duck goes into a bar...'

>>> setup.strip('.')
'a duck goes into a bar'

>>> setup.capitalize()
'A duck goes into a bar...'

>>> setup.title()
'A Duck Goes Into A Bar...'

>>> setup.upper()
'A DUCK GOES INTO A BAR...'

>>> setup.lower()
'a duck goes into a bar...'

>>> setup.swapcase()
'a DUCK GOES INTO A BAR...'

>>> setup.center(30)
    '  a duck goes into   '

>>> setup.ljust(30) 
>>> 'a duck goes into a bar... '

>>> setup.rjust(30)
' a duck goes into a bar...'

#replace()
>>> setup.replace('duck', 'marmoset') 
   'a marmoset goes into a bar...'

```


### Homewrok:字串文字接龍
```python
#wordLink.pyworwor

失敗就會退出遊戲
請輸入一個字串:Python
上一個字串是Python
請輸入-n-開始的字串:new
上一個字串是Python-new
請輸入-w-開始的字串:well
上一個字串是Python-new-well
請輸入-l-開始的字串: long time
上一個次串是Python-new-well-long time
請輸入-e-開始的字串
```
[解題](./wordLink.py)



