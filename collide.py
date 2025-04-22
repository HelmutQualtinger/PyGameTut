import pygame

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption("Sprite Collision Example")

# Define sprite class
class MySprite(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y):
        super().__init__()
        self.image = pygame.Surface((width, height))
#        self.image.set_alpha(100)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Create two sprites
sprite1 = MySprite((255, 0, 0,10), 90, 90, 100, 100)
sprite2 = MySprite((0, 0, 255,10), 50, 50, 200, 200)

# Sprite group (optional but useful)
import sys

all_sprites = pygame.sprite.Group(sprite1, sprite2)

# Main loop
clock = pygame.time.Clock()
running = True

while running:
    screen.fill((255, 255, 255))  # Clear screen with white

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            # Check if the left mouse button is pressed (index 0)
            if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[1]:
                # Update the center of sprite1 to the mouse position
                sprite1.rect.center = event.pos

    # Move sprite2 with arrow keys (for testing collisions)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        sprite2.rect.x -= 1
    if keys[pygame.K_RIGHT]:
        sprite2.rect.x += 1
    if keys[pygame.K_UP]:
        sprite2.rect.y -= 1
    if keys[pygame.K_DOWN]:
        sprite2.rect.y += 1
    
    # Draw sprites
    all_sprites.draw(screen)

    # Collision detection
    if pygame.sprite.collide_rect(sprite1, sprite2):
        pygame.draw.rect(screen, (0, 255, 0), sprite1.rect, 3)
        pygame.draw.rect(screen, (0, 255, 0), sprite2.rect, 3)
        print("Collision detected!")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
