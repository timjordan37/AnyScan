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

        popup = tk.Toplevel(padx=10, pady=10)
        popup.wm_title("Scan Report")

        device_name_label = tk.Label(popup, text="Device Name: ")
        device_name_entry = tk.Label(popup, text=self.device_name)
        device_name_label.grid(column=0, row=0, padx=5, pady=5)
        device_name_entry.grid(column=1, row=0, padx=5, pady=5)

        device_manufacturer_label = tk.Label(popup, text="Device Manufacturer")
        device_manufacturer_entry = tk.Label(popup, text=self.device_manufacturer)
        device_manufacturer_label.grid(column=0, row=1, padx=5, pady=5)
        device_manufacturer_entry.grid(column=1, row=1, padx=5, pady=5)

        cpe_uri_label = tk.Label(popup, text="cpeURI: ")
        cpe_uri_entry = tk.Label(popup, text=self.cpe_uri)
        cpe_uri_label.grid(column=0, row=2, padx=5, pady=5)
        cpe_uri_entry.grid(column=1, row=2, padx=5, pady=5)

        scan_id_label = tk.Label(popup, text="Scan ID: ")
        scan_id_entry = tk.Label(popup, text=self.scan_id)
        scan_id_label.grid(column=0, row=3, padx=5, pady=5)
        scan_id_entry.grid(column=1, row=3, padx=5, pady=5)

        date_label = tk.Label(popup, text="Date: ")
        date_entry = tk.Label(popup, text=self.date)
        date_label.grid(column=0, row=4, padx=5, pady=5)
        date_entry.grid(column=1, row=4, padx=5, pady=5)

        duration_label = tk.Label(popup, text="Duration: ")
        duration_entry = tk.Label(popup, text=self.duration)
        duration_label.grid(column=0, row=5, padx=5, pady=5)
        duration_entry.grid(column=1, row=5, padx=5, pady=5)

        host_id_label = tk.Label(popup, text="Host ID: ")
        host_id_entry = tk.Label(popup, text=self.host_id)
        host_id_label.grid(column=0, row=7, padx=5, pady=5)
        host_id_entry.grid(column=1, row=7, padx=5, pady=5)

        host_ip_label = tk.Label(popup, text="Host IP: ")
        host_ip_entry = tk.Label(popup, text=self.host_ip)
        host_ip_label.grid(column=0, row=8, padx=5, pady=5)
        host_ip_entry.grid(column=1, row=8, padx=5, pady=5)

        host_macAddress_label = tk.Label(popup, text="Host MacAddress: ")
        host_macAddress_entry = tk.Label(popup, text=self.host_macAddress)
        host_macAddress_label.grid(column=0, row=9, padx=5, pady=5)
        host_macAddress_entry.grid(column=1, row=9, padx=5, pady=5)

        host_osFamily_label = tk.Label(popup, text="Host OS Family: ")
        host_osFamily_entry = tk.Label(popup, text=self.host_osFamily)
        host_osFamily_label.grid(column=0, row=10, padx=5, pady=5)
        host_osFamily_entry.grid(column=1, row=10, padx=5, pady=5)
