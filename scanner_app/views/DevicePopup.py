import tkinter as tk
from tkinter import ttk


class DevicePopup:
    model = ""
    cpe_uri = ""
    manufacturer = ""

    def __init__(self, device_details):
        self.model = device_details[0]
        self.cpe_uri = device_details[1]
        self.manufacturer = device_details[2]

    def new_popup(self):

        # Creating the Popup Window
        root = tk.Toplevel()
        root.wm_title("Device")
        device_popup = ttk.Frame(root)
        device_popup.grid(row=0, column=0, sticky="nsew")


        # Adding the fields to the popup
        related_mod = tk.Label(device_popup, text=self.model)
        related_mod_label = tk.Label(device_popup, text="Model")
        related_mod_label.grid(column=0, row=0, padx=5, pady=5)
        related_mod.grid(column=1, row=0, padx=5, pady=5)

        cpe_uri_entry = tk.Label(device_popup, text=self.cpe_uri)
        cpe_uri_label = tk.Label(device_popup, text="CPE URI")
        cpe_uri_label.grid(column=0, row=1, padx=5, pady=5)
        cpe_uri_entry.grid(column=1, row=1, padx=5, pady=5)

        manufacturer_entry = tk.Label(device_popup, text=self.manufacturer)
        manufacturer_label = tk.Label(device_popup, text="Manufacturer")
        manufacturer_label.grid(column=0, row=2, padx=5, pady=5)
        manufacturer_entry.grid(column=1, row=2, padx=5, pady=5)