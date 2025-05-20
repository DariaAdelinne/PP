fun String.toPascalCase(): String = //format PascalCase
    split("\\s+".toRegex()) //despare in cuvinte, pe baza spatiilor
        .joinToString("") { word -> //reuneste cuvintele cu un singur spatiu
            word.lowercase() //transformam in litere mici
                .replaceFirstChar { it.uppercaseChar() } //prima o facem mare
        }

class MutableMapFunctor<K, V>(private val backing: MutableMap<K, V>) { //clasa gennerica ce actioneaza ca un functor 
    fun map(transform: (V) -> V): MutableMapFunctor<K, V> { //transforma o valoare intr o noua valoare
        val result = mutableMapOf<K, V>() //harta temporara ce stocheaza rezultatele
        for ((key, value) in backing) {
            result[key] = transform(value) //aplicam functia pe fiecare valoare
        }
        return MutableMapFunctor(result)
    }

    fun value(): MutableMap<K, V> = backing //returneaza harta finala continuta de acest functor
}

fun main() {
    val data = mutableMapOf( //perechi int/string
        1 to "hello world",
        2 to "kotlin functor example",
        3 to "functional programming",
        4 to "zip and map"
    )

    val finalMap = MutableMapFunctor(data) //constrium functorul
        .map { "Test$it" }    
        .map { it.toPascalCase() } 
        .value() //extrage harta finala

    println(finalMap)
}
