import pygame
import os

win_width = 800
win_height = 400

def load_artwork():
    global stationary, left, right, bullet_img, background, win_height, win_width, right_enemy, left_enemy
    stationary = pygame.image.load(os.path.join("Assets/Hero", "standing.png"))
    left =  [pygame.image.load(os.path.join("Assets/Hero", f"L{i}.png")) for i in range (1, 10)]
    right = [pygame.image.load(os.path.join("Assets/Hero", f"R{i}.png")) for i in range (1, 10)]
    bullet_img = pygame.transform.scale(pygame.image.load(os.path.join("Assets/Bullets", "light_bullet.png")), (10, 10))
    background = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Background.png")), (win_width, win_height))
    left_enemy = [pygame.image.load(os.path.join("Assets/Enemy", f"L{i}E.png")) for i in range(1, 9)] + \
                 [pygame.image.load(os.path.join("Assets/Enemy", f"L{i}P.png")) for i in range(9, 12)]
    right_enemy = [pygame.image.load(os.path.join("Assets/Enemy", f"R{i}E.png")) for i in range(1, 9)] + \
                  [pygame.image.load(os.path.join("Assets/Enemy", f"R{i}P.png")) for i in range(9, 12)]

class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images_right = right
        self.images_left = left
        self.image = stationary
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velx = 10
        self.vely = 10
        self.face_right = True
        self.face_left = False
        self.stepIndex = 0
        self.jump = False
        self.bullets = pygame.sprite.Group()
        self.cooldown = 0
        self.health = 100

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
            self.rect.y -= self.vely * 4
            self.vely -= 1
        if self.vely < -10:
            self.jump = False
            self.vely = 10

    def shoot(self, userInput):
        if userInput[pygame.K_f] and not self.cooldown:
            bullet = Bullet(self.rect.x, self.rect.y, 1 if self.face_right else -1)
            self.bullets.add(bullet)
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
        win.blit(self.image, self.rect.topleft)
        for bullet in self.bullets:
            bullet.draw(win)
        pygame.draw.rect(win, (0, 255, 0), (self.rect.x, self.rect.y+64, 30, 10))
        pygame.draw.rect(win, (255, 0, 0), (self.rect.x, self.rect.y+64, 30-self.health, 10))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.images_right = right_enemy
        self.images_left = left_enemy
        self.direction = direction
        self.stepIndex = 0
        self.image = self.images_right[0] if direction == 1 else self.images_left[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velx = 5
        self.health = 30

    def update(self):
        self.rect.x += self.velx * self.direction
        if self.rect.x <= 0 or self.rect.x >= win_width:
            self.direction *= -1
        self.stepIndex = (self.stepIndex + 1) % len(self.images_right)
        self.image = self.images_right[self.stepIndex] if self.direction == 1 else self.images_left[self.stepIndex]

    def draw(self, win):
        win.blit(self.image, self.rect.topleft)
        pygame.draw.rect(win, (0, 255, 0), (self.rect.x, self.rect.y+64, 30, 10))
        pygame.draw.rect(win, (255, 0, 0), (self.rect.x, self.rect.y+64, 30-self.health, 10))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
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

def draw_game(win, font, player, enemies):
    win.blit(background, (0,0))
    player.draw(win)
    for enemy in enemies:
        enemy.draw(win)
    text = font.render('Health: ' + str(player.health), True, "yellow")
    win.blit(text, (10, 10))
    pygame.display.flip()

def main():
    global stationary, left, right, bullet_img, background, win_height, win_width
    pygame.init()
    load_artwork()
    win = pygame.display.set_mode((win_width, win_height))
    font = pygame.font.Font('freesansbold.ttf', 18)
    player = Hero(250, 290)
    enemies = pygame.sprite.Group(
        Enemy(100, 190, 1),
        Enemy(400, 240, -1),
        Enemy(600, 290, 1)
    )
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        userInput = pygame.key.get_pressed()
        if userInput[pygame.K_ESCAPE] or userInput[pygame.K_q]:
            run = False
        player.shoot(userInput)
        player.update(userInput)
        enemies.update()

        # Kollisionsabfrage: Bullet trifft Enemy
        hits = pygame.sprite.groupcollide(player.bullets, enemies, True, False)
        for enemy in hits.values():
            enemy[0].health -= 1
            if enemy[0].health <= 0:
                enemy[0].kill()
                
        # Kollisionsabfrage: Enemy trifft Hero
        if pygame.sprite.spritecollide(player, enemies, False):
            player.health -= 1

        draw_game(win, font, player, enemies)

        pygame.time.delay(60)
    pygame.quit()

if __name__ == "__main__":
    main()