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

for i in range(12):
    fname = filedialog.askopenfilename()
    myImg = image.load(fname)
    myImg = transform.flip(myImg, True, False)
    fname = filedialog.asksaveasfilename()
    image.save(myImg, fname)
    print(fname)


# while running:
#     for evt in event.get():
#         if evt.type == QUIT:
#             running = False
#         if evt.type == MOUSEBUTTONDOWN:
#             mixer.music.load("Sound Effects\\smb_kick.wav")
#             mixer.music.play()
#     screen.fill(0)
#     mx,my=mouse.get_pos()
#     mb=mouse.get_pressed()
#     display.flip()
#     myClock.tick(60)
            
quit()
