# Create class bullet
import math

import pygame

from constants import bullet_speed, white, game_width, game_height


class Bullet:
    def __init__(self, x, y, direction, gameDisplay):
        self.x = x
        self.y = y
        self.dir = direction
        self.life = 30
        self.gameDisplay = gameDisplay

    def updateBullet(self):
        # Moving
        self.x += bullet_speed * math.cos(self.dir * math.pi / 180)
        self.y += bullet_speed * math.sin(self.dir * math.pi / 180)

        # Drawing
        pygame.draw.circle(self.gameDisplay, white, (int(self.x), int(self.y)), 3)

        # Wrapping
        if self.x > game_width:
            self.x = 0
        elif self.x < 0:
            self.x = game_width
        elif self.y > game_height:
            self.y = 0
        elif self.y < 0:
            self.y = game_height
        self.life -= 1
