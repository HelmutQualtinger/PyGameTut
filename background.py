import pygame
import os

pygame.init()
win = pygame.display.set_mode((1001, 500))
bg_img = pygame.image.load(os.path.join("Assets","background2.png"))
bg = pygame.transform.scale(bg_img, (1000, 500))
clock = pygame.time.Clock()
width = 1000
i = 0

run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    win.fill((0,0,0))

    #Create looping background
    win.blit(bg, (i, 0))
    win.blit(bg, (width+i,0))
    if i == -width:
        win.blit(bg, (width+i, 0))
        i = 0
    i -= 1
    clock.tick(60)

    pygame.display.update()