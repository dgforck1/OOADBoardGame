# Pull from scripts table
# Pull from games table
from TTT.models import users, scripts, game

def create_html():
    count = users.objects.count()
    ai_count = scripts.objects.count()
    game_count = game.objects.count()

    #user = users.objects.get(pk=1)
    #ai = scripts.objects.get(pk=1) 
    #p = game(player1=user, state=0, ai1script=ai)
    #p.save()
    
    html_str = """
    <!DOCTYPE html>
    <html>
    <head>
    	<style type="text/css">
    	.rwd-table {
		  margin: 1em 0;
		  min-width: 300px;
		}
		.rwd-table tr {
		  border-top: 1px solid #ddd;
		  border-bottom: 1px solid #ddd;
		}
		.rwd-table th {
		  display: none;
		}
		.rwd-table td {
		  display: block;
		}
		.rwd-table td:first-child {
		  padding-top: .5em;
		}
		.rwd-table td:last-child {
		  padding-bottom: .5em;
		}
		.rwd-table td:before {
		  content: attr(data-th) ": ";
		  font-weight: bold;
		  width: 6.5em;
		  display: inline-block;
		}
		@media (min-width: 480px) {
		  .rwd-table td:before {
		    display: none;
		  }
		}
		.rwd-table th, .rwd-table td {
		  text-align: left;
		}
		@media (min-width: 480px) {
		  .rwd-table th, .rwd-table td {
		    display: table-cell;
		    padding: .25em .5em;
		  }
		  .rwd-table th:first-child, .rwd-table td:first-child {
		    padding-left: 0;
		  }
		  .rwd-table th:last-child, .rwd-table td:last-child {
		    padding-right: 0;
		  }
		}

		body {
		  padding: 0 2em;
		  font-family: Montserrat, sans-serif;
		  -webkit-font-smoothing: antialiased;
		  text-rendering: optimizeLegibility;
		  color: #444;
		  background: #eee;
		}

		h1 {
		  font-weight: normal;
		  letter-spacing: -1px;
		  color: #34495E;
		}

		.rwd-table {
		  background: #34495E;
		  color: #fff;
		  border-radius: .4em;
		  overflow: hidden;
		}
		.rwd-table tr {
		  border-color: #46627f;
		}
		.rwd-table th, .rwd-table td {
		  margin: .5em 1em;
		}
		@media (min-width: 480px) {
		  .rwd-table th, .rwd-table td {
		    padding: 1em !important;
		  }
		}
		.rwd-table th, .rwd-table td:before {
		  color: #dd5;
		}
    	</style>
    <meta chaarset=UTF-8>
    <title>Game Lobby</title>
    </head>
    <body bgcolor="#E6E6FA">
    <h1>Game Lobby</h1>
    <table class="rwd-table">
    <tr>
        <th>Username</th>
        <th>Game ID</th>
    </tr>
    """ 
    for games in game.objects.filter(state=0):
        html_str += """ 
    	<tr>
			<td data-th="Username">%s</td>
			<td data-th="Game ID">%s</td>
		</tr>
        """ % (games.player1.user_name, games.id)
  
    html_str += """
    <tr>
    	<th>Available AI</th>
    <tr>
    """

    for AI in scripts.objects.all():
        html_str += """
        <tr>
			<td data-th="Available AI">%s</td>
		</tr>
        """ % (AI.name)
    
    html_str += """
	</table>
    </body> 
    </html>
    """

    return html_str

def show_open_games():
    return create_html()
