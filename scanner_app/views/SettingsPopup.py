import tkinter as tk
from util import System


class SettingsPopup():

    def __init__(self):
        print("Look, im a popup")

    @staticmethod
    def new_popup():

        # Setup root ui
        root = tk.Toplevel()
        root.title("Scanner App - Settings")

        sort_settings_header_label = tk.Label(root, text="Host Display Settings", font='Helvetica 14 bold', anchor="w",
                                              width=24)
        sort_settings_header_label.grid(row=0, column=0)

        host_sort_radio_btn_frame = tk.Frame(root)
        host_sort_radio_btn_frame.grid(row=1, column=0, sticky="nsew")
        host_sort_radio_btn_frame.grid_rowconfigure(1, weight=1)
        host_sort_radio_btn_frame.grid_columnconfigure(0, weight=1)

        # setup sort options
        sort_options = []
        for opt in System.SortType:
            sort_options.append((System.SortType.display_name_for_sort_type(opt.value), opt.value))

        selection_var = tk.IntVar()
        sort_type = System.Settings.get_host_sort_type()
        selection_var.set(sort_type.value)

        def on_sort_select():
            new_sort_type = System.SortType.sort_type_for_int(selection_var.get())
            System.Settings.set_host_sort_type(new_sort_type)

        for name, value in sort_options:
            b = tk.Radiobutton(host_sort_radio_btn_frame, text=name, variable=selection_var, value=value,
                               command=on_sort_select, anchor="w", width=24, justify="left")
            b.pack()

        # setup vuln sort options
        vuln_sort_settings_header_label = tk.Label(root, text="Vulnerability Display Settings",
                                                   font='Helvetica 14 bold', anchor="w", width=24)
        vuln_sort_settings_header_label.grid(row=2, column=0)

        vuln_sort_radio_btn_frame = tk.Frame(root)
        vuln_sort_radio_btn_frame.grid(row=3, column=0, sticky="nsew")
        vuln_sort_radio_btn_frame.grid_rowconfigure(1, weight=1)
        vuln_sort_radio_btn_frame.grid_columnconfigure(0, weight=1)

        vuln_sort_options = []
        for opt in System.SortType:
            vuln_sort_options.append((System.SortType.display_name_for_sort_type(opt.value), opt.value))

        vuln_sort_selection_var = tk.IntVar()
        vuln_sort_type = System.Settings.get_vuln_sort_type()
        vuln_sort_selection_var.set(vuln_sort_type.value)

        def on_vuln_sort_select():
            new_sort_type = System.SortType.sort_type_for_int(vuln_sort_selection_var.get())
            System.Settings.set_vuln_sort_type(new_sort_type)

        for name, value in vuln_sort_options:
            b = tk.Radiobutton(vuln_sort_radio_btn_frame, text=name, variable=vuln_sort_selection_var, value=value,
                               command=on_vuln_sort_select, anchor="w", width=24, justify="left")
            b.pack()

        # setup scan type options
        scan_type_settings_header_label = tk.Label(root, text="Scan Type", font='Helvetica 14 bold', anchor="w",
                                                   width=24)
        scan_type_settings_header_label.grid(row=4, column=0, pady=(16, 0))

        scan_type_radio_btn_frame = tk.Frame(root)
        scan_type_radio_btn_frame.grid(row=5, column=0, sticky="nsew")
        scan_type_radio_btn_frame.grid_rowconfigure(1, weight=1)
        scan_type_radio_btn_frame.grid_columnconfigure(0, weight=1)

        scan_types = []
        for opt in System.ScanType:
            scan_types.append((System.ScanType.display_name_for_scan_type(opt.value), opt.value))

        scan_type_selection_var = tk.IntVar()
        scan_type = System.Settings.get_scan_type()
        scan_type_selection_var.set(scan_type.value)

        def on_scan_type_select():
            new_scan_type = System.ScanType.scan_type_for_int(scan_type_selection_var.get())
            System.Settings.set_scan_type(new_scan_type)

        for name, value in scan_types:
            b = tk.Radiobutton(scan_type_radio_btn_frame, text=name, variable=scan_type_selection_var, value=value,
                               command=on_scan_type_select, anchor="w", width=24, justify="left")
            b.pack()

        # setup pdf size options
        pdf_size_settings_header_label = tk.Label(root, text="Report PDF Size", font="Helvetica 14 bold", anchor="w",
                                                  width=24)
        pdf_size_settings_header_label.grid(row=6, column=0, pady=(16, 0))

        pdf_size_radio_btn_frame = tk.Frame(root)
        pdf_size_radio_btn_frame.grid(row=7, column=0, sticky="nsew")
        pdf_size_radio_btn_frame.grid_rowconfigure(1, weight=1)
        pdf_size_radio_btn_frame.grid_columnconfigure(0, weight=1)

        pdf_sizes = []
        for opt in System.PdfSize:
            pdf_sizes.append((System.PdfSize.display_name_for_pdf_size(opt.value), opt.value))

        pdf_size_selection_var = tk.IntVar()
        pdf_size = System.Settings.get_pdf_size()
        pdf_size_selection_var.set(pdf_size.value)

        def on_pdf_size_select():
            new_pdf_size = System.PdfSize.pdf_size_for_int(pdf_size_selection_var.get())
            System.Settings.set_pdf_size(new_pdf_size)

        for name, value in pdf_sizes:
            b = tk.Radiobutton(pdf_size_radio_btn_frame, text=name, variable=pdf_size_selection_var, value=value,
                               command=on_pdf_size_select, anchor="w", width=24, justify="left")
            b.pack()

        root.geometry("400x500")
        root.minsize(400, 500)
