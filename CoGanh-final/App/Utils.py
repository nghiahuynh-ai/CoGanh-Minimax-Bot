class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Move:
    def __init__(self, start, end):
        self.start = start
        self.end = end


def copy(board):
    return [[board[i][j] for j in range(0, 5)] for i in range(0, 5)]


def label(value):
    _label = 'O'
    if value == -1:
        _label = 'X'
    elif value == 0:
        _label = '-'
    return _label


def printBoard(board):
    for i in range(0, 5):
        print(label(board[i][0]), label(board[i][1]), label(board[i][2]), label(board[i][3]), label(board[i][4]))


def getNeighbors(board, position, playerId):
    neighbors = []
    x = position.x
    y = position.y
    if x > 0:
        if board[x - 1][y] == playerId:
            neighbors.append(Position(x - 1, y))
    if x < 4:
        if board[x + 1][y] == playerId:
            neighbors.append(Position(x + 1, y))
    if y > 0:
        if board[x][y - 1] == playerId:
            neighbors.append(Position(x, y - 1))
    if y < 4:
        if board[x][y + 1] == playerId:
            neighbors.append(Position(x, y + 1))
    if (x + y) % 2 == 0:
        if (x > 0) & (y > 0):
            if board[x - 1][y - 1] == playerId:
                neighbors.append(Position(x - 1, y - 1))
        if (x < 4) & (y > 0):
            if board[x + 1][y - 1] == playerId:
                neighbors.append(Position(x + 1, y - 1))
        if (x < 4) & (y < 4):
            if board[x + 1][y + 1] == playerId:
                neighbors.append(Position(x + 1, y + 1))
        if (x > 0) & (y < 4):
            if board[x - 1][y + 1] == playerId:
                neighbors.append(Position(x - 1, y + 1))
    return neighbors


def canMoveTo(board, position, playerId):
    validPositions = []
    x = position.x
    y = position.y
    if board[x][y] == playerId:
        if x > 0:
            if board[x - 1][y] == 0:
                validPositions.append(Position(x - 1, y))
        if x < 4:
            if board[x + 1][y] == 0:
                validPositions.append(Position(x + 1, y))
        if y > 0:
            if board[x][y - 1] == 0:
                validPositions.append(Position(x, y - 1))
        if y < 4:
            if board[x][y + 1] == 0:
                validPositions.append(Position(x, y + 1))
        if (x + y) % 2 == 0:
            if (x > 0) & (y > 0):
                if board[x - 1][y - 1] == 0:
                    validPositions.append(Position(x - 1, y - 1))
            if (x < 4) & (y > 0):
                if board[x + 1][y - 1] == 0:
                    validPositions.append(Position(x + 1, y - 1))
            if (x < 4) & (y < 4):
                if board[x + 1][y + 1] == 0:
                    validPositions.append(Position(x + 1, y + 1))
            if (x > 0) & (y < 4):
                if board[x - 1][y + 1] == 0:
                    validPositions.append(Position(x - 1, y + 1))
    return validPositions


def isErrorMove(board, move):
    cond1 = (move.start.x == move.end.x) & (move.start.y == move.end.y)
    cond2 = (board[move.end.x][move.end.y] == 1) | (board[move.end.x][move.end.y] == -1)
    cond3 = (move.end.x > move.start.x + 1) | (move.end.y > move.start.y + 1)
    cond4 = (move.start.x < 0) | (move.start.x > 4) | (move.start.y < 0) | (move.start.y > 4) | \
            (move.end.x < 0) | (move.end.y > 4) | (move.end.x < 0) | (move.end.y > 4)
    return cond1 | cond2 | cond3 | cond4


def isFree(board, playerId):
    for i in range(0, 5):
        for j in range(0, 5):
            if len(canMoveTo(board, Position(i, j), playerId)) > 0:
                return True
    return False


def ganh(board, move, playerId):
    ganhPositions = []
    if isErrorMove(board, move):
        return ganhPositions
    x = move.end.x
    y = move.end.y
    if (x > 0) & (x < 4):
        if (board[x + 1][y] == -playerId) & (board[x - 1][y] == -playerId):
            ganhPositions.append(Position(x + 1, y))
            ganhPositions.append(Position(x - 1, y))
    if (y > 0) & (y < 4):
        if (board[x][y + 1] == -playerId) & (board[x][y - 1] == -playerId):
            ganhPositions.append(Position(x, y + 1))
            ganhPositions.append(Position(x, y - 1))
    if ((x == 1) & (y == 1)) | ((x == 1) & (y == 3)) | ((x == 2) & (y == 2)) | ((x == 3) & (y == 1)) | (
            (x == 3) & (y == 3)):
        if (board[x - 1][y - 1] == -playerId) & (board[x + 1][y + 1] == -playerId):
            ganhPositions.append(Position(x - 1, y - 1))
            ganhPositions.append(Position(x + 1, y + 1))
        if (board[x + 1][y - 1] == -playerId) & (board[x - 1][y + 1] == -playerId):
            ganhPositions.append(Position(x + 1, y - 1))
            ganhPositions.append(Position(x - 1, y + 1))
    return ganhPositions


