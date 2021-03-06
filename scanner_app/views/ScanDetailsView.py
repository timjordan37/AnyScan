import tkinter as tk
import enum
from datetime import date
from tkinter.filedialog import asksaveasfilename
from tkinter import simpledialog
from views import VulnPopup as vp, SettingsPopup as sp
from util.Reporter import Reporter
from util.DataShare import DataShare
from util.DBFunctions import DBFunctions
from views.TableView import TableView
from tkinter import ttk

"""
This class generates the UI displayed on the default tab when the application is initially launched.
This will display host information when a host is selected from the 'Hosts Scanned' section on the left,
as well as display vulnerabilities present directly after a scan is run.  The vulnerabilities will be
displayed by CVE name and sorted from highest to lowest CVSS Score.
"""


class ScanDetailsView:
    host_name_entry_var = None
    mac_address_entry_var = None
    port_number_entry_var = None
    check_vulnerabilities_button = None
    vulnerabilities = None
    cpes = None
    scanned_hosts = None
    vulnerabilities_header_label = None

    def new_vuln_popup(self):
        """Click handler for new vuln button"""
        vp.VulnPopup.new_popup()

    def on_settings(self):
        """Click handler for the Settings button"""
        sp.SettingsPopup.new_popup()

    def save_report_data(self, vulns, cpes, scanned_hosts):
        self.vulnerabilities = vulns
        self.cpes = cpes
        self.scanned_hosts = scanned_hosts

    def on_report(self):
        """Click hanlder for report button"""
        print("User clicked 'Report'")

        vulnerabilities = DataShare.get_vulns()
        cpes = DataShare.get_cpes()
        scanned_hosts = DataShare.get_hosts()

        #if vulnerabilities and cpes and scanned_hosts:
        if True:
            report = {
                'hosts': scanned_hosts,
                'cpes': cpes,
                'vulns': vulnerabilities
            }
            time = date.today().isoformat()
            name = simpledialog.askstring("Enter Name...",
                                          "Who is generating this report? \n"
                                          "Note: This will be listed as the report Author.")

            fname = asksaveasfilename(title='Select File to Save Report...', defaultextension='.pdf',
                                      initialfile='Report_' + str(time) + '.pdf')

            r = Reporter(report, fname, name)
            r.build_pdf()

    def get_view(self, parent_frame):
        self.host_name_entry_var = tk.StringVar()
        self.mac_address_entry_var = tk.StringVar()
        self.port_number_entry_var = tk.StringVar()

        frame = ttk.Frame(parent_frame)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_rowconfigure(6, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # Right frame header label
        header_label = ttk.Label(frame, text="Host Info")
        header_label.grid(row=0, column=0, pady=(8, 8))

        #  Host name UI
        host_name_frame = ttk.Frame(frame)
        host_name_frame.grid(row=1, column=0, sticky="nsew")
        host_name_frame.grid_columnconfigure(1, weight=1)

        host_name_label = ttk.Label(host_name_frame, text="Host Name:")
        host_name_label.grid(row=0, column=0, padx=(16, 0))

        self.host_name_entry_var.set("")
        host_name_text_entry = ttk.Entry(host_name_frame, textvariable=self.host_name_entry_var)
        host_name_text_entry.grid(row=0, column=1, sticky="nsew", padx=(0, 16))

        #  MAC Address UI
        mac_address_frame = ttk.Frame(frame)
        mac_address_frame.grid(row=2, column=0, sticky="nsew")
        mac_address_frame.grid_columnconfigure(1, weight=1)

        mac_address_label = ttk.Label(mac_address_frame, text="MAC Address:")
        mac_address_label.grid(row=0, column=0, padx=(16, 0))

        self.mac_address_entry_var.set("")
        mac_address_text_entry = ttk.Entry(mac_address_frame, textvariable=self.mac_address_entry_var)
        mac_address_text_entry.grid(row=0, column=1, sticky="nsew", padx=(0, 16))

        #  Port Number UI
        port_number_frame = ttk.Frame(frame)
        port_number_frame.grid(row=3, column=0, sticky="nsew", pady=(0, 8))
        port_number_frame.grid_columnconfigure(1, weight=1)

        port_number_label = ttk.Label(port_number_frame, text="IP:")
        port_number_label.grid(row=0, column=0, padx=(16, 0))

        self.port_number_entry_var.set("")
        port_number_text_entry = ttk.Entry(port_number_frame, textvariable=self.port_number_entry_var)
        port_number_text_entry.grid(row=0, column=1, sticky="nsew", padx=(0, 16))

        #################
        # Check Vulnerabilities UI
        #################
        #
        # Check Vulnerabilities button
        self.check_vulnerabilities_button = ttk.Button(frame, text="Check Vulnerabilities")
        self.check_vulnerabilities_button.grid(row=4, column=0, pady=(0, 8))
        self.check_vulnerabilities_button.config(state="disabled")

        #################
        # Vulnerabilities listBox Frame
        #################
        #
        vulnerabilities_frame = ttk.Frame(frame)
        vulnerabilities_frame.grid(row=5, column=0)

        # Vulnerabilities ListBox label
        vulnerabilities_header_label = ttk.Label(vulnerabilities_frame, text="Vulnerabilities")
        vulnerabilities_header_label.grid(row=0, column=0)

        # Vulnerabilities number
        vulnerabilities_number_label = ttk.Label(vulnerabilities_frame, text="")
        vulnerabilities_number_label.grid(row=0, column=1)

        # Vulnerabilities selection label
        vulnerability_label = ttk.Label(vulnerabilities_frame, text="")
        vulnerability_label.grid(row=0, column=2)

        # Vulnerabilities listbox

        class TreeColumns(enum.Enum):
            cveName = 0

            @staticmethod
            def display_name_for_column(col):
                display_names = {
                    0: "CVE Name"
                }
                return display_names[col]

            @staticmethod
            def all_cases():
                cases = []

                for col in TreeColumns:
                    cases.append(TreeColumns.display_name_for_column(col.value))

                return cases

        # TableView
        sections_tuple = TreeColumns.all_cases()

        data = []
        vulnerabilities_tableview = TableView(frame, 6, sections_tuple, data)
        vulnerabilities_tableview

        #################
        # Vulnerabilities button frame
        #################
        #
        vulnerabilities_button_frame = ttk.Frame(frame)
        vulnerabilities_button_frame.grid(row=7, column=0, pady=(8, 8))

        # Report
        vulnerability_report_button = ttk.Button(vulnerabilities_button_frame,
                                                 text="Report",
                                                 command=self.on_report)
        vulnerability_report_button.grid(row=0, column=0)

        # Add Vulnerability
        add_vulnerabilities_button = ttk.Button(vulnerabilities_button_frame, text="Add Vulnerability",
                                                command=self.new_vuln_popup)
        add_vulnerabilities_button.grid(row=0, column=1)

        # Settings
        add_vulnerabilities_button = ttk.Button(vulnerabilities_button_frame,
                                                text="Settings", command=self.on_settings)

        add_vulnerabilities_button.grid(row=0, column=3)

        return frame
