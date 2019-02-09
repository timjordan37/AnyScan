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

        # TableView
        sections_tuple = TreeColumns.all_cases()
        all_devices = dbf.DBFunctions.get_all_devices()

        data = []
        for device in all_devices:
            data.append(list(device))

        self.table_view = TableView(frame, 6, sections_tuple, data)

        return frame

    def on_search(self):
        query_tuple = self.build_query_string()
        data = dbf.DBFunctions.get_all_qhere(query_tuple[0], query_tuple[1])
        self.table_view.reload_data(data)

    def build_query_string(self):
        query_str = """SELECT Model, Manufacturer from Devices"""
        query_str_params_list = []
        query_params_list = []

        if self.device_name_entry_var.get() or self.device_manufacturer_entry_var.get():
            query_str += """WHERE"""

        if self.device_name_entry_var.get():
            query_str_params_list.append(""" Model LIKE (?) """)
            query_params_list.append("%" + self.device_name_entry_var.get() + "%")

        if self.device_manufacturer_entry_var.get():
            query_str_params_list.append(""" Manufacturer LIKE (?) """)
            query_params_list.append("%" + self.device_manufacturer_entry_var.get() + "%")

        params_count = len(query_str_params_list)
        for idx, param_str in enumerate(query_str_params_list):
            additional_param_str = ""
            if params_count > 1 and idx > 0:
                additional_param_str += " AND "
            query_str += (additional_param_str + param_str)

        return query_str, tuple(query_params_list)


class TreeColumns(enum.Enum):
    device_name = 0
    device_manufacturer = 1

    @staticmethod
    def display_name_for_column(col):
        display_names = {
            0: "Model",
            1: "Manufacturer"
        }
        return display_names[col]

    @staticmethod
    def all_cases():
        cases = []
        for col in TreeColumns:
            cases.append(TreeColumns.display_name_for_column(col.value))
        return cases
