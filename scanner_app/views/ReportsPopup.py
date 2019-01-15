import tkinter as tk

class ReportsPopup():

    _report_generator = ''

    device_name = ''
    device_manufacturer = ''
    cpe_uri = ''

    scan_id = ''
    date = ''
    duration = ''

    host_id = ''
    host_ip = ''
    host_macAddress = ''
    host_osFamily = ''
    host_osGen = ''
    host_name = ''
    host_vendor = ''

    parameter_value = ''
    parameter_type = ''

    pen_test_id = ''
    result = ''

    def __init__(self, report_generator):
        self._report_generator = report_generator

        self.device_name = report_generator[0]
        self.device_manufacturer = report_generator[1]
        self.cpe_uri = report_generator[2]

        self.scan_id = report_generator[3]
        self.date = report_generator[4]
        self.duration = report_generator[5]
        self.host_id = report_generator[6]
        self.host_ip = report_generator[7]
        self.host_macAddress = report_generator[8]
        self.host_osFamily = report_generator[9]
        self.host_osGen = report_generator[10]
        self.host_name = report_generator[11]
        self.host_vendor = report_generator[12]

        self.parameter_value = report_generator[13]
        self.parameter_type = report_generator[14]

        self.pen_test_id = report_generator[15]
        self.result = report_generator[16]

    def new_popup(self):

