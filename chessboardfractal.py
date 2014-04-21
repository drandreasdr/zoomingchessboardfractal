#from __future__ import division
import pygame
import math, random

class ChessBoard:
    POLARITY_TOP_LEFT_WHITE = 0
    POLARITY_TOP_LEFT_BLACK = 1
    def __init__(self, nCells, polarity):
        self.nCells = nCells
        self.polarity = polarity

    def draw(self, displaysurf):
        for i in range(0, self.nCells*self.nCells):
            col = i % self.nCells
            row = i // self.nCells
            if (col + row + self.polarity) % 2 == 0:
                color = (255,255,255)
            else:
                color = (0,0,0)
            #Draw rectangle between (x+col*cellSize, y+row*cellSize) and (x+col*cellSize+cellSize, y+row*cellSize+cellSize):
            #pygame.draw.rect(displaysurf, color, pygame.Rect(self.x + col*self.cellSize, self.y + row*self.cellSize, self.cellSize, self.cellSize))
            x1 = round(self.x + col*self.cellSize)
            y1 = round(self.y + row*self.cellSize)
            x2 = round(self.x + col*self.cellSize + self.cellSize)
            y2 = round(self.y + row*self.cellSize + self.cellSize)
            pygame.draw.rect(displaysurf, color, pygame.Rect(x1, y1, x2-x1, y2-y1))

class ChessBoardFractal:
    def __init__(self, nBoards, x, y, size, nCells, polarity, zoomDoublingTime):
        self.nBoards = nBoards
        self.x = x
        self.y = y
        self.size = size
        self.nCells = nCells
        self.polarity = polarity
        self.zoomDoublingTime = zoomDoublingTime
        self.generationTime = math.log(nCells)*zoomDoublingTime/math.log(2)
        self.chessBoards = [0]*nBoards
        self.subBoardIndices = [0]*nBoards
        #self.APA = 7 + 6*7 #XXX
        #self.APA = 2
        for i in range(0, nBoards):
            self.chessBoards[i] = ChessBoard(nCells, polarity)
            self.subBoardIndices[i] = random.randrange(0, nCells*nCells)
            #self.subBoardIndices[i] = self.APA #XXX

        #Initializations:
        self.elapsedTime = 0
        #Initialize first chess board:
        self.chessBoards[0].x = x
        self.chessBoards[0].y = y
        self.chessBoards[0].cellSize = size/nCells

        #Update all others:
        self.updateChessBoards()

    def tick(self, dt):
        self.elapsedTime += dt
        if self.elapsedTime > self.generationTime:
            self.elapsedTime -= self.generationTime
            self.shiftGenerations()
            #Don't need to updateChessBoards here since it is only the top two boards that are manipulated before the next update.
            #
        #Update largest chessboard:
        cellSize0Initial = self.size/self.nCells
        cellSize0 = cellSize0Initial*math.pow(2, self.elapsedTime/self.zoomDoublingTime)
        row1 = self.subBoardIndices[0] // self.nCells #row of board 1 in board 0
        col1 = self.subBoardIndices[0] % self.nCells #column -||-
        x1Initial = col1*cellSize0Initial #note, absolute coordinate
        y1Initial = row1*cellSize0Initial
        #double x1 = (1 - elapsedTime/generationTime)*x1Initial;
		#double y1 = (1 - elapsedTime/generationTime)*y1Initial;
        x1 = 1.*x1Initial/(self.size - cellSize0Initial)*(self.size - cellSize0)
        y1 = 1.*y1Initial/(self.size - cellSize0Initial)*(self.size - cellSize0)
        x0 = x1 - col1*cellSize0
        y0 = y1 - row1*cellSize0
        self.chessBoards[0].cellSize = cellSize0
        self.chessBoards[0].x = x0
        self.chessBoards[0].y = y0

        #Update all other chessboards:
        self.updateChessBoards()

    def draw(self, displaysurf):
        for chessBoard in self.chessBoards:
            chessBoard.draw(displaysurf)

    #Note: doesn't update chess boards
    def shiftGenerations(self):
        #Shift all chess boards one step up, replacing the largest one:
        for i in range(0, self.nBoards - 1):
            self.chessBoards[i] = self.chessBoards[i+1]
            self.subBoardIndices[i] = self.subBoardIndices[i+1]
        #Set new smallest chess board:
        self.chessBoards[self.nBoards-1] = ChessBoard(self.nCells, self.polarity)
        self.subBoardIndices[self.nBoards-1] = random.randrange(0, self.nCells*self.nCells)
        #self.subBoardIndices[self.nBoards-1] = self.APA #XXX

    #Recomputes positions and sizes of chess boards 1 -- n-1 based on the largest one?
    def updateChessBoards(self):
        xi = self.chessBoards[0].x
        yi = self.chessBoards[0].y
        cellSizei = self.chessBoards[0].cellSize
        for i in range(1, self.nBoards):
            col = self.subBoardIndices[i-1] % self.nCells
            row = self.subBoardIndices[i-1] // self.nCells
            xi += col*cellSizei
            yi += row*cellSizei
            cellSizei /= self.nCells
            #Update ChessBoard i:
            self.chessBoards[i].x = xi
            self.chessBoards[i].y = yi
            self.chessBoards[i].cellSize = cellSizei