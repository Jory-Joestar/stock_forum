'''
定义Stock类，包含代码、名称、注册地、行业、市场、上市时间的基础信息，
方法get_price为获取股票行情（返回值类型为Dataframe)，
方法draw_kline为绘制K线图（返回值类型为pyecharts.charts.kline.Kline）

三个函数
get_stock获取所有股票的基础信息（返回值类型为Dataframe)
select_basic_name用股票名称选择股票（不能模糊查找，返回类型为Stock类）
select_basic_code用股票代码选择股票（不能模糊查找，返回类型为Stock类）
'''
import tushare as ts
from pyecharts import Kline
import pandas as pd
import time


class Stock(object):
    # 定义股票类
    def __init__(self, code, name, area, industry, market, list_date):
        # 股票基本信息：代码、名称、注册地、行业、市场、上市时间
        self.code = code
        self.name = name
        self.area = area
        self.industry = industry
        self.market = market
        self.list_date = list_date

    def show_info(self):
        # 展示股票基本信息
        print('代码:', self.code)
        print('名称:', self.name)
        print('注册地:', self.area)
        print('行业:', self.industry)
        print('市场:', self.market)
        print('上市时间:', self.list_date)

    def get_price(self, start, end,pro):
        # 输入起始时间、终止时间获取股票日行情
        price = pro.daily(ts_code=self.code, start_date=start, end_date=end)
        return price

    def draw_kline(self, start, end,pro):
        # 输入起始时间、终止时间绘制K线图，并将K线图保存到本地
        price = self.get_price(start, end,pro)
        price.index = pd.to_datetime(price.trade_date)
        price = price.sort_index()
        v1 = list(price.loc[:, ['open', 'close', 'low', 'high']].values)
        v0 = list(price.index.strftime('%Y%m%d'))
        kline = Kline(self.name + 'K线图', title_text_size=15)
        kline.add("", v0, v1, is_datazoom_show=True,
                  mark_line=["average"],
                  mark_point=["max", "min"],
                  mark_point_symbolsize=60,
                  mark_line_valuedim=['highest', 'lowest'])

        # 将K线图保存到本地
        kline.render(self.name + start + '-' + end + '.html')
        return kline


def get_basic(pro):
    
    # 股票代码、简称、注册地、行业、上市时间等信息
    basic = pro.stock_basic(list_status='L')
    return basic


def select_basic_name(name,pro):
    # 在basic中，用名称选择某一支股票
    basic = get_basic(pro)
    for index in range(0, basic.shape[0]):
        if basic.loc[index]['name'] == name:
            stock = Stock(basic.loc[index]['ts_code'],
                          basic.loc[index]['name'],
                          basic.loc[index]['area'],
                          basic.loc[index]['industry'],
                          basic.loc[index]['market'],
                          basic.loc[index]['list_date'])
            return stock
    # 如果搜不到，给股票全部赋值None
    stock = Stock('None', 'None', 'None', 'None', 'None', 'None', )
    return stock


def select_basic_code(code,pro):
    # 在basic中，用代码选择某一支股票
    basic = get_basic(pro)
    for index in range(0, basic.shape[0]):
        if basic.loc[index]['ts_code'] == code:
            stock = Stock(basic.loc[index]['ts_code'],
                          basic.loc[index]['name'],
                          basic.loc[index]['area'],
                          basic.loc[index]['industry'],
                          basic.loc[index]['market'],
                          basic.loc[index]['list_date'])
            return stock
    # 如果搜不到，给股票全部赋值None
    stock = Stock('None', 'None', 'None', 'None', 'None', 'None', )
    return stock


def main():
    token = 'c89761557a8c339b857a2fedebea03685aee396dd2501d063d7271fd'
    ts.set_token(token)
    pro = ts.pro_api(token)
    # 下面是测试
    stock_1 = select_basic_name('南京银行',pro)
    stock_2 = select_basic_code('000001.SZ',pro)
    #print(stock_2.get_price('20200101', '20200201',pro))
    #stock_1.draw_kline('20200101', '20200201',pro)
    res=stock_1.get_price('20200415','20200415',pro)
    if res.values.tolist():
        print('yes')
    print(res.values.tolist()[0])
    print(res.columns.values.tolist())

if __name__ == "__main__":
    main()
