
# python內建的資料結構
## Lists, Tuples, Dictionaries, and Sets
### tuple 與 list 的差異
- 括號不同:
	- tuple 是用小括號將元素包起來。
	- list 是用中括號將元素包起來。

- 元素可否變更:
	- tuple 決定了元素的內容就不可以變更。
	- list 可以隨時修改。

### list 介紹
- list 內資料用逗號隔開，放置於中括號的範圍內。 
	- list_name = [1,2,3 ]
- list 可以儲存不同類型的值或項目，如數字和字串。
	- list_name = [1, 2, ‘Python’, ‘lists’ ]
- list 內的資料可以進行增加、更新與移除。
- 可透過.index( )方法取得指定資料的索引。
### Create with [] or list()
```python
>>> empty_list = [ ]
>>> weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'] 
>>> big_birds = ['emu', 'ostrich', 'cassowary']
>>> first_names = ['Graham', 'John', 'Terry', 'Terry', 'Michael']


>>> another_empty_list = list() 
>>> another_empty_list
[]


#使用list()轉換其它型態為list
>>> list('cat')
    ['c', 'a', 't']


>>> a_tuple = ('ready', 'fire', 'aim') 
>>> list(a_tuple)
['ready', 'fire', 'aim']


>>> birthday = '1/6/1952' 
>>> birthday.split('/') 
['1', '6', '1952']


>>> splitme = 'a/b//c/d///e'
>>> splitme.split('/')
['a', 'b', '', 'c', 'd', '', '', 'e']


>>> splitme = 'a/b//c/d///e' 
>>> splitme.split('//')
['a/b', 'c/d', '/e']


>>> marxes = ['Groucho', 'Chico', 'Harpo']
>>> marxes[0]
    'Groucho'
>>> marxes[1]
	'Chico'
>>> marxes[2]
	'Harpo'

>>> marxes[-1] 
'Harpo'
>>> marxes[-2] 
'Chico'
>>> marxes[-3] 
'Groucho'


>>> marxes = ['Groucho', 'Chico', 'Harpo'] 
>>> marxes[5]
Traceback (most recent call last):
File "<stdin>", line 1, in <module> IndexError: list index out of range
>>> marxes[-5]
Traceback (most recent call last):
File "<stdin>", line 1, in <module> IndexError: list index out of range

```

### list 與 tuple:請留意輸出結果\

```python
#list0.py

 list1=['H','i'] 
 tuple1=('H','i') 
 
 print(tuple1) 
 print(list1) 
 
 tuple1[1]='a' 
 list1[1]='a' 
 
 print(tuple1) 
 print(list1)
```

###  索引標籤
- 索引編號放在 [ ] 內。
- 由左向右 ( 由前向後 ) 存取，編號由 0 開始遞增。
- 由右向左 ( 由後向前 ) 存取，編號由 -1 開始遞減。

| 0 | 1 | 2 | 3 | 4 | 5 |
|:--|:--|:--|:--|:--|:--|
| -6 | -5 | -4 | -3 | -2 | -1 |

#### Question: 請問執行後的結果哪一個是對的?(選擇題)
```python
tuple1=('1','2') 
tuple1[1]='0' 
print(tuple1)
```
(1) 02   
(2) 10   
(3) 120   
(4)錯誤  

---

####  請問執行後的結果哪一個是對的?(選擇題)
```python
list1=['1','2'] 
list1[1]='0' 
print(list1)
```
(1) 02   
(2) 10   
(3) 120   
(4) 錯誤  

---

#### 操作範例:請動手操作，並留意輸出結果

```python
#list1.py

list1=['H','e','l','l','o', 'W','o','r','l','d'] print(list1[0])
print(list1[1])
print(list1[-1])
print(list1[-3])
```

####  請問執行後的結果哪一個是對的?(選擇題)

```python
list1=['p','y','t','h','o','n']
print(list1[-2])
```
(1) y   
(2) n   
(3) o   
(4) p  

