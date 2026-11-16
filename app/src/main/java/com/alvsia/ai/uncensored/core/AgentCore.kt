package com.alvsia.ai.uncensored.core

/** Core contracts for ALVSIA's autonomous multi-agent runtime. */
enum class AgentRole { MANAGER, RESEARCH, ARCHITECTURE, CODING, SECURITY, BUILD, TEST, AUDIT, RELEASE, REPORT }
enum class RiskLevel { LOW, MEDIUM, HIGH, CRITICAL }
enum class Permission { READ, WRITE, EXECUTE, NETWORK, SECRET_REFERENCE, DEPLOY, DELETE, ADMIN }

data class AgentTask(
    val id: String,
    val role: AgentRole,
    val objective: String,
    val permissions: Set<Permission> = setOf(Permission.READ),
    val risk: RiskLevel = RiskLevel.LOW,
    val dependsOn: Set<String> = emptySet()
)

data class AgentResult(
    val taskId: String,
    val success: Boolean,
    val evidence: List<String> = emptyList(),
    val artifacts: List<String> = emptyList(),
    val error: String? = null
)

class PermissionBroker(private val approvals: MutableMap<String, Set<Permission>> = mutableMapOf()) {
    fun grant(scope: String, permissions: Set<Permission>) { approvals[scope] = permissions }
    fun allowed(scope: String, permission: Permission): Boolean = approvals[scope]?.contains(permission) == true
    fun require(scope: String, permission: Permission) {
        check(allowed(scope, permission)) { "Permission denied: $scope -> $permission" }
    }
}

class MissionPlanner {
    fun plan(objective: String): List<AgentTask> {
        val base = objective.trim().ifEmpty { error("Mission objective is empty") }
        return listOf(
            AgentTask("research", AgentRole.RESEARCH, "Research and collect authoritative context for: $base"),
            AgentTask("architecture", AgentRole.ARCHITECTURE, "Map architecture, dependencies, constraints and risks for: $base", dependsOn=setOf("research")),
            AgentTask("implementation", AgentRole.CODING, "Implement the requested change for: $base", setOf(Permission.READ, Permission.WRITE), RiskLevel.MEDIUM, setOf("architecture")),
            AgentTask("build", AgentRole.BUILD, "Build the affected project and capture reproducible artifacts", setOf(Permission.READ, Permission.EXECUTE), RiskLevel.MEDIUM, setOf("implementation")),
            AgentTask("test", AgentRole.TEST, "Run functional/regression tests and record evidence", setOf(Permission.READ, Permission.EXECUTE), RiskLevel.MEDIUM, setOf("build")),
            AgentTask("security", AgentRole.SECURITY, "Audit the resulting change for security and secret exposure", setOf(Permission.READ), RiskLevel.HIGH, setOf("implementation", "build")),
            AgentTask("verify", AgentRole.AUDIT, "Verify claims against build, test and security evidence", setOf(Permission.READ), RiskLevel.HIGH, setOf("test", "security")),
            AgentTask("report", AgentRole.REPORT, "Produce the final evidence-backed mission report", dependsOn=setOf("verify"))
        )
    }
}
