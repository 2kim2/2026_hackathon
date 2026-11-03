package com.example.seniorguard

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.foundation.Canvas
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun CompleteScreen(
    modifier: Modifier = Modifier,
    deletedCount: Int = 2,
    remainingCount: Int = 0,
    onHomeClick: () -> Unit = {}
) {
    val green = Color(0xFF207349)
    val dark = Color(0xFF1D2939)
    val gray = Color(0xFF526176)
    val orange = Color(0xFFF59A17)

    Column(
        modifier = modifier
            .fillMaxSize()
            .background(Color(0xFFF8F9FE))
            .padding(30.dp)
    ) {
        Spacer(modifier = Modifier.height(24.dp))

        Text(
            text = "안심 · 완료",
            fontSize = 22.sp,
            fontWeight = FontWeight.Bold,
            color = green
        )

        Spacer(modifier = Modifier.height(16.dp))

        Text(
            text = "의심 앱이\n발견되지 않았어요!",
            fontSize = 32.sp,
            fontWeight = FontWeight.Bold,
            lineHeight = 41.sp,
            color = green
        )

        Spacer(modifier = Modifier.height(16.dp))

        Text(
            text = "앱 ${deletedCount}개를 지운 뒤\n남은 앱을 다시 확인했어요.",
            fontSize = 20.sp,
            lineHeight = 30.sp,
            color = gray
        )

        Spacer(modifier = Modifier.height(26.dp))

        // 검사 완료 결과 카드
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .border(
                    1.dp,
                    Color(0xFFBBDDC8),
                    RoundedCornerShape(26.dp)
                )
                .background(
                    Color.White,
                    RoundedCornerShape(26.dp)
                )
                .padding(
                    horizontal = 20.dp,
                    vertical = 28.dp
                ),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            // 연한 초록색 원형 배경
            Box(
                modifier = Modifier
                    .size(140.dp)
                    .background(
                        Color(0xFFE7F4EC),
                        CircleShape
                    ),
                contentAlignment = Alignment.Center
            ) {
                // 원형 테두리와 체크 표시
                Canvas(modifier = Modifier.size(66.dp)) {
                    val stroke = 3.dp.toPx()

                    drawCircle(
                        color = green,
                        style = Stroke(width = stroke)
                    )

                    drawLine(
                        color = green,
                        start = Offset(
                            size.width * 0.28f,
                            size.height * 0.50f
                        ),
                        end = Offset(
                            size.width * 0.44f,
                            size.height * 0.66f
                        ),
                        strokeWidth = stroke,
                        cap = StrokeCap.Round
                    )

                    drawLine(
                        color = green,
                        start = Offset(
                            size.width * 0.44f,
                            size.height * 0.66f
                        ),
                        end = Offset(
                            size.width * 0.74f,
                            size.height * 0.35f
                        ),
                        strokeWidth = stroke,
                        cap = StrokeCap.Round
                    )
                }
            }

            Spacer(modifier = Modifier.height(32.dp))

            Text(
                text = "앱 확인을 끝냈어요!",
                fontSize = 27.sp,
                fontWeight = FontWeight.Bold,
                color = green,
                textAlign = TextAlign.Center
            )

            Spacer(modifier = Modifier.height(30.dp))

            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(105.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                // 지운 앱
                Column(
                    modifier = Modifier.weight(1f),
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.Center
                ) {
                    Text(
                        text = "지운 앱",
                        fontSize = 20.sp,
                        color = gray
                    )

                    Spacer(modifier = Modifier.height(12.dp))

                    Text(
                        text = "${deletedCount}개",
                        fontSize = 40.sp,
                        fontWeight = FontWeight.Bold,
                        color = dark
                    )
                }

                // 가운데 세로 구분선
                Box(
                    modifier = Modifier
                        .width(1.dp)
                        .fillMaxHeight()
                        .background(Color(0xFFD7E0EA))
                )

                // 남은 의심 앱
                Column(
                    modifier = Modifier.weight(1f),
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.Center
                ) {
                    Text(
                        text = "남은 의심 앱",
                        fontSize = 20.sp,
                        color = gray
                    )

                    Spacer(modifier = Modifier.height(12.dp))

                    Text(
                        text = "${remainingCount}개",
                        fontSize = 40.sp,
                        fontWeight = FontWeight.Bold,
                        color = green
                    )
                }
            }
        }

        Spacer(modifier = Modifier.weight(1f))

        Button(
            onClick = onHomeClick,
            modifier = Modifier
                .fillMaxWidth()
                .height(76.dp),
            shape = RoundedCornerShape(20.dp),
            colors = ButtonDefaults.buttonColors(
                containerColor = orange,
                contentColor = Color.Black
            )
        ) {
            Text(
                text = "홈으로 돌아가기",
                fontSize = 25.sp,
                fontWeight = FontWeight.Bold
            )
        }

        Spacer(modifier = Modifier.height(16.dp))
    }
}

@Preview(showBackground = true)
@Composable
fun CompleteScreenPreview() {
    CompleteScreen()
}
