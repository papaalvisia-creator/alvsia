package com.alvsia.ai.uncensored

import android.net.Uri
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.ui.platform.LocalContext
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.io.File

private val STInk = Color(0xFF03050B)
private val STPanel = Color(0xFF0E1224)
private val STViolet = Color(0xFF9D6CFF)
private val STCyan = Color(0xFF66E7FF)
private val STMuted = Color(0xFF9AA7C1)

class SmartToolActivity : ComponentActivity() {
    private var selectedUri by mutableStateOf<Uri?>(null)
    private val picker = registerForActivityResult(ActivityResultContracts.OpenDocument()) { selectedUri = it }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent { AlvsiaTheme { SmartToolScreen(selectedUri, { picker.launch(arrayOf("*/*")) }, { selectedUri = null }) } }
    }
}

@Composable
@OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)
private fun SmartToolScreen(uri: Uri?, onPick: () -> Unit, onClear: () -> Unit) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    var report by remember { mutableStateOf<SmartFileReport?>(null) }
    var lua by remember { mutableStateOf<LuaReport?>(null) }
    var busy by remember { mutableStateOf(false) }
    var log by remember { mutableStateOf("SMART ALVSIA TOOL siap. Semua operasi non-destruktif.") }
    var section by remember { mutableStateOf("HOME") }

    LaunchedEffect(uri) {
        val u = uri ?: return@LaunchedEffect
        busy = true
        report = withContext(Dispatchers.IO) { SmartToolEngine.analyze(context.contentResolver, u) }
        lua = null
        busy = false
        report?.let {
            log = "DETECT OK • ${it.type} • SHA-256 ${it.sha256.take(16)}…"
            if (it.type == "LUA") {
                val head = withContext(Dispatchers.IO) {
                    context.contentResolver.openInputStream(u)?.use { input ->
                        val b = ByteArray(65536)
                        val n = input.read(b)
                        if (n > 0) b.copyOf(n) else ByteArray(0)
                    } ?: ByteArray(0)
                }
                lua = SmartToolEngine.inspectLua(head)
            }
        }
    }

    Scaffold(containerColor = STInk, topBar = {
        TopAppBar(
            title = { Column {
                Text("SMART ALVSIA TOOL", color = Color.White, fontWeight = FontWeight.ExtraBold, fontSize = 17.sp)
                Text("PAK • LUA • BATCH • ANALYSIS", color = STMuted, fontSize = 8.sp, letterSpacing = 1.2.sp)
            }},
            navigationIcon = { TextButton(onClick = { (context as? ComponentActivity)?.finish() }) { Text("BACK", color = STCyan, fontSize = 9.sp) } },
            colors = TopAppBarDefaults.topAppBarColors(containerColor = STInk)
        )
    }) { pad ->
        Column(Modifier.fillMaxSize().padding(pad).background(Brush.verticalGradient(listOf(Color(0xFF0B0D1C), STInk))).padding(14.dp)) {
            Row(horizontalArrangement = Arrangement.spacedBy(4.dp), modifier = Modifier.fillMaxWidth()) {
                listOf("HOME","LUA","PAK","BATCH").forEach { tab ->
                    TextButton(onClick = { section = tab }) {
                        Text(tab, color = if (section == tab) STCyan else STMuted, fontWeight = FontWeight.Bold, fontSize = 9.sp)
                    }
                }
            }
            Spacer(Modifier.height(8.dp))
            when (section) {
                "HOME" -> {
                    ElevatedCard(colors = CardDefaults.elevatedCardColors(containerColor = STPanel), shape = RoundedCornerShape(22.dp)) {
                        Column(Modifier.padding(16.dp)) {
                            Text("UNIVERSAL TOOLCHAIN", color = STViolet, fontWeight = FontWeight.Bold, fontSize = 11.sp, letterSpacing = 1.4.sp)
                            Text("Satu workspace untuk file apa pun", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.ExtraBold)
                            Spacer(Modifier.height(8.dp))
                            Text("Berbasis temuan dua paket referensi: PAK/LUA pipeline, audit hash, batch/report dan proteksi non-destruktif.", color = STMuted, fontSize = 11.sp)
                            Spacer(Modifier.height(12.dp))
                            Button(onClick = onPick, modifier = Modifier.fillMaxWidth(), colors = ButtonDefaults.buttonColors(containerColor = STViolet)) { Text("OPEN ANY FILE", fontWeight = FontWeight.ExtraBold) }
                        }
                    }
                    FeatureCard("PAK ENGINE", "UE4 PAK detection • ZIP-compatible extraction • non-destructive output")
                    FeatureCard("LUA SMART PIPELINE", "Source • Lua bytecode • gzip/zlib candidates • XOR probe • diagnostics")
                    FeatureCard("BATCH ENGINE", "Audit/hash/report architecture untuk batch processing")
                    FeatureCard("AUDIT", "SHA-256 • operation report • zip-slip protection • explicit unsupported states")
                }
                "LUA" -> {
                    ToolActionCard("LUA SMART DECOMPILE", "Deteksi header, versi, source/bytecode dan kandidat obfuscation.") {
                        if (uri == null) onPick() else scope.launch {
                            busy = true
                            val result = withContext(Dispatchers.IO) {
                                SmartToolEngine.runOperation(context, uri, "lua")
                            }
                            log = result.toString(2)
                            val bytes = withContext(Dispatchers.IO) {
                                context.contentResolver.openInputStream(uri)?.use { input ->
                                    val b = ByteArray(65536); val n = input.read(b)
                                    if (n > 0) b.copyOf(n) else ByteArray(0)
                                } ?: ByteArray(0)
                            }
                            lua = SmartToolEngine.inspectLua(bytes)
                            busy = false
                        }
                    }
                    lua?.let { LuaCard(it) }
                }
                "PAK" -> {
                    ToolActionCard("PAK ANALYZE / EXTRACT", "UE4 PAK dikenali; ZIP-compatible fixture dapat diekstrak aman.") {
                        if (uri == null) onPick() else scope.launch {
                            busy = true
                            try {
                                val r = withContext(Dispatchers.IO) { SmartToolEngine.analyze(context, uri) }
                                report = r
                                if (r.type == "UE4_PAK") {
                                    val out = File(context.cacheDir, "smart_pak_extract_${System.currentTimeMillis()}")
                                    val result = withContext(Dispatchers.IO) { SmartToolEngine.runOperation(context, uri, "pak_extract", out) }
                                    log = result.toString(2)
                                } else if (r.type == "ZIP_CONTAINER") {
                                    val out = File(context.cacheDir, "smart_extract_${System.currentTimeMillis()}")
                                    val count = withContext(Dispatchers.IO) { SmartToolEngine.extractZip(context.contentResolver, uri, out) }
                                    log = "EXTRACT OK • $count entries • ${out.name}"
                                } else log = r.detail
                            } catch (e: Exception) { log = "PAK ERROR • ${e.message ?: "unknown"}" }
                            busy = false
                        }
                    }
                }
                else -> {
                    ToolActionCard("BATCH / AUDIT", "Analisis file, hash, klasifikasi dan laporan.") {
                        if (uri == null) onPick() else scope.launch {
                            busy = true
                            report = withContext(Dispatchers.IO) { SmartToolEngine.analyze(context, uri) }
                            log = report?.let { SmartToolEngine.batchClassify(context, uri) } ?: "Tidak ada laporan"
                            busy = false
                        }
                    }
                    Spacer(Modifier.height(10.dp))
                    Surface(color = Color(0xFF0B1020), shape = RoundedCornerShape(16.dp), modifier = Modifier.fillMaxWidth().weight(1f)) {
                        LazyColumn(Modifier.padding(12.dp)) { item { Text(log, color = Color(0xFFD8D8E8), fontSize = 10.sp) } }
                    }
                }
            }
            if (busy) { Spacer(Modifier.height(8.dp)); LinearProgressIndicator(Modifier.fillMaxWidth(), color = STCyan, trackColor = Color(0x223A4260)) }
            report?.let { SmartReportCard(it, onClear) }
        }
    }
}

