
package com.example.seniorguard

import android.app.AppOpsManager
import android.app.usage.UsageEvents
import android.app.usage.UsageStatsManager
import android.content.Context
import android.os.Process
import android.provider.Settings
import android.content.Intent

object UsageEventMonitor {

    // 사용 기록 접근 권한 확인
    fun hasUsageAccess(context: Context): Boolean {
        val appOps = context.getSystemService(Context.APP_OPS_SERVICE)
                as AppOpsManager

        val mode = appOps.checkOpNoThrow(
            AppOpsManager.OPSTR_GET_USAGE_STATS,
            Process.myUid(),
            context.packageName
        )

        return mode == AppOpsManager.MODE_ALLOWED
    }

    // 사용 기록 접근 설정 화면 열기
    fun openUsageAccessSettings(context: Context) {
        val intent = Intent(Settings.ACTION_USAGE_ACCESS_SETTINGS)
        context.startActivity(intent)
    }

    // 최근 앱 사용 이벤트 조회
    fun getRecentEvents(
        context: Context,
        sinceTime: Long
    ): List<Pair<String, Long>> {

        val usageStatsManager =
            context.getSystemService(Context.USAGE_STATS_SERVICE)
                    as UsageStatsManager

        val endTime = System.currentTimeMillis()
        val events = usageStatsManager.queryEvents(sinceTime, endTime)

        val result = mutableListOf<Pair<String, Long>>()
        val event = UsageEvents.Event()

        while (events.hasNextEvent()) {
            events.getNextEvent(event)

            if (event.eventType == UsageEvents.Event.ACTIVITY_RESUMED &&
                event.packageName != context.packageName
            ) {
                result.add(
                    Pair(event.packageName, event.timeStamp)
                )
            }
        }

        return result
    }
}
