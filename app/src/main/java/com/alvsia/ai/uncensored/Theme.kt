package com.alvsia.ai.uncensored

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Typography
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val Blue = Color(0xFF36A9FF)
private val DeepBlue = Color(0xFF06111F)
private val White = Color(0xFFF5FBFF)
private val Metal = Color(0xFFB8C7D9)

@Composable
fun AlvsiaTheme(content: @Composable () -> Unit) {
    val scheme = darkColorScheme(
        primary = Blue,
        secondary = Metal,
        background = DeepBlue,
        surface = Color(0xFF0A1828),
        onPrimary = Color.Black,
        onBackground = White,
        onSurface = White
    )
    MaterialTheme(colorScheme = scheme, typography = Typography(), content = content)
}
