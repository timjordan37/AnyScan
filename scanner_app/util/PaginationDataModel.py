
class PaginationDataModel:

    _items = []
    _cur_index = 0

    def __init__(self):
        self._items = []

    def __init__(self, items):
        self._items = items

    def curr_item(self):
        if self._cur_index < len(self._items):
            return self._items[self._cur_index]
        else:
            return None

    def next_item(self):
        next_index = self._cur_index + 1

        if next_index < len(self._items):
            self._cur_index += 1
            return self._items[self._cur_index]
        else:
            return None

    def prev_item(self):
        prev_index = self._cur_index - 1

        if prev_index >= 0 and prev_index < len(self._items):
            self._cur_index -= 1
            return self._items[self._cur_index]
        else:
            return None

    def has_next_item(self):
        return self.next_item() is not None

    def has_prev_item(self):
        return self.prev_items() is not None

    def get_items_count(self):
        return len(self._items)

    def get_curr_index(self):
        return self._cur_index
