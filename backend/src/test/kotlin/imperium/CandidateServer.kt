package imperium
import io.ktor.server.engine.*
import io.ktor.server.netty.*
/** Local review server uses test resources; candidate never becomes the production default here. */
object CandidateServer {
 @JvmStatic fun main(args:Array<String>) {
  val db=Database("jdbc:postgresql://127.0.0.1:55432/imperium_psychic_acceptance","postgres","");db.migrate()
  embeddedServer(Netty,host="127.0.0.1",port=8083){module(db,AppConfig("http://localhost:3200",false),rules=tier10Rules())}.start(wait=true)
 }
}
