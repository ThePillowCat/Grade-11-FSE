from pygame import *

init()

class Level():
    def __init__(self, screen, level_data, widthOfTile, heightOfTile, tileDict, screenshots, numOfKeysInLevels):
        self.screen = screen
        self.numOfKeysInLevels = numOfKeysInLevels
        self.levels = [level_data[0][0], level_data[0][1], level_data[0][2]]
        self.objects = [level_data[1][0], level_data[1][1], level_data[1][2]]
        self.rects = [level_data[2][0], level_data[2][1], level_data[2][2]]
        self.enemies = [level_data[3][0], level_data[3][1], level_data[3][2]]
        self.levelLengths = [len(level_data[0][0][0])*widthOfTile, len(level_data[0][1][0])*widthOfTile, len(level_data[0][2][0])*widthOfTile]
        self.screenshots = screenshots
        self.keyLocations = []
        self.tileDict = tileDict
        self.level_data = level_data
        self.widthOfTile = widthOfTile
        self.heightOfTile = heightOfTile
        self.currentLevel = 0
        self.doorFrame = 1
        self.temp = 0
        self.doorOpening = False
        self.doorIsOpen = False
        self.stuffToDrawOverBackground = []
        self.gameOver = False
        self.circleThickness = 1
        self.eggs = []
        self.gameOverFont = font.Font("Textures\\png\\Fonts\\PressStart2P-Regular.ttf", 50).render("Game Over", True, (255,255,255))
    def calcDrawingBounds(self):
        pass
    def drawLevel(self, offset):
        for i in range(len(self.screenshots[self.currentLevel])):
            self.screen.blit(self.screenshots[self.currentLevel][i], (1200*i+offset, 0))
        for it in self.stuffToDrawOverBackground:
            self.screen.blit(self.tileDict[it[0]], (it[1][0]+offset, it[1][1]))
    def playAnimations(self):
        if self.doorOpening:
            #temp represents the door rectangle from the level objects
            X = self.level_data[1][self.currentLevel][self.temp][0]//self.widthOfTile
            Y = self.level_data[1][self.currentLevel][self.temp][1]//self.heightOfTile
            self.levels[self.currentLevel][Y][X] = ["door"+str(int(self.doorFrame))]
            self.stuffToDrawOverBackground.append(["door"+str(int(self.doorFrame)), [self.level_data[1][self.currentLevel][self.temp][0], self.level_data[1][self.currentLevel][self.temp][1]]])
            self.doorFrame+=0.05
            if self.doorFrame >= 4.05:
                self.doorOpening = False
                self.doorIsOpen = True
                self.doorFrame = 1
    def gameOverAnimation(self):
        if self.gameOver:
            draw.circle(self.screen, (0,0,0), (600, 351), 800, self.circleThickness)
            self.circleThickness+=50
            if self.circleThickness == 500:
                self.screen.blit(self.gameOver, (100,100))

    def drawEnemies(self):
        if self.enemies[self.currentLevel] != []:
            for e in self.enemies[self.currentLevel]:
                e.checkCollision()
                e.drawSelf()
            tempLen = len(self.enemies[self.currentLevel])
            for i in range(tempLen-1,-1,-1):
                if self.enemies[self.currentLevel][i].dead:
                    del self.enemies[self.currentLevel][i]