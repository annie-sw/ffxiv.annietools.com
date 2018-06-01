from core.builder import BaseBuilder
import generated.Eorzea.DB
import generated.Eorzea.FishingItem
import generated.Eorzea.FishingSpot


class FishingBuilder(BaseBuilder):
    def compile(self, store):
        fishing_spot_table = store.get_table('FishingSpot')
        territory_type_table = store.get_table('TerritoryType')
        item_table = store.get_table('Item')

        fish_map = {}
        spot_map = {}

        for fishing_spot in fishing_spot_table:
            level = fishing_spot.get_by_name('GatheringLevel')
            if level <= 0:
                continue

            territory_id = fishing_spot.get_by_name('TerritoryType')
            territory = territory_type_table.get(territory_id)
            if not territory:
                continue

            spot_category = fishing_spot.get_by_name('FishingSpotCategory')
            x = fishing_spot.get_by_name('X')
            z = fishing_spot.get_by_name('Z')
            radius = fishing_spot.get_by_name('Radius')
            spot_id = fishing_spot.get_by_name('PlaceName')
            item_ids = [fishing_spot.get_by_name('Item[{}]'.format(x)) for x in range(10)]
            item_ids = [x for x in item_ids if x is not 0]

            if not item_ids:
                continue

            region_id = territory.get_by_name('PlaceName{Region}')
            place_id = territory.get_by_name('PlaceName')

            store.place_name_ids |= set([spot_id, region_id, place_id])

            spot_map[fishing_spot.id] = dict(
                    level=level,
                    x=x,
                    z=x,
                    radius=radius,
                    spot_category=spot_category,
                    region_id=region_id,
                    place_id=place_id,
                    spot_id=spot_id,
                )

            for item_id in item_ids:
                m = fish_map[item_id] = fish_map.get(item_id) or set()
                m.add(fishing_spot.id)

        store.item_name_ids |= set(fish_map.keys())

        self.spot_map = spot_map
        self.item_map = fish_map

    def build(self, builder, store):
        spot_map = {}

        spots = sorted(self.spot_map.items(), key=lambda x: x[0])
        for spot_id, spot in reversed(spots):
            generated.Eorzea.FishingSpot.FishingSpotStart(builder)
            generated.Eorzea.FishingSpot.FishingSpotAddLevel(builder, spot['level'])
            generated.Eorzea.FishingSpot.FishingSpotAddX(builder, spot['x'])
            generated.Eorzea.FishingSpot.FishingSpotAddZ(builder, spot['z'])
            generated.Eorzea.FishingSpot.FishingSpotAddRadius(builder, spot['radius'])
            generated.Eorzea.FishingSpot.FishingSpotAddSpotId(builder, store.place_name_map[spot['spot_id']])
            generated.Eorzea.FishingSpot.FishingSpotAddRegionId(builder, store.place_name_map[spot['region_id']])
            generated.Eorzea.FishingSpot.FishingSpotAddPlaceId(builder, store.place_name_map[spot['place_id']])
            generated.Eorzea.FishingSpot.FishingSpotAddSpotCategory(builder, spot['spot_category'])
            spot_map[spot_id] = generated.Eorzea.FishingSpot.FishingSpotEnd(builder)

        item_offsets = []

        items = sorted(self.item_map.items(), key=lambda x: x[0])
        for item_id, spot_ids in items:
            generated.Eorzea.FishingItem.FishingItemStartSpotsVector(builder, len(spot_ids))
            for spot_id in spot_ids:
                builder.PrependUOffsetTRelative(spot_map[spot_id])
            spots_offset = builder.EndVector(len(spot_ids))
            generated.Eorzea.FishingItem.FishingItemStart(builder)
            generated.Eorzea.FishingItem.FishingItemAddItemId(builder, store.item_name_map[item_id])
            generated.Eorzea.FishingItem.FishingItemAddSpots(builder, spots_offset)
            offset = generated.Eorzea.FishingItem.FishingItemEnd(builder)
            item_offsets.append(offset)

        generated.Eorzea.DB.DBStartFishingItemsVector(builder, len(item_offsets))
        for offset in reversed(item_offsets):
            builder.PrependUOffsetTRelative(offset)
        fishing_items = builder.EndVector(len(item_offsets))
        return fishing_items

