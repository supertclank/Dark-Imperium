package imperium

import io.ktor.client.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.http.*
import io.ktor.server.testing.*
import kotlinx.serialization.json.*
import org.testcontainers.containers.PostgreSQLContainer
import java.util.UUID
import kotlin.test.*

class ApiIntegrationTest {
    companion object {
        // A supplied database must be disposable and explicitly named with a _test suffix.
        private val database: Database by lazy {
            val url = System.getenv("TEST_DATABASE_URL")
            val db = if (url != null) {
                require(url.substringBefore('?').endsWith("_test")) { "Tests require a database ending in _test" }
                Database(url, System.getenv("TEST_DATABASE_USER") ?: "postgres", System.getenv("TEST_DATABASE_PASSWORD") ?: "")
            } else {
                val postgres = PostgreSQLContainer<Nothing>("postgres:17-alpine")
                postgres.start()
                Database(postgres.jdbcUrl, postgres.username, postgres.password)
            }
            db.migrate(); db
        }
    }
    private fun runApi(block: suspend ApplicationTestBuilder.() -> Unit) = testApplication {
        application { module(database, AppConfig("http://localhost:3000", false)) }
        block()
    }
    private suspend fun HttpClient.postJson(path: String, body: String, cookie: String? = null) = post(path) {
        header(HttpHeaders.Origin,"http://localhost:3000"); contentType(ContentType.Application.Json)
        if (cookie != null) header(HttpHeaders.Cookie,cookie)
        setBody(body)
    }
    private suspend fun HttpClient.account(): String {
        val credentials = """{"email":"${UUID.randomUUID()}@example.com","password":"a strong test passphrase"}"""
        assertEquals(HttpStatusCode.Created, postJson("/api/auth/register",credentials).status)
        val login = postJson("/api/auth/login",credentials)
        assertEquals(HttpStatusCode.OK,login.status)
        val cookie = login.headers[HttpHeaders.SetCookie]!!
        assertTrue(cookie.contains("HttpOnly",ignoreCase=true))
        assertTrue(cookie.contains("SameSite=Lax",ignoreCase=true))
        return cookie.substringBefore(';')
    }
    private suspend fun HttpClient.create(cookie:String, name:String="Test soldier"): HttpResponse = postJson("/api/characters", """{"name":"$name","speciesId":"10000000-0000-0000-0000-000000000001","classId":"20000000-0000-0000-0000-000000000001","weaponId":"30000000-0000-0000-0000-000000000001"}""", cookie)
    private suspend fun HttpResponse.json() = Json.parseToJsonElement(bodyAsText()).jsonObject

