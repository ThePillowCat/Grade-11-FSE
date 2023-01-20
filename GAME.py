from pygame import *
from math import *
from random import *
import Level_picker
import ticTacToe
import tilesAndIdleStates
import levelOutline

init()

#OUTLINE OF CODE-----------------
#There are 3 levels, each stored in a 2D list
#The levels are read from text files, and are created by the level builder program
#Each grid cell in each level determines what that texture should be
#Each level also has two additional 1D arrays
#The first array has all the rects in the level that the player can collide with (stuff that isn't in "stuffWithNoCollision" array)
#The second array contains rectangles with powerups and eneimes
#To detect collision in these arrays, collidepoint is used as it is optimised for this sort of thing

#open the text files with the 2D lists that have what each tile is (a door, a grass block, etc.)
l1File = open("Levels\\level1.txt","r")
l2File = open("Levels\\level2.txt","r")
l3File = open("Levels\\level3.txt","r")

#open the text files that contain the hitboxes for platforms
l1FileRects = open("Levels\\level1collision.txt","r")
l2FileRects= open("Levels\\level2collision.txt","r")
l3FileRects= open("Levels\\level3collision.txt","r")

#open the text files that contain hitboxes for objects (lava, water, fireflower, etc.)
l1FileCollisionRects = open("Levels\\level1collisionobjects.txt", "r")
l1FileCollisionRects = eval(l1FileCollisionRects.readline().strip())

l2FileCollisionRects = open("Levels\\level2collisionobjects.txt", "r")
l2FileCollisionRects = eval(l2FileCollisionRects.readline().strip())

l3FileCollisionRects = open("Levels\\level3collisionobjects.txt", "r")
l3FileCollisionRects = eval(l3FileCollisionRects.readline().strip())

#store the 2D lists in a variable
level_1 = eval(l1File.readline().strip("\n"))
level_2 = eval(l2File.readline().strip("\n"))
level_3 = eval(l3File.readline().strip("\n"))

#convert the hitboxes stored in the text files into Rect objects
level_1_Rects = eval(l1FileRects.readline().strip("\n"))
for i in range(len(level_1_Rects)):
    level_1_Rects[i] = Rect(level_1_Rects[i][0], level_1_Rects[i][1], level_1_Rects[i][2], level_1_Rects[i][3])
level_2_Rects = eval(l2FileRects.readline().strip("\n"))
for i in range(len(level_2_Rects)):
    level_2_Rects[i] = Rect(level_2_Rects[i][0], level_2_Rects[i][1], level_2_Rects[i][2], level_2_Rects[i][3])
level_3_Rects = eval(l3FileRects.readline().strip("\n"))
for i in range(len(level_3_Rects)):
    level_3_Rects[i] = Rect(level_3_Rects[i][0], level_3_Rects[i][1], level_3_Rects[i][2], level_3_Rects[i][3])

#set the screen
width,height=1200,702
screen=display.set_mode((width,height))

#LEVEL LISTS AND VARIABLES
row = 13
col = 20
widthOfTile = width//col
heightOfTile = height//row

#boundries for scrolling:
level_1_Objects = []
level_1_Enemies = []
level_2_Objects = []
level_2_Enemies = []
level_3_Objects = []
level_3_Enemies = []

numOfKeysInLevels = [0, 0, 0]

#loading font
myFont = font.Font("Textures\\png\\Fonts\\PressStart2P-Regular.ttf", 30)

#base class for eneimies
class Enemy():
    def __init__(self, t, re, x, y):
        self.dead = False
        self.x = x
        self.y = y
        self.hitbox = re
        self.type = t
        self.speed = 5

