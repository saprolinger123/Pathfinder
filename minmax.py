from simple_eval import simple_eval
def minmax(board, current_depth, max_depth, is_maximizing, alpha = -float("inf"), beta = float("inf")):

	if board.check_win() == 1:
		return 1
	elif board.check_win() == 2:
		return -1

	if current_depth == max_depth:
		return simple_eval(board, 1 if is_maximizing else 2)

	moves = board.get_legal_moves()
	best_eval = float("inf") * (-1 if is_maximizing else 1)
	for move in moves:
		board.make_move(move)
		move_eval = minmax(board, current_depth + 1, max_depth, not is_maximizing, alpha, beta)
		if is_maximizing:
			if move_eval > best_eval:
				best_eval = move_eval
				alpha = move_eval
		
		else:
			if move_eval < best_eval:
				best_eval = move_eval
				beta = move_eval


		board.undo_move(move)
	
		if alpha >= beta:
			break

	return best_eval
