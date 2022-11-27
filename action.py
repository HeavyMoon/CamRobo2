#######################################
# CamRobo Action Patterns
#######################################
import time
import simpleaudio
import random

## TEMPLATE
#def SOUND_$(ACTION_NAME)():
#    wav_obj = simpleaudio.WaveObject.from_wave_file("sound/file.wav")
#    play_obj = wav_obj.play()
#    play_obj.wait_done()
#
#def LED_$(ACTION_NAME)(led_l, led_r):
#    for i in range(10)[::-1]:
#        led_l.setColorByRGB(i*0x07FF,0,0)
#        led_r.setColorByRGB(i*0x07FF,0,0)
#        time.sleep(0.02)
#

def SOUND_YES():
    wav_obj = simpleaudio.WaveObject.from_wave_file("sound/YES.wav")
    play_obj = wav_obj.play()
    play_obj.wait_done()

def LED_YES(led_l, led_r):
    for t in [0.2,0.4]:
        led_l.setRandomColor()
        led_r.setRandomColor()
        time.sleep(t)
    led_l.setColorByRGB(0,0x0FFF,0)
    led_r.setColorByRGB(0,0x0FFF,0)
    time.sleep(0.25)
    led_l.reset()
    led_r.reset()


def SOUND_NO():
    wav_list = ["sound/NO_1.wav","sound/NO_2.wav","sound/NO_3.wav"]
    wav_obj = simpleaudio.WaveObject.from_wave_file(random.choice(wav_list))
    play_obj = wav_obj.play()
    play_obj.wait_done()

def LED_NO(led_l, led_r):
    for i in range(10)[::-1]:
        led_l.setColorByRGB(i*0x07FF,0,0)
        led_r.setColorByRGB(i*0x07FF,0,0)
        time.sleep(0.02)
    led_l.reset()
    led_r.reset()


def SOUND_ROGER():
    wav_obj = simpleaudio.WaveObject.from_wave_file("sound/Roger.wav")
    play_obj = wav_obj.play()
    play_obj.wait_done()

def LED_ROGER(led_l, led_r):
    for t in [0.2,0.2,0.1,0.1,0.1,0.1]:
        led_l.setRandomColor()
        led_r.setRandomColor()
        time.sleep(t)
    led_l.setColorByRGB(0,0x0FFF,0)
    led_r.setColorByRGB(0,0x0FFF,0)
    time.sleep(0.25)
    led_l.reset()
    led_r.reset()


def SOUND_SCREAM():
    wav_obj = simpleaudio.WaveObject.from_wave_file("sound/Scream.wav")
    play_obj = wav_obj.play()
    play_obj.wait_done()

def LED_SCREAM(led_l, led_r):
    led_l.setColorByRGB(0x07FF,0,0)
    led_r.setColorByRGB(0x07FF,0,0)
    time.sleep(0.2)
    for i in range(10)[::-1]:
        led_l.setColorByRGB(i*0x07FF,i*0x07FF,0)
        led_r.setColorByRGB(i*0x07FF,i*0x07FF,0)
        time.sleep(0.11)
    led_l.reset()
    led_r.reset()


def SOUND_SHOCKED():
    wav_obj = simpleaudio.WaveObject.from_wave_file("sound/Shocked.wav")
    play_obj = wav_obj.play()
    play_obj.wait_done()

def LED_SHOCKED(led_l, led_r):
    for t in [0.2,0.2,0.2,0.2,0.2,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]:
        led_l.setRandomColor()
        led_r.setRandomColor()
        time.sleep(t)
    for t in range(35):
        led_l.setRandomColor()
        led_r.setRandomColor()
        time.sleep(0.02)
    led_l.reset()
    led_r.reset()


def SOUND_SING():
    wav_obj = simpleaudio.WaveObject.from_wave_file("sound/Singing.wav")
    play_obj = wav_obj.play()
    play_obj.wait_done()

def LED_SING(led_l, led_r):
    for t in [0.2,0.4,0.2,0.4,0.2,0.4,0.4,0.2,0.2,0.2,0.2]:
        led_l.setRandomColor()
        led_r.setRandomColor()
        time.sleep(t)
    led_l.reset()
    led_r.reset()


def SOUND_TALK_1():
    wav_obj = simpleaudio.WaveObject.from_wave_file("sound/Talk_1.wav")
    play_obj = wav_obj.play()
    play_obj.wait_done()

def LED_TALK_1(led_l, led_r):
    for t in [0.1,0.1,0.3,0.1,0.1,0.1,0.3]:
        led_l.setRandomColor()
        led_r.setRandomColor()
        time.sleep(t)
    led_l.reset()
    led_r.reset()


