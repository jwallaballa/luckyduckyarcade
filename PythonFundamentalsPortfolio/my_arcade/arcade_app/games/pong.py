# arcade_app/games/pong.py

import random

class AsciiPongGame:
    def __init__(self, width=80, height=20):
        self.width = width
        self.height = height
        self.ball_x = width // 2
        self.ball_y = height // 2
        self.ball_dx = random.choice([-1, 1])
        self.ball_dy = random.choice([-1, 1])
        self.paddle_a_y = height // 2 - 2
        self.paddle_b_y = height // 2 - 2
        self.paddle_height = 5
        self.score_a = 0
        self.score_b = 0
        self.game_over = False
        self.max_score = 5
        self.paddle_a_move_direction = 0 # -1 for up, 1 for down, 0 for stop
        self.paddle_b_move_direction = 0 # -1 for up, 1 for down, 0 for stop
        self.game_started = False


    def change_paddle_direction(self, paddle_id, direction):
        if self.game_over:
            return
        if paddle_id == 'A':
            self.paddle_a_move_direction = direction
        elif paddle_id == 'B':
            self.paddle_b_move_direction = direction

    def update(self):
        if self.game_over:
            return

        # Move paddles based on their direction
        self.paddle_a_y += self.paddle_a_move_direction
        self.paddle_b_y = self.ball_y - (self.paddle_height // 2) # Simple AI

        # Keep paddles within bounds
        self.paddle_a_y = max(0, min(self.paddle_a_y, self.height - self.paddle_height))
        self.paddle_b_y = max(0, min(self.paddle_b_y, self.height - self.paddle_height))

        # Move ball
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        # Wall collision (top/bottom)
        if self.ball_y <= 0:  # Hits top wall
            self.ball_y = 0  # Ensure it stays within bounds
            self.ball_dy = random.choice([1, 1, 1, 2])  # Introduce more randomness for upward bounce
            # Consider a small horizontal change for more unpredictability, but keep it subtle
            # self.ball_dx = random.choice([-1, 1]) if random.random() < 0.2 else self.ball_dx # 20% chance to slightly alter horizontal direction
        elif self.ball_y >= self.height - 1:  # Hits bottom wall
            self.ball_y = self.height - 1  # Ensure it stays within bounds
            self.ball_dy = random.choice([-1, -1, -1, -2])  # Introduce more randomness for downward bounce
            # self.ball_dx = random.choice([-1, 1]) if random.random() < 0.2 else self.ball_dx

        # Paddle collision (Player A - left)
        if self.ball_x <= 1:  # Ball is at paddle A's column
            if self.paddle_a_y <= self.ball_y < self.paddle_a_y + self.paddle_height:
                self.ball_dx *= -1
                self.ball_x = 2
                # Introduce randomness on paddle hit
                self.ball_dy = random.choice([-1, 1])  # Reset vertical direction on paddle hit
            else:
                self.score_b += 1  # Player B scores
                self.reset_ball()

        # Paddle collision (Player B - right)
        if self.ball_x >= self.width - 2:  # Ball is at paddle B's column
            if self.paddle_b_y <= self.ball_y < self.paddle_b_y + self.paddle_height:
                self.ball_dx *= -1
                self.ball_x = self.width - 3
                # Introduce randomness on paddle hit
                self.ball_dy = random.choice([-1, 1])  # Reset vertical direction on paddle hit
            else:
                self.score_a += 1  # Player A scores
                self.reset_ball()

        # Check for game over
        if self.score_a >= self.max_score or self.score_b >= self.max_score:
            self.game_over = True
            self.score = self.score_a # Set 'score' attribute for high score saving

    def reset_ball(self):
        self.ball_x = self.width // 2
        self.ball_y = self.height // 2
        self.ball_dx = random.choice([-1, 1])
        self.ball_dy = random.choice([-1, 1])

    def reset(self):
        self.ball_x = self.width // 2
        self.ball_y = self.height // 2
        self.ball_dx = random.choice([-1, 1])
        self.ball_dy = random.choice([-1, 1])
        self.paddle_a_y = self.height // 2 - 2
        self.paddle_b_y = self.height // 2 - 2
        self.score_a = 0
        self.score_b = 0
        self.game_over = False
        self.paddle_a_move_direction = 0
        self.paddle_b_move_direction = 0
        self.game_started = False
        self.score = 0

    def play(self, command):
        if command.lower() == 'reset':
            self.reset()
            return self.render()
        return "Unknown command."


    def render(self, high_score_data=None): # Keep the parameter
        board = [[" " for _ in range(self.width)] for _ in range(self.height)]

        # Place paddles
        for i in range(self.paddle_height):
            board[self.paddle_a_y + i][0] = "|"
            board[self.paddle_b_y + i][self.width - 1] = "|"

        # Place ball
        board[self.ball_y][self.ball_x] = "O"

        # Prepare score line (ONLY current game scores)
        current_score_display = f"P1: {self.score_a} | P2: {self.score_b}"

        # Center the score line
        score_line = current_score_display.center(self.width)


        # Construct the full ASCII output
        full_output_lines = []

        # Top border
        full_output_lines.append("#" * (self.width + 2))
        # Score line (centered)
        full_output_lines.append(f"#{score_line}#")
        # Separator line
        full_output_lines.append("#" * (self.width + 2))

        # Add game board rows
        for r in range(self.height):
            row_chars = ["#"] + board[r] + ["#"]
            full_output_lines.append("".join(row_chars))

        # Bottom border
        full_output_lines.append("#" * (self.width + 2))

        # Game over / Instructions messages below the board
        if self.game_over:
            winner = "PLAYER A" if self.score_a >= self.max_score else "PLAYER B"
            full_output_lines.append(f"\n    GAME OVER! {winner} WINS!\n"
                                     f"    PRESS 'R' TO RESTART OR 'BACK TO MENU' TO EXIT.")
        else:
            if not self.game_started:
                instructions_line = "PRESS ENTER TO START GAME".center(self.width)
                full_output_lines.append(f"\n    {instructions_line}\n")
            else:
                 full_output_lines.append(f"\n    USE 'W'/'S' to move your paddle. First to {self.max_score} wins.")

        return "\n".join(full_output_lines)

    def to_dict(self):
        return {
            'width': self.width,
            'height': self.height,
            'ball_x': self.ball_x,
            'ball_y': self.ball_y,
            'ball_dx': self.ball_dx,
            'ball_dy': self.ball_dy,
            'paddle_a_y': self.paddle_a_y,
            'paddle_b_y': self.paddle_b_y,
            'score_a': self.score_a,
            'score_b': self.score_b,
            'game_over': self.game_over,
            'max_score': self.max_score,  # Ensure this is always present when serializing
            'paddle_a_move_direction': self.paddle_a_move_direction,
            'paddle_b_move_direction': self.paddle_b_move_direction,
            'game_started': self.game_started,
            'score': self.score
        }

    @classmethod
    def from_dict(cls, data):
        game = cls(data['width'], data['height'])
        game.ball_x = data['ball_x']
        game.ball_y = data['ball_y']
        game.ball_dx = data['ball_dx']
        game.ball_dy = data['ball_dy']
        game.paddle_a_y = data['paddle_a_y']
        game.paddle_b_y = data['paddle_b_y']
        game.score_a = data['score_a']
        game.score_b = data['score_b']
        game.game_over = data['game_over']
        # --- FIX THIS LINE ---
        game.max_score = data.get('max_score', 5)  # Use .get() with a default value (e.g., 5, matching your __init__)
        # --- End Fix ---
        game.paddle_a_move_direction = data.get('paddle_a_move_direction',
                                                0)  # Also good to add defaults for new fields
        game.paddle_b_move_direction = data.get('paddle_b_move_direction',
                                                0)  # Also good to add defaults for new fields
        game.game_started = data.get('game_started', False)  # Already using .get(), good
        game.score = data.get('score', 0)  # Already using .get(), good
        return game