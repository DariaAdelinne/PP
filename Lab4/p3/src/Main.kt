import java.io.File
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

class Notita(val autor: String, val continut: String) {
    private val dataOra: String = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"))

    fun salveazaInFisier() {
        val numeFisier = "notite/${autor}_${dataOra.replace(":", "-").replace(" ", "_")}.md"
        File("notite").mkdirs()
        File(numeFisier).writeText("# Autor: $autor\n## Data: $dataOra\n\n$continut")
        println("Notita a fost salvata: $numeFisier")
    }
}

class ManagerNotite {
    fun listeazaNotite() {
        val director = File("notite")
        val fisiere = director.listFiles() ?: emptyArray()
        if (fisiere.isEmpty()) {
            println("Nu exista notite salvate.")
        } else {
            fisiere.sortedBy { it.lastModified() }.forEachIndexed { index, fisier ->
                println("${index + 1}. ${fisier.name}")
            }
        }
    }

    fun incarcaNotita(numeFisier: String) {
        val fisier = File("notite/$numeFisier")
        if (fisier.exists()) {
            println(fisier.readText())
        } else {
            println("Fisierul nu exista.")
        }
    }

    fun stergeNotita(numeFisier: String) {
        val fisier = File("notite/$numeFisier")
        if (fisier.exists() && fisier.delete()) {
            println("Notita $numeFisier a fost stearsa.")
        } else {
            println("Eroare la stergerea notitei.")
        }
    }
}

fun main() {
    val managerNotite = ManagerNotite()
    while (true) {
        println("\n1. Afisare notite\n2. Incarcare notita\n3. Creare notita\n4. Stergere notita\n5. Iesire")
        when (readLine()) {
            "1" -> managerNotite.listeazaNotite()
            "2" -> {
                println("Introduceti numele fisierului: ")
                val numeFisier = readLine() ?: ""
                managerNotite.incarcaNotita(numeFisier)
            }
            "3" -> {
                println("Introduceti autorul: ")
                val autor = readLine() ?: "Anonim"
                println("Introduceti continutul notitei: ")
                val continut = readLine() ?: ""
                Notita(autor, continut).salveazaInFisier()
            }
            "4" -> {
                println("Introduceti numele fisierului: ")
                val numeFisier = readLine() ?: ""
                managerNotite.stergeNotita(numeFisier)
            }
            "5" -> return
            else -> println("Optiune invalida.")
        }
    }
}
