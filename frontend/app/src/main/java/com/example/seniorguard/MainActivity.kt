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
                            Box(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .statusBarsPadding()
                                    .padding(horizontal = 8.dp, vertical = 4.dp)
                            ) {
                                TextButton(
                                    onClick = {
                                        currentScreen = "menu"
                                    }
                                ) {
                                    Text(
                                        text = "← 뒤로 가기",
                                        style = MaterialTheme.typography.titleMedium
                                    )
                                }
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
                                verticalArrangement = Arrangement.spacedBy(16.dp)
                            ) {
                                Text(
                                    text = "시니어가드 화면 테스트",
                                    style = MaterialTheme.typography.headlineSmall
                                )

                                // 1번 파트
                                Button(onClick = { currentScreen = "permission" }) { Text("권한 안내 화면") }
                                Button(onClick = { currentScreen = "mainScan" }) { Text("메인 검사 화면") }
                                Button(onClick = { currentScreen = "scanning" }) { Text("검사 진행 화면") }
                                Button(onClick = { currentScreen = "resultDanger" }) { Text("위험 감지 결과") }

                                // 2번 파트
                                Button(onClick = { currentScreen = "parent" }) { Text("부모용 가족 화면") }
                                Button(onClick = { currentScreen = "parentRequests" }) { Text("부모용 연결 요청 확인") }
                                Button(onClick = { currentScreen = "child" }) { Text("자녀용 가족 화면") }
                                Button(onClick = { currentScreen = "alerts" }) { Text("가족 알림 화면") }
                                Button(onClick = { currentScreen = "complete" }) { Text("검사 완료 화면") }
                            }
                        }

                        // 1번 파트
                        "permission" -> PermissionScreen(
                            modifier = Modifier.padding(innerPadding),
                            onNavigateToMain = { currentScreen = "mainScan" }
                        )
                        "mainScan" -> MainScanScreen(
                            modifier = Modifier.padding(innerPadding),
                            onStartScan = { currentScreen = "scanning" }
                        )
                        "scanning" -> ScanningScreen(
                            modifier = Modifier.padding(innerPadding),
                            onScanComplete = { isDanger ->
                                currentScreen = if (isDanger) "resultDanger" else "complete"
                            }
                        )
                        "resultDanger" -> ResultDangerScreen(
                            modifier = Modifier.padding(innerPadding),
                            onReScan = { currentScreen = "scanning" }
                        )

                        // 2번 파트
                        "parent" -> ParentFamilyScreen(
                            modifier = Modifier.padding(innerPadding),
                            onRequestClick = { currentScreen = "parentRequests" }
                        )
                        "parentRequests" -> ParentRequestScreen(
                            modifier = Modifier.padding(innerPadding)
                        )
                        "child" -> ChildFamilyScreen(
                            modifier = Modifier.padding(innerPadding)
                        )
                        "alerts" -> FamilyAlertScreen(
                            modifier = Modifier.padding(innerPadding),
                            alerts = emptyList()
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