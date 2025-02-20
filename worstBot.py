import random
import time
from copy import deepcopy

VALID_MOVES = ["a1", "a4", "a7", "b2", "b4", "b6", "c3", "c4", "c5",
               "d1", "d2", "d3", "d5", "d6", "d7", "e3", "e4", "e5",
               "f2", "f4", "f6", "g1", "g4", "g7"]

# Keep existing NEIGHBORS and MILLS definitions...
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


class GameState:
    def __init__(self, board, my_pieces, opponent_pieces, phase, pieces_in_hand):
        self.board = board
        self.my_pieces = my_pieces
        self.opponent_pieces = opponent_pieces
        self.phase = phase
        self.pieces_in_hand = pieces_in_hand


class LaskerMorrisPlayer:
    def __init__(self):
        self.board = {}
        self.my_color = None
        self.opponent_color = None
        self.my_pieces = []
        self.opponent_pieces = []
        self.phase = "placing"
        self.pieces_in_hand = 10
        self.max_depth = 4  # Adjust based on performance
        self.time_limit = 0.95  # 950ms time limit for moves
        self.start_time = None
        self.transposition_table = {}  # Add transposition table

    def initialize_game(self, color):
        self.my_color = 'X' if color == "blue" else 'O'
        self.opponent_color = 'O' if color == "blue" else 'X'
        for pos in VALID_MOVES:
            self.board[pos] = None

    def evaluate_position(self, state, is_terminal=False):
        """
        Evaluation function for non-terminal states
        Returns higher scores for better positions for the current player
        """
        if is_terminal:
            if len(state.my_pieces) < 3:
                return -1000  # Loss
            if len(state.opponent_pieces) < 3:
                return 1000  # Win

        score = 0

        # Piece advantage
        score += 10 * (len(state.my_pieces) - len(state.opponent_pieces))

        # Mill potential
        my_mills = self.count_mills(state.board, state.my_pieces, True)
        opp_mills = self.count_mills(state.board, state.opponent_pieces, False)
        score += 50 * (my_mills - opp_mills)

        # Mobility
        my_mobility = self.count_possible_moves(state, True)
        opp_mobility = self.count_possible_moves(state, False)
        score += 5 * (my_mobility - opp_mobility)

        # Control of center positions
        center_positions = ["b4", "d4", "f4", "d2", "d6"]
        my_center = sum(1 for pos in center_positions if pos in state.my_pieces)
        opp_center = sum(1 for pos in center_positions if pos in state.opponent_pieces)
        score += 3 * (my_center - opp_center)

        return score

    def count_mills(self, board, pieces, is_max_player):
        color = self.my_color if is_max_player else self.opponent_color
        mill_count = 0
        for mill in MILLS:
            if all(pos in pieces and board.get(pos) == color for pos in mill):
                mill_count += 1
        return mill_count

    def count_possible_moves(self, state, is_max_player):
        pieces = state.my_pieces if is_max_player else state.opponent_pieces
        count = 0

        if state.phase == "placing":
            return len([pos for pos in VALID_MOVES if state.board.get(pos) is None])
        elif state.phase == "flying" and len(pieces) <= 3:
            return len([(p, t) for p in pieces
                        for t in VALID_MOVES if state.board.get(t) is None])
        else:
            return len([(p, t) for p in pieces
                        for t in NEIGHBORS[p] if state.board.get(t) is None])

    def is_time_up(self):
        return time.time() - self.start_time > self.time_limit

    def iterative_deepening_search(self, state):
        """Iterative deepening search with transposition table."""
        self.start_time = time.time()
        best_move = None
        current_depth = 1

        try:
            while time.time() - self.start_time < self.time_limit:
                value, move = self.alpha_beta_search(
                    state,
                    current_depth,
                    float('-inf'),
                    float('inf'),
                    True,
                    True  # Use move ordering
                )
                if move:
                    best_move = move
                current_depth += 1
                if value >= 1000:  # Winning move found
                    break
        except TimeoutError:
            pass

        return best_move

    def alpha_beta_search(self, state, depth, alpha, beta, is_max_player, use_move_ordering=True):
        """Alpha-beta pruning with heuristics."""
        if self.is_time_up():
            raise TimeoutError

        state_hash = self.hash_state(state)
        if state_hash in self.transposition_table:
            stored_depth, stored_value, stored_move = self.transposition_table[state_hash]
            if stored_depth >= depth:
                return stored_value, stored_move

        if depth == 0:
            return self.evaluate_position(state), None

        possible_moves = self.get_possible_moves(state, is_max_player)
        if not possible_moves:
            return -1000 if is_max_player else 1000, None

        if use_move_ordering:
            possible_moves = self.order_moves(state, possible_moves, is_max_player)

        best_value, best_move = (float('-inf'), None) if is_max_player else (float('inf'), None)

        for move in possible_moves:
            new_state = self.apply_move(state, move, is_max_player)
            value, _ = self.alpha_beta_search(new_state, depth - 1, alpha, beta, not is_max_player,
                                              use_move_ordering)

            if is_max_player:
                if value > best_value:
                    best_value, best_move = value, move
                alpha = max(alpha, best_value)
            else:
                if value < best_value:
                    best_value, best_move = value, move
                beta = min(beta, best_value)

            if beta <= alpha:
                break  # Prune

        self.transposition_table[state_hash] = (depth, best_value, best_move)
        return best_value, best_move
    def order_moves(self, state, moves, is_max_player):
        """Order moves based on heuristics for better pruning"""
        move_scores = []

        for move in moves:
            score = 0

            # Prioritize moves that form mills
            if self.check_mill(move[0] if move[0] != "h" else "h", move[1]):
                score += 100

            # Prioritize moves to center positions
            if move[1] in ["b4", "d4", "f4", "d2", "d6"]:
                score += 50

            # Prioritize moves that block opponent mills
            new_state = self.apply_move(state, move, is_max_player)
            opponent_mills = self.count_mills(new_state.board,
                                              new_state.opponent_pieces if is_max_player else new_state.my_pieces,
                                              not is_max_player)
            score -= opponent_mills * 30

            move_scores.append((score, move))

        # Sort moves by score in descending order
        move_scores.sort(reverse=True)
        return [move for _, move in move_scores]

    def hash_state(self, state):
        """Create a hash of the current state for the transposition table"""
        board_str = ''.join(str(state.board.get(pos, 'E')) for pos in sorted(VALID_MOVES))
        return hash((board_str,
                     tuple(sorted(state.my_pieces)),
                     tuple(sorted(state.opponent_pieces)),
                     state.phase,
                     state.pieces_in_hand))

    def get_possible_moves(self, state, is_max_player):
        moves = []
        pieces = state.my_pieces if is_max_player else state.opponent_pieces
        color = self.my_color if is_max_player else self.opponent_color

        if state.phase == "placing":
            for pos in VALID_MOVES:
                if state.board.get(pos) is None:
                    moves.append(("h", pos))
        elif state.phase == "flying" and len(pieces) <= 3:
            for piece in pieces:
                for target in VALID_MOVES:
                    if state.board.get(target) is None:
                        moves.append((piece, target))
        else:
            for piece in pieces:
                for target in NEIGHBORS[piece]:
                    if state.board.get(target) is None:
                        moves.append((piece, target))

        return moves

    def apply_move(self, old_state, move, is_max_player):
        state = GameState(
            deepcopy(old_state.board),
            old_state.my_pieces.copy(),
            old_state.opponent_pieces.copy(),
            old_state.phase,
            old_state.pieces_in_hand
        )

        if move[0] == "h":  # placing phase
            position = move[1]
            color = self.my_color if is_max_player else self.opponent_color
            state.board[position] = color
            if is_max_player:
                state.my_pieces.append(position)
                state.pieces_in_hand -= 1
            else:
                state.opponent_pieces.append(position)
        else:  # moving or flying phase
            from_pos, to_pos = move
            color = self.my_color if is_max_player else self.opponent_color

            state.board[from_pos] = None
            state.board[to_pos] = color

            if is_max_player:
                state.my_pieces.remove(from_pos)
                state.my_pieces.append(to_pos)
            else:
                state.opponent_pieces.remove(from_pos)
                state.opponent_pieces.append(to_pos)

        return state

    def make_move(self):
        """Generate the best move with alpha-beta pruning and iterative deepening."""
        current_state = GameState(
            self.board.copy(),
            self.my_pieces.copy(),
            self.opponent_pieces.copy(),
            self.phase,
            self.pieces_in_hand
        )
        best_move = self.iterative_deepening_search(current_state)

        if not best_move:
            return None

        if best_move[0] == "h":
            remove_piece = self.get_removable_piece() if self.check_mill("h",
                                                                         best_move[1]) else "r0"
            return f"h{1 if self.my_color == 'X' else 2} {best_move[1]} {remove_piece}"
        else:
            from_pos, to_pos = best_move
            remove_piece = self.get_removable_piece() if self.check_mill(from_pos, to_pos) else "r0"
            return f"{from_pos} {to_pos} {remove_piece}"

    # Keep existing methods: check_mill, get_removable_piece, update_game_state, etc.
    def check_mill(self, source, target):
        if source in self.board:
            old_source_value = self.board[source]
            self.board[source] = None
        else:
            old_source_value = None

        self.board[target] = self.my_color

        forms_mill = False
        for mill in MILLS:
            if target in mill:
                stones_in_mill = sum(1 for pos in mill if self.board.get(pos) == self.my_color)
                if stones_in_mill == 3:
                    forms_mill = True
                    break

        if source in self.board:
            self.board[source] = old_source_value
        self.board[target] = None

        return forms_mill

    def get_removable_piece(self):
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


    def update_game_state(self, move):
        parts = move.split()

        if parts[0].startswith('h'):
            color = 'X' if parts[0] == 'h1' else 'O'
            position = parts[1]
            self.board[position] = color
            if color == self.my_color:
                self.my_pieces.append(position)
                self.pieces_in_hand -= 1
            else:
                self.opponent_pieces.append(position)
        else:
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

        if parts[2] != "r0":
            remove_pos = parts[2]
            if remove_pos in self.board:
                del self.board[remove_pos]
                if remove_pos in self.my_pieces:
                    self.my_pieces.remove(remove_pos)
                elif remove_pos in self.opponent_pieces:
                    self.opponent_pieces.remove(remove_pos)

        if self.pieces_in_hand == 0:
            if len(self.my_pieces) <= 3:
                self.phase = "flying"
            else:
                self.phase = "moving"

    # def minimax(board, depth, is_maximizing, my_color, opponent_color, alpha, beta):
    #     """
    #     Minimax function with alpha-beta pruning to evaluate the best move.

    #     :param board: Dictionary representing the board state {position: 'X' or 'O' or None}.
    #     :param depth: Current depth in the minimax search tree.
    #     :param is_maximizing: Boolean indicating whether we are maximizing or minimizing.
    #     :param my_color: The color of the current player ('X' for blue, 'O' for orange).
    #     :param opponent_color: The color of the opponent.
    #     :param alpha: Alpha value for pruning.
    #     :param beta: Beta value for pruning.
    #     :return: The best score for the given board configuration.
    #     """
    #     if depth == 0 or is_terminal_state(board, my_color, opponent_color):
    #         return evaluate_board(board, my_color, opponent_color)

    #     valid_moves = get_valid_moves(board, my_color if is_maximizing else opponent_color)

    #     if is_maximizing:
    #         max_eval = float('-inf')
    #         for move in valid_moves:
    #             new_board = simulate_move(board, move, my_color)
    #             eval_score = minimax(new_board, depth - 1, False, my_color, opponent_color, alpha, beta)
    #             max_eval = max(max_eval, eval_score)
    #             alpha = max(alpha, eval_score)
    #             if beta <= alpha:
    #                 break  # Beta cut-off
    #         return max_eval
    #     else:
    #         min_eval = float('inf')
    #         for move in valid_moves:
    #             new_board = simulate_move(board, move, opponent_color)
    #             eval_score = minimax(new_board, depth - 1, True, my_color, opponent_color, alpha, beta)
    #             min_eval = min(min_eval, eval_score)
    #             beta = min(beta, eval_score)
    #             if beta <= alpha:
    #                 break  # Alpha cut-off
    #         return min_eval
        
    # def is_terminal_state(board, my_color, opponent_color):
    #     """
    #     Checks if the game has reached a terminal state (win, loss, draw).

    #     :param board: The current board state.
    #     :param my_color: The current player's color.
    #     :param opponent_color: The opponent's color.
    #     :return: True if the game is over, False otherwise.
    #     """
    #     my_pieces = sum(1 for pos in board if board[pos] == my_color)
    #     opponent_pieces = sum(1 for pos in board if board[pos] == opponent_color)

    #     if my_pieces < 3 or opponent_pieces < 3:
    #         return True  # A player has lost
    #     if not get_valid_moves(board, opponent_color):
    #         return True  # Opponent is immobilized (win for current player)
    #     return False

    # def get_valid_moves(board, player_color):
    #     """
    #     Returns a list of valid moves for the given player.

    #     :param board: The current board state.
    #     :param player_color: The color of the player to get moves for.
    #     :return: List of valid moves.
    #     """
    #     moves = []
    #     for piece in [pos for pos in board if board[pos] == player_color]:
    #         for neighbor in NEIGHBORS.get(piece, []):
    #             if board.get(neighbor) is None:
    #                 moves.append((piece, neighbor))  # Move from piece to neighbor
    #     return moves

    # def simulate_move(board, move, player_color):
    #     """
    #     Simulates a move and returns a new board state.

    #     :param board: The current board state.
    #     :param move: The move to simulate (tuple: (from_pos, to_pos)).
    #     :param player_color: The color of the player making the move.
    #     :return: A new board dictionary after the move.
    #     """
    #     new_board = board.copy()
    #     from_pos, to_pos = move
    #     new_board[from_pos] = None
    #     new_board[to_pos] = player_color
    #     return new_board


def main():
    player = LaskerMorrisPlayer()
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