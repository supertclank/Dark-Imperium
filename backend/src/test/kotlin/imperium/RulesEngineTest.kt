package imperium

import kotlin.test.*

class RulesEngineTest {
    @Test fun `effects compose without content identity`() {
        assertEquals(CalculatedValues(8, 15), RulesEngine.calculate(
            Rules(effects=listOf(Effect("add", "movement", 8))),
            Rules(effects=listOf(Effect("add", "maxWounds", 12), Effect("add", "maxWounds", 3)))))
    }
    @Test fun `unsupported effects fail explicitly`() {
        assertFailsWith<IllegalArgumentException> { RulesEngine.calculate(Rules(effects=listOf(Effect("execute", "movement", 1)))) }
        assertFailsWith<IllegalArgumentException> { RulesEngine.calculate(Rules(schemaVersion=2)) }
    }
    @Test fun `passwords are salted and verified`() {
        val first = Security.hash("a long passphrase")
        assertNotEquals(first, Security.hash("a long passphrase"))
        assertTrue(Security.verify("a long passphrase", first))
        assertFalse(Security.verify("wrong passphrase", first))
    }
    @Test fun `rate limiting expires`() {
        var now = 0L
        val limiter = AuthLimiter { now }
        limiter.check("account", 1)
        assertFailsWith<ApiException> { limiter.check("account", 1) }
        now = 900_001
        limiter.check("account", 1)
    }
}
