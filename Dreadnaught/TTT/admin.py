from django.contrib import admin
from TTT.models import pending_games, game_results, users, scripts, game

# Register your models here.
admin.site.register(users)
admin.site.register(scripts)
admin.site.register(game)
admin.site.register(pending_games)
admin.site.register(game_results)
