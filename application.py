from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def winner():
    game = session["board"]
    for i in range(3):
        if game[i][0] and game[i][0]==game[i][1] and game[i][0]==game[i][2]:
            # row
            return game[i][0]
    for i in range(3):
        if game[0][i] and game[0][i]==game[1][i] and game[0][i]==game[2][i]:
            # col
            return game[0][i]

    if game[0][0] and game[1][1]==game[0][0] and game[0][0]==game[2][2]:
        # diag 1
        return game[0][0]
    if game[0][2] and game[1][1]==game[0][2] and game[2][0]==game[0][2]:
        # diag 2
        return game[0][2]
    return None

@app.route("/reset")
def reset():
    del session["board"]
    return redirect(url_for("index"))

@app.route("/")
def index():

    if "board" not in session:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        session["turn"] = "X"

    return render_template("game.html", game=session["board"], turn=session["turn"], winner=winner())

@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    game = session["board"]
    turn=session["turn"]
    game[row][col]=turn
    session["board"] = game
    if session["turn"] == "X":
        session["turn"] = "O"
    else:
        session["turn"] = "X"

    return redirect(url_for("index"))
