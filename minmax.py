from simple_eval import simple_eval
def minmax(engine, board, current_depth, max_depth, is_maximizing, alpha = -float("inf"), beta = float("inf")):
	remaining_depth = max_depth - current_depth
	if board.check_win() == 1:
		return 1
	elif board.check_win() == 2:
		return -1

	if current_depth == max_depth:
		return simple_eval(board)

	moves = board.get_legal_moves()
	best_eval = float("inf") * (-1 if is_maximizing else 1)
	for move in moves:
		board.make_move(*move)
		position_key = (tuple(board.player_1_pos), tuple(board.player_2_pos), tuple(tuple(tuple(part) for part in fence) for fence in board.fences), board.player_1_fences, board.player_2_fences, board.turn, remaining_depth)
		if position_key not in engine.position_evaluations:
			move_eval = minmax(engine, board, current_depth + 1, max_depth, not is_maximizing, alpha, beta)
			engine.position_evaluations[position_key] = move_eval
		else:
			move_eval = engine.position_evaluations[position_key]

		if is_maximizing:
			if move_eval > best_eval:
				best_eval = move_eval
				alpha = max(best_eval, alpha)
		
		else:
			if move_eval < best_eval:
				best_eval = move_eval
				beta = min(best_eval, beta)


		board.undo_move(*move)
	
		if alpha >= beta:
			break

	return best_eval