---
### 2維List
```python
>>> small_birds = ['hummingbird', 'finch']
>>> extinct_birds = ['dodo', 'passenger pigeon', 'Norwegian Blue'] 
>>> carol_birds = [3, 'French hens', 2, 'turtledoves']
>>> all_birds = [small_birds, extinct_birds, 'macaw', carol_birds]


>>> all_birds
	[['hummingbird', 'finch'], ['dodo', 'passenger pigeon', 'Norwegian Blue'], 'macaw', [3, 'French hens', 2, 'turtledoves']]


>>> all_birds[0]
   ['hummingbird', 'finch']


>>> all_birds[1]
['dodo', 'passenger pigeon', 'Norwegian Blue']


>>> all_birds[1][0] 
'dodo'


>>> marxes = ['Groucho', 'Chico', 'Harpo']
>>> marxes[2] = 'Wanda'
>>> marxes
['Groucho', 'Chico', 'Wanda']
```
###  部分取值
- list內部分取值採用[ n:m ]方式，n與m是整數。
	- n 代表起始位置，第一個為 0。
	- m 代表結束位置，不可以超過這個位置。

| 0 | 1 | 2 | 3 | 4 | 5 |
|:--|:--|:--|:--|:--|:--|
| -6 | -5 | -4 | -3 | -2 | -1 |

#### 操作範例:請動手操作，並留意輸出結果
```python
#list2.py

list1=['H','e','l','l','o', 'W','o','r','l','d'] print(list1[2:])
print(list1[:3])
print(list1[3:5])
```

#### 操作範例:請動手操作，並留意輸出結果
```python
#list2.py

list1=['H','e','l','l','o', 'W','o','r','l','d'] print(list1[2:])
print(list1[:3])
print(list1[3:5])
```
| H | e | l | l | o | W | o | r | l | d |
|:--|:--|:--|:--|:--|:--|:--|:--|:--|:--|
| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| -10 | -9 | -8 | -7 | -6 | -5 | -4 | -3 | -2 | -1 |

####  請選出以下程式碼跑出的結果。
```python
list1=['H','e','l','l','o', 'W','o','r','l','d']
print(list1[0])
```
(1)'H'  
(2)'W'  
(3)'l'  
(4)'d'  

---

####  請選出以下程式碼跑出的結果。
```python
list1=['H','e','l','l','o', 'W','o','r','l','d']
print(list1[-1])
```
(1)'H'  
(2)'W'  
(3)'l'  
(4)'d'  

---

```python
>>> marxes = ['Groucho', 'Chico,' 'Harpo']
>>> marxes[0:2]
['Groucho', 'Chico']


>>> marxes[::2]
['Groucho', 'Harpo']


>>> marxes[::-2] 
['Harpo', 'Groucho']


>>> marxes[::-1]
['Harpo', 'Chico', 'Groucho']


```

###  更新資料
- 指定 list 的索引編號就可以給予新的資料，將這個項目內容更新。
	- List1[2]=123

####  請問最後輸出結果會是什麼?(選擇題)
```python
list1=['a','b','c'] 
print(list1) 
list1[2]='dd' 
print(list1)
```
(1) ['a','dd','b','c']   
(2) ['a','b','dd','c']   
(3) ['a','b','dd']  
(4) ['a','dd','c']  

####  請依照下列問題找出正確的答案。(選擇題)
```python
你有一個list x:
x = ["a", "b", "b"]
請改變第2個"b"成為"c"
```

(1) x[2] = "c"  
(2) x[2] = c  
(3) x[3] = "c"  
(4) x[3] = c  

---

###  list 項目附加資料
- append 附加資料:
	-  你提供的資料就以一筆資料方式加入到 list。
	-  一次只能加入一個資料。
- 也可利用 + 的方式於原本的 list 之後附加新的資料。

```python
#list5.py

 list1= ['a', 'b', 'c'] 
 print("附加之前:", list1) 
 print("附加之前長度 = ", len(list1)) list1.append(["def","ghij"]) 
 print("附加之後:", list1) 
 print("附加之後長度 = ", len(list1)) print(list1[3])
```

