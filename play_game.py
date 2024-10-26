import chess


def play_game(agent_white, agent_black, K=32):
    moves = []
    board = chess.Board()
    feedback_white = ""
    feedback_black = ""
    move_count = 0  # Initialize move counter

    while not board.is_game_over():
        if board.turn:  # White's turn
            current_agent = agent_white
            feedback = feedback_white
        else:  # Black's turn
            current_agent = agent_black
            feedback = feedback_black

        board_state = board.fen()
        legal_moves_list = [board.san(move) for move in board.legal_moves]
        legal_moves = ', '.join(legal_moves_list)
        history = ', '.join(moves)

        while True:
            next_move_str = current_agent.get_next_move(board_state, legal_moves, history, feedback)

            try:
                move = board.parse_san(next_move_str)
                if move in board.legal_moves:
                    break
                else:
                    feedback = f"Illegal move: {next_move_str}. Legal moves are: {legal_moves}"
            except Exception as e:
                feedback = f"Failed to parse move '{next_move_str}': {e}"

        board.push(move)
        moves.append(next_move_str)
        move_count += 1  # Increment move counter
        print(f"{current_agent.name} plays: {next_move_str}")
        print(board)
        print("\n")

        # Check for draw or stalemate conditions
        if board.can_claim_threefold_repetition():
            print("Draw by threefold repetition.")
            break
        if board.can_claim_fifty_moves():
            print("Draw by the fifty-move rule.")
            break
        if board.is_stalemate():
            print("Draw by stalemate.")
            break
        if board.is_insufficient_material():
            print("Draw due to insufficient material.")
            break
        if board.is_seventyfive_moves():
            print("Draw by the seventy-five-move rule.")
            break
        if move_count >= 100:
            print("Draw due to exceeding maximum number of moves.")
            break

    # Determine the result and update ratings
    result = board.result()
    if result == "1-0":
        winner = agent_white
        loser = agent_black
        draw = False
    elif result == "0-1":
        winner = agent_black
        loser = agent_white
        draw = False
    else:
        draw = True

    # Calculate Elo rating updates
    if not draw:
        R_a = winner.rating
        R_b = loser.rating
        E_a = 1 / (1 + 10 ** ((R_b - R_a) / 400))
        S_a = 1
        winner.rating = R_a + K * (S_a - E_a)
        loser.rating = R_b + K * (0 - (1 - E_a))
        return winner.name
    else:
        # Update ratings for a draw
        R_a = agent_white.rating
        R_b = agent_black.rating
        E_a = 1 / (1 + 10 ** ((R_b - R_a) / 400))
        agent_white.rating = R_a + K * (0.5 - E_a)
        agent_black.rating = R_b + K * (0.5 - (1 - E_a))
        return "Draw"
