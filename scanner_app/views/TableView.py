import tkinter
from tkinter import ttk
from views.DetailsPopup import DetailsPopup

class TableView():

    """Sections is a list of strings, each string represents a section to be displayed"""
    _sections = None

    """The parent view which the table view will be displayed"""
    _parent_view = None

    """The grid row index which the table view will be displayed on the parent view"""
    _grid_row = None

    """Data is a list of lists to be displayed in the table view"""
    """Each List in this list should have the same amount of items as sections"""
    """When each list is iterated through, the value in each index will be displayed under the section with the same index"""
    _data = []


    _tree = None

    """
    sections: List of strings, the sections to be displayed
    data: List of lists, the data to be displayed, each list contains the items in the index that will be displayed in the tabel
    """
    def __init__(self, parent_view, grid_row, sections, data):

        def get_CVE(a):
            rowData = tree.focus()
            full_row = tree.item(rowData)
            cve_details = full_row['values']
            pop = DetailsPopup(cve_details)
            pop.new_popup()

        self._grid_row = grid_row
        self._parent_view = parent_view
        self._sections = sections

        tree = ttk.Treeview(self._parent_view, columns=tuple(self._sections))
        tree.grid(row=6, column=0, sticky="nsew", pady=(0, 8))

        for section in tuple(self._sections):
            tree.heading(section, text=section)
            tree.column(section, width=50)

        tree['show'] = 'headings'

        if len(data) != 0:
            i = 0
            for collection in data:
                tree.insert("", i, values=tuple(collection))
            i += 1


        tree.bind('<Double-Button-1>', get_CVE)
        self._tree = tree

    def reload_data(self, data):
        print("DATA: ", data)
        for i in self._tree.get_children():
            self._tree.delete(i)

        if len(data) != 0:
            i = 0
            for collection in data:
                self._tree.insert("", i, values=tuple(collection))
            i += 1

    def get_selected_item(self):
        selected_item = self._tree.focus()

        return self._tree.item(selected_item)
