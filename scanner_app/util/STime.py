from threading import Timer

"""
A simple timer in order for the user to keep track of the duration of a scanning period.
"""


class STimer:
    @staticmethod
    def do_after(completion, timer):
        t = Timer(timer, completion)
        t.start()
        return t

    @staticmethod
    def empty_timer():
        return Timer(0, ())
