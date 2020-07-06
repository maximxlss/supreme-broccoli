import random as rand
from checkBoard import checkBoard, winCombinations
import re


class game:
    def __init__(self, colors=(100, 47, 32)):
        self.colors = colors
        self.board = [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]]
        self.turn = 1
        self.win = winCombinations

    def render(self):
        screen = [[" ", " ", " "],
                  [" ", " ", " "],
                  [" ", " ", " "]]
        for y, row in zip(self.board, range(3)):
            for x, col in zip(y, range(3)):
                if x != 0:
                    screen[row][col] = "x" if x == 1 else "o"

        print(
            f"\033[{self.colors[0]}m\033[{self.colors[2]}m {screen[0][0]} \033[{self.colors[1]}m\033[{self.colors[2]}m {screen[0][1]} \033[{self.colors[0]}m\033[{self.colors[2]}m {screen[0][2]} \033[0m")
        print(
            f"\033[{self.colors[1]}m\033[{self.colors[2]}m {screen[1][0]} \033[{self.colors[0]}m\033[{self.colors[2]}m {screen[1][1]} \033[{self.colors[1]}m\033[{self.colors[2]}m {screen[1][2]} \033[0m")
        print(
            f"\033[{self.colors[0]}m\033[{self.colors[2]}m {screen[2][0]} \033[{self.colors[1]}m\033[{self.colors[2]}m {screen[2][1]} \033[{self.colors[0]}m\033[{self.colors[2]}m {screen[2][2]} \033[0m")
        print("---------")

    def move(self, turn, x, y):
        self.board[y][x] = turn
        self.turn = 2 if turn == 1 else 1

    def tutorial(self):
        print("Hello! This is a simple tic-tac-toe game.\n"
              "To make a move, input two numbers: x and y\n"
              "this is '11' |\n"
              "            \/\n"
              "             x|o|x\n"
              "             o|x|x <- this is '32'\n"
              "             o|x|o\n"
              "               /\\\n"
              "                | this is '23'\n")

    def readMove(self):
        spot = input("You are " + ("x" if self.turn == 1 else "o") + ". Make a move: ")
        spot = re.sub("[^\d]", '', spot)
        if len(spot) != 2 or int(spot[0]) > 3 or int(spot[0]) < 1 or int(spot[1]) > 3 or int(spot[1]) < 1:
            print("Oof! Out of range!")
            self.readMove()
            return
        if self.board[int(spot[1]) - 1][int(spot[0]) - 1] != 0:
            print("Alredy moved there!")
            self.readMove()
            return
        self.move(self.turn, int(spot[0]) - 1, int(spot[1]) - 1)

    def randMove(self):
        x = rand.randint(0, 2)
        y = rand.randint(0, 2)
        while self.board[y][x] != 0:
            x = rand.randint(0, 2)
            y = rand.randint(0, 2)
        self.move(self.turn, x, y)

    def reset(self):
        self.board = [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]]
        self.turn = 1

    def checkBoard(self):
        return checkBoard(self)
