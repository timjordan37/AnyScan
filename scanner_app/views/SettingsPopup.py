import tkinter as tk
from util import System

class SettingsPopup():

    def __init__(self):
        print("Look, im a popup")

    @staticmethod
    def new_popup():

        # Setup root ui
        root = tk.Toplevel()
        root.title("Scanner App - Settings")

        sort_settings_header_label = tk.Label(root, text="Host Display Settings", font='Helvetica 14 bold', anchor="w", width=24)
        sort_settings_header_label.grid(row=0, column=0)

        radio_btn_frame = tk.Frame(root)
        radio_btn_frame.grid(row=1, column=0, sticky="nsew")
        radio_btn_frame.grid_rowconfigure(1, weight=1)
        radio_btn_frame.grid_columnconfigure(0, weight=1)

        # setup sort options
        sort_options = []
        for type in System.SortType:
            sort_options.append((System.SortType.display_name_for_sort_type(type.value), type.value))

        selection_var = tk.IntVar()
        sort_type = System.Settings.get_host_sort_type()
        selection_var.set(sort_type.value)

        def on_sort_select():
            new_sort_type = System.SortType.sort_type_for_int(selection_var.get())
            System.Settings.set_host_sort_type(new_sort_type)

        for name, value in sort_options:
            b = tk.Radiobutton(radio_btn_frame, text=name, variable=selection_var, value=value, command=on_sort_select, anchor="w", width=24, justify="left")
            b.pack()

        # setup scan type options

        scan_type_radio_btn_frame = tk.Frame(root)
        scan_type_radio_btn_frame.grid(row=4, column=0, sticky="nsew")
        scan_type_radio_btn_frame.grid_rowconfigure(1, weight=1)
        scan_type_radio_btn_frame.grid_columnconfigure(0, weight=1)

        scan_type_settings_header_label = tk.Label(root, text="Scan Type", font='Helvetica 14 bold', anchor="w", width=24)
        scan_type_settings_header_label.grid(row=2, column=0, pady=(16, 0))

        scan_types = []
        for type in System.ScanType:
            scan_types.append((System.ScanType.display_name_for_scan_type(type.value), type.value))

        scan_type_selection_var = tk.IntVar()
        scan_type = System.Settings.get_scan_type()
        scan_type_selection_var.set(scan_type.value)

        def on_scan_type_select():
            new_scan_type = System.ScanType.scan_type_for_int(scan_type_selection_var.get())
            System.Settings.set_scan_type(new_scan_type)

        for name, value in scan_types:
            b = tk.Radiobutton(scan_type_radio_btn_frame, text=name, variable=scan_type_selection_var, value=value, command=on_scan_type_select, anchor="w", width=24, justify="left")
            b.pack()



        root.geometry("400x500")
        root.minsize(400, 500)
