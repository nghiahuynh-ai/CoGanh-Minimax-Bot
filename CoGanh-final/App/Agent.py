from Utils import *
import random


class Agent:
    def __init__(self, level, playerId):
        self.depth = level
        self.playerId = playerId

    def minSearch(self, curBoard, preBoard, depth, alpha, beta):
        moves = getValidMoves(curBoard, preBoard, -self.playerId)
        if (depth == 0) | (len(moves) == 0):
            return evaluate(curBoard, self.playerId)
        value = 100
        for m in moves:
            clone = copy(curBoard)
            makeMove(clone, m, -self.playerId)
            value = min(value, self.maxSearch(clone, curBoard, depth - 1, alpha, beta))
            if value <= alpha:
                return value
            beta = min(beta, value)
        # print("min", depth, value)
        return value

    def maxSearch(self, curBoard, preBoard, depth, alpha, beta):
        moves = getValidMoves(curBoard, preBoard, self.playerId)
        if (depth == 0) | (len(moves) == 0):
            return evaluate(curBoard, self.playerId)
        value = -100
        for m in moves:
            clone = copy(curBoard)
            makeMove(clone, m, self.playerId)
            value = max(value, self.minSearch(clone, curBoard, depth - 1, alpha, beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        # print("max", depth, value)
        return value

    def selectMove(self, curBoard, preBoard):
        bestMove = Move(Position(-1, -1), Position(-1, -1))
        moves = getValidMoves(curBoard, preBoard, self.playerId)
        bestMoves = []
        bestValues = []
        if isNewGame(curBoard, preBoard) | (self.depth == 0):
            return random.choice(moves)
        if len(moves) == 0:
            return bestMove
        if len(moves) == 1:
            return moves[0]
        bestSoFar = - 100
        beta = 100
        depth = self.depth
        for m in moves:
            clone = copy(curBoard)
            makeMove(clone, m, self.playerId)
            value = self.minSearch(clone, curBoard, depth - 1, bestSoFar, beta)
            if value >= bestSoFar:
                bestSoFar = value
                bestMoves.append(m)
                bestValues.append(value)
        # for move in bestMoves:
        #     print('(' + str(move.start.x) + ', ' + str(move.start.y) +
        #       ')->(' + str(move.end.x) + ', ' + str(move.end.y) + ')')
        # print(bestValues)
        if len(bestMoves) == 1:
            return bestMoves[0]
        finalBestMoves = []
        for i in range(0, len(bestMoves)):
            if bestValues[i] >= bestSoFar:
                finalBestMoves.append(bestMoves[i])
        bestMove = random.choice(finalBestMoves)
        return bestMove
