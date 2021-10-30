import socket


class DatagramSocket:
    def __init__(self, port) -> None:
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def bind_socket(self, addr = ''):
        self.socket.bind((addr, self.port))

    def receive_buffer(self, bufsize = 32768):
        return self.socket.recv(bufsize)

    # Really hackish way of getting local ip.
    # https://stackoverflow.com/questions/166506/
    def get_local_ip(self):
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_socket.connect(('8.8.8.8', 1))
        return temp_socket.getsockname()[0]
