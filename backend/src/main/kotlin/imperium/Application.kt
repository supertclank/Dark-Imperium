package imperium

import io.ktor.http.*
import io.ktor.serialization.kotlinx.json.*
import io.ktor.server.application.*
import io.ktor.server.engine.*
import io.ktor.server.netty.*
import io.ktor.server.plugins.*
import io.ktor.server.plugins.contentnegotiation.*
import io.ktor.server.plugins.statuspages.*
import io.ktor.server.request.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.serialization.SerializationException
import kotlinx.serialization.json.Json
import org.slf4j.LoggerFactory

data class AppConfig(val origin: String, val secureCookie: Boolean) {
    init { require(!secureCookie || origin.startsWith("https://")) { "Secure cookies require an HTTPS APP_ORIGIN" } }
}
fun main() {
    fun env(name: String) = requireNotNull(System.getenv(name)) { "$name is required" }
    val db = Database(env("DATABASE_URL"), env("DATABASE_USER"), env("DATABASE_PASSWORD"))
    db.migrate()
    val config = AppConfig(env("APP_ORIGIN"), (System.getenv("COOKIE_SECURE") ?: "true").toBooleanStrict())
    embeddedServer(Netty, port = 8080) {
        monitor.subscribe(ApplicationStopped) { db.close() }
        module(db, config)
    }.start(wait = true)
}
fun Application.module(db: Database, config: AppConfig, dice: DiceEngine = DiceEngine()) {
    val auth = AuthService(db)
    val content = ContentRepository(db)
    val characters = ProductionCharacters(db)
    val rolls = CharacterRolls(db,characters,dice)
    val freeRolls = FreeRolls(db,dice)
    val advancements = CharacterAdvancement(db,characters)
    val logger = LoggerFactory.getLogger("imperium.api")
    install(ContentNegotiation) { json(Json { ignoreUnknownKeys = false }) }
    install(StatusPages) {
        exception<InvalidDraft> { call, e -> call.respond(HttpStatusCode.UnprocessableEntity, DraftValidation("INVALID", e.issues)) }
        exception<ApiException> { call, e -> call.respond(HttpStatusCode.fromValue(e.status), ApiError(ErrorDetail(e.code, e.message))) }
        exception<BadRequestException> { call, _ -> call.respond(HttpStatusCode.BadRequest, ApiError(ErrorDetail("INVALID_REQUEST", "The request body is invalid."))) }
        exception<SerializationException> { call, _ -> call.respond(HttpStatusCode.BadRequest, ApiError(ErrorDetail("INVALID_REQUEST", "The request body is invalid."))) }
        exception<Throwable> { call, e ->
            logger.error("Request failed: {} {}", call.request.httpMethod.value, call.request.path(), e)
            call.respond(HttpStatusCode.InternalServerError, ApiError(ErrorDetail("INTERNAL_ERROR", "The request could not be completed. Please try again.")))
        }
    }
    intercept(ApplicationCallPipeline.Plugins) {
        call.response.header(HttpHeaders.CacheControl, "no-store")
        call.response.header("X-Content-Type-Options", "nosniff")
        if (call.request.httpMethod in listOf(HttpMethod.Post, HttpMethod.Patch, HttpMethod.Delete, HttpMethod.Put)) {
            if (call.request.header(HttpHeaders.Origin) != config.origin)
                throw ApiException(403, "INVALID_ORIGIN", "Request origin is not allowed.")
            if (call.request.header(HttpHeaders.ContentLength)?.toLongOrNull()?.let { it > 16_384 } == true)
                throw ApiException(413, "REQUEST_TOO_LARGE", "Request body is too large.")
        }
    }
    fun ApplicationCall.session() = request.cookies["di_session"]
    suspend fun ApplicationCall.owner() = withContext(Dispatchers.IO) { uuid(auth.user(session()).id) }
    fun ApplicationCall.cookie(token: String, maxAge: Int) {
        response.cookies.append(Cookie("di_session", token, path = "/", httpOnly = true,
            secure = config.secureCookie, maxAge = maxAge, extensions = mapOf("SameSite" to "Lax")))
    }
    routing {
        route("/api") {
            get("/health") { withContext(Dispatchers.IO) { db.read { it.query("SELECT 1") { r -> r.getInt(1) } } }; call.respond(mapOf("status" to "ok")) }
            post("/auth/register") {
                val input = call.receive<Credentials>()
                call.respond(HttpStatusCode.Created, withContext(Dispatchers.IO) { auth.register(input) })
            }
            post("/auth/login") {
                val input = call.receive<Credentials>()
                val (user, token) = withContext(Dispatchers.IO) { auth.login(input) }
                call.cookie(token, 7 * 24 * 60 * 60); call.respond(user)
            }
            post("/auth/logout") {
                withContext(Dispatchers.IO) { auth.logout(call.session()) }
                call.cookie("", 0); call.respond(HttpStatusCode.NoContent)
            }
            get("/auth/me") { call.respond(withContext(Dispatchers.IO) { auth.user(call.session()) }) }
            get("/species") { call.owner(); call.respond(withContext(Dispatchers.IO) { content.list(ContentKind.SPECIES) }) }
            get("/classes") { call.owner(); call.respond(withContext(Dispatchers.IO) { content.list(ContentKind.CLASS) }) }
            get("/weapons") { call.owner(); call.respond(withContext(Dispatchers.IO) { content.weapons() }) }
            get("/character-builder/profile") { call.owner(); call.respond(characters.rules.profile()) }
            post("/characters/validate") {
                call.owner(); val input=call.receive<NarrowDraft>()
                call.respond(withContext(Dispatchers.Default) { characters.rulesFor(input.profileId).validate(input) })
            }
            get("/characters") { val owner = call.owner(); call.respond(withContext(Dispatchers.IO) { characters.list(owner) }) }
            post("/characters") {
                val owner = call.owner(); val input = call.receive<NarrowDraft>()
                val sheet = withContext(Dispatchers.IO) { characters.create(owner, input) }
                call.response.header(HttpHeaders.Location, "/api/characters/${sheet.text("id")}")
                call.respond(HttpStatusCode.Created, sheet)
            }
            get("/characters/{id}") {
                val owner = call.owner(); val id = uuid(call.parameters["id"]!!)
                call.respond(withContext(Dispatchers.IO) { characters.get(owner, id) })
            }
            get("/characters/{id}/advancement") {
                val owner=call.owner();val id=uuid(call.parameters["id"]!!)
                call.respond(withContext(Dispatchers.IO) { advancements.readiness(owner,id) })
            }
            post("/characters/{id}/advancement/preview") {
                val owner=call.owner();val id=uuid(call.parameters["id"]!!);val input=call.receive<AdvanceRequest>()
                call.respond(withContext(Dispatchers.IO) { advancements.preview(owner,id,input) })
            }
            post("/characters/{id}/advance") {
                val owner=call.owner();val id=uuid(call.parameters["id"]!!);val input=call.receive<AdvanceRequest>()
                call.respond(withContext(Dispatchers.IO) { advancements.advance(owner,id,input) })
            }
            post("/rolls/free") {
                val owner=call.owner();val input=call.receive<FreeRollRequest>()
                call.respond(withContext(Dispatchers.IO) { freeRolls.execute(owner,input) })
            }
            get("/rolls/free") {
                val owner=call.owner();call.respond(withContext(Dispatchers.IO) { freeRolls.history(owner) })
            }
            get("/characters/{id}/rolls/options") {
                val owner=call.owner();val id=uuid(call.parameters["id"]!!)
                call.respond(withContext(Dispatchers.IO) { rolls.options(owner,id) })
            }
            post("/characters/{id}/rolls") {
                val owner=call.owner();val id=uuid(call.parameters["id"]!!);val input=call.receive<RollRequest>()
                call.respond(HttpStatusCode.OK,withContext(Dispatchers.IO) { rolls.execute(owner,id,input) })
            }
            get("/characters/{id}/rolls") {
                val owner=call.owner();val id=uuid(call.parameters["id"]!!)
                val limit=call.request.queryParameters["limit"]?.let { it.toIntOrNull() ?: throw ApiException(400,"INVALID_CONTEXT","History limit must be an integer.") } ?: 25
                call.respond(withContext(Dispatchers.IO) { rolls.history(owner,id,limit) })
            }
            patch("/characters/{id}") {
                val owner = call.owner(); val id = uuid(call.parameters["id"]!!); val input = call.receive<RenameCharacter>()
                call.respond(withContext(Dispatchers.IO) { characters.rename(owner, id, input.name) })
            }
            delete("/characters/{id}") {
                val owner = call.owner(); val id = uuid(call.parameters["id"]!!)
                withContext(Dispatchers.IO) { characters.delete(owner, id) }; call.respond(HttpStatusCode.NoContent)
            }
            route("/{...}") { handle { throw ApiException(404, "NOT_FOUND", "API resource not found.") } }
        }
    }
}
