import random

VALID_MOVES = ["a1", "a4", "a7", "b2", "b4", "b6", "c3", "c4", "c5",
               "d1", "d2", "d3", "d5", "d6", "d7", "e3", "e4", "e5",
               "f2", "f4", "f6", "g1", "g4", "g7"]

# Define adjacent positions as per referee code
NEIGHBORS = {
    "a1": ["a4", "d1"],
    "a4": ["a1", "a7", "b4"],
    "a7": ["a4", "d7"],
    "b2": ["b4", "d2"],
    "b4": ["b2", "b6", "a4", "c4"],
    "b6": ["b4", "d6"],
    "c3": ["c4", "d3"],
    "c4": ["c3", "c5", "b4"],
    "c5": ["c4", "d5"],
    "d1": ["a1", "d2", "g1"],
    "d2": ["b2", "d1", "d3", "f2"],
    "d3": ["c3", "d2", "e3"],
    "d5": ["c5", "d6", "e5"],
    "d6": ["b6", "d5", "d7", "f6"],
    "d7": ["a7", "d6", "g7"],
    "e3": ["d3", "e4"],
    "e4": ["e3", "e5", "f4"],
    "e5": ["d5", "e4"],
    "f2": ["d2", "f4"],
    "f4": ["e4", "f2", "f6", "g4"],
    "f6": ["d6", "f4"],
    "g1": ["d1", "g4"],
    "g4": ["f4", "g1", "g7"],
    "g7": ["d7", "g4"]
}

# Define all possible mills as per referee code
MILLS = [
    # Horizontal mills
    ["a1", "a4", "a7"],
    ["b2", "b4", "b6"],
    ["c3", "c4", "c5"],
    ["d1", "d2", "d3"],
    ["d5", "d6", "d7"],
    ["e3", "e4", "e5"],
    ["f2", "f4", "f6"],
    ["g1", "g4", "g7"],
    # Vertical mills
    ["a1", "d1", "g1"],
    ["b2", "d2", "f2"],
    ["c3", "d3", "e3"],
    ["a4", "b4", "c4"],
    ["e4", "f4", "g4"],
    ["c5", "d5", "e5"],
    ["b6", "d6", "f6"],
    ["a7", "d7", "g7"]
]


