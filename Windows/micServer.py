import socket


class DatagramSocket:
    def __init__(self, port) -> None:
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def bind_socket(self, addr = ''):
        self.socket.bind((addr, self.port))

    def receive_buffer(self, bufsize = 32768):
        return self.socket.recv(bufsize)

    def get_local_ip(self):
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)
