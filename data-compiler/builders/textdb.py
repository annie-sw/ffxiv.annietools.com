from core.builder import BaseBuilder
import generated.Eorzea.TextDB


class TextBuilder(BaseBuilder):
    def __init__(self, *args, **kwargs):
        super(TextBuilder, self).__init__(*args, **kwargs)
        self.add_builder(ItemNameBuilder(name='ItemNames'))
        self.add_builder(PlaceNameBuilder(name='PlaceNames'))
        self.add_builder(WeatherNameBuilder(name='WeatherNames'))

    def build(self, builder, store, values):
        generated.Eorzea.TextDB.TextDBStart(builder)
        generated.Eorzea.TextDB.TextDBAddItemNames(builder, values['ItemNames'])
        generated.Eorzea.TextDB.TextDBAddPlaceNames(builder, values['PlaceNames'])
        generated.Eorzea.TextDB.TextDBAddWeatherNames(builder, values['WeatherNames'])
        return generated.Eorzea.TextDB.TextDBEnd(builder)


class ItemNameBuilder(BaseBuilder):
    def precompile(self, store):
        store.item_name_ids = set()
        store.item_name_map = {}

    def build(self, builder, store):
        itemname_lang_table = store.get_lang_table('Item')
        item_names = [(itemname_lang_table.ja.get(x).get_by_name('Name'), x) for x in store.item_name_ids]
        item_names = sorted(item_names, key=lambda x: x[0])
        item_names = [(builder.CreateString(n), x) for n, x in item_names]

        store.item_name_map = {v[1]:i for i, v in enumerate(item_names)}

        generated.Eorzea.TextDB.TextDBStartItemNamesVector(builder, len(item_names))
        for name, _ in reversed(item_names):
            builder.PrependUOffsetTRelative(name)
        return builder.EndVector(len(item_names))


class PlaceNameBuilder(BaseBuilder):
    def precompile(self, store):
        store.place_name_ids = set()
        store.place_name_map = {}

    def build(self, builder, store):
        placename_lang_table = store.get_lang_table('PlaceName')
        place_names = [(placename_lang_table.ja.get(x).get_by_name('Name'), x) for x in store.place_name_ids]
        place_names = sorted(place_names, key=lambda x: x[0])
        #  print ([(i, n, x) for i, (n, x) in enumerate(place_names)])
        place_names = [(builder.CreateString(n), x) for n, x in place_names]

        store.place_name_map = {v[1]:i for i, v in enumerate(place_names)}

        generated.Eorzea.TextDB.TextDBStartPlaceNamesVector(builder, len(place_names))
        for name, _ in reversed(place_names):
            builder.PrependUOffsetTRelative(name)
        return builder.EndVector(len(place_names))


class WeatherNameBuilder(BaseBuilder):
    def precompile(self, store):
        store.weather_name_ids = set()
        store.weather_name_map = {}

    def build(self, builder, store):
        weather_lang_table = store.get_lang_table('Weather')
        weather_names = [(weather_lang_table.ja.get(x).get_by_name('Name'), x) for x in store.weather_name_ids]
        weather_names = sorted(weather_names, key=lambda x: x[0])
        weather_names = [(builder.CreateString(n), x) for n, x in weather_names]

        store.weather_name_map = {v[1]:i for i, v in enumerate(weather_names)}

        generated.Eorzea.TextDB.TextDBStartWeatherNamesVector(builder, len(weather_names))
        for name, _ in reversed(weather_names):
            builder.PrependUOffsetTRelative(name)
        return builder.EndVector(len(weather_names))
