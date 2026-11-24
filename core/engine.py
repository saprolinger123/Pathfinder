from core.board import Board
from core.minmax import minmax

class Engine:

    def analyze(self, board, depth):
        return minmax(board, 0, depth, board.turn == 1)

    def get_best_move(self, board, depth):
        best_eval = -float("inf") if board.turn == 1 else float("inf")
        best_move = None
        alpha = -float("inf")
        beta = float("inf")
        root_turn = board.turn

        legal_moves = board.get_legal_moves()
        shallow_results = []

        for move in legal_moves:
            board.make_move(*move)
            shallow_eval = self.analyze(board, 1)
            board.undo_move(*move)
            shallow_results.append((shallow_eval, move))

        shallow_results.sort(
            key=lambda result: result[0],
            reverse=root_turn == 1,
        )
        ordered_moves = [move for _, move in shallow_results]

        for move in ordered_moves:
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
