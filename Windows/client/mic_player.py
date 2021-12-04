# Manages the thread in charge of fetching data from the network
# and writing it to the audio stream
from threading import Thread
import pyaudio
import pydub


# Class for microphone IO.
class MicPlayer(pyaudio.PyAudio):
    def __init__(self):
        super().__init__()
        # ON/OFF flag for audio thread.
        self._running = False

        self.deepfry =  False

        # The configuration for the audio streams 
        # this class will open.
        self._audio_config = {
            'format': pyaudio.paInt16,
            'channels': 1,
            'rate': 44100
        }

    # Writes data to VBCable input
    def _thread_target(self, stream, socket):
        while self._running:
            audio_data = socket.recv(socket.bufsize)
            if self.deepfry:
                sound = pydub.AudioSegment(data=audio_data, sample_width=1, frame_rate=8000, channels=1)
                sound = sound + 1000
                sound = sound - 20
                stream.write(sound.raw_data)
            else:
                stream.write(audio_data)
        stream.close()

    def config_audio(self, *, audioformat, channels, rate):
        """Sets up the configuration for the audio stream.\n
        format: The bit-depth of the audio stream. Default config is 16-bit.\n
        channels: The audio channels the audio will output to. Default is Mono.\n
        rate: The sample rate of the audio stream. Default is 44100Hz."""
        self._audio_config = {
            'format': audioformat,
            'channels': channels,
            'rate': rate,
            'output': True
        }

    # Sets the running flag to false,
    # stopping the thread
    def stop(self):
        self._running = False

    # Starts the thread with the given socket.
    def start(self, socket, audio_device = None):
        # Set flag to ON and open stream
        self._running = True
        stream = self.open(rate=self._audio_config['rate'],
                        format=self._audio_config['format'],
                        channels=self._audio_config['channels'],
                        output_device_index=audio_device,
                        output=True)

        # Convert the thread target to a
        # thread object and run it
        thread = Thread(target=self._thread_target,
                        args=(stream, socket),
                        daemon=True)
        thread.start()