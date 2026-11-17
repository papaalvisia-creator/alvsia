package com.alvsia.ai.uncensored

import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import android.os.Bundle
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
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
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import com.alvsia.ai.uncensored.security.ApkIntegrity
import com.alvsia.ai.uncensored.security.RuntimeGuard
import com.alvsia.ai.uncensored.security.SessionGuard
import com.alvsia.ai.uncensored.security.ThreatReporter

private val Ink = Color(0xFF050B16)
private val Panel = Color(0xFF0D1B2B)
private val Blue = Color(0xFF53C8FF)
private val Cyan = Color(0xFF8DEBFF)
private val Muted = Color(0xFF9CB2C8)

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val integrity = ApkIntegrity.inspect(this)
        if (!integrity.valid) ThreatReporter.report("APK_INTEGRITY", integrity.reasons)
        val runtime = RuntimeGuard.inspect(this)
        if (!runtime.clean || runtime.softSignals.isNotEmpty()) ThreatReporter.report("RUNTIME_SCAN", runtime.hardSignals + runtime.softSignals)
        window.statusBarColor = android.graphics.Color.rgb(5, 11, 22)
        window.navigationBarColor = android.graphics.Color.rgb(3, 7, 14)
        setContent { AlvsiaTheme { AlvsiaApp() } }
    }
}

