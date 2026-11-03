package com.example.seniorguard

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun ChildFamilyScreen(
    modifier: Modifier = Modifier
) {
    var connectionCode by remember { mutableStateOf("") }
    var message by remember { mutableStateOf("") }

    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Spacer(modifier = Modifier.height(40.dp))

        Text(
            text = "가족 연결",
            fontSize = 30.sp,
            fontWeight = FontWeight.Bold
        )

        Spacer(modifier = Modifier.height(20.dp))

        Text(
            text = "부모님에게 받은\n연결 코드를 입력해주세요.",
            fontSize = 22.sp
        )

        Spacer(modifier = Modifier.height(40.dp))

        OutlinedTextField(
            value = connectionCode,
            onValueChange = {
                if (it.length <= 8 && it.all { ch -> ch.isDigit() }) {
                    connectionCode = it
                }
            },
            label = { Text("가족 연결 코드") },
            placeholder = { Text("8자리 숫자 입력") },
            keyboardOptions = KeyboardOptions(
                keyboardType = KeyboardType.Number
            ),
            singleLine = true,
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(modifier = Modifier.height(30.dp))

        Button(
            onClick = {
                message = if (connectionCode.length == 8) {
                    "코드 입력 완료! 서버 연결은 아직 준비 중이에요."
                } else {
                    "연결 코드는 8자리 숫자여야 해요."
                }
            },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text(
                text = "가족 연결하기",
                fontSize = 20.sp
            )
        }

        Spacer(modifier = Modifier.height(20.dp))

        Text(
            text = message,
            fontSize = 18.sp
        )
    }
}
