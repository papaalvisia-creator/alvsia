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
    private var secondaryUri by mutableStateOf<Uri?>(null)
    private var pickingSecondary = false
    private val picker = registerForActivityResult(ActivityResultContracts.OpenDocument()) {
        if (pickingSecondary) secondaryUri = it else selectedUri = it
        pickingSecondary = false
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent { AlvsiaTheme { SmartToolScreen(selectedUri, { pickingSecondary = false; picker.launch(arrayOf("*/*")) }, { selectedUri = null; secondaryUri = null }, secondaryUri, { pickingSecondary = true; picker.launch(arrayOf("*/*")) }) } }
    }
}

@Composable
@OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)
private fun SmartToolScreen(uri: Uri?, onPick: () -> Unit, onClear: () -> Unit, secondaryUri: Uri?, onPickSecondary: () -> Unit) {
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
        report = withContext(Dispatchers.IO) { SmartToolEngine.analyze(context, u) }
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
                Text("9 ENGINES • 33 SMART TOOLS", color = STMuted, fontSize = 8.sp, letterSpacing = 1.2.sp)
            }},
            navigationIcon = { TextButton(onClick = { (context as? ComponentActivity)?.finish() }) { Text("BACK", color = STCyan, fontSize = 9.sp) } },
            colors = TopAppBarDefaults.topAppBarColors(containerColor = STInk)
        )
    }) { pad ->
        Column(Modifier.fillMaxSize().padding(pad).background(Brush.verticalGradient(listOf(Color(0xFF0B0D1C), STInk))).padding(14.dp)) {
            Row(horizontalArrangement = Arrangement.spacedBy(4.dp), modifier = Modifier.fillMaxWidth()) {
                listOf("HOME","LUA","PAK / OBB","ASSET / UE","APK / DEX","NATIVE","CRYPTO / RECOVERY","FORENSIC / STRING","BATCH / DEV LAB").forEach { tab ->
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
                    FeatureCard("ASSET ENGINE", "UAsset • UExp • UBULK • LOCRES • UMAP classification and batch audit")
                    FeatureCard("FORENSIC LAB", "Strings • entropy • hex preview • signatures • SHA-256 • evidence report")
                    FeatureCard("SMART CORE", "Automatic routing, diagnostics, safe output and explicit fallback states")
                    FeatureCard("AUDIT", "SHA-256 • operation report • zip-slip protection • explicit unsupported states")
                }
                "LUA" -> {
                    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        ToolActionCard("LUA SMART ANALYZE", "Deteksi source, bytecode, LuaJIT, header dan obfuscation.") {
                            if (uri == null) onPick() else scope.launch { busy = true; try { log = withContext(Dispatchers.IO) { SmartToolEngine.runOperation(context, uri, "lua").toString(2) } } catch (e: Exception) { log = "LUA ANALYZE ERROR • " + (e.message ?: "unknown") }; busy = false }
                        }
                        ToolActionCard("LUA RECOVERY / CONVERSION", "Normalisasi, BGMI/T24 conversion dan header recovery.") {
                            if (uri == null) onPick() else scope.launch { busy = true; try { log = withContext(Dispatchers.IO) { SmartToolEngine.runOperation(context, uri, "lua").toString(2) } } catch (e: Exception) { log = "RECOVERY ERROR • " + (e.message ?: "unknown") }; busy = false }
                        }
                        ToolActionCard("LUA MULTI-BACKEND DECOMPILE", "Smart decompile dengan routing backend yang tersedia.") {
                            if (uri == null) onPick() else scope.launch { busy = true; try { log = withContext(Dispatchers.IO) { SmartToolEngine.runOperation(context, uri, "lua").toString(2) } } catch (e: Exception) { log = "DECOMPILE ERROR • " + (e.message ?: "unknown") }; busy = false }
                        }
                        ToolActionCard("LUA PROTECT", "Protection pipeline dari sumber Lua; output non-destruktif.") {
                            if (uri == null) onPick() else scope.launch { busy = true; try { log = withContext(Dispatchers.IO) { SmartToolEngine.runOperation(context, uri, "lua_protect").toString(2) } } catch (e: Exception) { log = "LUA PROTECT • " + (e.message ?: "engine belum tersedia") }; busy = false }
                        }
                        ToolActionCard("LUA CUSTOM INJECT", "Pilih Lua lalu pilih target PAK. Backend menjalankan injeksi nyata dan menghasilkan PAK baru.") {
                            if (uri == null) onPick()
                            else if (secondaryUri == null) { onPickSecondary(); log = "Pilih TARGET PAK untuk Lua injection." }
                            else scope.launch {
                                busy = true
                                try {
                                    val out = File(context.cacheDir, "smart_lua_injected_" + System.currentTimeMillis() + ".pak")
                                    log = withContext(Dispatchers.IO) { SmartToolEngine.runLuaCustomInject(context, uri, secondaryUri, out).toString(2) }
                                } catch (e: Exception) { log = "LUA CUSTOM INJECT ERROR • " + (e.message ?: "unknown") }
                                busy = false
                            }
                        }
                        ToolActionCard("LUA T24 / BGMI CONVERT", "Konversi bytecode T24/BGMI ke bentuk standard Lua 5.3.") {
                            if (uri == null) onPick() else scope.launch {
                                busy = true
                                try { log = withContext(Dispatchers.IO) { SmartToolEngine.runOperation(context, uri, "lua_t24_convert").toString(2) } }
                                catch (e: Exception) { log = "LUA CONVERT ERROR • " + (e.message ?: "unknown") }
                                busy = false
                            }
                        }
                        ToolActionCard("LUA MULTI-XOR", "Uji kandidat XOR multi-byte yang tersedia tanpa mengubah input.") {
                            if (uri == null) onPick() else scope.launch {
                                busy = true
                                try { log = withContext(Dispatchers.IO) { SmartToolEngine.runOperation(context, uri, "lua_multi_xor").toString(2) } }
                                catch (e: Exception) { log = "LUA XOR ERROR • " + (e.message ?: "unknown") }
                                busy = false
                            }
                        }
                        lua?.let { LuaCard(it) }
                    }
                }
                "PAK / OBB", "PAK" -> {
                    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    ToolActionCard("PAK INFO", "Baca versi, index encryption, mount point, jumlah entry dan path.") {
                        if (uri == null) onPick() else scope.launch {
                            busy=true
                            try { log=withContext(Dispatchers.IO){SmartToolEngine.runOperation(context,uri,"pak_info").toString(2)} }
                            catch(e:Exception){log="PAK INFO ERROR • "+(e.message?:"unknown")}
                            busy=false
                        }
                    }
                    ToolActionCard("PAK ANALYZE / EXTRACT", "Ekstraksi PAK nyata melalui TencentPakFile; output non-destruktif.") {
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
                                    val count = withContext(Dispatchers.IO) { SmartToolEngine.extractZip(context, uri, out) }
                                    log = "EXTRACT OK • $count entries • ${out.name}"
                                } else log = r.detail
                            } catch (e: Exception) { log = "PAK ERROR • ${e.message ?: "unknown"}" }
                            busy = false
                        }
                    }
                    ToolActionCard("PAK LUA INJECT", "Masukkan Lua ke PAK target dengan backend injeksi Smart Tool.") {
                        if (uri == null) onPick()
                        else if (secondaryUri == null) { onPickSecondary(); log="Pilih TARGET PAK." }
                        else scope.launch {
                            busy=true
                            try {
                                val out=File(context.cacheDir,"smart_pak_lua_"+System.currentTimeMillis()+".pak")
                                log=withContext(Dispatchers.IO){SmartToolEngine.runLuaCustomInject(context,uri,secondaryUri,out).toString(2)}
                            } catch(e:Exception){log="PAK INJECT ERROR • "+(e.message?:"unknown")}
                            busy=false
                        }
                    }
                    }
                }
                "ASSET / UE", "ASSET" -> {
                    ToolActionCard("UE4 ASSET ANALYZER", "UAsset • UExp • UBULK • LOCRES • UMAP: klasifikasi, hash, entropy dan laporan.") {
                        if (uri == null) onPick() else scope.launch {
                            busy = true
                            try {
                                val r = withContext(Dispatchers.IO) { SmartToolEngine.analyze(context, uri) }
                                report = r
                                log = withContext(Dispatchers.IO) { SmartToolEngine.runOperation(context, uri, "file_report").toString(2) }
                            } catch (e: Exception) { log = "ASSET ERROR • ${e.message ?: "unknown"}" }
                            busy = false
                        }
                    }
                    Spacer(Modifier.height(10.dp))
                    Surface(color = Color(0xFF0B1020), shape = RoundedCornerShape(16.dp), modifier = Modifier.fillMaxWidth().weight(1f)) {
                        LazyColumn(Modifier.padding(12.dp)) { item { Text(log, color = Color(0xFFD8D8E8), fontSize = 10.sp) } }
                    }
                }
                "FORENSIC / STRING", "FORENSIC" -> {
                    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        listOf(
                            "FILE REPORT" to "file_report",
                            "STRINGS" to "strings",
                            "ENTROPY" to "entropy",
                            "HEX PREVIEW" to "hex"
                        ).forEach { (title, op) ->
                            ToolActionCard(title, "ALVSIA forensic engine • non-destructive • output JSON.") {
                                if (uri == null) onPick() else scope.launch {
                                    busy = true
                                    try {
                                        log = withContext(Dispatchers.IO) { SmartToolEngine.runOperation(context, uri, op).toString(2) }
                                    } catch (e: Exception) { log = "FORENSIC ERROR • ${e.message ?: "unknown"}" }
                                    busy = false
                                }
                            }
                        }
                    }
                    Spacer(Modifier.height(10.dp))
                    Surface(color = Color(0xFF0B1020), shape = RoundedCornerShape(16.dp), modifier = Modifier.fillMaxWidth().weight(1f)) {
                        LazyColumn(Modifier.padding(12.dp)) { item { Text(log, color = Color(0xFFD8D8E8), fontSize = 10.sp) } }
                    }
                }
                else -> {
                    val menu = when (section) {
                        "APK / DEX" -> listOf("APK ANALYSIS" to "apk_audit", "DEX / BYTECODE" to "file_report", "APK STRINGS / URL" to "url_scan", "PACKAGE / SIGNATURE AUDIT" to "apk_audit")
                        "NATIVE" -> listOf("ELF / SO ANALYZER" to "so_audit", "NATIVE STRINGS / SYMBOLS" to "strings", "DEPENDENCY / ABI AUDIT" to "file_report")
                        "CRYPTO / RECOVERY" -> listOf("AES CANDIDATE SCAN" to "aes_scan", "STRING RECOVERY" to "string_recover", "URL / ENDPOINT SCAN" to "url_scan", "COMPRESSION / LAYER RECOVERY" to "forensics")
                        else -> listOf("BATCH AUDIT / CLASSIFY" to "batch_audit", "COMPARE / REGRESSION" to "batch_audit", "SELF TEST / ENGINE HEALTH" to "self_test")
                    }
                    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        Text(section, color = STCyan, fontSize = 11.sp, fontWeight = FontWeight.ExtraBold, letterSpacing = 1.2.sp)
                        menu.forEach { item ->
                            ToolActionCard(item.first, "ALVSIA Smart Engine • non-destructive routing • explicit result.") {
                                if (uri == null) onPick() else scope.launch {
                                    busy = true
                                    try { log = withContext(Dispatchers.IO) { SmartToolEngine.runOperation(context, uri, item.second).toString(2) } }
                                    catch (e: Exception) { log = item.first + " ERROR • " + (e.message ?: "engine unavailable") }
                                    busy = false
                                }
                            }
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
