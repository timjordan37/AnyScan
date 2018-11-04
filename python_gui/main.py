# Here is where we import the TKinter framework
# this gives us access to all of the GUI elements
import tkinter as tk

# intantiate the 'root' window element
root = tk.Tk()

# Here we are adding a simple label to the root window
w = tk.Label(root,
             text="This is the GUI for our app", # here we edit the text value
             fg="red") # here we edit the text color
w.pack() # here we provide the layout type for this element

root.mainloop() # The main loop method must be called to get the program to run