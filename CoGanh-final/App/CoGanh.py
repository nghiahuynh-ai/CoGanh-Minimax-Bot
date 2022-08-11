from settings import *
from Agent import *


class CoGanh:
    def __init__(self):
        self.initBoard = [[0 for j in range(0, 5)] for i in range(0, 5)]
        for i in range(0, 5):
            self.initBoard[0][i] = -1
            self.initBoard[4][i] = 1
        self.initBoard[1][0] = self.initBoard[1][4] = self.initBoard[2][4] = -1
        self.initBoard[2][0] = self.initBoard[3][0] = self.initBoard[3][4] = 1
        self.board = copy(self.initBoard)
        self.preBoard = copy(self.initBoard)
        self.numOfTurn = 0

    def resetGame(self):
        self.board = copy(self.initBoard)
        self.preBoard = copy(self.preBoard)
        self.numOfTurn = 0

    def play(self, firstTurn, player1, player2):
        listBoard = [copy(self.board)]
        player = firstTurn
        while not isWin(self.board):
            self.numOfTurn += 1
            if player == 1:
                m = player1.selectMove(self.board, self.preBoard)
                if m.start.x * m.start.y * m.end.x * m.end.y != 1:
                    self.preBoard = copy(self.board)
                    makeMove(self.board, m, player1.playerId)
                else:
                    break
            else:
                m = player2.selectMove(self.board, self.preBoard)
                if m.start.x * m.start.y * m.end.x * m.end.y != 1:
                    self.preBoard = copy(self.board)
                    makeMove(self.board, m, player2.playerId)
                else:
                    break
            listBoard = listBoard + [copy(self.board)]
            player *= -1
        self.resetGame()
        return listBoard

    def playOne(self, player1, curBoard, preBoard):
        m = player1.selectMove(curBoard, preBoard)
        if m.start.x * m.start.y * m.end.x * m.end.y != 1:
            preBoard = copy(curBoard)
            makeMove(curBoard, m, player1.playerId)
        if isWin(curBoard):
            return True, copy(preBoard), copy(curBoard)
        else:
            return False, copy(preBoard), copy(curBoard)
