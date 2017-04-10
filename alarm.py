#!/usr/bin/env python3

import os
#import time
from datetime import datetime
from multiprocessing import Process, Queue
import pygame
#from time import strftime, mktime, localtime
import io, libconf

class alarm(Process) :
    def __init__(self, updates) :
        super().__init__()
        self.updates = updates
        self.vol = 0.1
        self.alarm_length = 10
        
        with io.open('alarms.cfg') as f:
            self.config = libconf.load(f)
        
        #print (self.config)
        
        self.wakeup_days = {"Sun": None, "Mon": None, "Tue": None, "Wed": None, "Thu": None, "Fri": None, "Sat": None}
        
        if 'daily' in self.config['alarms']:
            for day in self.wakeup_days:
                self.wakeup_days[day] = self.config.alarms.daily
        
        if 'by_day' in self.config['alarms']:
            for day, tod in self.config.alarms.by_day.items():
                self.wakeup_days[day] = tod
        
        #self.wakeup_daily = ["06:15"]
        #self.wakeup_weekeday = ["06:15"]
        
        self.wakeup_sound = "nature.mp3"
        
        if 'sound' in self.config['alarms']:
            self.wakeup_sound = self.config.alarms.sound
        
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
        pygame.mixer.init()
        #pygame.mixer.music.load(self.wakeup_sound)
        #pygame.mixer.music.set_volume(self.vol)
        #pygame.mixer.music.play()
        
        self.clock = pygame.time.Clock()

    def run(self) :
        last_time = datetime.today().timestamp()
        while True:
            self.clock.tick(1)
            #local_time = localtime()
            local_time = datetime.today()
            #print (local_time)
            today = local_time.strftime("%a")
            if self.wakeup_days[today]:
                hr, min = self.wakeup_days[today].split(':')
                #print ('Alarm set for ' + hr + ':' + min + ' today.')
                wakeup_today = local_time.replace(hour = int(hr), minute = int(min), second = 0, microsecond = 0)
                #print (wakeup_today)
                wakeup_time = wakeup_today.timestamp()
                if(local_time.timestamp() >= wakeup_time and wakeup_time > last_time):
                    #print ("Wakeup!")
                    pygame.mixer.music.load(self.wakeup_sound)
                    pygame.mixer.music.set_volume(self.vol)
                    pygame.mixer.music.play(-1)
                    self.updates.put("alarm")
                    while pygame.mixer.music.get_busy():
                        clock.tick(2)
                        playtime = datetime.today()
                        if ((playtime - local_time) > datetime.timedelta(minutes = alarm_length)):
                            mygame.mixer.music.stop()
                            self.updates.put("")
                            break
                
                last_time = local_time.timestamp()
    
if __name__ == '__main__' :
    uq = Queue()
    al = alarm(uq)
    al.start()
    while True :
        print (uq.get())
