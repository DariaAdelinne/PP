import java.io.File

/**
 * Aplică cifrul Caesar pe un cuvânt, cu un offset dat.
 */
fun caesarCipher(word: String, offset: Int): String {
    val shift = offset % 26
    return buildString {
        for (c in word) {
            when {
                c.isUpperCase() -> {
                    val base = 'A'.code
                    val code = (c.code - base + shift + 26) % 26 + base
                    append(code.toChar())
                }
                c.isLowerCase() -> {
                    val base = 'a'.code
                    val code = (c.code - base + shift + 26) % 26 + base
                    append(code.toChar())
                }
                else -> append(c)
            }
        }
    }
}

fun main() {
    val inputPath  = "src/input.txt"
    val outputPath = "src/output.txt"
    val offset     = 3

    // 1) Citește fișierul sursă
    val text = File(inputPath).readText()

    // 2) Criptează toate cuvintele cu lungime între 4 și 7
    val processed = Regex("\\b\\w+\\b").replace(text) { m ->
        val w = m.value
        if (w.length in 4..7) caesarCipher(w, offset) else w
    }

    // 3) Scrie în fișierul de destinație
    File(outputPath).writeText(processed)
    println("Am procesat '$inputPath': '$outputPath' cu offset=$offset")
}
