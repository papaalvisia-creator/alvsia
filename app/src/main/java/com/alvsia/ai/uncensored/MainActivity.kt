package com.alvsia.ai.uncensored

import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import android.os.Bundle
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import androidx.compose.runtime.LaunchedEffect

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent { AlvsiaTheme { AlvsiaApp() } }
    }
}

@Composable
private fun AlvsiaApp() {
    var models by remember { mutableStateOf(ModelCatalog.starter) }
    var selected by remember { mutableStateOf(ModelCatalog.starter.first()) }
    var query by remember { mutableStateOf("") }
    var prompt by remember { mutableStateOf("") }
    var answer by remember { mutableStateOf("Pilih model lalu kirim pertanyaan.") }
    var busy by remember { mutableStateOf(false) }
    var showModels by remember { mutableStateOf(false) }
    val scope = rememberCoroutineScope()
    val context = androidx.compose.ui.platform.LocalContext.current
    val prefs = remember { SecurePrefs(context) }
    val gateway = remember { AiGateway(BuildConfig.PANEL_BASE_URL) }
    val catalog = remember { ModelCatalogRepository(BuildConfig.PANEL_BASE_URL) }
    LaunchedEffect(Unit) {
        val loaded = withContext(Dispatchers.IO) { catalog.load() }
        if (loaded.isNotEmpty()) { models = loaded; selected = loaded.first() }
    }

    Scaffold(containerColor = MaterialTheme.colorScheme.background) { pad ->
        Column(
            Modifier.fillMaxSize()
                .padding(pad)
                .background(Brush.verticalGradient(listOf(Color(0xFF06111F), Color(0xFF02060B))))
                .padding(16.dp)
        ) {
            Text("ALVSIA UNCENSORED AI", style = MaterialTheme.typography.headlineSmall, fontWeight = androidx.compose.ui.text.font.FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
            Text("PERSONAL AI OPERATING SYSTEM • ${models.size} models • @OriginalOnwerALV", color = MaterialTheme.colorScheme.onSurface.copy(alpha = .72f))
            Text("Telegram: t.me/ALVISIACHANEL", color = MaterialTheme.colorScheme.onSurface.copy(alpha = .55f))
            Spacer(Modifier.height(14.dp))

            ElevatedCard(shape = RoundedCornerShape(18.dp), modifier = Modifier.fillMaxWidth()) {
                Column(Modifier.padding(16.dp)) {
                    Text("MODEL", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.primary)
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        modifier = Modifier.fillMaxWidth().clickable { showModels = !showModels }
                    ) {
                        Column(Modifier.weight(1f)) {
                            Text(selected.name, style = MaterialTheme.typography.titleMedium)
                            Text(
                                "${selected.provider} • ${selected.tags.joinToString(" • ")}",
                                style = MaterialTheme.typography.bodySmall
                            )
                        }
                        Text(if (showModels) "▲" else "▼", color = MaterialTheme.colorScheme.primary)
                    }

                    if (showModels) {
                        OutlinedTextField(
                            value = query,
                            onValueChange = { query = it },
                            modifier = Modifier.fillMaxWidth().padding(top = 10.dp),
                            label = { Text("Cari model") }
                        )
                        LazyColumn(Modifier.heightIn(max = 280.dp).padding(top = 8.dp)) {
                            items(models.filter {
                                query.isBlank() ||
                                    it.name.contains(query, true) ||
                                    it.tags.any { tag -> tag.contains(query, true) }
                            }) { model ->
                                ListItem(
                                    headlineContent = { Text(model.name) },
                                    supportingContent = { Text(model.tags.joinToString(" • ")) },
                                    modifier = Modifier.clickable {
                                        selected = model
                                        prefs.setModelId(model.id)
                                        showModels = false
                                    }
                                )
                            }
                        }
                    }
                }
            }

            Spacer(Modifier.height(14.dp))
            Surface(
                Modifier.weight(1f).fillMaxWidth(),
                shape = RoundedCornerShape(18.dp),
                tonalElevation = 2.dp
            ) {
                Column(Modifier.padding(16.dp)) {
                    Text("SESSION", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.primary)
                    LazyColumn(Modifier.weight(1f)) {
                        item { Text(answer, style = MaterialTheme.typography.bodyLarge) }
                    }
                    OutlinedTextField(
                        value = prompt,
                        onValueChange = { prompt = it },
                        modifier = Modifier.fillMaxWidth(),
                        placeholder = { Text("Tulis pertanyaan atau tugas...") },
                        maxLines = 5
                    )
                    Spacer(Modifier.height(8.dp))
                    Button(
                        enabled = !busy && prompt.isNotBlank(),
                        onClick = {
                            val sent = prompt.trim()
                            prompt = ""
                            busy = true
                            scope.launch {
                                val result = withContext(Dispatchers.IO) {
                                    gateway.chat(selected, sent, prefs.token())
                                }
                                answer = result.getOrElse { "Gagal: ${it.message ?: "unknown error"}" }
                                busy = false
                            }
                        },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(if (busy) "MEMPROSES..." else "KIRIM • ${selected.name}")
                    }
                }
            }
            Spacer(Modifier.height(10.dp))
            Text(
                "ALVSIA • Blue/White Neon Metallic • Local/Remote model catalog",
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurface.copy(alpha = .45f)
            )
        }
    }
}
