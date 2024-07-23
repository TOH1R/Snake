import pygame
import random
pygame.init()

WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
CELL_SIZE = 20

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    
    def __init__(self):
        self.body = [(5, 5), (4, 5), (3, 5)]  
        self.direction = RIGHT  
        self.grow = False 

    def move(self):
        head_x, head_y = self.body[0]
        new_dir_x, new_dir_y = self.direction
        new_head = ((head_x + new_dir_x) % (SCREEN_WIDTH // CELL_SIZE),
                    (head_y + new_dir_y) % (SCREEN_HEIGHT // CELL_SIZE))
        
        if new_head in self.body[1:]:
            return False
        
        self.body.insert(0, new_head)

        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

        return True

    def grow_snake(self):
        
        self.grow = True

    def change_direction(self, new_direction):
        
        if (new_direction[0] + self.direction[0] == 0) and (new_direction[1] + self.direction[1] == 0):
            return
        self.direction = new_direction

    def draw(self, screen):
        
        for segment in self.body:
            pygame.draw.rect(
                screen, GREEN, (segment[0]*CELL_SIZE, segment[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))


class Food:
    

    def __init__(self):
        
        self.position = (random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1),
                          random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1))

    def randomize_position(self):
        
        self.position = (random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1),
                          random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1))

    def draw(self, screen):
        
        pygame.draw.rect(
            screen, RED, (self.position[0]*CELL_SIZE, self.position[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))


class Game:
    

    def __init__(self, screen):
        
        self.screen = screen
        self.snake = Snake()
        self.food = Food()
        self.score = 0  
        self.level = 1  
        self.speed = 10  

    def check_collision(self):
        
        if self.snake.body[0] == self.food.position:
            self.snake.grow_snake()
            self.food.randomize_position()
            self.score += 1
            if self.score % 10 == 0:
                self.level_up()

    def level_up(self):
        self.level += 1
        self.speed += 3  

    def run(self):
        # Main game loop
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction(RIGHT)

            if not self.snake.move():
                running = False

            self.check_collision()
            self.screen.fill(BLACK)  # background color
            self.snake.draw(self.screen)
            self.food.draw(self.screen)

            font = pygame.font.Font(None, 36)
            score_text = font.render(f'Score: {self.score}', True, WHITE)
            level_text = font.render(f'Level: {self.level}', True, WHITE)
            self.screen.blit(score_text, (10, 10))
            self.screen.blit(level_text, (10, 40))

            pygame.display.flip()
            clock.tick(self.speed)


if __name__ == "__main__":

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game")

    game = Game(screen)
    game.run()

    pygame.quit()