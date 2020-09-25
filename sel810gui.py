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
YOFFSET = 259
TRANXOFFSET = 136
TRANYOFFSET = 237
XLAMP = 20
YLAMP = 15
MASKS = (1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768)
tregister = 0
#               R    G    B
WHITE       = (255, 255, 255)
BLACK       = (  0,   0,   0)
BEIGE       = (227, 224, 200)

#LAMP_COUNT      = 85     # Number of lamps

class Toggle3(pygame.sprite.Sprite): #up, neutral, down
    togglevalue = 1
    name = "NONE"
    togtype = 3
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([30, 30])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
    def settoggle(self, value):
        self.togglevalue = value
        self.image.fill(WHITE)
        if self.togglevalue == 2: #down
            pygame.draw.polygon(self.image, BLACK, [(15, 5), (0, 30), (30, 30)])
        if self.togglevalue == 0: #up
            pygame.draw.polygon(self.image, BLACK, [(15, 25), (0, 0), (30, 0)])
        if self.togglevalue == 1: # neutral
            pygame.draw.polygon(self.image, BLACK, [(15, 10), (10, 15), (15, 20)])
        toggles.draw(SELPANEL)
        pygame.display.update()
        

class Toggle2(pygame.sprite.Sprite): #up, neutral, down
    togglevalue = 1
    name = "NONE"
    togtype = 2
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([30, 30])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
    def settoggle(self, value):
        self.togglevalue = value
        self.image.fill(WHITE)
        if self.togglevalue == 2: #down
            pygame.draw.polygon(self.image, BLACK, [(15, 5), (0, 30), (30, 30)])
        if self.togglevalue == 0: #up
            self.togglevalue = 1
        if self.togglevalue == 1: # neutral
            pygame.draw.polygon(self.image, BLACK, [(15, 10), (10, 15), (15, 20)])
        toggles.draw(SELPANEL)
        pygame.display.update()
    


    
    
class Lamp(pygame.sprite.Sprite):
    lampvalue = 0
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
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
    global SELPANEL, toggles, lamplist, lamps, t_hltclr, toggledict, a
    pygame.init()
    SELPANEL = pygame.display.set_mode((XPANELSIZE,YPANELSIZE))
    toggles = pygame.sprite.Group()
    lamps = pygame.sprite.Group()
    pygame.display.set_caption('SEL 810 Emulator')
    lamplist = []
    initlamps()
    print("lamps initialized")
    inittoggles()
    print("toggles initialized")
    a = ControlPanelClient("/tmp/SEL810_control_panel",draw_display)
    a.start()
    print("draw initialized")
    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    clicked_toggle = [s for s in toggles if s.rect.collidepoint(pos)]
                    if len(clicked_toggle) > 0:
                        height = clicked_toggle[0].rect.bottom - clicked_toggle[0].rect.top
                        top = clicked_toggle[0].rect.y
                        print("height",height,"top",top,"clicked",pos[1])
                        if(pos[1] <= top + (height/2)):
                            if clicked_toggle[0].togglevalue == 1:
                                print(clicked_toggle[0].name,"was", clicked_toggle[0].togglevalue," flipping up")
                                clicked_toggle[0].settoggle(0)
                        else:
                            if clicked_toggle[0].togglevalue == 0:
                                print(clicked_toggle[0].name,"was", clicked_toggle[0].togglevalue,"flipping down")
                                clicked_toggle[0].settoggle(1)
                            elif clicked_toggle[0].togglevalue == 1:
                                print(clicked_toggle[0].name,"was neutral, handling toggle")
                                togglehandler(clicked_toggle[0])
                                clicked_toggle[0].settoggle(2)
                                print(tregister)
                if event.type == pygame.MOUSEBUTTONUP:
                    for toggle in toggles:
                        if toggle.togglevalue == 2:
                            toggle.settoggle(1)
                        
                        
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

