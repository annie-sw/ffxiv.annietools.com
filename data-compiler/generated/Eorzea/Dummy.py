# automatically generated by the FlatBuffers compiler, do not modify

# namespace: Eorzea

import flatbuffers

class Dummy(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsDummy(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Dummy()
        x.Init(buf, n + offset)
        return x

    # Dummy
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

def DummyStart(builder): builder.StartObject(0)
def DummyEnd(builder): return builder.EndObject()
