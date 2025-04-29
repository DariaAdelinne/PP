// src/main/kotlin/com/example/browser/KidsBrowserFacade.kt
package com.example.browser

/**
 * Facade care ascunde logica prototip-factory-proxy
 */
class KidsBrowserFacade(
    private var duplicator: SiteDuplicator
) {

    /**
     * Încarcă prototipul de site de plecare
     */
    fun registerPrototype(site: LiveSite) {
        // refacem duplicatorul cu noul prototip
        duplicator = SiteDuplicator(site)
    }

    /**
     * Încearcă să deschidă un site nou, clonând prototipul și apoi proxy-ing-l
     */
    fun navigateTo(url: String) {
        val copy = duplicator.makeCopy()
        // suprascriem adresa originală cu cea cerută
        val custom = LiveSite(url)
        val safe = ProtectedSite(custom)
        safe.open()
    }
}
