from udpeasy import client
from udpeasy.packet import Packet
from basic_format import *
import sys

PORT = 5555
HOST = "0.0.0.0"
addr = (HOST, PORT)

class Client(client.Client):
    def __init__(self, host, port):
        super().__init__(host, port)

    def run_loop(self):
        while not self.dead:
            """handle responses from the server"""
            self.send(Packet(SamplePacketType.MESSAGE, self.sequence_number, SamplePayloadFormat.MESSAGE.pack("hello, world!".encode())))

            if self.die:
                self.dead = True

if __name__ == "__main__":
    if "-l" in sys.argv:
        HOST = "localhost"
    client = Client(HOST,  PORT)
    client.start()
