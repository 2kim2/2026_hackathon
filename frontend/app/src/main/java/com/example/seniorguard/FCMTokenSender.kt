
package com.example.seniorguard

import android.util.Log
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL
import java.util.concurrent.Executors

object FCMTokenSender {

    private val executor = Executors.newSingleThreadExecutor()

    fun sendToken(
        apiUrl: String,
        authToken: String,
        fcmToken: String
    ) {
        executor.execute {
            var connection: HttpURLConnection? = null

            try {
                val body = JSONObject().apply {
                    put("token", fcmToken)
                }

                connection = URL(apiUrl).openConnection()
                        as HttpURLConnection

                connection.requestMethod = "POST"
                connection.setRequestProperty(
                    "Content-Type",
                    "application/json"
                )
                connection.setRequestProperty(
                    "Authorization",
                    "Token $authToken"
                )
                connection.connectTimeout = 10000
                connection.readTimeout = 10000
                connection.doOutput = true

                connection.outputStream.use {
                    it.write(body.toString().toByteArray(Charsets.UTF_8))
                }

                Log.d(
                    "SeniorGuardFCM",
                    "서버 응답 코드: ${connection.responseCode}"
                )

            } catch (e: Exception) {
                Log.e(
                    "SeniorGuardFCM",
                    "FCM 토큰 전송 실패",
                    e
                )
            } finally {
                connection?.disconnect()
            }
        }
    }
}
