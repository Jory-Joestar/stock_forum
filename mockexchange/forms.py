
from django import forms
from mockexchange.models import *
from extends.data import stock_basic
import time
import tushare as ts


class CommissionForm(forms.ModelForm):
    token = 'c89761557a8c339b857a2fedebea03685aee396dd2501d063d7271fd'
    ts.set_token(token)
    pro = ts.pro_api(token)

    date = forms.CharField(widget=forms.HiddenInput(), initial=time.strftime("%Y%m%d", time.localtime()))
    time1 = forms.CharField(widget=forms.HiddenInput(), initial=time.strftime("%H:%M:%S", time.localtime()))
    code = forms.CharField(max_length=128, help_text="输入代码")
    name = forms.CharField(widget=forms.HiddenInput(), initial='None')
    operation = forms.CharField(widget=forms.HiddenInput(), initial='None')
    note = forms.CharField(widget=forms.HiddenInput(), initial='未成交')
    amount = forms.IntegerField(initial=0, help_text="输入数量")
    price = forms.FloatField(initial=0, help_text="输入价格")
    index = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Commission
        exclude=['user']


class CancelCommission(forms.ModelForm):
    index = forms.IntegerField(initial=0, help_text='输入委托序号')

    class Meta:
        model = Commission
        fields = ('index', )

