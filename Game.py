from pygame import *

init()

#OUTLINE OF CODE-----------------
#There are 3 levels, each stored in a 2D list
#The levels are read from text files, and are created by the level builder program
#Each grid cell in each level determines what that texture should be
#Each level also has two additional 1D arrays
#The first array has all the rects in the level that the player can collide with (stuff that isn't in "stuffWithNoCollision" array)
#The second array contains rectangles with powerups and eneimes
#To detect collision in these arrays, collidepoint is used as it is optimised for this sort of thing

l1File = open("Levels\\level1.txt","r")
l2File = open("Levels\\level2.txt","r")
l3File = open("Levels\\level3.txt","r")

level_1 = eval(l1File.readline().strip("\n"))
level_2 = eval(l2File.readline().strip("\n"))
level_3 = eval(l3File.readline().strip("\n"))

width,height=1200,703
screen=display.set_mode((width,height))

#LEVEL LISTS AND VARIABLES
row = 13
col = 20
widthOfTile = width//col
heightOfTile = height//row

#boundries for scrolling:
lenOfLevel = len(level_1[0])
right = lenOfLevel*widthOfTile-591

level_1_Rects = []
level_1_Objects = []
level_1_Enemies = []
level_2_Rects = []
level_2_Objects = []
level_2_Enemies = []
level_3_Rects = []
level_3_Objects = []
level_3_Enemies = []

#POSSIBLE SOURCE OF BUGS:
#LEN OF LEVEL
#ANOTHER IDEA:
#HAVE ENEMIES IN THEIR OWN ARRAY

class Enemy():
    def __init__(self, t, re, x, y):
        self.dead = False
        self.x = x
        self.y = y
        self.hitbox = re
        self.type = t
        self.speed = 5
    def fireBallDeath(self):
        pass

class Slime(Enemy):
    def __init__(self, t, re, x, y):
        #inheriting parrent stuff
        Enemy.__init__(self, t, re, x, y)
        self.vel = [0,0]
        self.gravity = 0.5
        self.speed = 5
        self.direction = "Right"
        self.playDeathAnimation = False
    def drawSelf(self):
        screen.blit(tileDict[self.type+self.direction], (self.hitbox[0]+player.offset, self.hitbox[1]))
        if self.playDeathAnimation:
            self.hitbox = self.hitbox.move(self.speed, self.vel[1])
            self.vel[1]+=self.gravity
            if self.hitbox[1] > height:
                self.dead = True
                return
        else:
            self.hitbox = self.hitbox.move(self.speed,0)
    def checkCollision(self):
        if not self.playDeathAnimation:
            X = self.hitbox[0]//widthOfTile
            Y = self.hitbox[1]//heightOfTile
            if level.levels[level.currentLevel][Y+1][X] == [] or level.levels[level.currentLevel][Y+1][X+1] == []:
                self.speed*=-1
                if self.direction == "Right":
                    self.direction = "Left"
                else:
                    self.direction = "Right"
            bottomOfPlayer = Rect(player.posInLevel+5, player.y+player.vel[1]+player.size[1], player.size[0]-10, 1)
            playerRect = Rect(player.posInLevel, player.y, player.size[0], player.size[1])
            if bottomOfPlayer.colliderect(self.hitbox):
                player.vel[1] = -10
                mixer.music.load("Sound Effects\\smb_stomp.mp3")
                mixer.music.play()
                if "Sq" in self.type:
                    self.dead = True
                else:
                    self.type = self.type[0:len(self.type)-1]+"Sq"
                    self.hitbox = Rect(self.hitbox[0], self.hitbox[1]+22, self.hitbox[2], self.hitbox[3])
            elif playerRect.colliderect(self.hitbox):
                player.resetPlayer()
            #Checking if hit by fireball
            else:
                for i in range(len(player.fireBalls)):
                    fireRect = Rect(player.fireBalls[i].x, player.fireBalls[i].y, player.fireBalls[i].rad*2, player.fireBalls[i].rad*2)
                    if fireRect.colliderect(self.hitbox):
                        self.type = self.type[0:len(self.type)-1]+"Dead"
                        player.fireBalls[i].bounces = 4
                        self.vel[1] = -10
                        self.playDeathAnimation = True
                        #making sure enemy goes to right during death
                        self.speed = abs(self.speed)

