from django.shortcuts import HttpResponse, render
from django.http import HttpResponseRedirect

from TTT.models import users, scripts, game
from game2 import play
from forms import *
from lobby import show_open_games

def save_script(s, n):
    currentuser = users.objects.get(pk=1)
        
    sc = scripts(user_id = currentuser, name = n)
    sc.save()
    
    path = '/home/student/Desktop/Ciss438/OOADBoardGame/Dreadnaught/TTT/scripts/%s%s.py' % (currentuser.user_name, sc.id)
    #path = '/home/student/CISS438/OOADBoardGame/Dreadnaught/TTT/scripts/%s%s.py' % (currentuser.user_name, sc.id)

    sc.location = path
    sc.save()

    with open(path, 'wb+') as destination:
        for chunk in s.chunks():
            destination.write(chunk)

def uploads(request):    
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        
        #process script here
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
        form = HumanGame(request.POST)

        if form.is_valid():
            ai1 = form.cleaned_data['ai1']
            ai2 = form.cleaned_data['ai2']

            g = game(ai1script = ai1, ai2script  = ai2)
            g.save()

            results = play(g)

            return HttpResponse(results)
    else:
        form = HumanGame()

    return render(request, 'human_game.html', {'form': form})



def home(request):
    
    request.session.set_expiry(0)
    #this is for testing purposes only, remove when pushing to prod

    username = ''
    user_id = 0

    request.session.set_expiry(0)
    if 'user_name' in request.session:
            username = request.session['user_name']
            if 'user_id' in request.session:
                user_id = request.session['user_id']
    else:
        if 'user_id' in request.session:
            u = users.objects.get(pk=request.session['user_id'])
            username = u.user_name
            user_id = request.session['user_id']
            request.session['user_name'] = username        
        else:
            request.session['user_name'] = 'Guest'
            username = 'Guest'
            user_id = 0
            
    
    return render(request, 'home.html', \
                  {'username': username, 'user_id': user_id})


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

            
def login(request):
    if 'user_id' in request.session:
        if request.session['user_id'] > 0:
            results = 'already logged in'
            return HttpResponse(results)
        else:
            results = 'not logged in'
            return HttpResponse(results)
    else:
        if request.method == 'POST':
            form = Login(request.POST)
            
            if form.is_valid():
                try:
                    username = request.POST['username']
                    password = request.POST['password']
                    u = users.objects.get(user_name = request.POST['username'])
                    p = u.password
                    
                    if password == p:
                        request.session.flush()
                        request.session['user_id'] = u.id
                        request.session['user_name'] = u.user_name
                        request.session.set_expiry(3600)
                        return HttpResponseRedirect('.')
                    else:
                        return HttpResponse('incorrect username or password')
                    
                except:
                    return HttpResponse('login failed')
                
            else:
                form = Login()
                return render(request, 'login.html', {'form': form})

        else:
            form = Login()
            return render(request, 'login.html', {'form': form})
    

def logout(request):
    request.session.flush()
    return HttpResponseRedirect('.')


def signup(request):
    if 'user_id' in request.session:                
        if request.session['user_id'] != 0:
            return HttpResponseRedirect('.')

    if request.method == 'POST':
        form = Signup(request.POST)
        
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
                
            try:
                u = users.objects.get(user_name = username)
                form = Signup()
                return render(request, 'signup.html', {'form': form})

            except:
                u = users(user_name = username, password = password)
                u.save()
                request.session.flush()
                request.session['user_name'] = u.user_name
                request.session['user_id'] = u.id
                return HttpResponseRedirect('.')
                
    else:
        form = Signup()
        return render(request, 'signup.html', {'form': form})

