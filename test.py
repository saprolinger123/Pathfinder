from engine import Engine
from board import Board

board = Board()
engine = Engine()

while True:
    best_move = engine.get_best_move(board, 2)
    print("Player " + str(board.turn) + ": " + str(best_move))
    board.make_move(*best_move)