stuffWithNoCollision = [["Tree_1"], ["Tree_2"], [], ["m_m_side_dirt"], ["door1"], ["bush (1)"], ["bush (2)"], ["bush (3)"], ["bush (4)"]]

#would include stuff like enemies
seperateObjects = [["door1"]]

#enemies array (contains all the enemies)
enemies = [["BlueSlime1Left"], ["PinkSlime1Left"], ["BlueSlime1Right"], ["PinkSlime1Right"]]

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

for i in range(row):
    for j in range(lenOfLevel):
        if level_1[i][j] in enemies:
            W = tileDict[level_1[i][j][0]].get_width()
            H = tileDict[level_1[i][j][0]].get_height()
            offset = 0
            if level_1[i][j] == ["BlueSlime1Right"]:
                offset = 20
                myObj = Slime("BlueSlime1", Rect(widthOfTile*j, heightOfTile*i+offset, W, H), widthOfTile*j, heightOfTile*i+offset) 
                level_1[i][j] = []
                level_1_Enemies.append(myObj)
            if level_1[i][j] == ["PinkSlime1Right"]:
                offset = 20
                myObj = Slime("PinkSlime1", Rect(widthOfTile*j, heightOfTile*i+offset, W, H), widthOfTile*j, heightOfTile*i+offset)
                level_1[i][j] = []
                level_1_Enemies.append(myObj)
        elif level_1[i][j] in seperateObjects:
            W = tileDict[level_1[i][j][0]].get_width()
            H = tileDict[level_1[i][j][0]].get_height()
            level_1_Objects.append(Rect(widthOfTile*j, heightOfTile*i, W, H))
        elif level_1[i][j] not in stuffWithNoCollision:
            level_1_Rects.append(Rect(widthOfTile*j, heightOfTile*i, widthOfTile, heightOfTile))

for i in range(row):
    for j in range(len(level_2[0])):
        if level_2[i][j] in enemies:
            W = tileDict[level_1[i][j][0]].get_width()
            H = tileDict[level_1[i][j][0]].get_height()
            offset = 0
            if level_2[i][j] == ["BlueSlime1"]:
                offset = 20
                myObj = Slime("BlueSlime1", Rect(widthOfTile*j, heightOfTile*i+offset, W, H), widthOfTile*j, heightOfTile*i+offset) 
                level_2[i][j] = []
            if level_2[i][j] == ["PinkSlime1"]:
                offset = 20
                myObj = Slime("PinkSlime1", Rect(widthOfTile*j, heightOfTile*i+offset, W, H), widthOfTile*j, heightOfTile*i+offset)
                level_2[i][j] = []
            level_2_Enemies.append(myObj)
        elif level_2[i][j] in seperateObjects:
            W = tileDict[level_2[i][j][0]].get_width()
            H = tileDict[level_2[i][j][0]].get_height()
            level_2_Objects.append(Rect(widthOfTile*j, heightOfTile*i, W, H))
        elif level_2[i][j] not in stuffWithNoCollision:
            level_2_Rects.append(Rect(widthOfTile*j, heightOfTile*i, widthOfTile, heightOfTile))

for i in range(row):
    for j in range(len(level_3[0])):
        if level_3[i][j] in enemies:
            W = tileDict[level_1[i][j][0]].get_width()
            H = tileDict[level_1[i][j][0]].get_height()
            offset = 0
            if level_3[i][j] == ["BlueSlime1Left"]:
                offset = 20
                myObj = Slime("BlueSlime1Left", Rect(widthOfTile*j, heightOfTile*i+offset, W, H), widthOfTile*j, heightOfTile*i+offset) 
                level_3[i][j] = []
            if level_3[i][j] == ["PinkSlime1Left"]:
                offset = 20
                myObj = Slime("PinkSlime1Left", Rect(widthOfTile*j, heightOfTile*i+offset, W, H), widthOfTile*j, heightOfTile*i+offset)
                level_3[i][j] = []
            level_3_Enemies.append(myObj)
        elif level_3[i][j] in seperateObjects:
            W = tileDict[level_3[i][j][0]].get_width()
            H = tileDict[level_3[i][j][0]].get_height()
            level_3_Objects.append(Rect(widthOfTile*j, heightOfTile*i, W, H))
        elif level_3[i][j] not in stuffWithNoCollision:
            level_3_Rects.append(Rect(widthOfTile*j, heightOfTile*i, widthOfTile, heightOfTile))

