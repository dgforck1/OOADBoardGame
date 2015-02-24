# Pull from scripts table
# Pull from games table
from TTT.models import users, scripts, game

def create_html():
    user = users.objects.get(pk=1)
    ai = scripts.objects.get(pk=1) 
    p = game(player1=user, state=0, ai1script=ai)
    p.save()
    #ai_available = []
    #pend_games = game.objects.filter(state=0)
    #ai_on_server = scripts.objects.all()
    #ai_available.append(ai_on_server)

    
    html_str = '<!DOCTYPE html> \
    <html> \
    <head> \
    <meta charset=UTF-8> \
    <title>Game Lobby</title> \
    </head> \
    <body> \
    <h1>Game Lobby</h1> \
    <p>username ai name game id</p>'
    
    for games in game.objects.filter(state=0):
        html_str += '<p>%s %s</p>' % (games.player1.user_name, p.ai1script.name)

    html_str += '<h1>Available AI</h1>' 

    for AI in scripts.objects.all():
        html_str += '<p>%s</p>' % (AI.name)
    
    html_str += '</body> \
                </html>' 

    return html_str

def show_open_games():
    return create_html()
