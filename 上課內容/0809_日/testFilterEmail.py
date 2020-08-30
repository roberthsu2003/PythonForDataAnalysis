import re

s = "New eID由央行(中央印製廠)承擔製卡作業國發會統bogusemail.123@sillymail.com由郵箱驗證及帳戶激活這種機制bb在匹配电子邮件地址时,roberthsu2003@gmail.com，測試使用robert@gmail.com啦啦啦"

'''
\w ==>原定義:單詞字元包括：a-z、A-Z、0-9、_(底線),
但實測後發現連中文都被當作單詞字元,
所以若 email前後有中文就不能用 \w作判斷,
可能是這個原因
'''
# res = r'\w+[.|\w]\w+@\w+[.]\w+[.|\w+]\w+'              #不可用
res = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}' #可用
# res = r'[A-Za-z0-9_\-\.]+@[\w\.-]+\.[a-zA-Z]{2,4}'     #可用

print(re.findall(res, s))