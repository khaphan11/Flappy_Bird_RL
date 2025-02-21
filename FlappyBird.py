import pygame
from pygame.locals import *
import random

pygame.init()
pygame.font.init()

Font = pygame.font.SysFont("comicsans", 30)

WIDTH, HEIGHT = 280, 511
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird - RL (SARSA)")

background = pygame.image.load("bg.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

bird_img = pygame.image.load("bird.png")
bird_img = pygame.transform.scale(bird_img, (40, 30))

pipe_img = pygame.image.load("pipe.png")
pipe_img = pygame.transform.scale(pipe_img, (50, 300))

ground_img = pygame.image.load("base.png")
ground_img = pygame.transform.scale(ground_img, (WIDTH, 50))

BIRD_X = 50
GRAVITY = 0.9
FLAP_STRENGTH = -6

PIPE_WIDTH = 50
PIPE_GAP = 150
PIPE_VELOCITY = 3

clock = pygame.time.Clock()

class Pipe(pygame.Rect):
    def __init__(self, left, top, width, height):
        super().__init__(left, top, width, height)
        self.passed = False

class FlappyBirdEnv:
    def __init__(self, delay=0):
        self.reset()
        self.delay = delay

    def reset(self):
        self.bird_y = HEIGHT // 2
        self.bird_velocity = 0
        self.pipes = [self.create_pipe()]
        self.score = 0
        return self.get_state()

    def create_pipe(self):
        pipe_height = random.randint(100, 300)
        top_pipe = Pipe(WIDTH, 0, PIPE_WIDTH, pipe_height)
        bottom_pipe = Pipe(WIDTH, pipe_height + PIPE_GAP, PIPE_WIDTH, HEIGHT - pipe_height - PIPE_GAP)
        return top_pipe, bottom_pipe

    def get_state(self):
        # pipe_top, pipe_bottom = self.pipes[0]
        # return (
        #     int(self.bird_y / 20),
        #     # round(self.bird_velocity / 10, 2),
        #     int(pipe_top.x / 20),
        #     int(pipe_top.height / 20)
        # )
        return self.convert()


    def convert(self):
        x = min(280, self.pipes[0][1].x)
        y = self.pipes[0][1].y - self.bird_y
        if y < 0:
            y = abs(y) + 408
        return int(x/40-1), int(y/40)

    def step(self, action):
        if self.delay > 0:
            # clock.tick(self.delay)
            pygame.time.delay(self.delay)

        if action == 1:
            self.bird_velocity = FLAP_STRENGTH

        self.bird_velocity += GRAVITY
        self.bird_y += self.bird_velocity

        reward = 15
        done = False

        new_pipes = []

        for pipe_top, pipe_bottom in self.pipes:
            pipe_top.x -= PIPE_VELOCITY
            pipe_bottom.x -= PIPE_VELOCITY

            if pipe_top.x < BIRD_X and not pipe_top.passed:
                # reward += 15
                self.score += 1
                pipe_top.passed = True



            if pipe_top.x + PIPE_WIDTH > 0:
                new_pipes.append((pipe_top, pipe_bottom))

        self.pipes = new_pipes

        if len(self.pipes) == 0 or self.pipes[-1][0].x < WIDTH - 250:
            self.pipes.append(self.create_pipe())

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

        done = self.check_collision()
        # reward = 15
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

    def render(self):
        pygame.event.get()
        score = Font.render("Score: "+ str(self.score), 1, (255,255,255))
        screen.blit(background, (0, 0))
        screen.blit(bird_img, (BIRD_X, int(self.bird_y)))
        for pipe_top, pipe_bottom in self.pipes:
            screen.blit(pygame.transform.flip(pipe_img, False, True), (pipe_top.x, pipe_top.bottom - pipe_img.get_height()))
            screen.blit(pipe_img, (pipe_bottom.x, pipe_bottom.y))
        screen.blit(ground_img, (0, HEIGHT - 50))
        screen.blit(score, (WIDTH - 10 -score.get_width(), 10))
        pygame.display.update()