def inittoggles():
    t_hltclr = Toggle3()
    t_hltclr.name = "hltclr"
    t_hltclr.rect.x = 75
    t_hltclr.rect.y = 430
    toggles.add(t_hltclr)
    
    for transtoggle in range (0,16):
        transfertoggle = Toggle3()
        transfertoggle.name = "trans" + str(transtoggle)
        transfertoggle.rect.x = (transtoggle*XSIZE) + TRANXOFFSET
        transfertoggle.rect.y = TRANYOFFSET + (YSIZE * 6)
        transfertoggle.settoggle(1)
        toggles.add(transfertoggle)

    t_mstrclr = Toggle2()
    t_mstrclr.name = "mstrclr"
    t_mstrclr.rect.x = 715
    t_mstrclr.rect.y = 430
    toggles.add(t_mstrclr)

    t_strtstop = Toggle2()
    t_strtstop.name = "strtstop"
    t_strtstop.rect.x = 75
    t_strtstop.rect.y = 507
    toggles.add(t_strtstop)

    t_step = Toggle2()
    t_step.name = "step"
    t_step.rect.x = 140
    t_step.rect.y = 507
    toggles.add(t_step)
    
    t_iorelease = Toggle2()
    t_iorelease.name = "iorelease"
    t_iorelease.rect.x = 206
    t_iorelease.rect.y = 507
    toggles.add(t_iorelease)
    
    t_intover = Toggle3()
    t_intover.name = "intover"
    t_intover.rect.x = 272
    t_intover.rect.y = 507
    toggles.add(t_intover)
    
    t_memdisp = Toggle3()
    t_memdisp.name = "memdisp"
    t_memdisp.rect.x = 272+66
    t_memdisp.rect.y = 507
    toggles.add(t_memdisp)
             
    t_mementer = Toggle3()
    t_mementer.name = "mementer"
    t_mementer.rect.x = 272+66+33
    t_mementer.rect.y = 507
    toggles.add(t_mementer)
              
    t_memstep = Toggle2()
    t_memstep.name = "memstep"
    t_memstep.rect.x = 272+66+33+33
    t_memstep.rect.y = 507
    toggles.add(t_memstep)
          
    t_setpc = Toggle3()
    t_setpc.name = "setpc"
    t_setpc.rect.x = 272+66+33+33+66
    t_setpc.rect.y = 507
    toggles.add(t_setpc)
           
    t_instr = Toggle2()
    t_instr.name = "instr"
    t_instr.rect.x = 272+99+99+33
    t_instr.rect.y = 507
    toggles.add(t_instr)
           
    t_aacc = Toggle2()
    t_aacc.name = "aacc"
    t_aacc.rect.x = 272+99+99+66
    t_aacc.rect.y = 507
    toggles.add(t_aacc)
          
    t_bacc = Toggle2()
    t_bacc.name = "bacc"
    t_bacc.rect.x = 272+99+99+99
    t_bacc.rect.y = 507
    toggles.add(t_bacc)
          
def togglehandler(clicked_toggle):
#    global tregister, globalpaneldict, a
    updatedict = {}
    if(clicked_toggle.name == "hltclr"):
        tregister = 0
        updatedict.update({"Transfer Register":0})
        a.update_panel(updatedict)
    elif("trans" in clicked_toggle.name):
        number = int(clicked_toggle.name.lstrip("trans"))
        if not(globalpaneldict["Transfer Register"] & MASKS[15-number]):
            tregister = globalpaneldict["Transfer Register"] + MASKS[15-number]
            updatedict.update({"Transfer Register":tregister})
            a.update_panel(updatedict)
    elif(clicked_toggle.name == "mstrclr"):
        tregister = 0
        updatedict.update({"master_clear":True})
        a.update_panel(updatedict)
    elif(clicked_toggle.name == "strtstop"):
        if globalpaneldict["halt"] == True:
#            a.starttog()
            updatedict.update({"halt":False})
        else:
            updatedict.update({"halt":True})
#            globalpaneldict["halt"] = True
        a.update_panel(updatedict)
    elif(clicked_toggle.name == "step"):
        updatedict.update({"step":True})
        a.update_panel(updatedict)
    elif(clicked_toggle.name == "iorelease"):
        tregister = 0
#???
    elif(clicked_toggle.name == "intover"):
        tregister = 0
#???
    elif(clicked_toggle.name == "memdisp"):
        updatedict.update({"display":True})
        a.update_panel(updatedict)
#???        
    elif(clicked_toggle.name == "mementer"):
        updatedict.update({"enter":True})
        a.update_panel(updatedict)
#????
    elif(clicked_toggle.name == "memstep"):
        updatedict.update({"Program Counter":globalpaneldict["Program Counter"] + 1})
        a.update_panel(updatedict)
    elif(clicked_toggle.name == "setpc"):
        updatedict.update({"Program Counter":globalpaneldict["Transfer Register"]})
        a.update_panel(updatedict)
    elif(clicked_toggle.name == "instr"):
        updatedict.update({"Instruction":globalpaneldict["Transfer Register"]})
        a.update_panel(updatedict)
    elif(clicked_toggle.name == "aacc"):
        updatedict.update({"A Register":globalpaneldict["Transfer Register"]})
        a.update_panel(updatedict)
    elif(clicked_toggle.name == "bacc"):
        updatedict.update({"B Register":globalpaneldict["Transfer Register"]})
        a.update_panel(updatedict)
    
    

#draw the board
def draw_display(paneldict):
    global globalpaneldict
    globalpaneldict = paneldict
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    panel = pygame.image.load("SEL_FRONT_PANEL.jpg")
    panel = pygame.transform.scale(panel, (XPANELSIZE,YPANELSIZE))
    SELPANEL.blit(panel, (0, 0))
#TODO add parity and interupt
    if(paneldict["halt"]):
        lamplist[0][0].setlamp(1)
    if not paneldict["parity"]:
        lamplist[1][0].setlamp(1)
    if paneldict["iowait"] :
        lamplist[2][0].setlamp(1)
    if paneldict["Interrupt Register"]:
        lamplist[3][0].setlamp(1)
    if paneldict["overflow"]:
        lamplist[4][0].setlamp(1)
    
    for bit in range(0,16):     
        for register in ((0, "Program Counter"), (1, "Instruction"), (2, "A Register"), (3, "B Register"), (4, "Transfer Register")):
            if(paneldict[register[1]] & MASKS[bit]):
                lamplist[register[0]][16-bit].setlamp(1)
            else:
                lamplist[register[0]][16-bit].setlamp(0)     
    toggles.draw(SELPANEL)
    lamps.draw(SELPANEL)
    pygame.display.update()

if __name__ == '__main__':
    main()
