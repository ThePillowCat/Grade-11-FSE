# menu.py

from pygame import *
GREEN=0,255,0
BLACK=0,0,0
WHITE=255,255,255
screen = display.set_mode((1200, 703))


def instructions():
    running = True
    inst = image.load("pics/Instructions.png")
    inst = transform.smoothscale(inst, screen.get_size())
    screen.blit(inst,(0,0))
    while running:
        #print("instructions")
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        if key.get_pressed()[27]:
            running = False
        display.flip()
    return "menu"
    

#story
def story():
    running = True
    story = image.load("pics/story.png")
    story = transform.smoothscale(story, screen.get_size())
    screen.blit(story,(0,0))
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        if key.get_pressed()[27]:#escape
            running = False
        display.flip()
    return "menu"

#start
def level1():
    running=True
    while running:#game loop level 1
        for evnt in event.get():            
            if evnt.type == QUIT:
                running=False
        screen.fill((125,100,100))
        
        display.flip()
        if key.get_pressed()[27]:
            running = False
    return "menu"




def menu():  
    running = True
    myClock = time.Clock()
    buttons=[Rect(600,400,363,151),Rect(600,300,252,87),Rect(900,300,155,80)]#creating the buttons
    instructionspic=image.load("pics/instructionspic.png")
    instructionspicB=image.load("pics/instructionspicB.png")
    storypic=image.load("pics/storypic.png")
    storypicB=image.load("pics/storypicB.png")
    startpic=image.load("pics/startpic.png")
    startpicB=image.load("pics/startpicB.png")
    bgmenu=image.load("pics/bgmenu.png")
    while running:
        #print("main menu")
        for evnt in event.get():            
            if evnt.type == QUIT:
                return "exit"
        screen.blit(bgmenu,(0,0))#####background of the menu
        
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
        for b in buttons:
            draw.rect(screen,WHITE,b)
        screen.blit(instructionspic,(600,300,235,70))
        screen.blit(storypic,(900,300,235,70))
        screen.blit(startpic,(600,400))

        if buttons[0].collidepoint(mx,my):
            draw.rect(screen,WHITE,(600,400,370,152))
            screen.blit(startpicB,(605,395))
            if mb[0]==1:
                    return "lev1"
        if buttons[1].collidepoint(mx,my):
            draw.rect(screen,WHITE,(600,300,252,87))
            screen.blit(instructionspicB,(595,295))
            if mb[0]==1:
                return "instructions"
        if buttons[2].collidepoint(mx,my):
            draw.rect(screen,WHITE,(900,300,173,80))
            screen.blit(storypicB,(895,295))
            if mb[0]==1:
                return "story"
                       
        display.flip()
        myClock.tick(60)


running = True
x,y = 0,0
OUTLINE = (150,50,30)
page = "menu"
while page != "exit":
    if page == "menu":
        page = menu()
    if page == "lev1":
        page = level1()
    if page == "instructions":
        page = instructions()    
    if page == "story":
        page = story()    
  
quit()
