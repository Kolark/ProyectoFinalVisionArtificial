import time


class TimeManager:
    def __init__(self):
        self.timePassed = 0

    def startTimer(self):
        self.start = time.time()

    def getTimePassed(self):
        self.timePassed = time.time() - self.start
        return self.timePassed

    def RestartTimer(self):
        self.start = time.time()


