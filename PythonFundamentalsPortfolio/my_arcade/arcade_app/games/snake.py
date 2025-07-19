# arcade_app/games/snake.py

'''
Simulates the Snake game on a 2D grid where the player controls a snake that moves around,
eats food to grow longer, and tries not to collide with itself or the walls.
It keeps track of score and game state and can render the game as ASCII art.
'''

import random

class AsciiSnakeGame:
    def __init__(self, width=60, height=20):
        self.width = width
        self.height = height
        self.snake = self._initialize_snake()
        self.food = self._generate_food()
        self.direction = 'RIGHT'
        self.score = 0
        self.game_over = False
        self.game_started = False # Flag to handle initial "Press Enter" state


    def _initialize_snake(self):
        head_x = self.width // 2
        head_y = self.height // 2
        return [(head_x, head_y)]

    def _generate_food(self):
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if (x, y) not in self.snake:
                return (x, y)

    def change_direction(self, new_direction):
        if self.game_over:
            return

        if new_direction == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        elif new_direction == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        elif new_direction == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        elif new_direction == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'

    def update(self):
        if self.game_over:
            return

        head_x, head_y = self.snake[0]

        if self.direction == 'UP':
            new_head = (head_x, head_y - 1)
        elif self.direction == 'DOWN':
            new_head = (head_x, head_y + 1)
        elif self.direction == 'LEFT':
            new_head = (head_x - 1, head_y)
        elif self.direction == 'RIGHT':
            new_head = (head_x + 1, head_y)

        # Check for collisions
        if not (0 <= new_head[0] < self.width and 0 <= new_head[1] < self.height):
            self.game_over = True
            return
        if new_head in self.snake:
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.food = self._generate_food()
        else:
            self.snake.pop()

    def reset(self):
        self.snake = self._initialize_snake()
        self.food = self._generate_food()
        self.direction = 'RIGHT'
        self.score = 0
        self.game_over = False
        self.game_started = False

    def play(self, command):
        if command.lower() == 'reset':
            self.reset()
            return self.render()
        return "Unknown command."


    def render(self, high_score_data=None):
        board_chars = [[" " for _ in range(self.width)] for _ in range(self.height)]

        # Place food
        board_chars[self.food[1]][self.food[0]] = "@"

        # Place snake
        for i, (x, y) in enumerate(self.snake):
            if i == 0: # Head
                board_chars[y][x] = "O"
            else: # Body
                board_chars[y][x] = "o"

        # Prepare score and high score lines
        current_score_display = f"SCORE: {self.score}"
        high_score_display = ""
        if high_score_data and high_score_data['score'] is not None:
            high_score_display = f"HIGH SCORE: {high_score_data['score']} ({high_score_data['initials']})"
        else:
            high_score_display = "HIGH SCORE: 0 (---)" # Default if no high score yet

        # Calculate padding to center/align scores
        # We'll put current score left-aligned and high score right-aligned in the middle line
        total_score_line_width = self.width
        # Calculate available space between current score and high score
        space_between = total_score_line_width - len(current_score_display) - len(high_score_display)
        if space_between < 1: # Ensure at least one space if too long
            space_between = 1
        score_line_content = f"{current_score_display}{' ' * space_between}{high_score_display}"

        # Pad the score line to fit the board width exactly, or truncate if it somehow exceeds
        score_line = score_line_content.ljust(self.width)[:self.width]

        # Construct the full ASCII output
        full_output_lines = []

        # Top border
        full_output_lines.append("#" * (self.width + 2))
        # Score line, centered
        full_output_lines.append(f"#{score_line}#")
        # Separator line
        full_output_lines.append("#" * (self.width + 2))

        # Add game board rows
        for r in range(self.height):
            row_chars = ["#"] + board_chars[r] + ["#"]
            full_output_lines.append("".join(row_chars))

        # Bottom border
        full_output_lines.append("#" * (self.width + 2))

        # Add game state messages below the board
        if self.game_over:
            full_output_lines.append(f"\n    GAME OVER! FINAL SCORE: {self.score}\n"
                                     f"    PRESS RESET GAME TO PLAY AGAIN GO BACK TO MENU")
        else:
            if not self.game_started:
                instructions_line = "PRESS ENTER TO START GAME".center(self.width)
                full_output_lines.append(f"\n    {instructions_line}\n")
            else:
                full_output_lines.append(f"\n    USE ARROW KEYS to move. Press 'R' to reset.")

        return "\n".join(full_output_lines)


    def to_dict(self):
        return {
            'width': self.width,
            'height': self.height,
            'snake': self.snake,
            'food': self.food,
            'direction': self.direction,
            'score': self.score,
            'game_over': self.game_over,
            'game_started': self.game_started,
        }

    @classmethod
    def from_dict(cls, data):
        game = cls(data['width'], data['height'])
        game.snake = [tuple(s) for s in data['snake']] # Ensure tuples after deserialization
        game.food = tuple(data['food']) # Ensure tuple
        game.direction = data['direction']
        game.score = data['score']
        game.game_over = data['game_over']
        game.game_started = data.get('game_started', True)
        return game