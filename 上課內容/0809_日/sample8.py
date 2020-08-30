import re

regular = r'\w+[.|\w]\w+@\w+[.]\w+[.|\w+]\w+'
emails = input('請輸入文字,搜尋所有的email:')
findallObject=re.findall(regular, emails)
print(findallObject)