// src/main/kotlin/com/example/browser/LiveSite.kt
package com.example.browser

/**
 * Reprezintă un site web real, cu un URL fix.
 * Implementăm şi clonarea prototip.
 */
class LiveSite(
    private val address: String
) : ISite {

    override fun open() {
        println("Deschidem site-ul: $address")
    }

    fun getAddress(): String = address

    fun duplicate(): LiveSite = LiveSite(address)
}
