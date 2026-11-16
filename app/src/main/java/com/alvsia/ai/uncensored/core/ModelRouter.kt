package com.alvsia.ai.uncensored.core

/** Policy-only model router. Provider adapters remain outside the Android UI and never carry master secrets. */
data class ModelCapability(val reasoning: Int, val coding: Int, val vision: Int, val speed: Int, val local: Boolean)
data class ModelRoute(val modelId: String, val reason: String)

class ModelRouter {
    fun choose(task: AgentTask, candidates: Map<String, ModelCapability>): ModelRoute {
        require(candidates.isNotEmpty()) { "No model candidates available" }
        val scored = candidates.map { (id, c) ->
            val roleScore = when (task.role) {
                AgentRole.CODING, AgentRole.BUILD, AgentRole.TEST => c.coding * 3 + c.reasoning * 2
                AgentRole.RESEARCH, AgentRole.MANAGER, AgentRole.SECURITY, AgentRole.AUDIT => c.reasoning * 3 + c.speed
                else -> c.reasoning * 2 + c.speed
            }
            id to roleScore
        }.maxBy { it.second }
        return ModelRoute(scored.first, "best capability score for ${task.role}")
    }
}
