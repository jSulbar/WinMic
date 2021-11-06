# Class derived from python's standard socket, with just an extra function
# and of predetermined type UDP.
import socket

# UDP socket class
class DatagramSocket(socket.socket):
    def __init__(self, port, bufsize = 32768) -> None:
        # Init as UDP using local network
        socket.socket.__init__(self, socket.AF_INET, socket.SOCK_DGRAM)

        # Make socket reusable to disable TIME_WAIT between sockets
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.port = port
        self.bufsize = bufsize

    # Really hackish way of getting local ip.
    # https://stackoverflow.com/questions/166506/
    def get_local_ip(self = None):
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_socket.connect(('8.8.8.8', 1))
        return temp_socket.getsockname()[0]