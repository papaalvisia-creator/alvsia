package com.alvsia.ai.uncensored

import android.net.Uri
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.alpha
import androidx.compose.ui.background
import androidx.compose.ui.clip
import androidx.compose.ui.draw.rotate
import androidx.compose.ui.draw.scale
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.platform.LocalContext
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import com.alvsia.ai.uncensored.security.ApkIntegrity
import com.alvsia.ai.uncensored.security.RuntimeGuard
import com.alvsia.ai.uncensored.security.SessionGuard
import com.alvsia.ai.uncensored.security.ThreatReporter

private val Ink = Color(0xFF03050B)
private val Deep = Color(0xFF070B18)
private val Panel = Color(0xFF0E1224)
private val Violet = Color(0xFF9D6CFF)
private val Violet2 = Color(0xFFD5B8FF)
private val Cyan = Color(0xFF66E7FF)
private val Green = Color(0xFF64E6B2)
private val Muted = Color(0xFF9AA7C1)

class MainActivity : ComponentActivity() {
    private var pickedUri by mutableStateOf<Uri?>(null)

    private val filePicker = registerForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->
        pickedUri = uri
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val integrity = ApkIntegrity.inspect(this)
        if (!integrity.valid) ThreatReporter.report("APK_INTEGRITY", integrity.reasons)
        val runtime = RuntimeGuard.inspect(this)
        if (!runtime.clean || runtime.softSignals.isNotEmpty()) {
            ThreatReporter.report("RUNTIME_SCAN", runtime.hardSignals + runtime.softSignals)
        }
        window.statusBarColor = android.graphics.Color.rgb(3, 5, 11)
        window.navigationBarColor = android.graphics.Color.rgb(2, 3, 8)
        setContent {
            AlvsiaTheme {
                AlvsiaApp(
                    pickedUri = pickedUri,
                    onPickFile = { filePicker.launch(arrayOf("*/*")) },
                    onClearFile = { pickedUri = null }
                )
            }
        }
    }
}

@Composable
private fun AlvsiaApp(
    pickedUri: Uri?,
    onPickFile: () -> Unit,
    onClearFile: () -> Unit
) {
    val context = LocalContext.current
    var splashDone by remember { mutableStateOf(false) }
    var bootStep by remember { mutableStateOf("INITIALIZING") }
    var bootProgress by remember { mutableFloatStateOf(0.05f) }

    LaunchedEffect(Unit) {
        val steps = listOf(
            "INITIALIZING" to 0.18f,
            "SECURE RUNTIME" to 0.42f,
            "LOADING MODELS" to 0.70f,
            "UNIVERSAL ENGINE" to 0.88f,
            "READY" to 1f
        )
        for ((label, progress) in steps) {
            bootStep = label
            bootProgress = progress
            delay(if (label == "READY") 360 else 340)
        }
        splashDone = true
    }

    AnimatedContent(
        targetState = splashDone,
        transitionSpec = { fadeIn(tween(500)) togetherWith fadeOut(tween(250)) },
        label = "app-root"
    ) { ready ->
        if (!ready) LiveSplash(step = bootStep, progress = bootProgress)
        else MainWorkspace(context, pickedUri, onPickFile, onClearFile)
    }
}

