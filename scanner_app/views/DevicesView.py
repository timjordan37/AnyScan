import tkinter as tk
import enum
from views.TableView import TableView
from util import DBFunctions as dbf


class DevicesView:
    device_name_entry_var = None
    device_manufacturer_entry_var = None
    search_button = None
    table_view = None

    def get_view(self, parent_frame):
        self.device_name_entry_var = tk.StringVar()
        self.device_manufacturer_entry_var = tk.StringVar()

        frame = tk.Frame(parent_frame)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)

        # header label
        header_label = tk.Label(frame, text="Devices")
        header_label.grid(row=0, column=0, pady=(8, 8))

        # Device Name Search
        device_name_frame = tk.Frame(frame)
        device_name_frame.grid(row=1, column=0, sticky="nsew")
        device_name_frame.grid_columnconfigure(1, weight=1)

        device_name_label = tk.Label(device_name_frame, text="Device Name:")
        device_name_label.grid(row=0, column=0, padx=(16, 0))

        self.device_name_entry_var.set("")
        device_name_text_entry = tk.Entry(device_name_frame, textvariable=self.device_name_entry_var)
        device_name_text_entry.grid(row=0, column=1, sticky="nsew", padx=(0, 16))

        # Device Manufacturer
        device_manufacturer_frame = tk.Frame(frame)
        device_manufacturer_frame.grid(row=2, column=0, sticky="nsew")
        device_manufacturer_frame.grid_columnconfigure(1, weight=1)

        device_manufacturer_label = tk.Label(device_manufacturer_frame, text="Manufacturer:")
        device_manufacturer_label.grid(row=0, column=0, padx=(16, 0))

        self.device_manufacturer_entry_var.set("")
        device_manufacturer_text_entry = tk.Entry(device_manufacturer_frame,
                                                  textvariable=self.device_manufacturer_entry_var)
        device_manufacturer_text_entry.grid(row=0, column=1, sticky="nsew", padx=(0, 16))

        # Search Button
        self.search_button = tk.Button(frame, text="Search")
        self.search_button.grid(row=3, column=0, pady=(8, 8))

        return frame
