import tkinter as tk
from tkinter import ttk
import enum
from views.TableView import TableView
from util import DBFunctions as dbf


class ScanHistoryView():

    scan_id_entry_var = None
    scan_duration_entry_var = None
    scan_date_entry_var = None
    
    search_button = None
    table_view = None

    def get_view(self, parent_frame):
        self.scan_id_entry_var = tk.StringVar()
        self.scan_duration_entry_var = tk.StringVar()
        self.scan_date_entry_var = tk.StringVar()
        self.vuln_score_entry_var = tk.StringVar()

        frame = tk.Frame(parent_frame)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)

        # header label
        header_label = tk.Label(frame, text="Scan History Search")
        header_label.grid(row=0, column=0, pady=(8, 8))

        #  Vuln Name Search
        scan_id_frame = tk.Frame(frame)
        scan_id_frame.grid(row=1, column=0, sticky="nsew")
        scan_id_frame.grid_columnconfigure(1, weight=1)

        scan_id_label = tk.Label(scan_id_frame, text="Scan ID:")
        scan_id_label.grid(row=0, column=0, padx=(16, 0))

        self.scan_id_entry_var.set("")
        scan_id_entry = tk.Entry(scan_id_frame, textvariable=self.scan_id_entry_var)
        scan_id_entry.grid(row=0, column=1, sticky="nsew", padx=(0, 16))

        #  Vuln CVSS Score
        scan_duration_frame = tk.Frame(frame)
        scan_duration_frame.grid(row=2, column=0, sticky="nsew")
        scan_duration_frame.grid_columnconfigure(1, weight=1)

        scan_duration_label = tk.Label(scan_duration_frame, text="Scan Duration:")
        scan_duration_label.grid(row=0, column=0, padx=(16, 0))

        self.scan_duration_entry_var.set("")
        scan_duration_entry = tk.Entry(scan_duration_frame, textvariable=self.scan_duration_entry_var)
        scan_duration_entry.grid(row=0, column=1, sticky="nsew", padx=(0, 16))

        #  Severity
        scan_date_frame = tk.Frame(frame)
        scan_date_frame.grid(row=3, column=0, sticky="nsew")
        scan_date_frame.grid_columnconfigure(1, weight=1)

        scan_date_label = tk.Label(scan_date_frame, text="Scan Date:")
        scan_date_label.grid(row=0, column=0, padx=(16, 0))

        self.scan_date_entry_var.set("")
        scan_date_entry = tk.Entry(scan_date_frame, textvariable=self.scan_date_entry_var)
        scan_date_entry.grid(row=0, column=1, sticky="nsew", padx=(0, 16))

        # Search Button
        self.search_button = tk.Button(frame, text="Search", command=self.on_search)
        self.search_button.grid(row=5, column=0, pady=(0, 8))

        # TableView
        sections_tuple = TreeColumns.all_cases()

        all_scans = dbf.ScanHistoryDB.get_all()

        data = []
        for scan in all_scans:
            data.append(list(scan))

        self.table_view = TableView(frame, 6, sections_tuple, data)

        return frame

    def on_search(self):
        query_tuple = self.build_query_string()
        data = dbf.ScanHistoryDB.get_all_where(query_tuple[0], query_tuple[1])
        print("DATA: ", data)
        self.table_view.reload_data(data)

    def build_query_string(self):
        query_str = """SELECT sh.ScanID as ScanID, 
                                sh.Duration as Duration, 
                                sh.ScanDate as Date, 
                                (SELECT COUNT(*) from Hosts where ScanID = sh.ScanID) as HostCount 
                                from ScanHistory sh JOIN Hosts h on sh.ScanID = h.ScanID"""
        query_str_params_list = []
        query_params_list = []

        if self.scan_id_entry_var.get() or self.scan_duration_entry_var.get() or self.scan_date_entry_var.get():
            query_str += """ WHERE"""

        if self.scan_id_entry_var.get():
            query_str_params_list.append(""" sh.ScanID = (?) """)
            query_params_list.append(self.scan_id_entry_var.get())

        if self.scan_date_entry_var.get():
            query_str_params_list.append(""" sh.ScanDate = (?) """)
            query_params_list.append(self.scan_date_entry_var.get())

        if self.scan_duration_entry_var.get():
            query_str_params_list.append(""" sh.Duration = (?) """)
            query_params_list.append(float(self.scan_duration_entry_var.get()))

        params_count = len(query_str_params_list)
        for idx, param_str in enumerate(query_str_params_list):
            additional_param_str = ""
            if params_count > 1 and idx > 0:
                additional_param_str += " AND "
            query_str += (additional_param_str + param_str)

        query_str += """ GROUP BY sh.ScanID """
        print()
        print(query_str)
        print(tuple(query_params_list))
        return (query_str, tuple(query_params_list))

class TreeColumns(enum.Enum):
    scan_id = 0
    scan_duration = 1
    scan_date = 2
    host_count = 3

    @staticmethod
    def display_name_for_column(col):
        display_names = {
            0: "id",
            1: "Duration",
            2: "Date",
            3: "Host Count"
        }
        return display_names[col]

    @staticmethod
    def all_cases():
        cases = []

        for col in TreeColumns:
            cases.append(TreeColumns.display_name_for_column(col.value))

        return cases
