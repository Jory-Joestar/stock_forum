from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Plate(models.Model):
    '''论坛的板块'''
    text=models.CharField(max_length=200)
    date_added=models.DateTimeField(auto_now_add=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        '''返回模型的字符串表示'''
        return self.text

class Post(models.Model):
    '''用户发表的帖子'''
    plate=models.ForeignKey(Plate,on_delete=models.CASCADE)
    text=models.TextField()
    date_added=models.DateTimeField(auto_now_add=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural='posts'
    
    def __str__(self):
        '''返回模型的字符串表示'''
        return self.text[:50]+"..."

class Comment(models.Model):
    '''对于某条帖子的评论'''
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    text=models.TextField()
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''返回模型的字符串表示'''
        return self.text

class Information(models.Model):
    '''主页公告，仅超级管理员编辑'''
    text=models.TextField()
    date_added=models.DateTimeField(auto_now_add=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.text