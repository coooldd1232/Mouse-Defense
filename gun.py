import pygame
import time
import math

from reusableClasses.Vector2 import Vector2
from reusableClasses.Collision import Collision
from reusableClasses.Approach import Approach

class Gun:
    def __init__(self, pos):
        self.pos = pos

        self.direcNorm = Vector2()
        self.bulletSpeed = 15
        self.bullets = []

        self.reloading = False

        self.bulletsLeft = 10
        self.bulletRounds = 10

        self.timeStartReload = 0
        self.reloadTime = 0.5

        self.homingBullets = False

    def Shoot(self, direc):
        if self.bulletsLeft > 0 and self.reloading is False:
            self.bullets.append(Bullet(self.pos, direc))
            self.bulletsLeft -= 1

    def Reload(self):
        if self.bulletsLeft != self.bulletRounds:
            self.reloading = True
            self.timeStartReload = time.time()

    def Update(self, dt, mousePos, fastEnemies):
        fastEnemiesDied = self.UpdateBullets(dt, fastEnemies)

        self.direcNorm = (mousePos - self.pos).GetNormalized()

        # if gun stopped reloading
        if time.time() - self.timeStartReload >= self.reloadTime:
            self.timeStartReload = time.time() + 100000
            self.bulletsLeft = self.bulletRounds
            self.reloading = False

        return fastEnemiesDied

    def UpdateBullets(self, dt, fastEnemies):
        fastEnemiesDied = 0

        for bullet in self.bullets:
            bullet.Update(dt, self.bulletSpeed, self.homingBullets, fastEnemies)

            if bullet.pos.x < 0 or bullet.pos.y < 0 or bullet.pos.y > 800:
                self.bullets.remove(bullet)

            for enemy in fastEnemies:
                if Collision.RectOnRect(bullet.pos - Vector2(bullet.radius, bullet.radius), Bullet.radius * 2, Bullet.radius * 2,
                                        enemy.pos, enemy.width, enemy.height):

                    self.bullets.remove(bullet)

                    enemy.health -= 1
                    if enemy.health <= 0:
                        fastEnemies.remove(enemy)
                        fastEnemiesDied += 1
                    break

        return fastEnemiesDied

class Bullet:

    radius = 3

    def __init__(self, pos, direc):
        self.pos = pos
        self.direc = direc.GetNormalized()

        self.homingTrianglePoints = []

        self.UpdatePoints()

    def Update(self, dt, speed, homingBullets, fastEnemies):
        currentAngle = self.direc.angle

        if homingBullets:
            for enemy in fastEnemies:
                if Collision.RectOnPoly(enemy.pos, enemy.width, enemy.height, self.homingTrianglePoints):
                    bulletToEnemy = (enemy.pos + (Vector2(enemy.width, enemy.height) / 2)) - self.pos
                    goalAngle = bulletToEnemy.angle

                    currentAngle = Approach(goalAngle, currentAngle, dt * 10)

                    self.direc = Vector2(math.cos(currentAngle), -math.sin(currentAngle))

                    self.UpdatePoints()

                    break

        movement = (self.direc * speed) * dt
        for i in range(len(self.homingTrianglePoints)):
            self.homingTrianglePoints[i] += movement

        self.pos += movement

    def UpdatePoints(self):
        triangleHomingLength = 500
        middleT = (self.direc * triangleHomingLength)

        middleTAngle = middleT.angle
        point1 = self.pos

        point2Angle = middleTAngle + math.radians(20)
        point2Direc = Vector2(math.cos(point2Angle), -math.sin(point2Angle))
        point2 = point1 + point2Direc * triangleHomingLength

        point3Angle = middleTAngle - math.radians(20)
        point3Direc = Vector2(math.cos(point3Angle), -math.sin(point3Angle))
        point3 = point1 + point3Direc * triangleHomingLength

        self.homingTrianglePoints = [point1, point2, point3]
