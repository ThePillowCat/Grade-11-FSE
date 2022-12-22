from pygame import *

l1File = open("level1.txt","r")

l2File = open("level2.txt","r")
l3File = open("level3.txt","r")

level_1 = eval(l1File.readline().strip("\n"))
level_2 = eval(l2File.readline().strip("\n"))
level_3 = eval(l3File.readline().strip("\n"))

width,height=1200,703
screen=display.set_mode((width,height))

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
    "door" : image.load("Textures\\png\\Door\\door1.png").convert(),
    "question" : image.load("Textures\\png\\Tiles\\block1.png").convert()
}

class UI():
    pass

class Level():
    def __init__(self, screen):
        self.screen = screen
        self.levels = [level_1, level_2, level_3]
        self.currentLevel = 0
        self.curFrame = 0
        self.door = [image.load("Textures\\png\\Door\\door" + str(i) + ".png") for i in range(1,5)]
    def drawLevel(self):
        for i in range(row):
            for j in range(lower, upper):
                if len(self.levels[self.currentLevel][i][j])!=0:
                    screen.blit(tileDict[self.levels[self.currentLevel][i][j][0]], (widthOfTile*j+player.offset, heightOfTile*i))
class Player():
    def __init__(self, x, y, screen):
        self.screen = screen
        self.x=x
        self.y=y
        self.vel = [0,0]
        self.gravity = 1
        self.size = [50, 100]
        self.groundY = height
        self.jumpPower = -22
        self.moving = True
        self.offset = 0
        self.posInLevel = 0
        self.animationFrames = [[image.load("Textures\\png\\Player\\Layer "+str(i+j)+".png") for i in range(1, 13)] for j in range(0, 13, 12)]
        self.moveSpot = 0
        self.direction = 0
        self.powerUp = "fireball"
        self.fireBalls = []

    def movePlayer(self):
        #getting keys list
        keys = key.get_pressed()
        self.vel[0] = 0
        self.vel[1]+=self.gravity
        #checking inputs
        if keys[K_LEFT]:
            self.vel[0]=-5
            self.x-=5
            playerRect = Rect(self.posInLevel-5, self.y+5, 2, self.size[1]-10)
            if playerRect.collidelist(level_1_Rects) != -1:
                self.vel[0]=0
                self.x+=5
            self.direction = 1
        elif keys[K_RIGHT]:
            self.vel[0]=5
            self.x+=5
            playerRect = Rect(self.posInLevel+self.size[0]+5, self.y+5, 1, self.size[1]-10)
            if playerRect.collidelist(level_1_Rects) != -1:
                self.vel[0]=0
                self.x-=5
            self.direction = 0
        if keys[K_SPACE] and self.y+self.size[1] == self.groundY and self.vel[1] <= 1:
            self.vel[1] = self.jumpPower

        #defaults the ground to be the void
        self.groundY = height

        #checks if hit ground or ceiling
        for i in range(row):
            for j in range(lower, upper):
                tileRect = Rect(widthOfTile*j+self.offset, heightOfTile*i, widthOfTile, heightOfTile)
                playerRect = Rect(self.x, self.y, self.size[0], self.size[1])
                if ["m_m_side_dirt"] != level.levels[level.currentLevel][i][j] != []:
                    if self.x+self.size[0]>widthOfTile*j+self.offset and self.x < widthOfTile*j+player.offset+widthOfTile and player.y+player.size[1]<=heightOfTile*i and player.y+player.size[1]+player.vel[1]>=heightOfTile*i:
                        self.groundY = height//row*i
                        self.vel[1] = 0
                        self.y = self.groundY-player.size[1]
                    tileRect = Rect(widthOfTile*j+self.offset, heightOfTile*i, widthOfTile, heightOfTile)
                    playerRect = Rect(self.x, self.y+self.vel[1], self.size[0], self.size[1])
                    if tileRect.colliderect(playerRect):
                        self.vel[1] = 0
        #updating the yPos of the player
        self.y+=self.vel[1]
        #moving player, adding gravity, updating position variable
        self.posInLevel=self.x+abs(self.offset)
        
        #determines if the player is moving or not
        if self.vel[0] != 0 and self.moving == False:
            self.moving = True
        if self.vel[0] == 0 and self.moving:
            self.moving = False

        #checking if player is in the void
        if self.y+self.size[1] >= height:
            self.vel[1] = 0
            self.groundY=height
            self.y = height-player.size[1]
    
    def checkPlayerCollision(self):
        #checks when the level should be scrolled
        #also check if the player is hitting an enemy
        if self.x+self.size[0] > 900 and self.posInLevel < right:
            self.x = 900-self.size[0]
            if self.moving:
                self.offset -= 5
        if self.x < 240 and self.posInLevel > 240:
            self.x = 240
            if self.moving and self.posInLevel > 240:
                self.offset += 5

    def drawPlayer(self):
        if not self.moving:
            self.moveSpot = 0
        if self.moveSpot > 10:
            self.moveSpot = 0
        self.moveSpot+=0.6
        screen.blit(self.animationFrames[self.direction][int(self.moveSpot)], (self.x, self.y))
    
    def usePowerUp(self, powerUp):
        if powerUp == "fireball":
            for i in range(len(self.fireBalls)):
                draw.circle(screen, RED, (self.fireBalls[i].x+self.offset, self.fireBalls[i].y), self.fireBalls[i].rad)
                bottomOfFireball = Rect(self.fireBalls[i].x+5, self.fireBalls[i].y+(self.fireBalls[i].rad*2), (self.fireBalls[i].rad*2)-10, 5)
                rightOfFireball = Rect(self.fireBalls[i].x+(self.fireBalls[i].rad*2), self.y+5, 1, (self.fireBalls[i].rad*2)-10)
                leftOfFireball = Rect(self.fireBalls[i].x, self.y, 1, (self.fireBalls[i].rad*2))
                #topOfFireball = Rect(self.fireBalls[i].x+self.offset+(self.fireBalls[i].rad*2)+self.offset, self.y, 1, (self.fireBalls[i].rad*2))
                #deletes fireball if it's in the void (at bottom of screen)
                if self.fireBalls[i].y+self.fireBalls[i].rad > height:
                    self.fireBalls[i].bounces = 4
                if rightOfFireball.collidelist(level_1_Rects) != -1:
                    self.fireBalls[i].bounces = 4
                if leftOfFireball.collidelist(level_1_Rects) != -1:
                    self.fireBalls[i].bounces = 4
                    print("yo")
                if bottomOfFireball.collidelist(level_1_Rects) != -1:
                    self.fireBalls[i].vel[1]=-8
                    self.fireBalls[i].bounces+=1
                # if leftOfFireball.collidelist(level_1_Rects) != -1:
                #     self.fireBalls[i].bounces = 4
                #increasing gravity, updating x and y based off velocites
                self.fireBalls[i].vel[1]+=self.fireBalls[i].gravity
                self.fireBalls[i].y+=self.fireBalls[i].vel[1]
                self.fireBalls[i].x+=self.fireBalls[i].speed
            temp = len(self.fireBalls)
            for i in range(temp-1,-1,-1):
                if self.fireBalls[i].bounces > 3:
                    del self.fireBalls[i]
