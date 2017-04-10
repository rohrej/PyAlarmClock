#!/usr/bin/env python3

from time import localtime, sleep
from multiprocessing import Process, Queue

class separator(Process) :
    def __init__(self, updates) :
        super().__init__()
        self.updates = updates

    def run(self) :
        lastTime = ""
        while True :
            if (localtime().tm_sec % 2 == 0) :
                current = ":"
            else :
                current = " "
            if(lastTime != current):
                #print (current)
                self.updates.put(current)
                lastTime = current

            sleep(0.25)


if __name__ == '__main__' :
    uq = Queue()
    sp = separator(uq)
    sp.start()
    while True :
        print (uq.get())
