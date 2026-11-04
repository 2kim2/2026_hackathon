package com.example.seniorguard

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun ResultScreen(modifier: Modifier = Modifier) {
    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(20.dp)
    ) {
        Text("확인 결과 · 주의", fontSize = 20.sp)

        Text(
            "위험이 감지된 앱이 있어요!",
            fontSize = 24.sp
        )

        Text("PDF 뷰어", fontSize = 20.sp)

        Text(
            "다른 앱을 쓰는 중에도 광고를 띄울 수 있어요.",
            fontSize = 20.sp
        )

        Button(onClick = {}) {
            Text("지우기")
        }

        Text("메모리 정리", fontSize = 20.sp)

        Text(
            "알림으로 지속적인 광고를 보낼 수 있어요.",
            fontSize = 20.sp
        )

        Button(onClick = {}) {
            Text("지우기")
        }

        Button(onClick = {}) {
            Text("다시 검사하기")
        }
    }
}
