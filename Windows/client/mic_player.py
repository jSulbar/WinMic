# Manages the thread in charge of fetching data from the network
# and writing it to the audio stream
from threading import Thread


# Class for microphone IO.
class MicPlayer:
    def __init__(self, stream, socket) -> None:
        self.running = False
        self.stream = stream
        self.socket = socket

    # Writes data to VBCable input
    def thread_target(self):
        while self.running:
            audio_data = self.socket.recv(self.socket.bufsize)
            self.stream.write(audio_data)
        self.stream.close()
        self.socket.close()

    # Sets the running flag to false,
    # stopping the thread
    def stop(self):
        self.running = False

    # Starts the thread with the given socket.
    def start(self):
        self.running = True
        thread = Thread(target=self.thread_target,
                        daemon=True)
        thread.start()