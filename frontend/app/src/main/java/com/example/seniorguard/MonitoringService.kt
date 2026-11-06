package com.example.seniorguard

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.Service
import android.content.Intent
import android.content.pm.ServiceInfo
import android.os.Build
import android.os.Handler
import android.os.IBinder
import android.os.Looper
import android.util.Log

class MonitoringService : Service() {

    private val handler = Handler(Looper.getMainLooper())
    private var lastCheckedTime = 0L

    private val monitorTask = object : Runnable {
        override fun run() {
            try {
                if (!UsageEventMonitor.hasUsageAccess(this@MonitoringService)) {
                    Log.w("SeniorGuardSnapshot", "사용 기록 접근 권한 없음")
                    stopSelf()
                    return
                }

                val events = UsageEventMonitor.getRecentEvents(
                    this@MonitoringService,
                    lastCheckedTime
                )

                lastCheckedTime = System.currentTimeMillis()

                events.forEach { (appPackage, eventTime) ->
                    val snapshot = SnapshotCollector.collect(
                        this@MonitoringService,
                        appPackage
                    )

                    Log.d(
                        "SeniorGuardSnapshot",
                        "앱=$appPackage, 이벤트=$eventTime, " +
                                "수집=${snapshot.snapshotTime}, " +
                                "권한=${snapshot.permissions.size}개, " +
                                "인터넷=${snapshot.internetConnected}, " +
                                "화면=${snapshot.screenInteractive}"
                    )
                }

            } catch (e: Exception) {
                Log.e("SeniorGuardSnapshot", "감시 오류", e)
            }

            handler.postDelayed(this, 5000L)
        }
    }

    override fun onCreate() {
        super.onCreate()

        val channelId = "seniorguard_monitor"

        val channel = NotificationChannel(
            channelId,
            "시니어가드 앱 감시",
            NotificationManager.IMPORTANCE_LOW
        )

        val manager = getSystemService(
            NotificationManager::class.java
        )
        manager.createNotificationChannel(channel)

        val notification = Notification.Builder(this, channelId)
            .setContentTitle("시니어가드 감시 중")
            .setContentText("앱 사용 이벤트를 확인하고 있습니다.")
            .setSmallIcon(android.R.drawable.ic_menu_view)
            .setOngoing(true)
            .build()

        if (Build.VERSION.SDK_INT >= 34) {
            startForeground(
                1,
                notification,
                ServiceInfo.FOREGROUND_SERVICE_TYPE_SPECIAL_USE
            )
        } else {
            startForeground(1, notification)
        }
    }

    override fun onStartCommand(
        intent: Intent?,
        flags: Int,
        startId: Int
    ): Int {
        handler.removeCallbacks(monitorTask)

        lastCheckedTime = System.currentTimeMillis()
        handler.post(monitorTask)

        return START_NOT_STICKY
    }

    override fun onDestroy() {
        handler.removeCallbacks(monitorTask)
        super.onDestroy()
    }

    override fun onBind(intent: Intent?): IBinder? = null
}
