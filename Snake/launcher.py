from game import game
from graphics import graphics
from asyncio import *

Game = game(10, 10, exit)
Graphics = graphics(Game)

async def main():
    speed, i = 100, 0
    while 1:
        i += 1
        await sleep(0.01)
        await Graphics.mainloop()
        if i >= speed:
            i = 0
            await Graphics.gameloop()
        speed /= 1.0001
        
run(main())
