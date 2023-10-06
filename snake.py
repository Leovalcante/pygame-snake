import os
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
        self.apple = pygame.image.load(
            os.path.join("assets", "images", "apple.png")
        ).convert_alpha()

    def draw(self):
        fruit_rect = get_grid_rect(self.x, self.y)
        screen.blit(self.apple, fruit_rect)
        # pygame.draw.rect(screen, (126, 166, 140), fruit_rect)

    def randomize(self):
        self.x = get_rand()
        self.y = get_rand()
        self.pos = Vector2(self.x, self.y)


class Snake:
    def __init__(self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False

        self.head_up = pygame.image.load(
            os.path.join("assets", "images", "head_up.png")
        ).convert_alpha()
        self.head_down = pygame.image.load(
            os.path.join("assets", "images", "head_down.png")
        ).convert_alpha()
        self.head_right = pygame.image.load(
            os.path.join("assets", "images", "head_right.png")
        ).convert_alpha()
        self.head_left = pygame.image.load(
            os.path.join("assets", "images", "head_left.png")
        ).convert_alpha()

        self.tail_up = pygame.image.load(
            os.path.join("assets", "images", "tail_up.png")
        ).convert_alpha()
        self.tail_down = pygame.image.load(
            os.path.join("assets", "images", "tail_down.png")
        ).convert_alpha()
        self.tail_right = pygame.image.load(
            os.path.join("assets", "images", "tail_right.png")
        ).convert_alpha()
        self.tail_left = pygame.image.load(
            os.path.join("assets", "images", "tail_left.png")
        ).convert_alpha()

        self.body_vertical = pygame.image.load(
            os.path.join("assets", "images", "body_vertical.png")
        ).convert_alpha()
        self.body_horizontal = pygame.image.load(
            os.path.join("assets", "images", "body_horizontal.png")
        ).convert_alpha()

        self.body_tr = pygame.image.load(
            os.path.join("assets", "images", "body_tr.png")
        ).convert_alpha()
        self.body_tl = pygame.image.load(
            os.path.join("assets", "images", "body_tl.png")
        ).convert_alpha()
        self.body_br = pygame.image.load(
            os.path.join("assets", "images", "body_br.png")
        ).convert_alpha()
        self.body_bl = pygame.image.load(
            os.path.join("assets", "images", "body_bl.png")
        ).convert_alpha()

        self.crunch_sound = pygame.mixer.Sound(
            os.path.join("assets", "sounds", "crunch.wav")
        )

    def reset(self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.direction = Vector2(0, 0)

    def draw(self):
        last_body_index = len(self.body) - 1
        for i, block in enumerate(self.body):
            block_rect = get_grid_rect(block.x, block.y)
            if i == 0:
                screen.blit(self.get_head_sprite(), block_rect)
            elif i == last_body_index:
                screen.blit(self.get_tail_sprite(), block_rect)
            else:
                screen.blit(
                    self.get_block_sprite(block, self.body[i - 1], self.body[i + 1]),
                    block_rect,
                )

    def get_block_sprite(self, block, previous, next):
        prev_relation = previous - block
        next_relation = next - block
        if prev_relation.x == next_relation.x:
            return self.body_vertical

        if prev_relation.y == next_relation.y:
            return self.body_horizontal

        #     -1
        # -1 | 0 | 1
        #      1
        sum_relation = prev_relation + next_relation
        if sum_relation.x == sum_relation.y:
            if sum_relation.x == 1:
                return self.body_br
            else:
                return self.body_tl

        if (
            prev_relation.x == -1
            and next_relation.y == 1
            or next_relation.x == -1
            and prev_relation.y == 1
        ):
            return self.body_bl

        return self.body_tr

    def get_head_sprite(self):
        if self.direction.y == -1:
            return self.head_up
        elif self.direction.x == -1:
            return self.head_left
        elif self.direction.y == 1:
            return self.head_down
        return self.head_right

    def get_tail_sprite(self):
        result = self.body[-2] - self.body[-1]
        if result.x == 1:
            return self.tail_left
        elif result.x == -1:
            return self.tail_right
        elif result.y == 1:
            return self.tail_up
        return self.tail_down

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
        self.crunch_sound.play()


class Game:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.game_over_sound = pygame.mixer.Sound(
            os.path.join("assets", "sounds", "game_over.wav")
        )

    def update(self):
        self.snake.move()
        self.check_collision()
        self.check_fail()

    def draw(self):
        self.draw_grass()
        self.snake.draw()
        self.fruit.draw()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.snake.eat()
            self.fruit.randomize()
            while self.fruit.pos in self.snake.body:
                self.fruit.randomize()

    def check_fail(self):
        head = self.snake.body[0]
        # wall check
        x_ok = 0 <= head.x < cell_number
        y_ok = 0 <= head.y < cell_number
        if not (x_ok and y_ok):
            self.game_over()

        # snake check
        # if head in self.snake.body[1:]:
        #     print(head)
        #     print(self.snake.body[1:])
        #     print("here?")
        #     self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        if self.snake.direction != (0, 0):
            self.game_over_sound.play()
            pygame.time.delay(2000)
        self.snake.reset()

    def draw_grass(self):
        grass_color = (169, 209, 61)
        for row in range(cell_number):
            for col in range(cell_number):
                if (row + col) % 2 == 0:
                    grass_rect = get_grid_rect(col, row)
                    pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score = len(self.snake.body) - 3
        score_surface = game_font.render(str(score), True, pygame.Color("black"))
        score_x = cell_size * cell_number - 60
        score_y = cell_size * cell_number - 40
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = self.fruit.apple.get_rect(
            midright=(score_rect.left, score_rect.centery)
        )
        bg_rect = pygame.Rect(
            apple_rect.left,
            apple_rect.top,
            apple_rect.width + score_rect.width + 6,
            apple_rect.height,
        )
        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(self.fruit.apple, apple_rect)
        screen.blit(score_surface, score_rect)
        pygame.draw.rect(screen, pygame.Color("black"), bg_rect, 2)


cell_size = 40
cell_number = 20
window_size = cell_size * cell_number

pygame.mixer.pre_init()
pygame.init()
screen = pygame.display.set_mode((window_size, window_size))
clock = pygame.time.Clock()
game_font = pygame.font.SysFont("Comic Sans MS", 25)

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
