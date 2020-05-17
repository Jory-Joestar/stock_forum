from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile,FollowingStocks,User
from forum.models import Plate,Post
from .models import UserProfile
from .forms import UserForm,UserProfileForm
from django.contrib.auth.models import User
#使用中间件时，有些视图可能不需要设置X-Frame-Options标头。对于这些情况，可以使用视图装饰器告知中间件不要设置标头
from django.views.decorators.clickjacking import xframe_options_exempt

# Create your views here.
def logout_view(request):
    '''注销用户'''
    logout(request)
    return HttpResponseRedirect(reverse('forum:index'))

def register(request):
    '''注册新用户'''
    info=None
    if request.method!="POST":
        #显示空的注册表单
        form=UserForm()
    else:
        #处理填写好的表单
        form=UserForm(data=request.POST)
        if form.is_valid():
            if form.cleaned_data['password1'] == form.cleaned_data['password2']:
                new_user=form.save()
                new_user.set_password(form.cleaned_data['password1'])
                new_user.save()
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
            else:
                info='两次密码输入不同'
    context={'form':form,'info':info}
    return render(request,'users/register.html',context)

@login_required
def user_space(request,user_id):
    '''用户个人中心主页面的视图函数'''
    user=User.objects.get(id=user_id)
    profile=UserProfile.objects.get(owner=user)
    context={'selecteduser':user,
             'profile':profile,
             }
    return render(request,'users/user_space.html',context)

#提供嵌套页面用的视图需要加上这个修饰器，不然请求会被拒绝！
@xframe_options_exempt
def user_information(request,user_id):
    '''个人中心里显示个人信息的子页面'''
    user=User.objects.get(id=user_id)
    userprofile=UserProfile.objects.get(owner=user)
    form=UserProfileForm({'job':userprofile.job,'picture':userprofile.picture,
                        'gender':userprofile.gender})
    if request.method=='POST':
        form=UserProfileForm(request.POST,request.FILES,instance=userprofile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:user_information',args=[user_id]))
        else:
            print(form.errors)
    context={'selecteduser':user,'userprofile':userprofile,'form':form}
    return render(request,'users/user_information.html',context)

@xframe_options_exempt
def user_following(request,profile_id):
    '''个人中心里显示用户关注的股票、文章、板块的子页面'''
    #首先通过profile_id获取profile对象
    profile=UserProfile.objects.get(id=profile_id)
    user=profile.owner
    #接着获取三个关注列表
    following_post=profile.following_post.all()
    following_plate=profile.following_plate.all()
    following_stocks=FollowingStocks.objects.get(owner=profile)
    stock_list=following_stocks.get_stock_list()
    context={'following_post':following_post,'following_plate':following_plate,'stock_list':stock_list,'selecteduser':user}
    return render(request,'users/user_following.html',context)

@xframe_options_exempt
def user_post(request,user_id):
    '''个人中心里管理用户文章的子页面'''
    user=User.objects.get(id=user_id)
    #获取owner为当前用户的文章对象列表
    #用plate__text获得关联的plate类的属性，注意是双下划线
    posts=Post.objects.exclude(plate__text='__private__').filter(owner=user)
    context={'posts':posts,'selecteduser':user}
    return render(request,'users/user_post.html',context)

@xframe_options_exempt
def user_plate(request,user_id):
    '''个人中心里管理用户板块的子页面'''
    user=User.objects.get(id=user_id)
    #获取owner为当前用户的板块对象列表
    plates=Plate.objects.filter(owner=user)
    context={'plates':plates,'selecteduser':user}
    return render(request,'users/user_plate.html',context)

@xframe_options_exempt
def show_private_post(request,user_id):
    '''显示用户的个人日志'''
    user=User.objects.get(id=user_id)
    #获取用户的个人日志列表
    posts=Post.objects.filter(plate__text='__private__').filter(owner=user)
    context={'posts':posts,'selecteduser':user}
    return render(request,'users/show_private_post.html',context)

def private_post(request):
    '''将用户编辑个人日志的请求重定向到文章编辑页面'''
    private_plate=None
    try:
        private_plate=Plate.object.get(text='__private__')
    except:
        private_plate=Plate()
        private_plate.text='__private__'
        private_plate.save()
    return HttpResponseRedirect(reverse('forum:new_post',
            args=[private_plate.id]))