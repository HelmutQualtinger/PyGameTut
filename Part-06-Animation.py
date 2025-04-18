import pygame
import os

pygame.init()
win = pygame.display.set_mode((1500, 500))

# Load Images of the Character (there are two popular ways)
stationary = pygame.transform.scale(pygame.image.load(os.path.join("Assets/Hero", "standing.png")), (192, 192))
# One way to do it - using the sprites that face left.
left    = [pygame.transform.scale(pygame.image.load(os.path.join("Assets/Hero", f"L{i}.png")), (192, 192)) for i in range(1, 10)]
right   = [pygame.transform.scale(pygame.image.load(os.path.join("Assets/Hero", f"R{i}.png")), (192, 192)) for i in range(1, 10)]



# Draw the Game
def draw_game():
    global stepIndex
    win.fill((0, 0, 0))
    if stepIndex >= 9:
        stepIndex = 0
    if move_left:
        win.blit(left[stepIndex], (x, y))
        stepIndex += 1
    elif move_right:
        win.blit(right[stepIndex], (x, y))
        stepIndex += 1
    else:
        win.blit(stationary, (x,y))


# Main Loop
def animation():
    global move_left, move_right, x, y, stepIndex
    stepIndex = 0
    x = 250
    y = 50
    vel = 10
    move_left = False
    move_right = False
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_game()

        # Movement
        move_left = False
        move_right = False
        userInput = pygame.key.get_pressed()
        if userInput[pygame.K_LEFT]:
            x -= vel
            move_left = True
        elif userInput[pygame.K_RIGHT]:
            x += vel
            move_right = True
    

        pygame.time.delay(60)
        pygame.display.update()
        
if __name__ == "__main__":
    animation()
    
