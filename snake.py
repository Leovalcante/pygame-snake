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


class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(6, 10), Vector2(7, 10)]
        self.direction = Vector2(1, 0)

    def draw(self):
        for block in self.body:
            block_rect = get_grid_rect(block.x, block.y)
            pygame.draw.rect(screen, (183, 111, 122), block_rect)

    def move(self):
        body = self.body[:-1]
        body.insert(0, body[0] + self.direction)
        self.body = body[:]


cell_size = 40
cell_number = 20
window_size = cell_size * cell_number

pygame.init()
screen = pygame.display.set_mode((window_size, window_size))
clock = pygame.time.Clock()

fruit = Fruit()
snake = Snake()

SCREEN_UPDATE_EVENT = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE_EVENT, 150)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == SCREEN_UPDATE_EVENT:
            snake.move()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.direction = Vector2(0, -1)
            elif event.key == pygame.K_DOWN:
                snake.direction = Vector2(0, 1)
            elif event.key == pygame.K_RIGHT:
                snake.direction = Vector2(1, 0)
            elif event.key == pygame.K_LEFT:
                snake.direction = Vector2(-1, 0)

    screen.fill((175, 215, 70))
    fruit.draw()
    snake.draw()
    pygame.display.update()
    clock.tick(60)
