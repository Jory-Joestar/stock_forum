from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserForm(forms.ModelForm):
    password1 = forms.CharField(label="Password",widget=forms.PasswordInput())
    password2 = forms.CharField(label="Password confirmation",widget=forms.PasswordInput())
    username = forms.CharField(label="Username",max_length=10,error_messages={})
    class Meta:
        model = User
        fields = ("username",)

class UserProfileForm(forms.ModelForm):
    ''' 定义用户编辑个人资料的表单 '''
     #工作
    job=forms.CharField(max_length=10,required=False,label='职业')
    #性别 0是female,1是male，可以为空
    #gender=forms.IntegerField(required=False,label='性别')
    gender=forms.fields.TypedChoiceField(required=False,label='性别',coerce=lambda x: int(x),choices=((2,'无'),(0,'女'),(1,'男')))
    #头像
    picture=forms.ImageField(required=False,label='头像')

    class Meta:
        model=UserProfile
        fields=['job','gender','picture']