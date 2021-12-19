package oss.jsulbar.winmic

import android.Manifest.permission
import android.app.*
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.media.AudioFormat
import android.media.AudioRecord
import android.media.MediaRecorder
import android.os.*
import androidx.appcompat.app.AppCompatActivity
import android.util.Log
import android.view.WindowManager
import android.widget.CompoundButton
import android.widget.EditText
import android.widget.ToggleButton
import androidx.core.app.ActivityCompat
import androidx.core.app.NotificationCompat
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

   fun stopRecording() {
        recorder.stop()
        Log.d("jSulbar", "Stopped Recording")
    }
}

internal class MicForegroundService : Service() {

    private val CHANNEL_ID = "WinMicForeground"
    private val WINMIC_STOP = "STOP_WINMIC"
    private val NOTIF_ID = 12358

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        if (intent!!.action == WINMIC_STOP && MicSocket.isRecording) {
            stopSelf()
        }
        else {
            createNotificationChannel()
            val notif = appNotification()
            startForeground(NOTIF_ID, notif)
            MicSocket.startRecording()
        }
        return START_STICKY
    }

    override fun onDestroy() {
        MicSocket.stopRecording()
        stopForeground(true)
    }

    // Create the notification for this foreground service.
    private fun appNotification(): Notification {
        val pendingIntent: PendingIntent =
            Intent(this, MicForegroundService::class.java).let { notificationIntent ->
                notificationIntent.setAction(WINMIC_STOP)
                PendingIntent.getService(this, 0, notificationIntent,
                    PendingIntent.FLAG_CANCEL_CURRENT)
            }
        return NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle(getString(R.string.servicenotif_title))
            .setContentText(getString(R.string.servicenotif_text))
            .setSmallIcon(R.mipmap.ic_launcher_foreground)
            .setContentIntent(pendingIntent)
            .build()
    }

    // Create notification channel, for compatibility with Oreo and above
    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val name = getString(R.string.servicenotif_channel)
            val descriptionText = getString(R.string.servicenotif_description)
            val importance = NotificationManager.IMPORTANCE_LOW
            val channel = NotificationChannel(CHANNEL_ID, name, importance).apply {
                description = descriptionText
            }
            // Register the channel with the system
            val notificationManager: NotificationManager =
                getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            notificationManager.createNotificationChannel(channel)
        }
    }

    override fun onBind(intent: Intent?): IBinder? {
        return null
    }
}

object MicSocket {

    private var recorder: VoiceRecorder? = null
    private var socket: SocketInstance? = null

    // Populate objects
    fun initProperties(ipAddress: String) {
        try {
            if (isRecording) {
                stopRecording()
            }
            socket = SocketInstance(ipAddress)
            recorder = VoiceRecorder()
        }
        catch (e: Exception) {
            Log.e("jSulbar", e.toString())
        }
    }

    // Keep track of recording
    var isRecording = false
    var micThread: Thread? = null

    // Create a thread to send audio packets from the mic's data.
    // Threads can only be used once, so this is called whenever a recording starts.
    private fun createMicThread() : Thread {
        val micThread = object : Thread() {
            override fun run() {
                recorder!!.startRecording()
                while (isRecording) {
                    val buffer: ByteArray = recorder!!.readAudioBytes()
                    socket!!.sendPacket(buffer)
                }
                recorder!!.stopRecording()
            }
        }
        return micThread
    }

    // Set isRecording to true, start mic
    // and send its audio through socket
    fun startRecording() {
        if (recorder == null || isRecording) {
            return
        }
        isRecording = true
        micThread = createMicThread()
        micThread!!.start()
    }

    // Stop mic processes
    fun stopRecording() {
        Log.d("jSulbar", "Stopped sending")
        if (!isRecording) {
            return
        }
        isRecording = false
    }
}

class MicControl : AppCompatActivity() {

    private var foregroundServiceIntent: Intent? = null

    // Start/Stop sending mic audio over network
    private fun startMic() {
        Log.d("jSulbar", "Pressed start")

        // Get the user's desired IP
        val ipView = findViewById<EditText>(R.id.ipinput)
        val ipAddress = ipView.text.toString()

        // Create socket instance with ip address then send message
        MicSocket.initProperties(ipAddress)
        startService(foregroundServiceIntent)
    }

    private fun stopMic() {
        Log.d("jSulbar", "Pressed end")
        // Stop recording
        stopService(foregroundServiceIntent)
    }

    // Functions to make permissions API less cryptic thx google
    // from your future self: you are a dumbass
    private fun hasMicPerms(): Boolean {
        return ContextCompat.checkSelfPermission(applicationContext, permission.RECORD_AUDIO) ==
                PackageManager.PERMISSION_GRANTED
    }

    private fun requestMicPerms() {
        ActivityCompat.requestPermissions(this@MicControl,
            arrayOf(permission.RECORD_AUDIO),
            1)
    }

    // Event listener for mic toggle, to only work when permissions are granted.
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

    // Disable togglebutton if the mic was turned off from outside the app
    override fun onResume() {
        super.onResume()
        val toggle = findViewById<ToggleButton>(R.id.mic_togglebutton)
        toggle.isChecked = MicSocket.isRecording
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_mic_control)

        foregroundServiceIntent = Intent(this, MicForegroundService::class.java)

        val toggle = findViewById<ToggleButton>(R.id.mic_togglebutton)
        toggle.setOnCheckedChangeListener(recordListener)
    }
}