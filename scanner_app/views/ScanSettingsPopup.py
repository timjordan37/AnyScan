import tkinter as tk
from util import System

class ScanSettingsPopup():

    def __init__(self):
        print("Look, im a popup")

    @staticmethod
    def new_popup():
        # Creating the Popup Window
        popup = tk.Toplevel(padx=10, pady=10)
        popup.wm_title("Scan Settings")

        scan_options = []
        for type in System.ScanType:
            scan_options.append((System.ScanType.display_name_for_scan_type(type.value), type.value))

        selection_var = tk.IntVar()
        scan_type = System.Settings.get_scan_type()
        selection_var.set(scan_type.value)

        def on_select():
            new_scan_type = System.ScanType.scan_type_for_int(selection_var.get())
            System.Settings.set_scan_type(new_scan_type)

        for name, value in scan_options:
            b = tk.Radiobutton(popup, text=name, variable=selection_var, value=value, command=on_select)
            b.pack()