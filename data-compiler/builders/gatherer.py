from core.builder import BaseBuilder
import generated.Eorzea.DB
import generated.Eorzea.GatheringItem
import generated.Eorzea.GatheringSpot


class GatheringBuilder(BaseBuilder):
    def compile(self, store):
        gathering_point_table = store.get_table('GatheringPoint')
        gathering_point_base_table = store.get_table('GatheringPointBase')
        gathering_item_table = store.get_table('GatheringItem')
        territory_type_table = store.get_table('TerritoryType')
        item_table = store.get_table('Item')

        def resolve_item_id(item_id):
            gathering_item = gathering_item_table.get(item_id)
            if gathering_item:
                item_id = gathering_item.get_by_name('Item')
                item = item_table.get(item_id)
                if item:
                    return item.id
            return 0

        spot_map = {}
        item_map = {}

        for gathering_point in gathering_point_table:
            base_id = gathering_point.get_by_name('GatheringPointBase')
            bonus0 = gathering_point.get_by_name('GatheringPointBonus[0]')
            bonus1 = gathering_point.get_by_name('GatheringPointBonus[1]')
            territory_type_id = gathering_point.get_by_name('TerritoryType')
            spot_id = gathering_point.get_by_name('PlaceName')
            sub_category_id = gathering_point.get_by_name('GatheringSubCategory')

            territory = territory_type_table.get(territory_type_id)
            if not territory:
                continue

            base = gathering_point_base_table.get(base_id)
            if not base:
                continue

            level = base.get_by_name('GatheringLevel')

            if level == 0:
                continue

            type_id = base.get_by_name('GatheringType')
            is_limited = base.get_by_name('IsLimited')
            item_ids = [resolve_item_id(base.get_by_name('Item[{}]'.format(x))) for x in range(8)]
            item_ids = [x for x in item_ids if x is not 0]

            if not item_ids:
                continue

            region_id = territory.get_by_name('PlaceName{Region}')
            place_id = territory.get_by_name('PlaceName')

            store.place_name_ids |= set([spot_id, region_id, place_id])
            store.item_name_ids |= set(item_ids)

            spot = dict(
                    level=level,
                    type_id=type_id,
                    sub_category_id=sub_category_id,
                    region_id=region_id,
                    place_id=place_id,
                    spot_id=spot_id,
                )

            spot_key = (type_id, level, spot_id)

            if spot_id in spot_map:
                for k in spot.keys():
                    if spot[k] != spot_map[spot_key][k]:
                        print (spot, spot_map[spot_key])
                        raise

            spot_map[spot_key] = spot

            for item_id in item_ids:
                m = item_map[item_id] = item_map.get(item_id) or set()
                m.add(spot_key)

        self.spot_map = spot_map
        self.item_map = item_map

    def build(self, builder, store):
        spot_map = {}

        spots = sorted(self.spot_map.items(), key=lambda x: x[0])
        #  spots = list(self.spot_map.items())
        for spot_key, spot in reversed(spots):
            generated.Eorzea.GatheringSpot.GatheringSpotStart(builder)
            generated.Eorzea.GatheringSpot.GatheringSpotAddLevel(builder, spot['level'])
            generated.Eorzea.GatheringSpot.GatheringSpotAddTypeId(builder, spot['type_id'])
            generated.Eorzea.GatheringSpot.GatheringSpotAddSpotId(builder, store.place_name_map[spot['spot_id']])
            generated.Eorzea.GatheringSpot.GatheringSpotAddRegionId(builder, store.place_name_map[spot['region_id']])
            generated.Eorzea.GatheringSpot.GatheringSpotAddPlaceId(builder, store.place_name_map[spot['place_id']])
            generated.Eorzea.GatheringSpot.GatheringSpotAddSubCategoryId(builder, spot['sub_category_id'])
            spot_map[spot_key] = generated.Eorzea.GatheringSpot.GatheringSpotEnd(builder)

        item_offsets = []

        items = sorted(self.item_map.items(), key=lambda x: x[0])
        for item_id, spot_keys in items:
            generated.Eorzea.GatheringItem.GatheringItemStartSpotsVector(builder, len(spot_keys))
            for spot_key in spot_keys:
                builder.PrependUOffsetTRelative(spot_map[spot_key])
            spots_offset = builder.EndVector(len(spot_keys))
            generated.Eorzea.GatheringItem.GatheringItemStart(builder)
            generated.Eorzea.GatheringItem.GatheringItemAddItemId(builder, store.item_name_map[item_id])
            generated.Eorzea.GatheringItem.GatheringItemAddSpots(builder, spots_offset)
            offset = generated.Eorzea.GatheringItem.GatheringItemEnd(builder)
            item_offsets.append(offset)

        generated.Eorzea.DB.DBStartGatheringItemsVector(builder, len(item_offsets))
        for offset in reversed(item_offsets):
            builder.PrependUOffsetTRelative(offset)
        gathering_items = builder.EndVector(len(item_offsets))
        return gathering_items