@Composable
private fun LiveSplash(step: String, progress: Float) {
    val transition = rememberInfiniteTransition(label = "splash")
    val pulse by transition.animateFloat(
        initialValue = 0.92f, targetValue = 1.08f,
        animationSpec = infiniteRepeatable(tween(1200, easing = FastOutSlowInEasing), RepeatMode.Reverse),
        label = "pulse"
    )
    val spin by transition.animateFloat(
        initialValue = 0f, targetValue = 360f,
        animationSpec = infiniteRepeatable(tween(7000), RepeatMode.Restart),
        label = "spin"
    )
    val reverseSpin by transition.animateFloat(
        initialValue = 360f, targetValue = 0f,
        animationSpec = infiniteRepeatable(tween(4800), RepeatMode.Restart),
        label = "reverse-spin"
    )
    val sweep by transition.animateFloat(
        initialValue = 0f, targetValue = 1f,
        animationSpec = infiniteRepeatable(tween(1600), RepeatMode.Reverse),
        label = "sweep"
    )

    Box(
        Modifier.fillMaxSize().background(
            Brush.radialGradient(listOf(Color(0xFF25104C), Deep, Ink), radius = 900f)
        ),
        contentAlignment = Alignment.Center
    ) {
        Canvas(Modifier.fillMaxSize().alpha(0.55f)) {
            val center = Offset(size.width / 2f, size.height * 0.42f)
            val radius = size.minDimension * 0.39f
            drawCircle(Color(0x309D6CFF), radius = radius * (0.92f + sweep * 0.08f))
            drawArc(
                Brush.sweepGradient(listOf(Color.Transparent, Violet, Color.Transparent)),
                startAngle = spin, sweepAngle = 95f, useCenter = false,
                topLeft = Offset(center.x - radius, center.y - radius),
                size = androidx.compose.ui.geometry.Size(radius * 2, radius * 2),
                style = Stroke(3f, cap = StrokeCap.Round)
            )
            drawArc(
                Brush.sweepGradient(listOf(Color.Transparent, Cyan, Color.Transparent)),
                startAngle = reverseSpin, sweepAngle = 70f, useCenter = false,
                topLeft = Offset(center.x - radius * 0.82f, center.y - radius * 0.82f),
                size = androidx.compose.ui.geometry.Size(radius * 1.64f, radius * 1.64f),
                style = Stroke(2f, cap = StrokeCap.Round)
            )
            repeat(12) { i ->
                val angle = Math.toRadians((i * 30.0) + spin * 0.35)
                val r1 = radius * 0.72f
                val r2 = radius * 0.78f
                drawLine(
                    Color(0x8066E7FF),
                    Offset(center.x + kotlin.math.cos(angle).toFloat() * r1, center.y + kotlin.math.sin(angle).toFloat() * r1),
                    Offset(center.x + kotlin.math.cos(angle).toFloat() * r2, center.y + kotlin.math.sin(angle).toFloat() * r2),
                    strokeWidth = 2f
                )
            }
        }

        Column(
            Modifier.fillMaxWidth().padding(horizontal = 28.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Box(contentAlignment = Alignment.Center, modifier = Modifier.size(245.dp)) {
                Canvas(Modifier.fillMaxSize().rotate(spin)) {
                    drawCircle(
                        Brush.radialGradient(listOf(Color(0x55D5B8FF), Color.Transparent)),
                        radius = size.minDimension * 0.47f
                    )
                    drawCircle(
                        Color.Transparent,
                        radius = size.minDimension * 0.40f,
                        style = Stroke(2f)
                    )
                }
                Image(
                    painterResource(R.drawable.alvsia_ai_logo),
                    contentDescription = "ALVSIA",
                    modifier = Modifier.size(138.dp).scale(pulse)
                )
            }
            Text("ALVSIA", color = Violet2, fontSize = 15.sp, fontWeight = FontWeight.Black, letterSpacing = 7.sp)
            Text("UNCENSORED AI", color = Color.White, fontSize = 28.sp, fontWeight = FontWeight.ExtraBold, letterSpacing = 1.2.sp)
            Text("UNIVERSAL INTELLIGENCE RUNTIME", color = Muted, fontSize = 9.sp, letterSpacing = 2.sp)
            Spacer(Modifier.height(34.dp))
            Text(step, color = Cyan, fontSize = 10.sp, fontWeight = FontWeight.Bold, letterSpacing = 2.sp)
            Spacer(Modifier.height(10.dp))
            Box(
                Modifier.fillMaxWidth(0.78f).height(5.dp).clip(RoundedCornerShape(5.dp))
                    .background(Color(0x303A4260))
            ) {
                Box(
                    Modifier.fillMaxWidth(progress.coerceIn(0f, 1f)).fillMaxHeight()
                        .background(Brush.horizontalGradient(listOf(Violet, Cyan)))
                )
            }
            Spacer(Modifier.height(10.dp))
            Text(
                "MULTI MODEL  •  UNIVERSAL FILE ENGINE  •  SECURE RUNTIME",
                color = Color(0xFF7886A3), fontSize = 8.sp, letterSpacing = 0.8.sp
            )
        }
    }
}

@Composable
private fun MainWorkspace(
    context: android.content.Context,
    pickedUri: Uri?,
    onPickFile: () -> Unit,
    onClearFile: () -> Unit
) {
    val prefs = remember { SecurePrefs(context) }
    val auth = remember { PanelAuth(BuildConfig.PANEL_BASE_URL) }
    val gateway = remember { AiGateway(BuildConfig.PANEL_BASE_URL) }
    val catalog = remember { ModelCatalogRepository(BuildConfig.PANEL_BASE_URL) }
    val scope = rememberCoroutineScope()
    var token by remember { mutableStateOf(prefs.token().orEmpty()) }
    val sessionGuard = remember { SessionGuard().apply { if (token.isNotBlank()) runCatching { activate(token) } } }
    var license by remember { mutableStateOf("") }
    var authBusy by remember { mutableStateOf(false) }
    var authError by remember { mutableStateOf<String?>(null) }
    var models by remember { mutableStateOf(ModelCatalog.starter) }
    var selected by remember { mutableStateOf(ModelCatalog.starter.first()) }
    var query by remember { mutableStateOf("") }
    var prompt by remember { mutableStateOf("") }
    var answer by remember { mutableStateOf("Sistem siap. Pilih model, masukkan file apa pun, atau langsung bicara dengan AI.") }
    var busy by remember { mutableStateOf(false) }
    var showModels by remember { mutableStateOf(false) }
    var analysis by remember { mutableStateOf<UniversalAnalysisResult?>(null) }
    var analysisBusy by remember { mutableStateOf(false) }

    LaunchedEffect(Unit) {
        val loaded = withContext(Dispatchers.IO) { catalog.load() }
        if (loaded.isNotEmpty()) {
            models = loaded
            selected = loaded.firstOrNull { it.id == prefs.modelId() } ?: loaded.first()
        }
    }

    LaunchedEffect(pickedUri) {
        val uri = pickedUri ?: return@LaunchedEffect
        analysisBusy = true
        analysis = withContext(Dispatchers.IO) {
            UniversalAnalysisEngine.analyze(context.contentResolver, uri)
        }
        analysisBusy = false
    }

    if (token.isBlank()) {
        LoginExperience(
            license, { license = it }, authBusy, authError,
            onLogin = {
                authBusy = true
                authError = null
                scope.launch {
                    val result = withContext(Dispatchers.IO) {
                        runCatching { auth.login(license, PanelAuth.deviceId(context)) }
                    }
                    result.onSuccess {
                        prefs.setToken(it.token)
                        sessionGuard.activate(it.token)
                        token = it.token
                        answer = "Sesi ALVSIA aktif."
                    }.onFailure {
                        authError = it.message ?: "Login gagal."
                    }
                    authBusy = false
                }
            }
        )
        return
    }

    Scaffold(containerColor = Ink, bottomBar = { BottomNav() }) { pad ->
        Column(
            Modifier.fillMaxSize().padding(pad)
                .background(Brush.verticalGradient(listOf(Color(0xFF0A0B1A), Ink, Color(0xFF020308))))
                .padding(horizontal = 16.dp, vertical = 12.dp)
        ) {
            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth()) {
                Box(contentAlignment = Alignment.Center) {
                    Box(Modifier.size(48.dp).clip(CircleShape).background(Color(0x302A1555)))
                    Image(painterResource(R.drawable.alvsia_ai_logo), null, modifier = Modifier.size(38.dp).clip(CircleShape))
                }
                Spacer(Modifier.width(12.dp))
                Column(Modifier.weight(1f)) {
                    Text("ALVSIA", color = Violet2, fontSize = 11.sp, fontWeight = FontWeight.Bold, letterSpacing = 3.sp)
                    Text("UNCENSORED AI", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.ExtraBold)
                    Text("UNIVERSAL INTELLIGENCE", color = Muted, fontSize = 8.sp, letterSpacing = 1.2.sp)
                }
                Surface(color = Color(0x1964E6B2), shape = RoundedCornerShape(20.dp)) {
                    Row(Modifier.padding(horizontal = 10.dp, vertical = 7.dp), verticalAlignment = Alignment.CenterVertically) {
                        Box(Modifier.size(6.dp).clip(CircleShape).background(Green))
                        Spacer(Modifier.width(6.dp))
                        Text("LIVE", color = Green, fontSize = 9.sp, fontWeight = FontWeight.Bold)
                    }
                }
            }

            Spacer(Modifier.height(14.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                GlassMetric("BRAIN", "READY", Modifier.weight(1f))
                GlassMetric("MODELS", models.size.toString(), Modifier.weight(1f))
                GlassMetric("ENGINE", "AUTO", Modifier.weight(1f))
            }

            Spacer(Modifier.height(12.dp))
            ElevatedCard(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(22.dp),
                colors = CardDefaults.elevatedCardColors(containerColor = Panel)
            ) {
                Column(Modifier.padding(15.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Column(Modifier.weight(1f)) {
                            Text("UNIVERSAL ENGINE", color = Violet2, fontSize = 10.sp, fontWeight = FontWeight.Bold, letterSpacing = 1.5.sp)
                            Text("Auto-detect • Stream • Analyze", color = Color.White, fontSize = 15.sp, fontWeight = FontWeight.Bold)
                        }
                        TextButton(onClick = onPickFile) { Text("OPEN FILE", color = Cyan, fontWeight = FontWeight.Bold, fontSize = 10.sp) }
                    }
                    if (analysisBusy) {
                        Spacer(Modifier.height(12.dp))
                        LinearProgressIndicator(
                            modifier = Modifier.fillMaxWidth().height(4.dp).clip(RoundedCornerShape(4.dp)),
                            color = Violet2, trackColor = Color(0x223A4260)
                        )
                        Text("Menganalisis secara streaming — RAM tetap terkendali untuk file sangat besar.", color = Muted, fontSize = 9.sp)
                    }
                    analysis?.let { result ->
                        Spacer(Modifier.height(10.dp))
                        AnalysisCard(result, onClearFile)
                    }
                }
            }

            Spacer(Modifier.height(12.dp))
            ElevatedCard(
                modifier = Modifier.fillMaxWidth().weight(1f),
                shape = RoundedCornerShape(24.dp),
                colors = CardDefaults.elevatedCardColors(containerColor = Color(0xFF0B0E1B))
            ) {
                Column(Modifier.padding(15.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Column(Modifier.weight(1f)) {
                            Text("AI WORKSPACE", color = Violet2, fontSize = 10.sp, fontWeight = FontWeight.Bold, letterSpacing = 1.5.sp)
                            Text(selected.name, color = Color.White, fontSize = 13.sp, fontWeight = FontWeight.Bold)
                        }
                        TextButton(onClick = { showModels = !showModels }) {
                            Text(if (showModels) "CLOSE" else "MODELS", color = Cyan, fontSize = 9.sp)
                        }
                    }
                    AnimatedVisibility(showModels) {
                        Column {
                            OutlinedTextField(query, { query = it }, modifier = Modifier.fillMaxWidth(), placeholder = { Text("Cari model") }, singleLine = true)
                            LazyColumn(Modifier.heightIn(max = 180.dp)) {
                                items(models.filter { query.isBlank() || it.name.contains(query, true) || it.tags.any { t -> t.contains(query, true) } }) { model ->
                                    ListItem(
                                        headlineContent = { Text(model.name, color = Color.White) },
                                        supportingContent = { Text(model.provider, color = Muted) },
                                        modifier = Modifier.clickable {
                                            selected = model
                                            prefs.setModelId(model.id)
                                            showModels = false
                                        },
                                        colors = ListItemDefaults.colors(containerColor = Color.Transparent)
                                    )
                                }
                            }
                        }
                    }
                    Spacer(Modifier.height(8.dp))
                    Surface(
                        modifier = Modifier.weight(1f).fillMaxWidth(),
                        color = Color(0xFF11152A),
                        shape = RoundedCornerShape(18.dp)
                    ) {
                        LazyColumn(Modifier.fillMaxSize().padding(12.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                            item {
                                Surface(color = Color(0xFF191A35), shape = RoundedCornerShape(4.dp, 18.dp, 18.dp, 18.dp)) {
                                    Text(answer, Modifier.padding(14.dp).fillMaxWidth(), color = Color(0xFFF3EEFF), fontSize = 13.sp)
                                }
                            }
                        }
                    }
                    Spacer(Modifier.height(8.dp))
                    OutlinedTextField(
                        value = prompt, onValueChange = { prompt = it },
                        modifier = Modifier.fillMaxWidth(),
                        placeholder = { Text("Tulis perintah, pertanyaan, atau analisis…", color = Muted) },
                        maxLines = 3, shape = RoundedCornerShape(16.dp)
                    )
                    Spacer(Modifier.height(8.dp))
                    Button(
                        enabled = !busy && prompt.isNotBlank(),
                        onClick = {
                            val runtime = RuntimeGuard.inspect(context)
                            val integrity = ApkIntegrity.inspect(context)
                            if (!BuildConfig.DEBUG && !integrity.valid) {
                                answer = "Pemeriksaan integritas APK gagal."
                                ThreatReporter.report("APK_INTEGRITY_BLOCK", integrity.reasons)
                            } else if (!sessionGuard.isActive()) {
                                answer = "Sesi keamanan tidak valid. Silakan login ulang."
                                sessionGuard.clear(); prefs.clearSession(); token = ""
                                ThreatReporter.report("SESSION_REJECTED", listOf("session_inactive"))
                            } else if (!BuildConfig.DEBUG && !runtime.clean) {
                                answer = "Operasi dihentikan karena runtime tidak lolos pemeriksaan."
                                ThreatReporter.report("RUNTIME_BLOCK", runtime.hardSignals)
                            } else {
                                val sent = prompt.trim()
                                prompt = ""
                                busy = true
                                scope.launch {
                                    val result = withContext(Dispatchers.IO) {
                                        gateway.chat(selected, sent, token, PanelAuth.deviceId(context))
                                    }
                                    answer = result.getOrElse { it.message ?: "Layanan AI belum tersedia." }
                                    busy = false
                                }
                            }
                        },
                        modifier = Modifier.fillMaxWidth().height(50.dp),
                        shape = RoundedCornerShape(15.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = Violet, contentColor = Color.White)
                    ) {
                        Text(if (busy) "PROCESSING…" else "SEND TO ALVSIA", fontWeight = FontWeight.ExtraBold, letterSpacing = 1.sp)
                    }
                }
            }
        }
    }
}

@Composable
private fun AnalysisCard(result: UniversalAnalysisResult, onClear: () -> Unit) {
    Surface(color = Color(0x161D2340), shape = RoundedCornerShape(16.dp), modifier = Modifier.fillMaxWidth()) {
        Column(Modifier.padding(12.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(result.typeLabel, color = Cyan, fontWeight = FontWeight.Bold, fontSize = 12.sp)
                Spacer(Modifier.weight(1f))
                TextButton(onClick = onClear) { Text("CLEAR", color = Muted, fontSize = 9.sp) }
            }
            Text(result.name, color = Color.White, fontWeight = FontWeight.Bold, fontSize = 13.sp)
            Text(
                formatBytes(result.sizeBytes) + "  •  " + result.extension + "  •  SHA-256 " + result.sha256.take(16) + "…",
                color = Muted, fontSize = 9.sp
            )
            Spacer(Modifier.height(6.dp))
            Text(result.summary, color = Color(0xFFD8D8E8), fontSize = 10.sp)
        }
    }
}

@Composable
private fun GlassMetric(label: String, value: String, modifier: Modifier = Modifier) {
    Surface(modifier, shape = RoundedCornerShape(16.dp), color = Color(0xCC101329)) {
        Column(Modifier.padding(horizontal = 11.dp, vertical = 10.dp)) {
            Text(label, color = Violet2, fontSize = 8.sp, fontWeight = FontWeight.Bold, letterSpacing = 1.sp)
            Text(value, color = Color.White, fontWeight = FontWeight.ExtraBold, fontSize = 13.sp)
        }
    }
}

@Composable
private fun BottomNav() {
    Surface(color = Color(0xEE080B17), tonalElevation = 8.dp, shadowElevation = 8.dp) {
        Row(
            Modifier.fillMaxWidth().padding(horizontal = 22.dp, vertical = 10.dp),
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            BottomItem("HOME", true)
            BottomItem("ENGINE", false)
            BottomItem("MEMORY", false)
            BottomItem("SETTINGS", false)
        }
    }
}

@Composable
private fun BottomItem(label: String, active: Boolean) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Box(Modifier.size(5.dp).clip(CircleShape).background(if (active) Violet else Color.Transparent))
        Spacer(Modifier.height(4.dp))
        Text(label, color = if (active) Violet2 else Color(0xFF69728B), fontSize = 8.sp, fontWeight = FontWeight.Bold, letterSpacing = 0.7.sp)
    }
}

