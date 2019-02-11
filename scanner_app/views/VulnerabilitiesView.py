import tkinter as tk
from tkinter import ttk
import enum
from views.TableView import TableView
from util import DBFunctions as dbf


class VulnerabilitiesView():

    vuln_name_entry_var = None
    vuln_cvss_score_entry_var = None
    vuln_severity_entry_var = None
    vuln_score_entry_var = None
    search_button = None
    table_view = None

    def get_view(self, parent_frame):
        self.vuln_name_entry_var = tk.StringVar()
        self.vuln_cvss_score_entry_var = tk.StringVar()
        self.vuln_severity_entry_var = tk.StringVar()
        self.vuln_score_entry_var = tk.StringVar()

        frame = tk.Frame(parent_frame)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)

        # header label
        header_label = tk.Label(frame, text="Vulnerabilities Search")
        header_label.grid(row=0, column=0, pady=(8, 8))

        #  Vuln Name Search
        vuln_name_frame = tk.Frame(frame)
        vuln_name_frame.grid(row=1, column=0, sticky="nsew")
        vuln_name_frame.grid_columnconfigure(1, weight=1)

        vuln_name_label = tk.Label(vuln_name_frame, text="Host Name:")
        vuln_name_label.grid(row=0, column=0, padx=(16, 0))

        self.vuln_name_entry_var.set("")
        host_name_text_entry = tk.Entry(vuln_name_frame, textvariable=self.vuln_name_entry_var)
        host_name_text_entry.grid(row=0, column=1, sticky="nsew", padx=(0, 16))

        #  Vuln CVSS Score
        vuln_cvss_frame = tk.Frame(frame)
        vuln_cvss_frame.grid(row=2, column=0, sticky="nsew")
        vuln_cvss_frame.grid_columnconfigure(1, weight=1)

        vuln_cvss_label = tk.Label(vuln_cvss_frame, text="CVSS Score:")
        vuln_cvss_label.grid(row=0, column=0, padx=(16, 0))

        self.vuln_cvss_score_entry_var.set("")
        mac_address_text_entry = tk.Entry(vuln_cvss_frame, textvariable=self.vuln_cvss_score_entry_var)
        mac_address_text_entry.grid(row=0, column=1, sticky="nsew", padx=(0, 16))

        #  Severity
        severity_frame = tk.Frame(frame)
        severity_frame.grid(row=3, column=0, sticky="nsew")
        severity_frame.grid_columnconfigure(1, weight=1)

        severity_label = tk.Label(severity_frame, text="Severity:")
        severity_label.grid(row=0, column=0, padx=(16, 0))

        self.vuln_severity_entry_var.set("")
        vuln_severity_text_entry = tk.Entry(severity_frame, textvariable=self.vuln_severity_entry_var)
        vuln_severity_text_entry.grid(row=0, column=1, sticky="nsew", padx=(0, 16))

        #  Score
        score_frame = tk.Frame(frame)
        score_frame.grid(row=4, column=0, sticky="nsew")
        score_frame.grid_columnconfigure(1, weight=1)

        score_label = tk.Label(score_frame, text="Score:")
        score_label.grid(row=0, column=0, padx=(16, 0))

        self.vuln_score_entry_var.set("")
        vuln_score_text_entry = tk.Entry(score_frame, textvariable=self.vuln_score_entry_var)
        vuln_score_text_entry.grid(row=0, column=1, sticky="nsew", padx=(0, 16))

        # Search Button
        self.search_button = tk.Button(frame, text="Search")
        self.search_button.grid(row=5, column=0, pady=(8, 8))

        # TableView
        sections_tuple = TreeColumns.all_cases()

        # dbf.DBFunctions.save_vulnerability("a","a","a","a","a","a","a","a","a","a","a","a","a","a","a",)
        # dbf.DBFunctions.save_vulnerability("b","b","b","b","b","b","b","b","b","b","b","b","b","b","b", )
        all_vulns = dbf.VulnerabilityDB.get_all()

        data = []
        for vuln in all_vulns:
            data.append(list(vuln))

        self.table_view = TableView(frame, 6, sections_tuple, data)

        return frame


class TreeColumns(enum.Enum):
    cve_name = 0
    description = 1
    cvssscore = 2
    base_score = 3
    severity = 4

    @staticmethod
    def display_name_for_column(col):
        display_names = {
            0: "id",
            1: "CVE Name",
            2: "Description",
            3: "CVSS Score",
            4: "Base Score",
            5: "Severity",
        }
        return display_names[col]

    @staticmethod
    def all_cases():
        cases = []

        for col in TreeColumns:
            cases.append(TreeColumns.display_name_for_column(col.value))

        return cases
