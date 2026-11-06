package com.example.seniorguard

import androidx.compose.foundation.layout.*
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp

@Composable
fun DeleteTestScreen(
    modifier: Modifier = Modifier
) {
    val context = LocalContext.current

    Column(
        modifier = modifier.padding(24.dp)
    ) {
        Text("앱 삭제 기능 테스트")

        Spacer(modifier = Modifier.height(24.dp))

        Button(
            onClick = {
                requestAppDeletion(
                    context = context,
                    packageName = "com.example.testapp"
                )
            }
        ) {
            Text("삭제 화면 열기")
        }
    }
}
