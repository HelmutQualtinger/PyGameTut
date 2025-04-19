import pygame
import os

# Init and Create Window (win)
pygame.init()
win_height = 800
win_width = 1200
win = pygame.display.set_mode((win_width, win_height), pygame.DOUBLEBUF | pygame.HWSURFACE)

# Load and Size Images
stationary = pygame.transform.scale(pygame.image.load(os.path.join("Assets/Hero", "standing.png")), (64*3/2, 64*3/2))

left =[pygame.transform.scale(pygame.image.load(os.path.join("Assets/Hero", f"L{i}.png")), (64*3/2, 64*3/2)) for i in range (1, 10)]
right =[pygame.transform.scale(pygame.image.load(os.path.join("Assets/Hero", f"R{i}.png")), (64*3/2, 64*3/2)) for i in range (1, 10)]


background = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Background.png")), (win_width, win_height))

class Hero:
    def __init__(self, x, y):
        # Walk
        self.x = x
        self.y = y
        self.velx = 10
        self.vely = 10
        self.face_right = False
        self.face_left = False
        self.stepIndex = 0
        # Jump
        self.jump = False

    def move_hero(self, userInput):
        if userInput[pygame.K_RIGHT] and self.x <= win_width - 62:
            self.x += self.velx
            self.face_right = True
            self.face_left = False
        elif userInput[pygame.K_LEFT] and self.x >= 0:
            self.x -= self.velx
            self.face_right = False
            self.face_left = True
        else:
            self.face_right = False
            self.face_left = False
            self.stepIndex = 0

    def draw(self, win):

        if self.face_left:
            win.blit(left[self.stepIndex], (self.x, self.y))
            self.stepIndex += 1
        elif self.face_right:
            win.blit(right[self.stepIndex], (self.x, self.y))
            self.stepIndex += 1
        else:
            win.blit(stationary, (self.x, self.y))
        self.stepIndex += 1
        self.stepIndex %= 9

    def jump_motion(self, userInput):
        if userInput[pygame.K_SPACE] and self.jump is False:
            self.jump = True
        if self.jump:
            self.y -= self.vely*4
            self.vely -= 1
        if self.vely < -10:
            self.jump = False
            self.vely = 10


# Draw Game
def draw_game():
    win.blit(background, (0,0))
    player.draw(win)
    pygame.time.delay(30)
    pygame.display.flip()

# Instance of Hero-Class
player = Hero(250, 400*3/2)
              

# Mainloop
run = True
while run:

    # Quit Game
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_q)):
            run = False
    # Input
    userInput = pygame.key.get_pressed()
    # Movement
    player.move_hero(userInput)
    player.jump_motion(userInput)
    # Draw Game in Window
    draw_game()
