from django import forms
from .models import Plate,Post,Comment

class PlateForm(forms.ModelForm):
    class Meta:
        model=Plate
        fields=['text']
        labels={'text':''}

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['text']
        labels={'text':''}
        widgets={'text':forms.Textarea(attrs={'cols':80})}

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['text']
        labels={'text':''}

class GetpriceForm(forms.Form):
    stock_name = forms.CharField(label='股票名称', max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}))
    date = forms.DateField(label='日期', widget=forms.DateInput(attrs={'type':'date'}))