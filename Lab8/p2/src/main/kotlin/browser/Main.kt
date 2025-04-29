// src/main/kotlin/com/example/browser/Main.kt
package com.example.browser

fun main() {
    // 1) setăm prototipul de pornire
    val defaultSite = LiveSite("https://www.example.com")
    var duplicator = SiteDuplicator(defaultSite)
    val browser = KidsBrowserFacade(duplicator)

    println("*** Acces site permis ***")
    browser.navigateTo("https://www.kidsgames.com")

    println("\n*** Acces site POTENTIAL periculos ***")
    browser.navigateTo("https://www.gamblingfun.com")

    println("\n*** Acces site educational ***")
    browser.navigateTo("https://open.university.edu")
}
