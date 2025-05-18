import kotlin.math.hypot

fun main() {
    // 1) Afișăm un mesaj de prompt
    println("Introduceti numarul de puncte si coordonatele lor:")

    // 2) Citim linia de input de la utilizator
    val line = readLine()?.trim()
    if (line.isNullOrEmpty()) {
        println("Nu ati introdus nimic.")
        return
    }

    // 3) Despărțim în numere
    val tokens = line
        .split(Regex("\\s+"))
        .mapNotNull { it.toDoubleOrNull() }
    if (tokens.isEmpty()) {
        println("Input invalid.")
        return
    }

    // 4) Primul token e n, apoi urmează 2*n coordonate
    val n = tokens[0].toInt()
    val coords = tokens.drop(1)

    // 5) Construim lista de puncte
    val points = coords
        .chunked(2)
        .map { (x, y) -> x to y }

    // 6) Sumă distanțe consecutive
    val sumAdj = points
        .zipWithNext { (x1,y1), (x2,y2) ->
            hypot(x2 - x1, y2 - y1)
        }
        .sum()

    // 7) Închidem poligonul (ultimul -> primul)
    val (xLast, yLast) = points.last()
    val (x0, y0)       = points.first()
    val sumClose = hypot(x0 - xLast, y0 - yLast)

    val perimeter = sumAdj + sumClose

    // 8) Afișăm rezultatul
    val out = if (perimeter % 1.0 == 0.0)
        perimeter.toInt().toString()
    else
        String.format("%.4f", perimeter)

    println("Perimetrul poligonului este: $out")
}
