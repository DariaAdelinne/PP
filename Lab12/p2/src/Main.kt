import java.io.File

fun caesarCipher(word: String, offset: Int): String { //aplica cifrul Caesar pe un String 
    val shift = offset % 26 //normalizeaza offset-ul [0,25]
    return buildString { //creaza un StringBuilder
        for (c in word) { 
            when {
                c.isUpperCase() -> {
                    val base = 'A'.code
                    val code = (c.code - base + shift + 26) % 26 + base // calculeaza nou caracter
                    append(code.toChar())
                }
                c.isLowerCase() -> {
                    val base = 'a'.code
                    val code = (c.code - base + shift + 26) % 26 + base
                    append(code.toChar())
                }
                else -> append(c) //daca nu e litera il lasa neschimbat
            }
        }
    }
}

fun main() {
    val inputPath  = "src/input.txt"
    val outputPath = "src/output.txt"
    val offset     = 3 //offsetul Caesar

    val text = File(inputPath).readText()

    val processed = Regex("\\b\\w+\\b").replace(text) { m -> //pentru a identifica cuvintele
        val w = m.value
        if (w.length in 4..7) caesarCipher(w, offset) else w //fiecare cuvant cu lungimea intre 4-7 se cripteaza
    }

    File(outputPath).writeText(processed)
    println("Am procesat '$inputPath': '$outputPath' cu offset=$offset")
}
