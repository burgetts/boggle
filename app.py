from boggle import Boggle
from flask import Flask, request, render_template, session, jsonify, redirect
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "beans"

debug = DebugToolbarExtension(app)

boggle_game = Boggle()
board = boggle_game.make_board()
# session['board'] = board


@app.route('/')
def show_home_page():
    """Render home page that shows game instructions."""
    return render_template('start.html')

@app.route('/play-boggle')
def play_game():
    """Show board and begin game."""
    session['board'] = board
    return render_template('game.html', board=board)

@app.route('/check-guess')
def check_guess():
    """Checks user's guess against word list and board. Returns "ok", "not-word", or "not-on-board". """
    guess = request.args['guess']
    valid = boggle_game.check_valid_word(board, guess) #"ok", "not-word","not-on-board"
    resp = jsonify({'result': valid})
    return resp

@app.route('/store-stats', methods=['GET','POST'])
def save_stats():
    """Increment number of times played in session, compares current score with high score and replaces if eligible. Returns true if new score becomes high score."""
    # Get score, save if max score
    json_resp = request.get_json()
    score = json_resp["params"]["score"]
    max_score = session.get('score', 0)
    if score > max_score:
        session['score'] = score
    
    # Update times played
    times_played = session.get('times_played', 0)
    session['times_played'] = times_played+1
    return jsonify(score > max_score)

@app.route('/stats/win')
def display_win():
    """Displays page once game is over and player beats high score. """
    return render_template('stats_win.html')

@app.route('/stats/lose')
def display_lose():
    """Displays page once game is over and player did not beat high score. """
    return render_template('stats_lose.html')

