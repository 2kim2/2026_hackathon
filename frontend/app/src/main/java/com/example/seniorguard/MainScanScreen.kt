package com.example.seniorguard

import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun MainScanScreen(
    onStartScan: () -> Unit,
    modifier: Modifier = Modifier
) {
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
                text = "내 휴대폰 살펴보기",
                fontSize = 21.sp,
                fontWeight = FontWeight.Bold,
                color = Color(0xFF1B2A3A)
            )
            Spacer(modifier = Modifier.height(8.dp))

            // 메인 대제목
            Text(
                text = "느려지는 핸드폰,\n함께 확인해 봐요",
                fontSize = 28.sp,
                fontWeight = FontWeight.ExtraBold,
                color = Color(0xFF1B2A3A),
                lineHeight = 38.sp
            )
        }

        // 중앙 메인 카드 버튼 (오렌지 배경)
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .height(320.dp)
                .clickable { onStartScan() },
            colors = CardDefaults.cardColors(containerColor = Color(0xFFF59E1B)),
            shape = RoundedCornerShape(32.dp),
            elevation = CardDefaults.cardElevation(defaultElevation = 0.dp)
        ) {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(24.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center
            ) {
                // 원형 영역 안에서 모서리가 삐져나가지 않도록 .clip(CircleShape) 적용
                Box(
                    modifier = Modifier
                        .size(136.dp)
                        .clip(CircleShape) // ★ 원형 클리핑 적용
                        .background(Color(0xFFE8F1F8)),
                    contentAlignment = Alignment.Center
                ) {
                    Image(
                        painter = painterResource(id = R.drawable.ic_shield),
                        contentDescription = "방패 아이콘",
                        contentScale = ContentScale.Crop, // ★ 네모 배경 자르기
                        modifier = Modifier
                            .size(136.dp)
                            .clip(CircleShape) // ★ 이미지에도 원형 클리핑 적용
                    )
                }

                Spacer(modifier = Modifier.height(20.dp))

                // 위험 앱 찾기 텍스트
                Text(
                    text = "위험 앱 찾기",
                    fontSize = 32.sp,
                    fontWeight = FontWeight.ExtraBold,
                    color = Color(0xFF1B2A3A)
                )
            }
        }

        Spacer(modifier = Modifier.height(48.dp))
    }
}