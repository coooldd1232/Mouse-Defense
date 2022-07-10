# TODO: add powers
# TODO: ADD SOUND

import pygame
import time

from reusableClasses.button import Button
from reusableClasses.Vector2 import Vector2
from reusableClasses.Collision import Collision
from reusableClasses.Approach import Approach

from player import Player
from gun import Bullet
from wall import Wall
from powers import Freeze
from wave import Wave
from shopItem import ShopItem


class Game:
    def __init__(self, screenWidth, screenHeight):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

        self.player = Player()

        self.font = pygame.font.Font('freesansbold.ttf', 50)
        self.nextWaveFont = pygame.font.Font('freesansbold.ttf', 30)
        self.shopUpgradesAndPowersFont = pygame.font.Font('freesansbold.ttf', 30)

        self.wall = Wall()

        self.nextWaveButton = Button((60, 60, 60), (30, 30, 30), "Next Wave", (200, 200, 200), self.nextWaveFont, Vector2(512.5, 662.5), 225, 75)
        self.playAgainButton = Button((60, 60, 60), (30, 30, 30), "Play Again", (200, 200, 200), self.nextWaveFont, Vector2(512.5, 662.5), 225, 75)

        self.wave = Wave()
        self.waveNumber = 0
        self.waves = [[0, 1], [5, 2], [5, 3], [5, 5], [5, 10], [5, 100]] # seconds per wave, fast enemies

        self.fastEnemies = self.wave.Start(self.waves[self.waveNumber])

        self.gunBarWidthGoal = self.player.gun.bulletsLeft / self.player.gun.bulletRounds * 196
        self.gunBarWidth = self.player.gun.bulletsLeft / self.player.gun.bulletRounds * 196

        self.money = 0

        # upgrades
        # image should be 70x50
        self.bulletClipSize = ShopItem(1000, "images/upgrades/clipSize.png", Vector2(220, 350), "+1 clip size", 70, 50)
        self.healWall = ShopItem(2000, "images/upgrades/healWall.png", Vector2(430, 350), "+20 wall health", 70, 50)
        self.wallUpgrades = ShopItem(self.wall.wallUpgradesCost[self.wall.wallUpgradeIndex], "images/upgrades/upgradeWall.png", Vector2(620, 350), "upgrade wall", 70, 50)
        self.homingBullets = ShopItem(70000, "images/upgrades/homingBullets.png", Vector2(800, 350), "homing bullets", 70, 50)
        self.addAnotherBullet = ShopItem(20000, "images/upgrades/anotherBullet.png", Vector2(990, 350), "+1 bullet", 70, 50)
        # powers
        # image should be 50x50
        self.freezePower = ShopItem(0, "images/powers/freeze.png", Vector2(220, 520), "freeze enemies", 50, 50)

        self.upgrades = [self.bulletClipSize, self.healWall, self.wallUpgrades, self.homingBullets, self.addAnotherBullet]
        self.listOfPowers = [self.freezePower]

        self.FREEZEPOWER = 0

        self.ownedPowers = []

        self.freezeStruct = Freeze()

        self.lose = False

    def Update(self, dt, mousePos):
        # if you haven't lost or are not in between a wave
        if self.wave.inBetweenWaves is False and self.lose is False:
            if self.freezeStruct.freezing and time.time() - self.freezeStruct.timeStartedFreezing > self.freezeStruct.TIMETOFREEZEFOR:
                self.freezeStruct.freezing = False
            # update enemies
            for enemy in self.fastEnemies:
                self.wall.health -= enemy.Update(dt * 60, self.wall.pos, self.freezeStruct.freezing)

            if self.wall.health <= 0:
                self.lose = True

            # kill enemies, gain money # and update player and bullets
            numFastEnemiesDied = self.player.Update(dt * 60, mousePos, self.fastEnemies)
            for fastEnemy in range(numFastEnemiesDied):
                self.money += 200

            # how much ammo you have left but it looks fancy
            self.gunBarWidthGoal = self.player.gun.bulletsLeft / self.player.gun.bulletRounds * 196
            self.gunBarWidth = Approach(self.gunBarWidthGoal, self.gunBarWidth, dt * 400)

            # if all enemies are dead, wave is finished
            if self.fastEnemies == [] and self.lose is False:
                self.wave.inBetweenWaves = True
                self.player.gun.bullets = []

        if self.lose:
            self.playAgainButton.Update(mousePos)

        # this code runs if wave is finished and you are choosing what to buy
        if self.wave.inBetweenWaves:
            self.nextWaveButton.Update(mousePos)

            for upgrade in self.upgrades:
                upgrade.Update(mousePos)
            for power in self.listOfPowers:
                power.Update(mousePos)

    def Draw(self, screen):
        # background
        screen.fill((0, 0, 0))

        # player
        pygame.draw.rect(screen, (200, 200, 200), (self.player.pos.x, self.player.pos.y, self.player.width, self.player.height))
        # players gun
        beginningPoint = (self.player.gun.pos.x, self.player.gun.pos.y)
        endingPoint = (beginningPoint[0] + self.player.gun.direcNorm.x * 40, beginningPoint[1] + self.player.gun.direcNorm.y * 40)
        pygame.draw.line(screen, (100, 100, 100), beginningPoint, endingPoint, 15)
        # players guns bullets
        for bullet in self.player.gun.bullets:
            pygame.draw.circle(screen, (186, 255, 0), (bullet.pos.x, bullet.pos.y), Bullet.radius)
        # wall
        screen.blit(self.wall.wallUpgradesImages[0], (self.wall.pos.x, self.wall.pos.y))
        # enemies
        for enemy in self.fastEnemies:
            pygame.draw.rect(screen, (255, 0, 0), (enemy.pos.x, enemy.pos.y, enemy.width, enemy.height))
        # draw bulletsLeft | Rounds
        text = self.font.render(f'{self.player.gun.bulletsLeft} | {self.player.gun.bulletRounds}', True, (26, 247, 253))
        textRect = text.get_rect()
        textRect.center = 225, 50
        screen.blit(text, textRect)
        # draw reload bar
        barRect = (123, 80, 204, textRect.height)
        pygame.draw.rect(screen, (205, 240, 123), barRect, 3)  # outside rect
        insideBarRect = pygame.rect.Rect(barRect[0] + 4, barRect[1] + 4, self.gunBarWidth, barRect[3] - 8)
        pygame.draw.rect(screen, (12, 245, 125), insideBarRect)  # inside rect
        # draw money
        moneyText = self.font.render(f'${self.money}', True, (203, 123, 1))
        moneyTextRect = moneyText.get_rect()
        moneyTextRect.center = 625, 50
        screen.blit(moneyText, moneyTextRect)
        # draw wall health
        wallHealthText = self.font.render(f'{self.wall.health} | {self.wall.maxHealth}', True, (26, 237, 253))
        wallHealthTextRect = wallHealthText.get_rect()
        wallHealthTextRect.center = 1025, 50
        screen.blit(wallHealthText, wallHealthTextRect)
        # draw wall health bar
        barRect = (928, 80, 204, textRect.height)
        pygame.draw.rect(screen, (205, 240, 123), barRect, 3)  # outside rect
        insideBarRect = pygame.rect.Rect(barRect[0] + 4, barRect[1] + 4, self.wall.health / self.wall.maxHealth * 196, barRect[3] - 8)
        pygame.draw.rect(screen, (12, 245, 125), insideBarRect)  # inside rect
        # draw powers you own list:
        for index, power in enumerate(self.ownedPowers):
            image = self.listOfPowers[power].image
            pos = 575 - (((len(self.ownedPowers) - 1) * 25)) + (index * 50), 700
            screen.blit(image, pos)

        # if the wave is finished draw shop, or if you lose draw losing screen
        if self.wave.inBetweenWaves or self.lose:
            pygame.draw.rect(screen, (0, 76, 76), (100, 150, 1050, 600))  # outside layer
            pygame.draw.rect(screen, (0, 76, 76), (100, 150, 1050, 100))  # top layer
            pygame.draw.rect(screen, (0, 76, 76), (100, 650, 1050, 100))  # bottom layer
            pygame.draw.rect(screen, (102,178,178), (140, 250, 970, 400))  # inside layer

            # find out message whether you pass wave or you lose
            message = f'Wave {self.waveNumber + 1} Complete!' if self.wave.inBetweenWaves else f'You Lose!'
            text = self.font.render(message, True, (0, 128, 128))
            textRect = text.get_rect()
            textRect.center = 625, 200
            screen.blit(text, textRect)

            # button
            button = self.nextWaveButton if self.wave.inBetweenWaves else self.playAgainButton
            pygame.draw.rect(screen, button.bgColor, button.GetRect())
            screen.blit(button.text, button.textRect)

            if self.wave.inBetweenWaves:
                # upgrades
                upgradesText = self.shopUpgradesAndPowersFont.render('upgrades', True, (24,116,205))
                upgradesTextRect = upgradesText.get_rect()
                upgradesTextRect.center = 640, 280
                screen.blit(upgradesText, upgradesTextRect)

                for upgrade in self.upgrades:
                    screen.blit(upgrade.image, upgrade.GetRect())
                    screen.blit(upgrade.textCost, upgrade.textCostRect)
                    screen.blit(upgrade.textDescription, upgrade.textDescriptionRect)

                # powers
                powersText = self.shopUpgradesAndPowersFont.render('powers', True, (24, 116, 205))
                powersTextRect = powersText.get_rect()
                powersTextRect.center = 640, 460
                screen.blit(powersText, powersTextRect)

                for power in self.listOfPowers:
                    screen.blit(power.image, power.GetRect())
                    screen.blit(power.textCost, power.textCostRect)
                    screen.blit(power.textDescription, upgrade.textDescriptionRect)

            elif self.lose:
                youLoseText = self.font.render(f'and made it to wave: {self.waveNumber + 1}', True, (200, 80, 0))
                youLoseTextRect = youLoseText.get_rect()
                youLoseTextRect.center = 620, 300
                screen.blit(youLoseText, youLoseTextRect)

        # flip buffers
        pygame.display.flip()

    def OnClick(self, button, mousePos):
        # if you are in game
        if self.wave.inBetweenWaves is False and self.lose is False:
            # if left click
            if button == 1:
                self.player.gun.Shoot(self.player.gun.direcNorm)
            if button == 3:
                self.player.gun.Reload()
            if button == 2:
                if len(self.ownedPowers) > 0:
                    powerUsed = 0
                    if self.ownedPowers[powerUsed] == self.FREEZEPOWER:
                        self.freezeStruct.freezing = True
                        self.freezeStruct.timeStartedFreezing = time.time()

                    self.ownedPowers.pop(powerUsed)

        if self.wave.inBetweenWaves:
            if button == 1:
                # if you hit the next wave button
                if Collision.PointOnRect(mousePos, self.nextWaveButton.pos, self.nextWaveButton.width, self.nextWaveButton.height):
                    self.wave.inBetweenWaves = False
                    self.player.gun.bulletsLeft = self.player.gun.bulletRounds
                    self.waveNumber += 1
                    self.fastEnemies = self.wave.Start(self.waves[self.waveNumber])
                # if you click on +1 bullet upgrade
                elif Collision.PointOnRect(mousePos, self.bulletClipSize.pos, self.bulletClipSize.width, self.bulletClipSize.height):
                    if self.money >= self.bulletClipSize.cost:
                        self.player.gun.bulletRounds += 1
                        self.money -= self.bulletClipSize.cost
                # if you click on +health for wall upgrade
                elif Collision.PointOnRect(mousePos, self.healWall.pos, self.healWall.width, self.healWall.height):
                    if self.money >= self.healWall.cost:
                        if self.wall.health < self.wall.maxHealth:
                            self.money -= self.healWall.cost
                            self.wall.health += 20
                            if self.wall.health >= self.wall.maxHealth:
                                self.wall.health = self.wall.maxHealth
                # if you click to upgrade wall
                elif Collision.PointOnRect(mousePos, self.wallUpgrades.pos, self.wallUpgrades.width, self.wallUpgrades.height):
                    if self.wallUpgrades.canUpgrade:
                        if self.money >= int(self.wallUpgrades.cost):
                            self.money -= int(self.wallUpgrades.cost)
                            self.wall.wallUpgradeIndex += 1
                            if self.wall.wallUpgradeIndex < len(self.wall.wallUpgrades):  # if you upgrade the wall to the max
                                if self.wall.wallUpgradeIndex < len(self.wall.wallUpgradesCost):
                                    self.wallUpgrades.SetCost(self.wall.wallUpgradesCost[self.wall.wallUpgradeIndex])
                                else:
                                    self.wallUpgrades.canUpgrade = False
                                    self.wallUpgrades.SetCost(0)
                            # wall health goes up with the max health
                            newMaxHealth = self.wall.wallUpgrades[self.wall.wallUpgradeIndex]
                            gainedHealth = newMaxHealth - self.wall.maxHealth
                            self.wall.health += gainedHealth
                            self.wall.maxHealth = newMaxHealth
                # if you click homing bullets
                elif Collision.PointOnRect(mousePos, self.homingBullets.pos, self.homingBullets.width, self.homingBullets.height):
                    if self.money >= self.homingBullets.cost and self.player.gun.homingBullets is False:
                        self.player.gun.homingBullets = True
                        self.homingBullets.canUpgrade = False
                        self.money -= self.homingBullets.cost
                        self.homingBullets.SetCost(0)
                # if you click on Add Another bullet
                elif Collision.PointOnRect(mousePos, self.addAnotherBullet.pos, self.addAnotherBullet.width, self.addAnotherBullet.height):
                    if self.money >= self.addAnotherBullet.cost:
                        self.player.gun.bulletsShootingPerClick += 1
                        self.money -= self.addAnotherBullet.cost
                # if you click on Freeze Power:
                elif Collision.PointOnRect(mousePos, self.freezePower.pos, self.freezePower.width, self.freezePower.height):
                    self.ownedPowers.append(self.FREEZEPOWER)

        if self.lose:
            if button == 1:
                if Collision.PointOnRect(mousePos, self.playAgainButton.pos, self.playAgainButton.width, self.playAgainButton.height):
                    self.__init__(1400, 800)

    def OnScroll(self, x, y):
        if self.wave.inBetweenWaves is False:
            y = -1 * y

            # if you scroll the opposite side the players moving instantly turn around
            if y > 0 > self.player.vel.y or y < 0 < self.player.vel.y:
                self.player.velGoal.y = 0
                self.player.vel.y = 0
                return

            self.player.velGoal.y += y * 2

    def OnWindowResize(self, screenWidth, screenHeight):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
