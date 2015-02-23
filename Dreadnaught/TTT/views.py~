from django.shortcuts import HttpResponse
from TTT.models import pending_games, game_results
from game import play


def index(request):
    #results = play_game()
    #return HttpResponse(results)
    a = pending_games(name = "a")
    a.save()
    firstai = 'ai1.py'
    secondai = 'ai2.py'
    
    results = play(a.id, firstai, secondai)
    return HttpResponse(results)
