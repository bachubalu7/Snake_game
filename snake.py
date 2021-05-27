import pygame
from pygame.locals import *
import time
import random

SIZE = 40
#BACKGROUND_COLOR = (110, 110, 5)
BACKGROUND_COLOR = (10, 8, 1)
class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("apple.jpg").convert()
        self.x = 520
        self.y = 520
        

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1,29)*SIZE
        self.y = random.randint(1,19)*SIZE

class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("block.jpg").convert()
        self.direction = 'right'

        self.length = 1
        self.x = [40]
        self.y = [40]
    #when snake is already moving right, snake cannot move left! so,to make snake move left the current direction of snake must not be right.
    def move_left(self):
        if self.direction!='right':
            self.direction = 'left'
    #when snake is already moving left, snake cannot move right! so,to make snake move right the current direction of snake must not be left.
    def move_right(self):
        if self.direction!='left':
            self.direction = 'right'
    #when snake is already moving down, snake cannot move up! so,to make snake move up the current direction of snake must not be down.
    def move_up(self):
        if self.direction!='down':
            self.direction = 'up'
    #when snake is already moving up, snake cannot move down! so,to make snake move down the current direction of snake must not be up.
    def move_down(self):
        if self.direction!='up':
            self.direction = 'down'

    def walk(self):
        # update body
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        # update head
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        self.parent_screen.fill(BACKGROUND_COLOR)

        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))
        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake And Apple Game")
        icon=pygame.image.load("snake1.png")
        pygame.display.set_icon(icon)        
        self.surface = pygame.display.set_mode((1200, 800))
        #self.surface.blit(img11,(300,300))
        self.highest_score=1
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)


    def is_collision(self, x1, y1, x2, y2):
        #x1 is taken as -10 but not at 0 because we want to travel at boundaries also so if we go beyond that we are out ,same with all boundaries
        if x1<=-10 or y1<=-10 or x1>=1170 or y1>=770:
            return True
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        
        return False

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake eating apple scenario
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.snake.increase_length()
            self.apple.move()

        # snake colliding with itself
        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise "Collision Occured"
            

    def display_score(self):
        font = pygame.font.SysFont('arial',40)
        score = font.render(f"Score: {self.snake.length}",True,(200,200,200))
        self.surface.blit(score,(850,10))

    
    def show_game_over(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial', 80)
        line1 = font.render("GAME OVER!", True, (255, 255, 255))
        self.surface.blit(line1, (400, 300))

        font1 = pygame.font.SysFont('arial', 30)
        line3 = font1.render(f"Your score: {self.snake.length-1}", True, (255, 255, 255))
        self.surface.blit(line3, (400, 400))

        
        line2 = font1.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (400, 500))

        #for highest score
        if self.snake.length-1 >= self.highest_score:
            self.highest_score=self.snake.length-1
        line4 = font1.render(f"highest: {self.highest_score}",True,(255,255,255))
        self.surface.blit(line4,(400,450))
        pygame.display.flip()
    

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit() 
                        running = False
                    #enter key
                    if event.key == K_RETURN:
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    pygame.quit()
                    running = False
            try:

                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(.11)

if __name__ == '__main__':
    game = Game()
    game.run()