#bird enemy
class Bird(Enemy):
    def __init__(self, t, re, x, y):
        #inheriting parrent stuff
        Enemy.__init__(self, t, re, x, y)
        self.animationFrames = [[image.load("Textures\\png\\Enemies\\bird"+str(i+j)+".png").convert_alpha() for i in range(1,8)] for j in range(0, 12, 7)]
        self.frame = 1
        self.eggTimer = 0
        self.direction = 0
        self.vel = [0,0]
        self.gravity = 0.5
        self.speed = 5
        self.playDeathAnimation = False
    def drawSelf(self):
        if not self.playDeathAnimation:
            self.eggTimer+=0.05
            #only move if at most 1200 pixels away from player
            if abs(self.x-player.posInLevel) < 1200:
                #makes sure the distance between the bird and the player
                #is large enough so it won't mess up animations
                if (abs(self.x-player.posInLevel)) > 1:
                    if self.x < player.posInLevel:
                        self.direction = 0
                        self.x+=2
                        self.hitbox = self.hitbox.move(2,0)
                    else:
                        self.direction = 1
                        self.x-=2
                        self.hitbox = self.hitbox.move(-2,0)
                #check if bird can lay an egg
                if 0 <= abs(self.x-player.posInLevel) <= 10 and self.eggTimer >= 2 and len(level.eggs) < 5:
                    level.eggs.append(Egg(self.x+20, self.y+50))
                    self.eggTimer = 0
                self.frame+=0.2
                if self.frame >= 7:
                    self.frame = 1
        else:
            #death animation
            self.hitbox = self.hitbox.move(self.speed, self.vel[1])
            self.x = self.hitbox[0]
            self.y = self.hitbox[1]
            self.vel[1]+=self.gravity
            if self.hitbox[1] > height:
                self.dead = True
        #draw the bird
        screen.blit(self.animationFrames[self.direction][int(self.frame)], (self.x+player.offset, self.y))
    def checkCollision(self):
        #checks if the player collides from the top, or if self is collided with bullet or fireball
        if not self.playDeathAnimation:
            playerRect = Rect(player.posInLevel, player.y, player.size[0], player.size[1])
            bottomOfPlayer = Rect(player.posInLevel+5, player.y+player.vel[1]+player.size[1], player.size[0]-10, 1)
            if bottomOfPlayer.colliderect(self.hitbox):
                player.vel[1] = -10
                mixer.music.load("Sound Effects\\smb_stomp.mp3")
                mixer.music.play()
                self.dead = True
            elif playerRect.colliderect(self.hitbox):
                player.resetPlayer()
                self.hitbox = self.hitbox.move(500, 0)
                self.x+=500
            else:
                for i in range(len(player.fireBalls)):
                    fireRect = Rect(player.fireBalls[i].x, player.fireBalls[i].y, player.fireBalls[i].rad*2, player.fireBalls[i].rad*2)
                    if fireRect.colliderect(self.hitbox):
                        mixer.music.load("Sound Effects\\smb_kick.wav")
                        mixer.music.play()
                        player.fireBalls[i].bounces = 4
                        self.vel[1] = -10
                        self.playDeathAnimation = True
                        #making sure enemy goes to right during death
                        self.speed = abs(self.speed)
                for i in range(len(player.bullets)):
                    bullRect = Rect(player.bullets[i].x, player.bullets[i].y, player.bullets[i].width, player.bullets[i].height)
                    if bullRect.colliderect(self.hitbox):
                        mixer.music.load("Sound Effects\\smb_kick.wav")
                        mixer.music.play()
                        self.vel[1] = -10
                        self.playDeathAnimation = True
                        #making sure enemy goes to right during death
                        self.speed = abs(self.speed)

#slime class (works very similar to other enemies)
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
        #draws either its idle state (walking) or its death animation
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
        #The slime enemy moves left and right
        #if it's going near an air tile, it knows to go the other way
        #similar mechanics to goombas in other mario games
        if not self.playDeathAnimation:
            X = self.hitbox[0]//widthOfTile
            Y = self.hitbox[1]//heightOfTile
            if level.levels[level.currentLevel][Y+1][X+1] == [] and self.direction == "Right":
                self.speed*=-1
                self.direction = "Left"
            elif level.levels[level.currentLevel][Y+1][X] == [] and self.direction == "Left":
                self.speed*=-1
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
            else:
                for i in range(len(player.fireBalls)):
                    fireRect = Rect(player.fireBalls[i].x, player.fireBalls[i].y, player.fireBalls[i].rad*2, player.fireBalls[i].rad*2)
                    if fireRect.colliderect(self.hitbox):
                        if "Sq" in self.type:
                            self.type = self.type[0:len(self.type)-2]+"Dead"
                        else:
                            self.type = self.type[0:len(self.type)-1]+"Dead"
                        mixer.music.load("Sound Effects\\smb_kick.wav")
                        mixer.music.play()
                        player.fireBalls[i].bounces = 4
                        self.vel[1] = -10
                        self.playDeathAnimation = True
                        #making sure enemy goes to right during death
                        self.speed = abs(self.speed)
                for i in range(len(player.bullets)):
                    bullRect = Rect(player.bullets[i].x, player.bullets[i].y, player.bullets[i].width, player.bullets[i].height)
                    if bullRect.colliderect(self.hitbox):
                        mixer.music.load("Sound Effects\\smb_kick.wav")
                        mixer.music.play()
                        if "Sq" in self.type:
                            self.type = self.type[0:len(self.type)-2]+"Dead"
                        else:
                            self.type = self.type[0:len(self.type)-1]+"Dead"
                        self.vel[1] = -10
                        self.playDeathAnimation = True
                        #making sure enemy goes to right during death
                        self.speed = abs(self.speed)

