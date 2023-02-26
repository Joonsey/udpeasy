import struct
import time

class Packet:
    HEADER_SIZE = struct.calcsize('IfIII')
    MAGIC_NUMBER = 0xDEADBEEF

    def __init__(self, packet_type, sequence_number, payload):
        self.packet_type = packet_type
        self.sequence_number = sequence_number
        self.time = time.time()
        self.payload = payload

    def serialize(self):
        magic_number_bytes = struct.pack('I', self.MAGIC_NUMBER)
        time_bytes = struct.pack('f', self.time)
        packet_type_bytes = struct.pack('I', self.packet_type)
        sequence_number_bytes = struct.pack('I', self.sequence_number)
        payload_length_bytes = struct.pack('I', len(self.payload))

        headers = magic_number_bytes + time_bytes + packet_type_bytes + sequence_number_bytes + payload_length_bytes
        serialized_packet = headers + self.payload

        return serialized_packet

    @classmethod
    def deserialize(cls, serialized_data):
        if len(serialized_data) < Packet.HEADER_SIZE:
            raise ValueError("Invalid packet - packet is too short")

        magic_number, time, packet_type, sequence_number, payload_length = struct.unpack('IIIII', serialized_data[:Packet.HEADER_SIZE])

        if magic_number != Packet.MAGIC_NUMBER:
            raise ValueError("Invalid packet - magic number mis-match of packets. \npacket will be disqualified")
        payload = serialized_data[Packet.HEADER_SIZE: Packet.HEADER_SIZE+ payload_length]

        packet = Packet(packet_type, sequence_number, payload)
        packet.time = time
        return packet
