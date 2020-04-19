from extends.data.stock_basic import select_basic_name
import tushare as ts
from pyecharts import Kline
import pandas as pd

class GetPrice():
    def __init__(self):
        self.token='c89761557a8c339b857a2fedebea03685aee396dd2501d063d7271fd'
        ts.set_token(self.token)
        self.pro = ts.pro_api(self.token)

    def by_name(self,stock_name,date):
        stock=select_basic_name(stock_name,self.pro)
        return stock.get_price(date,date,self.pro)

if __name__ == "__main__":
    getprise=GetPrice()
    print(getprise.by_name('南京银行','20200402'))