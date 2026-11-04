package com.example.seniorguard

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.tooling.preview.Preview

// 가족 알림 데이터 형태
data class FamilyAlert(
    val id: Int,
    val appName: String,
    val riskLevel: String,
    val reason: String,
    val detectedAt: String
)

@Composable
fun FamilyAlertScreen(
    modifier: Modifier = Modifier,
    alerts: List<FamilyAlert> = listOf(
        FamilyAlert(
            id = 1,
            appName = "PDF 뷰어",
            riskLevel = "위험",
            reason = "다른 앱 사용 중 광고를 표시할 가능성이 있어요.",
            detectedAt = "오늘 14:30"
        ),
        FamilyAlert(
            id = 2,
            appName = "메모리 정리",
            riskLevel = "주의",
            reason = "광고성 알림을 반복해서 보낼 가능성이 있어요.",
            detectedAt = "오늘 14:32"
        )
    )
) {
    val orange = Color(0xFFF59A17)

    Column(
        modifier = modifier
            .fillMaxSize()
            .background(Color(0xFFF8F9FE))
            .padding(24.dp)
    ) {
        Spacer(modifier = Modifier.height(20.dp))

        Text(
            text = "가족 알림",
            fontSize = 30.sp,
            fontWeight = FontWeight.Bold
        )

        Spacer(modifier = Modifier.height(12.dp))

        Text(
            text = "부모님 휴대폰에서 발견된\n주의가 필요한 앱을 확인해요.",
            fontSize = 20.sp,
            lineHeight = 30.sp
        )

        Spacer(modifier = Modifier.height(24.dp))

        if (alerts.isEmpty()) {
            Text(
                text = "아직 도착한 알림이 없어요.",
                fontSize = 20.sp
            )
        } else {
            LazyColumn(
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                items(
                    items = alerts,
                    key = { it.id }
                ) { alert ->
                    Card(
                        modifier = Modifier.fillMaxWidth(),
                        shape = RoundedCornerShape(20.dp),
                        colors = CardDefaults.cardColors(
                            containerColor = Color.White
                        )
                    ) {
                        Column(
                            modifier = Modifier.padding(20.dp),
                            verticalArrangement =
                                Arrangement.spacedBy(12.dp)
                        ) {
                            Text(
                                text = "부모님 휴대폰",
                                fontSize = 18.sp,
                                color = Color.DarkGray
                            )

                            Text(
                                text = alert.appName,
                                fontSize = 24.sp,
                                fontWeight = FontWeight.Bold
                            )

                            Text(
                                text = "위험 등급: ${alert.riskLevel}",
                                fontSize = 20.sp,
                                fontWeight = FontWeight.Bold,
                                color = if (
                                    alert.riskLevel == "위험"
                                ) Color(0xFFCA3434) else orange
                            )

                            Text(
                                text = alert.reason,
                                fontSize = 20.sp,
                                lineHeight = 28.sp
                            )

                            Text(
                                text = alert.detectedAt,
                                fontSize = 16.sp,
                                color = Color.Gray
                            )
                        }
                    }
                }
            }
        }
    }
}

@Preview(showBackground = true)
@Composable
fun FamilyAlertPreview() {
    FamilyAlertScreen()
}
