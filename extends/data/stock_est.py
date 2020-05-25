#Import the libraries
import math
import pandas_datareader as web
import numpy as np
import pandas as pd
import datetime
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

class Stock_e():
    def __init__(self,name):
        self.name=name

    def get_train(self,name):
        #这一部分内容比较多，作用是通过datareader读取股票信息，分割并训练模型，得到学习的结果
        #参数name是股票代码，如600895.ss
        start = '2019-06-30'
        end = datetime.date.today()
        df = company_quote = web.DataReader(name, data_source='yahoo', start=start, end=end)
        # Create a new dataframe with only the 'Close' column
        data = df.filter(['Close'])
        # Converting the dataframe to a numpy array
        dataset = data.values
        # Get /Compute the number of rows to train the model
        training_data_len = math.ceil(len(dataset) * .8)
        # Scale the all of the data to be values between 0 and 1
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(dataset)
        # Create the scaled training data set
        train_data = scaled_data[0:training_data_len, :]
        # Split the data into x_train and y_train data sets
        x_train = []
        y_train = []
        for i in range(60, len(train_data)):
            x_train.append(train_data[i - 60:i, 0])
            y_train.append(train_data[i, 0])
        # Convert x_train and y_train to numpy arrays
        x_train, y_train = np.array(x_train), np.array(y_train)
        # Reshape the data into the shape accepted by the LSTM
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
        model.add(LSTM(units=50, return_sequences=False))
        model.add(Dense(units=25))
        model.add(Dense(units=1))
        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(x_train, y_train, batch_size=1, epochs=1)
        # Test data set
        test_data = scaled_data[training_data_len - 60:, :]
        # Create the x_test and y_test data sets
        x_test = []
        y_test = dataset[training_data_len:, :]
        # Get all of the rows from index 1603 to the rest and all of the columns (in this case it's only column 'Close'), so 2003 - 1603 = 400 rows of data
        for i in range(60, len(test_data)):
            x_test.append(test_data[i - 60:i, 0])
        x_test = np.array(x_test)
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
        predictions = model.predict(x_test)
        predictions = scaler.inverse_transform(predictions)
        rmse = np.sqrt(np.mean((predictions - y_test) ** 2))
        # Plot/Create the data for the graph
        train = data[:training_data_len]
        valid = data[training_data_len:]
        valid['Predictions'] = predictions

        new_df = company_quote.filter(['Close'])
        # Get the last 60 day closing price
        last_60_days = new_df[-60:].values
        # Scale the data to be values between 0 and 1
        last_60_days_scaled = scaler.transform(last_60_days)
        # Create an empty list
        X_test = []
        # Append teh past 60 days
        X_test.append(last_60_days_scaled)
        # Convert the X_test data set to a numpy array
        X_test = np.array(X_test)
        # Reshape the data
        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
        # Get the predicted scaled price
        pred_price = model.predict(X_test)
        # undo the scaling
        pred_price = scaler.inverse_transform(pred_price)
        # get last week price
        lastweek_price=new_df[-7:].values
        lastweek_ave=sum(lastweek_price)/7
        return train,valid,pred_price,lastweek_ave
    #返回值中，train是训练数据，valid是有效数据和预测数据，pred——price是预测明天的价格，lastweek_ave是上周平均价格

    def pltstock(self,train,valid,name):
        #画图
        #传入参数train是训练数据，valid是有效数据和预测数据,name是股票代码
        plt.figure(figsize=(16, 8))
        plt.title(name,fontsize=18)
        plt.xlabel('Date', fontsize=18)
        plt.ylabel('Close Price', fontsize=18)
        plt.plot(train['Close'])
        plt.plot(valid[['Close', 'Predictions']])
        plt.legend(['Train', 'Val', 'Predictions'], loc='lower right')
        return plt
    #返回图像结果

    def forecasestock(self,pred_price,name):
        #生成关于预测明天价格的语句
        #pred——price是预测明天的价格，name股票代码
        str_last = "%s预计明天的价格是 %d" % (name, pred_price)
        return str_last
    #返回关于预测价格的语句

    def remark(self,pred_price,lastweek_ave):
        #生成关于股票近期表现情况的评语
        #pred——price是预测明天的价格，lastweek_ave是上周平均价格
        if lastweek_ave*1.2<pred_price:
            myremark='AAA'
            specialremark='强烈推荐买入'
        elif lastweek_ave*1.1<pred_price:
            myremark='AA'
            specialremark ='推荐买入'
        elif lastweek_ave<=pred_price:
            myremark='A'
            specialremark ='可以考虑选择'
        elif pred_price*1.2<lastweek_ave:
            myremark='B'
            specialremark ='极不推荐买入，请谨慎考虑风险'
        elif pred_price*1.1<lastweek_ave:
            myremark='BB'
            specialremark ='不推荐买入，请谨慎考虑风险'
        else:
            myremark='BBB'
            specialremark ='可以考虑但不推荐，请谨慎考虑风险'
        myremark="股票评级为%s" %(myremark)+specialremark
        return myremark
    #返回myremark时关于股票情况的评语和评级


def main():

    name = input("请输入公司对应的股票代码：")
    stock1=Stock_e(name)
    train,valid,pred_price,lastweek_ave=stock1.get_train(name)
    myplt=stock1.pltstock(train,valid,name)
    myforecast=stock1.forecasestock(pred_price,name)
    stockremark=stock1.remark(pred_price,lastweek_ave)
    #展示
    #myplt为图片
    myplt.savefig('stock.jpg')
    print(myforecast)  #myforecast为估计价格
    print(stockremark)  #stockremark为评估级别和评语


if __name__ == "__main__":
    main()
