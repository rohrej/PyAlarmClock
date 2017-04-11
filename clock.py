#!/usr/bin/env python3

import os
import multiprocessing as mp
#import time
import pygame
from pygame.locals import *

#from time import localtime
from datetime import datetime

from screen import screen
from timekeeper import timekeeper
from separator import separator
from calendar import calendar
from alarm import alarm

default_color = (255, 255, 0)
default_s_color = (127, 127, 0)
a_color = (255, 255, 0)
a_s_color = (127, 0, 0)
b_color = (0, 0, 0)

clock = pygame.time.Clock()
screen = screen()
pygame.mouse.set_visible(False)

#font = pygame.font.Font('segoeui.ttf', 126)
font = pygame.font.Font('segoeui.ttf', 196)
dateFont = pygame.font.Font('segoeui.ttf', 36)

os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

def touch(updates) :
    tx = datetime.today()
    while True :
        clock.tick(10)
        # Scan touchscreen events
        for event in pygame.event.get():
            if(event.type is MOUSEBUTTONDOWN):
                #pos = pygame.mouse.get_pos()
                #print("Down: " + str(pos))
                ts = datetime.today()
            elif(event.type is MOUSEBUTTONUP):
                pos = pygame.mouse.get_pos()
                #print("Up: " + str(pos))
                updates.put({'ts': ts, 'pos': pos})

touchQ = mp.Queue()
touchT = mp.Process(target=touch, args=(touchQ,))
touchT.start()
tq = mp.Queue()
tk = timekeeper(tq)
tk.start()
sq = mp.Queue()
sp = separator(sq)
sp.start()
dq = mp.Queue()
cd = calendar(dq)
cd.start()
aq = mp.Queue()
al = alarm(aq)
al.start()

current = "Starting"
currentSep = ""
currentDate = "Aquiring calendar data"
currentAlarm = ""
#lastTime = ""
while 1:
    clock.tick(100)
    #screen.scr.fill(b_color)
    #local_time = localtime()
    #current = strftime("%H:%M:%S  %Z", local_time)
    #current = strftime("%T", local_time)
    #current = strftime("%H %M", local_time)
    #if (local_time.tm_sec % 2 == 0):
    #    current = strftime("%H:%M", local_time)
    #else:
    #    current = strftime("%H %M", local_time)
    #tz = strftime("%Z", local_time)
    #print(current)
    #currentDate = strftime("%A, %B %d, %Y", local_time)
    newTouch = None
    try :
        newTouch = touchQ.get_nowait()
    except mp.queues.Empty :
        pass
    if (newTouch) :
        print (newTouch)
    
    newTime = None
    try :
        newTime = tq.get_nowait()
    except mp.queues.Empty :
        pass
    if (newTime) :
        current = newTime
    
    newSep = None
    try :
        newSep = sq.get_nowait()
    except mp.queues.Empty :
        pass
    if (newSep) :
        currentSep = newSep

    newDate = None
    try :
        newDate = dq.get_nowait()
    except mp.queues.Empty :
        pass
    if (newDate) :
        currentDate = newDate

    newAlarm = None
    try :
        newAlarm = aq.get_nowait()
    except mp.queues.Empty :
        pass
    if (newAlarm) :
        currentAlarm = newAlarm
    
    #if(lastTime != current) :
    if (newTime or newSep or newDate or newAlarm) :
        if (currentAlarm == "alarm") :
            color = a_color
            s_color = a_s_color
        else :
            color = default_color
            s_color = default_s_color
        
        time_surface = font.render(current, True, color)
        time_surface_shadow = font.render(current, True, s_color)
        colon_surface = font.render(currentSep, True, color)
        colon_surface_shadow = font.render(currentSep, True, s_color)
        #tz_surface = font.render(tz, True, color)
        date_surface = dateFont.render(currentDate, True, color)
        date_surface_shadow = dateFont.render(currentDate, True, s_color)
        
        screen.scr.fill(b_color)
        screen.scr.blit(time_surface_shadow, (8, 26))
        screen.scr.blit(time_surface, (4, 22))
        screen.scr.blit(colon_surface_shadow, (227, 26))
        screen.scr.blit(colon_surface, (223, 22))
        #screen.scr.blit(tz_surface, (120, 196))
        #screen.scr.blit(tz_surface, (120, 196))
        screen.scr.blit(date_surface_shadow, (12, 12))
        screen.scr.blit(date_surface, (10, 10))
        #lastTime = current
        pygame.display.update()
    

