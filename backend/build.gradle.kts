plugins {
    kotlin("jvm") version "2.2.20"
    kotlin("plugin.serialization") version "2.2.20"
    application
}
repositories { mavenCentral() }
val ktorVersion = "3.3.1"
dependencies {
    implementation("io.ktor:ktor-server-netty:$ktorVersion")
    implementation("io.ktor:ktor-server-content-negotiation:$ktorVersion")
    implementation("io.ktor:ktor-serialization-kotlinx-json:$ktorVersion")
    implementation("io.ktor:ktor-server-status-pages:$ktorVersion")
    implementation("com.zaxxer:HikariCP:6.3.3")
    implementation("org.postgresql:postgresql:42.7.8")
    implementation("org.flywaydb:flyway-core:11.13.2")
    implementation("org.flywaydb:flyway-database-postgresql:11.13.2")
    implementation("org.bouncycastle:bcprov-jdk18on:1.82")
    implementation("ch.qos.logback:logback-classic:1.5.20")
    testImplementation(kotlin("test"))
    testImplementation("io.ktor:ktor-server-test-host:$ktorVersion")
    testImplementation("org.testcontainers:postgresql:1.21.3")
}
kotlin { jvmToolchain(21) }
application { mainClass.set("imperium.ApplicationKt") }
sourceSets.main { resources.srcDir("../database") }
tasks.test { useJUnitPlatform() }
