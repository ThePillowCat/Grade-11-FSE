from pygame import *

class Player():
    def __init__(self, x, y, screen, level_data, height):
        self.screen = screen
        self.level_data = level_data
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
        self.crouched = True
        self.moveSpot = 0
        self.direction = 0
        self.powerUp = "normal"
        self.powerUpOffset = 0
        self.fireBalls = []
        self.lives = 3
        self.bullets = []
        self.bulletTimer = 0

    def movePlayer(self, currentLevel, widthOfTile, heightOfTile):
        #getting keys list
        keys = key.get_pressed()
        self.vel[0] = 0
        self.gravity = 1
        #checking inputs
        if not self.crouched:
            if keys[K_LEFT]:
                self.vel[0]=-5
                leftOfPlayer = Rect(self.posInLevel+self.vel[0], self.y, 2, self.size[1])
                if leftOfPlayer.collidelist(self.level_data[2][currentLevel]) != -1:
                    self.vel[0]=0
                self.direction = 1
            elif keys[K_RIGHT]:
                self.vel[0]=5
                rightOfPlayer = Rect(self.posInLevel+self.size[0]+self.vel[0], self.y, 1, self.size[1])
                if rightOfPlayer.collidelist(self.level_data[2][currentLevel]) != -1:
                    self.vel[0]=0
                self.direction = 0
            if keys[K_SPACE] and self.y+self.size[1] == self.groundY and self.vel[1] <= 2:
                self.vel[1] = self.jumpPower
                self.jumping = True
        #OBJECTS
        if len(self.level_data[1][currentLevel]) > 0:
            playerRect = Rect(self.posInLevel, self.y, self.size[0], self.size[1])
            temp = playerRect.collidelist(self.level_data[1][currentLevel])
            if temp != -1:
                X = self.level_data[1][currentLevel][temp][0]//widthOfTile
                Y = self.level_data[1][currentLevel][temp][1]//heightOfTile
                if self.level_data[0][currentLevel][Y][X] == ["water"] or self.level_data[0][currentLevel][Y][X] == ["water_top"]:
                    self.gravity = 0
                    if keys[K_SPACE]:
                        self.vel[1] = -3
                    else:
                        self.vel[1] = 3
                if self.level_data[0][currentLevel][Y][X] == ["fire_flower"]:
                    mixer.music.load("Sound Effects\\smb_powerup.mp3")
                    mixer.music.play()
                    self.powerUp = "fireball"
                    self.powerUpOffset = 4
                    ####these lines may cause problems in the future
                    del self.level_data[1][currentLevel][temp]
                    self.level_data[0][currentLevel][Y][X] = []
                if self.level_data[0][currentLevel][Y][X] == ["gun"]:
                    mixer.music.load("Sound Effects\\smb_powerup.mp3")
                    mixer.music.play()
                    self.powerUp = "gun"
                    self.powerUpOffset = 2
                    #REMEMBER THAT LEVEL NEEDS TO TAKE PLAYERS LEVEL LIST
                    del self.level_data[1][currentLevel][temp]
                    self.level_data[0][currentLevel][Y][X] = []
                if self.level_data[0][currentLevel][Y][X] == ["door1"] and keys[K_UP]:
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
                    self.checkPoint = [self.x, self.y, self.offset, self.vel[1]]
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
        if self.x+self.size[0] > 900 and self.posInLevel < level.levelLengths[level.currentLevel]:
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
                bulletRect = Rect(self.bullets[i].x, self.bullets[i].y, self.bullets[i].width, self.bullets[i].height)
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