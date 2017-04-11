#!/usr/bin/env python3

class StateMachine :
    def __init__(self) :
        self.states = {}
        self.state = ""
    
    def setState(self, state) :
        if state not in self.states :
            assert 0, state + " not implemmented"
        self.state = state
    
    def getState(self) :
        return self.state
    
    def next(self, event) :
        if event not in self.states[self.state] :
            assert 0, event + " not implemented in " + self.state
        self.state = self.states[self.state][event]
        return self.state

    def addState(self, state, event=None, transition=None) :
        if state not in self.states :
            self.states[state] = {}
        if transition and transition not in self.states :
            assert 0, transition + " not implemented in " + self.state
        if event and transition :
            self.states[state][event] = transition

if __name__ == '__main__' :
    m = StateMachine()
    m.addState('setup')
    m.addState('time', 'click', 'setup')
    m.setState('time')
    m.next('click')
    print (m.getState())

