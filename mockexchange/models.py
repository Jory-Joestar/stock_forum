from django.db import models
from users.models import UserProfile

'''
#这是测试版的对应user，交易参与者全部关联到userprofile类
class MockUser(models.Model):
    name = models.CharField(max_length=128, unique=True)
    cash = models.FloatField(default=200000)
    capital = models.FloatField(default=200000)

    def __str__(self):
        return self.name
'''


class Commission(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date = models.CharField(max_length=128, default='')
    time1 = models.CharField(max_length=128, default='')
    code = models.CharField(max_length=128, default='')
    name = models.CharField(max_length=128, default='')
    operation = models.CharField(max_length=128, default='')
    note = models.CharField(max_length=128, default='')
    amount = models.FloatField(default=0)
    price = models.FloatField(default=0)
    index = models.IntegerField(default=0)

    def __str__(self):
        return self.user.owner.username


class Deal(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date = models.CharField(max_length=128, default='')
    time1 = models.CharField(max_length=128, default='')
    code = models.CharField(max_length=128, default='')
    name = models.CharField(max_length=128, default='')
    operation = models.CharField(max_length=128, default='')
    amount = models.FloatField(default=0)
    price = models.FloatField(default=0)
    poundage = models.FloatField(default=0)
    stamp_tax = models.FloatField(default=0)

    def __str__(self):
        return self.user.owner.username


class OwnedStock(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    code = models.CharField(max_length=128, default='')
    name = models.CharField(max_length=128, default='')
    whole_balance = models.FloatField(default=0)
    available_balance = models.FloatField(default=0)
    blocked_balance = models.FloatField(default=0)
    thisday_blocked_balance = models.FloatField(default=0)
    cost = models.FloatField(default=1)
    price = models.FloatField(default=0)
    profit = models.FloatField(default=0)
    profit_proportion = models.FloatField(default=0)
    market_value = models.FloatField(default=0)
    whole_buy = models.FloatField(default=0)
    whole_sell = models.FloatField(default=0)

    def __str__(self):
        return self.user.owner.username
