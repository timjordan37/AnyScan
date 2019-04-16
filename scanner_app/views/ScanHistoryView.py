import tkinter as tk
import enum
from views.TableView import TableView
from util import DBFunctions as dbf
from tkinter import ttk

"""
This class is responsible for generating the UI displayed on the 'Scan History' tab of the application.
It will create search fields so that users can search for a specific previous scan and view the scan details 
if they wish to do so.  It will also compile a list of all previous scans that have been run and place them 
in a table organized by ID, Duration, Date and Host Count.  Users can opt out of using the search fields and 
can manually select any previous scan from this table.
"""

class ScanHistoryView:

    scan_id_entry_var = None
    scan_duration_entry_var = None
    scan_date_entry_var = None
    vuln_score_entry_var = None

    """The Method to be called when a scan is selected"""

    on_selected_scan_completion = None
    
    search_button = None
    table_view = None

    def get_view(self, parent_frame):
        self.scan_id_entry_var = tk.StringVar()
        self.scan_duration_entry_var = tk.StringVar()
        self.scan_date_entry_var = tk.StringVar()
        self.vuln_score_entry_var = tk.StringVar()

        frame = ttk.Frame(parent_frame)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_rowconfigure(6, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        """header label"""

        header_label = ttk.Label(frame, text="Scan History Search")
        header_label.grid(row=0, column=0, pady=(8, 8))

        """Vuln Name Search"""

        scan_id_frame = ttk.Frame(frame)
        scan_id_frame.grid(row=1, column=0, sticky="nsew")
        scan_id_frame.grid_columnconfigure(1, weight=1)

        scan_id_label = ttk.Label(scan_id_frame, text="Scan ID:")
        scan_id_label.grid(row=0, column=0, padx=(16, 0))

        self.scan_id_entry_var.set("")
        scan_id_entry = ttk.Entry(scan_id_frame, textvariable=self.scan_id_entry_var)
        scan_id_entry.grid(row=0, column=1, sticky="nsew", padx=(0, 16))

        """Vuln CVSS Score"""

        scan_duration_frame = ttk.Frame(frame)
        scan_duration_frame.grid(row=2, column=0, sticky="nsew")
        scan_duration_frame.grid_columnconfigure(1, weight=1)

        scan_duration_label = ttk.Label(scan_duration_frame, text="Scan Duration:")
        scan_duration_label.grid(row=0, column=0, padx=(16, 0))

        self.scan_duration_entry_var.set("")
        scan_duration_entry = ttk.Entry(scan_duration_frame, textvariable=self.scan_duration_entry_var)
        scan_duration_entry.grid(row=0, column=1, sticky="nsew", padx=(0, 16))

        """Severity"""

        scan_date_frame = ttk.Frame(frame)
        scan_date_frame.grid(row=3, column=0, sticky="nsew")
        scan_date_frame.grid_columnconfigure(1, weight=1)

        scan_date_label = ttk.Label(scan_date_frame, text="Scan Date:")
        scan_date_label.grid(row=0, column=0, padx=(16, 0))

        self.scan_date_entry_var.set("")
        scan_date_entry = ttk.Entry(scan_date_frame, textvariable=self.scan_date_entry_var)
        scan_date_entry.grid(row=0, column=1, sticky="nsew", padx=(0, 16))

        """Search Button"""

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=5, column=0)

        self.search_button = ttk.Button(button_frame, text="Search", command=self.on_search)
        self.search_button.grid(row=0, column=0, pady=(8, 8))

        """Scan Details button"""

        self.search_button = ttk.Button(button_frame, text="Scan Details", command=self.on_scan_details)
        self.search_button.grid(row=0, column=1, pady=(8, 8))

        """TableView"""

        sections_tuple = TreeColumns.all_cases()

        all_scans = dbf.DBFunctions.get_all_scans()

        data = []
        for scan in all_scans:
            data.append(list(scan))

        self.table_view = TableView(frame, 6, sections_tuple, data[::-1])

        return frame

    def on_search(self):
        query_tuple = self.build_query_string()
        data = dbf.DBFunctions.get_all_where(query_tuple[0], query_tuple[1])
        self.table_view.reload_data(data)

    def on_scan_details(self):
        selected_value = self.table_view.get_selected_item()["values"]

        if len(selected_value) > 0:
            """System.Settings.get_instance().current_selected_scan_id = selected_value[0]"""
            self.on_selected_scan_completion(selected_value[0])

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
            query_str_params_list.append(""" sh.ScanDate LIKE (?) """)
            query_params_list.append("%" + self.scan_date_entry_var.get() + "%")

        if self.scan_duration_entry_var.get():
            query_str_params_list.append(""" sh.Duration LIKE (?) """)
            query_params_list.append("%" + self.scan_duration_entry_var.get() + "%")

        params_count = len(query_str_params_list)
        for idx, param_str in enumerate(query_str_params_list):
            additional_param_str = ""
            if params_count > 1 and idx > 0:
                additional_param_str += " AND "
            query_str += (additional_param_str + param_str)

        query_str += """ GROUP BY sh.ScanID """
        return query_str, tuple(query_params_list)


class TreeColumns(enum.Enum):

    """Set up tree columns to be displayed on appropriate tab"""

    scan_id = 0
    scan_duration = 1
    scan_date = 2
    host_count = 3

    @staticmethod
    def display_name_for_column(col):
        display_names = {
            0: "ID",
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
