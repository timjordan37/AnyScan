import tkinter as tk

# Main method to handle setting up and managing the UI


def main():
    print("Main method called")

    # UI Updating Method
    def update_left_header_label(value):
        if value is None:
            # if the provided value is none, then update to the default header
            device_count = len(devices)
            device_count_text = f"({device_count}) Devices Scanned".format()
            left_frame_header_label_var.set(device_count_text)
        else:
            # else
            left_frame_header_label_var.set(value)

    def reload_devices_listbox():
        devices_listbox.delete(0, tk.END)
        for device in devices:
            devices_listbox.insert(tk.END, device)

    def reload_vulnerabilities_listbox():
        vulnerabilities_listbox.delete(0, tk.END)
        for vulnerability in vulnerabilities:
            vulnerabilities_listbox.insert(tk.END, vulnerability)

    # Click Handlers
    def on_scan():
        print("User clicked 'Scan'")

    def on_check_vulnerabilities():
        print("User clicked 'check vulnerabilities'")

    def on_details():
        print("User clicked 'Details'")

    def on_report():
        print("User clicked 'Report'")

    def new_device_popup():
        print("adding a new device")

    def new_vuln_popup():
        model = ""
        cpe_name = ""
        cpe_uri = ""
        description = ""
        versions_affected = ""
        cvss_score = ""
        attack_vector = ""
        attack_complexity = ""
        privileges_required  = ""
        user_interaction = ""
        confidentiality_impact = ""
        integrity_impact = ""
        availability_impact = ""
        base_score = ""
        base_severity = ""
        exploitability_score = ""

        vuln_popup = tk.Toplevel(padx=10, pady=10)
        vuln_popup.wm_title("Add Vulnerability")
        vuln_popup.geometry("500x500")

        related_mod = tk.Entry(vuln_popup, textvariable=model)
        related_mod.grid(column=0, row=0, padx=5, pady=5)

        cpe_name_entry = tk.Entry(vuln_popup, textvariable=cpe_name)
        cpe_name_entry.grid(column=0, row=1, padx=5, pady=5)

        cpe_uri_entry = tk.Entry(vuln_popup, textvariable=cpe_uri)
        cpe_uri_entry.pack()

        description_entry = tk.Entry(vuln_popup, textvariable=description)
        description_entry.pack()

        versions_affected_entry = tk.Entry(vuln_popup, textvariable=versions_affected)
        versions_affected_entry.pack()

        cvss_score_entry = tk.Entry(vuln_popup, textvariable=cvss_score)
        cvss_score_entry.pack()

        attack_vector_entry = tk.Entry(vuln_popup, textvariable=attack_vector)
        attack_vector_entry.pack()

        attack_complexity_entry = tk.Entry(vuln_popup, textvariable=attack_complexity)
        attack_complexity_entry.pack()

        privileges_required_entry = tk.Entry(vuln_popup, textvariable=privileges_required)
        privileges_required_entry.pack()

        user_interaction_entry = tk.Entry(vuln_popup, textvariable=user_interaction)
        user_interaction_entry.pack()

        confidentiality_impact_entry = tk.Entry(vuln_popup, textvariable=confidentiality_impact)
        confidentiality_impact_entry.pack()

        integrity_impact_entry = tk.Entry(vuln_popup, textvariable=integrity_impact)
        integrity_impact_entry.pack()

        availability_impact_entry = tk.Entry(vuln_popup, textvariable=availability_impact)
        availability_impact_entry.pack()

        base_score_entry = tk.Entry(vuln_popup, textvariable=base_score)
        base_score_entry.pack()

        base_severity_entry = tk.Entry(vuln_popup, textvariable=base_severity)
        base_severity_entry.pack()

        exploitability_score_entry = tk.Entry(vuln_popup, textvariable=exploitability_score)
        exploitability_score_entry.pack()



    # Variables
    devices = []
    vulnerabilities = []

    # Setup root ui
    root = tk.Tk()
    root.title("Scanner App")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    #################
    # Setup LeftFrame
    #################
    left_frame = tk.Frame(root)
    left_frame.grid(row=0, column=0, sticky="nsew")
    left_frame.grid_rowconfigure(1, weight=1)
    left_frame.grid_columnconfigure(0, weight=1)

    # Setup Left Frame header Label
    left_frame_header_label_var = tk.StringVar()
    update_left_header_label(None)
    left_frame_header_label = tk.Label(left_frame, textvariable=left_frame_header_label_var)
    left_frame_header_label.grid(row=0, column=0)

    # Setup Left frame DevicesListbox
    devices_listbox = tk.Listbox(left_frame)
    devices_listbox.grid(row=1, column=0, sticky="nsew", padx=(2, 0))
    reload_devices_listbox()

    # Setup Left frame scan button
    scan_button = tk.Button(left_frame, text="Scan", command=on_scan)
    scan_button.grid(row=2, column=0, pady=(8, 8))

    #################
    # Setup RightFrame
    #################
    right_frame = tk.Frame(root)
    right_frame.grid(row=0, column=1, sticky="nsew")
    right_frame.grid_rowconfigure(6, weight=1)
    right_frame.grid_columnconfigure(0, weight=1)

    # Right frame header label
    right_frame_header_label = tk.Label(right_frame, text="Device Info")
    right_frame_header_label.grid(row=0, column=0, pady=(8, 8))

    #  Device name UI
    device_name_frame = tk.Frame(right_frame)
    device_name_frame.grid(row=1, column=0, sticky="nsew")
    device_name_frame.grid_columnconfigure(1, weight=1)

    device_name_label = tk.Label(device_name_frame, text="Device Name:")
    device_name_label.grid(row=0, column=0, padx=(16, 0))

    device_name_text_entry = tk.Entry(device_name_frame)
    device_name_text_entry.grid(row=0, column=1, sticky="nsew", padx=(0, 16))

    #  MAC Address UI
    mac_address_frame = tk.Frame(right_frame)
    mac_address_frame.grid(row=2, column=0, sticky="nsew")
    mac_address_frame.grid_columnconfigure(1, weight=1)

    mac_address_label = tk.Label(mac_address_frame, text="MAC Address:")
    mac_address_label.grid(row=0, column=0, padx=(16, 0))

    mac_address_text_entry = tk.Entry(mac_address_frame)
    mac_address_text_entry.grid(row=0, column=1, sticky="nsew", padx=(0, 16))

    #  Port Number UI
    port_number_frame = tk.Frame(right_frame)
    port_number_frame.grid(row=3, column=0, sticky="nsew", pady=(0, 8))
    port_number_frame.grid_columnconfigure(1, weight=1)

    port_number_label = tk.Label(port_number_frame, text="Port Number:")
    port_number_label.grid(row=0, column=0, padx=(16, 0))

    port_number_text_entry = tk.Entry(port_number_frame)
    port_number_text_entry.grid(row=0, column=1, sticky="nsew", padx=(0, 16))

    # Check Vulnerabilities UI
    check_vulnerabilities_button = tk.Button(right_frame, text="Check Vulnerabilities", command=on_check_vulnerabilities)
    check_vulnerabilities_button.grid(row=4, column=0, pady=(0, 8))

    vulnerabilities_header_label = tk.Label(right_frame, text="Vulnerabilities")
    vulnerabilities_header_label.grid(row=5, column=0)

    # Vulnerabilities ListBox
    vulnerabilities_listbox = tk.Listbox(right_frame)
    vulnerabilities_listbox.grid(row=6, column=0, sticky="nsew", padx=(16, 16))
    reload_vulnerabilities_listbox()

    # Vulnerabilities button frame
    vulnerabilities_button_frame = tk.Frame(right_frame)
    vulnerabilities_button_frame.grid(row=7, column=0, pady=(8, 8))

    vulnerability_details_button = tk.Button(vulnerabilities_button_frame, text="Details", command=on_details)
    vulnerability_details_button.grid(row=0, column=0)

    vulnerability_report_button = tk.Button(vulnerabilities_button_frame, text="Report", command=on_report)
    vulnerability_report_button.grid(row=0, column=1)

    #################
    # Setup File Menu
    #################

    # Creating the menu
    file_menu = tk.Menu(root)
    file_menu.add_command(label="Add new Device", command=new_device_popup)
    file_menu.add_command(label="Add new Vulnerability", command=new_vuln_popup)

    # Display the menu
    root.config(menu=file_menu)

    # Run the program with UI
    root.geometry("500x400")
    root.minsize(500, 400)
    root.mainloop()


#  Runs the main method if this file is called to run
if __name__ == '__main__':
    main()
