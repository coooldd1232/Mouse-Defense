from reusableClasses.Vector2 import Vector2
from reusableClasses.Collision import Collision
from reusableClasses.Approach import Approach

from gun import Gun

class Player:
    def __init__(self):
        self.width = 150
        self.height = 50

        self.vel = Vector2(0, 0)
        self.velGoal = Vector2()
        # pos is the position of the player relative to the percent of the window
        self.pos = Vector2(1000, 400 - self.height/2)

        self.gun = Gun(Vector2(self.pos.x + 20, self.pos.y + 25))

    def Update(self, dt, mousePos, tankEnemies, fastEnemies):
        # update pos,velocity
        self.UpdateVelocity(dt)
        self.pos += self.vel * dt

        if self.pos.y < 0:
            self.pos.y = 0
        elif self.pos.y > 800 - self.height:
            self.pos.y = 800 - self.height
        # update gun
        self.gun.pos = Vector2(self.pos.x + 75, self.pos.y + 25)

        fastEnemiesDied = self.gun.Update(dt, mousePos, fastEnemies)
        tankEnemiesDied = self.CheckForCollisionWithTankEnemies(tankEnemies)

        return fastEnemiesDied, tankEnemiesDied

    def CheckForCollisionWithTankEnemies(self, enemies):
        tankEnemiesDied = 0
        for enemy in enemies:
            if Collision.RectOnRect(self.pos, self.width, self.height, enemy.pos, enemy.width, enemy.height):
                enemies.remove(enemy)
                tankEnemiesDied += 1

        return tankEnemiesDied

    def UpdateVelocity(self, dt):
        self.vel.y = Approach(self.velGoal.y, self.vel.y, dt * 40)

        # velocity approaches 0
        self.velGoal.y = self.velGoal.y - 0.1 if self.velGoal.y > 0 else self.velGoal.y + 0.1
        if abs(self.velGoal.y) <= 0.1:
            self.velGoal.y = 0
