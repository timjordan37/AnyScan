import threading

"""
This class handles threading that is done during the entire scanning period of the application
"""


class SThread(threading.Thread):
    def __init__(self, threadID, name, counter, completion):
        """Create SThread object given thread ID, name, counter, and completion

        :param threadID: ID of thread
        :param name: name of thread
        :param counter:
        :param completion:
        """
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.completion = completion

    def run(self):
        """Run thread"""
        print
        "Starting " + self.name
        self.completion()
        print
        "Exiting " + self.name
