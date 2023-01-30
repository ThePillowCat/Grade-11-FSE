from pygame import *
from random import *

font.init()
RED=(255,0,0)
GREY=(127,127,127)
BLACK=(0,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
YELLOW=(255,255,0)
WHITE=(255,255,255)

def runTicTacToe(s):
    width,height=650,650
    #display.set_mode((width,height))
    screen=s
    running=True
    Xplayer=image.load("pics/x_forTicTacToe.png") #inizalize the pictures
    Oplayer=image.load("pics/o_forTicTacToe.png")

    places=[[Rect(30,30,180,180),Rect(236,30,180,180),Rect(436,30,180,180)],
            [Rect(30,236,180,180),Rect(236,236,180,180),Rect(436,236,180,180)],
            [Rect(30,436,180,180),Rect(236,436,180,180),Rect(436,436,180,180)]]
            #where the coordinates of each square

    boardState = [["" for i in range(3)] for j in range(3)]
    #this is an empty list right now and used for the results later

    counter = 0

    screen.fill(WHITE)
    thickness=1
    isDrawingAnimation = False
    comicFont=font.SysFont("Comic Sans MS",30) #choose the font and size of text
    winner=[" "] #empty right now used for results
    while running:
        for evt in event.get():
            if evt.type==QUIT:
                running=False
    ##        if evt.type==MOUSEBUTTONDOWN: 
    # #this was the first atempt and then I realised I wanted to do it another way 
    ##            screen.blit(Xplayer,(0,0))
                        
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()


        if not isDrawingAnimation:
            #Lines
            draw.line(screen,BLACK,(225,25),(225,625),10)
            draw.line(screen,BLACK,(425,25),(425,625),10)
            draw.line(screen,BLACK,(25,225),(625,225),10)
            draw.line(screen,BLACK,(25,425),(625,425),10)

            #square coordinates 
        ##    draw.rect(screen,RED,(30,30,180,180)) #I just tested then coordinates
        ##    draw.rect(screen,RED,(236,30,180,180))
        ##    draw.rect(screen,RED,(436,30,180,180))
        ##
        ##    draw.rect(screen,RED,(30,236,180,180))
        ##    draw.rect(screen,RED,(236,236,180,180))
        ##    draw.rect(screen,RED,(436,236,180,180))
        ##
        ##    draw.rect(screen,RED,(30,436,180,180))
        ##    draw.rect(screen,RED,(236,436,180,180))
        ##    draw.rect(screen,RED,(436,436,180,180))

            for y in range(3):  #0,1,2
                for x in range(3):
                    if places[y][x].collidepoint(mx, my):
        ##                draw.rect(screen, GREEN, places[y][x]) #just a test
                        if mb[0]==1 and boardState[y][x] == "":
                            #this means if player clicks square and it is an empty space blit picture
                            screen.blit(Xplayer, places[y][x])
                            boardState[y][x] = "X" # filling the square with an x means it's no longer empty
                            counter += 1 #just so the compter knows when to stop playing
                            while True:
                                if counter == 5:
                                    break
                                j=randint(0,2)#row
                                h=randint(0,2)#collum
                                if places[j][h]!=places[y][x]and boardState[j][h] == "":
                                    #if places is no equals to the player rect and it's empty 
                                    #the computer is able to move there
                                    screen.blit(Oplayer, places[j][h])
                                    boardState[j][h] = "O" #adding o to the list
                                    break
                            if boardState[0][0]==boardState[0][1]==boardState[0][2]: #row 1
                                #this is the logic to find if someone won on the first row
                                if boardState[0][0]=="X":#if they won the screen will be animated to close and say You Win
                                    isDrawingAnimation = True
                                    winner=["You Win!"]
                                if boardState[0][0]=="O":
                                    isDrawingAnimation = True
                                    winner=["You lost! :("]#if they lost we blit You lost sad face

                            if boardState[1][0]==boardState[1][1]==boardState[1][2]:#row 2
                                #this is the logic to find if someone won on the second row
                                if boardState[1][0]=="X":
                                    isDrawingAnimation = True
                                    winner=["You Win!"]
                                if boardState[1][0]=="O":
                                    isDrawingAnimation = True
                                    winner=["You lost! :("]
                                    
                            if boardState[2][0]==boardState[2][1]==boardState[2][2]:#row 3
                                #this is the logic to find if someone won on the third row
                                if boardState[2][0]=="X":
                                    isDrawingAnimation = True
                                    winner=["You Win!"]
                                if boardState[2][0]=="O":
                                    isDrawingAnimation = True
                                    winner=["You lost! :("]
                                    
                            if boardState[0][0]==boardState[1][0]==boardState[2][0]:#collum 1
                                #this is the logic to find if someone won on the first collum
                                if boardState[2][0]=="X":
                                    isDrawingAnimation = True
                                    winner=["You Win!"]
                                if boardState[2][0]=="O":
                                    isDrawingAnimation = True
                                    winner=["You lost! :("]
                                    
                            if boardState[0][1]==boardState[1][1]==boardState[2][1]:#collum 2
                                #this is the logic to find if someone won on the second collum
                                if boardState[2][1]=="X":
                                    isDrawingAnimation = True
                                    winner=["You Win!"]
                                if boardState[2][1]=="O":
                                    isDrawingAnimation = True
                                    winner=["You lost! :("]
    
                            if boardState[0][2]==boardState[1][2]==boardState[2][2]:#collum 3
                                #this is the logic to find if someone won on the third collum
                                if boardState[2][2]=="X":
                                    isDrawingAnimation = True
                                    winner=["You Win!"]
                                if boardState[2][2]=="O":
                                    isDrawingAnimation = True
                                    winner=["You lost! :("]

                            if boardState[0][0]==boardState[1][1]==boardState[2][2]:#diagonal left to right
                                #this is the logic to find if someone won on the diagonal left to right
                                if boardState[2][2]=="X":
                                    isDrawingAnimation = True
                                    winner=["You Win!"]
                                if boardState[2][2]=="O":
                                    isDrawingAnimation = True
                                    winner=["You lost! :("]

                            if boardState[0][2]==boardState[1][1]==boardState[2][0]:#diagonal right to left
                                #this is the logic to find if someone won on the diagonal right to left
                                if boardState[0][2]=="X":
                                    isDrawingAnimation = True
                                    winner=["You Win!"]
                                if boardState[0][2]=="O":
                                    isDrawingAnimation = True
                                    winner=["You lost! :("]
                        if winner == [" "]:#If there is no winner by the end you print You tied
                            winner = ["You tied!"]
                            isDrawingAnimation = True
                            for x in range(3):
                                for y in range(3):
                                    if boardState[x][y] == "":
                                        winner = [" "]
                                        isDrawingAnimation = False
                                        break
        else:
            draw.circle(screen,BLACK,(325,325), 1000, thickness)#drawing a circle bigger than the screen
            thickness+=10#increase the thikness by 10 every time
            win=choice(winner) 
            result=comicFont.render(win,True,WHITE) #show result by drawing text
            screen.blit(result,(325,325))
            #brings the player back to the platformer
            if thickness >= 4000:
                running = False
                if winner == ["You Win!"]:
                    return "winner"
                else:
                    return "not winner"
        display.flip()
    quit()
