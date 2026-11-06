package com.example.seniorguard

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Intent
import android.os.Build
import android.util.Log
import androidx.core.app.NotificationCompat
import com.google.firebase.messaging.FirebaseMessagingService
import com.google.firebase.messaging.RemoteMessage

class SeniorGuardMessagingService : FirebaseMessagingService() {

    override fun onMessageReceived(message: RemoteMessage) {
        super.onMessageReceived(message)

        Log.d("SeniorGuardFCM", "푸시 메시지 수신")

        // notification 메시지는 앱이 실행 중일 때 직접 표시
        // data 메시지는 앱 상태에 따라 직접 표시
        val title = message.notification?.title
            ?: message.data["title"]
            ?: "시니어가드"

        val body = message.notification?.body
            ?: message.data["body"]
            ?: "새로운 알림이 도착했습니다."

        showNotification(title, body)
    }

    override fun onNewToken(token: String) {
        super.onNewToken(token)
        Log.d("SeniorGuardFCM", "FCM 토큰 갱신됨 (길이: ${token.length})")
        // 토큰이 갱신되면 로그인된 계정으로 재등록하는 처리 필요
    }

    private fun showNotification(title: String, body: String) {
        val channelId = "seniorguard_fcm"

        val manager = getSystemService(NotificationManager::class.java)

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                channelId,
                "위험 감지 알림",
                NotificationManager.IMPORTANCE_HIGH
            )
            manager.createNotificationChannel(channel)
        }

        val intent = Intent(this, MainActivity::class.java)
        val pendingIntent = PendingIntent.getActivity(
            this,
            0,
            intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val notification = NotificationCompat.Builder(this, channelId)
            .setSmallIcon(R.mipmap.ic_launcher)
            .setContentTitle(title)
            .setContentText(body)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setAutoCancel(true)
            .setContentIntent(pendingIntent)
            .build()

        manager.notify(System.currentTimeMillis().toInt(), notification)
    }
}