import sys
from random import randint

import pygame
from pygame.math import Vector2


def get_grid_rect(x, y):
    return pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)


def get_rand():
    return randint(0, cell_number - 1)


class Fruit:
    def __init__(self):
        self.x = get_rand()
        self.y = get_rand()
        self.pos = Vector2(self.x, self.y)

    def draw(self):
        fruit_rect = get_grid_rect(self.x, self.y)
        pygame.draw.rect(screen, (126, 166, 140), fruit_rect)

    def replace(self):
        self.x = get_rand()
        self.y = get_rand()
        self.pos = Vector2(self.x, self.y)


class Snake:
    def __init__(self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

    def draw(self):
        for block in self.body:
            block_rect = get_grid_rect(block.x, block.y)
            pygame.draw.rect(screen, (183, 111, 122), block_rect)

    def move(self):
        if self.new_block:
            body = self.body[:]
            self.new_block = False
        else:
            body = self.body[:-1]

        body.insert(0, body[0] + self.direction)
        self.body = body[:]

    def eat(self):
        self.new_block = True


class Game:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    def update(self):
        self.snake.move()
        self.check_collision()
        self.check_fail()

    def draw(self):
        self.snake.draw()
        self.fruit.draw()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.replace()
            self.snake.eat()

    def check_fail(self):
        head = self.snake.body[0]
        # wall check
        x_ok = 0 <= head.x < cell_number
        y_ok = 0 <= head.y < cell_number
        if not (x_ok and y_ok):
            self.game_over()

        # snake check
        if head in self.snake.body[1:]:
            print(head)
            print(self.snake.body[1:])
            print("machedavero?")
            self.game_over()

    def game_over(self):
        pygame.quit()
        sys.exit()


cell_size = 40
cell_number = 20
window_size = cell_size * cell_number

pygame.init()
screen = pygame.display.set_mode((window_size, window_size))
clock = pygame.time.Clock()

SCREEN_UPDATE_EVENT = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE_EVENT, 150)

game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == SCREEN_UPDATE_EVENT:
            game.update()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if game.snake.direction.y != 1:
                    game.snake.direction = Vector2(0, -1)
            elif event.key == pygame.K_DOWN:
                if game.snake.direction.y != -1:
                    game.snake.direction = Vector2(0, 1)
            elif event.key == pygame.K_RIGHT:
                if game.snake.direction.x != -1:
                    game.snake.direction = Vector2(1, 0)
            elif event.key == pygame.K_LEFT:
                if game.snake.direction.x != 1:
                    game.snake.direction = Vector2(-1, 0)
            elif event.key == pygame.K_c and pygame.key.get_mods() & pygame.K_LCTRL:
                pygame.quit()
                sys.exit()

    screen.fill((175, 215, 70))
    game.draw()
    pygame.display.update()
    clock.tick(60)
