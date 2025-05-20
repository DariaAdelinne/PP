fun main() {
    val numbers = listOf(1, 21, 75, 39, 7, 2, 35, 3, 31, 7, 8)
    val filtered = numbers.filter { it >= 5 } 
    val pairs: List<Pair<Int,Int>> = filtered
        .chunked(2)            //imparte lista in subliste de 2 elemente
        .map { (a, b) ->     
            Pair(a, b)    //cream perechea
        }

    val products: List<Int> = pairs.map { (x, y) -> x * y }

    val sumOfProducts = products.sum()

    println("Filtered:   $filtered")
    println("Pairs:      $pairs")
    println("Products:   $products")
    println("Sum result: $sumOfProducts")
}