###  list 項目擴展資料
- extend 擴展資料
	- 如果引號括起來的字串有 [ ] 將會拆解成好幾個資料。
	- 可以把其他 list 加入到這個 list 內，擴展多個欄位。

#### 操作範例:請動手操作，並留意輸出結果

```python
#list6.py

list1= ['a', 'b', 'c']
print("擴展之前:", list1) 
print("擴展之前長度 = ", len(list1))
print("擴展之後:", list1) 
print("擴展之後長度 = ", len(list1)) 
print(list1[3])
```

```python
>>> marxes.append('Zeppo')
>>> marxes
['Groucho', 'Chico', 'Harpo', 'Zeppo']


>>> marxes = ['Groucho', 'Chico', 'Harpo', 'Zeppo'] 
>>> others = ['Gummo', 'Karl']
>>> marxes.extend(others)
>>> marxes
['Groucho', 'Chico', 'Harpo', 'Zeppo', 'Gummo', 'Karl']


>>> marxes = ['Groucho', 'Chico', 'Harpo', 'Zeppo']
>>> others = ['Gummo', 'Karl']
>>> marxes += others
>>> marxes
['Groucho', 'Chico', 'Harpo', 'Zeppo', 'Gummo', 'Karl']


>>> marxes = ['Groucho', 'Chico', 'Harpo', 'Zeppo'] 
>>> others = ['Gummo', 'Karl']
>>> marxes.append(others)
>>> marxes
['Groucho', 'Chico', 'Harpo', 'Zeppo', ['Gummo', 'Karl']]

```

### list 項目插入新資料
- list 可使用 insert 方式插入新的資料:
	- list.insert(索引值，插入的資料)。
	- list.insert(索引值，插入的資料)。
	- 
#### 操作範例:請動手操作，並留意輸出結果
```python
#list7.py

 list1 = ['this', 'is', 'list'] 
 print(list1) 
 list1.insert(1, 'item') 
 print(list1) 
 list1.insert(88, '88') 
 print(list1)
```

#### Question:請問以下的結果會是什麼?(選擇題)
```python
 list1 = ['a', 'b', 'c'] 
 list1.insert(1, 'x') 
 print(list1)
```
(1) ['x','a','b','c']   
  
(2) ['a','x','b','c'] 
    
(3) ['a','b','x','c'] 
   
(4) ['a','b','c','x']   

 ---
 
 ```python
 >>> marxes.insert(3, 'Gummo') 
>>> marxes
['Groucho', 'Chico', 'Harpo', 'Gummo', 'Zeppo']


>>> marxes.insert(10, 'Karl')
>>> marxes
['Groucho', 'Chico', 'Harpo', 'Gummo', 'Zeppo', 'Karl']

 ```
 
###  list 移除項目
- list 可透過以下三種方式移除項目:
	- list.remove( )
	- list.pop( )
	- del list[ ]

###  list.remove
- list 可透過 remove 方式移除資料
	- 依據內容進行刪除
	- list.remove(項目內容)

####  Question:請問以下的結果會是什麼?(選擇題)
```python
#1. 有兩個以上的相同資料， 會先移除哪一個呢?
#2. 如果沒有資料那會如何呢?

list1 = ['1', 'x', '2', 'x', '3'] 
list1.remove('x') 
print(list1)
```
(1) ['x','1', '2', '3'] 

(2) ['1', '2', '3'] 

(3) ['1', '2', 'x', '3']

(4) ['1','x', '2', '3']

---
###  list.pop
- list 可透過 pop 方式移除指定位置資料。
	- 如果 pop( ) 內沒有參數，則移除最後一筆資料。
	- pop( ) 內若有參數，則移除指定位置的資料。

####  Question:請問以下的結果會是什麼?(選擇題)
```python
list1 = ['1', 'x', '2', 'x', '3']
list1.pop( ) 
print(list1)
```
(1) ['x','2','x','3']
   
(2) ['1','x','2','x'] 
  
(3) ['x','2','x']

(4) ['1','2','x','3']

---

