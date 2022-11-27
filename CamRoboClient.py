#!/usr/bin/python
#######################################
# CamRobo Remote Control Client
#######################################
import logging
import socket
import pygame
from pygame.locals import *
import time

CAMROBO_ADDR = "192.168.0.2"
CAMROBO_PORT = 8080

PAD_BUTTON_B         =  0
PAD_BUTTON_A         =  1
PAD_BUTTON_Y         =  2
PAD_BUTTON_X         =  3
PAD_BUTTON_L1        =  4
PAD_BUTTON_R1        =  5
PAD_BUTTON_SELECT    =  6
PAD_BUTTON_START     =  7
PAD_BUTTON_HART      =  8
PAD_BUTTON_JOY_LEFT  =  9
PAD_BUTTON_JOY_RIGHT = 10
PAD_HAT = 0
PAD_AXIS_LEFT_HORIZONTAL  = 0
PAD_AXIS_LEFT_VERTICAL    = 1
PAD_AXIS_L2               = 2
PAD_AXIS_RIGHT_HORIZONTAL = 3
PAD_AXIS_RIGHT_VERTICAL   = 4
PAD_AXIS_R2               = 5

def motor_map(value):
    raw_min = -1.0001
    raw_max =  1
    pwm_min = -65534 /3
    pwm_max =  65534 /3
    return int((( value - raw_min)/(raw_max - raw_min)*(pwm_max - pwm_min)) + pwm_min)

class ListSelector():
    def __init__(self, pygame, screen, pos_x=10,pos_y=10, font_margin=10,font_size=50,bgcolor=(234,234,234),items=None):
        self.pygame = pygame
        self.screen = screen
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.font_size = font_size
        self.font_margin = font_margin
        self.font_offset = 30
        self.font_pointer_char = ">"
        self.pointer = 0
        self.items = None
        self.bgcolor = bgcolor
        self.items = items

    def show(self):
        listbox_width  = self.font_size * len(max(self.items,key=len))/1.5 + self.font_margin + self.font_offset
        listbox_height = (self.font_size + self.font_offset * 2) * len(self.items)/1.75
        self.pygame.draw.rect(self.screen, self.bgcolor, (self.pos_x, self.pos_y, self.pos_x + listbox_width, self.pos_y + listbox_height))
        self.pygame.draw.rect(self.screen, (0,0,0),(self.pos_x, self.pos_y, self.pos_x + listbox_width, self.pos_y + listbox_height),3)
        font  = self.pygame.font.SysFont("notosansmono",self.font_size)
        for i in range(len(self.items)):
            text = font.render(self.items[i], True, (0,0,0))
            self.screen.blit(text,[self.pos_x + self.font_margin + self.font_offset, self.pos_y + self.font_margin + self.font_size * i])
        text = font.render(self.font_pointer_char, True, (0,0,0))
        self.screen.blit(text,[self.pos_x + self.font_margin + self.font_offset / 6, self.pos_y + self.font_margin + self.font_size * self.pointer])

    def setItems(self, items):
        self.items = items
        self.pointer = 0

    def getSelectedItem(self):
        return self.items[self.pointer]

    def getPointer(self):
        return self.porinter

    def pointerDown(self):
        if self.pointer + 1 < len(self.items):
            self.pointer += 1
        else:
            self.pointer = 0

    def pointerUp(self):
        if 0 <= self.pointer - 1:
            self.pointer -= 1
        else:
            self.pointer = len(self.items) - 1

#######################################
# INIT
#######################################
logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%Y/%m/%d %H:%M:%S", level=logging.DEBUG)
logging.info("CamRobo Remote Controll Client Startup...")

logging.degbug("initialize GamePad SN30Pro")
pygame.init()
pygame.joystick.init()
joys = pygame.joystick.Joystick(0)
joys.init()

logging.debug("initialize Action Window")
screen = pygame.display.set_mode((600,400))
screen.fill(((234,234,234)))
pygame.display.set_caption("CamRobo Client - Action Menu")
pygame.display.update()

logging.debug("initialize Action Menu")
R2_Trigger = False
categories = ["response","emotions","talk"]
actions    = [["YES","NO","ROGER"],
              ["SCREAM","SHOCKED","SING","WARNING","WORRY"],
              ["TALK_1","TALK_2","TALK_3","TALK_4","TALK_5","TALK_6"]]
last_action = None
selector_lv = 0
selector0 = ListSelector(pygame, screen, bgcolor=(51,153,255),items=categories)
selector1 = ListSelector(pygame, screen, bgcolor=(255,153,51),pos_x=30,pos_y=30)
HEADLIGHT = False

logging.info("connect to RoboCam")
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect((CAMROBO_ADDR,CAMROBO_PORT))

