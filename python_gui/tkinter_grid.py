from tkinter import *
import threading


def main():

    def search_for_device():
        device_name = device_name_entry.get()
        add_device(device_name)
        reload_listbox()
        device_name_var.set("")

    def add_device(device_name):
        if device_name == "":
            return
        if device_name in devices:
            return
        devices.append(device_name)

    def reload_listbox():
        listbox.delete(0, END)
        for device in devices:
            listbox.insert(END, device)

    def on_scan():

        if not listbox.curselection():
            scanning_label_var.set("No device selected")
            return

        scanning_label_var.set("Scanning '" + devices[listbox.curselection()[0]] + "' ...")
        timer.start()

    def finish_scan():
        scanning_label_var.set("Scan Completed :)")
        timer.cancel()


    ## Variables
    devices = []
    timer = threading.Timer(2, finish_scan)

    root = Tk()
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    ## Left Frame
    left_frame = Frame(root)
    left_frame.grid(row=0, column=0, sticky="nsew")
    left_frame.grid_rowconfigure(0, weight=1)
    left_frame.grid_columnconfigure(0, weight=1)

    # Setup Listbox
    listbox = Listbox(left_frame)
    listbox.grid(row=0, column=0, sticky="nsew", padx=(2, 0))

    ## Right Frame
    right_frame = Frame(root, bg="#EEEEEE")
    right_frame.grid(row=0, column=1, sticky="nsew")
    right_frame.grid_columnconfigure(0, weight=1)

    # title label
    title_label = Label(right_frame, text="Fake Scanner")
    title_label.grid(row=0, column=0, pady=(8, 8))

    # Device name entry
    device_name_var = StringVar()
    device_name_var.set("")
    device_name_entry = Entry(right_frame, textvariable=device_name_var)
    device_name_entry.grid(row=1, column=0, sticky="nsew", padx=(4, 4))

    # Scan & Search button
    button_frame = Frame(right_frame)
    button_frame.grid(row=2, column=0, pady=(32, 0))

    scan_button = Button(button_frame, text="Scan", command=on_scan)
    scan_button.pack(side="left", padx=(0, 8))

    search_button = Button(button_frame, text="Search", command=search_for_device)
    search_button.pack(side="right")

    # Scanning Label
    scanning_label_var = StringVar()
    scanning_label_var.set("")
    scanning_label = Label(right_frame, textvariable=scanning_label_var)
    scanning_label.grid(row=3, column=0, pady=(16, 0))

    root.geometry("400x200")
    root.minsize(400, 200)
    root.mainloop()

if __name__ == '__main__':
    main()