#### Question:請問以下的結果會是什麼?(選擇題)
```python

list1 = ['1', 'x', '2', 'x', '3']
list1.pop(1) 
print(list1)
```

(1) ['x','2','x','3']  

(2) ['1','x','2','x'] 

(3) ['x','2','x']

(4) ['1','2','x','3']

---

###  del list[ ]
- list 可透過 del 方式移除指定位置資料。
- del list[ ] 必須指定範圍:
	- del list[n] 代表移除第 n 位索引值資料。
	- del list[:n] 代表移除第 n 位索引值之前 ( 不包含 n ) 資料。
	- del list[m:n] 代表移除第 m 到 n 位索引值之前 ( 不包含 n ) 資料。

####  Question:請問以下的結果會是什麼?(選擇題)
```python
list1 = ['1', 'x', '2', 'x', '3']
del list1[:1] 
print(list1)
```
(1) ['x','2','x','3'] 

(2) ['1','2','x','3'] 

(3) ['1','x','2','x']

(4) ['2','x','3']

---

####  請問以下的結果會是什麼?(選擇題)
```python
list1 = ['1', 'x', '2', 'x', '3']
del list1[2:4] 
print(list1)
```
(1) ['2','x','3'] 

(2) ['1','x','3'] 

(3) ['x','2','x']  

(4) ['1','x']

---

```python
>>> del marxes[-1]
>>> marxes
['Groucho', 'Chico', 'Harpo', 'Gummo', 'Zeppo']


>>> marxes = ['Groucho', 'Chico', 'Harpo', 'Gummo', 'Zeppo'] 
>>> marxes[2]
'Harpo'
>>> del marxes[2]
>>> marxes
['Groucho', 'Chico', 'Gummo', 'Zeppo']
>>> marxes[2]
'Gummo'


>>> marxes = ['Groucho', 'Chico', 'Harpo', 'Gummo', 'Zeppo'] 
>>> marxes.remove('Gummo')
>>> marxes
['Groucho', 'Chico', 'Harpo', 'Zeppo']


>>> marxes = ['Groucho', 'Chico', 'Harpo', 'Zeppo'] 
>>> marxes.pop()
'Zeppo'
>>> marxes
['Groucho', 'Chico', 'Harpo'] 
>>> marxes.pop(1)
'Chico'
>>> marxes
['Groucho', 'Harpo']
```

### list index(), in, count()
```python
>>> marxes = ['Groucho', 'Chico', 'Harpo', 'Zeppo'] 
>>> marxes.index('Chico')
1


>>> marxes = ['Groucho', 'Chico', 'Harpo', 'Zeppo'] 
>>> 'Groucho' in marxes
True
>>> 'Bob' in marxes
False


>>> words = ['a', 'deer', 'a' 'female', 'deer'] 
>>> 'deer' in words
True


>>> marxes = ['Groucho', 'Chico', 'Harpo'] 
>>> marxes.count('Harpo')
1
>>> marxes.count('Bob')
0
>>> snl_skit = ['cheeseburger', 'cheeseburger', 'cheeseburger'] 
>>> snl_skit.count('cheeseburger')
3

```

### join(),split()
```python
>>> marxes = ['Groucho', 'Chico', 'Harpo'] 
>>> sorted_marxes = sorted(marxes)
>>> sorted_marxes
['Chico', 'Groucho', 'Harpo']


>>> marxes
['Groucho', 'Chico', 'Harpo']
>>> marxes.sort()
>>> marxes
['Chico', 'Groucho', 'Harpo']
```

###  list 排序
- list 進行排序有 sorted( ) 與 sort( ) 兩個動作。
- 兩者差異:
	- sorted( )
		- 不會影響 list 本身結構，且可以輸出結果。
		- sorted(list項目)。
		- sorted( ) 可用來排序任何項目。
	- sort( )
		-  會影響 list 本身結構，且不可以於操作這個動作時進行輸出。
		-  list.sort( )
		-  sort( ) 只能用在list上排序。

###  排序原則與參數
- 排序原則:
	- 數字則依照大小排序。
	- 字串則依照 ASCII 編碼順序進行排序。

