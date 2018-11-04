import tkinter as tk
from tkinter import StringVar
    
# Define a method to handle the updating of the label
def update_label():
    label_text.set(entry.get())


root = tk.Tk() # root window element
frame = tk.Frame(root) # add a separate frame into the root window
frame.pack()

# Setup Text
entry = tk.Entry(frame)
entry.pack()

# Setup Label
label_text = StringVar()
label_text.set('')
label = tk.Label(frame, textvariable=label_text)
label.pack()

# Setup buttons
slogan = tk.Button(frame,
                   text="Hello",
                   command=update_label)
slogan.pack()

root.mainloop()