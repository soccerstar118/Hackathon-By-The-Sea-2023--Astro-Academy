import pygame
import random
from config import width, height, screen, amount_proj_trail
import os
from random import uniform


class Asteroid:
    def __init__(self, word, prompt, speed, override_pos=None, override_vel=None) -> None:
        self.word = word
        self.prompt = prompt
        self.pos = pygame.Vector2(random.uniform(3/8, 5/8)*width, 0)
        if override_pos is not None:
            self.pos = pygame.Vector2(override_pos)

        self.vel = pygame.Vector2(random.uniform(-2, 2)*speed, speed)
        if override_vel is not None:
            self.vel = pygame.Vector2(override_vel)

        self.radius = 35
        self.color = (0, 0, 0)
        self.surf = pygame.Surface((self.radius * 2, self.radius * 2))
        pygame.draw.circle(self.surf, self.color,
                           (self.radius, self.radius), self.radius)
        self.image = pygame.image.load(os.path.join("asteroid.png"))
        self.image = pygame.transform.scale(
            self.image, (2*self.radius, 2*self.radius))

    def draw(self):
        # pygame.draw.circle(screen, self.color, self.pos, self.radius)
        screen.blit(self.image, (self.pos.x -
                    self.radius, self.pos.y-self.radius))

    def move(self):
        self.pos += self.vel
        if self.pos.x < 0:
            self.pos.x = 0
            self.vel.x = abs(self.vel.x)
        if self.pos.x > width:
            self.pos.x = width
            self.vel.x = -abs(self.vel.x)

    def is_out_of_bounds(self):
        if self.pos.y-self.radius >= height:
            return True
        return False

    def update(self):
        self.move()
        self.draw()