class UI():
    def __init__(self):
        self.timeLeft = 200


class Level():
    def __init__(self, screen):
        self.screen = screen
        self.levels = [level_1, level_2, level_3]
        self.objects = [level_1_Objects, level_2_Objects, level_3_Rects]
        self.rects =[level_1_Rects, level_2_Rects, level_3_Rects]
        self.door = [image.load("Textures\\png\\Door\\door" + str(i) + ".png") for i in range(1,5)]
        self.enemies = [level_1_Enemies, level_2_Enemies, level_3_Enemies]
        self.currentLevel = 0
        self.doorFrame = 1
        self.doorOpening = False
        self.temp = 0
        self.doorIsOpen = False
    def drawLevel(self):
        for i in range(row):
            for j in range(lower, upper):
                if self.levels[self.currentLevel][i][j] != []:
                    screen.blit(tileDict[self.levels[self.currentLevel][i][j][0]], (widthOfTile*j+player.offset, heightOfTile*i))
    def playAnimations(self):
        if self.doorOpening:
            X = level.objects[level.currentLevel][self.temp][0]//widthOfTile
            Y = level.objects[level.currentLevel][self.temp][1]//heightOfTile
            self.levels[level.currentLevel][Y][X] = ["door"+str(int(level.doorFrame))]
            self.doorFrame+=0.05
            if level.doorFrame >= 5:
                self.doorOpening = False
                self.doorIsOpen = True
    def drawEnemies(self):
        for e in self.enemies[self.currentLevel]:
            e.drawSelf()
            e.checkCollision()
        tempLen = len(self.enemies[self.currentLevel])
        for i in range(tempLen-1,-1,-1):
            if self.enemies[self.currentLevel][i].dead:
                del self.enemies[self.currentLevel][i]
            
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
        self.powerUp = "normal"
        self.fireBalls = []
        self.lives = 3

    def movePlayer(self):
        #getting keys list
        keys = key.get_pressed()
        self.vel[0] = 0
        self.vel[1]+=self.gravity
        #checking inputs
        if keys[K_LEFT]:
            self.vel[0]=-5
            leftOfPlayer = Rect(self.posInLevel+self.vel[0], self.y, 2, self.size[1])
            if leftOfPlayer.collidelist(level.rects[level.currentLevel]) != -1:
                self.vel[0]=0
            self.direction = 1
        elif keys[K_RIGHT]:
            self.vel[0]=5
            rightOfPlayer = Rect(self.posInLevel+self.size[0]+self.vel[0], self.y, 1, self.size[1])
            if rightOfPlayer.collidelist(level.rects[level.currentLevel]) != -1:
                self.vel[0]=0
            self.direction = 0
        if keys[K_SPACE] and self.y+self.size[1] == self.groundY and self.vel[1] <= 1:
            self.vel[1] = self.jumpPower

        self.x+=self.vel[0]

        #defaults the ground to be the 1
        self.groundY = height
        '''
        Ideas for enemies:
        worm that digs through soil???
        snake that walks on platform
        '''
        
        bottomOfPlayer = Rect(self.posInLevel, self.y+self.vel[1]+self.size[1], self.size[0], 1)
        hitRect = bottomOfPlayer.collidelist(level.rects[level.currentLevel])
        if hitRect != -1:
            self.groundY = level.rects[level.currentLevel][hitRect][1]
            self.vel[1] = 0
            self.y = self.groundY-player.size[1]
        
        topOfPlayer = Rect(self.posInLevel, self.y+self.vel[1], self.size[0], 1)
        hitRect = topOfPlayer.collidelist(level.rects[level.currentLevel])
        if hitRect != -1:
            self.vel[1] = 0
            Y = self.y//heightOfTile
            X = self.posInLevel//widthOfTile
            if level.levels[level.currentLevel][Y-1][X] == ["question"]:
                level.levels[level.currentLevel][Y-1][X] = ["neutral_block"]
                level.levels[level.currentLevel][Y-2][X] = ["fire_flower"]
                level.objects[level.currentLevel].append(Rect(X*widthOfTile, (Y-2)*heightOfTile, widthOfTile, heightOfTile))
                mixer.music.load("Sound Effects\\smb_powerup_appears.mp3")
                mixer.music.play()
        #OBJECTS
        if len(level.objects[level.currentLevel]) > 0:
            playerRect = Rect(self.posInLevel, self.y, self.size[0], self.size[1])
            temp = playerRect.collidelist(level.objects[level.currentLevel])
            if temp != -1:
                X = level.objects[level.currentLevel][temp][0]//widthOfTile
                Y = level.objects[level.currentLevel][temp][1]//heightOfTile
                if level.levels[level.currentLevel][Y][X] == ["fire_flower"]:
                    mixer.music.load("Sound Effects\\smb_powerup.mp3")
                    mixer.music.play()
                    self.powerUp = "fireball"
                    del level.objects[level.currentLevel][temp]
                    level.levels[level.currentLevel][Y][X] = []
                if level.levels[level.currentLevel][Y][X] == ["door1"] and keys[K_UP]:
                    level.doorOpening = True
                    level.doorFrame = 1
                    level.temp = temp
                if level.levels[level.currentLevel][Y][X] == ["door4"]:
                    player.x = 100
                    player.y = 50
                    self.offset = 0
                    level.doorFrame = 1
                    level.doorOpening = False
                    self.posInLevel = 50
                    level.currentLevel+=1
        
        #determines if the player is moving or not
        if self.vel[0] != 0 and self.moving == False:
            self.moving = True
        if self.vel[0] == 0 and self.moving:
            self.moving = False

        #checking if player is in the void
        if self.y+self.size[1] >= height:
            self.resetPlayer()

        #updating the yPos of the player
        self.y+=self.vel[1]
        #moving player, adding gravity, updating position variable
        self.posInLevel=self.x+abs(self.offset)
    
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
                #fix speed?
                bottomOfFireball = Rect(self.fireBalls[i].x+5, self.fireBalls[i].y+(self.fireBalls[i].rad*2+self.fireBalls[i].vel[1]), (self.fireBalls[i].rad*2)-10, 5)
                rightOfFireball = Rect(self.fireBalls[i].x+(self.fireBalls[i].rad*2)+self.fireBalls[i].speed, self.fireBalls[i].y+5, 1, (self.fireBalls[i].rad*2)-10)
                leftOfFireball = Rect(self.fireBalls[i].x+5+self.fireBalls[i].speed, self.fireBalls[i].y, 1, (self.fireBalls[i].rad*2)-10)
                #deletes fireball if it's in the void (at bottom of screen)
                if self.fireBalls[i].y+self.fireBalls[i].rad > height:
                    self.fireBalls[i].bounces = 4
                    continue
                hitRect = bottomOfFireball.collidelist(level.rects[level.currentLevel])
                if hitRect != -1:
                    self.fireBalls[i].vel[1]=-8
                    self.fireBalls[i].bounces+=1
                    self.fireBalls[i].y = level.rects[level.currentLevel][hitRect][1]-self.fireBalls[i].rad
                elif rightOfFireball.collidelist(level.rects[level.currentLevel]) != -1:
                    self.fireBalls[i].bounces = 4
                    continue
                elif leftOfFireball.collidelist(level.rects[level.currentLevel]) != -1:
                    self.fireBalls[i].bounces = 4
                    continue
                #increasing gravity, updating x and y based off velocites
                self.fireBalls[i].vel[1]+=self.fireBalls[i].gravity
                self.fireBalls[i].y+=self.fireBalls[i].vel[1]
                self.fireBalls[i].x+=self.fireBalls[i].speed
            temp = len(self.fireBalls)
            for i in range(temp-1,-1,-1):
                if self.fireBalls[i].bounces > 3:
                    del self.fireBalls[i]
    def resetPlayer(self):
        self.x = 100
        self.y = 50
        self.offset = 0
        self.lives-=1
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
ui = UI()

bgForest = image.load("Textures\\png\\BG\\BG.png").convert()

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
        if evt.type==KEYDOWN:
            if evt.key == K_r and player.powerUp == "fireball":
                if len(player.fireBalls) < 3:
                    mixer.music.load("Sound Effects\\smb_fireball.mp3")
                    mixer.music.play()
                    player.fireBalls.append(Fireball(player.posInLevel,player.y))

    player.movePlayer()
    player.checkPlayerCollision()
    level.drawEnemies()
    level.drawLevel()
    level.playAnimations()
    player.drawPlayer()

    if player.powerUp != "normal":
        player.usePowerUp(player.powerUp)

    #flipping display and insuring 60fps
    display.flip()
    myClock.tick(60)

l1File.close()

quit()