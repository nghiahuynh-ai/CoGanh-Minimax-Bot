import pygame
import os
from settings import *
import numpy as np
from CoGanh import *
import random

assets_path = os.getcwd() + "\\..\\Assets"
os.chdir(assets_path)
leftArrow = pygame.image.load(os.getcwd() + '\\leftArrow.png')
leftArrow = pygame.transform.scale(leftArrow, (25, 25))
rightArrow = pygame.image.load(os.getcwd() + '\\rightArrow.png')
rightArrow = pygame.transform.scale(rightArrow, (25, 25))
upArrow = pygame.image.load(os.getcwd() + '\\upArrow.png')
upArrow = pygame.transform.scale(upArrow, (15, 15))
downArrow = pygame.image.load(os.getcwd() + '\\downArrow.png')
downArrow = pygame.transform.scale(downArrow, (15, 15))
background = pygame.image.load(os.getcwd() + '\\background.jpg')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

agent1 = Agent(level=HARD, playerId=1)
agent2 = Agent(level=MEDIUM, playerId=1)
agent3 = Agent(level=NORMAL, playerId=1)
agent4 = Agent(level=EASY, playerId=-1)


class Entry:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Co Ganh')
        self.running = True
        self.state = "init"
        self.listAlgorithm = ["Agent(EASY) VS Agent", "You VS Agent"]
        self.listAgentLevel = ["NORMAL", "MEDIUM", "HARD"]
        self.algorithmIdx = 0
        self.levelIdx = 0
        self.solution = self.initBoard()
        self.solIdx = 0
        self.board = self.initBoard()
        self.game = CoGanh()
        self.playerChoose = []
        self.playerChooseNext = []
        self.playerChoosingState = 0
        self.posNextMove = []
        self.firstTurn = 0
        self.nowTurn = 0
        self.numOfTurn = 0
        self.preBoard = copy(self.solution)

    def run(self):
        while self.running:
            # self.window.blit(background,(0,0))
            if self.state != "waiting":
                self.window.blit(background, (0, 0))
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONUP and self.state == "human":

                    if self.playerChoosingState == 0 or self.playerChoosingState == 1:
                        # print("check")
                        cellSize = BOARD_SIZE / 4
                        mpos = pygame.mouse.get_pos()
                        for i in range(5):
                            check = False
                            for j in range(5):
                                if self.solution[i][j] == -1:
                                    if self.checkInside(mpos, gridSoluPos[0] + cellSize * j,
                                                        gridSoluPos[1] + cellSize * i, 15):
                                        self.playerChoose = [i, j]
                                        validMoves = getValidMoves2(self.solution, self.preBoard, -1, self.playerChoose)
                                        self.posNextMove = []
                                        check = True
                                        # print(len(validMoves))
                                        for move in validMoves:
                                            self.posNextMove.append([move.end.x, move.end.y])
                                        break
                            if check is True:
                                self.playerChoosingState = 1
                                break
                    if self.playerChoosingState == 0 or self.playerChoosingState == 1:
                        # print("check1")
                        cellSize = BOARD_SIZE / 4
                        mpos = pygame.mouse.get_pos()
                        check = False
                        for pos in self.posNextMove:
                            if self.checkInside(mpos, gridSoluPos[0] + cellSize * pos[1],
                                                gridSoluPos[1] + cellSize * pos[0], 15):
                                # print(pos[0], pos[1])
                                check = True
                                move = Move(Position(self.playerChoose[0], self.playerChoose[1]),
                                            Position(pos[0], pos[1]))
                                break
                        if check == True:
                            self.preBoard = copy(self.solution)
                            self.solution = makeMove2(self.solution, move, -1)
                            self.playerChoosingState = 2
                            self.playerChoose = []
                            self.posNextMove = []
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT and self.state == "init":
                        if self.levelIdx < len(self.listAgentLevel) - 1:
                            self.levelIdx += 1
                        else:
                            self.levelIdx = 0
                    if event.key == pygame.K_LEFT and self.state == "init":
                        if self.levelIdx > 0:
                            self.levelIdx -= 1
                        else:
                            self.levelIdx = len(self.listAgentLevel) - 1
                    if event.key == pygame.K_UP and self.state == "init":
                        if self.algorithmIdx > 0:
                            self.algorithmIdx -= 1
                        else:
                            self.algorithmIdx = len(self.listAlgorithm) - 1
                    if event.key == pygame.K_DOWN and self.state == "init":
                        if self.algorithmIdx < len(self.listAlgorithm) - 1:
                            self.algorithmIdx += 1
                        else:
                            self.algorithmIdx = 0
                    if event.key == pygame.K_RETURN:
                        if self.state == "init":
                            self.firstTurn = random.choice([-1, 1])
                            self.nowTurn = self.firstTurn
                            if self.algorithmIdx == 0:
                                self.state = "execute"
                            else:
                                if self.firstTurn == -1:
                                    self.state = "human"
                                else:
                                    self.state = "bot"
                        if self.state == "done":
                            self.solIdx = 0
                            self.firstTurn = 0
                            self.nowTurn = 0
                            self.numOfTurn = 0
                            self.solution = self.initBoard()
                            self.board = self.initBoard()
                            self.preBoard = copy(self.solution)
                            self.state = "init"
            if self.state == "init":
                self.startScreen()
            if self.state == "execute":
                self.executeScreen()
                pygame.display.update()
                self.state = "waiting"
            if self.state == "waiting":
                if self.algorithmIdx == 0:
                    if self.levelIdx == 0:
                        secondAgent = agent3
                    elif self.levelIdx == 1:
                        secondAgent = agent2
                    else:
                        secondAgent = agent1
                    # print(self.firstTurn)
                    # print(secondAgent.depth)
                    self.solution = self.game.play(firstTurn=self.firstTurn, player1=secondAgent, player2=agent4)
                    self.numOfTurn = len(self.solution) - 1
                    if self.numOfTurn % 2 == 1:
                        self.nowTurn = -1 if self.firstTurn == -1 else 1
                    else:
                        self.nowTurn = 1 if self.firstTurn == -1 else -1
                    # print(self.solution)
                self.state = "playing"
            if self.state == "playing":
                self.playingScreen()
                self.solIdx = self.solIdx + 1
                self.clock.tick(4)
                if self.solIdx == len(self.solution) - 1:
                    self.state = "done"
            if self.state == "bot":
                if self.levelIdx == 0:
                    secondAgent = agent3
                elif self.levelIdx == 1:
                    secondAgent = agent2
                else:
                    secondAgent = agent1
                # print(self.solution)
                check, self.preBoard, self.solution = self.game.playOne(player1=secondAgent, curBoard=self.solution,
                                                                        preBoard=self.preBoard)
                # print(self.solution)
                if check is False:
                    # print(self.nowTurn)
                    self.stageScreen()
                    self.numOfTurn = self.numOfTurn + 1
                    self.nowTurn = -1
                    self.state = "human"
                    self.clock.tick(1)
                else:
                    self.state = "done"
            if self.state == "human":
                # print(self.solution)
                self.stageScreen()
                if self.playerChoosingState == 2:
                    if isWin(self.solution):
                        self.state = "done"
                    else:
                        self.playerChoosingState = 0
                        self.numOfTurn = self.numOfTurn + 1
                        self.nowTurn = 1
                        self.state = "bot"
            if self.state == "done":
                self.solutionScreen()
            pygame.display.update()
        pygame.quit()

    def checkInside(self, mpos, x, y, rad):
        # print(mpos, x, y)
        if pow(mpos[0] - x, 2) + pow(mpos[1] - y, 2) < pow(rad, 2):
            return True
        return False

    def initBoard(self):
        board = [[0 for j in range(0, 5)] for i in range(0, 5)]
        for i in range(0, 5):
            board[0][i] = -1
            board[4][i] = 1
        board[1][0] = board[1][4] = board[2][4] = -1
        board[2][0] = board[3][0] = board[3][4] = 1
        return board

    def draw_board(self, map, size, pos):
        mapSize = 4
        cellSize = size / mapSize
        pygame.draw.rect(self.window, BLACK, (pos[0], pos[1], cellSize * mapSize, cellSize * mapSize), 2)
        for x in range(mapSize):
            pygame.draw.line(self.window, BLACK, (pos[0] + (x * cellSize), pos[1]),
                             (pos[0] + (x * cellSize), pos[1] + size), 2)
            pygame.draw.line(self.window, BLACK, (pos[0], pos[1] + (x * cellSize)),
                             (pos[0] + size, pos[1] + +(x * cellSize)), 2)
        pygame.draw.line(self.window, BLACK, (pos[0], pos[1]), (pos[0] + size, pos[1] + size), 1)
        pygame.draw.line(self.window, BLACK, (pos[0], pos[1] + cellSize * mapSize),
                         (pos[0] + + cellSize * mapSize, pos[1]), 1)
        pygame.draw.line(self.window, BLACK, (pos[0], pos[1] + cellSize * mapSize / 2),
                         (pos[0] + cellSize * mapSize / 2, pos[1]), 1)
        pygame.draw.line(self.window, BLACK, (pos[0], pos[1] + cellSize * mapSize / 2),
                         (pos[0] + cellSize * mapSize / 2, pos[1] + cellSize * mapSize), 1)
        pygame.draw.line(self.window, BLACK, (pos[0] + cellSize * mapSize, pos[1] + cellSize * mapSize / 2),
                         (pos[0] + cellSize * mapSize / 2, pos[1]), 1)
        pygame.draw.line(self.window, BLACK, (pos[0] + cellSize * mapSize, pos[1] + cellSize * mapSize / 2),
                         (pos[0] + cellSize * mapSize / 2, pos[1] + cellSize * mapSize), 1)
        for i in range(5):
            for j in range(5):
                if map[i][j] == 1:
                    pygame.draw.circle(self.window, BLUE, (pos[0] + cellSize * j, pos[1] + cellSize * i), 15)
                if map[i][j] == -1:
                    pygame.draw.circle(self.window, RED, (pos[0] + cellSize * j, pos[1] + cellSize * i), 15)
        # pygame.draw.circle(self.window, BLUE, (pos[0], pos[1]), 17)
        # pygame.draw.circle(self.window, RED, (pos[0], pos[1]), 15)
        if len(self.playerChoose) != 0:
            pygame.draw.circle(self.window, BLACK,
                               (pos[0] + self.playerChoose[1] * cellSize, pos[1] + self.playerChoose[0] * cellSize), 18)
            pygame.draw.circle(self.window, RED,
                               (pos[0] + self.playerChoose[1] * cellSize, pos[1] + self.playerChoose[0] * cellSize), 15)

        if len(self.posNextMove) != 0:
            for i in range(len(self.posNextMove)):
                pygame.draw.circle(self.window, BLACK, (
                pos[0] + self.posNextMove[i][1] * cellSize, pos[1] + self.posNextMove[i][0] * cellSize), 15)

    def startScreen(self):
        os.chdir(assets_path)
        titleSize = pygame.font.Font('gameFont.ttf', 60)
        titleText = titleSize.render('Co Ganh', True, BLACK)
        titleRect = titleText.get_rect(center=(300, 50))
        self.window.blit(titleText, titleRect)

        desSize = pygame.font.Font('gameFont.ttf', 20)
        desText = desSize.render('Choose Mode and Agent Level.', True, BLACK)
        desRect = desText.get_rect(center=(300, 115))
        self.window.blit(desText, desRect)
        desText = desSize.render('Then press Enter to start.', True, BLACK)
        desRect = desText.get_rect(center=(300, 140))
        self.window.blit(desText, desRect)

        algorithmSize = pygame.font.Font('gameFont.ttf', 24)
        algorithmDes = algorithmSize.render('Mode', True, BLACK)
        algorithmRect = algorithmDes.get_rect(center=(300, 470))
        self.window.blit(algorithmDes, algorithmRect)

        algorithmSize = pygame.font.Font('gameFont.ttf', 28)
        algorithmText = algorithmSize.render(str(self.listAlgorithm[self.algorithmIdx]), True, BLACK)
        algorithmRect = algorithmText.get_rect(center=(300, 500))
        self.window.blit(algorithmText, algorithmRect)

        self.window.blit(upArrow, (350, 460))
        self.window.blit(downArrow, (350, 470))

        levelSize = pygame.font.Font('gameFont.ttf', 24)
        levelDes = levelSize.render('Agent Level: ' + str(self.listAgentLevel[self.levelIdx]), True, BLACK)
        levelRect = levelDes.get_rect(center=(300, 550))
        self.window.blit(levelDes, levelRect)
        self.window.blit(leftArrow, (120, 540))
        self.window.blit(rightArrow, (450, 540))
        self.draw_board(self.board, BOARD_SELECT_SIZE, gridSelectPos)

    def executeScreen(self):
        os.chdir(assets_path)
        self.window.blit(background, (0, 0))
        titleSize = pygame.font.Font('gameFont.ttf', 60)
        titleText = titleSize.render('Co Ganh', True, BLACK)
        titleRect = titleText.get_rect(center=(300, 50))
        self.window.blit(titleText, titleRect)

        desSize = pygame.font.Font('gameFont.ttf', 20)
        desText = desSize.render('Game is being solved. Please wait.', True, BLACK)
        desRect = desText.get_rect(center=(300, 115))
        self.window.blit(desText, desRect)

        algorithmSize = pygame.font.Font('gameFont.ttf', 24)
        algorithmDes = algorithmSize.render('Mode:', True, BLACK)
        algorithmRect = algorithmDes.get_rect(center=(300, 480))
        self.window.blit(algorithmDes, algorithmRect)

        algorithmSize = pygame.font.Font('gameFont.ttf', 24)
        algorithmText = algorithmSize.render(
            "Agent(EASY)-Red VS Agent(" + str(self.listAgentLevel[self.levelIdx]) + ")-Blue", True, BLACK)
        algorithmRect = algorithmText.get_rect(center=(300, 510))
        self.window.blit(algorithmText, algorithmRect)

        ftSize = pygame.font.Font('gameFont.ttf', 24)
        ftText = ""
        if self.firstTurn == -1:
            if self.algorithmIdx == 0:
                ftText = "Agent(EASY)"
            else:
                ftText = "You"
        else:
            ftText = "Agent(" + str(self.listAgentLevel[self.levelIdx]) + ")"

        ftText = ftSize.render("First Turn: " + ftText, True, BLACK)
        ftRect = ftText.get_rect(center=(300, 550))
        self.window.blit(ftText, ftRect)

        self.draw_board(self.board, BOARD_SELECT_SIZE, gridSelectPos)

    def playingScreen(self):
        os.chdir(assets_path)
        self.window.blit(background, (0, 0))
        titleSize = pygame.font.Font('gameFont.ttf', 60)
        titleText = titleSize.render('Co Ganh', True, BLACK)
        titleRect = titleText.get_rect(center=(300, 50))
        self.window.blit(titleText, titleRect)
        # print(self.solIdx)
        algorithmSize = pygame.font.Font('gameFont.ttf', 24)
        algorithmDes = algorithmSize.render('Mode:', True, BLACK)
        algorithmRect = algorithmDes.get_rect(center=(300, 480))
        self.window.blit(algorithmDes, algorithmRect)

        algorithmSize = pygame.font.Font('gameFont.ttf', 24)
        algorithmText = algorithmSize.render(
            "Agent(EASY)-Red VS Agent(" + str(self.listAgentLevel[self.levelIdx]) + ")-Blue", True, BLACK)
        algorithmRect = algorithmText.get_rect(center=(300, 510))
        self.window.blit(algorithmText, algorithmRect)

        ftSize = pygame.font.Font('gameFont.ttf', 24)
        ftText = ""
        if self.firstTurn == -1:
            if self.algorithmIdx == 0:
                ftText = "Agent(EASY)"
            else:
                ftText = "You"
        else:
            ftText = "Agent(" + str(self.listAgentLevel[self.levelIdx]) + ")"

        ftText = ftSize.render("First Turn: " + ftText, True, BLACK)
        ftRect = ftText.get_rect(center=(300, 550))
        self.window.blit(ftText, ftRect)
        self.draw_board(self.solution[self.solIdx], BOARD_SIZE, gridSoluPos)

    def stageScreen(self):
        os.chdir(assets_path)
        # print(self.nowTurn)

        self.window.blit(background, (0, 0))
        titleSize = pygame.font.Font('gameFont.ttf', 60)
        titleText = titleSize.render('Co Ganh', True, BLACK)
        titleRect = titleText.get_rect(center=(300, 40))
        self.window.blit(titleText, titleRect)
        # print(self.solIdx)
        algorithmSize = pygame.font.Font('gameFont.ttf', 24)
        algorithmDes = algorithmSize.render('Mode:', True, BLACK)
        algorithmRect = algorithmDes.get_rect(center=(300, 480))
        self.window.blit(algorithmDes, algorithmRect)

        algorithmSize = pygame.font.Font('gameFont.ttf', 24)
        algorithmText = algorithmSize.render("You(Red) VS Agent(" + str(self.listAgentLevel[self.levelIdx]) + ")-Blue",
                                             True, BLACK)
        algorithmRect = algorithmText.get_rect(center=(300, 510))
        self.window.blit(algorithmText, algorithmRect)

        ftSize = pygame.font.Font('gameFont.ttf', 24)
        ftText = ""
        if self.firstTurn == -1:
            if self.algorithmIdx == 0:
                ftText = "Agent(EASY)"
            else:
                ftText = "You"
        else:
            ftText = "Agent(" + str(self.listAgentLevel[self.levelIdx]) + ")"

        ftText = ftSize.render("First Turn: " + ftText, True, BLACK)
        ftRect = ftText.get_rect(center=(300, 550))
        self.window.blit(ftText, ftRect)

        desSize = pygame.font.Font('gameFont.ttf', 20)
        desText = desSize.render('Make a move on your turn.', True, BLACK)
        desRect = desText.get_rect(center=(300, 90))
        self.window.blit(desText, desRect)

        self.draw_board(self.solution, BOARD_SIZE, gridSoluPos)

    def solutionScreen(self):
        os.chdir(assets_path)
        self.window.blit(background, (0, 0))
        # titleSize = pygame.font.Font('gameFont.ttf', 60)
        # titleText = titleSize.render('Star Battle', True, BLACK)
        # titleRect = titleText.get_rect(center=(300, 50))
        # self.window.blit(titleText, titleRect)

        algorithmSize = pygame.font.Font('gameFont.ttf', 24)
        algorithmDes = algorithmSize.render('Mode:', True, BLACK)
        algorithmRect = algorithmDes.get_rect(center=(300, 470))
        self.window.blit(algorithmDes, algorithmRect)

        algorithmSize = pygame.font.Font('gameFont.ttf', 24)
        algorithmText = algorithmSize.render(
            "Agent(EASY)-Red" if self.algorithmIdx == 0 else "You(Red)" + " VS Agent(" + str(
                self.listAgentLevel[self.levelIdx]) + ")-Blue", True, BLACK)
        algorithmRect = algorithmText.get_rect(center=(300, 500))
        self.window.blit(algorithmText, algorithmRect)

        ftSize = pygame.font.Font('gameFont.ttf', 24)
        ftText = ""
        if self.firstTurn == -1:
            if self.algorithmIdx == 0:
                ftText = "Agent(EASY)"
            else:
                ftText = "You"
        else:
            ftText = "Agent(" + str(self.listAgentLevel[self.levelIdx]) + ")"

        ftText = ftSize.render("First Turn: " + ftText, True, BLACK)
        ftRect = ftText.get_rect(center=(300, 535))
        self.window.blit(ftText, ftRect)

        resultSize = pygame.font.Font('gameFont.ttf', 28)
        turns = resultSize.render('Num of turns: ' + str(self.numOfTurn), True, BLACK)
        turnsRec = turns.get_rect(center=(300, 90))
        self.window.blit(turns, turnsRec)

        if self.nowTurn == -1:
            wn = "Agent(EASY)" if self.algorithmIdx == 0 else "You"
        else:
            wn = "Agent(" + str(self.listAgentLevel[self.levelIdx]) + ")"

        winner = resultSize.render('Winner: ' + wn, True, BLACK)
        winnerRec = winner.get_rect(center=(300, 40))
        self.window.blit(winner, winnerRec)

        desSize = pygame.font.Font('gameFont.ttf', 20)
        desText = desSize.render('Enter to return.', True, BLACK)
        desRect = desText.get_rect(center=(300, 570))
        self.window.blit(desText, desRect)

        self.draw_board(self.solution[len(self.solution) - 1] if type(self.solution[0][0]) is list else self.solution,
                        BOARD_SIZE, gridSoluPos)