    @Test fun `registration login creation and persistent sheet retrieval`() = runApi {
        val cookie=client.account()
        val response=client.create(cookie)
        assertEquals(HttpStatusCode.Created,response.status)
        val created=response.json(); val id=created.getValue("id").jsonPrimitive.content
        assertEquals("Test soldier",created.getValue("name").jsonPrimitive.content)
        assertEquals(10,created.getValue("calculated").jsonObject.getValue("maxWounds").jsonPrimitive.int)
        assertEquals("Lasgun",created.getValue("equipment").jsonArray[0].jsonObject.getValue("name").jsonPrimitive.content)
        // A fresh HTTP request and repository connection must see the committed row.
        val fetched=client.get("/api/characters/$id") {header(HttpHeaders.Cookie,cookie)}
        assertEquals(HttpStatusCode.OK,fetched.status); assertEquals(created,fetched.json())
        val stored=database.read {it.query("SELECT count(*) FROM characters WHERE id=?",uuid(id)){r->r.getInt(1)}.single()}
        assertEquals(1,stored)
        val list=client.get("/api/characters"){header(HttpHeaders.Cookie,cookie)}
        assertEquals(1,Json.parseToJsonElement(list.bodyAsText()).jsonArray.size)
    }
    @Test fun `ownership blocks reads updates deletes and list leakage`() = runApi {
        val owner=client.account();val stranger=client.account()
        val id=client.create(owner).json().getValue("id").jsonPrimitive.content
        assertEquals(HttpStatusCode.NotFound,client.get("/api/characters/$id"){header(HttpHeaders.Cookie,stranger)}.status)
        assertEquals(HttpStatusCode.NotFound,client.patch("/api/characters/$id"){
            header(HttpHeaders.Cookie,stranger);header(HttpHeaders.Origin,"http://localhost:3000")
            contentType(ContentType.Application.Json);setBody("""{"name":"stolen"}""")
        }.status)
        assertEquals(HttpStatusCode.NotFound,client.delete("/api/characters/$id"){
            header(HttpHeaders.Cookie,stranger);header(HttpHeaders.Origin,"http://localhost:3000")
        }.status)
        val list=client.get("/api/characters"){header(HttpHeaders.Cookie,stranger)}
        assertEquals(0,Json.parseToJsonElement(list.bodyAsText()).jsonArray.size)
        assertEquals(HttpStatusCode.OK,client.get("/api/characters/$id"){header(HttpHeaders.Cookie,owner)}.status)
    }
    @Test fun `seed species classes and weapons are available to authenticated users`() = runApi {
        val cookie=client.account()
        for ((path,name) in mapOf("species" to "Human","classes" to "Guardsman","weapons" to "Lasgun")) {
            val response=client.get("/api/$path"){header(HttpHeaders.Cookie,cookie)}
            assertEquals(HttpStatusCode.OK,response.status)
            assertEquals(name,Json.parseToJsonElement(response.bodyAsText()).jsonArray[0].jsonObject.getValue("name").jsonPrimitive.content)
        }
    }
    @Test fun `logout revokes cookie and unauthenticated requests fail`() = runApi {
        assertEquals(HttpStatusCode.Unauthorized,client.get("/api/characters").status)
        val cookie=client.account()
        assertEquals(HttpStatusCode.NoContent,client.postJson("/api/auth/logout","{}",cookie).status)
        assertEquals(HttpStatusCode.Unauthorized,client.get("/api/auth/me"){header(HttpHeaders.Cookie,cookie)}.status)
    }
    @Test fun `invalid credentials input and origin return structured errors`() = runApi {
        val invalid=client.postJson("/api/auth/register","""{"email":"bad","password":"short"}""")
        assertEquals(HttpStatusCode.BadRequest,invalid.status);assertTrue(invalid.json().containsKey("error"))
        assertEquals(HttpStatusCode.Unauthorized,client.postJson("/api/auth/login","""{"email":"absent@example.com","password":"not a valid password"}""").status)
        assertEquals(HttpStatusCode.Forbidden,client.post("/api/auth/register"){header(HttpHeaders.Origin,"https://evil.example")}.status)
        assertEquals(HttpStatusCode.Forbidden,client.post("/api/auth/logout").status)
        assertEquals(HttpStatusCode.BadRequest,client.postJson("/api/auth/login","{").status)
    }
    @Test fun `invalid content never creates a partial character`() = runApi {
        val cookie=client.account()
        val response=client.postJson("/api/characters","""{"name":"Invalid","speciesId":"10000000-0000-0000-0000-000000000001","classId":"20000000-0000-0000-0000-000000000001","weaponId":"${UUID.randomUUID()}"}""",cookie)
        assertEquals(HttpStatusCode.BadRequest,response.status)
        assertEquals("[]",client.get("/api/characters"){header(HttpHeaders.Cookie,cookie)}.bodyAsText())
        assertEquals(HttpStatusCode.BadRequest,client.create(cookie," ").status)
    }
    @Test fun `owner can rename and delete and equipment is removed`() = runApi {
        val cookie=client.account();val id=client.create(cookie).json().getValue("id").jsonPrimitive.content
        val renamed=client.patch("/api/characters/$id"){
            header(HttpHeaders.Cookie,cookie);header(HttpHeaders.Origin,"http://localhost:3000")
            contentType(ContentType.Application.Json);setBody("""{"name":"Renamed soldier"}""")
        }
        assertEquals(HttpStatusCode.OK,renamed.status);assertEquals("Renamed soldier",renamed.json().getValue("name").jsonPrimitive.content)
        assertEquals(HttpStatusCode.NoContent,client.delete("/api/characters/$id"){
            header(HttpHeaders.Cookie,cookie);header(HttpHeaders.Origin,"http://localhost:3000")
        }.status)
        assertEquals(HttpStatusCode.NotFound,client.get("/api/characters/$id"){header(HttpHeaders.Cookie,cookie)}.status)
        assertEquals(0,database.read{it.query("SELECT count(*) FROM character_equipment WHERE character_id=?",uuid(id)){r->r.getInt(1)}.single()})
    }
}
