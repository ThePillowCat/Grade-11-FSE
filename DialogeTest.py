from pygame import *
from tkinter import *
from tkinter import filedialog


init()
soundFrame = 5

width,height=800,600
screen=display.set_mode((width,height))
RED=(255,0,0)
GREY=(127,127,127)
BLACK=(0,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
YELLOW=(255,255,0)

running=True

myClock = time.Clock()

# myImg = image.load("Textures\\Png\\Enemies\\PinkSlimeDeadRight.png")
# myImg = transform.flip(myImg, True, False)
# fname = filedialog.asksaveasfilename(defaultextension=".png")
# image.save(myImg, fname)

# while running:
#     screen.fill(0)
#     for evt in event.get():
#         if evt.type==QUIT:
#             running=False
#     if soundFrame > 5:
#         mixer.music.load("Sound Effects\\Retro_Multiple_v1_wav.wav")
#         mixer.music.play()
#         soundFrame = 0
#     soundFrame+=0.14
#     draw.rect(screen, (255,255,255), (30, 370, width-60,200))
#     mx,my=mouse.get_pos()
#     mb=mouse.get_pressed()
#     display.flip()
#     myClock.tick(60)
            
quit()
