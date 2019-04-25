class PaginationDataModel:
    """This class is responsible for the pagination of the  different exploit descriptions that are available to
    view on the 'Exploit' tab  when the user hits 'Next' or 'Prev'.
    """

    _items = []
    _cur_index = 0

    def __init__(self):
        """No items pagination
        """
        self._items = []

    def __init__(self, items):
        """Pagination with specified items
        """
        self._items = items

    def curr_item(self):
        """Return current item

        :return current item or None
        """
        if self._cur_index < len(self._items):
            return self._items[self._cur_index]
        else:
            return None

    def next_item(self):
        """Returns the next item in the lsit


        :return next item or None
        """
        next_index = self._cur_index + 1

        if next_index < len(self._items):
            self._cur_index += 1
            return self._items[self._cur_index]
        else:
            return None

    def prev_item(self):
        """Returns previous item in the list

        :return previous item or None
        """
        prev_index = self._cur_index - 1

        if prev_index >= 0 and prev_index < len(self._items):
            self._cur_index -= 1
            return self._items[self._cur_index]
        else:
            return None

    def has_next_item(self):
        """Check if there is a next item available

        :return true is there is next item
        """
        return self.next_item() is not None

    def has_prev_item(self):
        """Check if there is a previous item available

        :return true is there is a previous item
        """
        return self.prev_items() is not None

    def get_items_count(self):
        """Get total items

        :return: len of store items
        """
        return len(self._items)

    def get_curr_index(self):
        """Get current index in items

        :return current position of items
        """
        return self._cur_index
