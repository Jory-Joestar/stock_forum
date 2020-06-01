from django.shortcuts import render
from django.http import HttpResponseRedirect,Http404,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Plate,Post,Comment,Information
from .forms import PlateForm,PostForm,CommentForm,GetpriceForm,GetstockForm,GetgapForm
from extends.get_price import GetPrice
from extends.get_est import GetEst
#from extends.get_stock_index import draw_index
#使用中间件时，有些视图可能不需要设置X-Frame-Options标头。对于这些情况，可以使用视图装饰器告知中间件不要设置标头
from django.views.decorators.clickjacking import xframe_options_exempt
from users.models import UserProfile,FollowingStocks,User
#对话框返回信息
from django.contrib import messages
import datetime


# Create your views here.
def index(request):
    '''论坛的主页'''
    #画指数图
    #draw_index()
    #获取所有板块
    plates=Plate.objects.all().exclude(text='__private__')
    #获取前10名最热板块
    hot_plates=plates.order_by('-hot')[:10]
    #获得精选文章
    hot_posts=Post.objects.all().exclude(plate__text='__private__').order_by('id')[:5]
    #资产排行榜
    capital_rank_list = UserProfile.objects.all().order_by('-capital')[:5]
    if request.method == 'POST':
        if 'search_plate' in request.POST:
            plate_name=request.POST['search_item']
            return HttpResponseRedirect(reverse('forum:search_plate',args=[plate_name]))
        elif 'search_post' in request.POST:
            post_name=request.POST['search_item']
            return HttpResponseRedirect(reverse('forum:search_post_all',args=[post_name]))
        elif 'search_stock' in request.POST:
            stock_name=request.POST['search_item']
            return HttpResponseRedirect(reverse('forum:get_stock_result',args=[stock_name]))
    informations=Information.objects.all().order_by('-date_added')
    context={'informations':informations,'hot_plates':hot_plates,'hot_posts':hot_posts,'capital_rank_list':capital_rank_list,}
    return render(request,'forum/index.html',context)

#@login_required
def plates(request):
    '''显示论坛所有板块'''
    #获取所有板块
    plates=Plate.objects.all().exclude(text='__private__')
    #获取前10名最热板块
    hot_plates=plates.order_by('-hot')[:10]
    #获取国内市场板块
    domestic=plates.filter(market=0)
    domestic_num=len(domestic)
    domestic=[domestic[i:i + 4] for i in range(0, domestic_num, 4)]
    #获取海外市场板块
    foreign=plates.filter(market=1)
    foreign_num=len(foreign)
    foreign=[foreign[i:i + 4] for i in range(0, foreign_num, 4)]
    #获取其他类型板块
    others=plates.filter(market=2)
    others_num=len(others)
    others=[others[i:i + 4] for i in range(0, others_num, 4)]
    if request.user.is_authenticated:
        profile=UserProfile.objects.get(owner=request.user)
        #获得当前用户关注的板块
        following_plates=profile.following_plate.all()
        #获取当前用户创建的板块
        owned_plates=Plate.objects.filter(owner=request.user)
    else:
        following_plates=None
        owned_plates=None
    context={'hot_plates':hot_plates,'domestic':domestic,'foreign':foreign,
            'others':others,'following_plates':following_plates,'owned_plates':owned_plates,
            'domestic_num':domestic_num,'foreign_num':foreign_num,'others_num':others_num}
    return render(request,'forum/plates.html',context)

@login_required
def plate(request,plate_id):
    '''显示某板块内的所有po文'''
    plate=Plate.objects.get(id=plate_id)
    #获取用户对于当前板块的关注状态
    user=request.user
    profile=UserProfile.objects.get(owner=user)
    followed=False
    if plate in profile.following_plate.all():
        followed=True
    else:
        followed=False
    #确认请求的主题及其所有的条目
    posts=Post.objects.filter(plate=plate).order_by('-date_added')
    context={'plate':plate,'posts':posts,'followed':followed}
    return render(request,'forum/plate.html',context)

@login_required
def new_plate(request):
    '''添加新板块'''
    if request.method!='POST':
        #未提交数据：创建一个新表单
        form=PlateForm()
    else:
        #POST提交的数据，对数据进行处理
        form=PlateForm(request.POST)
        if form.is_valid():
            new_topic=form.save(commit=False)
            new_topic.owner=request.user
            new_topic.market=request.POST['market']
            new_topic.save()
            return HttpResponseRedirect(reverse('forum:plates'))
    context={'form':form}
    return render(request,'forum/new_plate.html',context)

@login_required
def new_post(request,plate_id):
    '''在特定的板块中添加新文章'''
    plate=Plate.objects.get(id=plate_id)
    if request.method!="POST":
        #未提交数据，创建一个空表单
        form=PostForm()
    else:
        #POST提交的数据，对数据进行处理
        form=PostForm(data=request.POST)
        if form.is_valid():
            new_post=form.save(commit=False)
            new_post.plate=plate
            new_post.owner=request.user
            new_post.save()
            if plate.text=='__private__':
                return HttpResponseRedirect(reverse('users:user_space',args=[request.user.id]))
            else:
                return HttpResponseRedirect(reverse('forum:plate',args=[plate_id]))
    context={'plate':plate,'form':form}
    return render(request,'forum/new_post.html',context)


