import tkinter as tk

class ScanDetailsView():


    def get_view(self, parent_frame):
        frame = tk.Frame(parent_frame)
        frame.grid(row=0, column=0, sticky="nsew")
        # frame.grid_rowconfigure(6, weight=1)
        # frame.grid_columnconfigure(0, weight=1)

        # Right frame header label
        header_label = tk.Label(frame, text="Host Info")
        header_label.grid(row=0, column=0, pady=(8, 8))

        #  Host name UI
        host_name_frame = tk.Frame(frame)
        host_name_frame.grid(row=1, column=0, sticky="nsew")
        host_name_frame.grid_columnconfigure(1, weight=1)

        host_name_label = tk.Label(host_name_frame, text="Host Name:")
        host_name_label.grid(row=0, column=0, padx=(16, 0))

        host_name_entry_var = tk.StringVar()
        host_name_entry_var.set("")
        host_name_text_entry = tk.Entry(host_name_frame, textvariable=host_name_entry_var)
        host_name_text_entry.grid(row=0, column=1, sticky="nsew", padx=(0, 16))

        #  MAC Address UI
        mac_address_frame = tk.Frame(frame)
        mac_address_frame.grid(row=2, column=0, sticky="nsew")
        mac_address_frame.grid_columnconfigure(1, weight=1)

        mac_address_label = tk.Label(mac_address_frame, text="MAC Address:")
        mac_address_label.grid(row=0, column=0, padx=(16, 0))

        mac_address_entry_var = tk.StringVar()
        mac_address_entry_var.set("")
        mac_address_text_entry = tk.Entry(mac_address_frame, textvariable=mac_address_entry_var)
        mac_address_text_entry.grid(row=0, column=1, sticky="nsew", padx=(0, 16))

        #  Port Number UI
        port_number_frame = tk.Frame(frame)
        port_number_frame.grid(row=3, column=0, sticky="nsew", pady=(0, 8))
        port_number_frame.grid_columnconfigure(1, weight=1)

        port_number_label = tk.Label(port_number_frame, text="IP:")
        port_number_label.grid(row=0, column=0, padx=(16, 0))

        port_number_entry_var = tk.StringVar()
        port_number_entry_var.set("")
        port_number_text_entry = tk.Entry(port_number_frame, textvariable=port_number_entry_var)
        port_number_text_entry.grid(row=0, column=1, sticky="nsew", padx=(0, 16))

        #################
        # Check Vulnerabilities UI
        #################
        #
        # Check Vulnerabilities button
        check_vulnerabilities_button = tk.Button(frame, text="Check Vulnerabilities")
        check_vulnerabilities_button.grid(row=4, column=0, pady=(0, 8))
        check_vulnerabilities_button.config(state="disabled")

        #################
        # Vulnerabilities listBox Frame
        #################
        #
        vulnerabilities_frame = tk.Frame(frame)
        vulnerabilities_frame.grid(row=5, column=0)

        # Vulnerabilities ListBox label
        vulnerabilities_header_label = tk.Label(vulnerabilities_frame, text="Vulnerabilities")
        vulnerabilities_header_label.grid(row=0, column=0)

        # Vulnerabilities number
        vulnerabilities_number_label = tk.Label(vulnerabilities_frame, text="")
        vulnerabilities_number_label.grid(row=0, column=1)

        # Vulnerabilities selection label
        vulnerability_label = tk.Label(vulnerabilities_frame, text="")
        vulnerability_label.grid(row=0, column=2)

        # Vulnerabilities listbox
        vulnerabilities_listbox = tk.Listbox(frame)
        vulnerabilities_listbox.grid(row=6, column=0, sticky="nsew", padx=(16, 16))
        # vulnerabilities_listbox.bind('<<ListboxSelect>>', on_vuln_listbox_select)
        # reload_vulnerabilities_listbox()

        #################
        # Vulnerabilities button frame
        #################
        #
        vulnerabilities_button_frame = tk.Frame(frame)
        vulnerabilities_button_frame.grid(row=7, column=0, pady=(8, 8))

        # Details
        vulnerability_details_button = tk.Button(vulnerabilities_button_frame, text="Details")
        vulnerability_details_button.grid(row=0, column=0)

        # Report
        vulnerability_report_button = tk.Button(vulnerabilities_button_frame, text="Report")
        vulnerability_report_button.grid(row=0, column=1)

        # Add Vulnerability
        add_vulnerabilities_button = tk.Button(vulnerabilities_button_frame, text="Add Vulnerability")
        add_vulnerabilities_button.grid(row=0, column=2)

        # Add Device
        add_vulnerabilities_button = tk.Button(vulnerabilities_button_frame, text="Add Device")
        add_vulnerabilities_button.grid(row=0, column=3)

        # Settings
        add_vulnerabilities_button = tk.Button(vulnerabilities_button_frame, text="Settings")
        add_vulnerabilities_button.grid(row=0, column=4)

        return frame