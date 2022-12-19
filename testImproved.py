from pygame import *

from pygame import *
GREEN=0,255,0


def instructions():
    running = True
    inst = image.load("pics/instructions.png")
    inst = transform.smoothscale(inst, screen.get_size())
    screen.blit(inst,(0,0))
    while running:
        print("instructions")
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        if key.get_pressed()[27]:
            running = False
        ##add a "back to main menu" button
        display.flip()
    return "menu"
    

def story():
    running = True
    story = image.load("pics/story.png")
    story = transform.smoothscale(story, screen.get_size())
    screen.blit(story,(0,0))
    while running:
        print("story")
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        ### add a back to menu button
        if key.get_pressed()[27]:#escape
            running = False
        ###add a "back to main menu" button
        display.flip()
    return "menu"

def start():
    running=True
    while running:#game loop level 1
        print("start game")
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
    buttons=[Rect(100+x*150,300,80,40) for x in range(4)]#creating the buttons
    while running:
        print("main menu")
        for evnt in event.get():            
            if evnt.type == QUIT:
                return "exit"
        screen.fill(0)
        
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
        for b in buttons:
            draw.rect(screen,GREEN,b)

        if mb[0]==1:
            if buttons[0].collidepoint(mx,my):
                return "start"
            if buttons[2].collidepoint(mx,my):
                return "instructions"
            if buttons[3].collidepoint(mx,my):
                return "story"
                       
        display.flip()
        myClock.tick(60)

# This is the important part of the example.
# The idea is we have a variable (page) that keeps
# track of which page we are one. We give control
# of the program to a function until it is done and
# the program returns the new page it should be on.
screen = display.set_mode((800, 600))
running = True
x,y = 0,0
OUTLINE = (150,50,30)
page = "menu"
while page != "exit":
    if page == "menu":
        page = menu()
    if page == "start":
        page = start() 
    if page == "instructions":
        page = instructions()    
    if page == "story":
        page = story()    
  
