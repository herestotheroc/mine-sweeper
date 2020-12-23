import pygame
import grid
from math import floor

pygame.init()

size = (800, 830)
screen = pygame.display.set_mode(size)
black = (0,0,0)
white = (255,255,255)
grey = (200,200,200)
red = (200,25,25)
green = (85,245,60)
screen.fill((0,0,0))
pygame.display.set_caption("Minesweeper")
gcols = 20
grows = 20
b = 50
lossScreen = False
winScreen = False

minefield = grid.grid(gcols,grows)

sl = size[0]/minefield.cols
bombfontsize = floor(size[0]/(minefield.cols*1.25))
losefontsize = 200
uifontsize = 35

flagstextpos = (10,802.5)

font = pygame.font.SysFont(None, bombfontsize)
losefont = pygame.font.SysFont(None, losefontsize)
uifont = pygame.font.SysFont(None, uifontsize)

def drawGrid(grid):
    for x in range(grid.cols):
        for y in range(grid.rows):
            currentSquare = grid.getSquare(x+1,y+1)
            pos = (x*sl,y*sl,sl,sl)
            textpos = (x*sl+sl/2-bombfontsize*0.2,y*sl+sl/2-bombfontsize*0.3)
            if grid.face(currentSquare) == -2:
                pygame.draw.rect(screen,green,pos,0)
                num = font.render("F", True, black)
                screen.blit(num,textpos)
            elif grid.face(currentSquare) == -3:
                pygame.draw.rect(screen,white,pos,0)
            elif grid.face(currentSquare) == -1:
                pygame.draw.rect(screen,red,pos,0)
                num = font.render("X", True, black)
                screen.blit(num,textpos)
            elif grid.face(currentSquare) == 0:
                pygame.draw.rect(screen,grey,pos,0)
            else:
                pygame.draw.rect(screen,grey,pos,0)
                num = font.render(str(grid.getNeighborBombs(currentSquare)), True, black)
                screen.blit(num,textpos)
            pygame.draw.rect(screen,black,pos,2)

def drawUI():
    flags = uifont.render(str(b - minefield.flags), True, white)
    screen.blit(flags,flagstextpos)    

def getClickedSquare(grid,x,y):
    for j in grid.grid:
        for i in j:
            if (x > (i.x*sl-sl) and x < (i.x*sl)) and (y > (i.y*sl-sl) and y < (i.y*sl)):
                return i 

def lose():
    losemsg0 = losefont.render("You Lose", True, black)
    screen.blit(losemsg0,(102,302))
    losemsg = losefont.render("You Lose", True, red)
    screen.blit(losemsg,(100,300))

def win():
    winmsg0 = losefont.render("You Win", True, black)
    screen.blit(winmsg0,(122,302))
    winmsg = losefont.render("You Win", True, green)
    screen.blit(winmsg,(120,300))

def drawScreen():
    screen.fill((0,0,0))
    drawGrid(minefield)
    drawUI()

def onClick(grid,mx,my,mb):
    global lossScreen
    global winScreen
    currentSquare = getClickedSquare(grid,mx,my)
    minefield.populateGrid(b, currentSquare)
    if (currentSquare):
        if mb == 0:
            if not currentSquare.flagged:
                if currentSquare.covered and currentSquare.bomb:
                    lossScreen = True
                    currentSquare.covered = False
                elif currentSquare.covered:
                    grid.uncover(currentSquare)
        elif mb == 2:
            grid.flag(currentSquare)
    
    if grid.checkWin():
        winScreen = True
drawScreen()

pygame.display.update()

while True:
    if minefield.checkWin():
            winScreen = True
    
    if not lossScreen and not winScreen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        onClick(minefield,pos[0],pos[1],0)
                        drawScreen()
                if event.button == 3:
                    pos = pygame.mouse.get_pos()
                    onClick(minefield,pos[0],pos[1],2)
                    drawScreen()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    minefield = grid.grid(gcols,grows)
                    minefield.populated = False
                    drawScreen()
                if event.key == pygame.K_x:
                    minefield.uncoverAll()
                    drawScreen()
                if event.key == pygame.K_z:
                    minefield.coverAll()
                    drawScreen()
    elif lossScreen:
        lose()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()           
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    minefield = grid.grid(gcols,grows)
                    minefield.populated = False
                    drawScreen()
                    lossScreen = False
    elif winScreen:
        win()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()           
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    minefield = grid.grid(gcols,grows)
                    minefield.populateGrid(b)
                    drawScreen()
                    winScreen = False

    pygame.display.update()
