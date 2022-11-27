#!/usr/bin/python
#######################################
# CamRobo Remote Control Server
#######################################
import logging
import socket
import time
from adafruit_motor   import servo
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio
import simpleaudio
import queue
import threading
import action
import random

class CRAWLER:
    def __init__(self):
        self.pca_motor_forward_ch = None
        self.pca_motor_back_ch    = None

    def setValue(self, duty):
        if duty < 0:
            self.pca_motor_forward_ch.duty_cycle = 0
            self.pca_motor_back_ch.duty_cycle    = abs(duty)
        elif duty > 0:
            self.pca_motor_forward_ch.duty_cycle = duty
            self.pca_motor_back_ch.duty_cycle    = 0
        else:
            self.pca_motor_forward_ch.duty_cycle = 0
            self.pca_motor_back_ch.duty_cycle    = 0

    def stop(self):
        print("stop crawler")

class LED_RGB:
    def __init__(self):
        self.pca_r_ch = None 
        self.pca_g_ch = None 
        self.pca_b_ch = None 

    def setColorByRGB(self, r, g, b):
        if 0x0000 <= r <= 0xFFFF:
            self.pca_r_ch.duty_cycle = r
        if 0x0000 <= g <= 0xFFFF:
            self.pca_g_ch.duty_cycle = g
        if 0x0000 <= b <= 0xFFFF:
            self.pca_b_ch.duty_cycle = b

    def setColorByName(self, name):
        if name == "WHITE":
            self.pca_r_ch.duty_cycle = 0x7FFF
            self.pca_g_ch.duty_cycle = 0x7FFF
            self.pca_b_ch.duty_cycle = 0x7FFF
        elif name == "RED":
            self.pca_r_ch.duty_cycle = 0x7FFF
            self.pca_g_ch.duty_cycle = 0x0000
            self.pca_b_ch.duty_cycle = 0x0000
        elif name == "GREEN":
            self.pca_r_ch.duty_cycle = 0x0000
            self.pca_g_ch.duty_cycle = 0x7FFF
            self.pca_b_ch.duty_cycle = 0x0000
        elif name == "BLUE":
            self.pca_r_ch.duty_cycle = 0x0000
            self.pca_g_ch.duty_cycle = 0x0000
            self.pca_b_ch.duty_cycle = 0x7FFF
        else:
            self.reset()

    def setRandomColor(self):
        self.pca_r_ch.duty_cycle = random.randrange(0x0FFF) 
        self.pca_g_ch.duty_cycle = random.randrange(0x0FFF) 
        self.pca_b_ch.duty_cycle = random.randrange(0x0FFF) 

    def reset(self):
        self.pca_r_ch.duty_cycle = 0x0000
        self.pca_g_ch.duty_cycle = 0x0000
        self.pca_b_ch.duty_cycle = 0x0000

#######################################
# INIT
#######################################
# logging
logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%Y/%m/%d %H:%M:%S", level=logging.DEBUG)
logging.info("CamRobo Remote Controll Server Startup...")


logging.debug("start sound thread")
sound_queue = queue.Queue(maxsize=1)
def sound_worker():
    while True:
        func = sound_queue.get()
        eval("action.SOUND_{}".format(func))()
        sound_queue.task_done()

sound_thread = threading.Thread(target=sound_worker, daemon=True)
sound_thread.start()


logging.debug("start led thread")
led_queue   = queue.Queue(maxsize=1)
def led_worker():
    while True:
        func = led_queue.get()
        eval("action.LED_{}".format(func))(led_l,led_r)
        led_queue.task_done()

led_thread = threading.Thread(target=led_worker, daemon=True)
led_thread.start()


# PCA9685 Parameters
logging.debug("initialize PCA9685")
PWM_FREQ = 60
PWM_SERVO_EYE           = 0
PWM_SERVO_ARM1          = 1
PWM_SERVO_ARM2          = 2
PWM_SERVO_ARM3          = 3
PWM_MOTOR_RIGHT_BACK    = 4
PWM_MOTOR_RIGHT_FORWARD = 5
PWM_MOTOR_LEFT_BACK     = 6
PWM_MOTOR_LEFT_FORWARD  = 7
PWM_LED_LEFT_R          = 8
PWM_LED_LEFT_G          = 9
PWM_LED_LEFT_B          = 10
# NOT USED                11
PWM_LED_RIGHT_R         = 12
PWM_LED_RIGHT_G         = 13
PWM_LED_RIGHT_B         = 14
PWM_FAN                 = 15