def vay(board, move, playerId):
    vayPositions = []
    if isErrorMove(board, move):
        return vayPositions
    clone = copy(board)
    clone[move.start.x][move.start.y] = 0
    clone[move.end.x][move.end.y] = playerId
    flag = True
    while flag:
        count = 0
        for i in range(0, 5):
            isChanged = False
            for j in range(0, 5):
                if (clone[i][j] == -playerId) & (len(canMoveTo(clone, Position(i, j), -playerId)) > 0):
                    clone[i][j] = 0
                    isChanged = True
                    break
                count += 1
            if isChanged:
                break
        if count == 25:
            flag = False
    for i in range(0, 5):
        for j in range(0, 5):
            if clone[i][j] == -playerId:
                vayPositions.append(Position(i, j))
    return vayPositions


def bay(curBoard, preBoard, playerId):
    moveList = []
    prePlayer = preOpp = curPlayer = curOpp = 0
    for i in range(0, 5):
        for j in range(0, 5):
            if preBoard[i][j] == playerId:
                prePlayer += 1
            if preBoard[i][j] == -playerId:
                preOpp += 1
            if curBoard[i][j] == playerId:
                curPlayer += 1
            if curBoard[i][j] == -playerId:
                curOpp += 1
    target = Position(-1, -1)
    for i in range(0, 5):
        isChanged = False
        for j in range(0, 5):
            if (preBoard[i][j] == -playerId) & (curBoard[i][j] == 0):
                target = Position(i, j)
                isChanged = True
                break
        if isChanged:
            break
    if (prePlayer == curPlayer) & (preOpp == curOpp):
        oppNextToPositions = getNeighbors(curBoard, target, playerId)
        if len(oppNextToPositions) == 0:
            return moveList
        else:
            for oppPosition in oppNextToPositions:
                if len(ganh(curBoard, Move(oppPosition, target), playerId)) > 0:
                    moveList.append(Move(oppPosition, target))
    return moveList


def getValidMoves(curBoard, preBoard, playerId):
    validMoves = []
    bayMoves = bay(curBoard, preBoard, playerId)
    if len(bayMoves) != 0:
        validMoves = bayMoves
    else:
        for i in range(0, 5):
            for j in range(0, 5):
                if curBoard[i][j] == playerId:
                    for position in canMoveTo(curBoard, Position(i, j), playerId):
                        validMoves.append(Move(Position(i, j), position))
    return validMoves


def getValidMoves2(curBoard, preBoard, playerId, currPos):
    validMoves = []
    bayMoves = bay(curBoard, preBoard, playerId)
    if len(bayMoves) != 0:
        for position in canMoveTo(curBoard, Position(currPos[0], currPos[1]), playerId):
            if position.x == bayMoves[0].end.x and position.y == bayMoves[0].end.y:
                return bayMoves
        return []
    for position in canMoveTo(curBoard, Position(currPos[0], currPos[1]), playerId):
        validMoves.append(Move(Position(currPos[0], currPos[1]), position))
    return validMoves


def makeMove(board, move, playerId):
    if isErrorMove(board, move):
        print('Error move!')
    else:
        ganhPositions = ganh(board, move, playerId)
        if len(ganhPositions) > 0:
            for pos in ganhPositions:
                board[pos.x][pos.y] = playerId
        vayPositions = vay(board, move, playerId)
        if len(vayPositions) > 0:
            for pos in vayPositions:
                board[pos.x][pos.y] = playerId
        board[move.start.x][move.start.y] = 0
        board[move.end.x][move.end.y] = playerId


def makeMove2(board, move, playerId):
    if isErrorMove(board, move):
        print('Error move!')
    else:
        ganhPositions = ganh(board, move, playerId)
        if len(ganhPositions) > 0:
            for pos in ganhPositions:
                board[pos.x][pos.y] = playerId
        vayPositions = vay(board, move, playerId)
        if len(vayPositions) > 0:
            for pos in vayPositions:
                board[pos.x][pos.y] = playerId
        board[move.start.x][move.start.y] = 0
        board[move.end.x][move.end.y] = playerId
    return board


def isNewGame(curBoard, preBoard):
    for i in range(0, 5):
        for j in range(0, 5):
            if curBoard[i][j] != preBoard[i][j]:
                return False
    return True


def evaluate(board, playerId):
    score = 0
    for i in range(0, 5):
        for j in range(0, 5):
            if board[i][j] == playerId:
                score += 1
    return score


def isWin(board):
    count = sum(sum(board[i]) for i in range(0, 5))
    if abs(count) == 16:
        return True
    else:
        return False
