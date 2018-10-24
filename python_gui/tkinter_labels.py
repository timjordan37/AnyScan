import tkinter as tk

root = tk.Tk()

# Label with red text color
red1 = tk.Label(root,
    text="This is red text",
    fg="red")
red1.pack()

# Label with blue text color, 
blue1 = tk.Label(root,
    text="This is the blue text",
    fg="blue",
    font="Arial")
blue1.pack()


root.mainloop()