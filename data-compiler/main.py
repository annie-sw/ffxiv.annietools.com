import sys
import os
import core.db
import flatbuffers

from core.builder import Store, BaseBuilder
from builders.textdb import TextBuilder
from builders.weather import WeatherRateBuilder
from builders.treasure_hunt import TreasureMapBuilder
from builders.gatherer import GatheringBuilder
from builders.fisher import FishingBuilder

import generated.Eorzea.DB
import generated.Eorzea.TextDB
import generated.Eorzea.WeatherMap
import generated.Eorzea.WeatherRate


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


class DataBuilder(BaseBuilder):
    def __init__(self, *args, **kwargs):
        super(DataBuilder, self).__init__(*args, **kwargs)
        self.add_builder(WeatherRateBuilder(name='WeatherMaps'))
        #  data_builder.add_builder(TreasureMapBuilder(name='TreasureMaps'))
        self.add_builder(GatheringBuilder(name='GatheringItems'))
        self.add_builder(FishingBuilder(name='FishingItems'))

    def build(self, builder, store, values):
        generated.Eorzea.DB.DBStart(builder)
        generated.Eorzea.DB.DBAddGatheringItems(builder, values['GatheringItems'])
        generated.Eorzea.DB.DBAddFishingItems(builder, values['FishingItems'])
        generated.Eorzea.DB.DBAddWeatherMaps(builder, values['WeatherMaps'])
        return generated.Eorzea.DB.DBEnd(builder)


def main(root_dir):
    out_path = sys.argv[1]

    text_builder = TextBuilder(name='text')
    data_builder = DataBuilder(name='data')

    builder = Builder(root_dir)
    builder.add_builder(text_builder)
    builder.add_builder(data_builder)

    builder.build(out_path)


if __name__ == '__main__':
    dbpath = os.path.join(os.path.abspath(''), '..', 'data')
    main(dbpath)
