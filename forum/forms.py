from django import forms
from .models import Plate,Post,Comment

class PlateForm(forms.ModelForm):
    class Meta:
        model=Plate
        fields=['text']
        labels={'text':''}
        widgets={'text':forms.Textarea(attrs={'class':'span11','cols':60,'rows':2}),}

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['title','text']
        labels={'title':'','text':''}
        widgets={'title':forms.Textarea(attrs={'class':'span11','cols':60,'rows':2}),
        'text':forms.Textarea(attrs={'class':'span11','cols':60,'rows':12}),}

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['text']
        labels={'text':''}
        widgets={
            'text':forms.Textarea(attrs={'class':"span8",'name':"comment",'id':"comment",'cols':58 ,'rows':10})
        }

class GetpriceForm(forms.Form):
    stock_name = forms.CharField(label='股票名称', max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}))
    date = forms.DateField(label='日期', widget=forms.DateInput(attrs={'type':'date'}))

#按名称搜索股票的表单
class GetstockForm(forms.Form):
    stock_name = forms.CharField(label='', max_length=10, widget=forms.TextInput(attrs={'class': 'span8'}))

#获取日期区间
class GetgapForm(forms.Form):
    start_date=forms.DateField(label='起始日期', widget=forms.DateInput(attrs={'type':'date'}))
    end_date=forms.DateField(label='截止日期', widget=forms.DateInput(attrs={'type':'date'}))