from django.shortcuts import render
from django.http import HttpResponseRedirect,Http404,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Plate,Post,Comment,Information
from .forms import PlateForm,PostForm,CommentForm,GetpriceForm
from extends.get_price import GetPrice


# Create your views here.
def index(request):
    '''论坛的主页'''
    informations=Information.objects.all().order_by('-date_added')
    context={'informations':informations}
    return render(request,'forum/index.html',context)

@login_required
def plates(request):
    '''显示论坛所有板块'''
    plates=Plate.objects.all().order_by('date_added')
    context={'plates':plates}
    return render(request,'forum/plates.html',context)

@login_required
def plate(request,plate_id):
    '''显示某板块内的所有po文'''
    plate=Plate.objects.get(id=plate_id)
    #确认请求的主题及其所有的条目
    posts=Post.objects.filter(plate=plate).order_by('-date_added')
    context={'plate':plate,'posts':posts}
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
            return HttpResponseRedirect(reverse('forum:plate',args=[plate_id]))
    context={'plate':plate,'form':form}
    return render(request,'forum/new_post.html',context)


@login_required
def show_comments(request,post_id):
    '''评论页面，显示某文章的所有评论，添加评论，回复'''
    post=Post.objects.get(id=post_id)
    comments=Comment.objects.filter(post=post).order_by('-date_added')
    context={'post':post,'comments':comments}
    return render(request,'forum/show_comments.html',context)


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
            return HttpResponseRedirect(reverse('forum:show_comments',
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
            return HttpResponseRedirect(reverse('forum:show_comments',
            args=[post.id]))
    context={'comment':comment,'form':form,'entry':post}
    return render(request,'forum/response_comment.html',context)

@login_required
def show_dynamic(request):
    '''显示动态'''
    posts=Post.objects.all().order_by('-date_added')
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
def del_post(request,post_id):
    '''删除一条日志'''
    post=Post.objects.get(id=post_id)
    plate=post.plate
    if post.owner==request.user:
        post.delete()
        info='日志删除成功！'
    else:
        info='日志删除失败。 没有删除权限。'
    context={'info':info,'plate':plate}
    return render(request,'forum/del_post.html',context)

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

