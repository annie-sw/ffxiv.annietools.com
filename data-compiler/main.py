import sys
import os
import core.db
import itertools
import flatbuffers
import generated.Eorzea.DB
import generated.Eorzea.TextDB
import generated.Eorzea.WeatherMap
import generated.Eorzea.WeatherRate


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


class Writer(BaseBuilder):
    pass


class Builder(BaseBuilder):
    def __init__(self, db_root):
        super(Builder, self).__init__()
        self.store = Store(core.db.DB(db_root))

    def build(self, out_path):
        self.precompile(self.store)
        self.compile(self.store)
        self.postcompile(self.store)

        for builder in self.builders:
            buf = builder.output(self.store)
            with open(os.path.join(out_path, builder.name), 'wb') as f:
                f.write(buf)


class TextBuilder(BaseBuilder):
    def build(self, builder, store, values):
        generated.Eorzea.TextDB.TextDBStart(builder)
        generated.Eorzea.TextDB.TextDBAddPlaceNames(builder, values['PlaceNames'])
        generated.Eorzea.TextDB.TextDBAddWeatherNames(builder, values['WeatherNames'])
        return generated.Eorzea.TextDB.TextDBEnd(builder)


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


class DataBuilder(BaseBuilder):
    def build(self, builder, store, values):
        generated.Eorzea.DB.DBStart(builder)
        generated.Eorzea.DB.DBAddWeatherMaps(builder, values['WeatherMaps'])
        return generated.Eorzea.DB.DBEnd(builder)


class MapBuilder(BaseBuilder):
    pass


class WeatherRateBuilder(BaseBuilder):
    def compile(self, store):
        map_table = store.get_table('Map')
        territory_table = store.get_table('TerritoryType')
        weather_rate_table = store.get_table('WeatherRate')
        weather_group_table = store.get_table('WeatherGroup',
                lambda x: {int(float(x[0])):x[1:] for x in x if int(x[0].split('.', 1)[1]) == 0})

        place_list = []

        for map_data in map_table:
            id_str = map_data.get_by_name('Id')
            if not id_str:
                continue

            region_id = map_data.get_by_name('PlaceName{Region}')
            placename_id = map_data.get_by_name('PlaceName')

            territory_id = map_data.get_by_name('TerritoryType')
            territory_data = territory_table.get(territory_id)
            if not territory_data:
                continue

            #  if territory_data.get_by_name('TerritoryIntendedUse') == 0:
                #  continue

            weather_rate_id = territory_data.get_by_name('WeatherRate')
            if weather_rate_id < 0:
                continue

            weather_group_data = weather_group_table.get(weather_rate_id)
            if weather_group_data:
                weather_rate_id = weather_group_data.get_by_name('WeatherRate')

            weather_rate_data = weather_rate_table.get(weather_rate_id)
            if not weather_rate_data or not (0 < int(weather_rate_data.get_by_name('Rate[0]')) < 100):
                continue

            place_list.append((region_id, placename_id, weather_rate_id))


        place_list = sorted(set(place_list))

        store.place_name_ids |= set(itertools.chain(*[(region, place) for region, place, _ in place_list]))

        self.place_list = place_list
        self.weather_rate_ids = sorted(list(set(rate for _, _, rate in place_list)))

        weather_name_ids = []
        for rate_id in self.weather_rate_ids:
            r = weather_rate_table.get(rate_id)
            weather_name_ids += [r.get_by_name('Weather[{}]'.format(x)) for x in range(8)]
        store.weather_name_ids |= set(weather_name_ids)

    def build(self, builder, store):
        weather_rate_map = {}
        weather_rate_table = store.get_table('WeatherRate')

        for rate_id in self.weather_rate_ids:
            r = weather_rate_table.get(rate_id)

            weathers = [r.get_by_name('Weather[{}]'.format(i)) for i in range(8)]
            rates = [r.get_by_name('Rate[{}]'.format(i)) for i in range(8)]

            generated.Eorzea.WeatherRate.WeatherRateStartWeathersVector(builder, 8)
            for v in weathers:
                builder.PrependByte(store.weather_name_map[v])
            weathers_offset = builder.EndVector(8)

            generated.Eorzea.WeatherRate.WeatherRateStartRatesVector(builder, 8)
            for v in rates:
                builder.PrependByte(v)
            rates_offset = builder.EndVector(8)

            generated.Eorzea.WeatherRate.WeatherRateStart(builder)
            generated.Eorzea.WeatherRate.WeatherRateAddWeathers(builder, weathers_offset)
            generated.Eorzea.WeatherRate.WeatherRateAddRates(builder, rates_offset)
            offset = generated.Eorzea.WeatherRate.WeatherRateEnd(builder)
            weather_rate_map[rate_id] = offset

        weather_maps = []
        for region, place, rate_id in self.place_list:
            generated.Eorzea.WeatherMap.WeatherMapStart(builder)
            generated.Eorzea.WeatherMap.WeatherMapAddRegion(builder, store.place_name_map[region])
            generated.Eorzea.WeatherMap.WeatherMapAddPlace(builder, store.place_name_map[place])
            generated.Eorzea.WeatherMap.WeatherMapAddRate(builder, weather_rate_map[rate_id])
            offset = generated.Eorzea.WeatherMap.WeatherMapEnd(builder)
            weather_maps.append(offset)

        generated.Eorzea.DB.DBStartWeatherMapsVector(builder, len(self.place_list))
        for offset in reversed(weather_maps):
            builder.PrependUOffsetTRelative(offset)
        weather_maps = builder.EndVector(len(self.place_list))
        return weather_maps


def main(root_dir):
    out_path = sys.argv[1]

    text_builder = TextBuilder(name='text')
    text_builder.add_builder(PlaceNameBuilder(name='PlaceNames'))
    text_builder.add_builder(WeatherNameBuilder(name='WeatherNames'))

    data_builder = DataBuilder(name='data')
    data_builder.add_builder(WeatherRateBuilder(name='WeatherMaps'))

    builder = Builder(root_dir)
    builder.add_builder(text_builder)
    builder.add_builder(data_builder)

    builder.build(out_path)


if __name__ == '__main__':
    dbpath = os.path.join(os.path.abspath(''), '..', 'data')
    main(dbpath)
