import pygame
pygame.init()
win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("First Game")

x = 250
y = 250
radius = 15
vel = 1

run = True
while run:

    win.fill((0, 80, 20))
    pygame.draw.circle(win, (160, 0, 40), (int(x), int(y)), radius)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            run = False

    # Movement
    userInput = pygame.key.get_pressed()
    if userInput[pygame.K_LEFT]:
        x -= vel
    if userInput[pygame.K_RIGHT]:
        x += vel
    if userInput[pygame.K_UP]:
        y -= vel
    if userInput[pygame.K_DOWN]:
        y += vel
    y = min(max(y, radius), 500 - radius)
    x = min(max(x, radius), 500 - radius)

    pygame.time.delay(1)
    pygame.display.update()