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



