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

running=True

row = 13
col = 20
spot = 0

numOfRects=5

level_1 = [[[] for i in range(col*numOfRects)] for j in range(row)]

def drawLevel(screen):
    screen.fill(0)
    for i in range(row):
        for j in range(col*spot, col*spot+col):
            if level_1[i][j]==["X"]:
                draw.rect(screen,BROWN,(width//col*j-(spot)*width, height//row*i, width//col, height//row))
            if level_1[i][j]==["-"]:
                draw.rect(screen,RED,(width//col*j-(spot)*width, height//row*i, width//col, height//row))
    for i in range(col):
        draw.line(screen, GREEN, (width//col*i, 0), (width//col*i, height))
    for i in range(row):
        draw.line(screen, GREEN, (0, height//row*i), (width, height//row*i))

def addTile(x, y, t):
    for i in range(row):
        for j in range(col*spot, col*spot+col):
            if x > width//col*j-(spot)*width and x < width//col*j-(spot)*width+width//col:
                if y > height//row*i and y < height//row*i+height//row:
                    if t == "tile":
                        level_1[i][j] = ["X"]
                    elif t == "lava":
                        level_1[i][j] = ["-"]

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
                # lFile.write("[")
                # for r in level_1[spot]:
                #     lFile.write("\n"+str(repr(r))+",")
                # lFile.write("]")
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
    
    if mb[0]:
        addTile(mx, my, "tile")
    if mb[2]:
        addTile(mx, my, "lava")
    drawLevel(screen)
    display.flip()

quit()