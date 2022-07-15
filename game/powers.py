import pygame

import random

from reusableClasses.Vector2 import Vector2
from reusableClasses.Collision import Collision

class Freeze():
    def __init__(self):
        self.freezing = False
        self.timeStartedFreezing = 0
        self.TIMETOFREEZEFOR = 5

    def Reset(self):
        self.__init__()

class Clear():
    def __init__(self):
        self.pos = Vector2(49, 0)
        self.vel = Vector2()
        
        self.width = 1102
        self.height = 600

        self.clearing = False

        self.image = pygame.transform.scale(pygame.image.load("images/powers/powerPunch.png"), (self.width + 200, self.height))

    def Start(self):
        self.pos = Vector2(49, 800)
        self.vel = Vector2(0, -5)
        
        self.clearing = True

    def Update(self, dt, fastEnemies):
        self.pos += self.vel * dt

        for enemy in fastEnemies:
            if Collision.RectOnRect(self.pos, self.width, self.height, enemy.pos, enemy.width, enemy.height):
                fastEnemies.remove(enemy)

        if self.pos.y + self.height < 0:
            self.__init__()

    def Reset(self):
        self.__init__()
