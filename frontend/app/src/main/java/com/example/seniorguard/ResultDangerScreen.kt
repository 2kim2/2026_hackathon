package com.example.seniorguard

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Description
import androidx.compose.material.icons.filled.Folder
import androidx.compose.material.icons.filled.Notifications
import androidx.compose.material.icons.filled.Security
import androidx.compose.material.icons.filled.Warning
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

// 위험 앱 데이터 모델
data class DangerAppInfo(
    val icon: ImageVector,
    val appName: String,
    val description: String
)

@Composable
fun ResultDangerScreen(
    onReScan: () -> Unit,
    modifier: Modifier = Modifier
) {
    // 카드가 3~4개 이상으로 많아지는 경우 시뮬레이션용 데이터
    val dangerAppList = listOf(
        DangerAppInfo(
            icon = Icons.Default.Description,
            appName = "PDF 뷰어",
            description = "다른 앱을 쓰는 중에도\n광고를 띄울 수 있어요."
        ),
        DangerAppInfo(
            icon = Icons.Default.Folder,
            appName = "메모리 정리",
            description = "알림으로 지속적인\n광고를 보낼 수 있어요."
        ),
        DangerAppInfo(
            icon = Icons.Default.Notifications,
            appName = "무료 알람 클리너",
            description = "백그라운드에서 과도한\n배터리를 소모해요."
        ),
        DangerAppInfo(
            icon = Icons.Default.Security,
            appName = "스마트 보안 도구",
            description = "불필요한 개인정보 권한을\n요청하고 있어요."
        )
    )

    Column(
        modifier = modifier
            .fillMaxSize()
            .background(Color(0xFFF4F7F9))
            .navigationBarsPadding()
            .padding(horizontal = 24.dp),
        horizontalAlignment = Alignment.Start,
        verticalArrangement = Arrangement.SpaceBetween
    ) {
        // 1. 상단 타이틀 영역
        Column(
            modifier = Modifier.fillMaxWidth()
        ) {
            Spacer(modifier = Modifier.height(12.dp))

            Row(
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(
                    imageVector = Icons.Default.Warning,
                    contentDescription = null,
                    tint = Color(0xFFB3261E),
                    modifier = Modifier.size(24.dp)
                )
                Spacer(modifier = Modifier.width(6.dp))
                Text(
                    text = "확인 결과 · 주의",
                    fontSize = 21.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color(0xFFB3261E)
                )
            }
            Spacer(modifier = Modifier.height(8.dp))

            Text(
                text = "위험이 감지된\n앱이 있어요!",
                fontSize = 28.sp,
                fontWeight = FontWeight.ExtraBold,
                color = Color(0xFFB3261E),
                lineHeight = 38.sp
            )

            Spacer(modifier = Modifier.height(20.dp))
        }

        // 2. 중앙 스크롤 가능 영역 (weight로 남은 공간 차지 및 독립 스크롤)
        LazyColumn(
            modifier = Modifier
                .fillMaxWidth()
                .weight(1f),
            verticalArrangement = Arrangement.spacedBy(16.dp),
            contentPadding = PaddingValues(bottom = 16.dp)
        ) {
            items(dangerAppList) { app ->
                DangerAppCard(
                    icon = app.icon,
                    appName = app.appName,
                    description = app.description
                )
            }
        }

        // 3. 하단 고정 오렌지 [다시 검사하기] 버튼
        Column(
            modifier = Modifier.fillMaxWidth()
        ) {
            Spacer(modifier = Modifier.height(12.dp))
            Button(
                onClick = onReScan,
                modifier = Modifier
                    .fillMaxWidth()
                    .height(76.dp),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFF59E1B)),
                shape = RoundedCornerShape(24.dp),
                elevation = ButtonDefaults.buttonElevation(defaultElevation = 0.dp)
            ) {
                Text(
                    text = "다시 검사하기",
                    fontSize = 26.sp,
                    fontWeight = FontWeight.ExtraBold,
                    color = Color(0xFF1B2A3A)
                )
            }
            Spacer(modifier = Modifier.height(48.dp))
        }
    }
}

@Composable
private fun DangerAppCard(
    icon: ImageVector,
    appName: String,
    description: String
) {
    Surface(
        modifier = Modifier
            .fillMaxWidth()
            .border(1.5.dp, Color(0xFFF9DEDC), RoundedCornerShape(28.dp)),
        color = Color.White,
        shape = RoundedCornerShape(28.dp),
        shadowElevation = 0.dp
    ) {
        Column(
            modifier = Modifier.padding(20.dp)
        ) {
            Row(
                verticalAlignment = Alignment.CenterVertically
            ) {
                Box(
                    modifier = Modifier
                        .size(54.dp)
                        .background(Color(0xFFFCE8E6), shape = RoundedCornerShape(16.dp)),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        imageVector = icon,
                        contentDescription = null,
                        tint = Color(0xFFB3261E),
                        modifier = Modifier.size(28.dp)
                    )
                }

                Spacer(modifier = Modifier.width(16.dp))

                Text(
                    text = appName,
                    fontSize = 24.sp,
                    fontWeight = FontWeight.ExtraBold,
                    color = Color(0xFF1B2A3A)
                )
            }

            Spacer(modifier = Modifier.height(14.dp))

            Text(
                text = description,
                fontSize = 18.sp,
                fontWeight = FontWeight.Bold,
                color = Color(0xFF1B2A3A),
                lineHeight = 26.sp
            )

            Spacer(modifier = Modifier.height(18.dp))

            Button(
                onClick = { /* 지우기 로직 */ },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(60.dp),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFB3261E)),
                shape = RoundedCornerShape(18.dp),
                elevation = ButtonDefaults.buttonElevation(defaultElevation = 0.dp)
            ) {
                Text(
                    text = "지우기",
                    fontSize = 24.sp,
                    fontWeight = FontWeight.ExtraBold,
                    color = Color.White
                )
            }
        }
    }
}