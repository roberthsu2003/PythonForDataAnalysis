#! usr/bin/python3.x
'''
說明:驗證中華民國身份証
作者:robertHsu
'''

import re
regular = r'^[a-zA-Z][0-9]{9}$'
taiwanId=input("請輸入身份證字號:")
matchObject=re.match(regular,taiwanId,re.I)
if matchObject is None:
    print(taiwanId,'不正確')
else:
    print(matchObject.group(),"正確")
