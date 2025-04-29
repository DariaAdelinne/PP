interface ImplementarePoarta { //primeste o lista de biti si returneaza rezultatul
    fun calculeaza(intrari: List<Boolean>): Boolean
}

class FsmAndImplementor : ImplementarePoarta { //fsm pentru and, parcurge lista de biti si opreste bucla cand gaseste un false; defineste cum face
    override fun calculeaza(intrari: List<Boolean>): Boolean {
        var allTrue = true
        for (bit in intrari) {
            if (!bit) {
                allTrue = false
                break
            }
        }
        return allTrue
    }
}

abstract class Poarta(protected val implementare: ImplementarePoarta, protected val intrari: List<Boolean>) { //primeste un fsm si lista; defineste ce poate face
    abstract fun evalueaza(): Boolean //rezultatul logic pe intrarile respective
}

class PoartaAndGeneric(implementare: ImplementarePoarta, intrari: List<Boolean>) : Poarta(implementare, intrari) { //poarta AND, extinde Poarta
    override fun evalueaza(): Boolean = implementare.calculeaza(intrari)
}

class ConstructorPoarta(private val implementare: ImplementarePoarta, private val expectedInputs: Int) { //
    private val intrari = mutableListOf<Boolean>() //gol in care se adauga pas cu pas fiecare bit

    fun adaugaIntrare(bit: Boolean): ConstructorPoarta {
        intrari += bit //adauga bitul la coada listei
        return this //returneaza instanta de builder (permite apeluri in lant)
    }

    fun construieste(): PoartaAndGeneric {
        return PoartaAndGeneric(implementare, intrari.toList()) //returneaza instanta gata configurata
    }
}

fun genereazaCombinatii(n: Int): List<List<Int>> { //primeste numarul de biti din fiecare combinatie
    val rezultat = mutableListOf<List<Int>>() //lista de liste de int, unde fiecare sublista este o combinatie
    val total = 1 shl n //numarul de moduri de a alege n biti
    for (i in 0 until total) {
        val comb = mutableListOf<Int>() //pentru fiecare i cream o lista goala
        for (j in n - 1 downTo 0) { //parcurgem pozitiile bitilor de la cel mai semnificativ
            comb += (i shr j) and 1 //adauga in lista numarul
        }
        rezultat += comb //adaugam in rezultat lista
    }
    return rezultat
}

fun afiseazaRezultate(n: Int) {
    val implementare = FsmAndImplementor() //creaza o instanta a implementarii portii AND
    println("*** Porti AND cu $n intrari ***")
    for (comb in genereazaCombinatii(n)) { //parcurge toate combinatiile
        val builder = ConstructorPoarta(implementare, n) //pentru fiecare combinatie initializeaa un builder care foloseste implementare pentru calcul
        for (bit in comb) { // parcurge fiecare bit din combinatie
            builder.adaugaIntrare(bit == 1) //adauga fiecare valoate in lista builder
        }
        val poarta = builder.construieste() //se face o poartaAndGeneric care contine implementare si lista de intrari convertita in boolean

        val bits = comb.joinToString("") { if (it == 1) "1" else "0" } //transofrma lista in string si afiseaza
        println("$bits -> ${poarta.evalueaza()}")
    }
    println()
}

fun main() {
    listOf(2, 3, 4, 8).forEach { afiseazaRezultate(it) } //lista fixa cu valori si entru fiecare valoare afiseaza rezultatul
}
