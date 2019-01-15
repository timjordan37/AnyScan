import tkinter as tk

class ScanSettingsPopup():

    def __init__(self):
        print("Look, im a popup")

    @staticmethod
    def new_popup():
        # Creating the Popup Window
        popup = tk.Toplevel(padx=10, pady=10)
        popup.wm_title("New Popup")
