
def main(root_dir):
    map_table = db.get_table('Map')
    placename_lang_table = db.get_lang_table('PlaceName')
    weather_lang_table = db.get_lang_table('Weather')
    territory_table = db.get_table('TerritoryType')
    weather_rate_table = db.get_table('WeatherRate')
    weather_group_table = db.get_table('WeatherGroup',
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

    place_name_ids = sorted(list(set(itertools.chain(*[(region, place) for region, place, _ in place_list]))))
    weather_rate_ids = sorted(list(set(rate for _, _, rate in place_list)))
    weather_name_ids = []
    for rate_id in weather_rate_ids:
        r = weather_rate_table.get(rate_id)
        weather_name_ids += [r.get_by_name('Weather[{}]'.format(x)) for x in range(8)]
    weather_name_ids = sorted(list(set(weather_name_ids)))

    builder = flatbuffers.Builder(0)

    place_names = [(builder.CreateString(placename_lang_table.ja.get(x).get_by_name('Name')), x) for x in place_name_ids]
    store.place_names_map = {x[1]:i for i, x in enumerate(place_names)}

    weather_names = [(builder.CreateString(weather_lang_table.ja.get(x).get_by_name('Name')), x) for x in weather_name_ids]
    store.weather_names_map = {x[1]:i for i, x in enumerate(weather_names)}

    generated.Eorzea.Text.TextStartPlaceNamesVector(builder, len(place_names))
    for name, _ in place_names:
        builder.PrependUOffsetTRelative(name)
    place_names = builder.EndVector(len(place_names))

    generated.Eorzea.Text.TextStartWeatherNamesVector(builder, len(weather_names))
    for name, _ in weather_names:
        builder.PrependUOffsetTRelative(name)
    weather_names = builder.EndVector(len(weather_names))

    generated.Eorzea.Text.TextStart(builder)
    generated.Eorzea.Text.TextAddPlaceNames(builder, place_names)
    generated.Eorzea.Text.TextAddWeatherNames(builder, weather_names)
    lang_data = generated.Eorzea.Text.TextEnd(builder)
    builder.Finish(lang_data)

    print (builder.Output(), len(builder.Output()))


    builder = flatbuffers.Builder(0)

    store.weather_rate_map = {}

    generated.Eorzea.DB.DBStartWeatherRatesVector(builder, len(weather_rate_ids))
    for i, rate_id in enumerate(weather_rate_ids):
        store.weather_rate_map[rate_id] = i
        r = weather_rate_table.get(rate_id)
        for i in range(8):
            weather = r.get_by_name('Weather[{}]'.format(i))
            rate = r.get_by_name('Rate[{}]'.format(i))
            generated.Eorzea.WeatherRate.CreateWeatherRate(builder,
                    store.weather_names_map[weather],
                    rate,
                    )
    weather_rates = builder.EndVector(len(weather_rate_ids))

    generated.Eorzea.DB.DBStart(builder)
    generated.Eorzea.DB.DBAddWeatherRates(builder, weather_rates)
    eorzea_db = generated.Eorzea.DB.DBEnd(builder)
    builder.Finish(eorzea_db)

    print (builder.Output(), len(builder.Output()))


    #  generated.Eorzea.Text.TextStartPlaceNamesVector(builder, len(placename_ids))
    #  for placename_id in placename_ids:
        #  name = placename_lang_table.ja.get(placename_id).get_by_name('Name')
        #  #  print(dir(builder))
        #  print(builder.CreateString(name))
        #  #  builder.PrependUOffsetTRelative(builder.CreateString(name))
    #  placenames = builder.EndVector(len(placename_ids))





    #  weather_rate_map = {
            #  rate_id: (
                #  [weather_rate_table.get(rate_id).get_by_name('Weather[{}]'.format(x)) for x in range(8)],
                #  [weather_rate_table.get(rate_id).get_by_name('Rate[{}]'.format(x)) for x in range(8)],
                #  )
            #  for rate_id
            #  in set(rate for region, place, rate in place_list)
            #  }

    #  lang_data = {
            #  'place': {x:placename_lang_table.ja.get(x).get_by_name('Name') for x in set(
            #  }

    #  for (region_id, placename_id, weather_rate_id) in
        #  print ( placename_lang_table.ja.get(region_id).get_by_name('Name'),
                #  placename_lang_table.ja.get(placename_id).get_by_name('Name'),
                #  region_id, placename_id, weather_rate_id)



if __name__ == '__main__':
    dbpath = os.path.join(os.path.abspath(''), '..', 'data')
    main(dbpath)