def SOUND_TALK_2():
    wav_obj = simpleaudio.WaveObject.from_wave_file("sound/Talk_2.wav")
    play_obj = wav_obj.play()
    play_obj.wait_done()

def LED_TALK_2(led_l, led_r):
    for t in [0.1,0.1,0.1,0.1,0.3,0.6,0.2]:
        led_l.setRandomColor()
        led_r.setRandomColor()
        time.sleep(t)
    led_l.reset()
    led_r.reset()


def SOUND_TALK_3():
    wav_obj = simpleaudio.WaveObject.from_wave_file("sound/Talk_3.wav")
    play_obj = wav_obj.play()
    play_obj.wait_done()

def LED_TALK_3(led_l, led_r):
    for t in [0.1,0.6,0.3,0.3]:
        led_l.setRandomColor()
        led_r.setRandomColor()
        time.sleep(t)
    led_l.reset()
    led_r.reset()


def SOUND_TALK_4():
    wav_obj = simpleaudio.WaveObject.from_wave_file("sound/Talk_4.wav")
    play_obj = wav_obj.play()
    play_obj.wait_done()

def LED_TALK_4(led_l, led_r):
    for i in range(10):
        led_l.setColorByRGB(i*0x07FF,i*0x07FF,0)
        led_r.setColorByRGB(i*0x07FF,i*0x07FF,0)
        time.sleep(0.15)
    for t in [0.1,0.1,0.1,0.1,0.1,0.4,0.2]:
        led_l.setRandomColor()
        led_r.setRandomColor()
        time.sleep(t)
    led_l.reset()
    led_r.reset()


def SOUND_TALK_5():
    wav_obj = simpleaudio.WaveObject.from_wave_file("sound/Talk_5.wav")
    play_obj = wav_obj.play()
    play_obj.wait_done()

def LED_TALK_5(led_l, led_r):
    for t in [0.2,0.2,0.2,0.2,0.5]:
        led_l.setRandomColor()
        led_r.setRandomColor()
        time.sleep(t)
    led_l.reset()
    led_r.reset()


def SOUND_TALK_6():
    wav_obj = simpleaudio.WaveObject.from_wave_file("sound/Talk_6.wav")
    play_obj = wav_obj.play()
    play_obj.wait_done()

def LED_TALK_6(led_l, led_r):
    for t in [0.1,0.5,0.2,0.2,0.2,0.3,0.1,0.1,0.1,0.1,0.1]:
        led_l.setRandomColor()
        led_r.setRandomColor()
        time.sleep(t)
    led_l.reset()
    led_r.reset()


def SOUND_WARNING():
    wav_obj = simpleaudio.WaveObject.from_wave_file("sound/Warning.wav")
    play_obj = wav_obj.play()
    play_obj.wait_done()

def LED_WARNING(led_l, led_r):
    for i in range(10):
        led_l.setColorByRGB(i*0x07FF,0,0)
        led_r.setColorByRGB(i*0x07FF,0,0)
        time.sleep(0.05)
    for i in range(10):
        led_l.setColorByRGB(i*0x07FF,0,0)
        led_r.setColorByRGB(i*0x07FF,0,0)
        time.sleep(0.05)
    for t in [0.1,0.1,0.1,0.1,0.1,0.4,0.2]:
        led_l.setRandomColor()
        led_r.setRandomColor()
        time.sleep(t)
    led_l.reset()
    led_r.reset()


def SOUND_WORRY():
    wav_obj = simpleaudio.WaveObject.from_wave_file("sound/Worry.wav")
    play_obj = wav_obj.play()
    play_obj.wait_done()

def LED_WORRY(led_l, led_r):
    led_l.setColorByRGB(0x0FFF,0,0x0FFF)
    led_r.setColorByRGB(0x0FFF,0,0x0FFF)
    #time.sleep(0.2)
    for i in range(10)[::-1]:
        led_l.setColorByRGB(i*0x00FF,0,i*0x00FF)
        led_r.setColorByRGB(i*0x00FF,0,i*0x00FF)
        time.sleep(0.05)
    for i in range(10):
        led_l.setColorByRGB(0,0,i*0x00FF)
        led_r.setColorByRGB(0,0,i*0x00FF)
        time.sleep(0.05)
    led_l.reset()
    led_r.reset()

def SOUND_HEADLIGHT_ON():
    pass

def LED_HEADLIGHT_ON(led_l,led_r):
    led_l.setColorByRGB(0x3FFF,0x3FFF,0x3FFF)
    led_r.setColorByRGB(0x3FFF,0x3FFF,0x3FFF)

def SOUND_HEADLIGHT_OFF():
    pass

def LED_HEADLIGHT_OFF(led_l,led_r):
    led_l.reset()
    led_r.reset()

