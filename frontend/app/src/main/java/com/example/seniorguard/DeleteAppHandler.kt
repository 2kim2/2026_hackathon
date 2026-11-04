package com.example.seniorguard

import android.content.Context
import android.content.Intent
import android.net.Uri

fun requestAppDeletion(
    context: Context,
    packageName: String
) {
    val intent = Intent(
        Intent.ACTION_DELETE,
        Uri.parse("package:$packageName")
    )

    context.startActivity(intent)
}
