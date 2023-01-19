from pygame import *
from tkinter import filedialog
import tilesAndIdleStates

lFile = open("Levels\\level3.txt", "r")
level_1 = eval(lFile.read().strip())

tileDict = tilesAndIdleStates.tileDict

width,height=1200,702
screen=display.set_mode((width,height))
RED=(255,0,0)
GREY=(127,127,127)
BLACK=(0,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
YELLOW=(255,255,0)

row = 13
col = 20
spot = 0

numOfRects=5

dragging = False
origX, origY = 0, 0

widthOfTile = width//col
heightOfTile = height//row

running=True

bgForest = image.load("Textures\\png\\BG\\desertBG.png").convert()

while running:
    for evt in event.get():
        if evt.type==QUIT:
            running=False
        if evt.type==KEYDOWN:
            if evt.key == K_LEFT:
                if spot > 0:
                    spot-=1
            if evt.key == K_RIGHT:
                if spot < numOfRects-1:
                    spot+=1
            if evt.key == K_SPACE:
                myScreen = screen.subsurface(0, 0, width, height).copy()
                fname=filedialog.asksaveasfilename(defaultextension=".png")
                image.save(myScreen, fname)
    screen.blit(bgForest, (0, 0))
    for i in range(row):
        for j in range(col*spot, col*spot+col):
            if level_1[i][j] != ["key_red"] and level_1[i][j] != [] and level_1[i][j] != ["Bat1"] and level_1[i][j] != ["BlueSlime1Right"] and level_1[i][j] != ["PinkSlime1Right"] and level_1[i][j] != ["BlueSlime1Left"] and level_1[i][j] != ["PinkSlime1Left"] and level_1[i][j]!= ["bird1"]:
                screen.blit(tileDict[level_1[i][j][0]], (widthOfTile*j-(spot*width), heightOfTile*i))
    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()
      
   
    display.flip()
            
quit()

#fname=filedialog.asksaveasfilename(defaultextension=".png")