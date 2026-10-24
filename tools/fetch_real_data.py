"""從政府資料開放平台下載各章範例使用的真實資料，存成快照放在 tools/real_data/。

用法（在專案根目錄執行）：
    python tools/fetch_real_data.py              # 下載全部資料集
    python tools/fetch_real_data.py aqi mrt      # 只更新指定資料集

為什麼要存快照：開放資料的網址與內容會變動，範例 Notebook 一律讀快照，
課堂上每個學生看到的數字都一樣；想看最新資料時，各範例另附「抓最新資料」的程式。
更新快照後，請重新執行 build_student_materials.py 產生學生素材。

所有資料皆依「政府資料開放授權條款－第1版」使用，出處記錄在 tools/real_data/SOURCES.json。
"""
import io
import json
import sys
import time
import urllib.request
from datetime import date
from pathlib import Path
from urllib.parse import quote

import pandas as pd

OUT = Path(__file__).resolve().parent / 'real_data'
LICENSE = '政府資料開放授權條款－第1版'
AQI_KEY = '846e44e1-8cc5-4893-ad87-c79d2d383706'   # 環境部在政府資料開放平台公開的 API key
MRT_MONTH = '202603'                                 # 捷運使用的月份（一個月的原始檔約 300MB，下載後只留彙總）

SOURCES = {
    'youbike': dict(file='臺北市YouBike每月使用量.csv', dataset=135775, title='YouBike臺北市站位每月使用量', publisher='臺北市政府交通局',
                    url='https://data.taipei/api/dataset/d8cefb03-aba2-41ca-9996-d8774313cdc6/resource/8f690548-61bc-4bff-8baa-01d465eb672c/download'),
    'recycle': dict(file='臺北市各區資源回收量.csv', dataset=121705, title='臺北市各區清潔隊資源回收量', publisher='臺北市政府環境保護局',
                    url='https://data.taipei/api/dataset/34f4f00b-5386-43ab-bcc7-b0ae7ee3e305/resource/59a40935-9d5a-474b-b71d-bd861047b6ba/download'),
    'power_home': dict(file='台電住宅每戶平均用電與電費.csv', dataset=17062, title='台灣電力公司住宅用戶每月平均用電度數及電費', publisher='台灣電力股份有限公司',
                       url='https://service.taipower.com.tw/data/opendata/apply/file/d007004/001.csv'),
    'power_city': dict(file='台電各縣市用電統計.csv', dataset=29935, title='台灣電力公司各縣市住宅、服務業及機關用電統計資料', publisher='台灣電力股份有限公司',
                       url='https://service.taipower.com.tw/data/opendata/apply/file/d007012/001.csv'),
    'aqi': dict(file='日空氣品質指標_近一年.csv', dataset=40507, title='日空氣品質指標(AQI)', publisher='環境部',
                url=f'https://data.moenv.gov.tw/api/v2/aqx_p_434?api_key={AQI_KEY}&format=CSV'),
    'boxoffice': dict(file='全國電影票房_2016至今.json', dataset=94224, title='全國電影票房統計數據', publisher='文化部',
                      url='https://boxofficetw.tfai.org.tw/OpenData/statistic/since2016'),
    'a1': dict(file='A1類交通事故.csv', dataset=12818, title='即時交通事故資料(A1類)', publisher='內政部警政署',
               url='https://opdadm.moi.gov.tw/api/v1/no-auth/resource/api/dataset/02D40248-7CAA-4354-82EA-E27AB8DCAB39/resource/67214307-AD41-4FE7-A04F-D8051A0301DB/download'),
    'population_112': dict(file='各鄉鎮市區人口密度_112年.json', dataset=8410, title='各鄉鎮市區人口密度（民國 112 年底）', publisher='內政部',
                           url='https://www.ris.gov.tw/rs-opendata/api/v1/datastore/ODRP048/112'),
    'population_113': dict(file='各鄉鎮市區人口密度_113年.json', dataset=8410, title='各鄉鎮市區人口密度（民國 113 年底）', publisher='內政部',
                           url='https://www.ris.gov.tw/rs-opendata/api/v1/datastore/ODRP048/113'),
    'population_114': dict(file='各鄉鎮市區人口密度_114年.json', dataset=8410, title='各鄉鎮市區人口密度（民國 114 年底）', publisher='內政部',
                           url='https://www.ris.gov.tw/rs-opendata/api/v1/datastore/ODRP048/114'),
    'mrt': dict(file=f'臺北捷運各站分時進出量_{MRT_MONTH}.csv', dataset=128506, title='臺北捷運各站分時進出量統計', publisher='臺北大眾捷運股份有限公司',
                url='http://tcgmetro.blob.core.windows.net/stationod/' + quote(f'臺北捷運每日分時各站OD流量統計資料_{MRT_MONTH}.csv')),
}


