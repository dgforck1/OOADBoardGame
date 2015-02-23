# Pull from scripts table
# Pull from games table
from TTT.models import users, scripts, game

def create_html():

	test = []
	test.append('test1')
	test.append('test2')
	test.append('test3')

	html_str = """<!DOCTYPE html> 
    <html> 
    <head> 
    <meta charset=UTF-8> 
    <title>Game Lobby</title> 
    </head> 
    <body> 
    <h1>Game Lobby</h1> 
    <p>username ai name game id</p>
    
    </br> 
    </body> 
    </html>""" % (test)

	return html_str

def show_open_games():
	return create_html()
