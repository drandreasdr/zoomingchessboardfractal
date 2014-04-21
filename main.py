#from __future__ import division
import pygame, sys, os
import chessboardfractal
#Position of window on screen:
os.environ['SDL_VIDEO_CENTERED'] = '1'
#position = (50,50)
#os.environ['SDL_VIDEO_WINDOW_POS'] = str(position[0]) + "," + str(position[1])
from pygame.locals import *
#os.chdir('C:/Users/andreasdr/Dropbox/Programming/Python/workspace/zoomingchessboardfractal')
os.chdir(sys.path[0])
#os.chdir(os.path.dirname(sys.argv[0])) #if the above doesn't work

def main():
    #Simulation parameters:
    SIZEscreen = 8*80
    SIZEboard = 8*80.
    nBoards = 4
    nCells = 8
    zoomDoublingTime = 1./3
    MAXFPS = 60.

    #Initialize stuff:
    pygame.init() #must be called first
    pygame.display.set_caption('Zooming Chessboard Fractal')
    DISPLAYSURF = pygame.display.set_mode((SIZEscreen, SIZEscreen))
    chessBoardFractal = chessboardfractal.ChessBoardFractal(nBoards, 0, 0, SIZEboard, nCells, chessboardfractal.ChessBoard.POLARITY_TOP_LEFT_WHITE, zoomDoublingTime)

    running = True
    #Creating the time handler (right before the game loop starts so that
    # the first time step isn't too long).
    FPSCLOCK = pygame.time.Clock()
    while True:
        dt = FPSCLOCK.tick(MAXFPS)*1./1000
        #Event handling:
        for event in pygame.event.get():
            #quitting:
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYUP and event.key == K_p:
                running = not running
                print(running)
        if running == True:
            #Update game state:
            chessBoardFractal.tick(dt)
            #Render:
            pygame.draw.rect(DISPLAYSURF, (255,255,255), (0,0,SIZEscreen, SIZEscreen))
            chessBoardFractal.draw(DISPLAYSURF)
            pygame.display.update()

if __name__ == '__main__':
    main()
