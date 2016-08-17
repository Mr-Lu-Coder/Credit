__author__ = 'lushangqi'
from django.conf.urls import patterns,url
from credit import views
urlpatterns = patterns('',
    url(r'^$', views.login, name = 'login'),
    url(r'^login/$', views.login, name = 'login'),
    url(r'^index/$', views.index, name = 'index'),
    #url(r'^debug/$', views.debug, name = 'debug'),
)