class LaskerMorrisPlayer:
    def __init__(self):
        self.board = {}  # position -> color ('X' for blue, 'O' for orange)
        self.my_color = None
        self.opponent_color = None
        self.my_pieces = []  # List of positions where my pieces are
        self.opponent_pieces = []  # List of positions where opponent pieces are
        self.phase = "placing"  # "placing", "moving", or "flying"
        self.pieces_in_hand = 10

    def initialize_game(self, color):
        self.my_color = 'X' if color == "blue" else 'O'
        self.opponent_color = 'O' if color == "blue" else 'X'
        # Initialize empty board
        for pos in VALID_MOVES:
            self.board[pos] = None

    def check_mill(self, source, target):
        """Check if placing/moving a stone to target position forms a mill.
        Matches referee's mill checking logic."""
        # Temporarily update board state
        if source in self.board:
            old_source_value = self.board[source]
            self.board[source] = None
        else:
            old_source_value = None

        self.board[target] = self.my_color

        # Check for mills containing the target position
        forms_mill = False
        for mill in MILLS:
            if target in mill:
                stones_in_mill = sum(1 for pos in mill if self.board.get(pos) == self.my_color)
                if stones_in_mill == 3:
                    forms_mill = True
                    break

        # Restore board state
        if source in self.board:
            self.board[source] = old_source_value
        self.board[target] = None

        return forms_mill

    def get_valid_moves(self):
        """Get all valid moves based on current game phase"""
        if self.phase == "placing":
            return [pos for pos in VALID_MOVES if pos not in self.board or self.board[pos] is None]
        elif self.phase == "flying":
            return [(piece, target) for piece in self.my_pieces
                    for target in VALID_MOVES
                    if self.board.get(target) is None]
        else:  # moving phase
            return [(piece, target) for piece in self.my_pieces
                    for target in NEIGHBORS[piece]
                    if self.board.get(target) is None]

    def get_removable_piece(self):
        """Get a random opponent piece that can be removed.
        Prioritize pieces not in mills unless all pieces are in mills."""
        non_mill_pieces = []
        for pos in self.opponent_pieces:
            in_mill = False
            for mill in MILLS:
                if pos in mill and all(
                        p in self.board and self.board[p] == self.opponent_color for p in mill):
                    in_mill = True
                    break
            if not in_mill:
                non_mill_pieces.append(pos)

        if non_mill_pieces:
            return random.choice(non_mill_pieces)
        elif self.opponent_pieces:
            return random.choice(self.opponent_pieces)
        return "r0"
    
    def evaluate_board(board, my_color, opponent_color):
        """
        Evaluates the given board configuration and returns a score for the current player.
        
        :param board: Dictionary representing the board state {position: 'X' or 'O' or None}.
        :param my_color: The color of the current player ('X' for blue, 'O' for orange).
        :param opponent_color: The color of the opponent player.
        :return: Positive score if current player is winning, negative score if losing, 0 for draw.
        """
        my_pieces = sum(1 for pos in board if board[pos] == my_color)
        opponent_pieces = sum(1 for pos in board if board[pos] == opponent_color)

        # Check if the game is won/lost
        if opponent_pieces < 3:
            return 1000  # Winning score
        if my_pieces < 3:
            return -1000  # Losing score

        # Check if opponent is immobilized
        opponent_moves = sum(1 for pos in board if board[pos] == opponent_color and any(
            board.get(neigh) is None for neigh in NEIGHBORS.get(pos, [])))
        
        if opponent_moves == 0:
            return 1000  # Winning score

        # Heuristic scoring
        score = 10 * (my_pieces - opponent_pieces)  # More pieces is better
        my_mills = sum(1 for mill in MILLS if all(board.get(pos) == my_color for pos in mill))
        opponent_mills = sum(1 for mill in MILLS if all(board.get(pos) == opponent_color for pos in mill))
        
        score += 50 * (my_mills - opponent_mills)  # Mills are valuable

        return score


    def make_move(self):
        """Generate and return a valid random move"""
        if self.phase == "placing":
            valid_positions = [pos for pos in VALID_MOVES if self.board.get(pos) is None]
            if not valid_positions:
                return None

            target = random.choice(valid_positions)
            forms_mill = self.check_mill("h", target)
            remove_piece = self.get_removable_piece() if forms_mill else "r0"
            return f"h{1 if self.my_color == 'X' else 2} {target} {remove_piece}"

        else:  # moving or flying
            valid_moves = self.get_valid_moves()
            if not valid_moves:
                return None

            from_pos, to_pos = random.choice(valid_moves)
            forms_mill = self.check_mill(from_pos, to_pos)
            remove_piece = self.get_removable_piece() if forms_mill else "r0"
            return f"{from_pos} {to_pos} {remove_piece}"

    def update_game_state(self, move):
        """Update internal game state based on a move"""
        parts = move.split()

        if parts[0].startswith('h'):  # placing phase
            color = 'X' if parts[0] == 'h1' else 'O'
            position = parts[1]
            self.board[position] = color
            if color == self.my_color:
                self.my_pieces.append(position)
                self.pieces_in_hand -= 1
            else:
                self.opponent_pieces.append(position)
        else:  # moving or flying phase
            from_pos, to_pos = parts[0], parts[1]
            color = self.board.get(from_pos)

            if from_pos in self.board:
                del self.board[from_pos]
            self.board[to_pos] = color

            if color == self.my_color:
                self.my_pieces.remove(from_pos)
                self.my_pieces.append(to_pos)
            else:
                self.opponent_pieces.remove(from_pos)
                self.opponent_pieces.append(to_pos)

        # Handle piece removal
        if parts[2] != "r0":
            remove_pos = parts[2]
            if remove_pos in self.board:
                del self.board[remove_pos]
                if remove_pos in self.my_pieces:
                    self.my_pieces.remove(remove_pos)
                elif remove_pos in self.opponent_pieces:
                    self.opponent_pieces.remove(remove_pos)

        # Update game phase
        if self.pieces_in_hand == 0:
            if len(self.my_pieces) <= 3:
                self.phase = "flying"
            else:
                self.phase = "moving"

    def minimax(board, depth, is_maximizing, my_color, opponent_color, alpha, beta):
        """
        Minimax function with alpha-beta pruning to evaluate the best move.

        :param board: Dictionary representing the board state {position: 'X' or 'O' or None}.
        :param depth: Current depth in the minimax search tree.
        :param is_maximizing: Boolean indicating whether we are maximizing or minimizing.
        :param my_color: The color of the current player ('X' for blue, 'O' for orange).
        :param opponent_color: The color of the opponent.
        :param alpha: Alpha value for pruning.
        :param beta: Beta value for pruning.
        :return: The best score for the given board configuration.
        """
        if depth == 0 or is_terminal_state(board, my_color, opponent_color):
            return evaluate_board(board, my_color, opponent_color)

        valid_moves = get_valid_moves(board, my_color if is_maximizing else opponent_color)

        if is_maximizing:
            max_eval = float('-inf')
            for move in valid_moves:
                new_board = simulate_move(board, move, my_color)
                eval_score = minimax(new_board, depth - 1, False, my_color, opponent_color, alpha, beta)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Beta cut-off
            return max_eval
        else:
            min_eval = float('inf')
            for move in valid_moves:
                new_board = simulate_move(board, move, opponent_color)
                eval_score = minimax(new_board, depth - 1, True, my_color, opponent_color, alpha, beta)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha cut-off
            return min_eval
        
    def is_terminal_state(board, my_color, opponent_color):
        """
        Checks if the game has reached a terminal state (win, loss, draw).

        :param board: The current board state.
        :param my_color: The current player's color.
        :param opponent_color: The opponent's color.
        :return: True if the game is over, False otherwise.
        """
        my_pieces = sum(1 for pos in board if board[pos] == my_color)
        opponent_pieces = sum(1 for pos in board if board[pos] == opponent_color)

        if my_pieces < 3 or opponent_pieces < 3:
            return True  # A player has lost
        if not get_valid_moves(board, opponent_color):
            return True  # Opponent is immobilized (win for current player)
        return False

    def get_valid_moves(board, player_color):
        """
        Returns a list of valid moves for the given player.

        :param board: The current board state.
        :param player_color: The color of the player to get moves for.
        :return: List of valid moves.
        """
        moves = []
        for piece in [pos for pos in board if board[pos] == player_color]:
            for neighbor in NEIGHBORS.get(piece, []):
                if board.get(neighbor) is None:
                    moves.append((piece, neighbor))  # Move from piece to neighbor
        return moves

    def simulate_move(board, move, player_color):
        """
        Simulates a move and returns a new board state.

        :param board: The current board state.
        :param move: The move to simulate (tuple: (from_pos, to_pos)).
        :param player_color: The color of the player making the move.
        :return: A new board dictionary after the move.
        """
        new_board = board.copy()
        from_pos, to_pos = move
        new_board[from_pos] = None
        new_board[to_pos] = player_color
        return new_board


def main():
    player = LaskerMorrisPlayer()

    # Get color assignment
    color = input().strip()
    player.initialize_game(color)

    while True:
        try:
            if color == "blue":
                # Make move if it's our turn
                move = player.make_move()
                if move:
                    print(move, flush=True)
                    player.update_game_state(move)
                else:
                    break

                # Get opponent's move
                opponent_move = input().strip()
                if opponent_move.startswith("END"):
                    break
                player.update_game_state(opponent_move)
            else:
                # Get opponent's move
                opponent_move = input().strip()
                if opponent_move.startswith("END"):
                    break
                player.update_game_state(opponent_move)

                # Make our move
                move = player.make_move()
                if move:
                    print(move, flush=True)
                    player.update_game_state(move)
                else:
                    break

        except EOFError:
            break


if __name__ == "__main__":
    main()