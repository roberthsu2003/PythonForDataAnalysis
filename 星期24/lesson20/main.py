from urllib.request import Request, urlopen
import ssl
import pandas as pd

ssl._create_default_https_context = ssl._create_unverified_context
url = 'https://goldprice.org/cryptocurrency-price'
heads ={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
import_request = Request(url, headers=heads)
web_page_data = urlopen(import_request).read()
df = pd.read_html(web_page_data)
dataFrame = df[0]
dataFrame.drop(columns=['Circulating Supply','Volume (24h)','Price Chart (7d)'],inplace=True)
dataFrame.rename(columns={'Rank':'名次',
                          'CryptoCurrency':'加密貨幣',
                          'Market Cap.':'市場總市值',
                          'Price':'價格',
                          'Change (24h)':'24小時變化(%)'
                         },inplace=True)
dataFrame['市場總市值'] = dataFrame['市場總市值'].map(lambda value:value[1:])
dataFrame['價格'] = dataFrame['價格'].map(lambda value:value[1:])
dataFrame['24小時變化(%)'] = dataFrame['24小時變化(%)'].map(lambda value:value[:-1])
dataFrame['市場總市值'] = dataFrame['市場總市值'].str.replace(',','')
dataFrame['價格'] = dataFrame['價格'].str.replace(',','')
dataFrame['市場總市值'] = dataFrame['市場總市值'].astype(int)
dataFrame['價格'] = dataFrame['價格'].astype(float).round(2)
dataFrame['24小時變化(%)'] = dataFrame['24小時變化(%)'].astype(float).round(2)
bitcoin_rank = dataFrame[dataFrame['加密貨幣'] == 'Bitcoin']['名次'].iloc[0]
print(bitcoin_rank)
bitcoin_currency = dataFrame[dataFrame['加密貨幣'] == 'Bitcoin']['加密貨幣'].iloc[0]
print(bitcoin_currency)
bitcoin_price = dataFrame[dataFrame['加密貨幣'] == 'Bitcoin']['價格'].iloc[0]
print(bitcoin_price)
bitcoin_change = dataFrame[dataFrame['加密貨幣'] == 'Bitcoin']['24小時變化(%)'].iloc[0]
print(bitcoin_change)
bitcoin_market = dataFrame[dataFrame['加密貨幣'] == 'Bitcoin']['市場總市值'].iloc[0]
print(bitcoin_market)
