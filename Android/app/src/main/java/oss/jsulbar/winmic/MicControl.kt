package oss.jsulbar.winmic

import android.Manifest.permission
import android.content.pm.PackageManager
import android.media.AudioFormat
import android.media.AudioRecord
import android.media.MediaRecorder
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.view.WindowManager
import android.widget.CompoundButton
import android.widget.EditText
import android.widget.ToggleButton
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import java.lang.Exception
import java.net.*
import java.util.*

// Class for simplifying sockets so my dumb brain can use them.
internal class SocketInstance(ipAddress: String) {

    // Initiate variables for sending packets through the socket.
    private val ADDRESS = InetAddress.getByName(ipAddress)
    private val udpSocket = DatagramSocket()

    // Send a packet through the UDP socket
    fun sendPacket(buffer: ByteArray) {
        try {
            udpSocket.send(makePacket(buffer))
        } catch (e: Exception) {
            Log.e("jSulbar", e.toString())
        }
    }

    // Creates a packet for sendPacket. Port is hardcoded for now.
    private fun makePacket(buffer: ByteArray): DatagramPacket {
        return DatagramPacket(buffer, buffer.size, ADDRESS, 12358)
    }
}

internal class VoiceRecorder {
    // Initiate recorder variable, assign later
    private val recorder: AudioRecord

    // Get stuff for the recorder constructor, audio config
    private val sampleRate = 44100
    private val audioSource = MediaRecorder.AudioSource.MIC
    private val channelConfig = AudioFormat.CHANNEL_IN_MONO
    private val audioFormat = AudioFormat.ENCODING_PCM_16BIT
    private val bufferSize = AudioRecord.getMinBufferSize(sampleRate, channelConfig, audioFormat)

    init {
        recorder = AudioRecord(
            audioSource, sampleRate,
            channelConfig, audioFormat, bufferSize
        )
        Log.d("jSulbar", "Started recorder instance")
    }

    // Create buffer to store read data
    lateinit var audioBytes: ByteArray

    // Get number of bytes read from mic
    fun readAudioBytes(): ByteArray {
        // Return new buffer with only read bytes
        // Create buffer to store read data
        val buffer = ByteArray(bufferSize)

        // Get number of bytes read from mic
        val readBytes = recorder.read(buffer, 0, buffer.size)

        // Return new buffer with only read bytes
        return buffer.copyOfRange(0, readBytes)
    }

    fun startRecording() {
        recorder.startRecording()
        Log.d("jSulbar", "Started Recording")
    }

    public fun stopRecording() {
        recorder.stop()
        Log.d("jSulbar", "Stopped Recording")
    }
}

internal class MicSocket(ipAddress: String) {

    private lateinit var input: VoiceRecorder
    private lateinit var socket: SocketInstance

    // Populate objects
    init {
        try {
            Log.d("jSulbar", "Initiated micsocket")
            input = VoiceRecorder()
            socket = SocketInstance(ipAddress)
        } catch (e: Exception) {
            Log.e("jSulbar", e.toString())
        }
    }

    // Keep track of recording
    var isRecording = false

    // Thread that sends packets while recording.
    private val sendMicAudio: Thread = object : Thread() {
        override fun run() {
            input.startRecording()
            while (isRecording) {
                val buffer: ByteArray = input.readAudioBytes()
                socket.sendPacket(buffer)
            }
        }
    }

    // Set isRecording to true, start mic
    // and send its audio through socket
    fun startRecording() {
        isRecording = true
        sendMicAudio.start()
    }

    // Stop mic processes
    fun stopRecording() {
        Log.d("jSulbar", "Stopped sending")
        isRecording = false
        input.stopRecording()
    }
}

class MicControl : AppCompatActivity() {

    private var micInstance: MicSocket? = null

    // Start/Stop sending mic audio over network
    private fun startMic() {
        Log.d("jSulbar", "Pressed start")

        // Get the user's desired IP
        val ipView = findViewById<EditText>(R.id.ipinput)
        val ipAddress = ipView.text.toString()

        // Create socket instance with ip address then send message
        try {
            if (micInstance == null) {
                micInstance = MicSocket(ipAddress)
                micInstance!!.startRecording()
            }
        } catch (e: Exception) {
            Log.e("jSulbar", e.toString())
        }
    }
    private fun stopMic() {
        Log.d("jSulbar", "Pressed end")
        // Stop recording and delete mic instance
        try {
            if (micInstance != null && micInstance!!.isRecording) {
                micInstance!!.stopRecording()
                micInstance = null
            }
        } catch (e: Exception) {
            Log.e("jSulbar", e.toString())
        }
    }

    // Functions to make permissions API less cryptic thx google
    private fun hasMicPerms(): Boolean {
        return ContextCompat.checkSelfPermission(applicationContext, permission.RECORD_AUDIO) ==
                PackageManager.PERMISSION_GRANTED
    }
    private fun requestMicPerms() {
        ActivityCompat.requestPermissions(this@MicControl,
            arrayOf(permission.RECORD_AUDIO),
            1)
    }

    // Logic for toggle button, to only work when permissions are granted.
    private var recordListener =
        CompoundButton.OnCheckedChangeListener { buttonView, isChecked ->
            if (isChecked) {
                if (!hasMicPerms()) {
                    requestMicPerms()
                    if (hasMicPerms()) {
                        startMic()
                    } else {
                        buttonView.isChecked = false
                    }
                } else {
                    startMic()
                }
            } else {
                stopMic()
            }
        }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_mic_control)
        window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)

        val toggle = findViewById<ToggleButton>(R.id.mic_togglebutton)
        toggle.setOnCheckedChangeListener(recordListener)
    }
}