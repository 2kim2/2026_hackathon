package com.example.seniorguard

import android.content.Context
import android.content.pm.PackageManager
import android.net.ConnectivityManager
import android.net.NetworkCapabilities
import android.os.Build
import android.os.PowerManager

data class AppSnapshot(
    val packageName: String,
    val permissions: List<String>,
    val internetConnected: Boolean,
    val screenInteractive: Boolean,
    val processImportance: Int?,
    val snapshotTime: Long
)

object SnapshotCollector {

    fun collect(context: Context, packageName: String): AppSnapshot {

        // 1. 앱에서 요청한 권한 목록
        val permissions = try {
            val pm = context.packageManager

            val info = if (Build.VERSION.SDK_INT >= 33) {
                pm.getPackageInfo(
                    packageName,
                    PackageManager.PackageInfoFlags.of(
                        PackageManager.GET_PERMISSIONS.toLong()
                    )
                )
            } else {
                @Suppress("DEPRECATION")
                pm.getPackageInfo(
                    packageName,
                    PackageManager.GET_PERMISSIONS
                )
            }

            info.requestedPermissions?.toList() ?: emptyList()
        } catch (e: PackageManager.NameNotFoundException) {
            emptyList()
        }

        // 2. 기기의 인터넷 연결 여부
        val connectivityManager =
            context.getSystemService(Context.CONNECTIVITY_SERVICE)
                    as ConnectivityManager

        val network = connectivityManager.activeNetwork
        val capabilities =
            connectivityManager.getNetworkCapabilities(network)

        val internetConnected =
            capabilities?.hasCapability(
                NetworkCapabilities.NET_CAPABILITY_VALIDATED
            ) == true

        // 3. 기기 화면 활성 상태
        val powerManager =
            context.getSystemService(Context.POWER_SERVICE)
                    as PowerManager

        val screenInteractive = powerManager.isInteractive

        // 4. 다른 앱 프로세스 중요도는 일단 수집하지 않음
        val processImportance: Int? = null

        return AppSnapshot(
            packageName = packageName,
            permissions = permissions,
            internetConnected = internetConnected,
            screenInteractive = screenInteractive,
            processImportance = processImportance,
            snapshotTime = System.currentTimeMillis()
        )
    }
}
