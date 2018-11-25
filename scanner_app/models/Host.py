# Host object to represent the hosts retrieved through the scan
class Host:
    _ip = ""
    _state = ""
    _name = ""
    _osFamily = ""
    _osGen = ""
    _vendor = ""
    _macAddress = ""

    def __init__(self, ip, state, name, osFamily, osGen, vendor, macAddress):
        self._ip = ip
        self._state = state
        self._name = name
        self._osFamily = osFamily
        self._osGen = osGen
        self._vendor = vendor
        self._macAddress = macAddress

    def get_display_name(self):
        return f"IP: {self._ip}    State: {self._state}"

    def get_ip(self):
        return self._ip

    def get_mac_address(self):
        return self._macAddress