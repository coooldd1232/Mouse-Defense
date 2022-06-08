import pygame
import time

from reusableClasses.Vector2 import Vector2

from game import Game

pygame.init()

screen = pygame.display.set_mode((1400, 800), pygame.RESIZABLE)
pygame.display.set_caption('game')

game = Game(screen.get_width(), screen.get_height())

clock = pygame.time.Clock()

gameRunning = True

lastFrame = time.time()
while gameRunning:
    currentTime = time.time()
    dt = currentTime - lastFrame
    lastFrame = currentTime

    mousePos = pygame.mouse.get_pos()
    mousePos = Vector2(mousePos[0], mousePos[1])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRunning = False
        if event.type == pygame.WINDOWRESIZED:
            game.OnWindowResize(screen.get_width(), screen.get_height())
        if event.type == pygame.MOUSEBUTTONDOWN:
            game.OnClick(event.button, mousePos)
        if event.type == pygame.MOUSEWHEEL:
            game.OnScroll(event.x, event.y)

    game.Update(dt, mousePos)
    game.Draw(screen)

    clock.tick(120)

pygame.quit()
