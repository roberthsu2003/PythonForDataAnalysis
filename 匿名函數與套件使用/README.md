# 暱名函數與套件的使用
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

