from random import *
from pynput import keyboard
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

e = 0

grid = [[0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]]

x = randint(0, len(grid[0]) - 1)
y = randint(0, len(grid) - 1)

tile = choice([2, 4])

grid[y][x] = tile

for y in grid:
    for x in y:
        if x == 0:
            x = ' ≡ '
        else:
            x = ' ' + str(x) + ' '
        print(x, end='')
    print('')
print('__________________')

def move(d):
    global grid
    global e

    rgrid = []
    if d == 'u' or d == 'd':
        for i in range(6):
            rgrid.append([a[i] for a in grid])
        if d == 'r' or d == 'u':
            for l in rgrid:
                l.reverse()
    else: rgrid = grid

    for l in rgrid:
        if d == 'r' or d == 'u': l.reverse()
        while 1:
            try:
                l.remove(0)
            except ValueError:
                break
        if len(l) > 1:
            for i in range(len(l)-1):
                if l[i] == l[i+1]:
                    l[i+1] = l[i]*2
                    del l[i]
                    break

        while len(l) < 6:
            l.append(0)
        if d == 'r' or d == 'u': l.reverse()

    if d == 'u' or d == 'd':
        for l in rgrid:
            l.reverse()
        grid = [[0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0]]
        for y in range(6):
            for x in range(6):
                grid[x][y] = rgrid[y][x]

    x = randint(0, len(grid[0]) - 1)
    y = randint(0, len(grid) - 1)

    while grid[y][x] != 0:
        x = randint(0, len(grid[0]) - 1)
        y = randint(0, len(grid) - 1)

    tile = choice([2, 4])

    grid[y][x] = tile

    full = 0

    for y in grid:
        if 0 in y:
            break
        full += 1

    if full >= 6:
        print('Game Over!')
        input()
    cls()
    for y in grid:
        for x in y:
            if x == 0: x = ' ≡ '
            else: x = ' '+str(x)+' '
            print(x, end='')
        print('')
    print('__________________')

    return grid

def on_press(key):
    if key == keyboard.Key.up: grid = move("u")
    if key == keyboard.Key.down: grid = move("d")
    if key == keyboard.Key.left: grid = move("l")
    if key == keyboard.Key.right: grid = move("r")

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()