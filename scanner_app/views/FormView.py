from tkinter import ttk
import tkinter as tk
import enum

"""
The following class sets up a collection of FormRow objects that are responsible for the information that is displayed
within the 'Description' box on the 'Exploit' tab.  When users select a CVE and views exploit details, they can hit the
'Next' and 'Prev' buttons and the 'Description' text box will update with the valid exploit information as long as 
there are multiple exploits associated with the selected CVE.
"""


class FormView:
    """Collection of FormRow Objects"""

    _rows = []
    _super_frame = None

    def update(self):
        updateable_rows = filter(lambda row: row.get_type() == FormRowType.text, self._rows)

        for row in updateable_rows:
            row.update()

    def __init__(self, frame, rows=None):
        self._super_frame = frame

        if rows is not None:
            self._rows = rows

        for index, row in enumerate(self._rows):
            row_frame = ttk.Frame(self._super_frame)
            row_frame.grid_columnconfigure(1, weight=1)

            row_type = row.get_type()

            if row_type == FormRowType.entry:
                row_frame.grid(row=index, column=0, sticky="nsew")
                label = ttk.Label(row_frame, text=row.get_label_title())
                label.grid(row=0, column=0, padx=(16, 0))

                row.get_text_variable().set("")
                text_entry = ttk.Entry(row_frame, textvariable=row.get_text_variable())
                text_entry.grid(row=0, column=1, sticky="nsew", padx=(0, 16))
            elif row_type == FormRowType.text:
                row_frame.grid(row=index, column=0, sticky="nsew")
                label = ttk.Label(row_frame, text=row.get_label_title())
                label.grid(row=0, column=0, padx=(16, 0))

                row.get_text_variable().set("")
                text_view = tk.Text(row_frame, height=10)
                text_view.grid(row=0, column=1, sticky="nsew", padx=(0, 16))
                row._input_view = text_view
            elif row_type == FormRowType.button:
                row_frame.grid(row=index, column=0)
                for btn_row_index, button_info in enumerate(row.get_button_infos()):
                    button = ttk.Button(row_frame, text=button_info[0], command=button_info[1])
                    button.grid(row=0, column=btn_row_index, pady=(8, 8))


class FormRow:
    _label_title = None
    _type = None
    _input_view = None
    _textvariable = None
    _button_infos = []
    _update_completion = None

    def __init__(self, label_title, textvariable, type=None):
        self._label_title = label_title
        self._textvariable = textvariable
        if type is None:
            type = FormRowType.entry
        self._type = type

    def add_button(self, title, click_completion):
        if not self._type == FormRowType.button:
            return

        self._button_infos.append((title, click_completion))

    def get_button_infos(self):
        return self._button_infos

    def get_label_title(self):
        return self._label_title

    def get_text_variable(self):
        return self._textvariable

    def get_type(self):
        return self._type

    def update(self):
        if self._type == FormRowType.text:
            self._input_view.delete(1.0, tk.END)
            self._input_view.insert(tk.END, self._textvariable.get())


class FormRowType(enum.Enum):
    entry = 0
    text = 1
    button = 2
