import pygame
import os
win_width = 800
win_height = 400
# Init and Create Window (win)

# Load and Size Images
# Load images for the hero's stationary, left, and right movements

def load_artwork():
    global stationary, left, right, bullet_img, background,win_height, win_width, right_enemy, left_enemy, font
    stationary = pygame.image.load(os.path.join("Assets/Hero", "standing.png"))
    left =  [pygame.image.load(os.path.join("Assets/Hero", f"L{i}.png")) for i in range (1, 10)]
    right = [pygame.image.load(os.path.join("Assets/Hero", f"R{i}.png")) for i in range (1, 10)]

    bullet_img = pygame.transform.scale(pygame.image.load(os.path.join("Assets/Bullets", "light_bullet.png")), (10, 10))
    background = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Background.png")), (win_width, win_height))

# Load enemy images
    left_enemy = [ pygame.image.load(os.path.join("Assets/Enemy", f"L{i}E.png")) for i in range (1, 9)] + \
            [ pygame.image.load(os.path.join("Assets/Enemy", f"L{i}P.png")) for i in range (9, 12)]
    left_enemy = [pygame.transform.scale(img, (img.get_width() * 1, img.get_height() * 1)) for img in left_enemy]
    right_enemy = [pygame.image.load(os.path.join("Assets/Enemy", f"R{i}E.png")) for i in range (1, 9)] + \
                [pygame.image.load(os.path.join("Assets/Enemy", f"R{i}P.png")) for i in range (9, 12)]
    right_enemy = [pygame.transform.scale(img, (img.get_width() * 1, img.get_height() * 1)) for img in right_enemy]
    for i in range(len(right_enemy)):
        right_enemy[i].set_alpha(255)
    for i in range(len(left_enemy)):
        left_enemy[i].set_alpha(255)
       
                

# Load and Resize Image
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
        self.health = 100

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
        # draw empty rectangle for the hero
        if self.hit():
            color = (255, 0, 0)
        else:
            color = (0, 255, 0)
            
        

        pygame.draw.rect(win, color, (self.x+20, self.y+12, 23, 40), 2)  # Draw a red rectangle for the hero
        pygame.draw.rect(win, (0, 255, 0), (self.x, self.y+64, 30, 10)) # Draw a green  rectangle for the hero's damage
        pygame.draw.rect(win, (255, 00, 0), (self.x, self.y+64, 30-self.health, 10))  # Draw a green background rectangle for the hero

    def jump_motion(self, userInput):
        """Handles the hero's jump motion."""
        if userInput[pygame.K_SPACE] or userInput[pygame.K_UP]:
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
        for bullet in self.bullets:
            bullet.move()
        self.bullets = list(filter(lambda bullet: not bullet.off_screen(), self.bullets))
           
    def hit(self):
        """Handles the enemy being hit by a bullet."""
        # You can implement the logic for when the enemy is hit here
        for enemy in enemies:
            if self.x <= enemy.x <= self.x + 50 and self.y <= enemy.y <= self.y + 50:
# enemy hit by Hero
                self.health -= 5
                print ("Hero hit by goblin!")
                return True
        return False



                 
class Enemy:
    """Represents an enemy in the game."""
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.velx = 5
        self.direction = direction  # 1 for right, -1 for left
        self.stepIndex = 0
        self.health = 30

    def move(self):
        """Moves the enemy horizontally and changes direction if it hits the window boundaries."""
        self.x += self.velx * self.direction
        if self.x <= 0 or self.x >= win_width :
            self.direction *= -1

    def draw(self, win):
        if self.direction == 1:
            win.blit(right_enemy[self.stepIndex], (self.x, self.y))
        if self.direction == -1:
            win.blit(left_enemy[self.stepIndex], (self.x, self.y))
            
        color = (255, 0, 0,12) if self.hit() else (0, 255, 0,10)
        pygame.draw.rect(win, color, (self.x+15, self.y+10, 28, 50), 2)  # Draw a red rectangle for the enemy
        # Draw health bar
        pygame.draw.rect(win, (0, 255, 0,10), (self.x, self.y+64, 30, 10))  # Draw a green background rectangle for the enemy
        pygame.draw.rect(win, (255, 0, 0,10), (self.x, self.y+64, 30 - self.health, 10)) # Draw a red rectangle for the enemy's damege
    
        self.stepIndex += 1
        self.stepIndex %= 11  # Loop through the animation frames
        
    def hit(self):
        """Handles the enemy being hit by a bullet."""
        # You can implement the logic for when the enemy is hit here
        for bullet in player.bullets:
            if self.x <= bullet.x <= self.x + 50 and self.y <= bullet.y <= self.y + 50:
                    # Remove the bullet and the enemy from the game
                    print ("Enemy hit by bullet!")
                    self.health -= 1
                    player.bullets.remove(bullet)
                    return True
        return False

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
def draw_game(win, font):    
    """Draws all game elements on the window."""
    global player, enemies
    win.blit(background, (0,0))
    for bullet in player.bullets:
        bullet.draw_bullet(win)
    player.draw(win)
    for enemy in enemies:
        enemy.draw(win)
    text = font.render('Health: ' + str(player.health), True, "yellow")
    win.blit(text, (10, 10))

    pygame.time.delay(60)
    pygame.display.flip()




# Mainloop
# Instance of Hero-Class
def main():
    global stationary, left, right, bullet_img, background,win_height, win_width,enemies
    load_artwork()
    global player

    pygame.init()
    win_height = 400
    win_width = 800
    win = pygame.display.set_mode((win_width, win_height), pygame.HWSURFACE | pygame.DOUBLEBUF)
    run = True
    font = pygame.font.Font('freesansbold.ttf', 18)     
    
    enemies = [ Enemy(100, 190, 1), Enemy(400, 240, -1), Enemy(600, 290, 1) ]
    player = Hero(250, 290)
    print(enemies)
    while run:
        # Quit Game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Input
        userInput = pygame.key.get_pressed()

        if userInput[pygame.K_ESCAPE] or userInput[pygame.K_q]:
            run = False 
        # Shoot
        player.shoot(userInput)

        # Movement
        player.move_hero(userInput)
        player.jump_motion(userInput)
        
        for enemy in enemies:
            enemy.move()

        # Draw Game in Window
        draw_game(win, font)


if __name__ == "__main__":
    main()
    pygame.quit()