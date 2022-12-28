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

#THINGS TO DO IN GAME-----------
#-->Add heart powerup
#-->Fix door
#-->Create dungeon level
#-->Add ammo powerup
#-->Add UI
#Add dog enemy
#Fix any bugs/touchups
#(maybe add speech bubbles)

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
right = len(level_2[0])*widthOfTile
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
                        player.bullets[i].dead = True
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
            if bottomOfPlayer.colliderect(self.hitbox):
                player.vel[1] = -10
                self.dead = True
                mixer.music.load("Sound Effects\\smb_stomp.mp3")
                mixer.music.play()
            elif playerRect.colliderect(self.hitbox):
                player.resetPlayer()
            #Checking if hit by fireball
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
                        player.bullets[i].dead = True
                        mixer.music.load("Sound Effects\\smb_kick.wav")
                        mixer.music.play()
                        self.vel[1] = -10
                        self.playDeathAnimation = True
                        #making sure enemy goes to right during death
                        self.speed = abs(self.speed)

stuffWithNoCollision = [["Tree_1"], ["Tree_2"], [], ["m_m_side_dirt"], ["door1"], ["Bush (1)"], ["Bush (2)"], ["Bush (3)"], ["Bush (4)"]]

#would include stuff like enemies
seperateObjects = [["door1"], ["water"], ["water_top"], ["flag_red"], ["lava"], ["lava_top"]]

#enemies array (contains all the enemies)
enemies = [["BlueSlime1Left"], ["PinkSlime1Left"], ["BlueSlime1Right"], ["PinkSlime1Right"], ["Bat1"]]

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
    "question_fire_flower" : image.load("Textures\\png\\Tiles\\block1.png").convert_alpha(),
    "question_gun" : image.load("Textures\\png\\Tiles\\block1.png").convert_alpha(),
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
    "water_top": image.load("Textures\png\Tiles\water_top.png").convert_alpha(),
    "water": image.load("Textures\png\Tiles\water.png").convert_alpha(),
    "flag_red" : image.load("Textures\png\Object\\flag_red.png"),
    "flag_blue" : image.load("Textures\png\Object\\flag_blue.png"),
    "castle" : image.load("Textures\\png\\Tiles\\castle.png").convert_alpha(),
    "castleCenter" : image.load("Textures\\png\\Tiles\\castleCenter.png").convert_alpha(),
    "castleCliffLeft" : image.load("Textures\\png\\Tiles\\castleCliffLeft.png").convert_alpha(),
    "castleCliffLeftAlt" : image.load("Textures\\png\\Tiles\\castleCliffLeftAlt.png").convert_alpha(),
    "castleCliffRight" : image.load("Textures\\png\\Tiles\\castleCliffRight.png").convert_alpha(),
    "castleCliffRightAlt" : image.load("Textures\\png\\Tiles\\castleCliffRightAlt.png").convert_alpha(),
    "castleLeft" : image.load("Textures\\png\\Tiles\\castleLeft.png").convert_alpha(),
    "castleMid" : image.load("Textures\\png\\Tiles\\castleMid.png").convert_alpha(),
    "castleRight" : image.load("Textures\\png\\Tiles\\castleRight.png").convert_alpha(),
    "lava_top" : image.load("Textures\\png\\Tiles\\lava_top.png").convert_alpha(),
    "lava_bottom" : image.load("Textures\\png\\Tiles\\lava_bottom.png").convert_alpha(),
    "Bat1": image.load("Textures\png\Enemies\Bat1.png").convert_alpha(),
    "gun" : image.load("Textures\png\Tiles\gun.png")
}

idleStates = {
    "normal0" : image.load("Textures\png\Player\\normal.png"),
    "normal1" : image.load("Textures\png\Player\\normal.png"),
    "fireball0" : image.load("Textures\png\Player\\fireball.png"),
    "fireball1" : image.load("Textures\png\Player\\fireball.png"),
    "gun0" : image.load("Textures\png\Player\\gun0.png"),
    "gun1" : image.load("Textures\png\Player\\gun1.png"),
}

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
        elif level_1[i][j] in seperateObjects:
            W = tileDict[level_1[i][j][0]].get_width()
            H = tileDict[level_1[i][j][0]].get_height()
            level_1_Objects.append(Rect(widthOfTile*j, heightOfTile*i, W, H))
        elif level_1[i][j] not in stuffWithNoCollision:
            level_1_Rects.append(Rect(widthOfTile*j, heightOfTile*i, widthOfTile, heightOfTile))

for i in range(row):
    for j in range(len(level_2[0])):
        if level_2[i][j] in enemies:
            W = tileDict[level_2[i][j][0]].get_width()
            H = tileDict[level_2[i][j][0]].get_height()
            offset = 0
            if level_2[i][j] == ["BlueSlime1Right"]:
                offset = 20
                myObj = Slime("BlueSlime1", Rect(widthOfTile*j, heightOfTile*i+offset, W, H), widthOfTile*j, heightOfTile*i+offset) 
                level_2[i][j] = []
                level_2_Enemies.append(myObj)
            if level_2[i][j] == ["PinkSlime1Right"]:
                offset = 20
                myObj = Slime("PinkSlime1", Rect(widthOfTile*j, heightOfTile*i+offset, W, H), widthOfTile*j, heightOfTile*i+offset)
                level_2[i][j] = []
                level_2_Enemies.append(myObj)
            if level_2[i][j] == ["Bat1"]:
                myObj = Bat("Bat", Rect(widthOfTile*j, heightOfTile*i, W, H), widthOfTile*j, heightOfTile*i)
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

