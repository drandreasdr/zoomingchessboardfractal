import pygame
SIZE = 200
pygame.init()
DISPLAYSURF = pygame.display.set_mode((SIZE, SIZE))
D=70.9
xT=0.3
yT=0
#pygame.draw.rect(DISPLAYSURF, (255,0,0),     (0, 0, SIZE, SIZE))
pygame.draw.rect(DISPLAYSURF, (255,255,255), (xT,   yT,   D, D))
pygame.draw.rect(DISPLAYSURF, (255,255,255), (xT+D, yT+D, D, D))
pygame.draw.rect(DISPLAYSURF, (0,0,0),       (xT,   yT+D, D, D))
pygame.draw.rect(DISPLAYSURF, (0,0,0),       (xT+D, yT,   D, D))
pygame.display.update()