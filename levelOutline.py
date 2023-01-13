from pygame import *

class Level():
    def __init__(self, screen, level_data, widthOfTile, heightOfTile, row, tileDict, screenshots):
        self.screen = screen
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
        self.hasKey = False
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
            self.doorFrame+=0.05
            if self.doorFrame >= 4.05:
                self.doorOpening = False
                self.doorIsOpen = True
                self.doorFrame = 1
            self.stuffToDrawOverBackground.append(["door"+str(int(self.doorFrame)), (self.level_data[1][self.currentLevel][self.temp][0], self.level_data[1][self.currentLevel][self.temp][1])])
            for o in self.stuffToDrawOverBackground:
                if o[0] == "door"+str(int(self.doorFrame)-1):
                    del self.stuffToDrawOverBackground[self.stuffToDrawOverBackground.index(o)]
    def drawEnemies(self):
        if self.enemies[self.currentLevel] != []:
            for e in self.enemies[self.currentLevel]:
                e.drawSelf()
                e.checkCollision()
            tempLen = len(self.enemies[self.currentLevel])
            for i in range(tempLen-1,-1,-1):
                if self.enemies[self.currentLevel][i].dead:
                    del self.enemies[self.currentLevel][i]