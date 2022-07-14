import random
from typing import List, Dict
import math


def get_info() -> dict:
    """
    This controls your Battlesnake appearance and author permissions.
    For customization options, see https://docs.battlesnake.com/references/personalization

    TIP: If you open your Battlesnake URL in browser you should see this data.
    """
    return {
        "apiversion": "1",
        "author": "Goldeneyes",
        "color": "#00ff00",  # "color": "#EB6443",
        "head": "missile",
        "tail": "rocket",
    }


def choose_move(data: dict) -> str:
    """
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: A String, the single move to make. One of "up", "down", "left" or "right".

    Use the information in 'data' to decide your next move. The 'data' variable can be interacted
    with as a Python Dictionary, and contains all of the information about the Battlesnake board
    for each move of the game.

    """
    my_snake = data["you"]      # A dictionary describing your snake's position on the board
    # A dictionary of coordinates like {"x": 0, "y": 0}
    my_head = my_snake["head"]
    # A list of coordinate dictionaries like [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}]
    my_body = my_snake["body"]

    # Uncomment the lines below to see what this data looks like in your output!
    # print(f"~~~ Turn: {data['turn']}  Game Mode: {data['game']['ruleset']['name']} ~~~")
    # print(f"All board data this turn: {data}")
    # print(f"My Battlesnake this turn is: {my_snake}")
    # print(f"My Battlesnakes head this turn is: {my_head}")
    # print(f"My Battlesnakes body this turn is: {my_body}")

    possible_moves = ["up", "down", "left", "right"]

    # Step 0: Don't allow your Battlesnake to move back on it's own neck.
    possible_moves = _avoid_my_neck(my_body, possible_moves)
    board = data['board']
    # board_height = board['height']
    # board_width = board['width']

    # other_snakes = board['snakes']
    # other_snakes_pos = []
    # for snake in other_snakes:
    #     for i in snake["body"]:
    #         other_snakes_pos.append(i["x"], i["y"])

    # food = data["board"]["food"]

    moves = {
        "up": [my_head['x'], my_head['y']+1],
        "down": [my_head['x'], my_head['y']-1],
        "left": [my_head['x']-1, my_head['y']],
        "right": [my_head['x']+1, my_head['y']]
    }

    possible_moves = _filter_wall_moves(my_body, possible_moves, board)
    possible_moves = _filter_self_moves(my_body, possible_moves)

    # for direction in possible_moves:
    #     # Don't hit walls
    #     if 1 >= moves[direction][0] >= board_width-1:
    #         possible_moves.remove(direction)
    #     elif 1 >= moves[direction][1] >= board_height-1:
    #         possible_moves.remove(direction)

    # # Don't hit yourself
    # for segment in my_body:
    #     if segment["x"] == moves[direction][0] or segment["y"] == moves[direction][1]:
    #         possible_moves.remove(direction)

    # # Don't hit others
    # for segment in other_snakes_pos:
    #     if segment["x"] == moves[direction][0] or segment["y"] == moves[direction][1]:
    #         possible_moves.remove(direction)

    # if food != {}:
    #     possible_food_moves = []
    #     closest = [food[0]["x"], food[0]["y"]]
    #     for i in food:
    #         if math.dist((my_head["x"], my_head["y"]), (i["x"], i["y"])) < math.dist((my_head["x"], my_head["y"]), (closest["x"], closest["y"])):
    #             closest = [i["x"], i["y"]]

    #     for direction in possible_moves:
    #         if math.dist(moves[direction], closest) > math.dist((my_head["x"], my_head["y"]), closest):
    #             possible_food_moves.append(direction)
    #     if possible_food_moves:
    #         move = random.choice(possible_food_moves)
    #     else:
    #         move = random.choice(possible_moves)
    # else:
    #     move = random.choice(possible_moves)
    move = random.choice(possible_moves)

    # TODO: Step 2 - Don't hit yourself.
    # Use information from `my_body` to avoid moves that would collide with yourself.

    # TODO: Step 3 - Don't collide with others.
    # Use information from `data` to prevent your Battlesnake from colliding with others.

    # TODO: Step 4 - Find food.
    # Use information in `data` to seek out and find food.
    # food = data['board']['food']

    # Choose a random direction from the remaining possible_moves to move in, and then return that move

    # TODO: Explore new strategies for picking a move that are better than random

    print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")

    return move


def _filter_wall_moves(my_body: dict, possible_moves: List[str], board: dict) -> List[str]:
    my_head = my_body[0]

    board_height = board['height']
    board_width = board['width']

    moves = {
        "up": {"x": my_head['x'], "y": my_head['y']+1},
        "down": {"x": my_head['x'], "y": my_head['y']-1},
        "left": {"x": my_head['x']-1, "y": my_head['y']},
        "right": {"x": my_head['x']+1, "y": my_head['y']}
    }
    print(moves)
    for direction in possible_moves:

        # Don't hit walls
        if direction == "right" or direction == "left":
            if 0 == moves[direction]["x"] or moves[direction]["x"] >= board_width-1:
                possible_moves.remove(direction)
        elif direction == "up" or direction == "down":
            if 0 == moves[direction]["y"] or moves[direction]["y"] >= board_height-1:
                possible_moves.remove(direction)

    print(possible_moves)
    print("\n")
    return possible_moves


def _filter_self_moves(my_body: dict, possible_moves: List[str]) -> List[str]:
    my_head = my_body[0]

    moves = {
        "up": {"x": my_head['x'], "y": my_head['y']+1},
        "down": {"x": my_head['x'], "y": my_head['y']-1},
        "left": {"x": my_head['x']-1, "y": my_head['y']},
        "right": {"x": my_head['x']+1, "y": my_head['y']}
    }

    for direction in possible_moves:
        for segment in my_body[1:]:
            if direction == "right" or direction == "left":
                if segment["x"] == moves[direction]["x"]:
                    possible_moves.remove(direction)
            elif direction == "up" or direction == "down":
                if segment["y"] == moves[direction]["y"]:
                    possible_moves.remove(direction)

    return possible_moves


def _avoid_my_neck(my_body: dict, possible_moves: List[str]) -> List[str]:
    """
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves, with the 'neck' direction removed
    """
    my_head = my_body[0]  # The first body coordinate is always the head
    # The segment of body right after the head is the 'neck'
    my_neck = my_body[1]

    if my_neck["x"] < my_head["x"]:  # my neck is left of my head
        possible_moves.remove("left")
    elif my_neck["x"] > my_head["x"]:  # my neck is right of my head
        possible_moves.remove("right")
    elif my_neck["y"] < my_head["y"]:  # my neck is below my head
        possible_moves.remove("down")
    elif my_neck["y"] > my_head["y"]:  # my neck is above my head
        possible_moves.remove("up")

    return possible_moves
