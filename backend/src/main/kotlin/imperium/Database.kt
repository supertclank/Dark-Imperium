package imperium

import com.zaxxer.hikari.HikariConfig
import com.zaxxer.hikari.HikariDataSource
import org.flywaydb.core.Flyway
import java.sql.Connection
import java.sql.PreparedStatement
import java.sql.ResultSet
import java.util.UUID

class Database(url: String, user: String, password: String) : AutoCloseable {
    private val pool = HikariDataSource(HikariConfig().apply {
        jdbcUrl = url; username = user; this.password = password
        maximumPoolSize = 8; connectionTimeout = 5000
    })
    fun migrate() { Flyway.configure().dataSource(pool).locations("classpath:migrations").load().migrate() }
    fun <T> read(block: (Connection) -> T): T = pool.connection.use(block)
    fun <T> transaction(block: (Connection) -> T): T = read { connection ->
        connection.autoCommit = false
        try { block(connection).also { connection.commit() } }
        catch (e: Exception) { connection.rollback(); throw e }
        finally { connection.autoCommit = true }
    }
    override fun close() = pool.close()
}

fun PreparedStatement.bind(values: Array<out Any?>) = values.forEachIndexed { i, v -> setObject(i + 1, v) }
fun Connection.execute(sql: String, vararg values: Any?): Int = prepareStatement(sql).use { it.bind(values); it.executeUpdate() }
fun <T> Connection.query(sql: String, vararg values: Any?, map: (ResultSet) -> T): List<T> =
    prepareStatement(sql).use { statement ->
        statement.bind(values)
        statement.executeQuery().use { rows -> buildList { while (rows.next()) add(map(rows)) } }
    }
fun uuid(value: String): UUID = try { UUID.fromString(value) } catch (_: IllegalArgumentException) {
    throw ApiException(400, "INVALID_ID", "A valid UUID is required.")
}
