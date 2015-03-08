from django.shortcuts import HttpResponse, render
from django.http import HttpResponseRedirect
from settings import SCRIPTS_FOLDER

from TTT.models import users, scripts, game
from game2 import play, play_turn
from forms import *
from lobby import show_open_games

def save_script(s, n, request):
    
    currentuser = request.session['user_id']
    currentuser = users.objects.get(pk = currentuser)
        
    sc = scripts(user_id = currentuser, name = n)
    sc.save()


    path = SCRIPTS_FOLDER + '%s%s.py' % (currentuser.user_name, sc.id)
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
            save_script(request.FILES['file'], request.POST['title'], request)
        
            return HttpResponseRedirect('.')

    else:
        form = UploadFileForm()

    return render(request, 'uploads.html', {'form': form})


def game_lobby(request):
    if 'user_id' in request.session:
        if request.session['user_id'] > 0:
            u = request.session['user_id']
            u = users.objects.get(id = u)
            
            try:
                all_games = game.objects.filter(state=0)
                all_AI = scripts.objects.all()
                return render(request, 'lobby.html', \
                          {'games': all_games, 'AI' : all_AI})
            
            except:
                message = "No games available"
                
                return render(request, 'lobby.html', \
                              {'message': message})
            
        else:
            return HttpResponseRedirect('.')
    
    return HttpResponseRedirect('.')


def select_game(request):
    if request.method == 'POST':
        form = SelectGame(request.POST)

        if form.is_valid():
            ai1 = form.cleaned_data['player1']
            ai2 = form.cleaned_data['player2']

            g = game(ai1script = ai1, ai2script  = ai2, state = 1)
            g.save()

            print (g.state)
            gid = g.id

            results = play_turn(g)

            return render(request, 'human_game.html', {'form': HumanGame(request.POST), 'gid': gid, 'html_string': results})
    else:
        form = SelectGame()

    return render(request, 'select_game.html', {'form': form})


def human_game(request):
    gid = -1
    
    if request.method == 'POST':
        form = HumanGame(request.POST)

        if form.is_valid():
            move = form.cleaned_data['move']

        gid = request.POST['gameid']
        print "Game ID:", gid

        g = game.objects.get(id = gid)
        g.history += '%d' % (move)
        g.state = ((g.state % 2) + 1)
        g.save()

        results = play_turn(g)
    else:
        form = HumanGame()
        gid = -1
        results = 'Suck a dick'

    return render(request, 'human_game.html', {'form': HumanGame(request.POST), 'gid': gid, 'html_string': results})
    


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
            confirm_pass = request.POST['confirm_pass']
            email = request.POST['email']

            if password == confirm_pass:
                try:
                    u = users.objects.get(user_name = username)
                    form = Signup()
                    message = "That user already exists"
                    return render(request, 'signup.html', {'form': form, \
                                                           'message': message})

                except:                
                    try:
                        u = users.objects.get(email = email)
                        form = Signup()
                        message = "That email already exists"
                        return render(request, 'signup.html', {'form': form, \
                                                               'message': message})
                    except:
                        u = users(user_name = username, password = password, \
                                  email = email)
                        u.save()
                        request.session.flush()
                        request.session['user_name'] = u.user_name
                        request.session['user_id'] = u.id
                        return HttpResponseRedirect('.')
            else:
                message = "Passwords don't match"
                return render(request, 'signup.html', {'form': form, \
                                                       'message': message})
        else:
            message = "Not valid!"
            return render(request, 'signup.html', {'form': form, \
                                                       'message': message})
            
                
    else:
        form = Signup()
        return render(request, 'signup.html', {'form': form})

    return HttpResponseRedirect('.')


def view_script_list(request):
    
    if 'user_id' in request.session:
        if request.session['user_id'] > 0:
            u = request.session['user_id']
            u = users.objects.get(id = u)
            
            try:
                user_scripts = scripts.objects.filter(user_id = u.id) 
                return render(request, 'view_script_list.html', \
                          {'scripts': user_scripts})
            
            except:
                message = "You don't have any scripts!"
                
                return render(request, 'view_script_list.html', \
                              {'message': message})
            
        else:
            return HttpResponseRedirect('.')
    
    return HttpResponseRedirect('.')


def view_script(request, id):
    try:
        id = int(id)

        
    except:
        message = "Invalid script id"
        return HttpResponseRedirect(message)

    try:
        script = scripts.objects.get(pk=id)

        import os
        location = script.location
        module_dir = os.path.dirname(__file__)  
        file_path = os.path.join(module_dir, location)

        file = open(file_path)

        file_string = []
        
        for line in file.readlines():
            file_string.append(line)
            

        return render(request, 'view_script.html', \
                      {'file_string': file_string})

    except:
        message = "Invalid script id"
        return HttpResponseRedirect(message)


    return HttpResponse('a')

def view_script_games(request, id):
    try:
        id = int(id)
        
        

    except:
        return HttpResponseRedirect('.')

    try:
        games = game.objects.filter(ai1script = id) |  \
                game.objects.filter(ai2script = id)
        #get all of the ai's games
        
        d = {'games' : games}

        script = scripts.objects.get(pk=id)
        d['name'] = script.name


        
        return render(request, 'view_script_games.html', d)
    except:
        return HttpResponseRedirect('.')


    return HttpResponse('a')


def game_results(request, id):

    try:
        id = int(id)
        
    except:
        return HttpResponseRedirect('.')


    #try:
    import copy
    games = game.objects.get(pk = id)
    history = games.history
    
    d = {'game' : games}

    historylist = []
    board = ['&nbsp;&nbsp;','&nbsp;&nbsp;','&nbsp;&nbsp;','&nbsp;&nbsp;', \
             '&nbsp;&nbsp;','&nbsp;&nbsp;','&nbsp;&nbsp;','&nbsp;&nbsp;', \
             '&nbsp;&nbsp;']

    temp = ''

    for i in range(len(history)):        
        b = int(history[i])
        
        if i % 2 == 0:
            board[b] = 'X'
        else:
            board[b] = 'O'

        historylist.append(copy.deepcopy(board))

    
    d['history'] = historylist
        
    return render(request, 'game_results.html', d)
    '''
    except:
        return HttpResponseRedirect('../../')
    '''
