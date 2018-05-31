import itertools
from core.builder import BaseBuilder
import generated.Eorzea.DB
import generated.Eorzea.WeatherRate
import generated.Eorzea.WeatherMap


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