i2c_bus = busio.I2C(SCL,SDA)
pca = PCA9685(i2c_bus)
pca.frequency = PWM_FREQ

servo0 = servo.Servo(pca.channels[PWM_SERVO_EYE])
servo0.angle = 50
servo1 = servo.Servo(pca.channels[PWM_SERVO_ARM1])
servo2 = servo.Servo(pca.channels[PWM_SERVO_ARM2])
servo3 = servo.Servo(pca.channels[PWM_SERVO_ARM3])

crawlerR = CRAWLER()
crawlerR.pca_motor_forward_ch = pca.channels[PWM_MOTOR_RIGHT_FORWARD]
crawlerR.pca_motor_back_ch    = pca.channels[PWM_MOTOR_RIGHT_BACK]
crawlerR.setValue(0)

crawlerL = CRAWLER()
crawlerL.pca_motor_forward_ch = pca.channels[PWM_MOTOR_LEFT_FORWARD]
crawlerL.pca_motor_back_ch    = pca.channels[PWM_MOTOR_LEFT_BACK]
crawlerL.setValue(0)

led_r  = LED_RGB()
led_r.pca_r_ch = pca.channels[PWM_LED_LEFT_R]
led_r.pca_g_ch = pca.channels[PWM_LED_LEFT_G]
led_r.pca_b_ch = pca.channels[PWM_LED_LEFT_B]
led_r.setColorByRGB(0,0,0)

led_l  = LED_RGB()
led_l.pca_r_ch = pca.channels[PWM_LED_RIGHT_R]
led_l.pca_g_ch = pca.channels[PWM_LED_RIGHT_G]
led_l.pca_b_ch = pca.channels[PWM_LED_RIGHT_B]
led_l.setColorByRGB(0,0,0)

# Server 
logging.debug("initialize socket")
ADDR = "0.0.0.0"
PORT = 8080
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind((ADDR,PORT))
sock.listen(1)

logging.info("start listening at {}:{}. waiting for connection from client...".format(ADDR, PORT))

ACTION="SING"
if sound_queue.empty(): sound_queue.put(ACTION)
if led_queue.empty(): led_queue.put(ACTION)

#######################################
# MAIN
#######################################
while True:
    logging.info("reset physical state")
    servo0.angle = 50
    crawlerR.setValue(0)
    crawlerL.setValue(0)
    led_r.reset()
    led_l.reset()

    logging.info("waiting for connection from client...")
    client,remote_addr = sock.accept()
    logging.info("accepted connection from client{}.".format(remote_addr))
    ACTION="YES"
    if sound_queue.empty(): sound_queue.put(ACTION)
    if led_queue.empty(): led_queue.put(ACTION)
    
    # COMMAND REFERENCE
    # ---------------------------
    # CMD=$value;[...]
    #
    #
    # COMMAND LIST
    # ---------------------------
    # MR=$value
    # ML=$value
    #   -65535 <= $value <= 65535(0xFFFF)
    #   move Motor Right/Left
    #
    # S0=$value
    # S1=$value
    # S2=$value
    # S3=$value
    #   move Servo to specific angle or increment angle
    #
    # L1=$valueR,$valueG,$valueB
    # L2=$valueR,$valueG,$valueB
    #   -65535 <= $valueR/G/B <= 65535(0xFFFF)
    #
    # AC=$value
    #   $value = Action Name
    #
    
    END_FLAG = 0
    while True:
        rcv_data = client.recv(1024)
        if rcv_data:
            for context in str(rcv_data.decode("utf-8")).split(";"):
                logging.debug("context={}".format(context))
                if context:
                    cmd,args = context.split("=")
                    logging.debug("cmd={}, args={}".format(cmd,args))
                    if cmd == "MR":
                        crawlerR.setValue(int(args))
                    elif cmd == "ML":
                        crawlerL.setValue(int(args))
                    elif cmd == "AC":
                        if sound_queue.empty(): sound_queue.put(args)
                        if led_queue.empty(): led_queue.put(args)
                    elif cmd == "S0":
                        if int(args) > 0:
                            tmp = servo0.angle - 10
                            logging.debug("S0 {}".format(servo0.angle))
                            servo0.angle = tmp if tmp > 15 else 15
                        else:
                            logging.debug("S0 {}".format(servo0.angle))
                            tmp = servo0.angle + 10
                            servo0.angle = tmp if tmp < 150 else 150
                    elif cmd == "END":
                        client.shutdown(socket.SHUT_RDWR)
                        client.close()
                        END_FLAG = 1
                        break
        if END_FLAG == 1:
            break
    
logging.info("close socket")
sock.close()
pca.deinit()
