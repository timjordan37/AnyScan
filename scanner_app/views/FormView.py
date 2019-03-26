from tkinter import ttk

class FormView:
    # Collection of FormRow Objects
    _rows = []
    _super_frame = None

    def __init__(self, frame, rows=None):
        self._super_frame = frame

        if rows is not None:
            self._rows = rows

        for index, row in enumerate(self._rows):
            row_frame = ttk.Frame(self._super_frame)
            row_frame.grid_columnconfigure(1, weight=1)

            if row.get_is_button_row():
                row_frame.grid(row=index, column=0)
                for btn_row_index, button_info in enumerate(row.get_button_infos()):
                    button = ttk.Button(row_frame, text = button_info[0], command = button_info[1])
                    button.grid(row=0, column=btn_row_index, pady=(8, 8))

            else:
                row_frame.grid(row=index, column=0, sticky="nsew")
                label = ttk.Label(row_frame, text=row.get_label_title())
                label.grid(row=0, column=0, padx=(16, 0))

                row.get_text_variable().set("")
                text_entry = ttk.Entry(row_frame, textvariable=row.get_text_variable())
                text_entry.grid(row=0, column=1, sticky="nsew", padx=(0, 16))


class FormRow:
    _label_title = None
    _type = None
    _input_view = None
    _textvariable = None
    _is_button_row = False
    _button_infos = []

    def __init__(self, label_title, textvariable, is_button_row=False):
        self._label_title = label_title
        self._textvariable = textvariable
        self._is_button_row = is_button_row

    def add_button(self, title, click_completion):
        if not self._is_button_row:
            return

        self._button_infos.append((title, click_completion))

    def get_is_button_row(self):
        return self._is_button_row

    def get_button_infos(self):
        return self._button_infos

    def get_label_title(self):
        return self._label_title

    def get_text_variable(self):
        return self._textvariable
