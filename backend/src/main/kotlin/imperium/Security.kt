package imperium

import org.bouncycastle.crypto.generators.Argon2BytesGenerator
import org.bouncycastle.crypto.params.Argon2Parameters
import java.security.MessageDigest
import java.security.SecureRandom
import java.util.Base64

object Security {
    private val random = SecureRandom()
    private val encoder = Base64.getUrlEncoder().withoutPadding()
    private val decoder = Base64.getUrlDecoder()
    fun token(): String = encoder.encodeToString(ByteArray(32).also(random::nextBytes))
    fun digest(value: String): String = MessageDigest.getInstance("SHA-256").digest(value.toByteArray())
        .joinToString("") { "%02x".format(it) }
    // OWASP Argon2id baseline: 19 MiB, 2 iterations, parallelism 1.
    private fun derive(password: String, salt: ByteArray): ByteArray {
        val generator = Argon2BytesGenerator()
        generator.init(Argon2Parameters.Builder(Argon2Parameters.ARGON2_id)
            .withVersion(Argon2Parameters.ARGON2_VERSION_13).withMemoryAsKB(19456)
            .withIterations(2).withParallelism(1).withSalt(salt).build())
        return ByteArray(32).also { generator.generateBytes(password.toCharArray(), it) }
    }
    fun hash(password: String): String {
        val salt = ByteArray(16).also(random::nextBytes)
        return "argon2id-v1:${encoder.encodeToString(salt)}:${encoder.encodeToString(derive(password, salt))}"
    }
    fun verify(password: String, encoded: String): Boolean {
        val parts = encoded.split(':')
        if (parts.size != 3 || parts[0] != "argon2id-v1") return false
        return MessageDigest.isEqual(decoder.decode(parts[2]), derive(password, decoder.decode(parts[1])))
    }
}

/** Single-process fixed-window limiter; bounded storage, not based on spoofable forwarding headers. */
class AuthLimiter(private val clock: () -> Long = System::currentTimeMillis) {
    private data class Bucket(var count: Int, val expires: Long)
    private val buckets = mutableMapOf<String, Bucket>()
    @Synchronized fun check(key: String, limit: Int) {
        val now = clock()
        buckets.entries.removeIf { it.value.expires <= now }
        val bucket = buckets[key] ?: Bucket(0, now + 900_000).also {
            if (buckets.size >= 10_000) throw ApiException(429, "RATE_LIMITED", "Please try again later.")
            buckets[key] = it
        }
        if (++bucket.count > limit) throw ApiException(429, "RATE_LIMITED", "Too many attempts. Try again in 15 minutes.")
    }
}
