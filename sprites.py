import pygame
import os
import math

win_width = 800
win_height = 400

def load_artwork():
    global stationary, left, right, bullet_img, background, win_height, win_width, right_enemy, left_enemy,castle,pop_sound,quake_sound
    stationary = pygame.image.load(os.path.join("Assets/Hero", "standing.png"))
    left =  [pygame.image.load(os.path.join("Assets/Hero", f"L{i}.png")) for i in range (1, 10)]
    right = [pygame.image.load(os.path.join("Assets/Hero", f"R{i}.png")) for i in range (1, 10)]
    bullet_img = pygame.transform.scale(pygame.image.load(os.path.join("Assets/Bullets", "light_bullet.png")), (10, 10))
    background = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Background.png")), (win_width, win_height))
    left_enemy =[pygame.image.load(os.path.join("Assets/Enemy", f"L{i}E.png")) for i in range(1, 9)] + \
                [pygame.image.load(os.path.join("Assets/Enemy", f"L{i}P.png")) for i in range(9, 12)]
    right_enemy =   [pygame.image.load(os.path.join("Assets/Enemy", f"R{i}E.png")) for i in range(1, 9)] + \
                    [pygame.image.load(os.path.join("Assets/Enemy", f"R{i}P.png")) for i in range(9, 12)]
                
    castle = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Tower.png")), (200, 200))
    
    pygame.mixer.music.load(os.path.join("Assets/Audio", "music.ogg"))
    pop_sound = pygame.mixer.Sound(os.path.join("Assets/Audio", "pop.ogg"))
    quake_sound = pygame.mixer.Sound(os.path.join("Assets/Audio", "crash.mp3"))
    pygame.mixer.music.play(-1)


