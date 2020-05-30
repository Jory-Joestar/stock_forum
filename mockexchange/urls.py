from django.conf.urls import url
from mockexchange import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^userinfo/$', views.userinfo, name='userinfo'),
    url(r'^buy/$', views.buy, name='buy'),
    url(r'^sell/$', views.sell, name='sell'),
    url(r'^cancel/$', views.cancel, name='cancel'),
    url(r'^newthread/$', views.newthread, name='newthread'),
]