#Bat enemy (similar to slime and bird enemies)
class Bat(Enemy):
    def __init__(self, t, re, x, y):
        Enemy.__init__(self, t, re, x, y)
        self.animationFrames = [[image.load("Textures\\png\\Enemies\\Bat"+str(i+j)+".png") for i in range(1,4)] for j in range(0, 6, 3)]
        self.playDeathAnimation = False
        self.vel = [0,0]
        self.gravity = 0.5
        self.speed = 5
        self.direction = 1
        self.curFrame = 0
    def drawSelf(self):
        screen.blit(self.animationFrames[self.direction][int(self.curFrame)], (self.hitbox[0]+player.offset, self.hitbox[1]))
        if self.playDeathAnimation:
            self.hitbox = self.hitbox.move(self.speed, self.vel[1])
            self.vel[1]+=self.gravity
            if self.hitbox[1] > height:
                self.dead = True
                return
        self.curFrame+=0.2
        if self.curFrame > 3:
            self.curFrame = 0
        else:
            if self.hitbox[0] > player.posInLevel:
                self.hitbox =  self.hitbox.move(-2, 0)
                self.direction = 1
            else:
                self.hitbox =  self.hitbox.move(2, 0)
                self.direction = 0
            if self.hitbox[1] < player.y+50:
                self.hitbox =  self.hitbox.move(0, 2)
            else:
                self.hitbox =  self.hitbox.move(0, -2)
    def checkCollision(self):
        if not self.playDeathAnimation:
            bottomOfPlayer = Rect(player.posInLevel+5, player.y+player.vel[1]+player.size[1], player.size[0]-10, 1)
            playerRect = Rect(player.posInLevel, player.y, player.size[0], player.size[1])
            #if stomped on by player
            if bottomOfPlayer.colliderect(self.hitbox):
                player.vel[1] = -10
                self.dead = True
                mixer.music.load("Sound Effects\\smb_stomp.mp3")
                mixer.music.play()
            #if collided with player
            elif playerRect.colliderect(self.hitbox):
                player.resetPlayer()
            else:
                #Checking if hit by fireball
                for i in range(len(player.fireBalls)):
                    fireRect = Rect(player.fireBalls[i].x, player.fireBalls[i].y, player.fireBalls[i].rad*2, player.fireBalls[i].rad*2)
                    if fireRect.colliderect(self.hitbox):
                        mixer.music.load("Sound Effects\\smb_kick.wav")
                        mixer.music.play()
                        player.fireBalls[i].bounces = 4
                        self.vel[1] = -10
                        self.playDeathAnimation = True
                        #making sure enemy goes to right during death
                        self.speed = abs(self.speed)
                #checking if hit by bullet
                for i in range(len(player.bullets)):
                    bullRect = Rect(player.bullets[i].x, player.bullets[i].y, player.bullets[i].width, player.bullets[i].height)
                    if bullRect.colliderect(self.hitbox):
                        mixer.music.load("Sound Effects\\smb_kick.wav")
                        mixer.music.play()
                        self.vel[1] = -10
                        self.playDeathAnimation = True
                        #making sure enemy goes to right during death
                        self.speed = abs(self.speed)

#this is the class for key objects in the level
#the player needs a certain amount of keys to beat a level
class epicKey(Enemy):
    def __init__(self, t, re, x, y):
        #inheriting parrent stuff
        Enemy.__init__(self, t, re, x, y)
        self.origX = x
        self.origY = y
        self.counter =10
        self.moveAmount = 1
    def drawSelf(self):
        self.hitbox = self.hitbox.move(0, sin(self.counter*0.1)*3)
        self.counter+=1
        screen.blit(tileDict[self.type], (self.hitbox[0]+player.offset, self.hitbox[1]))
    def checkCollision(self):
        playerRect = Rect(player.posInLevel, player.y, player.size[0], player.size[1])
        if Rect.colliderect(self.hitbox, playerRect):
            self.dead = True
            level.hasKey = True
            player.numOfKeys+=1

#------------------------------------------------
'''
THIS PART OF THE CODE LOOPS THROUGH EACH LEVEL'S 2D LIST
IT CHECKS WHERE ENEMIES SHOULD BE ADDED, AND WHICH OBJECTS SHOULDN'T HAVE COLLISION
'''
stuffWithNoCollision = [["Tree_1"], ["Tree_2"], [], ["m_m_side_dirt"], ["Bush (1)"], ["Bush (2)"], ["Bush (3)"], ["Bush (4)"]]

seperateObjects = [["door1"], ["flag_red"], ["lava"], ["lava_top"], ["arcade"]]

enemies = [["bird1"],["BlueSlime1Left"], ["PinkSlime1Left"], ["BlueSlime1Right"], ["PinkSlime1Right"], ["Bat1"], ["key_red"]]

stuffToDrawOverBackground = []

#dictionaries with tiles and other states of the player
tileDict = tilesAndIdleStates.tileDict
idleStates = tilesAndIdleStates.idleStates

for i in range(row):
    for j in range(len(level_1[0])):
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
            if level_1[i][j] == ["key_red"]:
                level_1[i][j] = []
                level_1_Enemies.append(epicKey("key_red", Rect(widthOfTile*j, heightOfTile*i, W, H), widthOfTile*j, heightOfTile*i))
                numOfKeysInLevels[0]+=1
        elif level_1[i][j] in seperateObjects:
            # if level_1[i][j] == ["door1"]:
            #     stuffToDrawOverBackground.append(["door1", (j*widthOfTile, i*heightOfTile)])
            W = tileDict[level_1[i][j][0]].get_width()
            H = tileDict[level_1[i][j][0]].get_height()
            level_1_Objects.append(Rect(widthOfTile*j, heightOfTile*i, W, H))

level_1_Objects += l1FileCollisionRects

