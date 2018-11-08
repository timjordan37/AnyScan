import tkinter as tk
import nmap
from scanner_app.helpers.EntryValidator import Validator

from scanner_app.helpers.Scanner import Scanner
from scanner_app.helpers.Scanner import ScannerError

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
        scanner.host_discover()
        print(scanner.get_hosts())

    def on_check_vulnerabilities():
        print("User clicked 'check vulnerabilities'")

    def on_details():
        print("User clicked 'Details'")

    def on_report():
        print("User clicked 'Report'")

    # Variables
    devices = []
    vulnerabilities = []
    scanner = Scanner('127.0.0.1', '22-30')

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

    ## Setup scan port label frame
    scan_port_label_frame = tk.Frame(left_frame)
    scan_port_label_frame.grid(row=2, column=0)

    ## Setup scan port label
    port_start_label = tk.Label(scan_port_label_frame, text="Start Port")
    port_start_label.grid(row=0, column=0, padx=(0, 8))

    port_end_label = tk.Label(scan_port_label_frame, text="End Port")
    port_end_label.grid(row=0, column=1, padx=(8, 0))

    ## Setup scan port frame
    scan_port_frame = tk.Frame(left_frame)
    scan_port_frame.grid(row=3, column=0)

    ## Setup scan port entries
    port_start_entry = tk.Entry(scan_port_frame, width=4)
    port_start_entry.grid(row=0, column=0, padx=(0, 16))

    port_end_entry = tk.Entry(scan_port_frame, width=4)
    port_end_entry.grid(row=0, column=1, padx=(16, 0))

    # Setup Left frame scan button
    scan_button = tk.Button(left_frame, text="Scan", command=on_scan)
    scan_button.grid(row=4, column=0, pady=(8, 8))

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

    # Run the program with UI
    root.geometry("500x400")
    root.minsize(500, 400)
    root.mainloop()


#  Runs the main method if this file is called to run
if __name__ == '__main__':
    main()
