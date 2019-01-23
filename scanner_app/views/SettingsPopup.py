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

        sort_settings_header_label = tk.Label(root, text="Host Display Settings")
        sort_settings_header_label.grid(row=0, column=0)

        radio_btn_frame = tk.Frame(root)
        radio_btn_frame.grid(row=1, column=0, sticky="nsew")
        radio_btn_frame.grid_rowconfigure(1, weight=1)
        radio_btn_frame.grid_columnconfigure(0, weight=1)

        sort_options = []
        for type in System.SortType:
            sort_options.append((System.SortType.display_name_for_sort_type(type.value), type.value))

        selection_var = tk.IntVar()
        sort_type = System.Settings.get_host_sort_type()
        selection_var.set(sort_type.value)

        def on_select():
            new_sort_type = System.SortType.sort_type_for_int(selection_var.get())
            System.Settings.set_host_sort_type(new_sort_type)

        for name, value in sort_options:
            b = tk.Radiobutton(radio_btn_frame, text=name, variable=selection_var, value=value, command=on_select)
            b.pack()

        root.geometry("400x500")
        root.minsize(400, 500)
