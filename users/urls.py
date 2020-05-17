'''为应用程序users定义URL模式'''
from django.conf.urls import url
from django.contrib.auth.views import LoginView

from . import views

urlpatterns=[
    #登陆页面
    url(r'^login/$',LoginView.as_view(template_name='users/login.html'),
    name='login'),
    #注销
    url(r'^logout/$',views.logout_view,name='logout'),
    #注册页面
    url(r'^register/$',views.register,name='register'),
    #用户个人中心页面
    url(r'^user_space/(?P<user_id>\d+)/$',views.user_space,name='user_space'),
    #用户个人资料
    url(r'^user_information/(?P<user_id>\d+)/$',views.user_information,name='user_information'),
    #用户关注页面
    url(r'^user_following/(?P<profile_id>\d+)/$',views.user_following,name='user_following'),
    #用户文章管理
    url(r'^user_post/(?P<user_id>\d+)/$',views.user_post,name='user_post'),
    #用户板块管理
    url(r'^user_plate/(?P<user_id>\d+)/$',views.user_plate,name='user_plate'),
    #用户撰写个人日志
    url(r'^private_post/$',views.private_post,name='private_post'),
    #用户管理个人日志
    url(r'^show_private_post/(?P<user_id>\d+)/$',views.show_private_post,name='show_private_post'),
]