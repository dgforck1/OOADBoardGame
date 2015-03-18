from django.shortcuts import HttpResponse, render
from django.http import HttpResponseRedirect
from settings import SCRIPTS_FOLDER

from TTT.models import users, scripts, game
from forms import *
from lobby import show_open_games


def get_user(request):
    #determine whether the user is logged in
    #if logged in, returns a user object, otherwise returns 0
    if 'user_id' in request.session:
        if request.session['user_id'] > 0:
            u = request.session['user_id']
            u = users.objects.get(id = u)

            return u
    return 0

def save_script(s, n, request):
    
    currentuser = request.session['user_id']
    currentuser = users.objects.get(pk = currentuser)


    already_exists = scripts.objects.filter(user_id = currentuser, name = n)

    if already_exists:
        return ['Script must have a unique name', 0]
    else:

        
        sc = scripts(user_id = currentuser, name = n)
        sc.save()

    
        try:
            path = SCRIPTS_FOLDER + '%s.py' % (sc.id)
            sc.location = path
            sc.save()

            with open(path, 'wb+') as destination:
                for chunk in s.chunks():
                    destination.write(chunk)

            #validate script
            v = open(path, 'r')

            valid = 1
            
            for i, line in enumerate(v):
                if i == 0:
                    if line != 'getmove()':
                        valid = 0
                
            if valid == 1:
                return ['Script uploaded successfully!', 1]
            else:
                import os
                v.close()
                os.remove(path)
                sc.delete()
                
                return ['Script failed validation!', 0]
        except:
            return ['Script failed to save, please try again', 0]




def uploads(request):    
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        
        #process script here
        if form.is_valid():
            message = save_script(request.FILES['file'], \
                                  request.POST['title'], request)

            if message[1] == 1:
                form = UploadFileForm() #reset form


            d = {'form': form}
            d['message'] = message[0]
                
            
            return render(request, 'uploads.html', d)            

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



def checkers_test(request):
    return render(request, 'checkers_temp.html')
    


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


'''def select_ai(request):
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

    return render(request, 'selectai.html', {'form': form})'''

            
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
                        return render(request, 'signup.html', \
                                      {'form': form, 'message': message})
                    
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


def user_script_list(request):
    
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

def profile(request):
    u = get_user(request)

    if u:
        
        return render(request, 'profile.html', {'user': u})
    else:
        return HttpResponseRedirect('/TTT/')



def change_pass(request):

    u = get_user(request)

    if u:
        d = {'user': u}
        
        if request.method=='POST': #form was submitted
            form = Change_Pass(request.POST) #put data back into form
            
            if form.is_valid():
                prev_pass = request.POST['prev_password']
                new_pass = request.POST['new_password']

                current_password = u.password

                if prev_pass == current_password:
                    u.password = new_pass
                    message = 'password successfully changed'
                    form = Change_Pass()
                    
                    d['form'] = form
                    d['message'] = message


                    return render(request, 'change_pass.html', d)
                else:
                    message = 'incorrect password'
                    form = Change_Pass()
                    
                    d['form'] = form
                    d['message'] = message


                    return render(request, 'change_pass.html', d)
                    
            else:
                message = 'Invalid input'
                form = Change_Pass()
                
                d['form'] = form
                d['message'] = message
                
                return render(request, 'change_pass.html', d)
            
        else: #initial loading of page
        
            form = Change_Pass()
            
            d['form'] = form            
            return render(request, 'change_pass.html', d)
    
    else:
        return HttpResponseRedirect('/TTT/')
