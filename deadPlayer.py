# Create class for shattered ship
import math
import random

import pygame

from constants import white


class DeadPlayer:
    def __init__(self, x, y, l, gameDisplay):
        self.angle = random.randrange(0, 360) * math.pi / 180
        self.dir = random.randrange(0, 360) * math.pi / 180
        self.rtspd = random.uniform(-0.25, 0.25)
        self.x = x
        self.y = y
        self.lenght = l
        self.speed = random.randint(2, 8)
        self.gameDisplay = gameDisplay

    def updateDeadPlayer(self):
        pygame.draw.line(self.gameDisplay, white,
                         (self.x + self.lenght * math.cos(self.angle) / 2,
                          self.y + self.lenght * math.sin(self.angle) / 2),
                         (self.x - self.lenght * math.cos(self.angle) / 2,
                          self.y - self.lenght * math.sin(self.angle) / 2))
        self.angle += self.rtspd
        self.x += self.speed * math.cos(self.dir)
        self.y += self.speed * math.sin(self.dir)
