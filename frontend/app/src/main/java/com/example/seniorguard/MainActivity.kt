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
import androidx.compose.ui.text.input.PasswordVisualTransformation
import com.example.seniorguard.ui.theme.SeniorGuardTheme


class MainActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {

        super.onCreate(savedInstanceState)
        android.util.Log.d(
            "SeniorGuardUsage",
            "사용 기록 접근 권한: ${UsageEventMonitor.hasUsageAccess(this)}"
        )

        enableEdgeToEdge()

        FCMTokenManager.fetchToken { fcmToken ->
            // 여기에 나중에 FCMTokenSender.sendToken(...) 연결
        }

        setContent {
            SeniorGuardTheme {
                var currentScreen by remember {
                    mutableStateOf("menu")
                }
                var serverUrl by remember { mutableStateOf("") }
                var username by remember { mutableStateOf("") }
                var password by remember { mutableStateOf("") }
                var loginStatus by remember { mutableStateOf("") }
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
                                OutlinedTextField(
                                    value = serverUrl,
                                    onValueChange = { serverUrl = it },
                                    label = { Text("BE1 서버 주소") },
                                    placeholder = { Text("http://서버IP:포트") }
                                )

                                OutlinedTextField(
                                    value = username,
                                    onValueChange = { username = it },
                                    label = { Text("테스트 계정 아이디") }
                                )

                                OutlinedTextField(
                                    value = password,
                                    onValueChange = { password = it },
                                    label = { Text("테스트 계정 비밀번호") },
                                    visualTransformation = PasswordVisualTransformation()
                                )

                                Button(
                                    enabled = serverUrl.isNotBlank() &&
                                            username.isNotBlank() &&
                                            password.isNotBlank(),
                                    onClick = {
                                        loginStatus = "로그인 요청 중..."

                                        AuthManager.loginAndRegisterFCM(
                                            baseUrl = serverUrl,
                                            username = username,
                                            password = password,
                                            onResult = { message ->
                                                runOnUiThread {
                                                    loginStatus = message
                                                }
                                            }
                                        )
                                    }
                                ) {
                                    Text("로그인 후 FCM 토큰 등록")
                                }

                                Text(loginStatus)

                                Button(
                                    onClick = {
                                        if (UsageEventMonitor.hasUsageAccess(this@MainActivity)) {
                                            val intent = android.content.Intent(
                                                this@MainActivity,
                                                MonitoringService::class.java
                                            )

                                            androidx.core.content.ContextCompat.startForegroundService(
                                                this@MainActivity,
                                                intent
                                            )
                                        } else {
                                            UsageEventMonitor.openUsageAccessSettings(
                                                this@MainActivity
                                            )
                                        }
                                    }
                                ) {
                                    Text("백그라운드 감시 시작")
                                }

                                Button(
                                    onClick = {
                                        val intent = android.content.Intent(
                                            this@MainActivity,
                                            MonitoringService::class.java
                                        )
                                        stopService(intent)
                                    }
                                ) {
                                    Text("백그라운드 감시 중지")
                                }


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