for i in range(row):
    for j in range(len(level_2[0])):
        if level_2[i][j] in enemies:
            W = tileDict[level_2[i][j][0]].get_width()
            H = tileDict[level_2[i][j][0]].get_height()
            offset = 0
            if level_2[i][j] == ["BlueSlime1Right"]:
                offset = 20
                level_2[i][j] = []
                level_2_Enemies.append(Slime("BlueSlime1", Rect(widthOfTile*j, heightOfTile*i+offset, W, H), widthOfTile*j, heightOfTile*i+offset) )
            if level_2[i][j] == ["PinkSlime1Right"]:
                offset = 20
                level_2[i][j] = []
                level_2_Enemies.append(Slime("PinkSlime1", Rect(widthOfTile*j, heightOfTile*i+offset, W, H), widthOfTile*j, heightOfTile*i+offset))
            if level_2[i][j] == ["Bat1"]:
                level_2[i][j] = []
                level_2_Enemies.append(Bat("Bat", Rect(widthOfTile*j, heightOfTile*i, W, H), widthOfTile*j, heightOfTile*i))
            if level_2[i][j] == ["key_red"]:
                level_2[i][j] = []
                level_2_Enemies.append(epicKey("key_red", Rect(widthOfTile*j, heightOfTile*i, W, H), widthOfTile*j, heightOfTile*i))
                numOfKeysInLevels[1]+=1
        elif level_2[i][j] in seperateObjects:
            W = tileDict[level_2[i][j][0]].get_width()
            H = tileDict[level_2[i][j][0]].get_height()
            level_2_Objects.append(Rect(widthOfTile*j, heightOfTile*i, W, H))

level_2_Objects += l2FileCollisionRects

for i in range(row):
    for j in range(len(level_3[0])):
        if level_3[i][j] in enemies:
            W = tileDict[level_3[i][j][0]].get_width()
            H = tileDict[level_3[i][j][0]].get_height()
            offset = 0
            if level_3[i][j] == ["BlueSlime1Right"]:
                offset = 20
                level_3[i][j] = []
                level_3_Enemies.append(Slime("BlueSlime1", Rect(widthOfTile*j, heightOfTile*i+offset, W, H), widthOfTile*j, heightOfTile*i+offset) )
            if level_3[i][j] == ["PinkSlime1Right"]:
                offset = 20
                level_3[i][j] = []
                level_3_Enemies.append(Slime("PinkSlime1", Rect(widthOfTile*j, heightOfTile*i+offset, W, H), widthOfTile*j, heightOfTile*i+offset))
            if level_3[i][j] == ["key_red"]:
                level_3[i][j] = []
                level_3_Enemies.append(epicKey("key_red", Rect(widthOfTile*j, heightOfTile*i, W, H), widthOfTile*j, heightOfTile*i))
                numOfKeysInLevels[2]+=1
            if level_3[i][j] == ["bird1"]:
                level_3[i][j] = []
                level_3_Enemies.append(Bird("bird1", Rect(widthOfTile*j, heightOfTile*i, W, H), widthOfTile*j, heightOfTile*i))
            if level_3[i][j] == ["Bat1"]:
                level_3[i][j] = []
                level_3_Enemies.append(Bat("Bat", Rect(widthOfTile*j, heightOfTile*i, W, H), widthOfTile*j, heightOfTile*i))
        if level_3[i][j] in seperateObjects:
            W = tileDict[level_3[i][j][0]].get_width()
            H = tileDict[level_3[i][j][0]].get_height()
            level_3_Objects.append(Rect(widthOfTile*j, heightOfTile*i, W, H))

level_3_Objects += l3FileCollisionRects
numOfKeysInLevels[2]+=1

bgForest = image.load("Textures\\png\\BG\\BG.png").convert()
bgCave = image.load("Textures\\png\\BG\\CaveBG.png").convert()
bgDesert = image.load("Textures\\png\\BG\\desertBG.png").convert()

#level class is stored in a seperate py file that is imported
#so, you need to pass in some data when making the level class
#this code isn't the best way to do this, but it works for this game
level_data = [[level_1, level_2, level_3],
              [level_1_Objects, level_2_Objects, level_3_Objects],
              [level_1_Rects, level_2_Rects, level_3_Rects],
              [level_1_Enemies, level_2_Enemies, level_3_Enemies]]

class UI():
    def __init__(self):
        self.startTime = 200
        self.lives = 5
        self.heart = image.load("Textures\\png\\UI\\heart\\heart pixel art 32x32.png").convert_alpha()
        self.timePast = 0
    #ADD PERAMETER FOR THE NUMBER OF REMAINING LIVES
    def drawUI(self):
        for i in range(player.lives, 0, -1):
            screen.blit(self.heart, (15+(i-1)*40,15))
        self.timeLeft = self.startTime - self.timePast//60
        self.timePast+=1
        screen.blit(myFont.render(str(self.timeLeft), BLACK, True), (1100, 15))
        screen.blit(myFont.render(str(player.numOfKeys)+"/"+str(level.numOfKeysInLevels[level.currentLevel]), BLACK, True), (500,15))
        screen.blit(tileDict["key_red"], (600,-5))

