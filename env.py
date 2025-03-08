import pygame
from pygame.locals import *
import random

pygame.init()
pygame.font.init()

Font = pygame.font.SysFont("comicsans", 30)

WIDTH, HEIGHT = 280, 511
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird - RL (SARSA)")

background = pygame.image.load("./assets/bg.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

bird_img = pygame.image.load("./assets/bird.png")
bird_img = pygame.transform.scale(bird_img, (40, 30))

pipe_img = pygame.image.load("./assets/pipe.png")
pipe_img = pygame.transform.scale(pipe_img, (50, 300))

ground_img = pygame.image.load("./assets/base.png")
ground_img = pygame.transform.scale(ground_img, (WIDTH, 50))

BIRD_X = 50
GRAVITY = 0.9
FLAP_STRENGTH = -6

PIPE_WIDTH = 50
PIPE_GAP = 150
PIPE_VELOCITY = 3
PIPE_DISTANCE = 300

clock = pygame.time.Clock()

class Pipe(pygame.Rect):
    def __init__(self, left, top, width, height):
        super().__init__(left, top, width, height)
        self.passed = False

class Gift(pygame.Rect):
    def __init__(self, left, top, width, height):
        super().__init__(left, top, width, height)
        self.collected = False

class FlappyBirdEnv:
    def __init__(self, delay=0):
        self.reset()
        self.delay = delay

    def reset(self):
        self.bird_y = HEIGHT // 2
        self.bird_velocity = 0
        self.pipes = [self.create_pipe()]
        self.score = 0
        self.n_gift = 0
        self.gift = self.create_gift()
        return self.get_state()

    def create_pipe(self):
        pipe_height = random.randint(50, 300)
        top_pipe = Pipe(WIDTH, 0, PIPE_WIDTH, pipe_height)
        bottom_pipe = Pipe(WIDTH, pipe_height + PIPE_GAP, PIPE_WIDTH, HEIGHT - pipe_height - PIPE_GAP)
        return top_pipe, bottom_pipe

    def get_state(self):
        x_pipe, y_bird = self.convert()
        # x_gift, y_gift = int(self.gift.x / 40), int(self.gift.y / 40)
        x_gift, y_gift = self.gift.x, self.gift.y

        x_gift = (x_gift - BIRD_X) // 40
        y_gift = (y_gift - self.bird_y) // 40

        return x_pipe, y_bird, x_gift, y_gift

    def convert(self):
        x = min(280, self.pipes[0][1].x)
        y = self.pipes[0][1].y - self.bird_y
        if y < 0:
            y = abs(y) + 408
        return int(x/40-1), int(y/40)

    def create_gift(self):
        # gift_x = random.randint(WIDTH // 2, WIDTH - 50)
        x = self.pipes[0][0].x + PIPE_WIDTH
        gift_x = self.pipes[0][0].x + 125
        if len(self.pipes) > 1:
            gift_x = self.pipes[1][0].x + 125
        # gift_x = random.randint(x + 10, x + 150)
        gift_y = random.randint(100, HEIGHT - 200)
        return Gift(gift_x, gift_y, 30, 30)

    def step(self, action):
        if self.delay > 0:
            pygame.time.delay(self.delay)

        if action == 1:
            self.bird_velocity = FLAP_STRENGTH

        self.bird_velocity += GRAVITY
        self.bird_y += self.bird_velocity

        reward = 0
        done = False

        new_pipes = []

        for pipe_top, pipe_bottom in self.pipes:
            pipe_top.x -= PIPE_VELOCITY
            pipe_bottom.x -= PIPE_VELOCITY

            if pipe_top.x < BIRD_X and not pipe_top.passed:
                self.score += 1
                pipe_top.passed = True
                reward = 200

            if pipe_top.x + PIPE_WIDTH > 0:
                new_pipes.append((pipe_top, pipe_bottom))

        self.pipes = new_pipes

        if len(self.pipes) == 0 or self.pipes[-1][0].x < WIDTH - PIPE_DISTANCE:
            self.pipes.append(self.create_pipe())

        # gift_collected = False
        self.gift.x -= PIPE_VELOCITY
        if self.gift.colliderect((BIRD_X, self.bird_y, 40, 30)):
            self.gift.collected = True
            reward += 500
            self.n_gift += 1
            self.gift = self.create_gift()

        if self.gift.x < 0 and not self.gift.collected:
            reward -= 50
            self.gift = self.create_gift()

        # if self.pipes[0][0].height < self.bird_y < self.pipes[0][0].height + PIPE_GAP:
        #     reward += 1

        # if self.bird_y < 100:
        #     reward -= 10

        # if self.bird_y + 30 > HEIGHT - 50:
        #     reward = -1000
        #     done = True

        # if self.bird_y + bird_img.get_height() > HEIGHT - 50 or self.bird_y < 0:
        #     reward = -1000
        #     done = True

        # if self.gift.collected:
        #     reward = 30

        done = self.check_collision()
        if done:
            reward = -1000

        return self.get_state(), reward, done


    def check_collision(self):
        """"""
        if self.bird_y + bird_img.get_height() > HEIGHT - 50 or self.bird_y < 0:
            return True

        pipe_top, pipe_bottom = self.pipes[0]

        if pipe_top.colliderect((BIRD_X, self.bird_y, bird_img.get_width(), bird_img.get_height())) or \
            pipe_bottom.colliderect((BIRD_X, self.bird_y, bird_img.get_width(), bird_img.get_height())):
            return True

        return False

    def render(self, episode_idx=-1):
        pygame.event.get()
        score = Font.render("Score: "+ str(self.score), 1, (255,255,255))
        gift = Font.render("Gift: "+ str(self.n_gift), 1, (255,255,255))

        screen.blit(background, (0, 0))
        screen.blit(bird_img, (BIRD_X, int(self.bird_y)))
        for pipe_top, pipe_bottom in self.pipes:
            screen.blit(pygame.transform.flip(pipe_img, False, True), (pipe_top.x, pipe_top.bottom - pipe_img.get_height()))
            screen.blit(pipe_img, (pipe_bottom.x, pipe_bottom.y))
        screen.blit(ground_img, (0, HEIGHT - 50))
        pygame.draw.rect(screen, (255, 215, 0), self.gift)

        if episode_idx == -1:
            screen.blit(score, (20, 10))
            screen.blit(gift, (20, 40))
        else:
            episode = Font.render("Episode: "+ str(episode_idx), 1, (255,255,255))
            screen.blit(episode, (20, 10))
            screen.blit(score, (20, 40))
            screen.blit(gift, (20, 70))

        pygame.display.update()
