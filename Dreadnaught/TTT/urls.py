from django.conf.urls import patterns, url

from TTT import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^uploads$', views.uploads, name='uploads'),
    url(r'^uploads/$', views.uploads, name='uploads'),
    url(r'^lobby$', views.game_lobby, name='game_lobby'),
)
