from pygame import *
from pprint import *

lFile = open("level1.txt", "w")

width,height=1200,703
screen=display.set_mode((width,height))
RED=(255,0,0)
GREY=(127,127,127)
BLACK=(0,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
YELLOW=(255,255,0)
BROWN=(205, 127, 50)

tileDict = {
    "t_l_side_dirt" : image.load("Textures\\png\\Tiles\\t_l_side_dirt.png"),
    "t_m_side_dirt" : image.load("Textures\\png\\Tiles\\dirt.png"),
    "t_r_side_dirt" : image.load("Textures\\png\\Tiles\\t_r_side_dirt.png"),
    "m_r_side_dirt" : image.load("Textures\\png\\Tiles\\m_r_side_dirt.png"),
    "m_l_side_dirt" : image.load("Textures\\png\\Tiles\\m_l_side_dirt.png"),
    "m_m_side_dirt" : image.load("Textures\\png\\Tiles\\m_dirt.png"),
    "b_r_side_dirt" : image.load("Textures\\png\\Tiles\\b_r_side_dirt.png"),
    "b_l_side_dirt" : image.load("Textures\\png\\Tiles\\b_l_side_dirt.png"),
    "b_m_side_dirt" : image.load("Textures\\png\\Tiles\\b_m_side_dirt.png"),
    "door" : image.load("Textures\\png\\Door\\door1.png"),
    "question" : image.load("Textures\\png\\Tiles\\block1.png")
}

bgForest = image.load("Textures\\png\\BG\\BG.png").convert()

running=True

row = 13
col = 20
spot = 0

numOfRects=3

level_1 = [[[] for i in range(col*numOfRects)] for j in range(row)]


widthOfTile = width//col
heightOfTile = height//row

def drawLevel(screen):
    screen.blit(bgForest,(0,0))
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
                    if t is "erase":
                        level_1[i][j] = []
                    else:
                        level_1[i][j] = [t]

while running:
    
    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()

    for evt in event.get():
        if evt.type==QUIT:
            running=False
        if evt.type==MOUSEBUTTONDOWN:
            if evt.button==2:
                lFile.write(repr(level_1))
        if evt.type==KEYDOWN:
            if evt.key == K_LEFT:
                if spot > 0:
                    spot-=1
            if evt.key == K_RIGHT:
                if spot < numOfRects-1:
                    spot+=1
            if evt.key == K_n:
                addTile(mx, my, "door")
            if evt.key == K_m:
                addTile(mx, my, "question")
            if evt.key == K_e:
                addTile(mx,my,"erase")
            if evt.key == K_1:
                addTile(mx, my, "t_l_side_dirt")
            if evt.key == K_2:
                addTile(mx, my, "t_m_side_dirt")
            if evt.key == K_3:
                addTile(mx, my, "t_r_side_dirt")
            if evt.key == K_4:
                addTile(mx, my, "m_l_side_dirt")
            if evt.key == K_5:
                addTile(mx, my, "m_m_side_dirt")
            if evt.key == K_6:
                addTile(mx, my, "m_r_side_dirt")
            if evt.key == K_7:
                addTile(mx, my, "b_l_side_dirt")
            if evt.key == K_8:
                addTile(mx, my, "b_m_side_dirt")
            if evt.key == K_9:
                addTile(mx, my, "b_r_side_dirt")
            if evt.key == K_SPACE:
                lFile.write(repr(level_1))
    
    if mb[0]:
        addTile(mx, my, "t_m_side_dirt")
    if mb[2]:
        addTile(mx, my, "lava")
    drawLevel(screen)
    display.flip()

quit()
