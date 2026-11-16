package com.alvsia.ai.uncensored.core

/** Provider-neutral connector/tool registry. External connectors can implement this contract without coupling the UI to a vendor. */
data class ToolDescriptor(
    val id: String,
    val name: String,
    val capabilities: Set<String>,
    val requiredPermissions: Set<Permission>
)

interface AlvsiaTool {
    val descriptor: ToolDescriptor
    fun execute(input: Map<String, String>): ToolExecution
}

data class ToolExecution(
    val success: Boolean,
    val output: String = "",
    val evidence: List<String> = emptyList(),
    val artifacts: List<String> = emptyList(),
    val error: String? = null
)

class ToolFabric {
    private val tools = linkedMapOf<String, AlvsiaTool>()
    fun register(tool: AlvsiaTool) { tools[tool.descriptor.id] = tool }
    fun get(id: String): AlvsiaTool? = tools[id]
    fun list(): List<ToolDescriptor> = tools.values.map { it.descriptor }
}
