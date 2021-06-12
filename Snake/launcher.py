from game import game
from graphics import graphics
from asyncio import *

Game = game(10, 10, exit) # width, height, function to call on lose
Graphics = graphics(Game)

async def main():
    speed = 50 # initial game speed. lower is faster
    i = 0
    while 1:
        i += 1
        await sleep(0.01)
        await Graphics.mainloop()
        if i >= speed:
            i = 0
            await Graphics.gameloop()
        speed /= 1.0001 # comment out this line to make speed constant

run(main())
