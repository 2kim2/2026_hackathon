package com.example.seniorguard

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun ParentFamilyScreen(
    modifier: Modifier = Modifier,
    onRequestClick: () -> Unit = {}
) {
    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Spacer(modifier = Modifier.height(40.dp))

        Text(
            text = "가족 연결",
            fontSize = 30.sp
        )

        Spacer(modifier = Modifier.height(20.dp))

        Text(
            text = "자녀와 연결하면\n위험 앱 발견 시 알려드려요.",
            fontSize = 22.sp
        )

        Spacer(modifier = Modifier.height(40.dp))

        Text(
            text = "가족 연결 코드",
            fontSize = 20.sp
        )

        Spacer(modifier = Modifier.height(16.dp))

        Text(
            text = "482913",
            fontSize = 36.sp
        )

        Spacer(modifier = Modifier.height(30.dp))

        Button(
            onClick = {
                // 추후 백엔드 코드 생성 API 연결
            }
        ) {
            Text("연결 코드 만들기", fontSize = 20.sp)
        }
        Spacer(modifier = Modifier.height(16.dp))

        OutlinedButton(
            onClick = onRequestClick,
            modifier = Modifier
                .fillMaxWidth()
                .height(70.dp)
        ) {
            Text(
                text = "받은 연결 요청 확인",
                fontSize = 20.sp
            )
        }
    }
}
