# python imports
import datetime
import ctypes
import sys
import platform
import os
import random
import ntpath
# 3rd party imports
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import *
from pathlib import Path
from elevate import elevate
# custom modules imports
from util.Scanner import Scanner
from util.SThread import SThread
from util.STime import STimer
from util.DataShare import DataShare
from util import DBFunctions as df, System
from views.ScanDetailsView import ScanDetailsView
from views.VulnerabilitiesView import VulnerabilitiesView
from views.ScanHistoryView import ScanHistoryView
from views.ExploitView import ExploitView
from views.VulnPopup import VulnPopup
from models.Host import Host
from views.TableView import TableView


from ttkthemes import ThemedStyle
from ttkthemes import ThemedTk


# Main method to handle setting up and managing the UI


def main():
    print("Scanner App Started...")

    # UI Updating Method
    def update_left_header_label(value):
        """UI Updating Method
        :param value: value to be set in left header
        """
        if value is None:
            # if the provided value is none, then update to the default header
            host_count = DataShare.get_hosts_total()
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
        host_count = DataShare.get_hosts_total()
        host_count_text = f"({host_count}) Hosts Scanned".format()
        left_frame_header_label_var.set(host_count_text)

    def reload_hosts_tableview():
        """Update hosts box with scanned hosts"""
        # hosts_listbox.delete(0, tk.END)
        sorted_scanned_hosts = None

        # Sort according to the Host Sort Setting
        reverse_sort = False

        if System.Settings.get_host_sort_type() == System.SortType.alphaDESC:
            reverse_sort = True

        if DataShare.get_hosts():
            sorted_scanned_hosts = sorted(DataShare.get_hosts(), key=lambda x: (x.get_display_name()), reverse=reverse_sort)

        if sorted_scanned_hosts is None:
            return

        # Update hosts to the sorted version to ensure details on select are correct
        DataShare.set_hosts(sorted_scanned_hosts)

        data = list(map(lambda host: (host.get_ip(), host.get_display_name(), host.get_vendor()), sorted_scanned_hosts))

        # We need to reverse the data shown here because the table view will display the data in the reversed order
        # this is needed so that clicking the tableview will result in the correct host being selected: Task189
        hosts_table_view.reload_data(data[::-1])

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

        print("Scan start")
        set_host(scanner.get_scan_details(System.Settings.get_scan_type()))
        set_cpes_vulns(scanner.get_cpes())
        print("Scan END")

        scan_button.config(state="normal")
        scan_details_view.check_vulnerabilities_button.config(state="normal")

        scan_end_date = datetime.datetime.now()
        timedelta = scan_end_date - scan_start_date
        timedelta.total_seconds()

        last_row_id = df.DBFunctions.save_scan(scan_start_date, timedelta.total_seconds())

        for host in get_hosts():
            df.DBFunctions.save_host(host, last_row_id)

        update_left_header_label(f"Scan finished in {timedelta} seconds")
        STimer.do_after(reset_left_header_label, 2)
        waiting_scanner1.cancel()
        waiting_scanner2.cancel()
        waiting_scanner3.cancel()

    def set_host(h):
        """Set scanned hosts for ui
        :param h: hosts found
        """
        if h:
            DataShare.set_hosts(h)
            reload_hosts_tableview()

    def get_hosts():
        """Get scanned hosts"""
        return DataShare.get_hosts()

    def set_cpes_vulns(c):
        """Set vulnerabilities from cps"""
        DataShare.set_cpes(c)
        DataShare.set_vulns(df.DBFunctions.query_cves(c))
        # reload ui

    # Click Handlers
    def on_scan():
        """Click handler for scan btn to start scanner thread"""
        # MAKE SURE TO VALIDATE INPUT
        scan_thread = SThread(0, "SCAN_THREAD_1", 5, scan_thread_completion)
        scan_thread.start()

    def on_select_scan(id):
        query = "SELECT * FROM Hosts WHERE ScanID = ?"
        params = (id,)

        data = df.DBFunctions.get_all_where(query, params)
        print(data)
        # these need to be set, but not sure if the cpes and vulns are differentiate
        # by scans like hosts are
        # todo: set cpes and vulns in DataShare
        print(DataShare.get_cpes())
        print(DataShare.get_vulns())

        curr_hosts = []
        # for each host scanned
        for host_raw in data:
            ip = host_raw[1]
            state = "Old Host"
            mac = host_raw[2]
            os_gen = host_raw[3]
            os_family = host_raw[4]
            name = host_raw[5]
            vendor = host_raw[6]

            curr_hosts.append(Host(ip, state, name, os_family, os_gen, vendor, mac))

        set_host(curr_hosts)

    def find_exploit(cve):
        if cve:
            if exploit_view:
                exploit_view.update_cve(cve)
        else:
            print('No CVE selected')

    def update_exploit_tab(cve):
        main_note_book.select(2)
        exploit_view.cve_var.set(cve)
        # todo update exploit tab variables

    def on_host_tableview_select(event):
        """Click handler to update right ui when user clicks on a host in left box"""
        index = hosts_table_view.get_selected_index()
        hosts = DataShare.get_hosts()

        scan_details_view.host_name_entry_var.set(hosts[index].get_display_name())
        scan_details_view.mac_address_entry_var.set(hosts[index].get_mac_address())
        scan_details_view.port_number_entry_var.set(hosts[index].get_ip())

    def donothing():
        filewin = Toplevel(root)
        button = Button(filewin, text="Do nothing button")
        button.pack()

    def update_import():
        # Only takes json currently.
        #path = askopenfilename(title='Select Database file to import...', defaultextension='.db', filetypes=(("database files", "*.db"),("datafeeds", "*.json"),("all files", "*.*")))
        path = askopenfilename(title='Select Database file to import...', filetypes=[('Json', '*.json')])

        # ntpath for os compatibility with differing separators
        # head and tail if path ends in backslash
        head, tail = ntpath.split(path)
        fname = tail or ntpath.basename(head)

        if fname.endswith('.json'):
        # for use to support multiple file types
        # elif json_fp.endswith(('.json', '.db', '.xml'):
            df.DBFunctions.import_NVD_JSON(fname)
        else:
            tk.messagebox.showerror("Error", "File must be of type: json")

    class TreeColumns(enum.Enum):
        name = 0
        mac_address = 1

        @staticmethod
        def display_name_for_column(col):
            display_names = {
                0: "ip",
                1: "name",
            }
            return display_names[col]

        @staticmethod
        def all_cases():
            cases = []

            for col in TreeColumns:
                cases.append(TreeColumns.display_name_for_column(col.value))

            return cases

    # Setup root ui

    root = ThemedTk()
    root.ttkStyle = ThemedStyle()
    # Themes
    # "'alt', 'scidsand', 'classic', 'scidblue', 'scidmint', 'scidgreen', 'equilux', 'default', 'scidpink', 'aqua',
    # 'scidgrey', 'scidpurple', 'clam')
    root.ttkStyle.set_theme("equilux")
    root.title("GlenTest")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    #################
    # Setup LeftFrame
    #################
    left_frame = ttk.Frame(root)
    left_frame.grid(row=0, column=0, sticky="nsew")
    left_frame.grid_rowconfigure(1, weight=1)
    left_frame.grid_columnconfigure(0, weight=1)

    # Setup Left Frame header Label
    left_frame_header_label_var = tk.StringVar()
    update_left_header_label(None)
    left_frame_header_label = ttk.Label(left_frame, textvariable=left_frame_header_label_var)
    left_frame_header_label.grid(row=0, column=0)

    # Setup Left Frame Host TableView
    sections_tuple = TreeColumns.all_cases()
    data = []
    hosts_table_view = TableView(left_frame, 1, sections_tuple, data)
    hosts_table_view.bind_method('<ButtonRelease-1>', on_host_tableview_select)
    reload_hosts_tableview()

    # Setup scan host frame
    scan_host_frame = ttk.Frame(left_frame)
    scan_host_frame.grid(row=2, column=0)

    # Setup scan host label
    scan_host_label = ttk.Label(scan_host_frame, text="Hosts:")
    scan_host_label.grid(row=0, column=0)

    # Setup scan host entry
    scan_host_entry_var = tk.StringVar()
    scan_host_entry_var.set("192.168.1.0/28")
    scan_host_entry = ttk.Entry(scan_host_frame, textvariable=scan_host_entry_var)
    scan_host_entry.grid(row=0, column=1)

    ## Setup scan port label frame
    scan_port_label_frame = ttk.Frame(left_frame)
    scan_port_label_frame.grid(row=3, column=0)

    ## Setup scan port label
    port_start_label = ttk.Label(scan_port_label_frame, text="Start Port")
    port_start_label.grid(row=0, column=0, padx=(0, 8))
    port_end_label = ttk.Label(scan_port_label_frame, text="End Port")
    port_end_label.grid(row=0, column=1, padx=(8, 0))

    ## Setup scan port frame
    scan_port_frame = ttk.Frame(left_frame)
    scan_port_frame.grid(row=4, column=0)

    ## Setup scan port entries
    port_start_entry_var = tk.StringVar()
    port_start_entry_var.set("21")
    port_start_entry = ttk.Entry(scan_port_frame, width=4, textvariable=port_start_entry_var)
    port_start_entry.grid(row=0, column=0, padx=(0, 16))

    port_end_entry_var = tk.StringVar()
    port_end_entry_var.set("30")
    port_end_entry = ttk.Entry(scan_port_frame, width=4, textvariable=port_end_entry_var)
    port_end_entry.grid(row=0, column=1, padx=(16, 0))

    scan_button_frame = ttk.Frame(left_frame)
    scan_button_frame.grid(row=5, column=0)

    # Setup Left frame scan button
    scan_button = ttk.Button(scan_button_frame,
                            text="Scan",
                            command=on_scan)

    scan_button.grid(row=0, column=0, pady=(8, 8))

    #################
    # Setup RightFrame
    #################


    # Setup Notebook for right frame
    rows = 0
    while rows < 50:
        root.columnconfigure(rows + 1, weight=1)
        rows += 1

    # Setup Root Notebook
    main_note_book = ttk.Notebook(root)

    main_note_book.grid(row=0, column=1, columnspan=50, rowspan=49, sticky="NESW")

    # Setup Scan Details Tab
    scan_details_view = ScanDetailsView()
    scan_details_tab = scan_details_view.get_view(main_note_book)
    main_note_book.add(scan_details_tab, text="Scan Details")

    # Setup Vulnerabilities Tab
    vulnerabilities_view = VulnerabilitiesView()
    vulnerabilities_tab = vulnerabilities_view.get_view(main_note_book)
    main_note_book.add(vulnerabilities_tab, text="Vulnerabilities")
    vulnerabilities_view.on_selected_cve = find_exploit
    vulnerabilities_view.move_to_exploit = update_exploit_tab

    # Setup Exploits Tab
    exploit_view = ExploitView()
    exploit_tab = exploit_view.get_view(main_note_book)
    main_note_book.add(exploit_tab, text='Exploits')

    # Setup Scan History Tab
    scan_history_view = ScanHistoryView()
    scan_history_tab = scan_history_view.get_view(main_note_book)
    main_note_book.add(scan_history_tab, text="Scan History")
    scan_history_view.on_selected_scan_completion = on_select_scan

    # File Menu Bar
    menubar = Menu(root)  # create menu bar
    filemenu = Menu(menubar, tearoff=0)  # create a menu to add some stuff too

    # Save Vulnerability in file menu bar
    savemenu = Menu(menubar, tearoff=0)
    savemenu.add_command(label="Save Vulnerability", command=VulnPopup.new_popup)
    filemenu.add_cascade(label='Save', menu=savemenu)

    # DB import in file menu bar
    importmenu = Menu(menubar, tearoff=0)
    importmenu.add_command(label="Database", command=update_import)
    filemenu.add_cascade(label="Import", menu=importmenu)

    filemenu.add_separator()  # more prettiness

    # Scan settings in file menu bar
    settingsmenu = Menu(menubar, tearoff=0)
    settingsmenu.add_command(label="Scan Settings", command=scan_details_view.on_settings)
    filemenu.add_cascade(label='Settings', menu=settingsmenu)
    filemenu.add_separator()  # pretty

    def change_theme(theme):
        root.ttkStyle.set_theme(theme)

    themesmenu = Menu(menubar, tearoff=0)
    themesmenu.add_command(label="Alt", command=lambda: change_theme("alt"))
    themesmenu.add_command(label="Aqua", command=lambda: change_theme("aqua"))
    themesmenu.add_command(label="Clam", command=lambda: change_theme("clam"))
    themesmenu.add_command(label="Classic", command=lambda: change_theme("classic"))
    themesmenu.add_command(label="Default", command=lambda: change_theme("default"))
    themesmenu.add_command(label="Equilux", command=lambda: change_theme("equilux"))
    themesmenu.add_command(label="Scidblue", command=lambda: change_theme("scidblue"))
    themesmenu.add_command(label="Scidgreen", command=lambda: change_theme("scidgreen"))
    themesmenu.add_command(label="Scidgrey", command=lambda: change_theme("scidgrey"))
    themesmenu.add_command(label="Scidmint", command=lambda: change_theme("scidmint"))
    themesmenu.add_command(label="Scidpink", command=lambda: change_theme("scidpink"))
    themesmenu.add_command(label="Scidpurple", command=lambda: change_theme("scidpurple"))
    themesmenu.add_command(label="Scidsand", command=lambda: change_theme("scidsand"))

    filemenu.add_cascade(label='Themes', menu=themesmenu)
    filemenu.add_separator()  # pretty
    filemenu.add_command(label="Exit", command=root.quit)

    editmenu = Menu(menubar, tearoff=0)  # create another menu to add some stuff too
    editmenu.add_command(label="Undo", command=donothing)
    
    menubar.add_cascade(label="File", menu=filemenu)  # add file to menu bar
    # On macOS there are some default things added to this menu, but are not added to the same menu
    # under File. 
    menubar.add_cascade(label='Edit', menu=editmenu)  # add edit to menu bar too, for fun

    # Run the program with UI
    root.config(menu=menubar)
    root.geometry("800x500")
    root.minsize(800, 500)
    root.mainloop()


#  Runs the main method if this file is called to run
if __name__ == '__main__':
    def is_win_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False


    def is_root():
        return os.getuid() == 0


    if platform.system() == 'Windows':
        if is_win_admin():
            db_location = Path("vulnDB.db")
            if not db_location.exists():
                df.DBFunctions.build_db()
                # Maybe abstract this out for user controller importing
                df.DBFunctions.import_NVD_JSON()

            main()
        else:
            # todo handle rejection of UAC prompt gracefully
            # restarts with admin privileges
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    else:
        if not is_root():
            # todo ensure works on pi and test further
            # recreates process with AppleScript, sudo, or other appropriate command
            # attempts graphical escalation first
            elevate()
        db_location = Path("vulnDB.db")
        if not db_location.exists():
            df.DBFunctions.build_db()
            df.DBFunctions.import_NVD_JSON()
        main()
