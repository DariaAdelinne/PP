import kotlin.math.hypot

fun main() {
    println("Introduceti numarul de puncte si coordonatele lor:")

    val line = readLine()?.trim()
    if (line.isNullOrEmpty()) {
        println("Nu ati introdus nimic.")
        return
    }

    val tokens = line
        .split(Regex("\\s+")) //despartim sirul dupa unul/mai multe spatii
        .mapNotNull { it.toDoubleOrNull() } //convertim la double
    if (tokens.isEmpty()) {
        println("Input invalid.")
        return
    }

    val n = tokens[0].toInt() //nr de puncte
    val coords = tokens.drop(1) //coordonatele

    val points = coords
        .chunked(2) //grupeaza cate doua valori
        .map { (x, y) -> x to y } //creeaza perechi

    val sumAdj = points // suma distantelor intre perechi consecutive
        .zipWithNext { (x1,y1), (x2,y2) ->
            hypot(x2 - x1, y2 - y1)
        }
        .sum()

    val (xLast, yLast) = points.last() //calculam distantele de la ultimul punct la primul
    val (x0, y0)       = points.first()
    val sumClose = hypot(x0 - xLast, y0 - yLast)

    val perimeter = sumAdj + sumClose

    val out = if (perimeter % 1.0 == 0.0) 
        perimeter.toInt().toString()
    else
        String.format("%.4f", perimeter)

    println("Perimetrul poligonului este: $out")
}
