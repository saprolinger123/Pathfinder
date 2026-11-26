from core.engine import Engine
from core.board import Board
game = eval(input("Enter the game log: \n"))
ratings = []
board = Board()
engine = Engine()
i = 0
for move in game[2:]:
    if board.turn == 2:
        ratings.append(engine.rate_move(board, move, 3)) 
        i += 1
        print("analyzing move: " +  str(i) + "/" + str(int(len(game[2:]) / 2)))
    board.make_move(*move)
    if board.check_win() != 0:
        break
player_distance = board.get_path_length_to_goal(board.player_2_pos, 2)
engine_distance = board.get_path_length_to_goal(board.player_1_pos, 1)
path_distance_difference = player_distance - engine_distance
print(game[0], game[1], ratings, path_distance_difference, (sum(ratings) / len(ratings) if ratings else 0) * 100)