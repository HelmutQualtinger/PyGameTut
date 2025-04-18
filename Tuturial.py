import pygame
from math import sin, pi

print(pygame.init())
surface = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Tutorial")
clock = pygame.time.Clock()
clock.tick(60)
print(clock)
i = 0  # Initialize i outside the loop
rect_x = 100
rect_y = 100
rect_width = 100
rect_height = 200

while True:
    i += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()
    rect_x = 100 + round(sin(i / 60 * 2 * pi) * 100)
    rect_y = 100 + round(sin(i / 60 * 2 * pi) * 100)
    rect_width = 100 + i % 100
    rect_height = 200 + i % 100
    surface.fill((255, 255, 255))  # Fill the surface before drawing
    pygame.draw.rect(surface, (128, 0, 0), (rect_x, rect_y, rect_width, rect_height))
    pygame.display.flip()  # Use flip instead of update for smoother animation
    clock.tick(60)

