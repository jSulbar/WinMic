<div align="center">
<img height="100px" src="logo.png"/>
  
# WinMic  
</div>

WinMic takes your phone mic audio and plays it on your PC, sending it via local network. Although its supposed to be used as a PC mic, this is easily done by installing [VB-Cable](https://vb-audio.com/Cable/index.htm) and selecting the "CABLE Input" audio device.

### How to use
#### Windows:
- Download and unzip WinMic_x86.zip on your computer
- Open WinMic.exe and select your desired device through which the audio will be sent. Then select "Start recording"
#### Android:
- Download WinMic-release.apk and go to the file's location on your file manager, then install the app
- Open the app and enter on it the IPv4 address displayed on your computer's WinMic, then tap the toggle button
- You should start hearing your phone's audio now!

# Building
The release version of WinMic is just a pyinstaller package. I've included a script that installs the modules inside a virtual environment and creates the package, however as this app requires pyaudio you will need Visual Studio build tools to download and install if you're on windows. Alternatively, you can download a pip wheel and install it as specified [here](https://stackoverflow.com/a/55630212).
