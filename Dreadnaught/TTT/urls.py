from django.conf.urls import patterns, url

from TTT import views
from TTT import game

urlpatterns = patterns('',
    url(r'^select_game$', game.select_game, name='select_game'),
    url(r'^select_game/$', game.select_game, name='select_game'),
    url(r'^play_game$', game.play_game, name='play_game'),
    url(r'^play_game/$', game.play_game, name='play_game'),
    url(r'^checkers_test$', views.checkers_test, name='checkers_test'),
    url(r'^checkers_test/$', views.checkers_test, name='checkers_test'),
    url(r'^$', views.home, name='home'),
    url(r'^home/$', views.home, name='home'),
    url(r'^uploads$', views.uploads, name='uploads'),
    url(r'^uploads/$', views.uploads, name='uploads'),
    url(r'^lobby$', views.game_lobby, name='game_lobby'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^view_script_list$', views.user_script_list, \
        name='View Script List'),
    url(r'^view_script_list/(\d+)/$', views.view_script, name='View Script'),
    url(r'^view_script_games/(\d+)/$', views.view_script_games, \
        name='View Script Games'),
    url(r'^game_results/(\d+)/$', views.game_results, \
        name='Game Results'),
    url(r'^profile/$', views.profile, \
        name='Game Results'),
    url(r'^change_password/$', views.change_pass, \
        name='Change Password'),
)
