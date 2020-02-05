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

>>> for card in accusation: # or, for card in accusation.keys():
		print(card)

room
weapon
person

=====================================

#使用values()方法取出元素的值
>>> for value in accusation.values(): 
		print(value)

ballroom
lead pipe 
Col. Mustard

======================================

#使用items()方法,取出包含key和value的tuple, 
>>> for item in accusation.items(): 
		print(item)

('room', 'ballroom')
('weapon', 'lead pipe') 
('person', 'Col. Mustard')


=======================================

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

=================================================

#如果使用-1,則每次-1
>>> for x in range(2, -1, -1):
		print(x)

2
1
0
>>> list( range(2, -1, -1) ) 
[2, 1, 0]

====================================================

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

=============================================

#使用zip()組合每個串列內元素成為tuple
>>> english = 'Monday', 'Tuesday', 'Wednesday'
>>> french = 'Lundi', 'Mardi', 'Mercredi'
>>> list( zip(english, french) )
[('Monday', 'Lundi'), ('Tuesday', 'Mardi'), ('Wednesday', 'Mercredi')]

>>> dict( zip(english, french) )
{'Monday': 'Lundi', 'Tuesday': 'Mardi', 'Wednesday': 'Mercredi'}


```




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



#使用str()轉換為字串型別
>>> str(98.6) 
    '98.6'
>>> str(1.0e4) 
    '10000.0'
>>> str(True)
    'True'




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


>>> name = 'Henny'
>>> name.replace('H', 'P') 
   'Penny'
>>> 'P' + name[1:] 
    'Penny'



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



#len()
>>> len(letters)
    26
>>> empty = ""
>>> len(empty)
    0
    
    
#split()
>>> todos = 'get gloves,get mask,give cat vitamins,call ambulance' 
>>> todos.split(',')
['get gloves', 'get mask', 'give cat vitamins', 'call ambulance']


#join()
>>> crypto_list = ['Yeti', 'Bigfoot', 'Loch Ness Monster'] 
>>> crypto_string = ', '.join(crypto_list)
>>> print('Found and signing book deals:', crypto_string) Found and signing book deals: Yeti, Bigfoot, Loch Ness Monster




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

