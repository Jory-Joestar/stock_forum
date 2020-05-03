from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile,FollowingStocks,User
from forum.models import Plate,Post
from .models import UserProfile
#使用中间件时，有些视图可能不需要设置X-Frame-Options标头。对于这些情况，可以使用视图装饰器告知中间件不要设置标头
from django.views.decorators.clickjacking import xframe_options_exempt

# Create your views here.
def logout_view(request):
    '''注销用户'''
    logout(request)
    return HttpResponseRedirect(reverse('forum:index'))

def register(request):
    '''注册新用户'''
    if request.method!="POST":
        #显示空的注册表单
        form=UserCreationForm()
    else:
        #处理填写好的表单
        form=UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user=form.save()
            #新建与当前用户相关联的userprofile对象
            new_user_profile=UserProfile()
            new_user_profile.owner=new_user
            new_user_profile.save()
            #新建与当前用户相关两的股票关注列表对象
            new_following_stocks=FollowingStocks()
            new_following_stocks.owner=new_user_profile
            new_following_stocks.stocks=''
            new_following_stocks.save()
            #让用户自动登陆，再重定向到主页
            authenticated_user=authenticate(username=new_user.username,
            password=request.POST['password1'])
            login(request,authenticated_user)
            return HttpResponseRedirect(reverse('forum:index'))
    context={'form':form}
    return render(request,'users/register.html',context)

@login_required
def user_space(request):
    '''用户个人中心主页面的视图函数'''
    user=request.user
    profile=UserProfile.objects.get(owner=user)
    context={'user':user,
             'profile':profile,
             }
    return render(request,'users/user_space.html',context)

#提供嵌套页面用的视图需要加上这个修饰器，不然请求会被拒绝！
@xframe_options_exempt
def user_information(request,user_id):
    '''个人中心里显示个人信息的子页面'''
    user=User.objects.get(id=user_id)
    context={'user':user}
    return render(request,'users/user_information.html',context)

@xframe_options_exempt
def user_following(request,profile_id):
    '''个人中心里显示用户关注的股票、文章、板块的子页面'''
    #首先通过profile_id获取profile对象
    profile=UserProfile.objects.get(id=profile_id)
    #接着获取三个关注列表
    following_post=profile.following_post.all()
    following_plate=profile.following_plate.all()
    following_stocks=FollowingStocks.objects.get(owner=profile)
    stock_list=following_stocks.get_stock_list()
    context={'following_post':following_post,'following_plate':following_plate,'stock_list':stock_list}
    return render(request,'users/user_following.html',context)

@xframe_options_exempt
def user_post(request,user_id):
    '''个人中心里管理用户文章的子页面'''
    user=User.objects.get(id=user_id)
    #获取owner为当前用户的文章对象列表
    posts=Post.objects.filter(owner=user)
    context={'posts':posts}
    return render(request,'users/user_post.html',context)

@xframe_options_exempt
def user_plate(request,user_id):
    '''个人中心里管理用户文章的子页面'''
    user=User.objects.get(id=user_id)
    #获取owner为当前用户的板块对象列表
    plates=Plate.objects.filter(owner=user)
    context={'plates':plates}
    return render(request,'users/user_plate.html',context)

