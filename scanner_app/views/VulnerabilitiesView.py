import tkinter as tk
import enum
from views.TableView import TableView
from util import DBFunctions as dbf
from util.DataShare import DataShare
from tkinter import ttk


class VulnerabilitiesView:

    vuln_name_entry_var = None
    vuln_cvss_score_entry_var = None
    vuln_severity_entry_var = None
    vuln_score_entry_var = None
    search_button = None
    pass_cve_button = None
    table_view = None

    # Method to be called to get selected cve
    on_selected_cve = None

    def get_view(self, parent_frame):
        self.vuln_name_entry_var = tk.StringVar()
        self.vuln_cvss_score_entry_var = tk.StringVar()
        self.vuln_severity_entry_var = tk.StringVar()
        self.vuln_score_entry_var = tk.StringVar()

        frame = ttk.Frame(parent_frame)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_rowconfigure(6, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # header label
        header_label = ttk.Label(frame, text="Vulnerabilities Search")
        header_label.grid(row=0, column=0, pady=(8, 8))

        #  Vuln Name Search
        vuln_name_frame = ttk.Frame(frame)
        vuln_name_frame.grid(row=1, column=0, sticky="nsew")
        vuln_name_frame.grid_columnconfigure(1, weight=1)

        vuln_name_label = ttk.Label(vuln_name_frame, text="CVE Name:")
        vuln_name_label.grid(row=0, column=0, padx=(16, 0))

        self.vuln_name_entry_var.set("")
        host_name_text_entry = ttk.Entry(vuln_name_frame, textvariable=self.vuln_name_entry_var)
        host_name_text_entry.grid(row=0, column=1, sticky="nsew", padx=(0, 16))

        #  Vuln CVSS Score
        vuln_cvss_frame = ttk.Frame(frame)
        vuln_cvss_frame.grid(row=2, column=0, sticky="nsew")
        vuln_cvss_frame.grid_columnconfigure(1, weight=1)

        vuln_cvss_label = ttk.Label(vuln_cvss_frame, text="CVSS Score:")
        vuln_cvss_label.grid(row=0, column=0, padx=(16, 0))

        self.vuln_cvss_score_entry_var.set("")
        mac_address_text_entry = ttk.Entry(vuln_cvss_frame, textvariable=self.vuln_cvss_score_entry_var)
        mac_address_text_entry.grid(row=0, column=1, sticky="nsew", padx=(0, 16))

        #  Severity
        severity_frame = ttk.Frame(frame)
        severity_frame.grid(row=3, column=0, sticky="nsew")
        severity_frame.grid_columnconfigure(1, weight=1)

        severity_label = ttk.Label(severity_frame, text="Severity:")
        severity_label.grid(row=0, column=0, padx=(16, 0))

        self.vuln_severity_entry_var.set("")
        vuln_severity_text_entry = ttk.Entry(severity_frame, textvariable=self.vuln_severity_entry_var)
        vuln_severity_text_entry.grid(row=0, column=1, sticky="nsew", padx=(0, 16))

        #  Score
        score_frame = ttk.Frame(frame)
        score_frame.grid(row=4, column=0, sticky="nsew")
        score_frame.grid_columnconfigure(1, weight=1)

        score_label = ttk.Label(score_frame, text="Score:")
        score_label.grid(row=0, column=0, padx=(16, 0))

        self.vuln_score_entry_var.set("")
        vuln_score_text_entry = ttk.Entry(score_frame, textvariable=self.vuln_score_entry_var)
        vuln_score_text_entry.grid(row=0, column=1, sticky="nsew", padx=(0, 16))

        # Search Button
        self.search_button = ttk.Button(frame, text="Search", command=self.on_search)
        self.search_button.grid(row=5, column=0, pady=(8, 8))

        # self.pass_cve_button = tk.Button(frame, text="Pass CVE", command=self.on_cve_select)
        # self.pass_cve_button.grid(row=5, column=1, pady=(8, 8))

        # TableView
        sections_tuple = TreeColumns.all_cases()
        all_vulns = dbf.DBFunctions.get_all_vulns()

        data = []
        for vuln in all_vulns:
            data.append(list(vuln))

        self.table_view = TableView(frame, 6, sections_tuple, data[::-1])
        self.table_view.bind_method('<ButtonRelease-1>', self.on_cve_select)
        self.table_view.bind_method('<Double-Button-1>', self.on_cve_double_click)

        return frame

    def on_search(self):
        query_tuple = self.build_query_string()
        data = dbf.DBFunctions.get_all_where(query_tuple[0], query_tuple[1])
        self.table_view.reload_data(data)

    def build_query_string(self):
        query_str = """SELECT VulnID, cveName, CVSSScore, baseScore, baseSeverity from Vulnerabilities"""
        query_str_params_list = []
        query_params_list = []

        if self.vuln_name_entry_var.get() or self.vuln_cvss_score_entry_var.get() or self.vuln_score_entry_var.get() or self.vuln_severity_entry_var.get():
            query_str += """ WHERE"""

        if self.vuln_name_entry_var.get():
            query_str_params_list.append(""" cveName LIKE (?) """)
            query_params_list.append("%" + self.vuln_name_entry_var.get() + "%")

        if self.vuln_cvss_score_entry_var.get():
            query_str_params_list.append(""" CVSSScore = (?) """)
            query_params_list.append(self.vuln_cvss_score_entry_var.get())

        if self.vuln_score_entry_var.get():
            query_str_params_list.append(""" baseScore = (?) """)
            query_params_list.append(int(self.vuln_score_entry_var.get()))

        if self.vuln_severity_entry_var.get():
            query_str_params_list.append(""" baseSeverity = (?) """)
            query_params_list.append(int(self.vuln_severity_entry_var.get()))

        params_count = len(query_str_params_list)
        for idx, param_str in enumerate(query_str_params_list):
            additional_param_str = ""
            if params_count > 1 and idx > 0:
                additional_param_str += " AND "
            query_str += (additional_param_str + param_str)

        return query_str, tuple(query_params_list)

    def on_cve_select(self, event):
        selected_value = self.table_view.get_selected_item()['values']
        print('From Vuln View: ', selected_value[1])

        if len(selected_value) > 0:
            DataShare.set_selected_cve(selected_value[1])
            self.on_selected_cve(selected_value[1])

    def on_cve_double_click(self, event):
        selected_value = self.table_view.get_selected_item()['values']
        print('From Vuln View DOULBE CLICK: ', selected_value[1])

        if len(selected_value) > 0:
            DataShare.set_selected_cve(selected_value[1])
            self.move_to_exploit(selected_value[1])


class TreeColumns(enum.Enum):
    id = 0
    cveName = 1
    cvssScore = 2
    baseScore = 3
    baseSeverity = 4

    @staticmethod
    def display_name_for_column(col):
        display_names = {
            0: "id",
            1: "CVE Name",
            2: "CVSS Score",
            3: "Base Score",
            4: "Base Severity",
        }
        return display_names[col]

    @staticmethod
    def all_cases():
        cases = []

        for col in TreeColumns:
            cases.append(TreeColumns.display_name_for_column(col.value))

        return cases
