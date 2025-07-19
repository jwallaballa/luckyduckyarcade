import random


class TicTacToeGame:
    def __init__(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.human_player = None  # Will be 'X' or 'O'
        self.ai_player = None     # Will be the opposite of human_player
        self.current_player = "X"
        self.game_over = False
        self.winner = None
        self.state = "CHOICE"  # "CHOICE", "PLAYING", or "GAME_OVER"

    def reset(self):
        """Reset the game to its initial state."""
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.human_player = None
        self.ai_player = None
        self.current_player = "X"
        self.game_over = False
        self.winner = None
        self.state = "CHOICE"

    def render(self):
        """Return a string representation of the game board."""
        output = ""
        if self.state == "CHOICE":
            output += "WELCOME TO TIC-TAC-TOE!\n\n"
            output += "CHOOSE YOUR SIDE: TYPE 'X' OR 'O'\n"
            return output

        output += "  0   1   2\n"
        output += "-------------\n"
        for i, row in enumerate(self.board):
            output += f"{i} | {' | '.join(row)} |\n"
            output += "-------------\n"

        if self.game_over:
            if self.winner:
                output += f"\nPLAYER {self.winner} WINS!\n"
            else:
                output += "\nIT'S A DRAW!\n"
            output += "\nGAME OVER. PRESS RESET TO PLAY AGAIN."
        else:
            output += f"\nPLAYER {self.current_player}'s TURN."
            if self.current_player == self.human_player:
                output += " ENTER ROW,COL (E.G., '0,0'):\n"
            else:
                output += " (AI IS THINKING...)\n"
        return output

    def check_win(self, player):
        """Check if the given player has won."""
        # Rows and columns
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)):
                return True
            if all(self.board[j][i] == player for j in range(3)):
                return True
        # Diagonals
        if (
            self.board[0][0] == player and
            self.board[1][1] == player and
            self.board[2][2] == player
        ) or (
            self.board[0][2] == player and
            self.board[1][1] == player and
            self.board[2][0] == player
        ):
            return True
        return False

    def is_board_full(self):
        """Return True if the board is full."""
        return all(cell != " " for row in self.board for cell in row)

    def make_move(self, row, col, player):
        """Make a move for a player if the space is free."""
        if not (0 <= row <= 2 and 0 <= col <= 2):
            return False
        if self.board[row][col] != " ":
            return False

        self.board[row][col] = player

        if self.check_win(player):
            self.winner = player
            self.game_over = True
            self.state = "GAME_OVER"
        elif self.is_board_full():
            self.game_over = True
            self.state = "GAME_OVER"
        else:
            self.current_player = "O" if self.current_player == "X" else "X"
        return True

    def get_available_moves(self):
        """Return list of available move tuples (row, col)."""
        return [
            (r, c)
            for r in range(3)
            for c in range(3)
            if self.board[r][c] == " "
        ]

    def ai_make_move(self):
        """AI logic to choose and make a move."""
        moves = self.get_available_moves()
        if not moves:
            return False

        # 1. Win if possible
        for r, c in moves:
            self.board[r][c] = self.ai_player
            if self.check_win(self.ai_player):
                self.winner = self.ai_player
                self.game_over = True
                self.state = "GAME_OVER"
                return True
            self.board[r][c] = " "

        # 2. Block opponent
        for r, c in moves:
            self.board[r][c] = self.human_player
            if self.check_win(self.human_player):
                self.board[r][c] = self.ai_player
                if self.is_board_full():
                    self.game_over = True
                    self.state = "GAME_OVER"
                else:
                    self.current_player = self.human_player
                return True
            self.board[r][c] = " "

        # 3. Take center
        if (1, 1) in moves:
            self.make_move(1, 1, self.ai_player)
            return True

        # 4. Take corners
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        random.shuffle(corners)
        for r, c in corners:
            if (r, c) in moves:
                self.make_move(r, c, self.ai_player)
                return True

        # 5. Take sides
        sides = [(0, 1), (1, 0), (1, 2), (2, 1)]
        random.shuffle(sides)
        for r, c in sides:
            if (r, c) in moves:
                self.make_move(r, c, self.ai_player)
                return True

        # 6. Fallback
        r, c = random.choice(moves)
        self.make_move(r, c, self.ai_player)
        return True

    def play(self, user_input):
        """Handle user input and process game logic."""
        user_input = user_input.strip().upper()

        if self.state == "CHOICE":
            if user_input in ["X", "O"]:
                self.human_player = user_input
                self.ai_player = "O" if user_input == "X" else "X"
                self.state = "PLAYING"
                if self.current_player == self.ai_player:
                    self.ai_make_move()
                return self.render()
            return self.render() + "\nINVALID CHOICE. PLEASE TYPE 'X' OR 'O'."

        if self.game_over:
            return self.render()

        if self.current_player == self.human_player:
            parts = user_input.split(',')
            if len(parts) == 2:
                try:
                    row = int(parts[0].strip())
                    col = int(parts[1].strip())
                    if self.make_move(row, col, self.human_player):
                        if not self.game_over and self.current_player == self.ai_player:
                            self.ai_make_move()
                        return self.render()
                    return (
                        self.render() +
                        "\nINVALID MOVE. SPOT TAKEN OR OUT OF BOUNDS. TRY AGAIN (E.G., 0,0)."
                    )
                except ValueError:
                    return (
                        self.render() +
                        "\nINVALID INPUT. PLEASE ENTER ROW,COL (E.G., 0,0)."
                    )
            return self.render() + "\nINVALID FORMAT. USE ROW,COL (E.G., 0,0)."
        return self.render() + "\nIT'S THE AI'S TURN. PLEASE WAIT."

    def to_dict(self):
        """Convert game state to a dictionary."""
        return {
            'board': self.board,
            'human_player': self.human_player,
            'ai_player': self.ai_player,
            'current_player': self.current_player,
            'game_over': self.game_over,
            'winner': self.winner,
            'state': self.state,
        }

    @classmethod
    def from_dict(cls, data):
        """Restore a game instance from a dictionary."""
        game = cls()
        game.board = data['board']
        game.current_player = data['current_player']
        game.game_over = data['game_over']
        game.winner = data['winner']
        game.human_player = data.get('human_player')
        game.ai_player = data.get('ai_player')
        game.state = data.get(
            'state',
            'PLAYING' if game.human_player else 'CHOICE'
        )
        return game
