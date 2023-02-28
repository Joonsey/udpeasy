from abc import ABC, abstractmethod
import socket
from udpeasy.packet import *
import threading


class Client(ABC):
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = host
        self.port = port
        self.addr = (host, port)
        self.sequence_number = 0
        self.die = False
        self.dead = False

    def start(self):
        thread = threading.Thread(target=self.run_loop())
        thread.start()

    def stop(self):
        self.die = True

    def send(self, packet: Packet):
        self.sock.sendto(packet.serialize(), self.addr)

    @abstractmethod
    def run_loop(self):
        ...