fireBall = image.load("Textures\\png\\Object\\fireball.png").convert_alpha()

class Player():
    def __init__(self, x, y, screen):
        self.screen = screen
        self.hitArcadeCoords = [0,0]
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
        self.animationFrames = [[image.load("Textures\\png\\Player\\Layer "+str(i+j)+".png").convert_alpha() for i in range(1, 13)] for j in range(0, 72, 12)]
        self.checkPoint = [100, 50, 0, 0]
        self.bullets = []
        self.fireBalls = []
        self.collidedSquares = []
        self.powerUp = "normal"
        self.jumping = False
        self.crouched = False
        self.swimming = False
        self.moveSpot = 0
        self.direction = 0
        self.powerUpOffset = 0
        self.lives = 5
        self.bulletTimer = 0
        self.numOfKeys = 0
        self.playingTicTacToe = False
    def movePlayer(self):
        global switchLevel
        #getting keys list
        keys = key.get_pressed()
        self.vel[0] = 0
        self.gravity = 1
        #getting which row and tile the player is on (0 indexed)
        X = self.posInLevel//widthOfTile
        Y = self.y//heightOfTile
        if not self.crouched:
            if keys[K_LEFT] and Rect(self.posInLevel-5, self.y, 2, self.size[1]).collidelist(level.rects[level.currentLevel]) == -1:
                self.vel[0]=-5
                self.direction = 1
            elif keys[K_RIGHT] and Rect(self.posInLevel+self.size[0]+5, self.y, 1, self.size[1]).collidelist(level.rects[level.currentLevel]) == -1:
                self.vel[0]=5
                self.direction = 0
            if keys[K_SPACE] and self.y+self.size[1] == self.groundY and self.vel[1] <= 2:
                self.vel[1] = self.jumpPower
                self.jumping = True
        #OBJECTS
        self.swimming = False
        if len(level.objects[level.currentLevel]) > 0:
            playerRect = Rect(self.posInLevel, self.y, self.size[0], self.size[1])
            temp = playerRect.collidelist(level.objects[level.currentLevel])
            if temp != -1:
                #gets the row and collumn the object is on
                X = level.objects[level.currentLevel][temp][0]//widthOfTile
                Y = level.objects[level.currentLevel][temp][1]//heightOfTile
                if level.levels[level.currentLevel][Y][X] == ["water"] or level.levels[level.currentLevel][Y][X] == ["water_top"]:
                    if not self.swimming:
                        self.swimming = True
                    self.gravity = 0
                    if keys[K_SPACE]:
                        self.vel[1] = -3
                    else:
                        self.vel[1] = 3
                elif level.levels[level.currentLevel][Y][X] == ["lava_top"] or level.levels[level.currentLevel][Y][X] == ["lava_bottom"]:
                    self.resetPlayer()
                elif level.levels[level.currentLevel][Y][X] == ["fire_flower"]:
                    powerUpSound = mixer.Sound(("Sound Effects\\smb_powerup.mp3"))
                    powerUpSound.set_volume(0.4)
                    mixer.Channel(2).play(powerUpSound)
                    self.powerUp = "fireball"
                    self.powerUpOffset = 4
                    del level.objects[level.currentLevel][temp]
                    for o in level.stuffToDrawOverBackground:
                        if o[1][0] == X*widthOfTile and o[1][1] == Y*heightOfTile:
                            del level.stuffToDrawOverBackground[level.stuffToDrawOverBackground.index(o)]
                    level.levels[level.currentLevel][Y][X] = []
                elif level.levels[level.currentLevel][Y][X] == ["arcade"] and keys[K_UP]:
                    player.playingTicTacToe = True
                    player.hitArcadeCoords = [X, Y]
                elif level.levels[level.currentLevel][Y][X] == ["gun"]:
                    powerUpSound = mixer.Sound(("Sound Effects\\smb_powerup.mp3"))
                    powerUpSound.set_volume(0.4)
                    mixer.Channel(2).play(powerUpSound)
                    self.powerUp = "gun"
                    self.powerUpOffset = 2
                    del level.objects[level.currentLevel][temp]
                    for o in level.stuffToDrawOverBackground:
                        if o[1][0] == X*widthOfTile and o[1][1] == Y*heightOfTile:
                            del level.stuffToDrawOverBackground[level.stuffToDrawOverBackground.index(o)]
                    level.levels[level.currentLevel][Y][X] = []
                elif level.levels[level.currentLevel][Y][X] == ["door1"] and keys[K_UP]:
                    if player.numOfKeys == level.numOfKeysInLevels[level.currentLevel]:
                        level.doorOpening = True
                        level.doorFrame = 1
                        level.temp = temp
                    else:
                        mixer.music.load("Sound Effects\\locked.mp3")
                        mixer.music.play()
                elif level.levels[level.currentLevel][Y][X] == ["door4"]:
                    player.x = 100
                    player.y = 50
                    self.offset = 0
                    level.doorFrame = 1
                    level.doorOpening = False
                    self.posInLevel = 100
                    if level.currentLevel < 2:
                        level.currentLevel+=1
                    else:
                        # switchLevel = True
                        level.gameOver = True
                        level.won = True
                        gameOver = mixer.Sound("Sound Effects\\smb_world_clear.wav")
                        mixer.Channel(6).play(gameOver)
                    level.stuffToDrawOverBackground = []
                    self.checkPoint = [self.x, self.y, 0, self.vel[1]]
                elif level.levels[level.currentLevel][Y][X] == ["flag_red"]:
                    mixer.music.load("Sound Effects\\checkpoint.ogg")
                    mixer.music.play()
                    level.stuffToDrawOverBackground.append(["flag_blue", (X*widthOfTile, Y*heightOfTile)])
                    level.levels[level.currentLevel][Y][X] = ["flag_blue"]
                    self.checkPoint = [self.x, self.y, self.offset, self.vel[1]]

        self.vel[1]+=self.gravity
        self.x+=self.vel[0]

        #defaults the ground to be the 1
        self.groundY = height

        '''
        Ideas for enemies:
        worm that digs through soil???
        grenade that explodes after 1 bounce
        snake that walks on platform
        '''
        
        bottomOfPlayer = Rect(self.posInLevel, self.y+self.vel[1]+self.size[1], self.size[0], 1)
        hitRect = bottomOfPlayer.collidelist(level.rects[level.currentLevel])
        if hitRect != -1:
            self.jumping = False
            self.groundY = level.rects[level.currentLevel][hitRect][1]
            self.vel[1] = 0
            self.y = self.groundY-player.size[1]
        
        topOfPlayer = Rect(self.posInLevel, self.y+self.vel[1], self.size[0], 1)
        hitRect = topOfPlayer.collidelist(level.rects[level.currentLevel])
        if hitRect != -1:
            self.vel[1] = 0
            Y = self.y//heightOfTile
            X = self.posInLevel//widthOfTile  
            if level.levels[level.currentLevel][Y-1][X] != [] and level.levels[level.currentLevel][Y-1][X][0][:8] == "question":
                if level.levels[level.currentLevel][Y-1][X][0][9:] == "gun":
                    level.levels[level.currentLevel][Y-3][X] = ["gun"]
                    level.stuffToDrawOverBackground.append(["gun", (X*widthOfTile, (Y-3)*heightOfTile)])
                    level.objects[level.currentLevel].append(Rect(X*widthOfTile, (Y-3)*heightOfTile, widthOfTile, heightOfTile))
                else:
                    level.levels[level.currentLevel][Y-2][X] = [level.levels[level.currentLevel][Y-1][X][0][9:]]
                    level.stuffToDrawOverBackground.append([level.levels[level.currentLevel][Y-1][X][0][9:], (X*widthOfTile, (Y-2)*heightOfTile)])
                    level.objects[level.currentLevel].append(Rect(X*widthOfTile, (Y-2)*heightOfTile, widthOfTile, heightOfTile))
                level.levels[level.currentLevel][Y-1][X] = ["neutral_block"]
                level.stuffToDrawOverBackground.append(["neutral_block", (X*widthOfTile, (Y-1)*heightOfTile)])
                powerUpSound = mixer.Sound(("Sound Effects\\smb_powerup_appears.mp3"))
                powerUpSound.set_volume(0.4)
                mixer.Channel(1).play(powerUpSound)
        
        #determines if the player is moving or not
        if self.vel[0] != 0 and self.moving == False:
            self.moving = True
        if self.vel[0] == 0 and self.moving:
            self.moving = False

        #checking if player is in the void
        if self.y >= height:
            self.resetPlayer()

        #updating the yPos of the player
        self.y+=self.vel[1]
        #moving player, adding gravity, updating position variable
        self.posInLevel=self.x+abs(self.offset)

        #checks when the level should be scrolled
        #also check if the player is hitting an enemy
        if self.x+self.size[0] > 900 and self.posInLevel < level.levelLengths[level.currentLevel]-345:
            self.x = 900-self.size[0]
            if self.moving:
                self.offset -= 5
        if self.x < 240 and self.posInLevel > 240:
            self.x = 240
            if self.moving and self.posInLevel > 240:
                self.offset += 5

    def drawPlayer(self):
        if not self.moving:
            if self.powerUp == "gun" and self.crouched:
                screen.blit(idleStates["crouch"+str(self.direction)], (self.x, self.y))
            else:
                screen.blit(idleStates[str(self.powerUp)+str(self.direction)], (self.x, self.y))
        else:
            if self.jumping or self.swimming:
                screen.blit(self.animationFrames[self.direction+self.powerUpOffset][-1], (self.x, self.y))
            else:
                if self.moveSpot > 10:
                    self.moveSpot = 0
                self.moveSpot+=0.6
                screen.blit(self.animationFrames[self.direction+self.powerUpOffset][int(self.moveSpot)], (self.x, self.y))
        self.bulletTimer += 0.02
    def usePowerUp(self, powerUp):
        if powerUp == "fireball":
            for i in range(len(self.fireBalls)):
                screen.blit(fireBall, (self.fireBalls[i].x+self.offset, self.fireBalls[i].y))
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
        if powerUp == "gun":
            for i in range(len(self.bullets)):
                bulletRect = Rect(self.bullets[i].x, self.bullets[i].y, self.bullets[i].width, self.bullets[i].height)
                draw.ellipse(screen, BROWN, (self.bullets[i].x+self.offset, self.bullets[i].y, self.bullets[i].width, self.bullets[i].height))
                if bulletRect.collidelist(level.rects[level.currentLevel]) != -1 or self.bullets[i].x+self.offset+self.bullets[i].width > width or self.bullets[i].x+self.offset < 0:
                    self.bullets[i].dead = True
                self.bullets[i].x+=self.bullets[i].speed
            temp = len(self.bullets)
            for i in range(temp-1, -1, -1):
                if self.bullets[i].dead:
                    del self.bullets[i]
    def resetPlayer(self):
        self.x = self.checkPoint[0]
        self.y = self.checkPoint[1]
        self.vel[1] = self.checkPoint[3]

        self.offset = self.checkPoint[2]
        self.lives-=1
        if self.lives == 0:
            level.gameOver = True
            gameOver = mixer.Sound("Sound Effects\\smb_gameover.mp3")
            mixer.Channel(6).play(gameOver)
        self.powerUp = "normal"
        self.powerUpOffset = 0

