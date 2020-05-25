from extends.data.stock_basic import select_basic_name,get_related_name
import tushare as ts

class GetPrice():
    def __init__(self):
        self.token='c89761557a8c339b857a2fedebea03685aee396dd2501d063d7271fd'
        ts.set_token(self.token)
        self.pro = ts.pro_api(self.token)

    def by_name(self,stock_name,date):
        stock=select_basic_name(stock_name,self.pro)
        return stock.get_price(date,date,self.pro)

    def current_price(self, stock_name):
        stock = select_basic_name(stock_name, self.pro)
        stock_code=verified_code(stock.code)
        return (stock_code,stock.get_current_price())

    def draw_kline(self, stock_name, start_date, end_date):
        stock = select_basic_name(stock_name, self.pro)
        stock.draw_kline(start_date, end_date, self.pro)
        return

    def get_related(self, input_name):
        return get_related_name(input_name, self.pro)

def verified_code(name):
    ''' 将以.SH为后缀的股票代码改为以.SS为后缀的股票代码 '''
    list_name=list(name)
    if list_name[-2]=='S' and list_name[-1]=='H':
        list_name[-1]='S'
    return ''.join(list_name)

if __name__ == "__main__":
    getprise=GetPrice()
    print(getprise.by_name('南京银行','20200402'))