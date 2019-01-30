import tkinter as tk
from tkinter import ttk

print("Tabs Prototype started...")

# Setup root ui
root = tk.Tk()
root.title("Tabs Prototype")

rows = 0
while rows < 50:
    root.rowconfigure(rows, weight=1)
    root.columnconfigure(rows, weight=1)
    rows += 1

# Setup Root Notebook
main_note_book = ttk.Notebook(root)
main_note_book.grid(row=1, column=0, columnspan=50, rowspan=49, sticky="NESW")

# Setup Tab 1
tab1 = tk.Frame(main_note_book)
main_note_book.add(tab1, text="Tab 1")

# Setup Tab 1
tab2 = tk.Frame(main_note_book)
main_note_book.add(tab2, text="Tab 2")

# Run the program with UI
root.geometry("800x500")
root.minsize(800, 500)
root.mainloop()