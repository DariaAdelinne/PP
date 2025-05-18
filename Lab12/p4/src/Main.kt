// 1) Definim o extensie pentru String care transformă un text în PascalCase
fun String.toPascalCase(): String =
    split("\\s+".toRegex())
        .joinToString("") { word ->
            word.lowercase()
                .replaceFirstChar { it.uppercaseChar() }
        }

// 2) Functor pentru MutableMap<K,V>, care permite să „mapăm” valorile
class MutableMapFunctor<K, V>(
    private val backing: MutableMap<K, V>
) {
    /**
     * Aplică transform(value) pe fiecare valoare din hartă,
     * returnând un nou MutableMapFunctor cu rezultatul.
     */
    fun map(transform: (V) -> V): MutableMapFunctor<K, V> {
        val result = mutableMapOf<K, V>()
        for ((key, value) in backing) {
            result[key] = transform(value)
        }
        return MutableMapFunctor(result)
    }

    /** Returnează harta rezultată după toate map-urile. */
    fun value(): MutableMap<K, V> = backing
}

// 3) Testăm funcționalitatea
fun main() {
    // inițial un MutableMap<Int, String>
    val data = mutableMapOf(
        1 to "hello world",
        2 to "kotlin functor example",
        3 to "functional programming",
        4 to "zip and map"
    )

    // Construim functorul, aplicăm două map-uri și luăm harta finală
    val finalMap = MutableMapFunctor(data)
        .map { "Test$it" }       // 1. adaugă prefixul "Test"
        .map { it.toPascalCase() } // 2. transformă în PascalCase
        .value()

    // Afișăm rezultatul
    println(finalMap)
}
