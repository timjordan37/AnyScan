from threading import Timer


class STimer:
    @staticmethod
    def do_after(completion, timer):
        t = Timer(timer, completion)
        t.start()
        return t

    @staticmethod
    def empty_timer():
        return Timer(0, ())
