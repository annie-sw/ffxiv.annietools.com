import flatbuffers


class Store:
    def __init__(self, db):
        self.db = db
        self.cached_table = {}
        self.cached_lang_table = {}

    def get_table(self, name, *args, **kwargs):
        table = self.cached_table.get(name)
        if not table:
            table = self.cached_table[name] = self.db.get_table(name, *args, **kwargs)
        return table

    def get_lang_table(self, name):
        table = self.cached_lang_table.get(name)
        if not table:
            table = self.cached_lang_table[name] = self.db.get_lang_table(name)
        return table


class BaseBuilder:
    def __init__(self, name=None):
        self.builders = []
        self.name = name

    def add_builder(self, builder):
        self.builders.append(builder)

    def precompile(self, store):
        for builder in self.builders:
            builder.precompile(store)

    def compile(self, store):
        for builder in self.builders:
            builder.compile(store)

    def postcompile(self, store):
        for builder in self.builders:
            builder.postcompile(store)

    def output(self, store):
        offset = 0
        fbs_builder = flatbuffers.Builder(0)
        values = {builder.name:builder.build(fbs_builder, store) for builder in self.builders}
        offset = self.build(fbs_builder, store, values)
        fbs_builder.Finish(offset)
        return fbs_builder.Output()

    def build(self, fbs_builder, store, values):
        return 0
