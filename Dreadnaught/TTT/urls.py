from django.conf.urls import patterns, url

from TTT import views

urlpatterns = patterns('',
    url(r'^play_game$', views.select_ai, name='play_game'),
    url(r'^selectai$', views.select_ai, name='select_ai'),
    url(r'^play_game$', views.select_ai, name='play_game'),
    url(r'^$', views.home, name='home'),
    url(r'^home/$', views.home, name='home'),
    url(r'^uploads$', views.uploads, name='uploads'),
    url(r'^uploads/$', views.uploads, name='uploads'),
    url(r'^lobby$', views.game_lobby, name='game_lobby'),
)
