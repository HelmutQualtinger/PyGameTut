import pygame
import os
win_width = 800
win_height = 400
# Init and Create Window (win)

# Load and Size Images
# Load images for the hero's stationary, left, and right movements

def load_artwork():
    global stationary, left, right, bullet_img, background,win_height, win_width
    stationary = pygame.image.load(os.path.join("Assets/Hero", "standing.png"))
    left =  [pygame.image.load(os.path.join("Assets/Hero", f"L{i}.png")) for i in range (1, 10)]
    right = [pygame.image.load(os.path.join("Assets/Hero", f"R{i}.png")) for i in range (1, 10)]

    bullet_img = pygame.transform.scale(pygame.image.load(os.path.join("Assets/Bullets", "light_bullet.png")), (10, 10))
    background = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Background.png")), (win_width, win_height))

class Hero:
    """Represents the main player character in the game."""
    def __init__(self, x, y):
        # Walk
        self.x = x
        self.y = y
        self.velx = 10
        self.vely = 10
        self.face_right = True
        self.face_left = False
        self.stepIndex = 0
        # Jump
        self.jump = False
        # Bullet
        self.bullets = []
        self.cooldown = 0

    def move_hero(self, userInput):
        """Moves the hero based on user input (left or right arrow keys)."""
        if userInput[pygame.K_RIGHT] and self.x <= win_width - 62:
            self.x += self.velx
            self.face_right = True
            self.face_left = False
        elif userInput[pygame.K_LEFT] and self.x >= 0:
            self.x -= self.velx
            self.face_right = False
            self.face_left = True
        else:
            self.stepIndex = 0

    def draw(self, win):
        """Draws the hero on the game window, animating the movement."""
        if self.stepIndex >= 9:
            self.stepIndex = 0
        if self.face_left:
            win.blit(left[self.stepIndex], (self.x, self.y))
            self.stepIndex += 1
        if self.face_right:
            win.blit(right[self.stepIndex], (self.x, self.y))
            self.stepIndex += 1

    def jump_motion(self, userInput):
        """Handles the hero's jump motion."""
        if userInput[pygame.K_SPACE] :
            self.jump = True
        if self.jump:
            self.y -= self.vely*4
            self.vely -= 1
        if self.vely < -10:
            self.jump = False
            self.vely = 10

    def direction(self):
        """Returns the direction the hero is facing (1 for right, -1 for left)."""
        if self.face_right:
            return 1
        if self.face_left:
            return -1

    def shoot(self,userInput):
        if userInput[pygame.K_f] and not self.cooldown:
            # Create a new bullet if the 'f' key is pressed and cooldown is not active
            bullet = Bullet(self.x, self.y, self.direction())
            self.bullets.append(bullet)
            self.cooldown = 3
        elif self.cooldown > 0:
            # Decrement the cooldown if it's active
            self.cooldown -= 1
        self.bullets = list(filter(lambda bullet: not bullet.off_screen(), self.bullets))
        # Filter out bullets that are off-screen and move the remaining bullets
        for bullet in self.bullets:
            bullet.move()
                 
class Bullet:
    """Represents a bullet fired by the hero."""
    def __init__(self, x, y, direction):
        self.x = x + 15
        self.y = y + 25
        self.direction = direction
        """Initializes the bullet's position and direction."""

    def draw_bullet(self,win):
        win.blit(bullet_img, (self.x, self.y))

    def move(self):
        # Move the bullet based on its direction
        if self.direction == 1:
            self.x += 15
        if self.direction == -1:
            self.x -= 15

    def off_screen(self):
        """Checks if the bullet is off-screen."""
        return not(self.x >= 50 and self.x <= win_width-50)

# Draw Game
def draw_game(win):    
    """Draws all game elements on the window."""
    win.blit(background, (0,0))
    player.draw(win)
    for bullet in player.bullets:
        bullet.draw_bullet(win)
    pygame.time.delay(30)
    pygame.display.flip()



# Mainloop
# Instance of Hero-Class
def main():
    global stationary, left, right, bullet_img, background,win_height, win_width
    load_artwork()
    global player
    player = Hero(250, 290)
    pygame.init()
    win_height = 400
    win_width = 800
    win = pygame.display.set_mode((win_width, win_height))
    run = True
    while run:
        # Quit Game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Input
        userInput = pygame.key.get_pressed()

        # Shoot
        player.shoot(userInput)

        # Movement
        player.move_hero(userInput)
        player.jump_motion(userInput)

        # Draw Game in Window
        draw_game(win)


if __name__ == "__main__":
    main()
    pygame.quit()