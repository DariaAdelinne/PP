package org.example

import org.jsoup.Jsoup

fun procesareJsoup(url: String): MutableMap<String, MutableMap<String, String>> //primeste string si returneaza MutableMap
{
    val documentHtml = Jsoup.connect(url).get() //se conecteaza la link
    val lista = mutableMapOf<String, MutableMap<String, String>>() //creeaza afisarea

    val iteme = documentHtml.select("item") //selecteaza fiecare item din url
    for (item in iteme) {
        val titlu = item.select("title").text() //selecteaza titlul

        val deAdaugat = mutableMapOf( //creaza mutablemap cu informatiile necesare
            "Link" to item.select("link").text(),
            "Descriere" to item.select("description").text(),
            "Data Publicatiei" to item.select("pubDate").text()
        )
        lista[titlu] = deAdaugat
    }
    return lista
}

fun main() {
    val url = "http://rss.cnn.com/rss/edition.rss" //url
    val lista = procesareJsoup(url) //lista cu prelucrarea url ului
    lista.forEach { //parcurge fiecare element din lista si afiseaza informatiile
        println("${it.key}: ") 
        println("Link: ${it.value["Link"]}")
        println("Descriere: ${it.value["Descriere"]}")
        println("Data Publicatiei: ${it.value["Data Publicatiei"]}")
        println() 
    }
}
