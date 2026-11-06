
package com.example.seniorguard

import android.content.Intent
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import androidx.core.content.ContextCompat
import com.example.seniorguard.ui.theme.SeniorGuardTheme

class MainActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        android.util.Log.d(
            "SeniorGuardUsage",
            "사용 기록 접근 권한: ${
                UsageEventMonitor.hasUsageAccess(this)
            }"
        )

        enableEdgeToEdge()

        // FCM 토큰 발급 기능 유지
        FCMTokenManager.fetchToken()

        setContent {
            SeniorGuardTheme {

                var currentScreen by remember {
                    mutableStateOf("permission")
                }

                var monitoringStarted by remember {
                    mutableStateOf(false)
                }

                var serverUrl by remember {
                    mutableStateOf("")
                }

                var username by remember {
                    mutableStateOf("")
                }

                var password by remember {
                    mutableStateOf("")
                }

                var loginStatus by remember {
                    mutableStateOf("")
                }

                // 실제 모니터링 시작
                fun startMonitoring() {
                    if (UsageEventMonitor.hasUsageAccess(
                            this@MainActivity
                        )
                    ) {
                        val intent = Intent(
                            this@MainActivity,
                            MonitoringService::class.java
                        )

                        ContextCompat.startForegroundService(
                            this@MainActivity,
                            intent
                        )

                        monitoringStarted = true
                        currentScreen = "scanning"

                    } else {
                        UsageEventMonitor.openUsageAccessSettings(
                            this@MainActivity
                        )
                    }
                }

                // 실제 모니터링 중지
                fun stopMonitoring() {
                    val intent = Intent(
                        this@MainActivity,
                        MonitoringService::class.java
                    )

                    stopService(intent)

                    monitoringStarted = false
                    currentScreen = "mainScan"
                }

                Scaffold(
                    modifier = Modifier.fillMaxSize(),

                    topBar = {
                        if (
                            currentScreen != "permission" &&
                            currentScreen != "mainScan" &&
                            currentScreen != "menu"
                        ) {
                            Box(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .statusBarsPadding()
                                    .padding(
                                        horizontal = 8.dp,
                                        vertical = 4.dp
                                    )
                            ) {
                                TextButton(
                                    onClick = {
                                        currentScreen = "mainScan"
                                    }
                                ) {
                                    Text("← 뒤로 가기")
                                }
                            }
                        }
                    }

                ) { innerPadding ->

                    when (currentScreen) {

                        // 개발용 테스트 메뉴 유지
                        "menu" -> {
                            Column(
                                modifier = Modifier
                                    .padding(innerPadding)
                                    .fillMaxSize()
                                    .padding(24.dp),
                                verticalArrangement =
                                    Arrangement.spacedBy(12.dp)
                            ) {

                                Text(
                                    text = "시니어가드 화면 테스트",
                                    style = MaterialTheme
                                        .typography.headlineSmall
                                )

                                OutlinedTextField(
                                    value = serverUrl,
                                    onValueChange = {
                                        serverUrl = it
                                    },
                                    label = {
                                        Text("BE1 서버 주소")
                                    }
                                )

                                OutlinedTextField(
                                    value = username,
                                    onValueChange = {
                                        username = it
                                    },
                                    label = {
                                        Text("테스트 계정 아이디")
                                    }
                                )

                                OutlinedTextField(
                                    value = password,
                                    onValueChange = {
                                        password = it
                                    },
                                    label = {
                                        Text("테스트 계정 비밀번호")
                                    },
                                    visualTransformation =
                                        PasswordVisualTransformation()
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
                                        startMonitoring()
                                    }
                                ) {
                                    Text("백그라운드 감시 시작")
                                }

                                Button(
                                    onClick = {
                                        stopMonitoring()
                                    }
                                ) {
                                    Text("백그라운드 감시 중지")
                                }

                                Button(
                                    onClick = {
                                        currentScreen = "permission"
                                    }
                                ) {
                                    Text("권한 안내 화면")
                                }

                                Button(
                                    onClick = {
                                        currentScreen = "mainScan"
                                    }
                                ) {
                                    Text("메인 검사 화면")
                                }

                                Button(
                                    onClick = {
                                        currentScreen = "parent"
                                    }
                                ) {
                                    Text("부모용 가족 화면")
                                }

                                Button(
                                    onClick = {
                                        currentScreen = "parentRequests"
                                    }
                                ) {
                                    Text("부모용 연결 요청 확인")
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

                                Button(
                                    onClick = {
                                        currentScreen = "resultDanger"
                                    }
                                ) {
                                    Text("위험 감지 결과 화면")
                                }
                            }
                        }

                        // 1. 권한 안내 화면
                        "permission" -> PermissionScreen(
                            modifier = Modifier.padding(innerPadding),

                            onNavigateToMain = {
                                if (
                                    UsageEventMonitor.hasUsageAccess(
                                        this@MainActivity
                                    )
                                ) {
                                    currentScreen = "mainScan"
                                } else {
                                    UsageEventMonitor
                                        .openUsageAccessSettings(
                                            this@MainActivity
                                        )
                                }
                            }
                        )

                        // 2. 메인 검사 화면
                        "mainScan" -> {
                            Column(
                                modifier = Modifier
                                    .padding(innerPadding)
                                    .fillMaxSize()
                            ) {

                                MainScanScreen(
                                    modifier = Modifier.weight(1f),

                                    onStartScan = {
                                        startMonitoring()
                                    }
                                )

                                if (monitoringStarted) {
                                    Button(
                                        onClick = {
                                            stopMonitoring()
                                        },
                                        modifier = Modifier
                                            .fillMaxWidth()
                                            .padding(
                                                horizontal = 24.dp,
                                                vertical = 12.dp
                                            )
                                    ) {
                                        Text("모니터링 중지")
                                    }
                                }
                            }
                        }

                        // 3. 실제 모니터링 상태 화면
                        "scanning" -> {
                            Column(
                                modifier = Modifier
                                    .padding(innerPadding)
                                    .fillMaxSize()
                                    .padding(24.dp),

                                verticalArrangement =
                                    Arrangement.Center
                            ) {

                                Text(
                                    text = "스마트폰 모니터링 중",
                                    style = MaterialTheme
                                        .typography.headlineMedium
                                )

                                Spacer(
                                    modifier = Modifier.height(16.dp)
                                )

                                Text(
                                    "앱 사용 기록과 기기 상태를 " +
                                            "수집하고 있어요."
                                )

                                Spacer(
                                    modifier = Modifier.height(12.dp)
                                )

                                Text(
                                    "위험도 자동 분석은 " +
                                            "아직 연결되지 않았습니다."
                                )

                                Spacer(
                                    modifier = Modifier.height(24.dp)
                                )

                                Button(
                                    onClick = {
                                        stopMonitoring()
                                    }
                                ) {
                                    Text("모니터링 중지")
                                }

                                Spacer(
                                    modifier = Modifier.height(12.dp)
                                )

                                OutlinedButton(
                                    onClick = {
                                        currentScreen = "mainScan"
                                    }
                                ) {
                                    Text("메인 화면으로")
                                }
                            }
                        }

                        // 4. 위험 결과 화면 (기존 UI 유지)
                        "resultDanger" -> ResultDangerScreen(
                            modifier = Modifier.padding(innerPadding),

                            onReScan = {
                                startMonitoring()
                            }
                        )

                        // 보호자 가족 화면
                        "parent" -> ParentFamilyScreen(
                            modifier = Modifier.padding(innerPadding),

                            onRequestClick = {
                                currentScreen = "parentRequests"
                            }
                        )

                        // 연결 요청 화면
                        "parentRequests" -> ParentRequestScreen(
                            modifier = Modifier.padding(innerPadding)
                        )

                        // 시니어 가족 화면
                        "child" -> ChildFamilyScreen(
                            modifier = Modifier.padding(innerPadding)
                        )

                        // 가족 알림 화면
                        "alerts" -> FamilyAlertScreen(
                            modifier = Modifier.padding(innerPadding),
                            alerts = emptyList()
                        )

                        // 검사 완료 화면
                        "complete" -> CompleteScreen(
                            modifier = Modifier.padding(innerPadding),

                            onHomeClick = {
                                currentScreen = "mainScan"
                            }
                        )
                    }
                }
            }
        }
    }
}
