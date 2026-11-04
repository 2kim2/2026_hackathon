package com.example.seniorguard

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.People

// 연결 요청 데이터
data class FamilyRequest(
    val id: Int,
    val guardianUsername: String,
    val status: String
)

@Composable
fun ParentRequestScreen(
    modifier: Modifier = Modifier
) {
    val green = Color(0xFF207349)
    val orange = Color(0xFFF59A17)
    val gray = Color(0xFF526176)

    // 테스트용 연결 요청
    var requests by remember {
        mutableStateOf(
            listOf(
                FamilyRequest(
                    id = 1,
                    guardianUsername = "guardian01",
                    status = "pending"
                )
            )
        )
    }

    var message by remember {
        mutableStateOf("")
    }

    Column(
        modifier = modifier
            .fillMaxSize()
            .background(Color(0xFFF8F9FE))
            .padding(16.dp)
    ) {
        Spacer(modifier = Modifier.height(24.dp))

        Text(
            text = "가족 연결 · 부모용",
            fontSize = 22.sp,
            fontWeight = FontWeight.Bold,
            color = green
        )

        Spacer(modifier = Modifier.height(16.dp))

        Text(
            text = "가족 연결 요청이\n도착했어요!",
            fontSize = 30.sp,
            lineHeight = 40.sp,
            fontWeight = FontWeight.Bold
        )

        Spacer(modifier = Modifier.height(12.dp))

        Text(
            text = "자녀가 보낸 연결 요청을\n확인해주세요.",
            fontSize = 20.sp,
            lineHeight = 30.sp,
            color = gray
        )

        Spacer(modifier = Modifier.height(24.dp))

        if (requests.isEmpty()) {
            Text(
                text = "현재 대기 중인 연결 요청이 없어요.",
                fontSize = 20.sp
            )
        } else {
            LazyColumn(
                verticalArrangement = Arrangement.spacedBy(16.dp),
                modifier = Modifier.weight(1f)
            ) {
                items(
                    items = requests,
                    key = { it.id }
                ) { request ->

                    Card(
                        modifier = Modifier.fillMaxWidth(),
                        shape = RoundedCornerShape(24.dp),
                        colors = CardDefaults.cardColors(
                            containerColor = Color.White
                        )
                    ) {
                        Column(
                            modifier = Modifier.padding(20.dp),
                            horizontalAlignment = Alignment.CenterHorizontally
                        ) {
                            Box(
                                modifier = Modifier
                                    .size(100.dp)
                                    .background(
                                        Color(0xFFE7F4EC),
                                        CircleShape
                                    ),
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(
                                    imageVector = Icons.Default.People,
                                    contentDescription = "가족 연결",
                                    tint = green,
                                    modifier = Modifier.size(56.dp)
                                )
                            }

                            Spacer(modifier = Modifier.height(20.dp))

                            Text(
                                text = "가족 연결 요청",
                                fontSize = 24.sp,
                                fontWeight = FontWeight.Bold,
                                color = green
                            )

                            Spacer(modifier = Modifier.height(12.dp))

                            Text(
                                text = "보호자: ${request.guardianUsername}",
                                fontSize = 20.sp,
                                textAlign = TextAlign.Center
                            )

                            Spacer(modifier = Modifier.height(28.dp))

                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement =
                                    Arrangement.spacedBy(12.dp)
                            ) {
                                OutlinedButton(
                                    onClick = {
                                        requests = requests.filter {
                                            it.id != request.id
                                        }
                                        message = "연결 요청을 거절했어요. (테스트)"
                                    },
                                    modifier = Modifier.weight(1f)
                                ) {
                                    Text(
                                        "거절하기",
                                        fontSize = 18.sp
                                    )
                                }

                                Button(
                                    onClick = {
                                        requests = requests.filter {
                                            it.id != request.id
                                        }
                                        message = "가족 연결을 수락했어요. (테스트)"
                                    },
                                    modifier = Modifier.weight(1f),
                                    colors = ButtonDefaults.buttonColors(
                                        containerColor = orange,
                                        contentColor = Color.Black
                                    )
                                ) {
                                    Text(
                                        "수락하기",
                                        fontSize = 18.sp
                                    )
                                }
                            }
                        }
                    }
                }
            }
        }

        if (message.isNotEmpty()) {
            Text(
                text = message,
                fontSize = 18.sp,
                color = green,
                modifier = Modifier.padding(vertical = 16.dp)
            )
        }
    }
}

@Preview(showBackground = true)
@Composable
fun ParentRequestPreview() {
    ParentRequestScreen()
}
