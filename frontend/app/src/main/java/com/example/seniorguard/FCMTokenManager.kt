
package com.example.seniorguard

import android.util.Log
import com.google.firebase.messaging.FirebaseMessaging

object FCMTokenManager {

    fun fetchToken(
        onTokenReady: (String) -> Unit = {}
    ) {
        FirebaseMessaging.getInstance().token
            .addOnCompleteListener { task ->

                if (!task.isSuccessful) {
                    Log.e(
                        "SeniorGuardFCM",
                        "FCM 토큰 발급 실패",
                        task.exception
                    )
                    return@addOnCompleteListener
                }

                val token = task.result

                Log.d(
                    "SeniorGuardFCM",
                    "FCM 토큰 발급 성공 (길이: ${token.length})"
                )

                // 서버 전송에 사용할 토큰 전달
                onTokenReady(token)
            }
    }
    fun registerToken(baseUrl: String, authToken: String) {
        fetchToken { fcmToken ->
            FCMTokenSender.sendToken(
                apiUrl = "${baseUrl.trimEnd('/')}/api/notifications/fcm-token/",
                authToken = authToken,
                fcmToken = fcmToken
            )
        }
    }
}
