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
RATIO = 9/16
WIDTH = 960  # 1920/2 # 480
SIZE = [WIDTH*RATIO, WIDTH]
FPS = 60
STEPS_PER_S = 10
NGON = 100
FONT = "minecraft"
CIRCLE_RADIUS = 200
CIRCLE_THICKNESS=10
MP3 = pygame.mixer.Sound("./ball.mp3")
BALL_ELASTICITY = .95
my_font = pygame.font.SysFont(FONT, 40)
collisions = 0
space = pymunk.Space()
space.gravity = 0, 500
screen = pygame.display.set_mode(tuple(SIZE), pygame.FULLSCREEN)
clock = pygame.time.Clock()
balls = []
lines = []
then = time.time()


def add_ball(coor: list[int], color=None):
    ballObj = pymunk.Body(pymunk.Body.DYNAMIC)
    ballObj.position = (coor[0], coor[1])
    ball = pymunk.Circle(ballObj, 10)
    ball.density = 1
    ball.elasticity = BALL_ELASTICITY
    balls.append([ball, color or random_color()])
    space.add(ballObj, ball)

    if len(balls) > 500:
        exit(0)


def add_balls():
    ball_coor = [
        [int(SIZE[0]/2)-randint(-30, 30), int(SIZE[1]/2) - randint(-30, 30)],
        [int(SIZE[0]/2)-randint(-30, 30), int(SIZE[1]/2) - randint(-30, 30)]
    ]
    for ball in ball_coor:
        add_ball(ball)


def add_circle():
    arcObj = pymunk.Body(0, 0, pymunk.Body.STATIC)
    arcObj.position = (0, 0)

    arc_coor = []
    for i in range(0, NGON):
        arc_coor.append((
            SIZE[0]/2 + CIRCLE_RADIUS*cos(2*pi * (i/NGON)),
            SIZE[1]/2 + CIRCLE_RADIUS*sin(2*pi * (i/NGON))
        ))

    for i in range(len(arc_coor)):
        # if i > 10 and i < 12:
        #     continue
        line = pymunk.Segment(arcObj,
            arc_coor[i],  # PB
            arc_coor[0 if (i == (len(arc_coor)-1)) else (i+1)],CIRCLE_THICKNESS)
        line.elasticity = 1
        lines.append(line)
    space.add(arcObj, *lines)


def random_coor():
    r = random()
    return [
        SIZE[0]/2 + random()*CIRCLE_RADIUS*cos(r * 2*pi),
        SIZE[1]/2 + random()*CIRCLE_RADIUS*sin(r * 2*pi)
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
                    # if COLLISIONS % 10 == 0:
                    #     add_ball(random_coor(),random_color())


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
        'Time: ' + " ".join([mins, secs]),
        'bimoware on Github',
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

add_circle()
add_balls()
game_loop()
