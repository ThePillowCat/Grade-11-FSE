from pygame import *

class Level():
    def __init__(self, screen, level_data, widthOfTile, heightOfTile, row, tileDict):
        self.screen = screen
        self.levels = [level_data[0][0], level_data[0][1], level_data[0][2]]
        self.objects = [level_data[1][0], level_data[2][0], level_data[3][0]]
        self.rects =[level_data[2][0], level_data[2][1], level_data[2][2]]
        self.enemies = [level_data[3][0], level_data[3][1], level_data[3][2]]
        self.background = [level_data[4][0], level_data[4][1], level_data[4][2]]
        self.levelLengths = [len(level_data[0][0][0])*widthOfTile, len(level_data[0][1][0])*widthOfTile, len(level_data[0][2][0])*widthOfTile]
        self.tileDict = tileDict
        self.level_data = level_data
        self.widthOfTile = widthOfTile
        self.heightOfTile = heightOfTile
        self.currentLevel = 0
        self.doorFrame = 1
        self.temp = 0
        self.doorOpening = False
        self.doorIsOpen = False
    def calcDrawingBounds(self):
        pass
    def drawLevel(self, row, lower, upper, widthOfTile, offset, heightOfTile):
        for i in range(row):
            for j in range(lower, upper):
                if self.levels[self.currentLevel][i][j] != []:
                    self.screen.blit(self.tileDict[self.levels[self.currentLevel][i][j][0]], (widthOfTile*j+offset, heightOfTile*i))
    def playAnimations(self):
        if self.doorOpening:
            #temp represents the door rectangle from the level objects
            X = self.level_data[1][self.currentLevel][self.temp][0]//self.widthOfTile
            Y = self.level_data[1][self.currentLevel][self.temp][1]//self.heightOfTile
            self.levels[self.currentLevel][Y][X] = ["door"+str(int(self.doorFrame))]
            self.doorFrame+=0.05
            if self.doorFrame >= 5:
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