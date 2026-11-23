from board import Board
from minmax import minmax

class Engine:

    def analyze(self, board, depth):
        return minmax(board, 0, depth, True)

    def get_best_move(self, board, depth):
        best_eval = -float("inf") if board.turn == 1 else float("inf")
        best_move = None
        alpha = -float("inf")
        beta = float("inf")

        for move in board.get_legal_moves():
            board.make_move(*move)
            move_eval = minmax(board, 1, depth, board.turn == 1, alpha, beta)
            board.undo_move(*move)

            if (move_eval > best_eval and board.turn == 1) or (move_eval < best_eval and board.turn == 2):
                best_eval = move_eval
                best_move = move

            if board.turn == 1:
                alpha = max(alpha, best_eval)
            else:
                beta = min(beta, best_eval)

        return best_move
