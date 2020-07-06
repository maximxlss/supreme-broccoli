winCombinations = (((0, 0), (1, 0), (2, 0)), ((0, 2), (1, 2), (2, 2)),
                   ((0, 0), (0, 1), (0, 2)), ((2, 0), (2, 1), (2, 2)),
                   ((0, 1), (1, 1), (2, 1)), ((1, 0), (1, 1), (1, 2)),
                   ((0, 0), (1, 1), (2, 2)), ((2, 0), (1, 1), (0, 2)))

def checkBoard(self):
    zeroN = 0
    for comb in winCombinations:
        if self.board[comb[0][0]][comb[0][1]] == 0:
            zeroN += 1
            continue
        else:
            i = self.board[comb[0][0]][comb[0][1]]
        if self.board[comb[1][0]][comb[1][1]] == i:
            if self.board[comb[2][0]][comb[2][1]] == i:
                return True
    if zeroN == 0:
        return "tie"
