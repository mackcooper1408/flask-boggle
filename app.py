from flask import Flask, request, render_template, jsonify, session
from uuid import uuid4

from boggle import BoggleGame, LETTERS_BY_FREQ

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.route("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.route("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game
    board = game.get_random_board(LETTERS_BY_FREQ)

    return jsonify({"gameId": game_id, "board": board})


@app.route("/api/score-word", methods=["POST"])
def score_word():
    """ Check if word is legal """

    word = request.args["word"]
    game_id = request.args["game_id"]
    game = games[game_id]
    result = {}

    if word not in game.word_list:
        result["result"] = result.get("result", "not-word")
    elif word not in game.board:
        result["result"] = result.get("result", "not-on-board")
    else:
        result["result"] = result.get("result", "ok")

    return jsonify(result)
