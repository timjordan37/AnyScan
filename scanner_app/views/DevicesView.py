import tkinter as tk


class DevicesView:

    device_name_entry_var = None

    def get_view(self, parent_frame):
        self.device_name_entry_var = tk.StringVar()

        frame = tk.Frame(parent_frame)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)

        # header label
        header_label = tk.Label(frame, text="Devices")
        header_label.grid(row=0, column=0, pady=(8, 8))

        # Device Name Search

        # Not sure what we want to do with this page so I left this commented out

        #device_name_frame = tk.Frame(frame)
        #device_name_frame.grid(row=1, column=0, sticky="nsew")
        #device_name_frame.grid_columnconfigure(1, weight=1)

        #device_name_label = tk.Label(device_name_frame, text="Device Name:")
        #device_name_label.grid(row=0, column=0, padx=(16, 0))

        #self.device_name_entry_var.set("")
        #device_name_text_entry = tk.Entry(device_name_frame, textvariable=self.device_name_entry_var)
        #device_name_text_entry.grid(row=0, column=1, sticky="nsew", padx=(0, 16))

        return frame
