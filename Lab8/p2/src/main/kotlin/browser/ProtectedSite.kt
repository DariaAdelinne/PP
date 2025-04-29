// src/main/kotlin/com/example/browser/ProtectedSite.kt
package com.example.browser

/**
 * Proxy care blochează accesul la URL-uri ce conțin termeni nepotriviți
 */
class ProtectedSite(
    private val underlying: LiveSite
) : ISite {

    private val forbiddenWords = setOf(
        "violence","porn","gambling","drugs","death","kill","weapon","blood",
        "crime","abuse","suicide","alcohol","tobacco","sex","rape","murder",
        "assault","horror","explicit","adult","darkweb","bet"
    )

    override fun open() {
        val url = underlying.getAddress()
        if (forbiddenWords.any { url.contains(it, ignoreCase = true) }) {
            println("Acces interzis: $url (filtrare parentală activă)")
        } else {
            underlying.open()
        }
    }
}
