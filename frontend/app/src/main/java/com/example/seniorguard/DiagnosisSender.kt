package com.example.seniorguard

import android.content.Context
import android.content.pm.PackageManager
import android.util.Log
import androidx.core.app.NotificationManagerCompat
import org.json.JSONArray
import org.json.JSONObject
import java.net.HttpURLConnection
import java.io.File
import java.net.URL
import java.security.MessageDigest
import java.util.concurrent.ConcurrentHashMap
import java.util.concurrent.Executors

/**
 * 스냅샷을 BE1 분석 API(POST /api/diagnoses/analyze/)로 보낸다.
 * BE1이 BE2 분석 서버에 넘기고, 결과가 danger면 보호자에게 FCM 알림까지 보낸다.
 */
object DiagnosisSender {

    private const val TAG = "SeniorGuardDiagnosis"
    private const val NOTIFICATION_LISTENER =
        "android.permission.BIND_NOTIFICATION_LISTENER_SERVICE"

    // 같은 앱을 5초마다 반복 전송하지 않도록 최소 간격 (무료 서버 부하, VirusTotal 분당 제한 대비)
    private const val MIN_INTERVAL_MS = 60_000L

    private val executor = Executors.newSingleThreadExecutor()
    private val lastSent = ConcurrentHashMap<String, Long>()

    // APK 해시 캐시: 패키지명 → (앱 업데이트 시각, sha256). 앱이 업데이트되기 전까지 재계산하지 않음
    private val hashCache = ConcurrentHashMap<String, Pair<Long, String>>()

    // 로그인 성공 시 AuthManager가 채워 준다 (앱 프로세스가 살아 있는 동안 유지)
    @Volatile var baseUrl: String? = null
    @Volatile var authToken: String? = null

    fun send(context: Context, snapshot: AppSnapshot, occurredAt: Long) {
        val url = baseUrl
        val token = authToken
        if (url.isNullOrBlank() || token.isNullOrBlank()) {
            Log.w(TAG, "로그인 전이라 분석 요청을 보내지 않음")
            return
        }
        // 우리 앱 자신은 분석하지 않음
        if (snapshot.packageName == context.packageName) return

        val now = System.currentTimeMillis()
        val prev = lastSent[snapshot.packageName]
        if (prev != null && now - prev < MIN_INTERVAL_MS) return
        lastSent[snapshot.packageName] = now

        val appContext = context.applicationContext
        executor.execute {
            var connection: HttpURLConnection? = null
            try {
                val body = buildBody(appContext, snapshot, occurredAt)

                connection = URL("${url.trimEnd('/')}/api/diagnoses/analyze/")
                    .openConnection() as HttpURLConnection
                connection.requestMethod = "POST"
                connection.setRequestProperty("Content-Type", "application/json")
                connection.setRequestProperty("Authorization", "Token $token")
                connection.connectTimeout = 15_000
                // BE1 → BE2 호출 + Render 무료 서버 콜드스타트를 고려해 넉넉하게
                connection.readTimeout = 90_000
                connection.doOutput = true

                connection.outputStream.use {
                    it.write(body.toString().toByteArray(Charsets.UTF_8))
                }

                val code = connection.responseCode
                val stream = if (code in 200..299) connection.inputStream else connection.errorStream
                val response = stream?.bufferedReader()?.use { it.readText() } ?: ""

                if (code in 200..299) {
                    val json = JSONObject(response)
                    Log.d(
                        TAG,
                        "분석 완료: 앱=${snapshot.packageName}, " +
                                "등급=${json.optString("risk_level")}, " +
                                "점수=${json.optInt("risk_score")}, " +
                                "요약=${json.optString("summary")}, " +
                                "VirusTotal=${json.optJSONObject("virustotal")?.optString("status")}"
                    )
                } else {
                    Log.e(TAG, "분석 요청 실패: HTTP $code, $response")
                    lastSent.remove(snapshot.packageName) // 실패하면 다음 이벤트 때 다시 시도
                }
            } catch (e: Exception) {
                Log.e(TAG, "분석 요청 연결 실패", e)
                lastSent.remove(snapshot.packageName)
            } finally {
                connection?.disconnect()
            }
        }
    }

    private fun buildBody(context: Context, snapshot: AppSnapshot, occurredAt: Long): JSONObject {
        val pm = context.packageManager

        // 요청한 권한 중 실제로 허용된 것인지 함께 보냄
        val permissions = JSONArray()
        snapshot.permissions.forEach { name ->
            val granted = pm.checkPermission(name, snapshot.packageName) ==
                    PackageManager.PERMISSION_GRANTED
            permissions.put(JSONObject().put("name", name).put("granted", granted))
        }

        // 알림 접근은 권한 목록에 안 나오므로 따로 확인해서 추가 (BE2와 약속한 이름)
        val hasNotificationAccess = NotificationManagerCompat
            .getEnabledListenerPackages(context)
            .contains(snapshot.packageName)
        if (hasNotificationAccess) {
            permissions.put(JSONObject().put("name", NOTIFICATION_LISTENER).put("granted", true))
        }

        return JSONObject().apply {
            put("package_name", snapshot.packageName)
            put("event_type", "ACTIVITY_RESUMED")
            put("occurred_at", occurredAt)                 // 이벤트 발생 시각 (epoch ms)
            put("collected_at", snapshot.snapshotTime)     // 상태 수집 시각 (epoch ms)
            put("permissions", permissions)
            put("network", JSONObject().put("is_connected", snapshot.internetConnected))
            put("screen", JSONObject().put("is_interactive", snapshot.screenInteractive))
            put("app_process_importance", JSONObject.NULL)
            // VirusTotal 조회용 APK 해시 (계산 실패하면 안 보냄 → VirusTotal 조회만 생략)
            apkSha256(context, snapshot.packageName)?.let { put("apk_sha256", it) }
        }
    }

    private fun apkSha256(context: Context, packageName: String): String? = try {
        val pm = context.packageManager
        @Suppress("DEPRECATION")
        val info = pm.getPackageInfo(packageName, 0)
        val updated = info.lastUpdateTime

        hashCache[packageName]?.takeIf { it.first == updated }?.second
            ?: run {
                val path = info.applicationInfo?.sourceDir ?: return@run null
                val md = MessageDigest.getInstance("SHA-256")
                File(path).inputStream().use { input ->
                    val buf = ByteArray(64 * 1024)
                    while (true) {
                        val n = input.read(buf)
                        if (n < 0) break
                        md.update(buf, 0, n)
                    }
                }
                md.digest().joinToString("") { "%02x".format(it) }
                    .also { hashCache[packageName] = updated to it }
            }
    } catch (e: Exception) {
        Log.w(TAG, "APK 해시 계산 실패: $packageName", e)
        null
    }
}
 