from threading import Timer


class STimer:
    """A simple timer in order for the user to keep track of the duration of a scanning period.
    """
    @staticmethod
    def do_after(completion, timer):
        """Create object given timer and completion

        :param completion: function to run
        :param timer: seconds to delay
        :return Timer object after start
        """
        t = Timer(timer, completion)
        t.start()
        return t

    @staticmethod
    def empty_timer():
        """Create empty timer

        :return empty timer
        """
        return Timer(0, ())
