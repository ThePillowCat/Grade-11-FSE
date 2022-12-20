from pygame import *
from pprint import *

lFile = open("level1.txt", "w")

width,height=1200,780
screen=display.set_mode((width,height))
RED=(255,0,0)
GREY=(127,127,127)
BLACK=(0,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
YELLOW=(255,255,0)
BROWN=(205, 127, 50)

tileDict = {
    "t_l_side_dirt" : image.load("FreeTileset\\png\\Tiles\\t_l_side_dirt.png"),
    "dirt" : image.load("FreeTileset\\png\\Tiles\\dirt.png"),
    "t_r_side_dirt" : image.load("FreeTileset\\png\\Tiles\\t_r_side_dirt.png"),
}

running=True

row = 13
col = 20
spot = 0

numOfRects=5

level_1 = [[[] for i in range(col*numOfRects)] for j in range(row)]

def fixTextures(level_1):
    for i in range(row):
        for j in range(col*spot, col*spot+col):
            if level_1[i][j] == ["dirt"]:
                for k in range(j, col*spot+col):
                    if level_1[i][k-1] == []:
                        level_1[i][k] = ["t_l_side_dirt"]
                    if level_1[i][k+1] == []:
                        level_1[i][k] = ["t_r_side_dirt"]
                        break
                if level_1[i][j-1] == [] and level_1[i][j+1] == []:
                    level_1[i][j] = ["dirt"]
    return level_1



widthOfTile = width//col
heightOfTile = height//row

def drawLevel(screen):
    screen.fill(0)
    for i in range(row):
        for j in range(col*spot, col*spot+col):
            if level_1[i][j] != []:
                screen.blit(tileDict[level_1[i][j][0]], (widthOfTile*j-(spot*width), heightOfTile*i))
    for i in range(col):
        draw.line(screen, GREEN, (width//col*i, 0), (width//col*i, height))
    for i in range(row):
        draw.line(screen, GREEN, (0, height//row*i), (width, height//row*i))

def addTile(x, y, t):
    for i in range(row):
        for j in range(col*spot, col*spot+col):
            if x > width//col*j-(spot*width) and x < width//col*j-(spot*width)+width//col:
                if y > height//row*i and y < height//row*i+height//row:
                    if t == "tile":
                        level_1[i][j] = ["dirt"]
                    elif t == "lava":
                        level_1[i][j] = ["lava"]
                    elif t == "door":
                        level_1[i][j] = ["door"]

while running:
    
    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()

    for evt in event.get():
        if evt.type==QUIT:
            running=False
        if evt.type==MOUSEBUTTONDOWN:
            # if evt.button==1:
            #     addTile(mx, my, "tile")
            if evt.button==2:
                lFile.write(repr(level_1))
            # if evt.button==3:
            #     addTile(mx,my,"lava")
        if evt.type==KEYDOWN:
            if evt.key == K_LEFT:
                if spot > 0:
                    spot-=1
            if evt.key == K_RIGHT:
                if spot < numOfRects-1:
                    spot+=1
            if evt.key == K_1:
                addTile(mx, my, "door")
            if evt.key == K_9:
                level_1 = fixTextures(level_1)
            if evt.key == K_SPACE:
                lFile.write(repr(level_1))
    
    if mb[0]:
        addTile(mx, my, "tile")
    if mb[2]:
        addTile(mx, my, "lava")
    drawLevel(screen)
    display.flip()

quit()
