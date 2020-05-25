from extends.data.stock_est import Stock_e
import os

class GetEst():
    def __init__(self,name):
        self.name=name
        self.error=None
        self.esting_stock=Stock_e(name)
        self.train,self.valid,self.pred_price,self.lastweek_ave=self.esting_stock.get_train(name)
    
    def plot_trends(self):
        ''' 画股票的趋势预测图 '''
        myplt=self.esting_stock.pltstock(self.train,self.valid,self.name)
        root_path = os.path.dirname(os.path.dirname(__file__))
        #尝试一下写到一个固定的临时文件，每次调用查看股票信息时删除，然后新建，以此来防止文件冲突和储存堆满
        #临时文件为static/trends/stock_trends.html
        target_file=os.path.join(root_path, 'static', 'trends', 'stock_trends' + '.jpg')
        if os.path.exists(target_file):
            os.remove(target_file)
        myplt.savefig(target_file)

    def remark(self):
        '''给出股票评级'''
        return self.esting_stock.remark(self.pred_price,self.lastweek_ave)

    def forecast(self):
        '''预测股票价格'''
        return self.esting_stock.forecasestock(self.pred_price,self.name)
        