LOOP = True
#######################################
# MAIN
#######################################
while LOOP:
    cmdlist = ""

    screen.fill(((234,234,234)))
    if R2_Trigger == True:
        selector0.show()
        if selector_lv == 1:
            selector1.show()

    pygame.display.update()

    for e in pygame.event.get():
        if e.type == pygame.locals.JOYBUTTONDOWN:
            if e.button == PAD_BUTTON_B:
                logging.debug("B down")
                cmdlist = cmdlist + "AC=NO;"
            elif e.button == PAD_BUTTON_A:
                logging.debug("A down")
                cmdlist = cmdlist + "AC=YES;"
            elif e.button == PAD_BUTTON_Y:
                logging.debug("Y down")
                if HEADLIGHT:
                    HEADLIGHT = False
                    cmdlist = cmdlist + "AC=HEADLIGHT_OFF;"
                else:
                    HEADLIGHT = True
                    cmdlist = cmdlist + "AC=HEADLIGHT_ON;"
            elif e.button == PAD_BUTTON_X:
                logging.debug("X down")
            elif e.button == PAD_BUTTON_L1:
                logging.debug("L1 down")
            elif e.button == PAD_BUTTON_R1:
                logging.debug("R1 down")
            elif e.button == PAD_BUTTON_SELECT:
                logging.debug("SELECT down")
            elif e.button == PAD_BUTTON_START:
                logging.debug("START down")
            elif e.button == PAD_BUTTON_HART:
                logging.debug("HART down")
                cmdlist = "END=0"
                LOOP = False
                break
            elif e.button == PAD_BUTTON_JOY_RIGHT:
                logging.debug("JOY R down")
            elif e.button == PAD_BUTTON_JOY_LEFT:
                logging.debug("JOY L down")

        elif e.type == pygame.locals.JOYBUTTONUP:
             if e.button == PAD_BUTTON_B:
                 logging.debug("B up")
             elif e.button == PAD_BUTTON_A:
                 logging.debug("A up")
             elif e.button == PAD_BUTTON_Y:
                 logging.debug("Y up")
             elif e.button == PAD_BUTTON_X:
                 logging.debug("X up")
             elif e.button == PAD_BUTTON_L1:
                 logging.debug("L1 up")
             elif e.button == PAD_BUTTON_R1:
                 logging.debug("R1 up")
             elif e.button == PAD_BUTTON_SELECT:
                 logging.debug("SELECT up")
             elif e.button == PAD_BUTTON_START:
                 logging.debug("START up")
             elif e.button == PAD_BUTTON_HART:
                 logging.debug("HART up")
             elif e.button == PAD_BUTTON_JOY_LEFT:
                 logging.debug("JOY L up")
             elif e.button == PAD_BUTTON_JOY_RIGHT:
                 logging.debug("JOY R up")

        elif e.type == pygame.locals.JOYAXISMOTION:
            if e.axis == PAD_AXIS_LEFT_HORIZONTAL:
                logging.debug("axis L H {}".format(e.value))
            elif e.axis == PAD_AXIS_LEFT_VERTICAL:
                logging.debug("axis L V {}".format(e.value))
                context = "ML={};".format(motor_map(e.value * -1))
                cmdlist = cmdlist + context
            elif e.axis == PAD_AXIS_L2:
                logging.debug("axis L2 {}".format(e.value))
            elif e.axis == PAD_AXIS_RIGHT_HORIZONTAL:
                logging.debug("axis R H {}".format(e.value))
            elif e.axis == PAD_AXIS_RIGHT_VERTICAL:
                logging.debug("axis R V {}".format(e.value))
                context = "MR={};".format(motor_map(e.value * -1))
                cmdlist = cmdlist + context
            elif e.axis == PAD_AXIS_R2:
                logging.debug("axis R2".format(e.value))
                R2_Trigger = False if e.value < 0 else True

        elif e.type == pygame.locals.JOYHATMOTION:
            if e.value[0] > 0:
                logging.debug("hat Right {}".format(e.value[0]))
                if R2_Trigger == False and (last_action is not None):
                    context = "AC={};".format(last_action)
                    cmdlist = cmdlist + context
                elif R2_Trigger == True and selector_lv == 0:
                    selector_lv += 1
                    logging.debug("category: {}".format(selector0.getSelectedItem()))
                    selector1.setItems(actions[selector0.pointer])
                elif R2_Trigger == True and selector_lv == 1:
                    logging.debug("action : {}".format(selector1.getSelectedItem()))
                    last_action = selector1.getSelectedItem()
                    context = "AC={};".format(selector1.getSelectedItem())
                    cmdlist = cmdlist + context

            if e.value[0] < 0:
                logging.debug("hat Left {}".format(e.value[0]))
                if R2_Trigger == True and 0 <= selector_lv -1:
                    selector_lv -= 1
            if e.value[1] > 0:
                logging.debug("hat Up".format(e.value[1]))
                if R2_Trigger == False:
                    cmdlist = cmdlist + "S0=1;"
                elif R2_Trigger == True and selector_lv == 0:
                    selector0.pointerUp()
                elif R2_Trigger == True and selector_lv == 1:
                    selector1.pointerUp()
            if e.value[1] < 0:
                logging.debug("hat Down".format(e.value[1]))
                if R2_Trigger == False:
                    cmdlist = cmdlist + "S0=-1;"
                elif R2_Trigger == True and selector_lv == 0:
                    selector0.pointerDown()
                elif R2_Trigger == True and selector_lv == 1:
                    selector1.pointerDown()

    if cmdlist:
        logging.info("cmdlist={}".format(cmdlist))
        sock.send(bytes(cmdlist,'utf-8'))

    time.sleep(0.1)

logging.debug("connection terminated. bye...")
sock.shutdown(socket.SHUT_RDWR)
sock.close()
pygame.quit()
pygame.joystick.quit()