quit()
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##l1File = open("level1.txt","r")
##
##class Level():
##    def __init__(self, screen):
##        self.screen = screen
##    def drawLevel(self):
##        #draw all three levels
##        for i in range(row):
##            for j in range(lower, upper):
##                if level_1[i][j]==["X"]:
##                    draw.rect(self.screen,BROWN,(widthOfTile*j+player.offset, heightOfTile*i, widthOfTile, heightOfTile))
##                if level_1[i][j]==["-"]:
##                    draw.rect(self.screen,RED,(widthOfTile*j+player.offset, heightOfTile*i, widthOfTile, heightOfTile))
##        #draw grid lines (just for debugging right now)
##        for i in range(col):
##            draw.line(self.screen, GREEN, (width//col*i, 0), (width//col*i, height))
##        for i in range(row):
##            draw.line(self.screen, GREEN, (0, height//row*i), (width, height//row*i))
##        #draw lines for when the screen should scroll (also just for debugging)
##        draw.line(self.screen,RED,(900,0),(900,height))
##        draw.line(self.screen,RED,(240,0),(240,height))
##
##class Player():
##    def __init__(self, x, y, screen):
##        self.screen = screen
##        self.x=x
##        self.y=y
##        self.vel = [0,0]
##        self.gravity = 1
##        self.size = [50, 100]
##        self.groundY = height
##        self.jumpPower = -22
##        self.moving = True
##        self.offset = 0
##        self.posInLevel = 0
##
##    def movePlayer(self):
##        #getting keys list
##        keys = key.get_pressed()
##
##        #resetting horizontal velocity
##        self.vel[0] = 0
##        if keys[K_LEFT]:
##            self.vel[0]=-5
##        if keys[K_RIGHT]:
##            self.vel[0]=5
##        if keys[K_SPACE] and self.y+self.size[1] == self.groundY and self.vel[1] < 1:
##            self.vel[1] = self.jumpPower
##
##        #determines if the player is moving or not
##        if self.vel[0] != 0 and self.moving == False:
##            self.moving = True
##        if self.vel[0] == 0 and self.moving:
##            self.moving = False
##
##        #adding x and y velocities
##        self.x+=self.vel[0]
##        self.vel[1]+=self.gravity
##        self.posInLevel=self.x+abs(self.offset)
##    
##    def checkPlayerCollision(self):
##        #checks when the level should be scrolled
##        if self.x+self.size[0] > 900 and self.posInLevel < right:
##            self.x = 900-self.size[0]
##            if self.moving:
##                self.offset -= 5
##        if self.x < 240 and self.posInLevel > 240:
##            self.x = 240
##            if self.moving and self.posInLevel > 240:
##                self.offset += 5
##        #checks if the player is hitting the ground
##        #default the ground to height-the void
##        #then loop through and check if there is a platform directly under the player
##        self.groundY=0
##        #Maybe revisit if statement here?
##        breakLoop=False
##        self.groundY = height
##        # if len(level_1[(self.y+self.size[1])//heightOfTile][self.posInLevel//widthOfTile]) != 0 or len(level_1[(self.y+self.size[1])//heightOfTile][self.posInLevel//widthOfTile+1]) != 0:
##        #     if self.x+self.size[0]>widthOfTile*j+self.offset and self.x < widthOfTile*j+player.offset+widthOfTile and player.y+player.size[1]<=heightOfTile*i and player.y+player.size[1]+player.vel[1]>=heightOfTile*i:
##        #                 self.groundY = height//row*i
##        #                 self.vel[1] = 0
##        #                 self.y = self.groundY-player.size[1]
##        #                 breakLoop=True
##        #                 break
##        for i in range(row):
##            for j in range(lower, upper):
##                if len(level_1[i][j]) !=0:
##                    if self.x+self.size[0]>widthOfTile*j+self.offset and self.x < widthOfTile*j+player.offset+widthOfTile and player.y+player.size[1]<=heightOfTile*i and player.y+player.size[1]+player.vel[1]>=heightOfTile*i:
##                        self.groundY = height//row*i
##                        self.vel[1] = 0
##                        self.y = self.groundY-player.size[1]
##                        breakLoop=True
##                        break
##            if breakLoop:
##                break
##        # #checking if player is in void
##        self.y+=self.vel[1]
##        if self.y+self.size[1] >= height:
##            self.vel[1] = 0
##            self.groundY=height
##            self.y = height-player.size[1]
##
##    def drawPlayer(self):
##        draw.rect(self.screen,RED,(self.x,player.y,player.size[0],player.size[1]))
##        
##width,height=1200,703
##screen=display.set_mode((width,height))
##RED=(255,0,0)
##GREY=(127,127,127)
##BLACK=(0,0,0)
##BLUE=(0,0,255)
##GREEN=(0,255,0)
##YELLOW=(255,255,0)
##BLACK = (0,0,0)
##BROWN=(205, 127, 50)
##
##running=True
##
###OBJECTS
##myClock = time.Clock()
##player = Player(300,100,screen)
##level = Level(screen)
##
###LEVEL LISTS AND VARIABLES
##row = 13
##col = 20
##spot = 0
##widthOfTile = width//col
##heightOfTile = height//row
###Called level_1 instead of level bc I'm too lazy to change it lol
##level_1 = eval(l1File.readline().strip("\n"))
##
###boundries for scrolling:
##lenOfLevel = len(level_1[0])
##right = lenOfLevel*widthOfTile-591
##
##while running:
##    lower = (player.posInLevel)//widthOfTile-20
##    if lower < 0:
##        lower = 0
##    upper = (player.posInLevel+width)//widthOfTile+1
##    if upper > lenOfLevel:
##        upper = lenOfLevel
##    #getting mouse coords
##    mx,my=mouse.get_pos()
##    mb=mouse.get_pressed()
##
##    #drawing background - SUBJECT TO CHANGE
##    screen.fill(0)
##
##    for evt in event.get():
##        if evt.type==QUIT:
##            running=False
##        if evt.type==MOUSEBUTTONDOWN:
##            if evt.button==1:
##                print(mx,my)
##
##    player.movePlayer()
##    player.checkPlayerCollision()
##    level.drawLevel()
##    player.drawPlayer()
##
##    #flipping display and insuring 60fps
##    display.flip()
##    myClock.tick(60)
##
##l1File.close()            
##quit()
