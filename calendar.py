#!/usr/bin/env python3

from time import strftime, localtime, sleep
from multiprocessing import Process, Queue

class calendar(Process) :
    def __init__(self, updates) :
        super().__init__()
        self.updates = updates

    def run(self) :
        lastTime = ""
        while True :
            local_time = localtime()
            current = strftime("%A, %B %d, %Y", local_time)
            if(lastTime != current):
                #print (current)
                self.updates.put(current)
                lastTime = current

            sleep(10)


if __name__ == '__main__' :
    uq = Queue()
    cd = calendar(uq)
    cd.start()
    while True :
        print (uq.get())
