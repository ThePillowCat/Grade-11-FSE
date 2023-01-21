from pygame import *
from random import *

unlockedLevels = [False, True, False, False, False]

init()

def runLevelPicker(myScreen):
    screen=myScreen
    BLACK=(0,0,0)

<<<<<<< HEAD
bgmain=image.load("pics/LevPickMain.png")#initzaliing all  the pictures
bgmain1=image.load("pics/LevPickMain1.png")
bgmain2=image.load("pics/LevPickMain2.png")
bgmain3=image.load("pics/LevPickMain3.png")

stickmannorm=image.load("Textures/png/Player/normal.png")
loc=(210,310)#location

bglevel=bgmain #variable for the background
=======
    running=True

    bgmain=image.load("pics/LevPickMain.png").convert()
    bgmain1=image.load("pics/LevPickMain1.png").convert()
    bgmain2=image.load("pics/LevPickMain2.png").convert()
    bgmain3=image.load("pics/LevPickMain3.png").convert()

    stickmannorm=image.load("Textures/png/Player/normal.png").convert_alpha()
    loc=(210,310)
>>>>>>> 486870e41f3da7b528c6d35f2a05a04fd3215c5e

    bglevel=bgmain
    playingCirlceAnimation = False
    circleSize = 1

    comicFont=font.SysFont("Comic Sans MS",30)
    #"render" creates a picture

<<<<<<< HEAD
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
=======
    Levels_levelpicker=["Choose your level"]
    names_levelpicker=[" "]
    mixer.music.stop()
    mixer.music.load("Sound Effects\\levelSelect.mp3")
    mixer.music.play()
    while running:
        for evt in event.get():
            if evt.type==QUIT:
                running=False
            if evt.type==KEYDOWN and not playingCirlceAnimation:
                if evt.key==K_RIGHT:
                    if loc==(210,310):
                        loc=(418,440)
                        bglevel=bgmain1
                        Levels_levelpicker=["Level 1"]
                        names_levelpicker=["The Enchanted Forest"]
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
                if evt.key==K_LEFT:
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
                if evt.key == K_RETURN and Levels_levelpicker != ["Choose your level"] and unlockedLevels[int(Levels_levelpicker[0][-1])]:
                    mixer.music.stop()
                    mixer.music.load("Sound Effects\\choose.mp3")
                    mixer.music.play()
                    playingCirlceAnimation = True
                    unlockedLevels[int(Levels_levelpicker[0][-1])] = False
                    unlockedLevels[int(Levels_levelpicker[0][-1])+1] = True
        #return "game", int(Levels_levelpicker[0][-1])-1
        if not playingCirlceAnimation:
            screen.blit(bglevel,(0,0))
            screen.blit(stickmannorm,loc)
            level=choice(Levels_levelpicker)
            name=choice(names_levelpicker)
            picLevel=comicFont.render(level,True,BLACK).convert_alpha()#converting the string into a picture
            picknameForLevel=comicFont.render(name,True,BLACK).convert_alpha()
            screen.blit(picLevel,(20,20))
            screen.blit(picknameForLevel,(18,60))
            if Levels_levelpicker[0][-1] != "l":
                if unlockedLevels[int(Levels_levelpicker[0][-1])]:
                    screen.blit(comicFont.render("Unlocked", True, BLACK), (18, 100))
                else:
                    screen.blit(comicFont.render("Locked", True, BLACK), (18, 100))
        else:
            draw.circle(screen, BLACK, (loc[0], loc[1]), 1500, circleSize)
            circleSize+=40
            if not mixer.music.get_busy():
                playingCirlceAnimation = False
                return "game", int(Levels_levelpicker[0][-1])-1 
        display.flip()
    return "menu"
>>>>>>> 486870e41f3da7b528c6d35f2a05a04fd3215c5e
