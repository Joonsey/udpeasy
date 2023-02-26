import socket
from udpeasy.packet import *
import time
import sys
import threading


class Server:
    def __init__(self, host, port) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = host
        self.port = port
        self.last_packet_time = time.time()

    def handle_request(self, data, client_address):
        """overload this method"""
        pass

    def run(self):
        self.sock.bind((self.host, self.port))
        print(f"starting server...\nlistening on {(self.host, self.port)}")
        while True:
            data, client_address = self.sock.recvfrom(1024)

            threading.Thread(target=self.handle_request, args=(data, client_address)).start()
