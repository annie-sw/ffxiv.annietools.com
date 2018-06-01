# automatically generated by the FlatBuffers compiler, do not modify

# namespace: Eorzea

import flatbuffers

class GatheringItem(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsGatheringItem(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = GatheringItem()
        x.Init(buf, n + offset)
        return x

    # GatheringItem
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # GatheringItem
    def ItemId(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint16Flags, o + self._tab.Pos)
        return 0

    # GatheringItem
    def Spots(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from .FishingSpot import FishingSpot
            obj = FishingSpot()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # GatheringItem
    def SpotsLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

def GatheringItemStart(builder): builder.StartObject(2)
def GatheringItemAddItemId(builder, itemId): builder.PrependUint16Slot(0, itemId, 0)
def GatheringItemAddSpots(builder, spots): builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(spots), 0)
def GatheringItemStartSpotsVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def GatheringItemEnd(builder): return builder.EndObject()
