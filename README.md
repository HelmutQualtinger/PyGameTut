# Pygame learning
watched [following videos](https://www.youtube.com/watch?v=cFq3dKa6q0o&t=337s

## first video:

```py
import pygame
from math import sin, pi

print(pygame.init())
surface = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Tutorial")
clock = pygame.time.Clock()

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

```

- `pygame.init()`  initializes package
- `surface =pygame.display.set_mode((800, 600))`   create window with drawable surface
- `clock = pygame.time.Clock()` checks the clockspeed
- `if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):`
- ` pygame.event.get()` get keyboard und mouse event
- `surface.fill()`  empties the surface
- `pygame.draw.rect(surface, (128, 0, 0), (rect_x, rect_y, rect_width, rect_height))` draws a rectangle
- `pygame.display.flip()  # Use flip instead of update for smoother animation` outputs it on the screen


## second video Movement

[Second program](Movement.py)

-`pygame.draw.circle(win, (255, 255, 255), (int(x), int(y)), radius)` draws a circle
- `userInput = pygame.key.get_pressed()` Get the pressed keys
- `     userInput = pygame.key.get_pressed()
    if userInput[pygame.K_LEFT]:
        x -= vel
    if userInput[pygame.K_RIGHT]:
        x += vel
    if userInput[pygame.K_UP]:
        y -= vel
    if userInput[pygame.K_DOWN]:
        y += vel
   `  Compare for arrow keys
- `pygame.time.delay(10)`  wait a while 10 ms
- `pygame.display.update()` update the screen

## constraining movements

in video lots of if and comparison, but min max suggested by Gemini is much less verbose and elegant.

    y = min(max(y, radius), 500 - radius)
    x = min(max(x, radius), 500 - radius)

## changing speed in accordance with Newton and jump
[jumping.py](jumping.py)

Make the velocity variable. Change it when at each iteration.
pygame.event.key.get_pressed() returns a dictionary with all pressed keys

## having a running background
[background.py](background.py)]
Load a png file

```py
win = pygame.display.set_mode((1000, 500))
bg_img = pygame.image.load(os.path.join("Assets","Background.png"))
bg = pygame.transform.scale(bg_img, (1000, 500))
```

blitting images into other images

```py
win.blit(bg, (0+i, 0))
win.blit(bg, (width+i, 0))
````

## running characters and sprites

[Part-06-Animation.py](Part-06-Animation.py)

No particular sprite routines really using