bgForest = image.load("Textures\\png\\BG\\BG.png").convert()
bgCave = image.load("Textures\\png\\BG\\CaveBG.png").convert()
fireBall = image.load("Textures\\png\\Object\\fireball.png").convert_alpha()

class Level():
    def __init__(self, screen):
        self.screen = screen
        self.levels = [level_1, level_2, level_3]
        self.objects = [level_1_Objects, level_2_Objects, level_3_Rects]
        self.rects =[level_1_Rects, level_2_Rects, level_3_Rects]
        self.door = [image.load("Textures\\png\\Door\\door" + str(i) + ".png") for i in range(1,5)]
        self.enemies = [level_1_Enemies, level_2_Enemies, level_3_Enemies]
        self.background = [bgForest, bgCave, bgForest]
        self.levelLengths = [len(level_1[0])*widthOfTile, len(level_2[0])*widthOfTile, len(level_3[0])*widthOfTile]
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
        self.animationFrames = [[image.load("Textures\\png\\Player\\Layer "+str(i+j)+".png") for i in range(1, 13)] for j in range(0, 72, 12)]
        self.checkPoint = [100, 50, 0, 0]
        self.jumping = False
        self.moveSpot = 0
        self.direction = 0
        self.powerUp = "normal"
        self.powerUpOffset = 0
        self.fireBalls = []
        self.lives = 3
        self.bullets = []
        self.bulletTimer = 0

    def movePlayer(self):
        #getting keys list
        keys = key.get_pressed()
        self.vel[0] = 0
        self.gravity = 1
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
        if keys[K_SPACE] and self.y+self.size[1] == self.groundY and self.vel[1] <= 2:
            self.vel[1] = self.jumpPower
            self.jumping = True
        #OBJECTS
        if len(level.objects[level.currentLevel]) > 0:
            playerRect = Rect(self.posInLevel, self.y, self.size[0], self.size[1])
            temp = playerRect.collidelist(level.objects[level.currentLevel])
            if temp != -1:
                X = level.objects[level.currentLevel][temp][0]//widthOfTile
                Y = level.objects[level.currentLevel][temp][1]//heightOfTile
                if level.levels[level.currentLevel][Y][X] == ["water"] or level.levels[level.currentLevel][Y][X] == ["water_top"]:
                    self.gravity = 0
                    if keys[K_SPACE]:
                        self.vel[1] = -3
                    else:
                        self.vel[1] = 3
                if level.levels[level.currentLevel][Y][X] == ["fire_flower"]:
                    mixer.music.load("Sound Effects\\smb_powerup.mp3")
                    mixer.music.play()
                    self.powerUp = "fireball"
                    self.powerUpOffset = 4
                    del level.objects[level.currentLevel][temp]
                    level.levels[level.currentLevel][Y][X] = []
                if level.levels[level.currentLevel][Y][X] == ["gun"]:
                    mixer.music.load("Sound Effects\\smb_powerup.mp3")
                    mixer.music.play()
                    self.powerUp = "gun"
                    self.powerUpOffset = 2
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
                    self.posInLevel = 100
                    level.currentLevel+=1
                if level.levels[level.currentLevel][Y][X] == ["flag_red"]:
                    mixer.music.load("Sound Effects\\checkpoint.ogg")
                    mixer.music.play()
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
                    level.objects[level.currentLevel].append(Rect(X*widthOfTile, (Y-3)*heightOfTile, widthOfTile, heightOfTile))
                else:
                    level.levels[level.currentLevel][Y-2][X] = [level.levels[level.currentLevel][Y-1][X][0][9:]]
                    level.objects[level.currentLevel].append(Rect(X*widthOfTile, (Y-2)*heightOfTile, widthOfTile, heightOfTile))
                level.levels[level.currentLevel][Y-1][X] = ["neutral_block"]
                mixer.music.load("Sound Effects\\smb_powerup_appears.mp3")
                mixer.music.play()
        
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
            screen.blit(idleStates[str(self.powerUp)+str(self.direction)], (self.x, self.y))
        else:
            if self.jumping:
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
                bulletRect = Rect(self.bullets[i].x+self.offset, self.bullets[i].y, self.bullets[i].width, self.bullets[i].height)
                draw.ellipse(screen, BROWN, (self.bullets[i].x+self.offset, self.bullets[i].y, self.bullets[i].width, self.bullets[i].height))
                if bulletRect.collidelist(level.rects[level.currentLevel]) != -1 or self.bullets[i].x > level.levelLengths[level.currentLevel]:
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
        # self.powerUp = "normal"
        # self.powerUpOffset = 0

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
    screen.blit(level.background[level.currentLevel], (0,0))
    for evt in event.get():
        if evt.type==QUIT:
            running=False
        if evt.type==KEYDOWN:
            if evt.key == K_r:
                if player.powerUp == "fireball":
                    if len(player.fireBalls) < 3:
                        mixer.music.load("Sound Effects\\smb_fireball.mp3")
                        mixer.music.play()
                        #1 is left
                        #0 is right
                        if player.direction == 0:
                            player.fireBalls.append(Fireball(player.posInLevel+50,player.y))
                        else:
                            player.fireBalls.append(Fireball(player.posInLevel,player.y))
                if player.powerUp == "gun":
                    if len(player.fireBalls) < 10 and player.bulletTimer > 1:
                        mixer.music.load("Sound Effects\\gun_shot.mp3")
                        mixer.music.play()
                        if player.moving:
                            player.bullets.append(Bullet(player.posInLevel,player.y+30))
                        else:
                            player.bullets.append(Bullet(player.posInLevel,player.y+35))
                        player.bulletTimer = 0

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