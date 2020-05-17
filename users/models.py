from django.db import models
from django.contrib.auth.models import User
from forum.models import Plate,Post
# Create your models here.

class UserProfile(models.Model):
    owner = models.OneToOneField(User,on_delete=models.CASCADE)
    following_post = models.ManyToManyField(Post)
    following_plate = models.ManyToManyField(Plate)
    #用户可以补充的资料
    #工作
    job=models.CharField(max_length=10,blank=True,null=True)
    #性别 0是female,1是male，可以为空
    gender=models.IntegerField(null=True,blank=True,choices=((0,'女'),(1,'男'),(2,'无')))
    #头像
    picture=models.ImageField(upload_to='profile_images',blank=True,null=True)

    def __str__(self): 
        return self.auth.username

class FollowingStocks(models.Model):
    '''
    用来储存用户关注的股票名称列表
    '''
    stocks=models.CharField(max_length=200)
    owner=models.OneToOneField(UserProfile,on_delete=models.CASCADE,null=True)

    def get_stock_list(self):
        if self.stocks=='':
            return []
        else:
            return self.stocks.split(',')

    def stock_exist(self,stock):
        '''检查股票是否在用户关注的股票列表里'''
        stocklist=self.get_stock_list()
        if stock in stocklist:
            return True
        else:
            return False

    def add_stock(self,stock):
        '''添加关注的股票'''
        stocklist=self.get_stock_list()
        if stock not in stocklist:
            stocklist.append(stock)
            self.stocks=','.join(stocklist)
            return True
        else:
            return False

    def remove_stock(self,stock):
        '''取消关注某股票'''
        stocklist=self.get_stock_list()
        if stock in stocklist:
            stocklist.remove(stock)
            self.stocks=','.join(stocklist)
            return True
        else:
            return False


