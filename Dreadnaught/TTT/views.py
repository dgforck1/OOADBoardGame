from django.shortcuts import HttpResponse, render
from django.http import HttpResponseRedirect

from TTT.models import users, scripts, game
#from game import play
from game2 import play
from forms import UploadFileForm, SelectAI
from lobby import show_open_games

def save_script(s, n):
    currentuser = users.objects.get(pk=1)
        
    sc = scripts(user_id = currentuser, name = n)
    sc.save()
    
    path = '/home/student/Desktop/Ciss438/OOADBoardGame/Dreadnaught/TTT/scripts/%s%s.py' % (currentuser.user_name, sc.id)

    sc.location = path
    sc.save()

    with open(path, 'wb+') as destination:
        for chunk in s.chunks():
            destination.write(chunk)
    
'''
def play_game(request):
    a = pending_games(name = a)
    a.save()
    firstai = ai1.py
    secondai = ai2.py
    
    results = play(a.id, firstai, secondai)
    return HttpResponse(results)
'''

def uploads(request):    
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        
        #process data here
        if form.is_valid():        
            save_script(request.FILES['file'], request.POST['title'])
        
            return HttpResponseRedirect('.')

    else:
        form = UploadFileForm()

    return render(request, 'uploads.html', {'form': form})


def game_lobby(request):
    results = show_open_games()
    return HttpResponse(results)


def human_game(request):
    if request.method == 'POST':
        form = SelectAI(request.POST)

        if form.is_valid():
            ai1 = form.cleaned_data['ai1']

            g = game(ai1script = None, ai2script  = ai2)
            g.save()

            results = play(g)

            return HttpResponse(results)
    else:
        form = SelectAI()

    return render(request, 'human_game.html', {'form': form})



def home(request):
    results = get_home()
    return HttpResponse(results)


def select_ai(request):
    if request.method == 'POST':
        form = SelectAI(request.POST)

        if form.is_valid():
            #get ai1 id
            ai1 = form.cleaned_data['ai1']
            #get ai2 id
            ai2 = form.cleaned_data['ai2']
            #create game
            g = game(ai1script  = ai1, ai2script  = ai2   )
            g.save()
            #send game to play
            results = play(g)
            #return game string
            
            

            return HttpResponse(results)
    else:
        form = SelectAI()

    return render(request, 'selectai.html', {'form': form})

            



def get_home():
    string = '<!DOCTYPE html><html><head><title></title></head><body> \
    <ul> \
    <li><a href="uploads">Upload Scripts</a></li> \
    <li><a href="play_game">Play a game</a></li> \
    <li><a href="lobby">Game Lobby</a></li> \
    </ul></body></html>'

    return string