class Fireball():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 10
        self.vel = [self.speed, 8]
        if player.direction != 0:
            self.speed=-self.speed
        self.gravity = 0.5
        self.rad = 10
        self.bounces = 0

RED=(255,0,0)
GREY=(127,127,127)
BLACK=(0,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
YELLOW=(255,255,0)
BLACK = (0,0,0)
BROWN=(205, 127, 50)
running=True

#OBJECTS
myClock = time.Clock()
player = Player(300,100,screen)
level = Level(screen)

#LEVEL LISTS AND VARIABLES
row = 13
col = 20
spot = 0
widthOfTile = width//col
heightOfTile = height//row

#boundries for scrolling:
lenOfLevel = len(level_1[0])
right = lenOfLevel*widthOfTile-591

bgForest = image.load("Textures\\png\\BG\\BG.png").convert()

level_1_Rects = []
for i in range(row):
    for j in range(lenOfLevel):
        if level_1[i][j] != []:
            level_1_Rects.append(Rect(widthOfTile*j, heightOfTile*i, widthOfTile, heightOfTile))

while running:
    keys = key.get_pressed()
    lower = (player.posInLevel)//widthOfTile-20
    if lower < 0:
        lower = 0
    upper = (player.posInLevel+width)//widthOfTile+1
    if upper > lenOfLevel:
        upper = lenOfLevel
    #getting mouse coords
    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()

    #drawing background - SUBJECT TO CHANGE
    screen.blit(bgForest, (0,0))

    for evt in event.get():
        if evt.type==QUIT:
            running=False
        if evt.type==MOUSEBUTTONDOWN:
            if evt.button==1:
                print(mx,my)
        if evt.type==KEYDOWN:
            if evt.key == K_r and player.powerUp == "fireball":
                if len(player.fireBalls) < 3:
                    player.fireBalls.append(Fireball(player.posInLevel,player.y))

    player.movePlayer()
    player.checkPlayerCollision()
    level.drawLevel()
    player.drawPlayer()

    if player.powerUp != "normal":
        player.usePowerUp(player.powerUp)

    #flipping display and insuring 60fps
    display.flip()
    myClock.tick(60)

l1File.close()

quit()
