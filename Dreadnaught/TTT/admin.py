from django.contrib import admin
from TTT.models import users, scripts, game, turns, moves

# Register your models here.
admin.site.register(users)
admin.site.register(scripts)
admin.site.register(game)
admin.site.register(turns)
admin.site.register(moves)
