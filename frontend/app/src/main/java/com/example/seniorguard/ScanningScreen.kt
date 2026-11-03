package com.example.seniorguard

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.delay

@Composable
fun ScanningScreen(
    onScanComplete: (Boolean) -> Unit,
    modifier: Modifier = Modifier
) {
    var progress by remember { mutableIntStateOf(0) }

    // 시뮬레이션용 로딩 카운트업 (100% 도달 후 자동 이동)
    LaunchedEffect(Unit) {
        while (progress < 100) {
            delay(30)
            progress += 1
        }
        delay(400)
        onScanComplete(true) // 기본적으로 위험 결과 화면으로 이동 테스트
    }

    val currentAppCount = (progress * 30) / 100

    Column(
        modifier = modifier
            .fillMaxSize()
            .background(Color(0xFFF4F7F9))
            .navigationBarsPadding()
            .padding(horizontal = 24.dp),
        horizontalAlignment = Alignment.Start,
        verticalArrangement = Arrangement.SpaceBetween
    ) {
        Column(
            modifier = Modifier.fillMaxWidth()
        ) {
            Spacer(modifier = Modifier.height(12.dp))

            // 상단 소제목
            Text(
                text = "앱 확인 중",
                fontSize = 21.sp,
                fontWeight = FontWeight.Bold,
                color = Color(0xFF1B2A3A)
            )
            Spacer(modifier = Modifier.height(8.dp))

            // 메인 대제목
            Text(
                text = "살펴보고 있어요\n기다려주세요!",
                fontSize = 28.sp,
                fontWeight = FontWeight.ExtraBold,
                color = Color(0xFF1B2A3A),
                lineHeight = 38.sp
            )
        }

        // 중앙 원형 프로그래스 카드 (시안 디자인 100% 반영)
        Surface(
            modifier = Modifier
                .fillMaxWidth()
                .height(380.dp),
            color = Color.White,
            shape = RoundedCornerShape(28.dp),
            shadowElevation = 0.dp
        ) {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(24.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center
            ) {
                // 원형 프로그래스 바 + 중앙 퍼센트 텍스트
                Box(
                    modifier = Modifier.size(190.dp),
                    contentAlignment = Alignment.Center
                ) {
                    CircularProgressIndicator(
                        progress = { progress / 100f },
                        modifier = Modifier.fillMaxSize(),
                        color = Color(0xFFF59E1B), // 주황색 진행바
                        strokeWidth = 14.dp,
                        trackColor = Color(0xFFE9ECEF), // 연한 회색 배경 트랙
                        strokeCap = StrokeCap.Round
                    )
                    Text(
                        text = "$progress%",
                        fontSize = 42.sp,
                        fontWeight = FontWeight.ExtraBold,
                        color = Color(0xFFF59E1B)
                    )
                }

                Spacer(modifier = Modifier.height(36.dp))

                // 하단 진행 개수 안내
                Text(
                    text = "앱 30개 중 ${currentAppCount}개 확인",
                    fontSize = 22.sp,
                    fontWeight = FontWeight.ExtraBold,
                    color = Color(0xFF1B2A3A)
                )
            }
        }

        Spacer(modifier = Modifier.height(48.dp))
    }
}