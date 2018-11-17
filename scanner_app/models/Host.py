# Host object to represent the hosts retrieved through the scan
class Host:
    _ip = ""
    _state = ""

    def __init__(self, ip, state):
        self._ip = ip
        self._state = state

    def get_display_name(self):
        return f"IP: {self._ip}    State: {self._state}"

    def get_ip(self):
        return self._ip
