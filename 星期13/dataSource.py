import requests
import sqlite3
from sqlite3 import Error


def __create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
        return
    return conn


def __create_table_pm25(conn):
    sql = ''' 
    CREATE TABLE IF NOT EXISTS pm25 (
	id INTEGER PRIMARY KEY,
	站點 TEXT,
	城市 TEXT,
	pm25 REAL,
	日期 TEXT,
	單位 TEXT,
	UNIQUE(站點)
    );
    '''
    cursor = conn.cursor()
    cursor.execute(sql)
    # conn.commit()


def __replace_pm25(conn, values):
    """
    新增資料至projects資料庫
    :param conn:Connection物件
    :param project:tuple(加入至資料庫的內容)
    :return:自動建立id的最後一筆
    """
    sql = ''' 
    REPLACE INTO pm25 (站點,城市,pm25,日期,單位)
    VALUES (?,?,?,?,?)
    '''
    cursor = conn.cursor()
    cursor.execute(sql, values)
    conn.commit()


def __downloadData():
    urlpath = '	https://data.epa.gov.tw/api/v1/aqx_p_02?limit=1000&api_key=9be7b239-557b-4c10-9775-78cadfc555e9&sort=ImportDate%20desc&format=json'

    def stringToFloat(s):
        try:
            return float(s)
        except:
            return 999.0

    response = requests.get(urlpath)
    if response.status_code == 200:
        print('下載成功')
        data = response.json()
        datas = data["records"]
        importData = [
            (item['Site'], item['county'], stringToFloat(item['PM25']), item['DataCreationDate'], item['ItemUnit']) for
            item in datas]
        return importData


def __saveToDataBase(datas):
    '''
    儲存資料至資料庫db25
    :param datas: list->tuple
    :return:
    '''
    conn = __create_connection('pm25.db')
    print("資料庫連線成功")
    with conn:
        __create_table_pm25(conn)  # 建立資料表
        for value in datas:
            __replace_pm25(conn, value)  # 插入資料


def get_city_name():
    conn = __create_connection('pm25.db')
    print("資料庫連線成功")

    sql = ''' 
        SELECT DISTINCT 城市
        FROM pm25
        '''
    with conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        city_name_list = [row[0] for row in rows]
        return city_name_list


def get_site_name(city):
    conn = __create_connection('pm25.db')
    print("資料庫連線成功")
    sql = '''
    SELECT DISTINCT 站點
    FROM pm25
    WHERE 城市=?
    '''
    with conn:
        cursor = conn.cursor()
        cursor.execute(sql, (city,))
        rows = cursor.fetchall()
        sites = [item[0] for item in rows]
    return sites


def get_site_info(site):
    conn = __create_connection('pm25.db')
    print("資料庫連線成功")
    sql = '''
        SELECT  *
        FROM pm25
        WHERE 站點=?
        LIMIT 1
        '''
    cursor = conn.cursor()
    cursor.execute(sql, (site,))
    rows = cursor.fetchone()
    return rows


def get_better():
    conn = __create_connection('pm25.db')
    print("資料庫連線成功")
    sql = '''
        SELECT  *
        FROM pm25
        WHERE pm25 <= 35
        '''
    with conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
    return rows


def get_normal():
    conn = __create_connection('pm25.db')
    print("資料庫連線成功")
    sql = '''
        SELECT  *
        FROM pm25
        WHERE pm25 BETWEEN 35 AND 53
        '''
    with conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
    return rows


def get_bad():
    conn = __create_connection('pm25.db')
    print("資料庫連線成功")
    sql = '''
            SELECT  *
            FROM pm25
            WHERE pm25 > 53
            '''
    with conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
    return rows


def download_save_to_DataBase():
    importData = __downloadData()  # 下載資訊
    __saveToDataBase(importData)  # 儲存資料至資料庫