player = Player(300,100,screen)

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

#BULLET PROJECTILE
#KEEPS TRACK OF THE BULLETS POSITION ON SCREEN
#AND ITS VELOCITY
class Bullet():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 10
        self.speed = 15
        if player.direction != 0:
            self.speed=-self.speed
        self.dead = False

#EGG PROJECTILE
#KEEPS TRACK OF THE BULLETS POSITION ON SCREEN
#AND ITS VELOCITY
class Egg():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = image.load("Textures\\png\\Object\\egg.png").convert_alpha()
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.hitbox = Rect(self.x, self.y, self.width,self.height)
        self.speed = 5
        self.dead = False

RED=(255,0,0)
GREY=(127,127,127)
BLACK=(0,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
YELLOW=(255,255,0)
BLACK = (0,0,0)
BROWN=(205, 127, 50)
running=True

#THIS LINE NEEDS TO CHANGE
screenshots = [[image.load("Levels\\background\\"+str(i+j)+".png").convert() for i in range(1,6)] for j in range(0, 15, 5)]

#OBJECTS
myClock = time.Clock()
level = levelOutline.Level(screen, level_data, widthOfTile, heightOfTile, tileDict, screenshots, numOfKeysInLevels)
level.stuffToDrawOverBackground += stuffToDrawOverBackground
ui = UI()

paused = False

GREEN=0,255,0
BLACK=0,0,0
WHITE=255,255,255
screen = display.set_mode((width, height))

#instructions pannel
def instructions():
    inst = image.load("pics/Instructions.png")
    inst = transform.smoothscale(inst, screen.get_size())
    screen.blit(inst,(0,0))
    back=image.load("pics/Back.png")
    backRect=Rect(975,10,220,70)
    running=True
    while running:
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
        screen.blit(inst,(0,0))
        screen.blit(back,(975,10))
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False

        if backRect.collidepoint(mx,my)and mb[0]==1:
            running=False
        display.flip()

    return "menu"

#story pannel
def story(): #function when the player clicks story
    running = True
    story = image.load("pics/story.png")
    story = transform.smoothscale(story, screen.get_size())
    screen.blit(story,(0,0))
    back=image.load("pics/Back.png")
    backRect=Rect(975,10,220,70)
    while running:
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
        screen.blit(story,(0,0))
        screen.blit(back,(975,10))
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        if backRect.collidepoint(mx,my)and mb[0]==1:
            running=False
        display.flip()
    return "menu"

#level choosing pannel
def level1():
    global lev
    s, lev = Level_picker.runLevelPicker(screen)
    return s 

#actuall game
def game(lev):
    global screen
    global switchLevel
    switchLevel = False
    running = True
    paused = False
    level.currentLevel = lev*1
    bgMusic = mixer.Sound("Sound Effects\\music"+str(level.currentLevel+1)+".mp3")
    gunShot = mixer.Sound("Sound Effects\\gun_shot.mp3")
    fireBall = mixer.Sound("Sound Effects\\smb_fireball.mp3")
    mixer.Sound.set_volume(bgMusic, 0.3)
    mixer.Sound.set_volume(gunShot, 0.4)
    mixer.Sound.set_volume(fireBall, 0.4)
    mixer.Channel(6).play(bgMusic)
    player.numOfKeys = 0
    while running:
        #screen = display.set_mode((width, height))
        if ui.timeLeft < 0:
            ui.startTime = 200
            ui.timePast = 0
            player.resetPlayer()
        if player.playingTicTacToe:
            mixer.Channel(6).stop()
            screen = display.set_mode((650, 650))
            if ticTacToe.runTicTacToe(screen) == "winner":
                level.enemies[level.currentLevel].append(epicKey("key_red", Rect(player.posInLevel+100, player.y, W, H), player.posInLevel+100, player.y))
                level.levels[level.currentLevel][player.hitArcadeCoords[1]][player.hitArcadeCoords[0]] = []
            screen = display.set_mode((1200, 702))
            player.playingTicTacToe = False
            mixer.Channel(6).play(bgMusic)
        if not paused and not level.gameOver and not mixer.Channel(6).get_busy():
            mixer.Channel(6).play(bgMusic)
        if level.gameOver and not mixer.Channel(6).get_busy():
            return "exit"
        if level.currentLevel != lev or switchLevel:
            mixer.Channel(6).stop()
            return "lev1"
        keys = key.get_pressed()
        for evt in event.get():
            if evt.type==QUIT:
                running=False
                return "exit"
            if evt.type==KEYDOWN:
                if evt.key == K_p:
                    if not paused:
                        paused = True
                        mixer.music.load("Sound Effects\\smb_pause.wav")
                        mixer.music.play()
                        bgMusic.stop()
                    else:
                        paused = False
                #FIRING PROJECTILES
                if evt.key == K_r:
                    if player.powerUp == "fireball":
                        if len(player.fireBalls) < 3:
                            mixer.Channel(1).play(fireBall)
                            #1 is left
                            #0 is right
                            if player.direction == 0:
                                player.fireBalls.append(Fireball(player.posInLevel+50,player.y))
                            else:
                                player.fireBalls.append(Fireball(player.posInLevel,player.y))
                    if player.powerUp == "gun":
                        if len(player.fireBalls) < 10 and player.bulletTimer > 1:
                            mixer.Channel(0).play(gunShot)
                            if player.moving:
                                player.bullets.append(Bullet(player.posInLevel,player.y+30))
                            else:
                                if player.crouched:
                                    player.bullets.append(Bullet(player.posInLevel,player.y+57))
                                else:
                                    player.bullets.append(Bullet(player.posInLevel,player.y+35))
                            player.bulletTimer = 0
        #DRAWING THE SCREEN
        if not paused and not level.gameOver:
            player.movePlayer()
            level.drawLevel(player.offset)
            level.playAnimations()
            level.drawEnemies()
            player.drawPlayer()
            ui.drawUI()

            #code for handling the falling egg
            for e in level.eggs:
                screen.blit(e.img, (e.x+player.offset, e.y))
                if e.hitbox.collidelist(level.rects[level.currentLevel]) != -1:
                    e.dead = True
                if e.hitbox.colliderect(Rect(player.posInLevel, player.y, player.size[0],player.size[1])):
                    e.dead = True
                    player.resetPlayer()
                    break
                e.y+=e.speed
                e.hitbox = e.hitbox.move(0, e.speed)
            temp = len(level.eggs)
            for i in range(temp-1, -1, -1):
                if level.eggs[i].dead:
                    del level.eggs[i]

            if player.powerUp != "normal":
                player.usePowerUp(player.powerUp)
            if keys[K_DOWN] and player.powerUp == "gun":
                player.crouched = True
            else:
                player.crouched = False
        elif level.gameOver:
            level.gameOverAnimation()
        #flipping display and insuring 60fps
        display.flip()
        myClock.tick(60)

#LOADING IMAGES FOR THE MENU
instructionspic=image.load("pics/instructionspic.png")
instructionspicB=image.load("pics/instructionspicB.png")
storypic=image.load("pics/storypic.png")
storypicB=image.load("pics/storypicB.png")
startpic=image.load("pics/startpic.png")
startpicB=image.load("pics/startpicB.png")
bgmenu=image.load("pics/bgmenu.png")

#MENU FUNCTION
def menu():  
    running = True
    playingClickSound = False
    myClock = time.Clock()
    buttons=[Rect(600,400,363,151),Rect(600,300,252,87),Rect(900,300,155,80)]#creating the buttons
    while running:
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
            if playingClickSound:
                mixer.music.load("Sound Effects\\click.mp3")
                mixer.music.play()
                playingClickSound = False
            if mb[0]==1:
                    return "lev1"
        elif buttons[1].collidepoint(mx,my):
            draw.rect(screen,WHITE,(600,300,252,87))
            screen.blit(instructionspicB,(595,295))
            if playingClickSound:
                mixer.music.load("Sound Effects\\click.mp3")
                mixer.music.play()
                playingClickSound = False
            if mb[0]==1:
                return "instructions"
        elif buttons[2].collidepoint(mx,my):
            draw.rect(screen,WHITE,(900,300,173,80))
            screen.blit(storypicB,(895,295))
            if playingClickSound:
                mixer.music.load("Sound Effects\\click.mp3")
                mixer.music.play()
                playingClickSound = False
            if mb[0]==1:
                return "story"
        else:
            playingClickSound = True
                       
        display.flip()
        myClock.tick(60)

#MAIN LOOP THAT HANDLES ALL THE MENUS
#THIS IS TAKEN FROM THE MENU TEMPLATE PROGRAM
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
    if page == "game":
        page = game(lev)
  
quit()
