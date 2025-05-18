fun main() {
    val numbers = listOf(1, 21, 75, 39, 7, 2, 35, 3, 31, 7, 8)

    // 1) Eliminăm numerele mai mici decât 5
    val filtered = numbers.filter { it >= 5 }
    // filtered == [21, 75, 39, 7, 35, 31, 7, 8]

    // 2) Grupăm în perechi ne-supraviețuitoare de câte 2
    val pairs: List<Pair<Int,Int>> = filtered
        .chunked(2)            // List<List<Int>> cu subliste de câte 2
        .map { (a, b) ->       // destructurăm fiecare sublistă
            Pair(a, b)
        }
    // pairs == [(21,75), (39,7), (35,31), (7,8)]

    // 3) Multiplicăm elementele fiecărei perechi
    val products: List<Int> = pairs.map { (x, y) -> x * y }
    // products == [1575, 273, 1085, 56]

    // 4) Sumăm toate produsele
    val sumOfProducts = products.sum()  // 2989

    // Afișăm rezultatele
    println("Filtered:   $filtered")
    println("Pairs:      $pairs")
    println("Products:   $products")
    println("Sum result: $sumOfProducts")
}