@Composable
private fun LoginExperience(
    license: String,
    onLicense: (String) -> Unit,
    busy: Boolean,
    error: String?,
    onLogin: () -> Unit
) {
    Box(
        Modifier.fillMaxSize().background(Brush.radialGradient(listOf(Color(0xFF26114D), Deep, Ink), radius = 900f)),
        contentAlignment = Alignment.Center
    ) {
        Column(Modifier.fillMaxWidth().padding(24.dp), horizontalAlignment = Alignment.CenterHorizontally) {
            Image(painterResource(R.drawable.alvsia_ai_logo), null, modifier = Modifier.size(132.dp).clip(CircleShape))
            Spacer(Modifier.height(20.dp))
            Text("ALVSIA", color = Violet2, fontSize = 13.sp, fontWeight = FontWeight.Bold, letterSpacing = 5.sp)
            Text("UNCENSORED AI", color = Color.White, fontSize = 27.sp, fontWeight = FontWeight.Black)
            Text("PERSONAL AI OPERATING SYSTEM", color = Muted, fontSize = 9.sp, letterSpacing = 1.5.sp)
            Spacer(Modifier.height(26.dp))
            Surface(modifier = Modifier.fillMaxWidth(), color = Color(0xE90F1223), shape = RoundedCornerShape(25.dp)) {
                Column(Modifier.padding(22.dp)) {
                    Text("SECURE ACCESS", color = Cyan, fontWeight = FontWeight.Bold, fontSize = 10.sp, letterSpacing = 1.5.sp)
                    Text("ENTER YOUR ACCESS KEY", color = Color.White, fontSize = 18.sp, fontWeight = FontWeight.ExtraBold)
                    Spacer(Modifier.height(15.dp))
                    OutlinedTextField(
                        value = license, onValueChange = onLicense,
                        modifier = Modifier.fillMaxWidth(), singleLine = true,
                        label = { Text("License key") },
                        visualTransformation = PasswordVisualTransformation()
                    )
                    if (!error.isNullOrBlank()) {
                        Spacer(Modifier.height(9.dp))
                        Text(error, color = Color(0xFFFF8C9A), fontSize = 11.sp)
                    }
                    Spacer(Modifier.height(16.dp))
                    Button(
                        onClick = onLogin, enabled = !busy && license.isNotBlank(),
                        modifier = Modifier.fillMaxWidth().height(52.dp),
                        shape = RoundedCornerShape(15.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = Violet, contentColor = Color.White)
                    ) {
                        Text(if (busy) "AUTHENTICATING…" else "ENTER ALVSIA", fontWeight = FontWeight.ExtraBold, letterSpacing = 1.2.sp)
                    }
                }
            }
        }
    }
}

private fun formatBytes(bytes: Long): String {
    if (bytes < 0) return "unknown size"
    if (bytes < 1024) return bytes.toString() + " B"
    val units = arrayOf("KB", "MB", "GB", "TB")
    var value = bytes.toDouble()
    var index = -1
    while (value >= 1024 && index < units.lastIndex) {
        value /= 1024.0
        index++
    }
    return "%.1f %s".format(value, units[index])
}
