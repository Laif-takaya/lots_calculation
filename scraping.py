#import request
from bs4 import BeautifulSoup

def getNews(word):
    HTML = requests.get("https://info.finance.yahoo.co.jp/fx/list/")
    SOUP = BeautifulSoup(HTML.content, "html.parser")
    rm=word.split()

    currency_pair=rm[0]
    account_balance=rm[1]
    difference=rm[2]
    ab=float(account_balance)
    df=float(difference)

    if "JPY" in currency_pair:
        cp=100
    elif "GBP/USD" == currency_pair:
        RES = SOUP.find(id="GBPJPY_chart_ask")
        RES=RES.string
        cp=float(RES)
    elif "AUD/USD" == currency_pair:
        RES = SOUP.find(id="AUDJPY_chart_ask")
        RES=RES.string
        cp=float(RES)
    elif "EUR/GBP" == currency_pair:
        RES = SOUP.find(id="EURJPY_chart_ask")
        RES=RES.string
        cp=float(RES)
    elif "EUR/USD" == currency_pair:
        RES = SOUP.find(id="EURJPY_chart_ask")
        RES=RES.string
        cp=float(RES)
    elif "NZD/USD" == currency_pair:
        RES = SOUP.find(id="NZDJPY_chart_ask")
        RES=RES.string
        cp=float(RES)
    lots=ab*0.2/df/cp

    result = lots

    return result
