# SEL 810A EMULATOR GUI

import time, sys
import argparse
import pygame
from pygame.locals import *
from cpuclient import *
import json

#this is what the lamp size values are multiplied by
XPANELSIZE = 830
YPANELSIZE = 540
XSIZE=33;
YSIZE=32;
XOFFSET = 111
YOFFSET = 260
XLAMP = 20
YLAMP = 15
MASKS = (1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768)




#               R    G    B
WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
BLUE        = (  0,   0, 255)
BEIGE       = (227, 224, 200)



LAMP_COUNT      = 85     # Number of lamps

class Toggle(pygame.sprite.Sprite):
    togglevalue = 0
    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([30, 30])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
    def settoggle(self, value):
        self.togglevalue = value
        self.image.fill(WHITE)
        if self.togglevalue == 1:
            pygame.draw.polygon(self.image, BLACK, [(15, 5), (0, 30), (30, 30)])
        if self.togglevalue == 0:
            pygame.draw.polygon(self.image, BLACK, [(15, 25), (0, 0), (30, 0)])
        if self.togglevalue == 2:
            pygame.draw.polygon(self.image, BLACK, [(15, 10), (10, 15), (15, 20)])

class Lamp(pygame.sprite.Sprite):
    lampvalue = 0
    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([XSIZE, YSIZE])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
    def setlamp(self, value):
        self.lampvalue = value
        if self.lampvalue == 1:
            pygame.draw.rect(self.image, (255, 200, 0), (0, 0, XLAMP, YLAMP))
        if self.lampvalue == 0:
            pygame.draw.rect(self.image, (230, 224, 200), (0, 0, XLAMP, YLAMP))
       

def main():
    global SELPANEL, toggle, toggles, lamplist, lamps, t_hltclr

    pygame.init()
    SELPANEL = pygame.display.set_mode((XPANELSIZE,YPANELSIZE))
    toggles = pygame.sprite.Group()
    lamps = pygame.sprite.Group()
    pygame.display.set_caption('SEL 810 Emulator')
    lamplist = []
    initlamps()
    
    t_hltclr = Toggle()
    t_hltclr.rect.x = 75
    t_hltclr.rect.y = 430
    toggles.add(t_hltclr)
    a = ControlPanelClient("/tmp/SEL810_control_panel",draw_display)
    a.start()
    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
    # handle MOUSEBUTTONUP
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    clicked_toggle = [s for s in toggles if s.rect.collidepoint(pos)]
                    if clicked_toggle[0].togglevalue == 0:
                        clicked_toggle[0].settoggle(1)
                        print("was 0 now 1")
                    elif clicked_toggle[0].togglevalue == 1:
                        clicked_toggle[0].settoggle(0)
                        print("was", clicked_toggle[0].togglevalue,"now 0")
                    
    except KeyboardInterrupt:
        sys.exit()



def initlamps():
    for row in range(0,5):
        bitlist = []
        lamplist.append(bitlist)
        for bit in range(0,17):
            lamp = Lamp()
            lamp.setlamp(0)
            lamp.rect.x = (bit*XSIZE)+XOFFSET
            lamp.rect.y = (row*YSIZE)+YOFFSET
            bitlist.append(lamp)
            lamps.add(lamp)




#draw the board
def draw_display(paneldict):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    panel = pygame.image.load("SEL_FRONT_PANEL.jpg")
    panel = pygame.transform.scale(panel, (XPANELSIZE,YPANELSIZE))
    SELPANEL.blit(panel, (0, 0))
    print(paneldict["Program Counter"])

#TODO add parity and interupt
    if(paneldict["halt"]):
        lamplist[0][0].setlamp(1)
    if paneldict["iowait"] :
        lamplist[2][0].setlamp(1)
    if paneldict["overflow"]:
        lamplist[4][0].setlamp(1)
    
    for bit in range(0,16):
        if(paneldict["Program Counter"] & MASKS[bit]):
            lamplist[0][16-bit].setlamp(1)
        else:
            lamplist[0][16-bit].setlamp(0)

        if(paneldict["Instruction"] & MASKS[bit]):
            lamplist[1][16-bit].setlamp(1)
        else:
            lamplist[1][16-bit].setlamp(0) 
            
        if(paneldict["A Register"] & MASKS[bit]):
            lamplist[2][16-bit].setlamp(1)
        else:
            lamplist[2][16-bit].setlamp(0)
            
        if(paneldict["B Register"] & MASKS[bit]):
            lamplist[3][16-bit].setlamp(1)
        else:
            lamplist[3][16-bit].setlamp(0)
#TODO: need T register
        if(43690 & MASKS[bit]):
            lamplist[4][16-bit].setlamp(1)
        else:
            lamplist[4][16-bit].setlamp(0)
            
    toggles.draw(SELPANEL)
    lamps.draw(SELPANEL)
    pygame.display.update()


if __name__ == '__main__':
    main()
