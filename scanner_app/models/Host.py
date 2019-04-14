"""
This is a Host object to represent the hosts that are retrieved through various scans that will be performed by the
user.
"""


class Host:
    _hostID = ""
    _ip = ""
    _state = ""
    _name = ""
    _osFamily = ""
    _osGen = ""
    _vendor = ""
    _macAddress = ""

    def __init__(self, hostID, ip, state, name, osFamily, osGen, vendor, macAddress):
        self._hostID = hostID
        self._ip = ip
        self._state = state
        self._name = name
        self._osFamily = osFamily
        self._osGen = osGen
        self._vendor = vendor
        self._macAddress = macAddress

    def get_display_val(self):
        """Get display value for a given host to be displayed"""
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
            second_val = 'State: ' + self._state

        return f"{first_val} - {second_val}"

    def get_ip(self):
        """Get IP of host"""
        return self._ip

    def get_mac_address(self):
        """Get MAC address of host"""
        return self._macAddress

    def get_display_name(self):
        """Get name of host or vendor if not found"""
        if self._name != "":
            return self._name
        elif self._vendor != "":
            return self._vendor
        else:
            return ""

    def get_vendor(self):
        if self._vendor:
            return self._vendor

        return ""
      
    def get_id(self):
        """Get ID of host"""
        return self._hostID

