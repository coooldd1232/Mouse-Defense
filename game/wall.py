import pygame

from reusableClasses.Vector2 import Vector2

class Wall:
    def __init__(self):
        self.pos = Vector2(1200, 0)
        self.width = 200
        self.height = 800

        self.wallUpgradeIndex = 0
        self.wallUpgrades = [100, 200, 400, 700, 1000]  # health
        self.wallUpgradesCost = ['5000', '10000', '15000', '20000']
        self.wallUpgradesImages = [pygame.image.load('images/WallUpgrade2.png')]

        self.maxHealth = self.wallUpgrades[self.wallUpgradeIndex]
        self.health = self.maxHealth
