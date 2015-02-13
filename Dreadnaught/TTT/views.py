from django.shortcuts import HttpResponse
#import game


def index(request):
    #results = play_game()
    #return HttpResponse(results)
    
    return HttpResponse("This is the index page")
