from tkinter import *
from colorsys import hsv_to_rgb

class graphics():
    def __init__(self, game): # game.height/width are much different than graphics.height/width
        self.game = game      # game.height/width - grid size, while graphics.height/width is window size
        self.field = [[0] * (game.width + 1) for i in range(game.height + 1)]
        self.renderField = [[0] * (game.width + 1) for i in range(game.height + 1)]
        self.cellWidth = 100 if game.width < 6 else (600 // game.width)
        self.width = game.width * self.cellWidth
        self.cellHeight = 100 if game.height < 6 else (600 // game.height)
        self.height = game.height * self.cellHeight
        self.tk = Tk()
        self.tk.geometry(f"{self.width}x{self.height}")
        self.canvas = Canvas(width=self.width, height=self.height, bg="gray10")
        self.canvas.pack()
        self.color = 0
        self.tk.bind('<Up>', lambda e: self._ao([0,-1]))
        self.tk.bind('<Down>', lambda e: self._ao([0, 1]))
        self.tk.bind('<Left>', lambda e: self._ao([-1,0]))
        self.tk.bind('<Right>', lambda e: self._ao([1, 0]))

    def _ao(self, value):
        """Assign Orient"""
        self.game.orient = value

    def fillField(self):
        self.field = [[0] * (self.game.width + 1) for i in range(self.game.height + 1)]
        for cell in self.game.snake:
            self.field[cell[1]][cell[0]] = 1
        self.field[self.game.apple[1]][self.game.apple[0]] = 2

    async def gameloop(self):
        self.game.move()
        self.color = "green2" if self.color == "green3" else "green3"
        await self.update()

    async def update(self):
        queueNeeds = []
        queueTrash = []
        self.fillField()

        for yi, y in enumerate(self.field):
            for xi, x in enumerate(y):
                try:
                    if self.renderField[yi][xi] == 0 and x == 1:
                        queueNeeds.append((xi, yi, False))
                    elif self.renderField[yi][xi] == 0 and x == 2:
                        queueNeeds.append((xi, yi, True))
                    elif self.renderField[yi][xi][0] != 0 and x == 0:
                        queueTrash.append((xi, yi))
                except TypeError:
                    pass
                try:
                    if self.renderField[yi][xi][1] and self.field[yi][xi] != 2:
                        queueTrash.append((xi, yi))
                        queueNeeds.append((xi, yi, False))
                except TypeError:
                    pass
        for trash in queueTrash:
            self.canvas.delete(self.renderField[trash[1]][trash[0]][0])
            self.renderField[trash[1]][trash[0]] = 0
        for need in queueNeeds:
            self.renderField[need[1]][need[0]] = [self.canvas.create_rectangle \
                (need[0] * self.cellWidth, need[1] * self.cellHeight,
                (need[0] + 1) * self.cellWidth, (need[1] + 1) * self.cellHeight, fill=self.color if not need[2] else 'red'),
                need[2]]
        pass
    
    async def mainloop(self):
        self.tk.update_idletasks()
        self.tk.update()