class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images_right = right # frames when moving right
        self.images_left = left # frames when moving left
        self.image = stationary # frame facing player
        self.rect = self.image.get_rect(topleft=(x, y)) # where the player starts
        self.velx = 10 # standard speed
        self.vely = 10 # standard jump speed
        self.face_right = True
        self.face_left = False
        self.stepIndex = 0   # index of the current frame
        self.jump = False    # indicates if the hero is jumping
        self.bullets = pygame.sprite.Group()  # all fired bullets until the hit somethin of leave the screen
        self.cooldown = 0  # cooldown for shooting
        self.health = 30    # health of the player
        self.lives = 3      # lives of the player
        
    def __repr__(self):
        return super().__repr__()+f"right: {self.face_right}, left: {self.face_left}, health: {self.health} rect: {self.rect}, jump: {self.jump}, cooldown: {self.cooldown}"
    
    def update(self, userInput):
        if userInput[pygame.K_RIGHT] and self.rect.x <= win_width - 62:
            self.rect.x += self.velx
            self.face_right = True
            self.face_left = False
        elif userInput[pygame.K_LEFT] and self.rect.x >= 0:
            self.rect.x -= self.velx
            self.face_right = False
            self.face_left = True
        else:
            self.stepIndex = 0

        if userInput[pygame.K_SPACE] or userInput[pygame.K_UP]:
            self.jump = True
        if self.jump:
            self.rect.y -= self.vely * 2
            self.vely -= 1
        if self.vely < -10:
            self.jump = False
            self.vely = 10

    def shoot(self, userInput):
        global pop_sound
        if userInput[pygame.K_f] and not self.cooldown:
            bullet = Bullet(self.rect.x, self.rect.y, 1 if self.face_right else -1)
            self.bullets.add(bullet)
            pop_sound.play()
            self.cooldown = 3
        elif self.cooldown > 0:
            self.cooldown -= 1
        self.bullets.update()

    def draw(self, win):
        if self.stepIndex >= 9:
            self.stepIndex = 0
        if self.face_left:
            self.image = self.images_left[self.stepIndex]
            self.stepIndex += 1
        elif self.face_right:
            self.image = self.images_right[self.stepIndex]
            self.stepIndex += 1
 #       pygame.draw.rect(win, (0, 0, 0), self.rect,1)  # Hit box
        win.blit(self.image, self.rect.topleft)
        self.bullets.draw(win)
        pygame.draw.rect(win, (0, 255, 0), (self.rect.x+15, self.rect.y+64, 30, 10))
        pygame.draw.rect(win, (255, 0, 0), (self.rect.x+16, self.rect.y+64, 30-self.health, 10))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, direction,name):
        super().__init__()
        self.name = name
        self.images_right = right_enemy
        self.images_left = left_enemy
        self.direction = direction
        self.stepIndex = 0
        self.image = self.images_right[0] if direction == 1 else self.images_left[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velx = 2
        self.health = 30

    def update(self):
        self.rect.x += self.velx * self.direction
        if self.rect.x <= 0 or self.rect.x >= win_width:
            self.direction *= -1
        self.stepIndex = (self.stepIndex + 1) % len(self.images_right)
        self.image = self.images_right[self.stepIndex] if self.direction == 1 else self.images_left[self.stepIndex]

    def draw(self, win):
        win.blit(self.image, self.rect.topleft)
#        pygame.draw.rect(win, (0, 0, 0), (self.rect.x+15, self.rect.y+4, 32, 64),1)  # Hit box
        pygame.draw.rect(win, (0, 255, 0), (self.rect.x+15, self.rect.y+64, 30, 10))
        pygame.draw.rect(win, (255, 0, 0), (self.rect.x+15, self.rect.y+64, 30-self.health, 10))
    
    def __repr__(self):
        return super().__repr__()+f"Enemy {self.name}, health: {self.health} rect: {self.rect} stepIndex: {self.stepIndex}"

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super()xs.__init__()

        self.image = bullet_img
        self.rect = self.image.get_rect(center=(x+15, y+25))
        self.direction = direction

    def update(self):
        self.rect.x += 15 * self.direction
        if self.off_screen():
            self.kill()

    def draw(self, win):

        win.blit(self.image, self.rect.topleft)

    def off_screen(self):
        return not (0 <= self.rect.x <= win_width)
    
# Castle
class Castle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        global castle
        self.castle_hit = 0
        self.image = castle
        self.rect = self.image.get_rect(topleft=(x, y))
    def update(self):        
        global castle_health
#        self.rect = self.image.get_rect(topleft=(-50, win_height - 220))
        self.rect.y = 140 + (10 - castle_health) * 20
        if self.castle_hit>0 and castle_health > 0:
            shake =math.sin(self.castle_hit)*10
            self.rect.x = -50 + shake
            self.castle_hit -= 1
         
    def draw(self, win):
        pass
        global music
        music = pygame.mixer.music.load(os.path.join("Assets/Audio", "music.ogg"))
        pygame.mixer.music.play(-1)


    
def draw_game(win, font, player, enemies):
    global kills,castle_health,castle_group
    win.blit(background, (0,0))
    player.draw(win)
    for enemy in enemies:
        enemy.draw(win)
    castle_group.draw(win)
    text = font.render('Health: ' + str(player.health), True, "darkred")
    win.blit(text, (10, 10))
    text = font.render('Lives: ' + str(player.lives), True, "darkred")
    win.blit(text, (10, 30))
    text = font.render('Kills: ' + str(kills), True, "darkred")
    win.blit(text, (10, 50))
    text = font.render('Castle Health: ' + str(castle_health), True, "darkred")
    win.blit(text, (10, 70))




def main():
    global stationary, left, right, bullet_img, background 
    global win_height, win_width,kills,castle_health, castle,castle_obj,castle_group,enemies
    kills = 0
    pygame.init()
    load_artwork()
    win = pygame.display.set_mode((win_width, win_height))
    font = pygame.font.Font('freesansbold.ttf', 18)
    game_over = False
    player = Hero(250, 290)
    enemies = pygame.sprite.Group(
        Enemy(600, 290, 1, "Hugo")
        
    )
    castle_health = 10
    castle_obj      = Castle(-50, win_height - 220)
    castle_group = pygame.sprite.Group()
    castle_group.add(castle_obj)
    run = True
    while run:
        pygame.time.Clock().tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        userInput = pygame.key.get_pressed()
        if userInput[pygame.K_ESCAPE] or userInput[pygame.K_q]:
            run = False
        player.shoot(userInput)
        player.update(userInput)
        enemies.update()
        castle_obj.update()

        # Kollisionsabfrage: Bullet trifft Enemy
        hits = pygame.sprite.groupcollide(player.bullets, enemies, True, False)
        for enemy in hits.values():
            enemy[0].health -= 1

            if enemy[0].health <= 0:
                enemy[0].kill()
                kills += 1
                print("Enemy killed")
                enemies.add(Enemy(750, 290, -1, "Hugo"))
                
        # Kollisionsabfrage: Enemy trifft Hero
        for i, enemy in enumerate(pygame.sprite.spritecollide(player, enemies, False)):            
            if pygame.sprite.collide_mask(player, enemy):
#                print("Mask Collision with ", enemy)
                player.health -= 1
                if player.health <= 0:
                    print("Killed by ", enemy)
                    player.health = 30
                    player.lives -= 1
                    if player.lives <= 0:
                        print("Game Over")
                        game_over = True
            else:
                pass
#                print("Masks not colliding")

#       # Kollisionsabfrage: Enemy trifft Castle
        for enemy in pygame.sprite.spritecollide(castle_obj, enemies, False):
            if pygame.sprite.collide_mask(castle_obj, enemy):
                enemy.kill()
                enemies.add(Enemy(750, 290, -1, "Hugo"))
                castle_obj.castle_hit = 120
                quake_sound.play()
                castle_health -= 1
                if castle_health <= 0:
                    print("Castle destroyed")
                    game_over = True
            
            

        if game_over:
            text = font.render('Game Over, Press r to restart', True, "red")
            win.blit(text, (win_width // 2 - text.get_width() // 2, win_height // 2 - text.get_height() // 2))
            pygame.display.flip()
            if userInput[pygame.K_r]:
                game_over = False
                kills = 0
                castle_health = 10
                player.health = 30
                player.lives = 3
                enemies.empty()
                enemies.add(Enemy(600, 290, 1, "Hugo"))
                pygame.time.delay(20)
        else:

            draw_game(win, font, player, enemies)

            pygame.display.flip()


    pygame.quit()

if __name__ == "__main__":
    main()