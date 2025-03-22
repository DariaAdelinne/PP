interface MetodaPlata {
    fun plateste(suma: Double): Boolean
}

class PlataCash(private var soldDisponibil: Double) : MetodaPlata {
    override fun plateste(suma: Double): Boolean {
        return if (soldDisponibil >= suma) {
            soldDisponibil -= suma
            println("Platit $$suma cash.")
            true
        } else {
            println("Fonduri insuficiente.")
            false
        }
    }
}

class PlataCard(private val numarCard: String) : MetodaPlata {
    override fun plateste(suma: Double): Boolean {
        println("Platit $$suma folosind cardul $numarCard.")
        return true
    }
}

class PlataTransferBancar(private val iban: String) : MetodaPlata {
    override fun plateste(suma: Double): Boolean {
        println("Platit $$suma prin transfer bancar catre $iban.")
        return true
    }
}

class Film(val titlu: String, val durata: Int, val pret: Double)

class Bilet(val film: Film, val loc: String, val pret: Double)

class Utilizator(val nume: String, private val metodaPlata: MetodaPlata) {
    fun cumparaBilet(film: Film, loc: String): Bilet? {
        return if (metodaPlata.plateste(film.pret)) {
            println("$nume a cumparat un bilet pentru ${film.titlu} la locul $loc.")
            Bilet(film, loc, film.pret)
        } else {
            println("$nume nu a putut cumpara biletul.")
            null
        }
    }
}

fun main() {
    val film = Film("Inception", 148, 10.0)
    val utilizator1 = Utilizator("Alex", PlataCash(20.0))
    val utilizator2 = Utilizator("Maria", PlataCard("1234-5678-9012-3456"))
    val utilizator3 = Utilizator("Ion", PlataTransferBancar("RO49AAAA1B31007593840000"))

    utilizator1.cumparaBilet(film, "A10")
    utilizator2.cumparaBilet(film, "B5")
    utilizator3.cumparaBilet(film, "C3")
}
