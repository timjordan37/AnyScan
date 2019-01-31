import tkinter as tk

class VulnerabilitiesView():

    vuln_name_entry_var = None
    vuln_cvss_score_entry_var = None
    vuln_severity_entry_var = None
    vuln_score_entry_var = None

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

        return frame