@login_required
def show_post(request,post_id):
    '''文章详情页面，显示文章内容，文章的所有评论，添加评论，回复'''
    post=Post.objects.get(id=post_id)
    plate=post.plate
    #获取用户的关注状态
    user=request.user
    profile=UserProfile.objects.get(owner=user)
    followed=False
    if post in profile.following_post.all():
        followed=True
    else:
        followed=False
    comments=Comment.objects.filter(post=post).order_by('-date_added')
    #处理添加评论
    if request.method!='POST':
        #未提交评论，创建一个空表单
        form=CommentForm()
    else:
        #POST提交的数据，对数据进行处理
        form=CommentForm(data=request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.post=post
            new_comment.owner=request.user
            new_comment.save()
            return HttpResponseRedirect(reverse('forum:show_post',
            args=[post.id]))
    context={'post':post,'comments':comments,'plate':plate,'followed':followed,'form':form}
    return render(request,'forum/show_post.html',context)


@login_required
def new_comment(request,post_id):
    '''添加评论'''
    post=Post.objects.get(id=post_id)
    if request.method!='POST':
        #未提交评论，创建一个空表单
        form=CommentForm()
    else:
        #POST提交的数据，对数据进行处理
        form=CommentForm(data=request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.post=post
            new_comment.owner=request.user
            new_comment.save()
            return HttpResponseRedirect(reverse('forum:show_post',
            args=[post.id])) 
    context={'post':post,'form':form}
    return render(request,'forum/new_comment.html',context)

@login_required
def response_comment(request,comment_id):
    '''回复评论'''
    comment=Comment.objects.get(id=comment_id)
    post=comment.post
    if request.method!='POST':
        #未提交回复，创建空评论
        form=CommentForm()
    else:
        #initial={'text':str(comment.text)+'\nresponse:\n'}
        #POST提交的数据，对数据进行处理
        form=CommentForm(data=request.POST)
        if form.is_valid():
            new_response=form.save(commit=False)
            new_response.post=post
            new_response.owner=request.user
            new_response.text='回复：'+new_response.text+'\n------------------ Original ------------------\n'+str(comment.owner)+':'+comment.text
            new_response.save()
            return HttpResponseRedirect(reverse('forum:show_post',
            args=[post.id]))
    context={'comment':comment,'form':form,'post':post}
    return render(request,'forum/response_comment.html',context)

@login_required
def show_dynamic(request):
    '''显示动态'''
    posts=Post.objects.all().exclude(plate__text='__private__').order_by('-date_added')
    context={'posts':posts}
    return render(request,'forum/show_dynamic.html',context)

@login_required
def del_comment(request,comment_id):
    '''删除一条评论'''
    comment=Comment.objects.get(id=comment_id)
    post=comment.post
    if comment.owner==request.user or post.owner==request.user:
        comment.delete()
        info='评论删除成功！'
    else:
        info='评论删除失败。 没有删除权限。'
    context={'info':info,'post':post}
    return render(request,'forum/del_comment.html',context)

@login_required
def del_plate(request,plate_id):
    '''删除板块'''
    plate=Plate.objects.get(id=plate_id)
    if plate.owner==request.user:
        plate.delete()
        messages.success(request,"删除成功")
    else:
        messages.success(request,"删除失败，没有权限")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def del_post(request,post_id):
    '''删除文章'''
    post=Post.objects.get(id=post_id)
    plate=post.plate
    if post.owner==request.user:
        post.delete()
        messages.success(request,"删除成功")
    else:
        messages.success(request,"删除失败，没有权限")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def get_stock_price(request):
    '''查询股票价格'''
    result=''
    if request.method!='POST':
        #未提交查询内容，创建一个空表单
        form=GetpriceForm()
    else:
        #POST提交的数据，对数据进行处理
        form=GetpriceForm(data=request.POST)
        if form.is_valid():
            name=form.cleaned_data['stock_name']
            date=form.cleaned_data['date'].strftime('%Y%m%d')
            refer=GetPrice()
            result=refer.by_name(name,date)
            if not result.values.tolist():
                result='没有找到当天关于“'+name+'”的价格信息'
            else:
                title='    '.join(result.columns.values.tolist())
                value='    '.join([str(i) for i in result.values.tolist()[0]])
                result=title+'\n'+value
    context={'form':form,'result':result}
    return render(request,'forum/get_stock_price.html',context)

@login_required
def get_stock(request):
    '''查询股票视图'''
    if request.method != 'POST':
        form = GetstockForm()
    else:
        form = GetstockForm(data=request.POST)
        if form.is_valid():
            stock_name = form.cleaned_data['stock_name']
            return HttpResponseRedirect(reverse('forum:get_stock_result', args=[stock_name]))

    context = {'form': form}
    return render(request, 'forum/get_stock.html', context)

@login_required
def get_stock_result(request,stock_name):
    '''查询结果页面'''
    refer=GetPrice()
    results=refer.get_related(stock_name)
    context={'results':results,}
    return render(request,'forum/get_stock_result.html',context)

def search_plate(request,plate_name):
    '''查询板块'''
    results=Plate.objects.exclude(text='__private__').filter(text__icontains=plate_name)
    context={'results':results}
    return render(request,'forum/search_plate.html',context)

def search_post_all(request,post_name):
    '''查询网站内所有的文章，不包括用户日志'''
    results=Post.objects.exclude(plate__text='__private__').filter(text__icontains=post_name)
    context={'results':results}
    return render(request,'forum/search_post_all.html',context)

@login_required
def stock_info(request,stock_name):
    '''股票详情页面'''

    #获取用户的关注状态
    user=request.user
    profile=UserProfile.objects.get(owner=user)
    following=FollowingStocks.objects.get(owner=profile)
    followed=False
    if following.stock_exist(stock_name):
        followed=True
    else:
        followed=False

    refer=GetPrice()
    result_price=refer.current_price(stock_name)
    stock_code=result_price[0]
    current_price=result_price[1]

    start_date=(datetime.date.today() + datetime.timedelta(days = -30)).strftime("%Y%m%d")
    end_date=(datetime.date.today() + datetime.timedelta(days = -1)).strftime("%Y%m%d")
    #end_date=datetime.datetime.now().strftime('%Y%m%d')
    print(start_date)
    print(end_date)
    refer.draw_kline(stock_name,start_date,end_date)

    context={'stock_name':stock_name,'current_price':current_price,'followed':followed,'stock_code':stock_code}
    return render(request,'forum/stock_info.html',context)

@xframe_options_exempt
def custom_kline(request,stock_name):
    '''用户自定时间段画k线图'''
    result=False
    info=''
    if request.method!='POST':
        #未提交查询内容，创建一个空表单
        form=GetgapForm()
    else:
        #POST提交的数据，对数据进行处理
        form=GetgapForm(data=request.POST)
        if form.is_valid():
            start_date=form.cleaned_data['start_date'].strftime('%Y%m%d')
            end_date=form.cleaned_data['end_date'].strftime('%Y%m%d')
            refer=GetPrice()
            if refer.draw_kline(stock_name,start_date,end_date)!='':
                result=True
            else:
                info='K线图导出失败'
    context={'form':form,'result':result,'info':info,'stock_name':stock_name}
    return render(request,'forum/custom_kline.html',context)

@login_required
def follow_plate(request,plate_id):
    '''关注板块'''
    user=request.user
    profile=UserProfile.objects.get(owner=user)
    plate=Plate.objects.get(id=plate_id)
    if plate in profile.following_plate.all():
        messages.success(request,"你已经关注了")
    else:
        profile.following_plate.add(plate)
        messages.success(request,"关注成功")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def unfollow_plate(request,plate_id):
    '''取消关注板块'''
    user=request.user
    profile=UserProfile.objects.get(owner=user)
    plate=Plate.objects.get(id=plate_id)
    if plate not in profile.following_plate.all():
        messages.success(request,"你并没有关注")
    else:
        profile.following_plate.remove(plate)
        messages.success(request,"成功取消关注")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def follow_post(request,post_id):
    '''关注文章'''
    user=request.user
    profile=UserProfile.objects.get(owner=user)
    post=Post.objects.get(id=post_id)
    if post in profile.following_post.all():
        messages.success(request,"你已经关注了")
    else:
        profile.following_post.add(post)
        messages.success(request,"关注成功")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def unfollow_post(request,post_id):
    '''取消关注文章'''
    user=request.user
    profile=UserProfile.objects.get(owner=user)
    post=Post.objects.get(id=post_id)
    if post not in profile.following_post.all():
        messages.success(request,"你并没有关注")
    else:
        profile.following_post.remove(post)
        messages.success(request,"成功取消关注")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def follow_stock(request,stock_name):
    '''关注某只股票'''
    #获取用户关注的股票列表对象
    user=request.user
    profile=UserProfile.objects.get(owner=user)
    following=FollowingStocks.objects.get(owner=profile)
    if following.add_stock(stock_name):
        print(following.get_stock_list())
        following.save()
        messages.success(request,"关注成功")
    else:
        messages.success(request,"关注失败")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def unfollow_stock(request,stock_name):
    '''取消关注某只股票'''
    #获取用户关注的股票列表对象
    user=request.user
    profile=UserProfile.objects.get(owner=user)
    following=FollowingStocks.objects.get(owner=profile)
    if following.remove_stock(stock_name):
        following.save()
        messages.success(request,"取消关注成功")
    else:
        messages.success(request,"取消关注失败")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def stock_est(request,stock_code):
    ''' 股票预测 '''
    esting=GetEst(stock_code)
    if esting.error:
        return HttpResponse(esting.error)
    esting.plot_trends()
    forecast=esting.forecast()
    remark=esting.remark()
    context={'forecast':forecast,'remark':remark,'stock_code':stock_code}
    return render(request,'forum/stock_est.html',context)