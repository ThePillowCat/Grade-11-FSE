from pygame import *
from pprint import *

# lFile = open("Levels\\level3.txt", "w")

# row = 13
# col = 20

# numOfRects=5
# level_1 = [[[] for i in range(col*numOfRects)] for j in range(row)]

# lFile.write(repr(level_1))

lFile = open("Levels\\level3.txt", "r")
lFileRects = open("Levels\\level3collision.txt", "w")
lFileCollisionRects = open("Levels\\level3collisionobjects.txt", "w")

level_1 = eval(lFile.readline().strip())

lFile = open("Levels\\level3.txt", "w")

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
    "d1" : image.load("Textures\\png\\Tiles\\d1.png").convert_alpha(),
    "d2" : image.load("Textures\\png\\Tiles\\d2.png").convert_alpha(),
    "d3" : image.load("Textures\\png\\Tiles\\d3.png").convert_alpha(),
    "d4" : image.load("Textures\\png\\Tiles\\d4.png").convert_alpha(),
    "d5" : image.load("Textures\\png\\Tiles\\d5.png").convert_alpha(),
    "d6" : image.load("Textures\\png\\Tiles\\d6.png").convert_alpha(),
    "d7" : image.load("Textures\\png\\Tiles\\d7.png").convert_alpha(),
    "d8" : image.load("Textures\\png\\Tiles\\d8.png").convert_alpha(),
    "d9" : image.load("Textures\\png\\Tiles\\d9.png").convert_alpha(),
    "da" : image.load("Textures\\png\\Tiles\\da.png").convert_alpha(),
    "db" : image.load("Textures\\png\\Tiles\\db.png").convert_alpha(),
    "dc" : image.load("Textures\\png\\Tiles\\dc.png").convert_alpha(),
    "door1" : image.load("Textures\\png\\Door\\door1.png").convert_alpha(),
    "door2" : image.load("Textures\\png\\Door\\door2.png").convert_alpha(),
    "door3" : image.load("Textures\\png\\Door\\door3.png").convert_alpha(),
    "door4" : image.load("Textures\\png\\Door\\door4.png").convert_alpha(),
    "water_top": image.load("Textures\png\Tiles\water_top.png").convert_alpha(),
    "water": image.load("Textures\png\Tiles\water.png").convert_alpha(),
    "flag_red" : image.load("Textures\png\Object\\flag_red.png"),
    "flag_blue" : image.load("Textures\png\Object\\flag_blue.png"),
    "question_fire_flower" : image.load("Textures\\png\\Tiles\\block1.png").convert_alpha(),
    "question_gun" : image.load("Textures\\png\\Tiles\\block1.png").convert_alpha(),
    "Tree_2": image.load("Textures\png\Object\Tree_2.png"),
    "fire_flower" : image.load("Textures\png\Tiles\\fire_flower.png").convert_alpha(),
    "neutral_block" : image.load("Textures\png\Tiles\\neutral_block.png").convert_alpha(),
    "BlueSlime1Left": image.load("Textures\png\Enemies\BlueSlime1Left.png").convert_alpha(),
    "BlueSlime2Left": image.load("Textures\png\Enemies\BlueSlime2Left.png").convert_alpha(),
    "BlueSlimeSqRight": image.load("Textures\png\Enemies\BlueSlimeSqLeft.png").convert_alpha(),
    "BlueSlimeDeadRight": image.load("Textures\png\Enemies\BlueSlimeDeadRight.png").convert_alpha(),
    "PinkSlime1Left": image.load("Textures\png\Enemies\PinkSlime1Left.png").convert_alpha(),
    "PinkSlime2Left": image.load("Textures\png\Enemies\PinkSlime2Left.png").convert_alpha(),
    "PinkSlimeSqLeft": image.load("Textures\png\Enemies\PinkSlimeSqLeft.png").convert_alpha(),
    "PinkSlimeDeadRight": image.load("Textures\png\Enemies\PinkSlimeDeadRight.png").convert_alpha(),
    "key_red": image.load("Textures\png\Object\keyRed.png").convert_alpha(),
    "Bush (1)" : image.load("Textures\png\Object\Bush (1).png").convert_alpha(),
    "Bush (2)" : image.load("Textures\png\Object\Bush (2).png").convert_alpha(),
    "Bush (3)" : image.load("Textures\png\Object\Bush (3).png").convert_alpha(),
    "Bush (4)" : image.load("Textures\png\Object\Bush (4).png").convert_alpha(),
    "lava": image.load("Textures\png\Tiles\lava_bottom.png").convert_alpha(),
    "lava_top": image.load("Textures\png\Tiles\lava_top.png").convert_alpha(),
    "bird1" : image.load("Textures\\png\\Enemies\\bird1.png"),
    "BlueSlime1Right": image.load("Textures\png\Enemies\BlueSlime1Right.png").convert_alpha(),
    "PinkSlime1Right": image.load("Textures\png\Enemies\PinkSlime1Right.png").convert_alpha(),
    "Bat1": image.load("Textures\png\Enemies\Bat1.png").convert_alpha(),
}