@Composable private fun FeatureCard(title: String, body: String) {
    Surface(color = Color(0xB5101426), shape = RoundedCornerShape(16.dp), modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp)) {
        Column(Modifier.padding(13.dp)) { Text(title, color = STViolet, fontSize = 10.sp, fontWeight = FontWeight.Bold); Text(body, color = Color.White, fontSize = 11.sp) }
    }
}

@Composable private fun ToolActionCard(title: String, body: String, action: () -> Unit) {
    ElevatedCard(colors = CardDefaults.elevatedCardColors(containerColor = STPanel), shape = RoundedCornerShape(20.dp), modifier = Modifier.fillMaxWidth()) {
        Column(Modifier.padding(15.dp)) { Text(title, color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.ExtraBold); Text(body, color = STMuted, fontSize = 10.sp); Spacer(Modifier.height(10.dp)); Button(onClick = action, colors = ButtonDefaults.buttonColors(containerColor = STViolet)) { Text("RUN", fontWeight = FontWeight.ExtraBold) } }
    }
}

@Composable private fun LuaCard(r: LuaReport) {
    Surface(color = Color(0xFF11152A), shape = RoundedCornerShape(16.dp), modifier = Modifier.fillMaxWidth().padding(top = 10.dp)) {
        Column(Modifier.padding(13.dp)) {
            Text("LUA DIAGNOSTIC", color = STCyan, fontWeight = FontWeight.Bold)
            Text("${r.kind} • ${r.version}", color = Color.White, fontWeight = FontWeight.Bold)
            Text(r.header, color = STMuted, fontSize = 9.sp)
            Text(r.detail, color = Color(0xFFD8D8E8), fontSize = 10.sp)
            if (r.xorCandidates.isNotEmpty()) Text("Candidates: ${r.xorCandidates.joinToString()}", color = STViolet, fontSize = 9.sp)
        }
    }
}

@Composable private fun SmartReportCard(r: SmartFileReport, clear: () -> Unit) {
    Surface(color = Color(0x161D2340), shape = RoundedCornerShape(16.dp), modifier = Modifier.fillMaxWidth().padding(top = 10.dp)) {
        Column(Modifier.padding(12.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(r.type, color = STCyan, fontWeight = FontWeight.Bold)
                Spacer(Modifier.weight(1f))
                TextButton(onClick = clear) { Text("CLEAR", color = STMuted, fontSize = 9.sp) }
            }
            Text(r.name, color = Color.White, fontWeight = FontWeight.Bold)
            Text("${r.size} bytes • SHA-256 ${r.sha256.take(16)}…", color = STMuted, fontSize = 9.sp)
            Text(r.detail, color = Color(0xFFD8D8E8), fontSize = 10.sp)
        }
    }
}
