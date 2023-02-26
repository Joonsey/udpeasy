import struct

class SamplePacketType:
    MESSAGE = 1

class SamplePayloadFormat:
    MESSAGE = struct.Struct("32s")

