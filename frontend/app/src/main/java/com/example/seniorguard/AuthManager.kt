package com.example.seniorguard

import android.util.Log
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL
import java.util.concurrent.Executors

object AuthManager {
    private val executor = Executors.newSingleThreadExecutor()

    fun loginAndRegisterFCM(
        baseUrl: String,
        username: String,
        password: String,
        onResult: (String) -> Unit
    ) {
        executor.execute {
            var connection: HttpURLConnection? = null

            try {
                val url = "${baseUrl.trimEnd('/')}/api/accounts/login/"
                connection = URL(url).openConnection() as HttpURLConnection

                connection.requestMethod = "POST"
                connection.setRequestProperty("Content-Type", "application/json")
                connection.connectTimeout = 10000
                connection.readTimeout = 10000
                connection.doOutput = true

                val body = JSONObject().apply {
                    put("username", username)
                    put("password", password)
                }

                connection.outputStream.use {
                    it.write(body.toString().toByteArray(Charsets.UTF_8))
                }

                val code = connection.responseCode

                if (code == 200) {
                    val response = connection.inputStream.bufferedReader()
                        .use { it.readText() }

                    val authToken = JSONObject(response).getString("token")

                    Log.d("SeniorGuardFCM", "로그인 성공, FCM 등록 요청 시작")

                    FCMTokenManager.registerToken(
                        baseUrl = baseUrl,
                        authToken = authToken
                    )

                    onResult("로그인 성공! FCM 등록 요청 시작")
                } else {
                    Log.e("SeniorGuardFCM", "로그인 실패: HTTP $code")
                    onResult("로그인 실패: HTTP $code")
                }

            } catch (e: Exception) {
                Log.e("SeniorGuardFCM", "로그인 연결 실패", e)
                onResult("연결 실패: ${e.message}")
            } finally {
                connection?.disconnect()
            }
        }
    }
}