###  排序原則與參數
- 可加入的參數:
	- reverse=True
		- 有這個參數由大到小排序
		- 若沒有這個參數則由小到大排序
	- key=len
		- 依照 list 內元素字串長度進行排序
	- key=str.upper
		- 將 list 內元素轉換為大寫，再依照 ASCII 編碼順序進行排序
	- key=str.lower
		- 將 list 內元素轉換為小寫，再依照 ASCII 編碼順序進行排序

#### 排序的原理:ASCII
```python
list2 = ['c','b','a','A']
list2.sort()
print(list2)
print(ord('a'),ord('b'),ord('c'),ord('A'))


['A', 'a', 'b', 'c'] 
97 98 99 65
```

#### 操作範例:請動手操作，並留意輸出結果
```python
#list8.py

a = [5, 2, 1, 9, 6] 
print(sorted(a))
print(a)
print(sorted(a, reverse=True) ) 
print(a)
a.sort(reverse=True) 
print(a)

```

```python
>>> numbers = [2, 1, 4.0, 3] 
>>> numbers.sort()
>>> numbers
[1, 2, 3, 4.0]


>>> numbers = [2, 1, 4.0, 3] 
>>> numbers.sort(reverse=True) 
>>> numbers
[4.0, 3, 2, 1]


>>> marxes = ['Groucho', 'Chico', 'Harpo']
>>> len(marxes)
3
```

### copy()
```
>>>a=[1,2,3] 
>>> a
[1, 2, 3] 
>>>b=a


>>> b
[1, 2, 3]
>>> a[0] = 'surprise'
>>> a
['surprise', 2, 3]
>>> b
['surprise', 2, 3]


>>> b
['surprise', 2, 3]
>>> b[0] = 'I hate surprises'
>>> b
['I hate surprises', 2, 3]
>>> a
['I hate surprises', 2, 3]


>>>a=[1,2,3] 
>>> b = a.copy() 
>>> c = list(a) 
>>>d=a[:]


>>> a[0] = 'integer lists are boring'
>>> a
['integer lists are boring', 2, 3]
>>> b
[1, 2, 3]
>>> c
[1, 2, 3]
>>> d
[1, 2, 3]
```

###  資料反向
- 可利用 reverse( ) 函數進行反向排序動作。
- 這函數沒有傳回值，list 執行後就會進行反向排序。

#### Question: 請問以下的結果會是什麼?(選擇題)

```python
list2 = [12, 'ab', 'Ab', 'aB'] 
list2.reverse()
print (list2)
```
(1) ['aB', 'Ab', 'ab', 12] 

(2) ['Ab', 'aB', 'ab', 12] 

(3) ['ab', 'aB', 'Ab', 12] 

(4) [12,'ab', 'aB', 'Ab']

####  回家作業:清單中找水果
```python
請輸入喜歡的水果(enter 結束):木瓜
木瓜 不在list清單中!
請輸入喜歡的水果(enter 結束):西瓜
西瓜 在list清單中的第5項!
請輸入喜歡的水果(enter 結束):
```

## Tuples

```python
>>> empty_tuple = () 
>>> empty_tuple
()


>>> one_marx = 'Groucho', 
>>> one_marx ('Groucho',)


>>> marx_tuple = 'Groucho', 'Chico', 'Harpo' 
>>> marx_tuple
('Groucho', 'Chico', 'Harpo')


>>> marx_tuple = ('Groucho', 'Chico', 'Harpo') 
>>> marx_tuple
('Groucho', 'Chico', 'Harpo')


>>> marx_tuple = ('Groucho', 'Chico', 'Harpo') 
>>> a, b, c = marx_tuple
>>> a
'Groucho'
>>> b
'Chico'
>>> c
'Harpo'


>>> password = 'swordfish'
>>> icecream = 'tuttifrutti'
>>> password, icecream = icecream, password
>>> password
'tuttifrutti'
>>> icecream
'swordfish'


>>> marx_list = ['Groucho', 'Chico', 'Harpo'] 
>>> tuple(marx_list)
('Groucho', 'Chico', 'Harpo')
```


