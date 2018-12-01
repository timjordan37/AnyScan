import tkinter as tk
from util import DBFunctions as df
from tkinter import messagebox


class DevicePopup():

    @staticmethod
    def new_popup():
        model = ""
        cpe_uri = ""
        manufacturer = ""

        # Creating the Popup Window
        device_popup = tk.Toplevel(padx=10, pady=10)
        device_popup.wm_title("Add Device")

        # Adding the fields to the popup
        related_mod = tk.Entry(device_popup, textvariable=model)
        related_mod_label = tk.Label(device_popup, text="Model")
        related_mod_label.grid(column=0, row=0, padx=5, pady=5)
        related_mod.grid(column=1, row=0, padx=5, pady=5)

        cpe_uri_entry = tk.Entry(device_popup, textvariable=cpe_uri)
        cpe_uri_label = tk.Label(device_popup, text="CPE URI")
        cpe_uri_label.grid(column=0, row=1, padx=5, pady=5)
        cpe_uri_entry.grid(column=1, row=1, padx=5, pady=5)

        manufacturer_entry = tk.Entry(device_popup, textvariable=manufacturer)
        manufacturer_label = tk.Label(device_popup, text="Manufacturer")
        manufacturer_label.grid(column=0, row=2, padx=5, pady=5)
        manufacturer_entry.grid(column=1, row=2, padx=5, pady=5)

        # Function to call the save vulnerability function
        def save_device():

            if df.DBFunctions.save_device(model, manufacturer, cpe_uri):
                messagebox.showinfo("Success", "Device Saved Successfully")
            else:
                messagebox.showinfo("Failure", "Device Did Not Save Correctly")

            device_popup.destroy()

        # Adding the save button to the popup window
        save_button = tk.Button(device_popup, text="Save", command=save_device)
        save_button.grid(columnspan=2, row=16, padx=5, pady=5)