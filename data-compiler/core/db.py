import os
import csv

class DB:
    class Any(dict):
        def __getattr__(self, name):
            return self[name]

    Lang = Any(
        EN = 'en',
        JA = 'ja',
        FR = 'fr',
        DE = 'de',
        )

    def __init__(self, root_dir):
        self.root_dir = root_dir

    def _load(self, filepath, parser):
        filepath = self.root_dir + filepath
        if os.path.exists(filepath):
            return ExdTable(filepath, parser)
        return None

    def get_table(self, name, parser=None):
        return self._load('/rawexd/' + name + '.csv', parser)

    def get_lang_table(self, name):
        return self.__class__.Any(**{x:self._load('/exd-all/' + name + '.' + x + '.csv', None) for x in self.Lang.values()})


class ExdTable:
    def __init__(self, filepath, parser=None):
        with open(filepath, 'r') as f:
            rows = [x for x in csv.reader(f)]
            self.col_idx = rows[0][1:]
            self.col_name = rows[1][1:]
            self.col_type = rows[2][1:]
            self.rows = (parser or self._default_parser)(rows[3:])

    def _default_parser(self, rows):
        return {int(x[0]):x[1:] for x in rows}

    def __iter__(self):
        for id in self.rows.keys():
            yield self.get(id)

    def get(self, id):
        if id in self.rows:
            return ExdRecord(self, id)
        return None


class ExdRecord:
    def __init__(self, table, id):
        self.table = table
        self.id = id

    def get_by_name(self, name):
        index = self.table.col_name.index(name)
        return self.get_by_index(index)

    def get_by_index(self, index):
        value = self.table.rows[self.id][index].strip()
        value_type = self.table.col_type[index].strip()
        if value_type == 'str':
            return value
        if value_type.startswith('bit'):
            return bool(value)
        if value_type == 'single' or value_type == 'double':
            return float(value)
        return int(value)
