import logging
import os

from flask import Flask
from flask import request

from game import Game


app = Flask(__name__)

games = {}

@app.get("/")
def handle_info():
    """
    This function is called when you register your Battlesnake on play.battlesnake.com
    See https://docs.battlesnake.com/guides/getting-started#step-4-register-your-battlesnake
    """
    print("INFO")
    print("Hello World", flush=True)
    return {
            "apiversion": "1",
            "author": "Goldeneyes",
            "color": "#4C89C8",  # "color": "#EB6443",
            "head": "lantern-fish", #beluga
            "tail": "flame", #bolt
        }


@app.post("/start")
def handle_start():
    """
    This function is called everytime your Battlesnake enters a game.
    It's purely for informational purposes, you don't have to make any decisions here.
    request.json contains information about the game that's about to be played.
    """
    
    data = request.get_json()
    new_game = Game(data)
    game = {new_game.get_id() : new_game}
    games.update(game)
    
    print(f"{data['game']['id']} START")
    return "ok"


@app.post("/move")
def handle_move():
    """
    This function is called on every turn and is how your Battlesnake decides where to move.
    Valid moves are "up", "down", "left", or "right".
    """
    data = request.get_json()
    move = games[data["game"]["id"]].turn(data)
    print(f"{data['game']['id']} MOVE {move}")
    
    return {"move": move, "shout": ""}



@app.post("/end")
def handle_end():
    """
    This function is called when a game your Battlesnake was in has ended.
    It's purely for informational purposes, you don't have to make any decisions here.
    """
    data = request.get_json()
    games.pop(data["game"]["id"])
    
    print(f"{data['game']['id']} END")
    return "ok"


@app.after_request
def identify_server(response):
    response.headers["Server"] = "BattlesnakeOfficial/starter-snake-python"
    return response


if __name__ == "__main__":
    logging.getLogger("werkzeug").setLevel(logging.ERROR)

    host = "0.0.0.0"
    port = int(os.environ.get("PORT", "8080"))

    print(f"\nRunning Battlesnake server at http://{host}:{port}")
    # app.env = 'development'
    app.run(host=host, port=port, debug=True)
