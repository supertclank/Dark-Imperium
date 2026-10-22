package imperium

import java.util.Locale
import java.util.UUID

class AuthService(private val db: Database) {
    private val dummyHash = Security.hash(Security.token())
    private val limiter = AuthLimiter()
    private fun validate(input: Credentials): String {
        val email = input.email.trim().lowercase(Locale.ROOT)
        if (email.length !in 3..254 || !Regex("^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$").matches(email))
            throw ApiException(400, "INVALID_EMAIL", "Enter a valid email address.")
        if (input.password.length !in 12..128)
            throw ApiException(400, "INVALID_PASSWORD", "Passwords must contain 12 to 128 characters.")
        return email
    }
    private fun throttle(email: String) {
        limiter.check("global", 150)
        limiter.check(Security.digest(email), 15)
    }
    fun register(input: Credentials): UserView {
        val email = validate(input); throttle(email)
        val id = UUID.randomUUID()
        val hash = Security.hash(input.password)
        val inserted = db.read { it.execute("INSERT INTO users(id,email,password_hash) VALUES (?,?,?) ON CONFLICT(email) DO NOTHING", id, email, hash) }
        if (inserted == 0) throw ApiException(409, "EMAIL_UNAVAILABLE", "This email address cannot be registered.")
        return UserView(id.toString(), email)
    }
    fun login(input: Credentials): Pair<UserView, String> {
        val email = validate(input); throttle(email)
        val account = db.read { it.query("SELECT id,email,password_hash FROM users WHERE email=?", email) { r ->
            UserView(r.getString("id"), r.getString("email")) to r.getString("password_hash")
        }.singleOrNull() }
        val valid = Security.verify(input.password, account?.second ?: dummyHash)
        if (!valid || account == null) throw ApiException(401, "INVALID_CREDENTIALS", "Email or password is incorrect.")
        val token = Security.token()
        db.transaction {
            it.execute("DELETE FROM sessions WHERE expires_at < now()")
            it.execute("INSERT INTO sessions(token_hash,user_id,expires_at) VALUES (?,?,now()+interval '7 days')", Security.digest(token), uuid(account.first.id))
        }
        return account.first to token
    }
    fun user(token: String?): UserView {
        if (token == null || token.length != 43) throw ApiException(401, "UNAUTHENTICATED", "Please log in to continue.")
        return db.read { it.query("SELECT u.id,u.email FROM sessions s JOIN users u ON u.id=s.user_id WHERE s.token_hash=? AND s.expires_at>now()", Security.digest(token)) { r ->
            UserView(r.getString("id"), r.getString("email"))
        }.singleOrNull() } ?: throw ApiException(401, "UNAUTHENTICATED", "Your session has expired. Please log in.")
    }
    fun logout(token: String?) {
        if (token != null) db.read { it.execute("DELETE FROM sessions WHERE token_hash=?", Security.digest(token)) }
    }
}
