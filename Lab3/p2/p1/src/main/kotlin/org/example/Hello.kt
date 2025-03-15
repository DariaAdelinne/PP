package org.example

import org.jsoup.Jsoup

fun procesareJsoup(url: String): MutableMap<String, MutableMap<String, String>> {
    val documentHtml = Jsoup.connect(url).get()
    val lista = mutableMapOf<String, MutableMap<String, String>>()

    val iteme = documentHtml.select("item")
    for (item in iteme) {
        val titlu = item.select("title").text()

        val deAdaugat = mutableMapOf(
            "Link" to item.select("link").text(),
            "Descriere" to item.select("description").text(),
            "Data Publicatiei" to item.select("pubDate").text()
        )
        lista[titlu] = deAdaugat
    }
    return lista
}

fun main() {
    val url = "http://rss.cnn.com/rss/edition.rss"
    val lista = procesareJsoup(url)
    lista.forEach {
        println("${it.key}: ")
        println("Link: ${it.value["Link"]}")
        println("Descriere: ${it.value["Descriere"]}")
        println("Data Publicatiei: ${it.value["Data Publicatiei"]}")
        println() // Add a blank line for better readability
    }
}