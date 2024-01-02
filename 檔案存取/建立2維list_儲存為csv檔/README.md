## main.py

```python
import pyinputplus as pyip
from tools import getStudents,save_to_csv


if __name__ == "__main__":
    s_nums:int = pyip.inputInt("請輸入學生的人數(1~50):",min=1,max=50)
    students:list[dict] = getStudents(s_nums)
    fileName:str = pyip.inputFilename("請輸入檔案名稱(不用輸入副檔名稱):")
    save_to_csv(students,fileName)
```

```python
from random import randint,choices
import csv
from csv import DictWriter

def getStudents(nums:int) -> list[dict]:  
    students:list[dict] = []
    with open('names.txt',mode='r',encoding='utf-8') as file:
        names:str = file.read()
    nameList:list[str] = names.split('\n')
    names:list[str] = choices(nameList,k=nums)

    for i in range(nums):
        stu = {
        '姓名':names[i],
        '國文':randint(45,100),
        '英文':randint(45,100),
        '數學':randint(45,100),
        '地理':randint(45,100),
        '歷史':randint(45,100),
        }
        students.append(stu)
        
    return students

def save_to_csv(students:list[dict],fileName:str)->None:    
    fileNameWithExtension:str = fileName + '.csv'
    with open(fileNameWithExtension,mode='w',encoding='utf-8',newline='') as file:
        fieldnames:list[str] = ['姓名', '國文', '英文', '數學', '地理', '歷史']
        writer:DictWriter = csv.DictWriter(file,fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(students)
    print("寫入成功")

```