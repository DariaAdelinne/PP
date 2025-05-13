import kotlinx.coroutines.*
import kotlin.random.Random

// -------- Handler interface și implementare lanț dublu --------
interface Handler {
    var next: Handler?    // urmatorul in lant (forward)
    var prev: Handler?    // anteriorul in lant (backward)
    suspend fun handleRequest(message: String)
}

// -------- Factory Abstract și producător --------
abstract class AbstractFactory {
    abstract fun getHandler(handler: String): Handler
}

object FactoryProducer {
    fun getFactory(choice: String): AbstractFactory =
        when(choice.uppercase()) {
            "ELITE" -> EliteFactory()
            "HAPPY" -> HappyWorkerFactory()
            else -> throw IllegalArgumentException("Unknown factory: $choice")
        }
}

// -------- Fabrica pentru Elite (CEO, Executive, Manager) --------
class EliteFactory : AbstractFactory() {
    override fun getHandler(handler: String): Handler = when(handler) {
        "CEO" -> CEOHandler()
        "EXECUTIVE" -> ExecutiveHandler()
        "MANAGER" -> ManagerHandler()
        else -> throw IllegalArgumentException("Handler necunoscut Elite: $handler")
    }
}

// -------- Fabrica pentru HappyWorker --------
class HappyWorkerFactory : AbstractFactory() {
    override fun getHandler(handler: String): Handler = when(handler) {
        "HAPPYWORKER" -> HappyWorkerHandler()
        else -> throw IllegalArgumentException("Handler necunoscut Happy: $handler")
    }
}

// -------- Parsare mesaj Request: Priority:Mesaj --------
fun parseRequest(msg: String): Pair<Int, String>? {
    if (!msg.startsWith("Request-")) return null
    val body = msg.removePrefix("Request-")
    val sep = body.indexOf(':')
    if (sep < 1) return null
    val pr = body.substring(0, sep).toIntOrNull() ?: return null
    val text = body.substring(sep + 1)
    return pr to text
}

// -------- Implementari concrete Handler --------

abstract class BaseHandler(val name: String, val priority: Int) : Handler {
    override var next: Handler? = null
    override var prev: Handler? = null

    override suspend fun handleRequest(message: String) {
        coroutineScope {
            when {
                message.startsWith("Request-") -> {
                    // cerere primita
                    val parsed = parseRequest(message)
                    if (parsed != null && parsed.first == priority) {
                        // destinatarul corect
                        launch {
                            println("$name: Sunt $name si prelucrez mesajul: '${parsed.second}'")
                            // simuleaza procesare
                            delay(Random.nextLong(500, 1000))
                            val response = "Response-${parsed.second}"
                            // trimite raspuns pe lantul backward
                            prev?.let { p -> p.handleRequest(response) }
                        }
                    } else {
                        // nu e pentru mine, forward next
                        launch {
                            next?.handleRequest(message)
                        }
                    }
                }
                message.startsWith("Response-") -> {
                    // raspuns primiti
                    val respText = message.removePrefix("Response-")
                    launch {
                        println("$name: Raspuns primit: '$respText'")
                        delay(Random.nextLong(200, 500))
                        // propagate backward
                        prev?.let { p -> p.handleRequest(message) }
                    }
                }
                else -> println("$name: Mesaj necunoscut '$message'")
            }
        }
    }
}

class CEOHandler: BaseHandler("CEO", 1)
class ExecutiveHandler: BaseHandler("Executive", 2)
class ManagerHandler: BaseHandler("Manager", 3)
class HappyWorkerHandler: BaseHandler("HappyWorker", 4)

// -------- Demonstrare --------
fun main() = runBlocking<Unit> {
    // obtinem fabrici
    val eliteFactory = FactoryProducer.getFactory("ELITE")
    val happyFactory = FactoryProducer.getFactory("HAPPY")

    // cream handler-ele
    val ceo    = eliteFactory.getHandler("CEO")
    val exec   = eliteFactory.getHandler("EXECUTIVE")
    val manager= eliteFactory.getHandler("MANAGER")
    val happy  = happyFactory.getHandler("HAPPYWORKER")

    // legam dublu lantul: next si prev
    ceo.next = exec
    exec.prev = ceo
    exec.next = manager
    manager.prev = exec
    manager.next = happy
    happy.prev = manager

    // pornim flux: cerere pentru Executive (priority=2)
    println("=== Incepem flux cerere -> Executive ===")
    ceo.handleRequest("Request-2:Salut lume")

    // asteptam suficient pentru a vedea output complet
    delay(3000)

    println("=== Alta cerere -> Manager ===")
    ceo.handleRequest("Request-3:Verifica procese")
    delay(3000)

    println("=== Cerere -> HappyWorker ===")
    ceo.handleRequest("Request-4:Imparte cutii")
    delay(3000)

    println("Final")
}