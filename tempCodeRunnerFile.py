import pygame
import random
from collections import deque
from enum import Enum

# Game States
class GameState(Enum):
    MENU = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.is_hovered = False

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2, border_radius=12)
        
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            was_hovered = self.is_hovered
            self.is_hovered = self.rect.collidepoint(event.pos)
            self.current_color = self.hover_color if self.is_hovered else self.color
            # Return True if we just started hovering
            return self.is_hovered and not was_hovered
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

class SnakeGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()  # Initialize the sound mixer
        
        self.WIDTH = 800
        self.HEIGHT = 600
        self.BLOCK_SIZE = 20
        self.INITIAL_SPEED = 8
        self.SPEED_INCREMENT = 0.5
        self.MAX_SPEED = 25
        
        # Load sound effects
        self.sounds = {
            'eat': pygame.mixer.Sound('sounds/eat.wav'),
            'game_over': pygame.mixer.Sound('sounds/game_over.wav'),
            'button_hover': pygame.mixer.Sound('sounds/hover.wav'),
            'button_click': pygame.mixer.Sound('sounds/click.wav')
        }
        
        # Set volume for all sounds
        for sound in self.sounds.values():
            sound.set_volume(0.3)
        
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Snake Game with Menu')
        self.clock = pygame.time.Clock()
        
        # Initialize fonts
        self.title_font = pygame.font.Font(None, 74)
        self.button_font = pygame.font.Font(None, 36)
        
        # Create buttons
        button_width = 200
        button_height = 50
        button_x = self.WIDTH // 2 - button_width // 2
        start_y = self.HEIGHT // 2 - 30
        
        self.buttons = {
            'start': Button(button_x, start_y, button_width, button_height, 
                          'New Game', (0, 100, 0), (0, 150, 0)),
            'resume': Button(button_x, start_y + 70, button_width, button_height, 
                           'Resume Game', (0, 100, 0), (0, 150, 0)),
            'quit': Button(button_x, start_y + 140, button_width, button_height, 
                          'Quit Game', (139, 0, 0), (189, 0, 0))
        }
        
        self.create_background()
        self.game_state = GameState.MENU
        self.reset_game()

    def create_background(self):
        self.background = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.background.fill((0, 20, 0))
        
        for x in range(0, self.WIDTH, self.BLOCK_SIZE):
            pygame.draw.line(self.background, (0, 40, 0), (x, 0), (x, self.HEIGHT))
        for y in range(0, self.HEIGHT, self.BLOCK_SIZE):
            pygame.draw.line(self.background, (0, 40, 0), (0, y), (self.WIDTH, y))

    def reset_game(self):
        center_x = (self.WIDTH // self.BLOCK_SIZE // 2) * self.BLOCK_SIZE
        center_y = (self.HEIGHT // self.BLOCK_SIZE // 2) * self.BLOCK_SIZE
        self.snake = deque([
            (center_x, center_y),
            (center_x - self.BLOCK_SIZE, center_y),
            (center_x - 2 * self.BLOCK_SIZE, center_y)
        ])
        self.direction = Direction.RIGHT
        self.score = 0
        self.speed = self.INITIAL_SPEED
        self.food = self.generate_food()
        self.food_effect_radius = 0
        self.food_effect_growing = True

    def generate_food(self):
        snake_positions = set(self.snake)
        while True:
            x = random.randrange(1, (self.WIDTH - self.BLOCK_SIZE) // self.BLOCK_SIZE) * self.BLOCK_SIZE
            y = random.randrange(1, (self.HEIGHT - self.BLOCK_SIZE) // self.BLOCK_SIZE) * self.BLOCK_SIZE
            food = (x, y)
            if food not in snake_positions:
                return food

    def handle_menu_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if self.game_state == GameState.PLAYING:
                    self.game_state = GameState.PAUSED
                elif self.game_state == GameState.PAUSED:
                    self.game_state = GameState.PLAYING
            
            # Handle button events
            if self.game_state in [GameState.MENU, GameState.PAUSED, GameState.GAME_OVER]:
                for button_name, button in self.buttons.items():
                    # Check for hover sound
                    if button.handle_event(event) and event.type == pygame.MOUSEMOTION:
                        self.sounds['button_hover'].play()
                    # Check for click
                    elif event.type == pygame.MOUSEBUTTONDOWN and button.is_hovered:
                        self.sounds['button_click'].play()
                        if button_name == 'start':
                            self.reset_game()
                            self.game_state = GameState.PLAYING
                        elif button_name == 'resume':
                            if len(self.snake) > 0:  # Only resume if there's a game to resume
                                self.game_state = GameState.PLAYING
                        elif button_name == 'quit':
                            return False
        return True

    def handle_game_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = GameState.PAUSED
                elif event.key == pygame.K_UP and self.direction != Direction.DOWN:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                    self.direction = Direction.DOWN
                elif event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
        return True

    def update(self):
        if self.game_state != GameState.PLAYING:
            return

        if self.food_effect_growing:
            self.food_effect_radius += 0.5
            if self.food_effect_radius >= 5:
                self.food_effect_growing = False
        else:
            self.food_effect_radius -= 0.5
            if self.food_effect_radius <= 0:
                self.food_effect_growing = True

        head = self.snake[0]
        if self.direction == Direction.RIGHT:
            new_head = (head[0] + self.BLOCK_SIZE, head[1])
        elif self.direction == Direction.LEFT:
            new_head = (head[0] - self.BLOCK_SIZE, head[1])
        elif self.direction == Direction.UP:
            new_head = (head[0], head[1] - self.BLOCK_SIZE)
        else:
            new_head = (head[0], head[1] + self.BLOCK_SIZE)

        if (new_head in set(list(self.snake)) or
            new_head[0] < 0 or new_head[0] >= self.WIDTH or
            new_head[1] < 0 or new_head[1] >= self.HEIGHT):
            self.sounds['game_over'].play()
            self.game_state = GameState.GAME_OVER
            return

        self.snake.appendleft(new_head)

        if new_head == self.food:
            self.sounds['eat'].play()
            self.score += 1
            self.speed = min(self.speed + self.SPEED_INCREMENT, self.MAX_SPEED)
            self.food = self.generate_food()
        else:
            self.snake.pop()

    def draw_snake_segment(self, pos, is_head=False):
        x, y = pos
        if is_head:
            pygame.draw.rect(self.screen, (0, 200, 0), 
                           (x, y, self.BLOCK_SIZE, self.BLOCK_SIZE))
            pygame.draw.rect(self.screen, (0, 255, 0), 
                           (x + 2, y + 2, self.BLOCK_SIZE - 4, self.BLOCK_SIZE - 4))
            
            eye_color = (0, 0, 0)
            if self.direction == Direction.RIGHT:
                pygame.draw.circle(self.screen, eye_color, (x + 15, y + 5), 2)
                pygame.draw.circle(self.screen, eye_color, (x + 15, y + 15), 2)
            elif self.direction == Direction.LEFT:
                pygame.draw.circle(self.screen, eye_color, (x + 5, y + 5), 2)
                pygame.draw.circle(self.screen, eye_color, (x + 5, y + 15), 2)
            elif self.direction == Direction.UP:
                pygame.draw.circle(self.screen, eye_color, (x + 5, y + 5), 2)
                pygame.draw.circle(self.screen, eye_color, (x + 15, y + 5), 2)
            else:
                pygame.draw.circle(self.screen, eye_color, (x + 5, y + 15), 2)
                pygame.draw.circle(self.screen, eye_color, (x + 15, y + 15), 2)
        else:
            pygame.draw.rect(self.screen, (0, 180, 0), 
                           (x, y, self.BLOCK_SIZE, self.BLOCK_SIZE))
            pygame.draw.rect(self.screen, (0, 220, 0), 
                           (x + 2, y + 2, self.BLOCK_SIZE - 4, self.BLOCK_SIZE - 4))

    def draw_menu(self):
        # Draw title
        title_text = "Snake Game"
        if self.game_state == GameState.PAUSED:
            title_text = "Game Paused"
        elif self.game_state == GameState.GAME_OVER:
            title_text = "Game Over!"
            
        title_surface = self.title_font.render(title_text, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 4))
        
        # Add shadow effect to title
        shadow_surface = self.title_font.render(title_text, True, (0, 0, 0))
        shadow_rect = shadow_surface.get_rect(center=(self.WIDTH // 2 + 2, self.HEIGHT // 4 + 2))
        
        self.screen.blit(shadow_surface, shadow_rect)
        self.screen.blit(title_surface, title_rect)

        # Draw score if game is paused or over
        if self.game_state in [GameState.PAUSED, GameState.GAME_OVER]:
            score_text = f"Score: {self.score}"
            score_surface = self.button_font.render(score_text, True, (255, 255, 255))
            score_rect = score_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 3))
            self.screen.blit(score_surface, score_rect)

        # Draw buttons
        for button in self.buttons.values():
            button.draw(self.screen, self.button_font)

        # Draw instructions
        if self.game_state == GameState.PLAYING:
            instructions = "Press ESC to pause"
            inst_surface = self.button_font.render(instructions, True, (255, 255, 255))
            inst_rect = inst_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT - 30))
            self.screen.blit(inst_surface, inst_rect)

    def draw_game(self):
        self.screen.blit(self.background, (0, 0))

        # Draw snake
        for i, segment in enumerate(self.snake):
            self.draw_snake_segment(segment, is_head=(i == 0))

        # Draw food
        pygame.draw.circle(self.screen, (255, 50, 50),
                         (self.food[0] + self.BLOCK_SIZE // 2,
                          self.food[1] + self.BLOCK_SIZE // 2),
                         self.BLOCK_SIZE // 2 + self.food_effect_radius)
        pygame.draw.circle(self.screen, (255, 0, 0),
                         (self.food[0] + self.BLOCK_SIZE // 2,
                          self.food[1] + self.BLOCK_SIZE // 2),
                         self.BLOCK_SIZE // 2)

        # Draw score
        score_text = f'Score: {self.score} - Speed: {self.speed:.1f}'
        text = self.button_font.render(score_text, True, (255, 255, 255))
        shadow = self.button_font.render(score_text, True, (0, 0, 0))
        self.screen.blit(shadow, (12, 12))
        self.screen.blit(text, (10, 10))

    def draw(self):
        self.screen.fill((0, 20, 0))  # Dark green background

        if self.game_state == GameState.PLAYING:
            self.draw_game()
        else:
            if self.game_state == GameState.PAUSED:
                self.draw_game()  # Draw game state in background when paused
                s = pygame.Surface((self.WIDTH, self.HEIGHT))  # Transparent overlay
                s.set_alpha(128)
                s.fill((0, 0, 0))
                self.screen.blit(s, (0, 0))
            self.draw_menu()

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            if self.game_state == GameState.PLAYING:
                running = self.handle_game_input()
                self.update()
            else:
                running = self.handle_menu_input()
            
            self.draw()
            self.clock.tick(self.speed if self.game_state == GameState.PLAYING else 60)

if __name__ == "__main__":
    game = SnakeGame()
    game.run()