## Dictionaries 介紹
- 可以想像你現在手上有一本電子英漢字典，當你輸入英文單字的時候，
就可以查得到它的唯一翻譯。

- 你所關心的英文單字與翻譯之間有著 一對一 的關係:
	- 你輸入的英文單字，就叫做 Key 
	- 而得到的翻譯，就叫做 Value 
- 一個 Dictionary 是一群 Key : Value 配對的集合
- 資料結構是由 key:value 所組成。
- key 不能夠重複，否則會被後面的結果蓋過去。
- 可輸入 key 找尋您要找出來的值。
- 如果輸入的 key 不存在，那就會出現錯誤訊息。

#### 操作範例:請動手操作，並留意輸出結果
```python
# dict1.py
dict1={'a':100,'b':200,'c':300} 
print(dict1) 
dict1={'a':200,'b':400,'b':300} 
print(dict1)
print(dict1['a']) 
print(dict1['b']) 
print(dict1['d']) #不存在
```

#### Question: 請問執行後的結果哪一行是錯的?(選擇題)
```python
dict1={'a':100,'b':200, 'b':300} 
print(dict1)
print(dict1['a']) 
print(dict1['d'])
```
(1) print(dict1)   
(2) print(dict1['a'])  
(3) print(dict1['d'])  
(4) 沒有錯誤. 

####  請問執行後的結果是哪一個答案呢?(選擇題)
```python
dict1={'a':100,'b':200,'b':300}
print(dict1['b'])
```
(1) 100  
(2) 200   
(3) 300  
(4) 0  

### 建立Dictionary

```python
>>> empty_dict = {} 
>>> empty_dict
{}


>>> bierce = {
... "day": "A period of twenty-four hours, mostly misspent",
... "positive": "Mistaken at the top of one's voice",
... "misfortune": "The kind of fortune that never misses",
... } 
>>>


>>> bierce
{'misfortune': 'The kind of fortune that never misses', 'positive': "Mistaken at the top of one's voice", 'day': 'A period of twenty-four hours, mostly misspent'}


>>> lol = [ ['a', 'b'], ['c', 'd'], ['e', 'f'] ]
>>> dict(lol)
{'c': 'd', 'a': 'b', 'e': 'f'}


>>> lot = [ ('a', 'b'), ('c', 'd'), ('e', 'f') ]
>>> dict(lot)
{'c': 'd', 'a': 'b', 'e': 'f'}


>>> tol = ( ['a', 'b'], ['c', 'd'], ['e', 'f'] )
>>> dict(tol)
{'c': 'd', 'a': 'b', 'e': 'f'}


>>> los = [ 'ab', 'cd', 'ef' ]
>>> dict(los)
{'c': 'd', 'a': 'b', 'e': 'f'}


>>> tos = ( 'ab', 'cd', 'ef' )
>>> dict(tos)
{'c': 'd', 'a': 'b', 'e': 'f'}
``` 

###  key 與 value
- key 不能於程式內改變:
	- 可以用數字、字串或者 tuple
	- 不可以使用 list

- 如何找出所有的 key 與 value?
	- 您可以透過 dict1.keys( ) 這個方法找出所有的 key
	- 您可以透過 dict1. values( ) 這個方法找出所有的 value

###  新增與修改
- 新增一筆資料
	- 請將 key 與 value 儲存至一個變數內
	- 透過 dict.update(新增的資料) 這個方法的方式就可以新增

- 元素可否變更:
	- 以 = 指派方式指派給 key 就可以變更資料

#### 操作範例 1:請動手操作，並留意輸出結果
```python
#dict3.py

dict1={'a':100,'b':200, 'c':300} 
print(dict1)
add_dic={'d':400} 
dict1.update(add_dic) 
print(dict1)
```

```python
#dict4.py

dict1={'a':100,'b':200, 'c':300} 
print(dict1)
dict1['a']='test'
print(dict1)
```

