from django.contrib import admin
from TTT.models import pending_games, game_results

# Register your models here.
admin.site.register(pending_games)
admin.site.register(game_results)
