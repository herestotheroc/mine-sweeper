
from random import randint
from math import ceil

class square:
    def __init__(self, x, y):
        self.covered = True
        self.flagged = False
        self.bomb = False
        self.x = x
        self.y = y

class grid(square):
    def __init__(self, cols, rows):
        self.grid = []
        self.cols = cols
        self.rows = rows
        self.createGrid()
        self.flags = 0
        self.bombs = 0
        self.populated = False

    def createGrid(self):
            self.grid = [[square(x+1, y+1) for y in range(self.cols)] for x in range(self.rows)]

    def populateGrid(self, b, square):
        if not self.populated:
            tmp = 0
            self.bombs = b
            matr = []
            for i in range(1,4):
                for j in range(1,4):
                    matr.append(self.getSquare(square.x+(i-2),square.y+(j-2)))
            while tmp < b:
                x = randint(0,self.cols)
                y = randint(0,self.rows)
                currentSquare = self.getSquare(x,y)
                if currentSquare and not currentSquare.bomb and currentSquare not in matr:
                    currentSquare.bomb = True
                    tmp += 1
            self.populated = True
            return self.grid

    def getSquare(self, x, y):
        if self.isInGrid(x,y):
            return self.grid[x-1][y-1]
        else:
            return None

    def isInGrid(self, x, y):
        if x<1 or y<1:
            return False
        elif x>self.cols or y>self.rows:
            return False
        else:
            return True

    def getNeighborBombs(self, square):
        bombcount = 0
        for i in range(1,4):
            for j in range(1,4):
                currentSquare = self.getSquare(square.x+(i-2),square.y+(j-2))
                if currentSquare and currentSquare.bomb and currentSquare != square:
                    bombcount += 1
        return bombcount

    def face(self, square):
        if square:
            if square.flagged:
                return -2
            elif square.covered:
                return -3
            elif square.bomb:
                return -1
            else:
                return self.getNeighborBombs(square)
    
    def uncover(self,square):
        #wikipedia/flood fill
        if square:
            if square.covered:
                square.covered = False
                if self.face(square) == 0:
                    self.uncover(square)
                    self.uncover(self.getSquare(square.x,square.y+1))
                    self.uncover(self.getSquare(square.x,square.y-1))
                    self.uncover(self.getSquare(square.x-1,square.y))
                    self.uncover(self.getSquare(square.x+1,square.y))
                elif self.face(square) > 0:
                    square.covered = False
        return

    def flag(self, square):
        if square.covered:
            if not square.flagged:
                    if self.flags < self.bombs:
                        square.flagged = True
                        self.flags += 1
            else:
                square.flagged = False
                self.flags -= 1

    def checkWin(self):
        for i in self.grid:
            for j in i:
                if (j.bomb and not j.flagged) or (j.covered and not j.flagged):
                    return False
        return True
                    
    #debug

    def uncoverAll(self):
        for i in self.grid:
            for j in i:
                j.covered = False
    
    def coverAll(self):
        for i in self.grid:
            for j in i:
                j.covered = True


