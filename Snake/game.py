import numpy as np
from random import randint

class game:
    def __init__(self, width, height, gameOver):
        self.width = width
        self.height = height 
        self.gameOver = gameOver

        self.snake = [ [int(self.height / 2) - 1, int(self.width / 2) - 1] ]
        self.orient = [0,-1]

        self.apple = ()
        self.defineApple(first=True)

    def _ao(self, value, *args):
        """Assign Orient"""
        self.orient = value

    def defineApple(self, first=False):
        self.apple = [randint(0, self.width - 1), randint(0, self.height - 1)]
        while self.apple in self.snake:
            self.apple = [randint(0, self.width - 1), randint(0, self.height - 1)]

    def move(self):
        if self.snake[0][0] + self.orient[0] > self.width -1 or self.snake[0][0] + self.orient[0] < 0:
            self.gameOver()
        elif self.snake[0][1] + self.orient[1] > self.height - 1 or self.snake[0][1] + self.orient[1] < 0:
            self.gameOver()
        self.snake.insert(0, [self.snake[0][0] + self.orient[0], self.snake[0][1] + self.orient[1]])
        if self.snake[0] == self.apple:
            self.defineApple()
        else:
            self.snake.pop()
        if self.snake[0] in self.snake[1:]:
            self.gameOver()


