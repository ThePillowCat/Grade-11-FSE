from pygame import *
from random import *

width,height=650,650
screen=display.set_mode((width,height))
RED=(255,0,0)
GREY=(127,127,127)
BLACK=(0,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
YELLOW=(255,255,0)
WHITE=(255,255,255)

running=True

Xplayer=image.load("pics/x_forTicTacToe.png")
Oplayer=image.load("pics/o_forTicTacToe.png")

places=[[Rect(30,30,180,180),Rect(236,30,180,180),Rect(436,30,180,180)],
        [Rect(30,236,180,180),Rect(236,236,180,180),Rect(436,236,180,180)],
        [Rect(30,436,180,180),Rect(236,436,180,180),Rect(436,436,180,180)]]

boardState = [["" for i in range(3)] for j in range(3)]

counter = 0

screen.fill(WHITE)
thickness=1
isDrawingAnimation = False

while running:
    for evt in event.get():
        if evt.type==QUIT:
            running=False
##        if evt.type==MOUSEBUTTONDOWN:
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
    ##    draw.rect(screen,RED,(30,30,180,180))
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
    ##                draw.rect(screen, GREEN, places[y][x])
                    if mb[0]==1 and boardState[y][x] == "":
                        screen.blit(Xplayer, places[y][x])
                        boardState[y][x] = "X"
                        counter += 1
                        while True:
                            if counter == 5:
                                break
                            j=randint(0,2)#row
                            h=randint(0,2)
                            if places[j][h]!=places[y][x]and boardState[j][h] == "":
                                screen.blit(Oplayer, places[j][h])
                                boardState[j][h] = "O"
                                break
                        if boardState[0][0]==boardState[0][1]==boardState[0][2]: #row 1
                            if boardState[0][0]=="X" or boardState[0][0]=="O":
                                isDrawingAnimation = True

                        if boardState[1][0]==boardState[1][1]==boardState[1][2]:#row 2
                            if boardState[1][0]=="X" or boardState[1][0]=="O":
                                isDrawingAnimation = True
                                
                        if boardState[2][0]==boardState[2][1]==boardState[2][2]:#row 3
                            if boardState[2][0]=="X" or boardState[2][0]=="O":
                                isDrawingAnimation = True
                                
                        if boardState[0][0]==boardState[1][0]==boardState[2][0]:#collum 1
                            if boardState[2][0]=="X" or boardState[2][0]=="O":
                                isDrawingAnimation = True
                                
                        if boardState[0][1]==boardState[1][1]==boardState[2][1]:#collum 2
                            if boardState[2][1]=="X" or boardState[2][1]=="O":
                                isDrawingAnimation = True
  
                        if boardState[0][2]==boardState[1][2]==boardState[2][2]:#collum 3
                            if boardState[2][2]=="X" or boardState[2][2]=="O":
                                isDrawingAnimation = True

                        if boardState[0][0]==boardState[1][1]==boardState[2][2]:#diagonal left to right
                            if boardState[2][2]=="X" or boardState[2][2]=="O":
                                isDrawingAnimation = True

                        if boardState[0][2]==boardState[1][1]==boardState[2][0]:#diagonal right to left
                            if boardState[0][2]=="X" or boardState[0][2]=="O":
                                isDrawingAnimation = True
    else:
        draw.circle(screen,BLACK,(325,325), 1000, thickness)
        thickness+=10
        #brings the player back to the platformer
        if thickness == 1000:
            pass
                                
    
                    
                    
        
      
   
    display.flip()
            
quit()
