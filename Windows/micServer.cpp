#define MINIAUDIO_IMPLEMENTATION

#include <iostream>
#include <WinSock2.h>
#include <WS2tcpip.h>
#include <miniaudio.h>
using namespace std;

typedef struct {
	int *readBytes;
	char *buffer;
} myData;
// A lot of the code below is all copied because i don't know C++ haha

void data_callback(ma_device* pDevice, void* pOutput, const void* pInput, ma_uint32 frameCount)
{
	myData* userData = (myData*)pDevice->pUserData;
	memcpy(pOutput, userData->buffer, *userData->readBytes);
	(void)pOutput;
}


int main()
{
	// Init context to see audio devices
	ma_context context;
    if (ma_context_init(NULL, 0, NULL, &context) != MA_SUCCESS) {
        return -1;
    }

	// Get info for all devices, god i wish half of these args were optional
	// Init structs containing device info
	ma_device_info *pPlaybackInfos, *pCaptureInfos;
	// total input and output device count
    ma_uint32 playbackCount, captureCount;

	// Abort the program if device info can't be obtained
	if (ma_context_get_devices(&context, &pPlaybackInfos, 
	&playbackCount, &pCaptureInfos, &captureCount) != MA_SUCCESS) {
        return -1;
    }

	// Loop through each device and find the vbaudio input
	ma_device_id *playbackID;
	for (ma_uint32 deviceIndex; deviceIndex < playbackCount; deviceIndex++) {
		// convert char* device name to string
		string deviceName (pPlaybackInfos[deviceIndex].name);

		// use string.find to get vbaudio device
		if (deviceName.find("VB-Audio") != string::npos) {
			playbackID = &pPlaybackInfos[deviceIndex].id;
		}
	}

	// Inititate and clear audio buffer
	char buf[65000];
	ZeroMemory(buf, 65000);

	int read;
	myData myStruct;
	myStruct.buffer = buf;
	myStruct.readBytes = &read;

	// This is literally just copied from the docs
	ma_device_config config = ma_device_config_init(ma_device_type_playback);
	config.playback.pDeviceID = playbackID; // VBCable input device
    config.playback.format = ma_format_unknown;   // Set to ma_format_unknown to use the device's native format.
    config.playback.channels = 0;   
    config.sampleRate = 0;           // Set to 0 to use the device's native sample rate.
    config.dataCallback = data_callback;   // This function will be called when miniaudio needs more data.
	config.pUserData = &myStruct;

	// init device, abort if failed
	ma_device device;
    if (ma_device_init(NULL, &config, &device) != MA_SUCCESS) {
        return -1;  // Failed to initialize the device.
    }

	// Start device
	ma_device_start(&device);

	WSADATA data;
	WORD ver = MAKEWORD(2, 2);
	int wsOk = WSAStartup(ver, &data);
	if (wsOk != 0)
	{
		cout << "Problem starting socket." << endl;
		ExitProcess(EXIT_FAILURE);
	}

	// Set up UDP socket
	SOCKET server = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);

	// config socket to accept data from any ipv4 address on port 12358
	sockaddr_in serverHint;
	serverHint.sin_addr.S_un.S_addr = ADDR_ANY;
	serverHint.sin_family = AF_INET;
	serverHint.sin_port = htons(12358);

	if (bind(server, (sockaddr*)&serverHint, sizeof(serverHint)) == SOCKET_ERROR)
	{
		cout << "Can't bind socket." << endl;
		ExitProcess(EXIT_FAILURE);
	}

	sockaddr_in client;
	int clientLen = sizeof(client);
	ZeroMemory(&client, sizeof(client));

	while (true)
	{
		read = recvfrom(server, buf, 65000, 0, (sockaddr*)&client, &clientLen);	
	}

	ma_device_stop(&device);
	ma_device_uninit(&device);
	ma_context_uninit(&context);
	closesocket(server);
	WSACleanup();
	return 0;
}