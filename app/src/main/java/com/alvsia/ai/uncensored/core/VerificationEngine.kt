package com.alvsia.ai.uncensored.core

/** A result is only verified when explicit evidence supports each supplied claim. */
data class VerificationClaim(val id: String, val statement: String, val evidence: List<String>)
data class VerificationReport(val verified: Boolean, val claims: List<VerificationClaim>, val missingEvidence: List<String>)

class VerificationEngine {
    fun verify(claims: List<VerificationClaim>): VerificationReport {
        val missing = claims.filter { it.evidence.isEmpty() }.map { it.id }
        return VerificationReport(missing.isEmpty() && claims.isNotEmpty(), claims, missing)
    }
}
