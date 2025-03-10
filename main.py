# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing
from helper import moveHead, a_star

# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "",  # TODO: Your Battlesnake Username
        "color": "#888888",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    # Prevent Battlesnake from moving out of bounds
    board_width = game_state['board']['width'] - 1
    board_height = game_state['board']['height'] - 1

    if my_head["x"] == 0:
        is_move_safe["left"] = False
    if my_head["x"] == board_width:
        is_move_safe["right"] = False
    if my_head["y"] == 0:
        is_move_safe["down"] = False
    if my_head["y"] == board_height:
        is_move_safe["up"] = False


    # Prevent Battlesnake from colliding with itself and enemy snakes
    snakes = game_state['board']['snakes']
    body_cells = []
    for snake in snakes:
        body_cells.extend(snake['body'])
        body_cells.append(snake['head'])
    for move, isSafe in is_move_safe.items():
        if isSafe:
            next_move_head = moveHead(move, my_head)
            for body_cell in body_cells:
                if next_move_head == body_cell:
                    is_move_safe[move] = False

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)

    # Move towards food instead of random, to regain health and survive longer
    food = game_state['board']['food']
    start = (my_head["x"], my_head["y"])
    goal_positions = []
    obstacle_positions = []

    for goal in food:
        goal_pos = (goal["x"], goal["y"])
        goal_positions.append(goal_pos)
    
    for obstacle in snakes:
        for cell in obstacle["body"]:
            obstacle_pos = (cell["x"], cell["y"])
            obstacle_positions.append(obstacle_pos)
        if obstacle["id"] != game_state["you"]["id"]:
            head_pos = (obstacle["head"]["x"], obstacle["head"]["y"])
            obstacle_positions.append(head_pos)
    
    next_position = a_star(start, goal_positions, obstacle_positions, board_width, board_height)

    if next_position != None:
        print(f"The next_position is {next_position.position}")
        suggested_move = None
        if next_position.position[0] == start[0] - 1:
            suggested_move = "left"
        elif next_position.position[0] == start[0] + 1:
            suggested_move = "right"
        elif next_position.position[1] == start[1] + 1:
            suggested_move = "up"
        elif next_position.position[1] == start[1] - 1:
            suggested_move = "down"
        print(f"The suggested move is {suggested_move}")
        if suggested_move != None:
            return {"move": suggested_move}

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
