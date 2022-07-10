import pygame

from reusableClasses.Collision import Collision

pygame.init()

class ShopItem:

    font = pygame.font.Font('freesansbold.ttf', 20)

    def __init__(self, cost, imagePath, pos, textDescription, width, height):
        self.cost = cost

        self.image = pygame.image.load(imagePath)

        self.canUpgrade = True

        self.pos = pos

        self.width = width
        self.height = height

        self.textCost = self.font.render(f'${self.cost}', True, (0, 76, 76))
        self.textCostRect = self.textCost.get_rect()
        self.textCostRect.center = self.pos.x + self.width / 2 - 5, self.pos.y + self.height + 20

        self.textDescription = self.font.render(textDescription, True, (0, 76, 76))
        self.textDescriptionRect = self.textDescription.get_rect()
        self.textDescriptionRect.center = self.pos.x + self.width/2 - 5, self.pos.y - 20

    def SetCost(self, cost):
        self.cost = cost
        if self.canUpgrade:
            self.textCost = self.font.render(f'${self.cost}', True, (0, 76, 76))
            self.textCostRect = self.textCost.get_rect()
            self.textCostRect.center = self.pos.x + self.width / 2 - 5, self.pos.y + self.height + 20

        else:
            self.textCost = self.font.render(f"can't upgrade", True, (0, 76, 76))
            self.textCostRect = self.textCost.get_rect()
            self.textCostRect.center = self.pos.x + self.width / 2 - 5, self.pos.y + self.height + 20

    def GetRect(self):
        return self.pos.x, self.pos.y, self.width, self.height

    def Update(self, mousePos):
        if Collision.PointOnRect(mousePos, self.pos, self.width, self.height):
            self.image.set_alpha(255)
        else:
            self.image.set_alpha(150)
