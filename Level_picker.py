from pygame import *
from random import *

init()

def runLevelPicker(myScreen):
    screen=myScreen
    BLACK=(0,0,0)

    running=True

    bgmain=image.load("pics/LevPickMain.png").convert()
    bgmain1=image.load("pics/LevPickMain1.png").convert()
    bgmain2=image.load("pics/LevPickMain2.png").convert()
    bgmain3=image.load("pics/LevPickMain3.png").convert()

    stickmannorm=image.load("Textures/png/Player/normal.png").convert_alpha()
    loc=(210,310)

    bglevel=bgmain
    playingCirlceAnimation = False
    circleSize = 1

    comicFont=font.SysFont("Comic Sans MS",30)
    #"render" creates a picture

    Levels_levelpicker=["Choose your level"]
    names_levelpicker=[" "]
    mixer.music.stop()
    mixer.music.load("Sound Effects\\levelSelect.mp3")
    mixer.music.play()
    while running:
        for evt in event.get():
            if evt.type==QUIT:
                running=False
            if evt.type==KEYDOWN:
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
                if evt.key == K_RETURN and Levels_levelpicker[0][-1] != "l":
                    mixer.music.stop()
                    mixer.music.load("Sound Effects\\choose.mp3")
                    mixer.music.play()
                    playingCirlceAnimation = True
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
        else:
            draw.circle(screen, BLACK, (loc[0], loc[1]), 1500, circleSize)
            circleSize+=40
            if not mixer.music.get_busy():
                return "game", int(Levels_levelpicker[0][-1])-1 
        display.flip()
    
    return "menu"