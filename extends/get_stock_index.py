import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import MONDAY, DateFormatter, DayLocator, WeekdayLocator
import tushare as ts
from mpl_finance import candlestick_ohlc
import os


class zhishu():
    def __init__(self,name):
        self.name=name

    def plot_zhishu(self,name):
        mondays = WeekdayLocator(MONDAY)
        alldays = DayLocator()
        weekFormatter = DateFormatter('%b %d')
        dayFormatter = DateFormatter('%d')
        quotes = ts.get_k_data(name, ktype='D', autype='qfq', start='2020-01-01', end='')
        quotes.index = pd.to_datetime(quotes['date'])
        fig, ax = plt.subplots()
        fig.subplots_adjust(bottom=0.2)
        ax.xaxis.set_minor_locator(alldays)
        candlestick_ohlc(ax, zip(mdates.date2num(quotes.index.to_pydatetime()), quotes['open'], quotes['high'],
                                 quotes['low'], quotes['close']), width=0.6, colorup='r', colordown='g')
        ax.xaxis_date()
        ax.autoscale_view()
        plt.setp(plt.gca().get_xticklabels())
        return plt

def main():

    name='000001'
    zs=zhishu(name)
    zhishu_plt=zs.plot_zhishu(name)
    zhishu_plt.savefig('zhishu.jpg')

def draw_index():
    name='000001'
    zs=zhishu(name)
    zhishu_plt=zs.plot_zhishu(name)
    root_path = os.path.dirname(os.path.dirname(__file__))
    target_file=os.path.join(root_path, 'static', 'trends', 'zhishu' + '.jpg')
    if os.path.exists(target_file):
        os.remove(target_file)
    zhishu_plt.savefig(target_file)


if __name__ == "__main__":
    main()


