from pygame import *
from pprint import *

lFile = open("Levels\\level1.txt", "w")

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
    "t_l_side_dirt" : image.load("Textures\\png\\Tiles\\t_l_side_dirt.png").convert_alpha(),
    "t_m_side_dirt" : image.load("Textures\\png\\Tiles\\dirt.png").convert_alpha(),
    "t_r_side_dirt" : image.load("Textures\\png\\Tiles\\t_r_side_dirt.png").convert_alpha(),
    "m_r_side_dirt" : image.load("Textures\\png\\Tiles\\m_r_side_dirt.png").convert_alpha(),
    "m_l_side_dirt" : image.load("Textures\\png\\Tiles\\m_l_side_dirt.png").convert_alpha(),
    "m_m_side_dirt" : image.load("Textures\\png\\Tiles\\m_dirt.png").convert_alpha(),
    "b_r_side_dirt" : image.load("Textures\\png\\Tiles\\b_r_side_dirt.png").convert_alpha(),
    "b_l_side_dirt" : image.load("Textures\\png\\Tiles\\b_l_side_dirt.png").convert_alpha(),
    "b_m_side_dirt" : image.load("Textures\\png\\Tiles\\b_m_side_dirt.png").convert_alpha(),
    "p_l_side_dirt" : image.load("Textures\\png\\Tiles\\p_l_side_dirt.png").convert_alpha(),
    "p_m_side_dirt" : image.load("Textures\\png\\Tiles\\p_m_side_dirt.png").convert_alpha(),
    "p_r_side_dirt" : image.load("Textures\\png\\Tiles\\p_r_side_dirt.png").convert_alpha(),
    "door1" : image.load("Textures\\png\\Door\\door1.png").convert_alpha(),
    "door2" : image.load("Textures\\png\\Door\\door2.png").convert_alpha(),
    "door3" : image.load("Textures\\png\\Door\\door3.png").convert_alpha(),
    "door4" : image.load("Textures\\png\\Door\\door4.png").convert_alpha(),
    "question" : image.load("Textures\\png\\Tiles\\block1.png").convert_alpha(),
    "Tree_2": image.load("Textures\png\Object\Tree_2.png"),
    "fire_flower" : image.load("Textures\png\Tiles\\fire_flower.png").convert_alpha(),
    "neutral_block" : image.load("Textures\png\Tiles\\neutral_block.png").convert_alpha(),
    "Bush (1)" : image.load("Textures\png\Object\Bush (1).png").convert_alpha(),
    "Bush (2)" : image.load("Textures\png\Object\Bush (2).png").convert_alpha(),
    "Bush (3)" : image.load("Textures\png\Object\Bush (3).png").convert_alpha(),
    "Bush (4)" : image.load("Textures\png\Object\Bush (4).png").convert_alpha(),
    "BlueSlime1Left": image.load("Textures\png\Enemies\BlueSlime1Left.png").convert_alpha(),
    "BlueSlime2Left": image.load("Textures\png\Enemies\BlueSlime2Left.png").convert_alpha(),
    "BlueSlimeSqLeft": image.load("Textures\png\Enemies\BlueSlimeSqLeft.png").convert_alpha(),
    "BlueSlimeDeadLeft": image.load("Textures\png\Enemies\BlueSlimeDeadLeft.png").convert_alpha(),
    "PinkSlime1Left": image.load("Textures\png\Enemies\PinkSlime1Left.png").convert_alpha(),
    "PinkSlime2Left": image.load("Textures\png\Enemies\PinkSlime2Left.png").convert_alpha(),
    "PinkSlimeSqLeft": image.load("Textures\png\Enemies\PinkSlimeSqLeft.png").convert_alpha(),
    "PinkSlimeDeadLeft": image.load("Textures\png\Enemies\PinkSlimeDeadRight.png").convert_alpha(),
    "BlueSlime1Right": image.load("Textures\png\Enemies\BlueSlime1Right.png").convert_alpha(),
    "BlueSlime2Right": image.load("Textures\png\Enemies\BlueSlime2Right.png").convert_alpha(),
    "BlueSlimeSqRight": image.load("Textures\png\Enemies\BlueSlimeSqRight.png").convert_alpha(),
    "BlueSlimeDeadRight": image.load("Textures\png\Enemies\BlueSlimeDeadRight.png").convert_alpha(),
    "PinkSlime1Right": image.load("Textures\png\Enemies\PinkSlime1Right.png").convert_alpha(),
    "PinkSlime2Right": image.load("Textures\png\Enemies\PinkSlime2Right.png").convert_alpha(),
    "PinkSlimeSqRight": image.load("Textures\png\Enemies\PinkSlimeSqRight.png").convert_alpha(),
    "PinkSlimeDeadRight": image.load("Textures\png\Enemies\PinkSlimeDeadRight.png").convert_alpha(),
    "water_top": image.load("Textures\png\Enemies\water_top.png").convert_alpha(),
    "water": image.load("Textures\png\Enemies\water.png").convert_alpha(),
}

bgForest = image.load("Textures\\png\\BG\\BG.png").convert()

running=True

row = 13
col = 20
spot = 0

numOfRects=5

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
                addTile(mx, my, "door1")
            if evt.key == K_m:
                addTile(mx, my, "question")
            if evt.key == K_SPACE:
                lFile.write(repr(level_1))
    keys = key.get_pressed()
    if keys[K_e]:
        addTile(mx,my,"erase")
    elif keys[K_1]:
        addTile(mx, my, "t_l_side_dirt")
    elif keys[K_2]:
        addTile(mx, my, "t_m_side_dirt")
    elif keys[K_3]:
        addTile(mx, my, "t_r_side_dirt")
    elif keys[K_4]:
        addTile(mx, my, "m_l_side_dirt")
    elif keys[K_5]:
        addTile(mx, my, "m_m_side_dirt")
    elif keys[K_6]:
        addTile(mx, my, "m_r_side_dirt")
    elif keys[K_7]:
        addTile(mx, my, "b_l_side_dirt")
    elif keys[K_8]:
        addTile(mx, my, "b_m_side_dirt")
    elif keys[K_9]:
        addTile(mx, my, "b_r_side_dirt")
    elif keys[K_a]:
        addTile(mx, my, "p_l_side_dirt")
    elif keys[K_b]:
        addTile(mx, my, "p_m_side_dirt")
    elif keys[K_c]:
        addTile(mx, my, "p_r_side_dirt")
    elif keys[K_t]:
        addTile(mx,my,"Tree_2")
    elif keys[K_h]:
        addTile(mx, my, "Bush (1)")
    elif keys[K_j]:
        addTile(mx, my, "Bush (2)")
    elif keys[K_k]:
        addTile(mx, my, "Bush (3)")
    elif keys[K_l]:
        addTile(mx, my, "Bush (4)")
    elif keys[K_o]:
        addTile(mx,my, "BlueSlime1Right")
    elif keys[K_p]:
        addTile(mx,my, "PinkSlime1Right")
    elif keys[K_z]:
        addTile(mx,my,"water_top")
    elif keys[K_x]:
        addTile(mx,my,"water")
    if mb[0]:
        addTile(mx, my, "t_m_side_dirt")
    if mb[2]:
        addTile(mx, my, "lava")
    drawLevel(screen)
    display.flip()

quit()
