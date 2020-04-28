'''定义forum的URL模式'''
from django.conf.urls import url
from . import views
urlpatterns=[
    #主页
    url(r'^$',views.index,name='index'),
    #显示所有的板块
    url(r'^plates/$',views.plates,name='plates'),
    #特定板块的详细页面
    url(r'^plates/(?P<plate_id>\d+)/$',views.plate,name='plate'),
    #用于添加新板块的网页
    url(r'^new_plate/$',views.new_plate,name='new_plate'),
    #用于添加新文章的页面
    url(r'^new_post/(?P<plate_id>\d+)/$',views.new_post,name='new_post'),
    #显示当前文章所有评论的页面
    url(r'^show_comments/(?P<post_id>\d+)/$',views.show_comments,name='show_comments'),
    #编写评论回复页面
    url(r'^response_comment/(?P<comment_id>\d+)/$',views.response_comment,name='response_comment'),
    #编写评论页面
    url(r'^new_comment/(?P<post_id>\d+)/$',views.new_comment,name='new_comment'),
    #显示所有动态的页面
    url(r'^show_dynamic/$',views.show_dynamic,name='show_dynamic'),
    #删除某条评论
    url(r'^del_comment/(?P<comment_id>\d+)/$',views.del_comment,name='del_comment'),
    #删除某条文章
    url(r'^del_post/(?P<post_id>\d+)/$',views.del_post,name='del_post'),
    #查询股票价格
    url(r'^get_stock_price/$',views.get_stock_price,name='get_stock_price'),
    #测试展示南京银行K线图
    #url(r'^get_nj_bank_test/$', views.nj_bank_test, name='get_nj_bank_test'),
]