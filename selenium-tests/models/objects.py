import re


class RecipeRow:
    def __init__(self, row):
        self._row = row

    @property
    def name(self):
        return self.link.text

    @property
    def index(self):
        return int(self._row.find_element_by_tag_name('th').text)

    @property
    def link(self):
        td = self._tds()[0]
        return td.find_element_by_tag_name('a')

    @property
    def time(self):
        td = self._tds()[1]
        time = td.text.replace("'", "")
        return int(time)

    @property
    def difficulty(self):
        td = self._tds()[2]
        return -1  # TODO: do policzenia

    def _tds(self):
        return self._row.find_elements_by_tag_name('td')

    def go_to_details(self):
        self.link.click()

    def __repr__(self):
        return "RecipeRow: id: %d, name: %s, time: %d, difficulty: %d" % (
            self.index, self.name, self.time, self.difficulty)


class IngredientRow:
    def __init__(self, row):
        self._row = row
        self.name = self._row.find_element_by_tag_name('th').text
        self.amount, self.unit = self._decode_amount()

    def _decode_amount(self):
        text = self._row.find_element_by_tag_name('td').text
        match = re.match(r'(?P<amount>\d*) ?(?P<unit>[a-zA-Z]*)', text)
        return int(match.group('amount')), match.group('unit')

    def __repr__(self):
        return "IngredientRow: name: %s, amount: %d, unit: %s" % (self.name, self.amount, self.unit)
