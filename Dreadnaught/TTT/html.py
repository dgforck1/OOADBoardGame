

html_str = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Tic-Tac-Toe</title>
</head>

<body>
    <h1>Welcome!</h1>
    <h2>Tic-Tac-Toe</h2>
    <table border=1>
        <tr>
            <th>X</th>
            <th>O</th>
            <th>O</th>
        </tr>
        <tr>
            <th>O</th>
            <th>X</th>
            <th>O</th>
        </tr>
        <tr>
            <th>X</th>
            <th>X</th>
            <th>O</th>
        </tr>
    </table>
</body>

</html>  

"""

Html_file = open("tictactoe.html","w")
Html_file.write(html_str)
Html_file.close()
