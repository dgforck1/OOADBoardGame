from django.shortcuts import HttpResponse, render
from django.http import HttpResponseRedirect
from TTT.models import pending_games, game_results
from TTT.models import users, scripts
from game import play
from forms import UploadFileForm


def save_script(s, n):
    currentuser = users.objects.get(pk=1)
        
    sc = scripts(user_id = currentuser, name = n)
    sc.save()
    
    path = '/home/student/Desktop/Ciss438/OOADBoardGame/Dreadnaught/TTT/scripts/%s%s.py' % (currentuser.user_name, sc.id)

    with open(path, 'wb+') as destination:
        for chunk in s.chunks():
            destination.write(chunk)
    

    

def index(request):
    a = pending_games(name = "a")
    a.save()
    firstai = 'ai1.py'
    secondai = 'ai2.py'
    
    results = play(a.id, firstai, secondai)
    return HttpResponse(results)


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

    
