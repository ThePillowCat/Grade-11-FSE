from pygame import *
from random import *

font.init()

width,height=1200, 703
screen=display.set_mode((width,height))
RED=(255,0,0)
GREY=(127,127,127)
BLACK=(0,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
YELLOW=(255,255,0)
WHITE=(255,255,255)

running=True

bgmain=image.load("pics/LevPickMain.png")#initzaliing all  the pictures
bgmain1=image.load("pics/LevPickMain1.png")
bgmain2=image.load("pics/LevPickMain2.png")
bgmain3=image.load("pics/LevPickMain3.png")

stickmannorm=image.load("Textures/png/Player/normal.png")
loc=(210,310)#location

bglevel=bgmain #variable for the background

comicFont=font.SysFont("Comic Sans MS",30)
#"render" creates a picture

Levels_levelpicker=["Choose your level"]
names_levelpicker=[" "]

##def addPics(name,start,end):
##    '''
##    this function returns a LIST OF PICTURES (1D).
##
##    '''
##    mypics=[]
##    for i in range(start,end+1):
##        mypics.append(image.load(f"Textures/png/Player/Layer {i}.png"))
##
##    return mypics #1D list
##
##
##pics=[]#this will be a 2D list
##pics.append(addPics("Layer",1,12)) #right facing pics
##pics.append(addPics("Layer",12,24)) #down facing pics 

while running:
    for evt in event.get():
        if evt.type==QUIT:
            running=False
        if evt.type==KEYDOWN:
            if evt.key==K_RIGHT:
                if loc==(210,310):
                    #so if we move right from the first location
                    #then our location becomes the second
                    loc=(418,440)
                    bglevel=bgmain1#changing the background
                    Levels_levelpicker=["Level 1"]#which level
                    names_levelpicker=["The Enchanted Forest"]#name of the level so I can blit it underneath
                elif loc==(418,440):
                    loc=(700,126)
                    bglevel=bgmain2
                    Levels_levelpicker=["Level 2"]
                    names_levelpicker=["The Ice Cave"]
                elif loc==(700,126):
                    loc=(983,241)
                    bglevel=bgmain3
                    Levels_levelpicker=["Level 3"]
                    names_levelpicker=["The Hot Dessert"]
            if evt.key==K_LEFT:#if they go left
                if loc==(983,241):
                    loc=(700,126)
                    bglevel=bgmain2
                    Levels_levelpicker=["Level 2"]
                    names_levelpicker=["The Ice Cave"]
                elif loc==(700,126):
                    loc=(418,440)
                    bglevel=bgmain1
                    Levels_levelpicker=["Level 1"]
                    names_levelpicker=["The Enchanted Forest"]
                elif loc==(418,440):
                    loc=(210,310)
                    bglevel=bgmain
                    Levels_levelpicker=["Choose your level"]
                    names_levelpicker=[" "]
                
                
                       
    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()
##    print(mx,my)#this was to check the lockations of the little circles
    
    screen.blit(bglevel,(0,0))#bliting the level
    screen.blit(stickmannorm,loc)#adding the charcter
##    screen.blit(stickmannorm,(418,440))
##    screen.blit(stickmannorm,(700,126))
##    screen.blit(stickmannorm,(983,241))
    level=choice(Levels_levelpicker)
    name=choice(names_levelpicker)
    picLevel=comicFont.render(level,True,BLACK)#converting the string into a picture
    picknameForLevel=comicFont.render(name,True,BLACK)
    screen.blit(picLevel,(20,20))#this is the level 1,2,3
    screen.blit(picknameForLevel,(18,60))#this is the name of the level
    
    
      
   
    display.flip()
            
quit()
