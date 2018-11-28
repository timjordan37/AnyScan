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

    def get_display_val(self):
        first_val = ""
        second_val = ""

        # f"IP: {self._ip} - State: {self._state}"

        if self._name != "":
            first_val = self._name
        elif self._vendor != "":
            first_val = self._vendor
        else:
            first_val = self._ip

        if self._macAddress != "":
            second_val = self._macAddress
        else:
            second_val = 'State: '
            second_val += self._state

        return f"{first_val} - {second_val}"

    def get_ip(self):
        return self._ip

    def get_mac_address(self):
        return self._macAddress

    def get_display_name(self):
        if self._name != "":
            return self._name
        elif self._vendor != "" :
            return self._vendor
        else:
            return ""