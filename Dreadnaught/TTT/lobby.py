# Pull from scripts table
# Pull from games table
from TTT.models import users, scripts, game

def create_html():

    #available = []
    #ai_available = []
    
    #pend_games = game.objects.filter(state=0)
    #ai_on_server = scripts.objects.all()
    
    #available.append(pend_games)
    #ai_available.append(ai_on_server)

    html_str = '<!DOCTYPE html> \
    <html> \
    <head> \
    <meta charset=UTF-8> \
    <title>Game Lobby</title> \    
    </head> \
    <body> \
    <h1>Game Lobby</h1> \    
    <p>username ai name game id</p> \
    <p></p> \
    <p></p> \
    </br> \
    </body> \ 
    </html>'
    #% (available, ai_available)

    return html_str

def show_open_games():
    return create_html()
