import threading

"""
This class handles threading that is done during the entire scanning period of the application
"""


class SThread(threading.Thread):
    def __init__(self, threadID, name, counter, completion):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.completion = completion

    def run(self):
        print
        "Starting " + self.name
        self.completion()
        print
        "Exiting " + self.name
