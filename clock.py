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

class clock :
    def __init__(self) :
        self.default_color = (255, 255, 0)
        self.default_s_color = (127, 127, 0)
        self.a_color = (255, 255, 0)
        self.a_s_color = (127, 0, 0)
        self.b_color = (0, 0, 0)

        self.clock = pygame.time.Clock()
        self.screen = screen()
        pygame.mouse.set_visible(False)

        #self.font = pygame.font.Font('segoeui.ttf', 126)
        self.font = pygame.font.Font('segoeui.ttf', 195)
        self.dateFont = pygame.font.Font('segoeui.ttf', 36)

        os.putenv('SDL_MOUSEDRV', 'TSLIB')
        os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

    def touch(self, updates) :
        tx = datetime.today()
        while True :
            self.clock.tick(10)
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
    
    def run(self) :
        touchQ = mp.Queue()
        touchT = mp.Process(target=self.touch, args=(touchQ,))
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
            self.clock.tick(100)
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
                    color = self.a_color
                    s_color = self.a_s_color
                else :
                    color = self.default_color
                    s_color = self.default_s_color
        
                time_surface = self.font.render(current, True, color)
                time_surface_shadow = self.font.render(current, True, s_color)
                colon_surface = self.font.render(currentSep, True, color)
                colon_surface_shadow = self.font.render(currentSep, True, s_color)
                #tz_surface = self.font.render(tz, True, color)
                date_surface = self.dateFont.render(currentDate, True, color)
                date_surface_shadow = self.dateFont.render(currentDate, True, s_color)
        
                self.screen.scr.fill(self.b_color)
                self.screen.scr.blit(time_surface_shadow, (8, 26))
                self.screen.scr.blit(time_surface, (4, 22))
                self.screen.scr.blit(colon_surface_shadow, (227, 26))
                self.screen.scr.blit(colon_surface, (223, 22))
                #self.screen.scr.blit(tz_surface, (120, 196))
                #self.screen.scr.blit(tz_surface, (120, 196))
                self.screen.scr.blit(date_surface_shadow, (12, 12))
                self.screen.scr.blit(date_surface, (10, 10))
                #lastTime = current
                pygame.display.update()
    
if __name__ == '__main__' :
    c = clock()
    c.run()
