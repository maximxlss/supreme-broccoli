import pygame as pg
from time import time, sleep
import numpy as np
import math
from random import randint
from physics import PhysicalObject as PObj

pg.init() 
clock = pg.time.Clock()
screen = pg.display.set_mode((1100, 700))

shipFigure = np.array(((0,-8), (8,8), (0,0), (-8,8)))
rotatedShip = np.array(((0,-8), (8,8), (0,0), (-8,8)))

up = False
left = False
right = False

particles = []

pobj = PObj()
speed = 20
rotation = 0

def rot(point, deg):
    rad = math.radians(deg)
    x, y = point
    xx = x * math.cos(rad) + y * math.sin(rad)
    yy = -x * math.sin(rad) + y * math.cos(rad)

    return xx, yy


while 1:
    screen.fill((0,0,0))
    if left and right: pass
    elif left:
        rotation += 1
        if rotation <= -360 or rotation >= 360:
            rotation = 0
        rotatedShip = []
        for point in shipFigure:
            rotatedShip.append(rot(point, rotation))
    elif right:
        rotation += -1
        if rotation <= -360 or rotation >= 360:
            rotation = 0
        rotatedShip = []
        for point in shipFigure:
            rotatedShip.append(rot(point, rotation))
    if up:
        pobj.acc = np.array((np.cos(math.radians(360-rotation-90))*speed, np.sin(math.radians(360-rotation-90))*speed), dtype="float")
        pobj.acc -= pobj.vel / 4
        particles.append(PObj())
        particles[-1].pos = pobj.pos
        particles[-1].acc = np.array((np.cos(math.radians(rotation-90+randint(-3,3)))*speed, np.sin(math.radians(rotation-90+randint(-3,3)))*speed), dtype="float")
    else:
        pobj.acc = -pobj.vel / 4

    pobj.update()
    for particle in particles:
        particle.acc -= particle.vel / 4
        particle.update()

    pg.draw.polygon(screen, (255,0,0), rotatedShip + pobj.pos + (300, 300))

    pg.display.flip()

    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            exit()
        elif e.type == pg.KEYDOWN or e.type == pg.KEYUP:
            if e.key == pg.K_LEFT:
                left = e.type == pg.KEYDOWN
            elif e.key == pg.K_RIGHT:
                right = e.type == pg.KEYDOWN
            elif e.key == pg.K_UP:
                up = e.type == pg.KEYDOWN

    clock.tick(60)