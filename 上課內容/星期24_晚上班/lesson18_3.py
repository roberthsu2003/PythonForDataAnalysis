import numpy as np
import pandas as pd

def main():
    dataFrame = pd.read_csv('各鄉鎮市區人口密度.csv')
    dataFrame1 = dataFrame.dropna()
    dataFrame2 = dataFrame1[dataFrame1['people_total'] != '年底人口數']
    dataFrame3=dataFrame2.replace(to_replace="… ",value=0)
    dataFrame3['people_total'] = dataFrame3['people_total'].astype(np.int32)
    dataFrame3['area'] = dataFrame3['area'].astype(np.float16)
    dataFrame3['population_density'] = dataFrame3['population_density'].astype(np.int32)  
    dataFrame3.to_excel('各鄉鎮市區人口密度.xlsx')
    
if __name__ == "__main__":
    main()