bgForest = image.load("Textures\\png\\BG\\desertBG.png").convert()

running=True

row = 13
col = 20
spot = 0

numOfRects=5

widthOfTile = width//col
heightOfTile = height//row

dragging = False
dragging2 = False
origX, origY = 0, 0
collisionRects = []
collisionObjects = []
previewRects = [[] for i in range(numOfRects)]
previewObjects = [[] for i in range(numOfRects)]

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
    for c in previewRects[spot]:
        draw.rect(screen, GREEN, c, 10)
    for c in previewObjects[spot]:
        draw.rect(screen, RED, c, 10)

def addTile(x, y, t):
    for i in range(row):
        for j in range(col*spot, col*spot+col):
            if x > width//col*j-(spot*width) and x < width//col*j-(spot*width)+width//col:
                if y > height//row*i and y < height//row*i+height//row:
                    if t == "erase":
                        level_1[i][j] = []
                    else:
                        level_1[i][j] = [t]

def addCollisionBoundry(x, y):
    myRect = Rect(origX, origY, abs(origX-x//widthOfTile*widthOfTile), abs(origY-y//heightOfTile*heightOfTile))
    draw.rect(screen, GREEN, myRect)
    return [coords for coords in myRect]

def addCollisionBoundryObject(x, y):
    myRect = Rect(origX, origY, abs(origX-x//widthOfTile*widthOfTile), abs(origY-y//heightOfTile*heightOfTile))
    draw.rect(screen, RED, myRect)
    return [coords for coords in myRect]

while running:
    
    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()

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
            if evt.key == K_n:
                addTile(mx, my, "door1")
            if evt.key == K_SPACE:
                lFile.write(str(repr(level_1)))
                lFileRects.write(str(repr(collisionRects)))
                lFileCollisionRects.write(str(repr(collisionObjects)))
                lFile.close()
                running = False
    keys = key.get_pressed()
    if keys[K_e]:
        addTile(mx,my,"erase")
    elif keys[K_1]:
        addTile(mx, my, "d1")
    elif keys[K_2]:
        addTile(mx, my, "d2")
    elif keys[K_3]:
        addTile(mx, my, "d3")
    elif keys[K_4]:
        addTile(mx, my, "d4")
    elif keys[K_5]:
        addTile(mx, my, "d5")
    elif keys[K_6]:
        addTile(mx, my, "d6")
    elif keys[K_7]:
        addTile(mx, my, "d7")
    elif keys[K_8]:
        addTile(mx, my, "d8")
    elif keys[K_9]:
        addTile(mx, my, "d9")
    elif keys[K_a]:
        addTile(mx, my, "da")
    elif keys[K_b]:
        addTile(mx, my, "db")
    elif keys[K_c]:
        addTile(mx, my, "dc")
    elif keys[K_t]:
        addTile(mx,my,"Tree_2")
    elif keys[K_h]:
        addTile(mx, my, "Bush (1)")
    elif keys[K_j]:
        addTile(mx, my, "Bush (2)")
    elif keys[K_k]:
        addTile(mx, my, "Bush (3)")
    elif keys[K_o]:
        addTile(mx,my, "BlueSlime1Right")
    elif keys[K_p]:
        addTile(mx,my, "PinkSlime1Right")
    elif keys[K_z]:
        addTile(mx,my,"water_top")
    elif keys[K_x]:
        addTile(mx,my,"water")
    elif keys[K_u]:
        addTile(mx,my,"question_fire_flower")
    elif keys[K_i]:
        addTile(mx,my,"question_gun")
    elif keys[K_q]:
        addTile(mx,my,"key_red")
    elif keys[K_s]:
        addTile(mx,my,"lava")
    elif keys[K_v]:
        addTile(mx,my,"lava_top")
    elif keys[K_0]:
        addTile(mx,my,"bird1")
    elif keys[K_l]:
        addTile(mx,my,"flag_red")
    elif keys[K_y]:
        addTile(mx,my,"Bat1")

    drawLevel(screen)
    if mb[2]:
        if not dragging:
            origX = mx//widthOfTile*widthOfTile
            origY = my//heightOfTile*heightOfTile
            dragging = True
        addCollisionBoundryObject(mx, my)
    elif dragging:
        dragging = False
        myRect = addCollisionBoundryObject(mx, my)
        myRect[0] += spot*width
        collisionObjects.append(myRect)
        previewObjects[spot].append(addCollisionBoundryObject(mx, my))
    if mb[1]:
        if not dragging2:
            origX = mx//widthOfTile*widthOfTile
            origY = my//heightOfTile*heightOfTile
            dragging2 = True
        addCollisionBoundry(mx, my)
    elif dragging2:
        dragging2 = False
        myRect = addCollisionBoundry(mx, my)
        myRect[0] += spot*width
        collisionRects.append(myRect)
        previewRects[spot].append(addCollisionBoundry(mx, my))
    display.flip()

quit()