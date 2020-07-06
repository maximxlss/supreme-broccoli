import pygame as pg
from pygame import gfxdraw
from time import time, sleep
import numpy as np
import math
from random import randint
from physics import PhysicalObject 

width, height = 700, 700

pg.init() 
clock = pg.time.Clock()
screen = pg.display.set_mode((width, height))

shipFigure = np.array(((0,-16), (14,10), (0,-4), (-14,10)))
rotatedShip = np.array(((0,-16), (14,10), (0,-4), (-14,10)))

blackHoleFigure = np.array(((-1,2),(-2,1),(-1,-1),(1,-1),(-1,-2),(-2,-1),(-1,-2),(1,-1),(1,1),(2,-1),(1,-2),(2,-1),(1,1),(-1,1),(1,2),(2,1),(1,2),(-1,1),(-1,-1),(-2,1)))

up = False
left = False
right = False
space = False

particles = []
bullets = []

pobj = PhysicalObject()
pobj.pos = np.array((-250,-250), dtype="float")
speed = 50
rotation = 0
bhrot = 0
ptime = 0
btime = 0

def rot(point, deg):
    rad = math.radians(deg)
    x, y = point
    xx = x * np.cos(rad) + y * np.sin(rad)
    yy = -x * np.sin(rad) + y * np.cos(rad)

    return xx, yy


while 1:
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
            elif e.key == pg.K_SPACE:
                space = e.type == pg.KEYDOWN

    ptime += 1
    screen.fill((0,0,0))
    if left and right: pass
    elif left:
        rotation += 2
        if abs(rotation) >= 360:
            rotation = 0
        rotatedShip = []
        for point in shipFigure:
            rotatedShip.append(rot(point, rotation))
    elif right:
        rotation += -2
        if abs(rotation) >= 360:
            rotation = 0
        rotatedShip = []
        for point in shipFigure:
            rotatedShip.append(rot(point, rotation))
    if up:
        pobj.acc = np.array((np.cos(math.radians(360-rotation-90))*speed, np.sin(math.radians(360-rotation-90))*speed), dtype="float")
        if ptime >= 12:
            ptime = 0
            particles.append(PhysicalObject())
            particles[-1].pos = np.array(list(pobj.pos))
            particles[-1].acc += np.array((np.cos(math.radians(360-rotation+90+randint(-45,45)))*speed*2, np.sin(math.radians(360-rotation+90+randint(-45,45))*speed*2)), dtype="float")
    else:
        pobj.acc = -pobj.vel / 3
    bhangle = math.degrees(math.atan2(pobj.pos[1], pobj.pos[0]))
    force = min(height, width)-math.sqrt(pobj.pos[1]**2+pobj.pos[0]**2)
    force = 600 if force <= 0 else force/15
    pobj.acc += np.array((np.cos(math.radians(bhangle+180))*force, np.sin(math.radians(bhangle+180))*force))
    if space:
        if btime == 0:
            btime = 15
            bullets.append(PhysicalObject())
            bullets[-1].pos = np.array(list(pobj.pos))
            bullets[-1].vel = np.array((np.cos(math.radians(360-rotation-90))*speed*4, np.sin(math.radians(360-rotation-90))*speed*4))
            bullets[-1].rot = rotation
        btime -= 1
    else:
        btime = 0
    pobj.update()
    tparticles = particles
    for i, particle in enumerate(tparticles):
        particle.acc -= particle.vel / 2
        particle.size = (1 - particle.alive) * 10
        if particle.alive >= 1:
            particles.pop(i)
            del particle
            continue
        particle.update()
        gfxdraw.filled_polygon(screen, ((particle.size/2, 0), (0, particle.size), (-particle.size/2, 0)) + particle.pos + (width/2, height/2), (200,200,200,200))
        gfxdraw.aapolygon(screen, ((particle.size/2, 0), (0, particle.size), (-particle.size/2, 0)) + particle.pos + (width/2, height/2), (100,100,100, 100))


    tbullets = bullets
    for i, bullet in enumerate(tbullets):
        if abs(bullet.pos[0]) >= width/2 or abs(bullet.pos[1]) >= height/2:
            bullets.pop(i)
            del bullet
            continue
        bullet.update()
        form = [rot((1,6), bullet.rot), rot((-1,6), bullet.rot), rot((-1,-6), bullet.rot), rot((1,-6), bullet.rot)]
        gfxdraw.filled_polygon(screen, form + bullet.pos + (width/2, height/2), (255, 0, 0))
        gfxdraw.aapolygon(screen, form + bullet.pos + (width/2, height/2), (255, 0, 0))

    bhrot += 0.5
    rotatedBH = []
    for point in blackHoleFigure:
        rotatedBH.append(rot(point, bhrot))
    gfxdraw.aapolygon(screen, rotatedShip + pobj.pos + (width/2, height/2), (0, 255, 0))
    gfxdraw.aapolygon(screen, np.array(rotatedBH)*10 + (width/2, height/2), (0, 255, 0))
    #if ship.colliderect(blackHole):
    #    while 1:
    #        screen.fill((255,255,255))
    #        clock.tick(60)
    #        screen.fill((0,0,0))
    #        clock.tick(60)

    pg.display.flip()

    clock.tick(60)