@Composable
private fun AlvsiaApp() {
    val context = androidx.compose.ui.platform.LocalContext.current
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
    var expiry by remember { mutableStateOf("") }
    var models by remember { mutableStateOf(ModelCatalog.starter) }
    var selected by remember { mutableStateOf(ModelCatalog.starter.first()) }
    var query by remember { mutableStateOf("") }
    var prompt by remember { mutableStateOf("") }
    var answer by remember { mutableStateOf("Sesi siap. Pilih model dan mulai percakapan.") }
    var busy by remember { mutableStateOf(false) }
    var showModels by remember { mutableStateOf(false) }

    LaunchedEffect(Unit) {
        val loaded = withContext(Dispatchers.IO) { catalog.load() }
        if (loaded.isNotEmpty()) { models = loaded; selected = loaded.first() }
    }

    if (token.isBlank()) {
        LoginExperience(
            license = license, onLicense = { license = it },
            busy = authBusy, error = authError,
            onLogin = {
                authBusy = true; authError = null
                scope.launch {
                    val result = withContext(Dispatchers.IO) {
                        runCatching { auth.login(license, PanelAuth.deviceId(context)) }
                    }
                    result.onSuccess {
                        prefs.setToken(it.token)
                        sessionGuard.activate(it.token)
                        token = it.token
                        expiry = it.expiry
                        answer = "Login panel berhasil. Sesi ALVSIA aktif."
                    }.onFailure { authError = it.message ?: "Login gagal." }
                    authBusy = false
                }
            }
        )
        return
    }

    Scaffold(containerColor = Ink) { pad ->
        Column(
            Modifier.fillMaxSize().padding(pad)
                .background(Brush.verticalGradient(listOf(Color(0xFF071729), Ink, Color(0xFF02050B))))
                .padding(horizontal = 16.dp, vertical = 12.dp)
        ) {
            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth()) {
                Image(painterResource(R.drawable.alvsia_ai_logo), null, modifier = Modifier.border(2.dp, Brush.sweepGradient(listOf(Color(0xFF55C7FF), Color(0xFFCAD7E5), Color(0xFF244A70), Color(0xFF55C7FF))), CircleShape).padding(4.dp).size(54.dp).shadow(14.dp, CircleShape))
                Spacer(Modifier.width(12.dp))
                Column(Modifier.weight(1f)) {
                    Text("ALVSIA", color = Blue, fontSize = 12.sp, fontWeight = FontWeight.Bold, letterSpacing = 3.sp)
                    Text("UNCENSORED AI", color = Color.White, fontSize = 21.sp, fontWeight = FontWeight.ExtraBold)
                    Text("PERSONAL AI OPERATING SYSTEM", color = Muted, fontSize = 9.sp, letterSpacing = 1.sp)
                }
                TextButton(onClick = { sessionGuard.clear(); prefs.clearSession(); token = ""; license = "" }) { Text("KELUAR", color = Cyan, fontSize = 10.sp) }
            }
            Spacer(Modifier.height(16.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                MetricCard("BRAIN", "READY")
                MetricCard("SESSION", "ACTIVE")
                MetricCard("MODELS", models.size.toString())
            }
            Spacer(Modifier.height(14.dp))
            ElevatedCard(
                modifier = Modifier.fillMaxWidth().shadow(12.dp, RoundedCornerShape(20.dp)),
                shape = RoundedCornerShape(20.dp),
                colors = CardDefaults.elevatedCardColors(containerColor = Color(0xFF101E30))
            ) {
                Column(Modifier.padding(16.dp)) {
                    Text("MODEL ROUTER", color = Blue, fontSize = 10.sp, fontWeight = FontWeight.Bold, letterSpacing = 1.4.sp)
                    Row(Modifier.fillMaxWidth().clickable { showModels = !showModels }.padding(top = 7.dp), verticalAlignment = Alignment.CenterVertically) {
                        Column(Modifier.weight(1f)) {
                            Text(selected.name, color = Color.White, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                            Text(selected.provider + "  •  " + selected.tags.joinToString(" • "), color = Muted, fontSize = 10.sp)
                        }
                        Text(if (showModels) "⌃" else "⌄", color = Cyan, fontSize = 24.sp)
                    }
                    if (showModels) {
                        OutlinedTextField(query, { query = it }, modifier = Modifier.fillMaxWidth().padding(top = 10.dp), placeholder = { Text("Cari model") }, singleLine = true)
                        LazyColumn(Modifier.heightIn(max = 210.dp)) {
                            items(models.filter { query.isBlank() || it.name.contains(query, true) || it.tags.any { t -> t.contains(query, true) } }) { model ->
                                ListItem(
                                    headlineContent = { Text(model.name, color = Color.White) },
                                    supportingContent = { Text(model.provider, color = Muted) },
                                    modifier = Modifier.clickable { selected = model; prefs.setModelId(model.id); showModels = false },
                                    colors = ListItemDefaults.colors(containerColor = Color.Transparent)
                                )
                            }
                        }
                    }
                }
            }
            Spacer(Modifier.height(14.dp))
            Surface(
                modifier = Modifier.weight(1f).fillMaxWidth().shadow(18.dp, RoundedCornerShape(24.dp)),
                shape = RoundedCornerShape(24.dp),
                color = Color(0xFF0B2032)
            ) {
                Column(Modifier.padding(16.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text("AI WORKSPACE", color = Blue, fontSize = 10.sp, fontWeight = FontWeight.Bold, letterSpacing = 1.4.sp)
                        Spacer(Modifier.weight(1f))
                        Text("● ONLINE SESSION", color = Color(0xFF64E6B2), fontSize = 9.sp)
                    }
                    Spacer(Modifier.height(12.dp))
                    LazyColumn(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                        item {
                            Surface(color = Color(0xFF142D42), shape = RoundedCornerShape(topStart = 4.dp, topEnd = 18.dp, bottomEnd = 18.dp, bottomStart = 18.dp)) {
                                Text(answer, Modifier.padding(14.dp).fillMaxWidth(), color = Color(0xFFEAF6FF), fontSize = 14.sp)
                            }
                        }
                    }
                    OutlinedTextField(
                        value = prompt, onValueChange = { prompt = it },
                        modifier = Modifier.fillMaxWidth(),
                        placeholder = { Text("Tulis perintah atau pertanyaan…", color = Muted) },
                        maxLines = 4, shape = RoundedCornerShape(16.dp),
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedBorderColor = Blue, unfocusedBorderColor = Color(0xFF31546C),
                            focusedTextColor = Color.White, unfocusedTextColor = Color.White,
                            cursorColor = Cyan
                        )
                    )
                    Spacer(Modifier.height(9.dp))
                    Button(
                        enabled = !busy && prompt.isNotBlank(),
                        onClick = {
                            val runtime = RuntimeGuard.inspect(context)
                            val integrity = ApkIntegrity.inspect(context)
                            if (!BuildConfig.DEBUG && !integrity.valid) {
                                answer = "Pemeriksaan integritas APK gagal: ${integrity.reasons.joinToString()}"
                                ThreatReporter.report("APK_INTEGRITY_BLOCK", integrity.reasons)
                            } else if (!sessionGuard.isActive()) {
                                answer = "Sesi keamanan tidak valid atau kedaluwarsa. Silakan login ulang."
                                sessionGuard.clear(); prefs.clearSession(); token = ""
                                ThreatReporter.report("SESSION_REJECTED", listOf("session_inactive"))
                            } else if (!runtime.clean) {
                                answer = "Operasi dihentikan karena terdeteksi indikasi instrumentation aktif: ${runtime.hardSignals.joinToString()}"
                                ThreatReporter.report("RUNTIME_BLOCK", runtime.hardSignals)
                            } else {
                                val sent = prompt.trim(); prompt = ""; busy = true
                                scope.launch {
                                    val result = withContext(Dispatchers.IO) { gateway.chat(selected, sent, token) }
                                    answer = result.getOrElse { it.message ?: "Layanan AI belum tersedia." }
                                    busy = false
                                }
                            }
                        },
                        modifier = Modifier.fillMaxWidth().height(50.dp).shadow(8.dp, RoundedCornerShape(15.dp)),
                        shape = RoundedCornerShape(15.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = Blue, contentColor = Ink)
                    ) { Text(if (busy) "MENJALANKAN MISI…" else "KIRIM PERINTAH", fontWeight = FontWeight.ExtraBold, letterSpacing = 1.sp) }
                }
            }
            Spacer(Modifier.height(12.dp))
            Surface(color = Color(0xFF0B1A2A), shape = RoundedCornerShape(18.dp), modifier = Modifier.fillMaxWidth()) {
                Row(Modifier.padding(14.dp), verticalAlignment = Alignment.CenterVertically) {
                    Column(Modifier.weight(1f)) {
                        Text("ACCOUNT PROFILE", color = Blue, fontSize = 9.sp, fontWeight = FontWeight.Bold, letterSpacing = 1.2.sp)
                        Text("ALVSIA AI • v${BuildConfig.VERSION_NAME}", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                        Text(if (expiry.isBlank()) "Panel session authenticated" else "License active • $expiry", color = Muted, fontSize = 10.sp)
                    }
                    Text("SECURE", color = Color(0xFF64E6B2), fontSize = 10.sp, fontWeight = FontWeight.Bold)
                }
            }
        }
    }
}

@Composable
private fun MetricCard(label: String, value: String) {
    Surface(
        modifier = Modifier.weightFix(),
        shape = RoundedCornerShape(16.dp),
        color = Color(0xFF10243A)
    ) {
        Column(Modifier.padding(horizontal = 12.dp, vertical = 13.dp)) {
            Text(label, color = Blue, fontSize = 9.sp, fontWeight = FontWeight.Bold)
            Text(value, color = Color.White, fontWeight = FontWeight.ExtraBold, fontSize = 14.sp)
        }
    }
}

private fun Modifier.weightFix(): Modifier = this.fillMaxWidth(0.333f)

@Composable
private fun LoginExperience(
    license: String, onLicense: (String) -> Unit, busy: Boolean, error: String?, onLogin: () -> Unit
) {
    Box(
        Modifier.fillMaxSize().background(Brush.verticalGradient(listOf(Color(0xFF071A2D), Ink, Color(0xFF02050B)))),
        contentAlignment = Alignment.Center
    ) {
        Column(Modifier.fillMaxWidth().padding(24.dp), horizontalAlignment = Alignment.CenterHorizontally) {
            Image(painterResource(R.drawable.alvsia_ai_logo), null, modifier = Modifier.border(2.dp, Brush.sweepGradient(listOf(Color(0xFF55C7FF), Color(0xFFCAD7E5), Color(0xFF244A70), Color(0xFF55C7FF))), CircleShape).padding(6.dp).size(150.dp).shadow(28.dp, CircleShape))
            Spacer(Modifier.height(22.dp))
            Text("ALVSIA", color = Blue, fontSize = 13.sp, fontWeight = FontWeight.Bold, letterSpacing = 5.sp)
            Text("UNCENSORED AI", color = Color.White, fontSize = 27.sp, fontWeight = FontWeight.Black)
            Text("PERSONAL AI OPERATING SYSTEM", color = Muted, fontSize = 10.sp, letterSpacing = 1.4.sp)
            Spacer(Modifier.height(28.dp))
            Surface(
                modifier = Modifier.fillMaxWidth().shadow(24.dp, RoundedCornerShape(26.dp)),
                color = Color(0xE9102236), shape = RoundedCornerShape(26.dp)
            ) {
                Column(Modifier.padding(22.dp)) {
                    Text("SECURE ACCESS", color = Cyan, fontWeight = FontWeight.Bold, fontSize = 11.sp, letterSpacing = 1.5.sp)
                    Text("ENTER THE KEY YOU NOOBS", color = Color.White, fontSize = 18.sp, fontWeight = FontWeight.ExtraBold, letterSpacing = 0.7.sp)
                    Spacer(Modifier.height(16.dp))
                    OutlinedTextField(
                        value = license, onValueChange = onLicense,
                        modifier = Modifier.fillMaxWidth(), singleLine = true,
                        label = { Text("License key") },
                        visualTransformation = PasswordVisualTransformation(),
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedBorderColor = Blue, unfocusedBorderColor = Color(0xFF36536B),
                            focusedTextColor = Color.White, unfocusedTextColor = Color.White,
                            cursorColor = Cyan
                        )
                    )
                    if (!error.isNullOrBlank()) {
                        Spacer(Modifier.height(10.dp))
                        Text(error, color = Color(0xFFFF8C9A), fontSize = 12.sp)
                    }
                    Spacer(Modifier.height(18.dp))
                    Button(
                        onClick = onLogin, enabled = !busy && license.isNotBlank(),
                        modifier = Modifier.fillMaxWidth().height(52.dp),
                        shape = RoundedCornerShape(15.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = Blue, contentColor = Ink)
                    ) { Text(if (busy) "AUTHENTICATING…" else "LOGIN", fontWeight = FontWeight.ExtraBold, letterSpacing = 1.5.sp) }
                }
            }
        }
    }
}
