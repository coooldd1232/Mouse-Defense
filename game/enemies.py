import random
import time

from reusableClasses.Vector2 import Vector2
from reusableClasses.Collision import Collision

class FastEnemy:
    def __init__(self, timeToMove):
        self.pos = Vector2(-75, random.randint(0, 750))
        self.vel = Vector2(0, 0)
        self.width = 50
        self.height = 50
        self.health = 1
        self.speed = 5
        self.checkWhenStartMoving = False
        self.moving = False

        self.timeToMove = time.time() + timeToMove

        self.attacking = False
        self.damage = 1
        self.lastAttack = time.time()
        self.timeBetweenAttacks = 0.5

    def StartMoving(self):
        self.moving = True
        self.vel.x = self.speed

    def Update(self, dt, wallPos, freezing):
        if self.moving is False:
            # check when enemy should move
            if freezing:
                self.timeToMove += dt / 60
            if self.checkWhenStartMoving is False and time.time() - self.timeToMove > 0:
                self.checkWhenStartMoving = True
                self.StartMoving()

        if self.moving:
            if freezing is False:
                self.pos += self.vel * dt

        if self.pos.x + self.width > wallPos.x:
            self.pos.x = wallPos.x - self.width
            self.moving = False
            self.attacking = True

        if self.attacking:
            if self.lastAttack + self.timeBetweenAttacks < time.time():
                self.lastAttack = time.time()
                if freezing is False:
                    return self.damage

        return 0
