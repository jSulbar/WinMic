package com.serpento.winmic;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.Manifest.permission;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.util.Log;


// UI imports
import android.view.Window;
import android.view.WindowManager;
import android.widget.CompoundButton;
import android.widget.CompoundButton.OnCheckedChangeListener;
import android.widget.EditText;

// Imports for multimedia
import android.media.AudioRecord;
import android.media.AudioFormat;
import android.media.MediaRecorder;
import android.widget.ToggleButton;

// Java imports
import java.net.*;
import java.util.*;

// Class for simplifying sockets so my dumb brain can use them. Or maybe
// it exists for no reason. idk.
class SocketInstance {
    // Initiate variables for sending packets through the socket. Not much to see here.
    // Port is hardcoded for now, don't know if i should change it?
    private InetAddress ADDRESS;
    private DatagramSocket udpSocket;

    // Constructor for this class. Takes an IP to send packets to, and populates
    // socket and addr.
    public SocketInstance(String ipAddr) throws UnknownHostException, SocketException {
        ADDRESS = InetAddress.getByName(ipAddr);
        udpSocket = new DatagramSocket();
    }

    // Send data via socket.
    public void sendPacket(byte[] buffer) {
        try {
            udpSocket.send(makePacket(buffer));
        }
        catch(Exception e) {
            Log.e("Serpento", e.toString());
        }
    }

    // Creates a packet for sendPacket. Port is hardcoded for now.
    private DatagramPacket makePacket(byte[] buffer) {
        DatagramPacket packet = new DatagramPacket(buffer, buffer.length, ADDRESS, 12358);
        return packet;
    }
}

// Class to manage the recorder easier. Or to make code look prettier? idk. i'm bad at this.
class VoiceRecorder {
    // Initiate recorder variable, assign later
    private AudioRecord recorder;

    // Get stuff for the recorder constructor, audio config
    private int sampleRate = 44100;
    private int audioSource = MediaRecorder.AudioSource.MIC;
    private int channelConfig = AudioFormat.CHANNEL_IN_MONO;
    private int audioFormat = AudioFormat.ENCODING_PCM_16BIT;
    private int bufferSize = AudioRecord.getMinBufferSize(sampleRate, channelConfig, audioFormat);

    public VoiceRecorder() {
        recorder = new AudioRecord(audioSource, sampleRate,
        channelConfig, audioFormat, bufferSize);
        Log.d("Serpento", "Started recorder instance");
    }

    public byte[] getAudioBytes() {
        // Create buffer to store read data
        byte[] buffer = new byte[bufferSize];

        // Get number of bytes read from mic
        int readBytes = recorder.read(buffer, 0, buffer.length);

        // Return new buffer with only read bytes
        byte[] readBuffer = Arrays.copyOfRange(buffer, 0, readBytes);
        return readBuffer;
    }

    public void startRecording() {
        recorder.startRecording();
        Log.d("Serpento", "Started Recording");
    }

    public void stopRecording() {
        recorder.stop();
        Log.d("Serpento", "Stopped Recording");
    }
}

class MicSocket {

    // Variables for the socket to use while sending,
    // and the recording object
    private VoiceRecorder input;
    private SocketInstance socket;
    private String ipAddr;

    // Keep track of recording
    private boolean isRecording;

    // Thread that sends packets while recording.
    private Thread sendMicAudio = new Thread() {
        public void run() {
            input.startRecording();
            while (isRecording) {
                byte[] buffer = input.getAudioBytes();
                socket.sendPacket(buffer);
            }
        }
    };

    // Populate objects
    public MicSocket(String ipAddr) {
        try {
            Log.d("Serpento", "Initiated micsocket");
            input = new VoiceRecorder();
            socket = new SocketInstance(ipAddr);
            this.ipAddr = ipAddr;
        } catch (Exception e) {
            Log.e("Serpento", e.toString());
        }
    }

    // Set isRecording to true, start mic 
    // and send its audio through socket
    public void startRecording() {
        isRecording = true;
        sendMicAudio.start();
    }

    // Stop mic processes
    public void stopRecording() throws UnknownHostException, SocketException{
        Log.d("Serpento", "Stopped sending");
        isRecording = false;
        input.stopRecording();
    }

    public boolean isRecording() {
        return isRecording;
    }
}

public class MainActivity extends AppCompatActivity {

    private MicSocket micInstance;

    // Start/Stop sending mic audio over network
    private void startMic() {
        Log.d("Serpento", "Pressed start");

        // Get the user's desired IP
        EditText ipView = findViewById(R.id.ipInput);
        String ipAddr = ipView.getText().toString();

        // Create socket instance with ip address then send message
        try {
            if (micInstance == null) {
                micInstance = new MicSocket(ipAddr);
                micInstance.startRecording();
            }
        } catch (Exception e) {
            Log.e("Serpento", e.toString());
        }
    }
    private void stopMic() {
        Log.d("Serpento", "Pressed end");
        // Stop recording and delete mic instance
        try {
            if (micInstance != null && micInstance.isRecording()) {
                micInstance.stopRecording();
                micInstance = null;
            }
        } catch (Exception e) {
            Log.e("Serpento", e.toString());
        }
    }

    // Functions to make permissions API less fuckin' cryptic thx google
    private boolean hasMicPerms() {
        return (ContextCompat.checkSelfPermission(
                getApplicationContext(), permission.RECORD_AUDIO) ==
                PackageManager.PERMISSION_GRANTED);
    }
    private void requestMicPerms() {
        ActivityCompat.requestPermissions(MainActivity.this,
                new String[] { permission.RECORD_AUDIO }, 1);
    }

    // Logic for toggle button, to only work when permissions are granted.
    OnCheckedChangeListener recordListener = new OnCheckedChangeListener() {
        public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
            if (isChecked) {
                if (!hasMicPerms()) {
                    requestMicPerms();
                    if (hasMicPerms()) {
                        startMic();
                        buttonView.setChecked(true);
                    } else {
                        buttonView.setChecked(false);
                        return;
                    }
                } else {
                    startMic();
                }
            } else {
                stopMic();
            }
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

        ToggleButton toggle = findViewById(R.id.toggleButton);
        toggle.setOnCheckedChangeListener(recordListener);
    }
}