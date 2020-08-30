import re
'''
bogusemail123@sillymail.com, ,,,roberthsu2003@gmail.com,,,robert@gmail.com
'''
regular = r'\w+[.|\w]\w+@\w+[.]\w+[.|\w+]\w+'
emails = input('請輸入文字,搜尋所有的email:')
findallList=re.findall(regular, emails)
print(findallList)
