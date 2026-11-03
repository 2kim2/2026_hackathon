package com.example.seniorguard

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.example.seniorguard.ui.theme.SeniorGuardTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

        FCMTokenManager.fetchToken()

        setContent {
            SeniorGuardTheme {
                var currentScreen by remember {
                    mutableStateOf("menu")
                }
                Scaffold(
                    modifier = Modifier.fillMaxSize(),
                    topBar = {
                        if (currentScreen != "menu") {
                            TextButton(
                                onClick = {
                                    currentScreen = "menu"
                                }
                            ) {
                                Text("← 뒤로 가기")
                            }
                        }
                    }
                ) { innerPadding ->
                when (currentScreen) {
                        "menu" -> {
                            Column(
                                modifier = Modifier
                                    .padding(innerPadding)
                                    .padding(24.dp),
                                verticalArrangement =
                                    Arrangement.spacedBy(16.dp)
                            ) {
                                Text(
                                    text = "시니어가드 화면 테스트",
                                    style = MaterialTheme.typography.headlineSmall
                                )

                                Button(
                                    onClick = {
                                        currentScreen = "parent"
                                    }
                                ) {
                                    Text("부모용 가족 화면")
                                    Button(
                                        onClick = {
                                            currentScreen = "parentRequests"
                                        }
                                    ) {
                                        Text("부모용 연결 요청 확인")
                                    }
                                }

                                Button(
                                    onClick = {
                                        currentScreen = "child"
                                    }
                                ) {
                                    Text("자녀용 가족 화면")
                                }

                                Button(
                                    onClick = {
                                        currentScreen = "alerts"
                                    }
                                ) {
                                    Text("가족 알림 화면")
                                }

                                Button(
                                    onClick = {
                                        currentScreen = "complete"
                                    }
                                ) {
                                    Text("검사 완료 화면")
                                }
                            }
                        }

                        "parent" -> ParentFamilyScreen(
                            modifier = Modifier.padding(innerPadding),
                            onRequestClick = {
                                currentScreen = "parentRequests"
                            }
                        )
                        "parentRequests" -> ParentRequestScreen(
                            modifier = Modifier.padding(innerPadding)
                        )

                        "child" -> ChildFamilyScreen(
                            modifier = Modifier.padding(innerPadding)
                        )

                        "alerts" -> FamilyAlertScreen(
                            modifier = Modifier.padding(innerPadding)
                        )

                        "complete" -> CompleteScreen(
                            modifier = Modifier.padding(innerPadding),
                            onHomeClick = {
                                currentScreen = "menu"
                            }
                        )
                    }
                }
            }
        }
    }
}
