import tkinter as tk
import VulnPopup as vp
import DevicePopup as dp
import DBFunctions as df
from pathlib import Path
import random
from helpers.Scanner import Scanner
from util.SThread import SThread
from util.STime import STimer
import datetime
from DBFunctions import DBFunctions
# Main method to handle setting up and managing the UI


# Constants
HOME_IP = '192.168.1.1' # default gateway, not really home

def main():
    print("Scanner App Started...")

    # UI Updating Method
    def update_left_header_label(value):
        """UI Updating Method
        :param value: value to be set in left header
        """
        if value is None:
            # if the provided value is none, then update to the default header
            host_count = len(scanned_hosts)
            host_count_text = f"({host_count}) Hosts Scanned".format()
            left_frame_header_label_var.set(host_count_text)
        else:
            # else
            left_frame_header_label_var.set(value)

    def update_left_header_label_random_waiting_msg():
        """Update waiting header randomly"""
        random_waiting_responses = [
            "This may take a while...",
            "I'm sorry this will be a while...",
            "Scanning...",
            "Scanning in Process..."
        ]
        update_left_header_label(random.choice(random_waiting_responses))

    def reset_left_header_label():
        """Update left header with number of hosts scanned"""
        host_count = len(scanned_hosts)
        host_count_text = f"({host_count}) Hosts Scanned".format()
        left_frame_header_label_var.set(host_count_text)

    def reload_hosts_listbox():
        """Update hosts box with scanned hosts"""
        hosts_listbox.delete(0, tk.END)
        for host in scanned_hosts:
            hosts_listbox.insert(tk.END, host.get_display_val())

    def reload_vulnerabilities_listbox():
        """Update vulnerabilites box with found vulnerabilites"""
        vulnerabilities_listbox.delete(0, tk.END)
        for vulnerability in vulnerabilities:
            vulnerabilities_listbox.insert(tk.END, vulnerability)

    def scan_thread_completion():
        """Scan given inputs, update associated ui, and save scan data"""
        scan_start_date = datetime.datetime.now()
        update_left_header_label("Scan in process...")
        scan_button.config(state="disabled")
        waiting_scanner1 = STimer.do_after(update_left_header_label_random_waiting_msg, 15)
        waiting_scanner2 = STimer.do_after(update_left_header_label_random_waiting_msg, 30)
        waiting_scanner3 = STimer.do_after(update_left_header_label_random_waiting_msg, 45)

        ports = f'{port_start_entry_var.get()}-{port_end_entry_var.get()}'
        hosts = scan_host_entry_var.get()
        scanner = Scanner(hosts, ports)
        nonlocal scanned_hosts

        print("Scan start")
        set_host(scanner.get_os_service_scan_details())
        set_cpes_vulns(scanner.get_cpes())
        print("Scan END")

        scan_button.config(state="normal")

        # could get this from the scan itself
        scan_end_date = datetime.datetime.now()
        timedelta = scan_end_date - scan_start_date
        timedelta.total_seconds()
        ##


        last_row_id = DBFunctions.save_scan(scan_start_date, timedelta.total_seconds())

        for host in get_hosts():
            DBFunctions.save_host(host, last_row_id)

        update_left_header_label(f"Scan finished in {timedelta} seconds")
        STimer.do_after(reset_left_header_label, 2)
        waiting_scanner1.cancel()
        waiting_scanner2.cancel()
        waiting_scanner3.cancel()

    def set_host(h):
        """Set scanned hosts for ui
        :param h: hosts found
        """
        nonlocal scanned_hosts
        scanned_hosts = h
        reload_hosts_listbox()

    def set_cpes_vulns(c):
        """Set vulnerabilities from cps"""
        nonlocal cpes
        cpes = c
        DBFunctions.query_cves(cpes)
        # query
        # todo reload after querying for cves and setting vulnerabilities[]
        #reload_vulnerabilities_listbox()

    def get_hosts():
        """Get scanned hosts"""
        nonlocal scanned_hosts
        return scanned_hosts

    # Click Handlers
    def on_scan():
        """Click handler for scan btn to start scanner thread"""
        # MAKE SURE TO VALIDATE INPUT
        scan_thread = SThread(0, "SCAN_THREAD_1", 5, scan_thread_completion)
        scan_thread.start()

    def on_check_vulnerabilities():
        """Click hanlder for check vulnerabilities button"""
        # todo set_cpes_vulns() test
        if cpes:
            set_cpes_vulns(cpes)
        print("User clicked 'check vulnerabilities'")

    def new_vuln_popup():
        """Click handler for new vuln button"""
        vp.VulnPopup.new_popup()

    def on_details():
        """Click handler for details button"""
        # todo query for selected cve fromm listbox
        print("User clicked 'Details'")

    def on_report():
        """Click hanlder for report button"""
        print("User clicked 'Report'")

    def on_host_listbox_select(evt):
        """Click handler to update right ui when user clicks on a host in left box"""
        # Note here that Tkinter passes an event object to onselect()
        listbox = evt.widget
        index = int(listbox.curselection()[0])
        host_name_entry_var.set(scanned_hosts[index].get_display_name())
        mac_address_entry_var.set(scanned_hosts[index].get_mac_address())
        port_number_entry_var.set(scanned_hosts[index].get_ip())

    def new_device_popup():
        """Click handler for new device button"""
        dp.DevicePopup.new_popup()



    # Variables
    vulnerabilities = []
    scanned_hosts = []
    cpes ={}

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

    # Setup Left frame HostListbox
    hosts_listbox = tk.Listbox(left_frame, width="30")
    hosts_listbox.grid(row=1, column=0, sticky="nsew", padx=(2, 0))
    hosts_listbox.bind('<<ListboxSelect>>', on_host_listbox_select)
    reload_hosts_listbox()

    # Setup scan host frame
    scan_host_frame = tk.Frame(left_frame)
    scan_host_frame.grid(row=2, column=0)

    # Setup scan host label
    scan_host_label = tk.Label(scan_host_frame, text="Hosts:")
    scan_host_label.grid(row=0, column=0)

    # Setup scan host entry
    scan_host_entry_var = tk.StringVar()
    scan_host_entry_var.set("192.168.1.0/28")
    scan_host_entry = tk.Entry(scan_host_frame, textvariable=scan_host_entry_var)
    scan_host_entry.grid(row=0, column=1)

    ## Setup scan port label frame
    scan_port_label_frame = tk.Frame(left_frame)
    scan_port_label_frame.grid(row=3, column=0)

    ## Setup scan port label
    port_start_label = tk.Label(scan_port_label_frame, text="Start Port")
    port_start_label.grid(row=0, column=0, padx=(0, 8))

    port_end_label = tk.Label(scan_port_label_frame, text="End Port")
    port_end_label.grid(row=0, column=1, padx=(8, 0))

    ## Setup scan port frame
    scan_port_frame = tk.Frame(left_frame)
    scan_port_frame.grid(row=4, column=0)

    ## Setup scan port entries
    port_start_entry_var = tk.StringVar()
    port_start_entry_var.set("21")
    port_start_entry = tk.Entry(scan_port_frame, width=4, textvariable=port_start_entry_var)
    port_start_entry.grid(row=0, column=0, padx=(0, 16))

    port_end_entry_var = tk.StringVar()
    port_end_entry_var.set("30")
    port_end_entry = tk.Entry(scan_port_frame, width=4, textvariable=port_end_entry_var)
    port_end_entry.grid(row=0, column=1, padx=(16, 0))

    # Setup Left frame scan button
    scan_button = tk.Button(left_frame, text="Scan", command=on_scan)
    scan_button.grid(row=5, column=0, pady=(8, 8))

    #################
    # Setup RightFrame
    #################
    right_frame = tk.Frame(root)
    right_frame.grid(row=0, column=1, sticky="nsew")
    right_frame.grid_rowconfigure(6, weight=1)
    right_frame.grid_columnconfigure(0, weight=1)

    # Right frame header label
    right_frame_header_label = tk.Label(right_frame, text="Host Info")
    right_frame_header_label.grid(row=0, column=0, pady=(8, 8))

    #  Host name UI
    host_name_frame = tk.Frame(right_frame)
    host_name_frame.grid(row=1, column=0, sticky="nsew")
    host_name_frame.grid_columnconfigure(1, weight=1)

    host_name_label = tk.Label(host_name_frame, text="Host Name:")
    host_name_label.grid(row=0, column=0, padx=(16, 0))

    host_name_entry_var = tk.StringVar()
    host_name_entry_var.set("")
    host_name_text_entry = tk.Entry(host_name_frame, textvariable=host_name_entry_var)
    host_name_text_entry.grid(row=0, column=1, sticky="nsew", padx=(0, 16))

    #  MAC Address UI
    mac_address_frame = tk.Frame(right_frame)
    mac_address_frame.grid(row=2, column=0, sticky="nsew")
    mac_address_frame.grid_columnconfigure(1, weight=1)

    mac_address_label = tk.Label(mac_address_frame, text="MAC Address:")
    mac_address_label.grid(row=0, column=0, padx=(16, 0))

    mac_address_entry_var = tk.StringVar()
    mac_address_entry_var.set("")
    mac_address_text_entry = tk.Entry(mac_address_frame, textvariable=mac_address_entry_var)
    mac_address_text_entry.grid(row=0, column=1, sticky="nsew", padx=(0, 16))

    #  Port Number UI
    port_number_frame = tk.Frame(right_frame)
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
    check_vulnerabilities_button = tk.Button(right_frame, text="Check Vulnerabilities", command=on_check_vulnerabilities)
    check_vulnerabilities_button.grid(row=4, column=0, pady=(0, 8))

    # Vulnerabilities ListBox label
    vulnerabilities_header_label = tk.Label(right_frame, text="Vulnerabilities")
    vulnerabilities_header_label.grid(row=5, column=0)

    #################
    # Vulnerabilities ListBox
    #################
    #
    vulnerabilities_listbox = tk.Listbox(right_frame)
    vulnerabilities_listbox.grid(row=6, column=0, sticky="nsew", padx=(16, 16))
    reload_vulnerabilities_listbox()

    #################
    # Vulnerabilities button frame
    #################
    #
    vulnerabilities_button_frame = tk.Frame(right_frame)
    vulnerabilities_button_frame.grid(row=7, column=0, pady=(8, 8))

    # Details
    vulnerability_details_button = tk.Button(vulnerabilities_button_frame, text="Details", command=on_details)
    vulnerability_details_button.grid(row=0, column=0)

    # Report
    vulnerability_report_button = tk.Button(vulnerabilities_button_frame, text="Report", command=on_report)
    vulnerability_report_button.grid(row=0, column=1)
    # Add Vulnerability
    add_vulnerabilities_button = tk.Button(vulnerabilities_button_frame, text="Add Vulnerability",
                                           command=new_vuln_popup)
    add_vulnerabilities_button.grid(row=0, column=2)

    # Add Device
    add_vulnerabilities_button = tk.Button(vulnerabilities_button_frame, text="Add Device", command=new_device_popup)
    add_vulnerabilities_button.grid(row=0, column=3)


    # Run the program with UI
    root.geometry("800x500")
    root.minsize(800, 500)
    root.mainloop()


#  Runs the main method if this file is called to run
if __name__ == '__main__':
    db_location = Path("vulnDB.db")
    if not db_location.exists():
        df.DBFunctions.build_db()
    main()
