// src/main/kotlin/com/example/browser/SiteDuplicator.kt
package com.example.browser

/**
 * Factory care folosește prototipul pentru a produce copii
 */
class SiteDuplicator(
    private val prototype: LiveSite
) {
    fun makeCopy(): LiveSite = prototype.duplicate()
}
