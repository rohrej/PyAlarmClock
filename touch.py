#!/usr/bin/env python3

import os
from multiprocessing import Process
import pygame
from pygame.locals import *


class touch(Process) :
    def __init__(self) :
        super().__init__()
        os.putenv('SDL_MOUSEDRV', 'TSLIB')
        os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
        self.clock = pygame.time.Clock()
        
    def run(self) :
        while True:
            self.clock.tick(10)
            # Scan touchscreen events
            for event in pygame.event.get():
                if(event.type is MOUSEBUTTONDOWN):
                    pos = pygame.mouse.get_pos()
                    print("Down: " + str(pos))
                elif(event.type is MOUSEBUTTONUP):
                    pos = pygame.mouse.get_pos()
                    print("Up: " + str(pos))

    def __del__(self) :
        "Destructor"

if __name__ == '__main__' :
    os.putenv('SDL_FBDEV', '/dev/fb1')
    os.putenv('SDL_VIDEODRIVER', 'fbcon')
    pygame.display.init()
    pygame.mouse.set_visible(False)
    lcd = pygame.display.set_mode((480, 320))
    touchscreen = touch()
    touchscreen.start()
    touchscreen.join()
