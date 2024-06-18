import pygame.locals
import pygame
from math import cos, sin, pi, sqrt
from random import random, randint
import time
import pymunk
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

pygame.init()
pygame.mixer.init()
pygame.font.init()
pygame.display.set_caption("Jeu 1")

# Unmodifiable
SIZE = [540, 960]
FPS = 60
STEPS_PER_S = 10
FONT = "minecraft"
MP3 = pygame.mixer.Sound("./ball.mp3")
my_font = pygame.font.SysFont(FONT, 40)
collisions = 0
space = pymunk.Space()
space.gravity = 0, 500
screen = pygame.display.set_mode(tuple(SIZE), pygame.FULLSCREEN)
clock = pygame.time.Clock()
balls = []
lines = []
then = time.time()


def add_ball(coor, color=None):
    ballObj = pymunk.Body(pymunk.Body.DYNAMIC)
    ballObj.position = (coor[0], coor[1])
    ball = pymunk.Circle(ballObj, 10)
    ball.density = 1
    ball.elasticity = .99
    balls.append([ball, color or random_color()])
    space.add(ballObj, ball)

    if len(balls) > 500:
        exit(0)


def add_circle(sides, radius, position, thickness, exclude=[]):
    arcObj = pymunk.Body(0, 0, pymunk.Body.STATIC)
    arcObj.position = (0, 0)

    arc_coor = []
    for i in range(0, sides):
        arc_coor.append((
            position[0] + radius*cos(2*pi * (i/sides)),
            position[1] + radius*sin(2*pi * (i/sides))
        ))

    for i in range(len(arc_coor)):
        if i in exclude:
            continue
        line = pymunk.Segment(arcObj,
                              arc_coor[i],  # PB
                              arc_coor[0 if (i == (len(arc_coor)-1)) else (i+1)], thickness)
        line.elasticity = 1
        lines.append(line)
    space.add(arcObj, *lines)
    return arcObj


def random_coor_inside_circle(position, radius):
    r1 = random()
    r2 = random()
    return [
        position[0] + r2*radius*cos(r1 * 2*pi),
        position[1] + r2*radius*sin(r1 * 2*pi)
    ]


def random_color():
    return (randint(0, 255), randint(0, 255), randint(0, 255))


def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                exit(0)
            elif keys[pygame.locals.K_2]:
                FPS += 1
            elif keys[pygame.locals.K_1]:
                FPS -= 1
            elif keys[pygame.locals.K_3]:
                SPEED += 1
            elif keys[pygame.locals.K_4]:
                SPEED -= 1


def remove_gone_balls():
    offset = 0
    for a in range(len(balls)):
        a = a-offset
        if balls[a][0].body.position[-1] > 1000:
            space.remove(balls[a][0])
            del balls[a]
            offset += 1


def count_collision():
    global collisions
    for a in range(len(balls)):
        for b in range(a, len(balls)):
            if a != b:
                if len(balls[a][0].shapes_collide(balls[b][0]).points):
                    MP3.play()
                    collisions += 1


def draw_balls():
    for ball in balls:
        pygame.draw.circle(screen,
                           ball[1],
                           ball[0].body.position,
                           ball[0].radius)


def draw_circle():
    for i in range(len(lines)):
        pygame.draw.line(
            screen,
            "white",
            lines[i].a,
            lines[i].b,
            int(lines[i].radius)
        )


def draw_text():
    duration = time.time() - then
    # integer minutes & seconds
    mins = int(duration / 60)
    secs = int(duration % 60)
    # String representation
    mins = (str(mins)+"m") if mins else ""
    secs = (str(secs)+"s") if secs else ""

    texts = [
        'Number of collisions: '+str(collisions),
        'Time:' + " ".join([mins, secs])
    ]

    for i in range(len(texts)):
        text_surface = my_font.render(
            list(reversed(texts))[i],
            False,
            "white"
        )
        screen.blit(text_surface, (50, SIZE[1]/5 - 40*i))


def game_loop():
    while True:
        check_events()
        space.step(1/FPS / STEPS_PER_S)

        remove_gone_balls()
        count_collision()
        # Background
        screen.fill("black")
        draw_balls()
        draw_circle()
        draw_text()

        pygame.display.flip()
        clock.tick(FPS * STEPS_PER_S)


radius = 200
circle_position = list(map(lambda x: int(x/2), SIZE))
add_circle(
    sides=100,
    radius=radius,
    position=circle_position,
    thickness=10
)
for _ in range(2):
    add_ball(
        random_coor_inside_circle(circle_position, 200),
        random_color()
    )

game_loop()