def download(url, timeout=300):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (PythonForDataAnalysis course)'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def fetch_aqi(src):
    """一次最多 1000 筆，依日期由新到舊分頁，抓滿最近 365 天。"""
    frames, offset = [], 0
    while True:
        raw = download(f"{src['url']}&limit=1000&offset={offset}&sort=monitordate%20desc")
        part = pd.read_csv(io.BytesIO(raw), dtype=str)
        frames.append(part)
        offset += 1000
        days = pd.concat(frames)['monitordate'].nunique()
        if part.empty or days > 366:
            break
        time.sleep(0.3)
    df = pd.concat(frames)
    keep = sorted(df['monitordate'].unique())[-365:]
    df = df[df['monitordate'].isin(keep)].drop_duplicates(['siteid', 'monitordate'])
    df = df.dropna(subset=['siteid', 'monitordate'])
    df = df.assign(_site=pd.to_numeric(df['siteid'])).sort_values(['monitordate', '_site']).drop(columns='_site')
    df.to_csv(OUT / src['file'], index=False, encoding='utf-8')


def fetch_mrt(src):
    """原始檔是「日期、時段、進站、出站、人次」的起訖（OD）資料，彙總成每站每小時的進站與出站人次。"""
    tmp = OUT / '_mrt_raw.csv'
    tmp.write_bytes(download(src['url'], timeout=1200))
    totals = []
    for chunk in pd.read_csv(tmp, chunksize=1_000_000, encoding='utf-8-sig'):
        chunk.columns = ['日期', '時段', '進站', '出站', '人次']
        inbound = chunk.groupby(['日期', '時段', '進站'])['人次'].sum().rename('進站人次')
        outbound = chunk.groupby(['日期', '時段', '出站'])['人次'].sum().rename('出站人次')
        inbound.index.names = outbound.index.names = ['日期', '時段', '車站']
        totals.append(pd.concat([inbound, outbound], axis=1))
    tmp.unlink()
    df = pd.concat(totals).groupby(level=[0, 1, 2]).sum().astype(int).reset_index()
    df.to_csv(OUT / src['file'], index=False, encoding='utf-8')


def fetch(name):
    src = SOURCES[name]
    if name == 'aqi':
        fetch_aqi(src)
    elif name == 'mrt':
        fetch_mrt(src)
    else:
        (OUT / src['file']).write_bytes(download(src['url']))   # 原封不動保存（包含 Big5 編碼、千分位等「真實的髒」）
    size = (OUT / src['file']).stat().st_size
    print(f'✅ {name}: {src["file"]}（{size / 1024:,.0f} KB）')


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    names = [a for a in sys.argv[1:]] or list(SOURCES)
    meta_path = OUT / 'SOURCES.json'
    meta = json.loads(meta_path.read_text(encoding='utf-8')) if meta_path.exists() else {}
    for name in names:
        fetch(name)
        src = SOURCES[name]
        meta[name] = {**{k: src[k] for k in ('file', 'title', 'publisher', 'url')},
                      'page': f"https://data.gov.tw/dataset/{src['dataset']}", 'license': LICENSE,
                      'fetched': date.today().isoformat()}
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')
