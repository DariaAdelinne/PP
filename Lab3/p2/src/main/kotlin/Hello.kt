import java.io.File
import java.io.IOException

fun eliminaSpatiiMultiple(text: String): String
{
    return text.replace(Regex("\\s+"), " ")//inlocuieste mai multe spatii cu unul singur
}

fun eliminaLiniiGoale(text: String): String
{
    return text.replace(Regex("(\r?\n)+"), "\n")//inlocuieste mai multe endl cu unul singur
}

fun eliminaNumerePagini(text: String): String
{
    return text.replace(Regex("\\s\\d+\\s"), " ")//elimina nr de pag
}

fun eliminaNumeAutor(text: String): String
{
    val cuvinte = text.split(Regex("\\s+"))//imparte textul in cuvinte
    val perechiCuvinte = mutableListOf<String>()//creeaza perechi de cuvinte
    for (i in 0 until cuvinte.size - 1)
    {
        perechiCuvinte.add("${cuvinte[i]} ${cuvinte[i + 1]}")
    }

    val frecventaPerechi = perechiCuvinte.groupingBy { it }.eachCount()//calculeaza frecventa perechilor
    val perecheFrecventa = frecventaPerechi.maxByOrNull { it.value }?.key//se afla perechea care apare cel mai des

    return if (perecheFrecventa != null)//perechea cea mai frecventa este eliminata din text
    {
        text.replace(perecheFrecventa, "")
    } else
    {
        text
    }
}

fun inlocuiesteCaractere(text: String): String
{
    val inlocuiriCaractere = mapOf( //perechi de caractere noi/vechi
        'ă' to 'a', 'Ă' to 'A',
        'â' to 'a', 'Â' to 'A',
        'î' to 'i', 'Î' to 'I',
        'ș' to 's', 'Ș' to 'S',
        'ț' to 't', 'Ț' to 'T'
    )

    var textNormalizat = text
    for ((caracterVechi, caracterNou) in inlocuiriCaractere)
    {
        textNormalizat = textNormalizat.replace(caracterVechi, caracterNou)//inlocuieste caracterele vechi cu cele noi
    }
    return textNormalizat
}

fun eliminaTitluriCapitole(text: String): String
{
    return text.replace(Regex("Capitolul\\s+[IVXLCDM]+"), "")//elimina capitolele
}

fun main()
{
    val fisierIntrare = "ebook.txt"
    val fisierIesire = "Rez.txt"

    try {
        var continut = File(fisierIntrare).readText(Charsets.UTF_8)

        continut = eliminaSpatiiMultiple(continut)
        continut = eliminaLiniiGoale(continut)
        continut = eliminaNumerePagini(continut)
        continut = eliminaNumeAutor(continut)
        continut = inlocuiesteCaractere(continut)
        continut = eliminaTitluriCapitole(continut)

        File(fisierIesire).writeText(continut, Charsets.UTF_8)
        println("Fisierul a fost salvat in $fisierIesire")
    }
    catch (e: IOException)
    {
        println("Eroare: ${e.message}")
    }
}