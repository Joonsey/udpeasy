from udpeasy import server
from udpeasy.packet import Packet
from examples.basic_example_formats import *
import sys

HOST = "0.0.0.0"
PORT = 5555


class Server(server.Server):
    def __init__(self, host, port) -> None:
        super().__init__(host, port)

    def handle_request(self, data, client_address):
        packet = Packet.deserialize(data)
        if packet.packet_type == SamplePacketType.MESSAGE:
            message = SamplePayloadFormat.MESSAGE.unpack(packet.payload)
            message = message[0].decode()
            # unpack always returns a tuple. Even if it is just one element
            print(message)


if __name__ == "__main__":
    if "-l" in sys.argv:
        HOST = "localhost"
    s = Server(HOST, PORT)
    s.run()