####  Question:請問執行後的結果哪一個是對的?(選擇題)
```python
dict1={'a':100,'b':200, 'c':300} 
add_dic={'d':400} 
dict1.update(add_dic) 
print(dict1['d'])
```

(1) 產生錯誤  
(2) 200  
(3) 300  
(4) 400

---
####  請問執行後的結果哪一個是對的?(選擇題)
```python
dict1={'a':100,'b':200, 'c':300} 
add_dic={'d':400} 
dict1.update(add_dic) 
print(dict1['e'])
``` 
(1) 產生錯誤  
(2) 200  
(3) 300  
(4) 400   

---

```python
>>> pythons = {
... 'Chapman': 'Graham',
... 'Cleese': 'John',
... 'Idle': 'Eric',
... 'Jones': 'Terry',
... 'Palin': 'Michael',
... }

>>> pythons
{'Cleese': 'John', 'Jones': 'Terry', 'Palin': 'Michael', 'Chapman': 'Graham', 'Idle': 'Eric'}


>>> pythons['Gilliam'] = 'Gerry'
>>> pythons
{'Cleese': 'John', 'Gilliam': 'Gerry', 'Palin': 'Michael',
'Chapman': 'Graham', 'Idle': 'Eric', 'Jones': 'Terry'}


>>> pythons['Gilliam'] = 'Terry'
>>> pythons
{'Cleese': 'John', 'Gilliam': 'Terry', 'Palin': 'Michael',
'Chapman': 'Graham', 'Idle': 'Eric', 'Jones': 'Terry'}

```

```python
>>> pythons = {
... 'Chapman': 'Graham',
... 'Cleese': 'John',
... 'Gilliam': 'Terry',
... 'Idle': 'Eric',
... 'Jones': 'Terry',
... 'Palin': 'Michael'
... }
>>> pythons
{'Cleese': 'John', 'Gilliam': 'Terry', 'Palin': 'Michael', 'Chapman': 'Graham', 'Idle': 'Eric', 'Jones': 'Terry'}


>>> others = { 'Marx': 'Groucho', 'Howard': 'Moe' }
>>> pythons.update(others)
>>> pythons
{'Cleese': 'John', 'Howard': 'Moe', 'Gilliam': 'Terry', 'Palin': 'Michael', 'Marx': 'Groucho', 'Chapman': 'Graham', 'Idle': 'Eric', 'Jones': 'Terry'}


```

###  刪除動作
- 刪除動作可分刪除資料、清除所有項目與刪除字典三種:
	- del dict[key]  刪除某一個 key 的資料
	- dict.clear( )  清除所有項目
	- del dict  刪除字典

###  關於 key 的判斷
- 請以 (key in dict1.keys( )) 方式進行判斷
- 存在傳回 true
- 不存在傳回 false

#### 操作範例 :請動手操作，並留意輸出結果
```python
#dict5.py

dict1={'a':100,'b':200, 'c':300} 
print(dict1)
del dict1['c']
print(dict1)
print('c' in dict1.keys( )) 
print('a' in dict1.keys( ))
```

####  Question:請問執行後的結果哪一個是對的?(選擇題)
```python
dict1={'a':100,'b':200, 'c':300} 
del dict1['b']
print ('b' in dict1.keys())
```
(1) 產生錯誤  
(2) True  
(3) 200  
(4) False  

---

#### Question: 請問執行後的結果哪一個是對的?(選擇題)

```python
dict1={'a':100,'b':200, 'c':300} 
dict1.clear( )
print ('b' in dict1.keys( ))
```
(1) 產生錯誤  
(2) True  
(3) 200  
(4) False 

```python
>>> first = {'a': 1, 'b': 2} 
>>> second = {'b': 'platypus'} 
>>> first.update(second)
>>> first
{'b': 'platypus', 'a': 1}

>>> del pythons['Marx']

``` 

