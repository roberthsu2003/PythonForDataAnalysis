# 暱名函數與套件的使用
##  匿名函數
1. 不需要定義函數名稱的，只需要用運算式或表達分析語法。
2. Python 使用 lambda 語法定義匿名函數。
3. 匿名函數是一個表達式/計算式，並不是一個執行流程區塊。
4. 匿名函數可以出現在一般函數不允許的地方，例如像 list 內部或函數 呼叫參數的位置。

###  匿名函數說明
1. 匿名函數會自動返回計算式結果，一般函數必須進行規劃設計才能返回。
2. 匿名函數用於一個計算式的處理，而一般函數可以做更多複雜的事情。
3. 匿名函數語法:
	- lambda 參數: 運算式,資料來源
	- 參數-可能是多個值
	- 資料來源-於第一個之後的都是資料來源，這裏得對應資料輸入

### Functions Are First-Class Citizens
```python
>>> def answer(): 
		print(42)

>>> answer()
42

==========================================

>>> def run_something(func): 
		func()

>>> run_something(answer) 
42
```


```python
def add_args(arg1, arg2): 
	print(arg1 + arg2)
	

>>> type(add_args)
<class 'function'>


def run_something_with_args(func, arg1, arg2):
	func(arg1, arg2)
	

>>> run_something_with_args(add_args, 5, 9) 
14

```

```python
def sum_args(*args): 
	return sum(args)
	

def run_with_positional_args(func, *args):
	return func(*args)


>>> run_with_positional_args(sum_args, 1, 2, 3, 4)
10	
```

### Inner Functions

```python
def outer(a, b):
	def inner(c, d): 
		returnc+d
	return inner(a, b)


>>> outer(4, 7)
11


def knights(saying):
	def inner(quote):	
		return "We are the knights who say: '%s'" % quote
	return inner(saying)
	
	
>>> knights('Ni!')
    "We are the knights who say: 'Ni!'"
```

### Closures
```python
def knights2(saying):
	def inner2():
		return "We are the knights who say: '%s'" % saying
	return inner2

>>> a = knights2('Duck')
>>> b = knights2('Hasenpfeffer')

>>> type(a) <class 'function'> 
>>> type(b) <class 'function'>

>>> a
<function knights2.<locals>.inner2 at 0x10193e158> 
>>> b
<function knights2.<locals>.inner2 at 0x10193e1e0>

>>> a()
"We are the knights who say: 'Duck'"
>>> b()
"We are the knights who say: 'Hasenpfeffer'"
```

### Anonymous Functions: the lambda() Function
```python
def edit_story(words, func):
	for word in words:
		print(func(word))


>>> stairs = ['thud', 'meow', 'thud', 'hiss']


def enliven(word): # give that prose more punch 
	return word.capitalize() + '!'
	
>>> edit_story(stairs, enliven) 
Thud!
Meow!
Thud!
Hiss!


>>> edit_story(stairs, lambda word: word.capitalize() + '!') 
Thud!
Meow!
Thud!
Hiss!
```

