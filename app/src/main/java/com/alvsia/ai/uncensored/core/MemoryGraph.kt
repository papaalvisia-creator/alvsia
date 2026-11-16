package com.alvsia.ai.uncensored.core

/** Lightweight project graph foundation: structured facts and relationships are kept separate from chat history. */
data class MemoryNode(val id: String, val type: String, val value: String)
data class MemoryEdge(val from: String, val relation: String, val to: String)

class ProjectMemoryGraph {
    private val nodes = linkedMapOf<String, MemoryNode>()
    private val edges = mutableListOf<MemoryEdge>()
    fun upsert(node: MemoryNode) { nodes[node.id] = node }
    fun relate(from: String, relation: String, to: String) { edges += MemoryEdge(from, relation, to) }
    fun node(id: String): MemoryNode? = nodes[id]
    fun edgesFrom(id: String): List<MemoryEdge> = edges.filter { it.from == id }
    fun snapshot(): Pair<List<MemoryNode>, List<MemoryEdge>> = nodes.values.toList() to edges.toList()
}
