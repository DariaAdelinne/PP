import java.io.File
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

//clasa care retine o comanda si momentul executiei
data class HistoryLogRecord(val timestamp: Long, val command: String) : Comparable<HistoryLogRecord> {
    override fun compareTo(other: HistoryLogRecord): Int = this.timestamp.compareTo(other.timestamp) //suprascriem metoda pentru a compara obiectele dupa timestamp
}

//transforma o data calendaristica in timestamp
fun parseDateToTimestamp(dateStr: String): Long {
    val formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss") //formatul exact al datei
    val dateTime = LocalDateTime.parse(dateStr, formatter) //transformam textul intr un obiect data
    return dateTime.toEpochSecond(java.time.ZoneOffset.UTC) //transforma in timestamp numeric ca sa il putem folosi in comparatii
}

//parcurge fisierul si extrage ultimele 'n' inregistrari
fun extrageUltimeleComenzi(cale: String, numar: Int = 50): List<HistoryLogRecord> {
    val linii = File(cale).readLines().asReversed() //citim fisierul de la sfarsit spre inceput
    val rezultate = mutableListOf<HistoryLogRecord>() //unde salvam rezultatele

    var dataStart: Long? = null
    var linieComanda: String? = null

    for (linie in linii) {
        when { //daca linia incepe cu "Start-Date" sau "CommandLine" eliminam prefixele/spatiile si convertim in long
            linie.startsWith("Start-Date:") -> {
                val dataText = linie.removePrefix("Start-Date:").trim()
                dataStart = parseDateToTimestamp(dataText)
            }
            linie.startsWith("Commandline:") -> {
                linieComanda = linie.removePrefix("Commandline:").trim()
            }
        }

        if (dataStart != null && linieComanda != null) { //daca le avem pe amandoua le adaugam in rez
            rezultate.add(HistoryLogRecord(dataStart, linieComanda))
            if (rezultate.size >= numar) break //daca am adunat deja un nr de comenzi ne oprim
            dataStart = null
            linieComanda = null
        }
    }
    return rezultate
}

//gaseste valoarea maxima dintre doua obiecte comparabile
fun <T : Comparable<T>> gasesteMaxim(a: T, b: T): T {
    return if (a >= b) a else b
}

//inlocuieste un element intr-un map daca exista
fun <T> inlocuiesteElement(map: MutableMap<Long, out T>, vechi: T, nou: T) where T : HistoryLogRecord {
    if (map.containsKey(vechi.timestamp)) {
        (map as MutableMap<Long, T>)[vechi.timestamp] = nou
    }
}

fun main() {
    val caleFisier = "src/history.log"
    val istoric = extrageUltimeleComenzi(caleFisier)

    val mapaComenzi = mutableMapOf<Long, HistoryLogRecord>()
    for (intrare in istoric) {
        mapaComenzi[intrare.timestamp] = intrare
    }

    println("Cele mai recente 50 de comenzi executate:")
    mapaComenzi.values.sortedByDescending { it.timestamp }
        .forEach { println("${it.timestamp}: ${it.command}") }

    if (istoric.size >= 2) {
        val prima = istoric[0]
        val aDoua = istoric[1]
        val maiRecenta = gasesteMaxim(prima, aDoua)
        println("\nComanda mai recenta este:")
        println("${maiRecenta.timestamp}: ${maiRecenta.command}")

        //simulam o modificare a comenzii
        val modificata = HistoryLogRecord(maiRecenta.timestamp, "${maiRecenta.command}")
        inlocuiesteElement(mapaComenzi, maiRecenta, modificata)

        println("\nDupa inlocuire in mapa:")
        mapaComenzi[modificata.timestamp]?.let {
            println("${it.timestamp}: ${it.command}")
        }
    }
}
