import khttp.get
import org.jsoup.Jsoup
import org.json.JSONObject
import org.yaml.snakeyaml.Yaml

interface Parser {
    fun parse(text: String): Map<String, Any>
}

class ParserJson : Parser {
    override fun parse(text: String): Map<String, Any> {
        val obiectJson = JSONObject(text)
        return obiectJson.toMap() // Convertim JSON in Map
    }
}

class ParserXml : Parser {
    override fun parse(text: String): Map<String, Any> {
        val documentXml = Jsoup.parse(text, "", org.jsoup.parser.Parser.xmlParser())
        return mapOf("radacina" to documentXml.outerHtml()) // Returnam continutul XML
    }
}

class ParserYaml : Parser {
    override fun parse(text: String): Map<String, Any> {
        val yaml = Yaml()
        return yaml.load(text) as Map<String, Any> // Parsam YAML folosind SnakeYAML
    }
}

class CrawlerWeb(private val url: String) {
    fun obtineResursa(): String {
        val raspuns = get(url)
        return raspuns.text
    }

    fun proceseazaContinut(tipContinut: String, parser: Parser): Map<String, Any> {
        val continut = obtineResursa()
        return parser.parse(continut)
    }
}

fun main() {
    val url = "https://jsonplaceholder.typicode.com/todos/1" // Exemplu pentru JSON
    val crawler = CrawlerWeb(url)

    val parserJson = ParserJson()
    val dateParsate = crawler.proceseazaContinut("application/json", parserJson)

    println(dateParsate)
}
