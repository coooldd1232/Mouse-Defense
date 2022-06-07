import random
import time

from reusableClasses.Vector2 import Vector2

class TankEnemy:
    def __init__(self, timeToMove):
        self.pos = Vector2(-75, random.randint(0, 750))
        self.vel = Vector2(0, 0)
        self.width = 70
        self.height = 50
        self.speed = 3
        self.checkWhenStartMoving = False
        self.moving = False

        self.timeToMove = time.time() + timeToMove

        self.attacking = False
        self.damage = 4
        self.lastAttack = time.time()
        self.timeBetweenAttacks = 1.5

    def StartMoving(self):
        self.moving = True
        self.vel.x = self.speed

    def Update(self, dt, wallPos):
        if self.moving is False:
            # check when enemy should move
            if self.checkWhenStartMoving is False and time.time() - self.timeToMove > 0:
                self.checkWhenStartMoving = True
                self.StartMoving()

        if self.moving:
            self.pos += self.vel * dt

        if self.pos.x + self.width > wallPos.x:
            self.moving = False
            self.attacking = True

        if self.attacking:
            if self.lastAttack + self.timeBetweenAttacks < time.time():
                self.lastAttack = time.time()
                return self.damage

        return 0


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

    def Update(self, dt, wallPos):
        if self.moving is False:
            # check when enemy should move
            if self.checkWhenStartMoving is False and time.time() - self.timeToMove > 0:
                self.checkWhenStartMoving = True
                self.StartMoving()

        if self.moving:
            self.pos += self.vel * dt

        if self.pos.x + self.width > wallPos.x:
            self.moving = False
            self.attacking = True

        if self.attacking:
            if self.lastAttack + self.timeBetweenAttacks < time.time():
                self.lastAttack = time.time()
                return self.damage

        return 0
