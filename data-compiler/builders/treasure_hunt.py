from core.builder import BaseBuilder


class TreasureMapBuilder(BaseBuilder):
    def compile(self, store):
        placename_lang_table = store.get_lang_table('PlaceName')

        map_table = store.get_table('Map')
        territory_type_table = store.get_table('TerritoryType')
        level_table = store.get_table('Level')
        treasure_spot_table = store.get_table('TreasureSpot',
            lambda x: {tuple((int(x) for x in x[0].split('.', 1))):x[1:] for x in x})

        for treasure_spot in treasure_spot_table:
            rank, map_number = treasure_spot.id
            level_id = treasure_spot.get_by_index(0)

            level = level_table.get(level_id)
            if not level:
                continue

            x = level.get_by_name('X')
            y = level.get_by_name('Y')
            z = level.get_by_name('Z')
            yaw = level.get_by_name('Yaw')
            radius = level.get_by_name('Radius')
            #  type_ = level.get_by_name('Type')  # == 40
            #  object_key = level.get_by_name('ObjectKey')
            map_id = level.get_by_name('Map')
            #  event_id = level.get_by_name('EventId')
            territory_id = level.get_by_name('Territory')

            map_ = map_table.get(map_id)
            territory = territory_type_table.get(territory_id)

            region_id = territory.get_by_name('PlaceName{Region}')
            place_id = territory.get_by_name('PlaceName')
            region_name = placename_lang_table.ja.get(region_id).get_by_name('Name')
            place_name = placename_lang_table.ja.get(place_id).get_by_name('Name')
            m_r = placename_lang_table.ja.get(map_.get_by_name('PlaceName{Region}')).get_by_name('Name')
            m_p = placename_lang_table.ja.get(map_.get_by_name('PlaceName')).get_by_name('Name')
            #  if map_id != territory.get_by_name('Map'):
            print(rank, map_number, (x, y, z), (yaw, radius), (region_name, place_name), (m_r, m_p))