```python


>>> pythons = {'Cleese': 'John', 'Howard': 'Moe', 'Gilliam': 'Terry', 'Palin': 'Michael', 'Chapman': 'Graham', 'Idle': 'Eric', 'Jones': 'Terry'}

>>> del pythons['Howard']
>>> pythons
{'Cleese': 'John', 'Gilliam': 'Terry', 'Palin': 'Michael', 'Chapman': 'Graham', 'Idle': 'Eric', 'Jones': 'Terry'}


>>> pythons.clear() 
>>> pythons
{}
>>> pythons = {}
>>> pythons
{}

```

####  Question:請問執行後的結果哪一個是對的?(選擇題)
```python
dict1={'a':100,'b':200, 'c':300} 
del dict1
print('b' in dict1.keys( ))
```
(1) 產生錯誤   
(2) True    
(3) 200     
(4) False  

#### 操作範例:請動手操作，並留意輸出結果
```python
dict1={'a':100,'b':200,'c':300} 
for c in dict1.keys( ):
	print(c) 
print("-----")

for c in dict1.keys( ):
	print(dict1[c]) 
print("-----")

for c in dict1: 
	print(c)
print("-----")

for c in dict1.values( ):
	print(c)
 
```

```python
>>> pythons = {'Chapman': 'Graham', 'Cleese': 'John',
'Jones': 'Terry', 'Palin': 'Michael'}
>>> 'Chapman' in pythons 
True
>>> 'Palin' in pythons 
True
>>> 'Gilliam' in pythons 
False


>>> pythons['Cleese']
'John'


>>> pythons['Marx']
    Traceback (most recent call last):
File "<stdin>", line 1, in <module> KeyError: 'Marx'


>>> 'Marx' in pythons 
False


>>> pythons.get('Cleese') 
'John'


>>> pythons.get('Marx', 'Not a Python')
'Not a Python'

```

### key(),values(),items(),copy()

```python

>>> signals = {'green': 'go', 'yellow': 'go faster', 'red': 'smile for the camera'} 
>>> signals.keys()
dict_keys(['green', 'red', 'yellow'])


>>> list( signals.values() )
['go', 'smile for the camera', 'go faster']


>>> list( signals.items() )
[('green', 'go'), ('red', 'smile for the camera'), ('yellow', 'go faster')]


>>> signals = {'green': 'go', 'yellow': 'go faster', 'red': 'smile for the camera'} 
>>> save_signals = signals
>>> signals['blue'] = 'confuse everyone'
>>> save_signals
    {'blue': 'confuse everyone', 'green': 'go',
    'red': 'smile for the camera', 'yellow': 'go faster'}


>>> signals = {'green': 'go', 'yellow': 'go faster', 'red': 'smile for the camera'} >>> original_signals = signals.copy()
>>> signals['blue'] = 'confuse everyone'
>>> signals
{'blue': 'confuse everyone', 'green': 'go',
'red': 'smile for the camera', 'yellow': 'go faster'}
>>> original_signals
{'green': 'go', 'red': 'smile for the camera', 'yellow': 'go faster'}



```

## Sets

```python
>>> empty_set = set()
>>> empty_set
set()
>>> even_numbers = {0, 2, 4, 6, 8} 
>>> even_numbers
{0,8,2,4,6}
>>> odd_numbers = {1, 3, 5, 7, 9} 
>>> odd_numbers
{9,3,1,5,7}


>>> set( 'letters' )
{'l', 'e', 't', 'r', 's'}


>>> set( ['Dasher', 'Dancer', 'Prancer', 'Mason-Dixon'] ) 
{'Dancer', 'Dasher', 'Prancer', 'Mason-Dixon'}


>>> set( ('Ummagumma', 'Echoes', 'Atom Heart Mother') )
{'Ummagumma', 'Atom Heart Mother', 'Echoes'}


>>> set( {'apple': 'red', 'orange': 'orange', 'cherry': 'red'} )
{'apple', 'cherry', 'orange'}


>>> drinks = {
... 'martini': {'vodka', 'vermouth'},
... 'black russian': {'vodka', 'kahlua'},
... 'white russian': {'cream', 'kahlua', 'vodka'},
... 'manhattan': {'rye', 'vermouth', 'bitters'},
... 'screwdriver': {'orange juice', 'vodka'}
... }



```




