---
name: mysql-connector-java-to-mariadb-migration
description: Domain knowledge for migrating Java applications from MySQL Connector/J 5.1.x to MariaDB Connector/J (mariadb-java-client 2.7.x / 3.x) on Rocky Linux 8.10. Covers Maven/Gradle dependency changes, RPM spec file updates, JDBC URL migration, driver and DataSource class changes, connection property mapping, SSL/TLS configuration, Spring/Hibernate/HikariCP integration, and common compilation and runtime errors.
applyTo: ["**/*.java", "**/pom.xml", "**/build.gradle", "**/build.gradle.kts", "**/*.properties", "**/application*.yml", "**/application*.yaml", "**/persistence.xml", "**/hibernate.cfg.xml", "**/context.xml", "**/web.xml", "**/*.spec", "**/Makefile*", "**/*.mk", "**/*.xml", "**/MANIFEST.MF", "**/*.conf", "**/*.cfg"]
---

# Java Connector Migration Guide: MySQL Connector/J 5.1.x → MariaDB Connector/J

This skill provides comprehensive guidance for migrating Java applications from MySQL Connector/J 5.1.x to MariaDB Connector/J (`mariadb-java-client` 2.7.x / 3.x) on Rocky Linux 8.10, covering dependency changes, JDBC URL and driver class migration, connection property mapping, framework integration, and common errors.

## Overview

### Why MariaDB Connector/J on Rocky Linux 8.10

Rocky Linux 8.10 does not ship MySQL Enterprise or the MySQL Connector/J driver. The MariaDB Connector/J driver (`mariadb-java-client`) is the supported JDBC driver for MariaDB 10.11 on Rocky Linux 8.10. It is available both as an RPM package (`mariadb-java-client`) in the AppStream repository and as a Maven artifact (`org.mariadb.jdbc:mariadb-java-client`).

MariaDB Connector/J implements the standard JDBC 4.2 API and maintains a high degree of compatibility with MySQL Connector/J for common operations, but has key differences in driver class names, DataSource classes, connection properties, and JDBC URL schemes.

### Version Comparison Summary

| Feature | MySQL Connector/J 5.1.x | MariaDB Connector/J 2.7.x | MariaDB Connector/J 3.x |
|---|---|---|---|
| Maven groupId | `mysql` | `org.mariadb.jdbc` | `org.mariadb.jdbc` |
| Maven artifactId | `mysql-connector-java` | `mariadb-java-client` | `mariadb-java-client` |
| JDBC URL scheme | `jdbc:mysql://` | `jdbc:mariadb://` (also accepts `jdbc:mysql://`) | `jdbc:mariadb://` (also accepts `jdbc:mysql://`) |
| Driver class | `com.mysql.jdbc.Driver` | `org.mariadb.jdbc.Driver` | `org.mariadb.jdbc.Driver` |
| DataSource class | `com.mysql.jdbc.jdbc2.optional.MysqlDataSource` | `org.mariadb.jdbc.MariaDbDataSource` | `org.mariadb.jdbc.MariaDbDataSource` |
| Pool DataSource | `MysqlConnectionPoolDataSource` | `MariaDbPoolDataSource` | `MariaDbPoolDataSource` |
| XA DataSource | `MysqlXADataSource` | `MariaDbDataSource` (implements XADataSource) | `MariaDbDataSource` (implements XADataSource) |
| SSL property | `useSSL=true/false` | `useSsl=true/false` | `sslMode=disable/trust/verify-ca/verify-full` |
| Auto-registration | Yes (JDBC 4+) | Yes (JDBC 4+) | Yes (JDBC 4+) |
| Rocky Linux RPM | Not available | `mariadb-java-client` (AppStream) | Not in AppStream; use Maven |
| Rocky 8.10 JAR path | N/A | `/usr/share/java/mariadb-java-client.jar` | N/A (embedded or Maven) |

> **Recommendation for Rocky Linux 8.10 + MariaDB 10.11:** Use MariaDB Connector/J **3.x** via Maven for the best compatibility with MariaDB 10.11 LTS. Use 2.7.x if the module relies on the system RPM package.

---

## 1. Maven / Gradle Dependency Changes

### 1a. Maven (`pom.xml`)

**Before:**
```xml
<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>5.1.49</version>
</dependency>
```

**After (MariaDB Connector/J 3.x — recommended for MariaDB 10.11):**
```xml
<dependency>
    <groupId>org.mariadb.jdbc</groupId>
    <artifactId>mariadb-java-client</artifactId>
    <version>3.3.3</version>
</dependency>
```

**After (MariaDB Connector/J 2.7.x — if using system RPM):**
```xml
<dependency>
    <groupId>org.mariadb.jdbc</groupId>
    <artifactId>mariadb-java-client</artifactId>
    <version>2.7.12</version>
    <scope>provided</scope>  <!-- provided by system RPM -->
</dependency>
```

> **Note on `<scope>provided</scope>`:** Use `provided` only when the `mariadb-java-client` JAR is installed as a system RPM and available on the runtime classpath (e.g., in `/usr/share/java/`). If the JAR is bundled in the application, use the default scope (`compile`).

### 1b. Gradle (`build.gradle`)

**Before:**
```groovy
dependencies {
    implementation 'mysql:mysql-connector-java:5.1.49'
}
```

**After:**
```groovy
dependencies {
    implementation 'org.mariadb.jdbc:mariadb-java-client:3.3.3'
}
```

**Gradle Kotlin DSL (`build.gradle.kts`):**
```kotlin
// Before
implementation("mysql:mysql-connector-java:5.1.49")

// After
implementation("org.mariadb.jdbc:mariadb-java-client:3.3.3")
```

### 1c. Direct JAR / Classpath (non-Maven builds)

For TMOS modules that embed the JDBC JAR directly in the source tree or reference a system-installed JAR:

**Before:**
```bash
# System-installed MySQL Connector/J
CLASSPATH=/usr/share/java/mysql-connector-java.jar

# Or embedded in source
CLASSPATH=lib/mysql-connector-java-5.1.49.jar
```

**After:**
```bash
# System-installed MariaDB Connector/J (from RPM)
CLASSPATH=/usr/share/java/mariadb-java-client.jar

# Or embedded — replace the JAR in the lib/ directory
CLASSPATH=lib/mariadb-java-client-3.3.3.jar
```

**Steps to replace an embedded JAR:**
```bash
# 1. Open files for edit in Perforce
p4 edit lib/mysql-connector-java-5.1.49.jar

# 2. Add the new JAR
# (download or copy from /usr/share/java/mariadb-java-client.jar)
cp /usr/share/java/mariadb-java-client.jar lib/mariadb-java-client-3.3.3.jar
p4 add lib/mariadb-java-client-3.3.3.jar

# 3. Mark old JAR for delete after confirming the new one works
# p4 delete lib/mysql-connector-java-5.1.49.jar
```

---

## 2. RPM Spec File Changes

### 2a. BuildRequires — Replace MySQL Connector/J with MariaDB Connector/J

**Before:**
```spec
BuildRequires: mysql-connector-java
BuildRequires: mysql-enterprise-java
BuildRequires: mysql-connector-java >= 5.1
```

**After:**
```spec
BuildRequires: mariadb-java-client
```

> **Note:** The `mariadb-java-client` RPM is available in the Rocky Linux 8.10 AppStream repository and installs the JAR at `/usr/share/java/mariadb-java-client.jar`.

### 2b. Runtime Requires

**Before:**
```spec
Requires: mysql-connector-java
Requires: mysql-enterprise-java
```

**After:**
```spec
Requires: mariadb-java-client
```

### 2c. Classpath References in `%build` Section

If the spec file explicitly references the MySQL Connector/J JAR in the build classpath:

**Before:**
```spec
%build
%{gcc_toolset_enable}
export CLASSPATH=/usr/share/java/mysql-connector-java.jar:$CLASSPATH
javac -cp /usr/share/java/mysql-connector-java.jar ...
```

**After:**
```spec
%build
%{gcc_toolset_enable}
export CLASSPATH=/usr/share/java/mariadb-java-client.jar:$CLASSPATH
javac -cp /usr/share/java/mariadb-java-client.jar ...
```

### 2d. Maven Build in Spec File

If the spec file invokes Maven and the driver dependency is managed through Maven:

**Before:**
```spec
%build
%{gcc_toolset_enable}
mvn package -Dmysql.connector.version=5.1.49
```

**After:**
```spec
%build
%{gcc_toolset_enable}
mvn package -Dmariadb.connector.version=3.3.3
```

Or if the version is hardcoded in `pom.xml`, updating `pom.xml` is sufficient (see Section 1a).

### 2e. Full Spec Diff Example

**Before:**
```spec
Summary: TMOS database module
Name:    mymodule
Version: %{version}
Release: %{release}
License: Commercial
Packager: F5 Networks <support@f5.com>

BuildRequires: java-21-openjdk-devel
BuildRequires: mysql-connector-java
Requires: mysql-connector-java
```

**After:**
```spec
Summary: TMOS database module
Name:    mymodule
Version: %{version}
Release: %{release}
License: Commercial
Packager: F5 Networks <support@f5.com>

%global debug_package %{nil}
# Include GCC toolchain configuration
%include %{_topdir}/gcc-toolchain.inc

BuildRequires: java-21-openjdk-devel
BuildRequires: mariadb-java-client
Requires: mariadb-java-client
```

---

## 3. JDBC URL Changes

### 3a. URL Scheme Migration

**Before (MySQL Connector/J):**
```
jdbc:mysql://hostname:3306/database
jdbc:mysql://hostname:3306/database?property1=value1&property2=value2
jdbc:mysql://hostname/database
jdbc:mysql:///database   (localhost via socket)
```

**After (MariaDB Connector/J):**
```
jdbc:mariadb://hostname:3306/database
jdbc:mariadb://hostname:3306/database?property1=value1&property2=value2
jdbc:mariadb://hostname/database
jdbc:mariadb:///database   (localhost via socket)
```

> **Backward Compatibility:** MariaDB Connector/J also accepts `jdbc:mysql://` URLs for drop-in compatibility. However, **always use `jdbc:mariadb://`** for new migrations to clearly identify the driver in use and avoid ambiguity if both drivers are ever present on the classpath.

### 3b. High-Availability URL Formats (MariaDB 3.x)

MariaDB Connector/J 3.x supports additional URL formats for high availability:

```
# Sequential failover
jdbc:mariadb:sequential://host1:3306,host2:3306/database

# Load balancing (round-robin)
jdbc:mariadb:loadbalance://host1:3306,host2:3306/database

# Galera cluster / synchronous replication
jdbc:mariadb:replication://primaryHost:3306,replicaHost:3306/database
```

These replace MySQL Connector/J's `jdbc:mysql:loadbalance://` and `jdbc:mysql:replication://` schemes.

### 3c. Search Patterns for URL Migration

```bash
# Find all JDBC URLs in Java source files
grep -rn "jdbc:mysql://" --include="*.java" .

# Find all JDBC URLs in properties and configuration files
grep -rn "jdbc:mysql://" --include="*.properties" --include="*.xml" --include="*.yml" --include="*.yaml" --include="*.conf" .

# Find all JDBC URLs in spec files
grep -rn "jdbc:mysql://" --include="*.spec" .
```

---

## 4. Driver Class and DataSource Changes

### 4a. Driver Class Registration

**Before (explicit Class.forName — required in JDBC 3, optional in JDBC 4+):**
```java
// MySQL Connector/J 5.1.x driver class names
Class.forName("com.mysql.jdbc.Driver");         // MySQL Connector/J 5.1.x
Class.forName("com.mysql.cj.jdbc.Driver");      // MySQL Connector/J 8.x
```

**After:**
```java
// MariaDB Connector/J driver class name
Class.forName("org.mariadb.jdbc.Driver");       // For explicit registration

// Or simply omit Class.forName entirely — JDBC 4.0+ auto-discovers drivers
// via META-INF/services/java.sql.Driver in the JAR (SPI mechanism)
// No Class.forName() call is needed when using JDBC 4.0+ (Java 6+)
```

> **Best Practice:** Remove `Class.forName()` entirely in new code. The driver is automatically registered when the `mariadb-java-client` JAR is on the classpath. Only keep `Class.forName()` if you must support explicit driver loading for compatibility with legacy code.

**Search for driver class references:**
```bash
# Find explicit driver class references in source files
grep -rn "com\.mysql\.jdbc\.Driver\|com\.mysql\.cj\.jdbc\.Driver" --include="*.java" --include="*.properties" --include="*.xml" --include="*.yml" .
```

### 4b. DataSource Classes

**Before:**
```java
// MySQL Connector/J 5.1.x
import com.mysql.jdbc.jdbc2.optional.MysqlDataSource;
import com.mysql.jdbc.jdbc2.optional.MysqlConnectionPoolDataSource;
import com.mysql.jdbc.jdbc2.optional.MysqlXADataSource;

MysqlDataSource ds = new MysqlDataSource();
ds.setServerName("localhost");
ds.setPort(3306);
ds.setDatabaseName("mydb");
ds.setUser("user");
ds.setPassword("password");
```

**After:**
```java
// MariaDB Connector/J
import org.mariadb.jdbc.MariaDbDataSource;
import org.mariadb.jdbc.MariaDbPoolDataSource;

// Basic DataSource (also implements ConnectionPoolDataSource and XADataSource)
MariaDbDataSource ds = new MariaDbDataSource();
ds.setUrl("jdbc:mariadb://localhost:3306/mydb");
ds.setUser("user");
ds.setPassword("password");

// Or using the URL constructor
MariaDbDataSource ds = new MariaDbDataSource("jdbc:mariadb://localhost:3306/mydb");
```

**Import search patterns:**
```bash
# Find all MySQL DataSource imports
grep -rn "com\.mysql\.jdbc\.jdbc2\.optional\|MysqlDataSource\|MysqlXADataSource\|MysqlConnectionPoolDataSource" --include="*.java" .
```

### 4c. Full Class Name Mapping

| MySQL Connector/J 5.1.x Class | MariaDB Connector/J Equivalent |
|---|---|
| `com.mysql.jdbc.Driver` | `org.mariadb.jdbc.Driver` |
| `com.mysql.cj.jdbc.Driver` | `org.mariadb.jdbc.Driver` |
| `com.mysql.jdbc.jdbc2.optional.MysqlDataSource` | `org.mariadb.jdbc.MariaDbDataSource` |
| `com.mysql.jdbc.jdbc2.optional.MysqlConnectionPoolDataSource` | `org.mariadb.jdbc.MariaDbPoolDataSource` |
| `com.mysql.jdbc.jdbc2.optional.MysqlXADataSource` | `org.mariadb.jdbc.MariaDbDataSource` |
| `com.mysql.jdbc.exceptions.jdbc4.CommunicationsException` | `java.sql.SQLNonTransientConnectionException` |
| `com.mysql.jdbc.exceptions.jdbc4.MySQLIntegrityConstraintViolationException` | `java.sql.SQLIntegrityConstraintViolationException` |
| `com.mysql.jdbc.exceptions.jdbc4.MySQLSyntaxErrorException` | `java.sql.SQLSyntaxErrorException` |
| `com.mysql.jdbc.exceptions.MySQLTimeoutException` | `java.sql.SQLTimeoutException` |
| `com.mysql.jdbc.PreparedStatement` | `java.sql.PreparedStatement` (use JDBC standard interface) |
| `com.mysql.jdbc.Statement` | `java.sql.Statement` (use JDBC standard interface) |

> **Key Principle:** Where possible, replace MySQL-specific class references with the equivalent standard JDBC interfaces (`java.sql.DataSource`, `java.sql.Connection`, `java.sql.PreparedStatement`, etc.). This makes the code portable across JDBC drivers.

---

## 5. Connection Properties Migration

MySQL Connector/J and MariaDB Connector/J use different property names for many configuration options. The table below maps the most commonly used MySQL Connector/J 5.1.x properties to their MariaDB Connector/J 3.x equivalents.

### 5a. Connection Property Mapping Table

| MySQL C/J 5.1.x Property | MariaDB C/J 2.7.x | MariaDB C/J 3.x | Notes |
|---|---|---|---|
| `useSSL=false` | `useSsl=false` | `sslMode=disable` | Different name and value in 3.x |
| `useSSL=true` | `useSsl=true` | `sslMode=trust` | Accepts the server cert without verification |
| `requireSSL=true` | `useSsl=true` | `sslMode=verify-ca` | Verifies CA but not hostname |
| `verifyServerCertificate=true` | `useSsl=true&trustServerCertificate=false` | `sslMode=verify-full` | Full verification (CA + hostname) |
| `serverTimezone=UTC` | `serverTimezone=UTC` | `timezone=UTC` | Property renamed in 3.x |
| `autoReconnect=true` | `autoReconnect=true` (deprecated) | Not supported | Use connection pooling instead |
| `allowPublicKeyRetrieval=true` | N/A | N/A | MySQL-specific (caching_sha2_password) |
| `useUnicode=true` | N/A (default UTF-8) | N/A | Not needed; always UTF-8 |
| `characterEncoding=UTF-8` | `charset=utf8` | `charset=utf8` | Set charset explicitly if needed |
| `characterEncoding=utf8mb4` | `charset=utf8mb4` | `charset=utf8mb4` | For full Unicode (emoji etc.) |
| `nullCatalogMeansCurrent=true` | `nullCatalogMeansCurrent=true` | `nullDatabaseMeansCurrent=true` | Renamed in 3.x |
| `clientCertificateKeyStoreUrl` | `keyStore` | `keyStore` | Renamed |
| `clientCertificateKeyStorePassword` | `keyStorePassword` | `keyStorePassword` | Renamed |
| `trustCertificateKeyStoreUrl` | `trustStore` | `trustStore` | Renamed |
| `trustCertificateKeyStorePassword` | `trustStorePassword` | `trustStorePassword` | Renamed |
| `connectTimeout=5000` | `connectTimeout=5000` | `connectTimeout=5000` | Same (milliseconds) |
| `socketTimeout=30000` | `socketTimeout=30000` | `socketTimeout=30000` | Same |
| `useServerPrepStmts=true` | `useServerPrepStmts=true` | `useServerPrepStmts=true` | Same |
| `cachePrepStmts=true` | `cachePrepStmts=true` | `cachePrepStmts=true` | Same |
| `prepStmtCacheSize=250` | `prepStmtCacheSize=250` | `prepStmtCacheSize=250` | Same |
| `prepStmtCacheSqlLimit=2048` | `prepStmtCacheSqlLimit=2048` | `prepStmtCacheSqlLimit=2048` | Same |
| `jdbcCompliantTruncation=false` | N/A | N/A | Controlled via SQL `sql_mode` |
| `maxAllowedPacket=` | `maxAllowedPacket=` | `maxAllowedPacket=` | Same |
| `defaultFetchSize=` | `defaultFetchSize=` | `defaultFetchSize=` | Same |
| `loginTimeout=` | `loginTimeout=` | `loginTimeout=` | Same |
| `allowMultiQueries=true` | `allowMultiQueries=true` | `allowMultiQueries=true` | Same |
| `rewriteBatchedStatements=true` | `rewriteBatchedStatements=true` | `rewriteBatchedStatements=true` | Same |

### 5b. URL Migration Examples

**Before:**
```properties
db.url=jdbc:mysql://localhost:3306/mydb?useSSL=false&serverTimezone=UTC&autoReconnect=true&characterEncoding=UTF-8&useUnicode=true
db.driver=com.mysql.jdbc.Driver
```

**After (MariaDB Connector/J 3.x):**
```properties
db.url=jdbc:mariadb://localhost:3306/mydb?sslMode=disable&timezone=UTC&charset=utf8mb4
db.driver=org.mariadb.jdbc.Driver
```

**After (MariaDB Connector/J 2.7.x):**
```properties
db.url=jdbc:mariadb://localhost:3306/mydb?useSsl=false&serverTimezone=UTC&charset=utf8mb4
db.driver=org.mariadb.jdbc.Driver
```

### 5c. Programmatic Connection Properties

**Before:**
```java
Properties props = new Properties();
props.setProperty("user", "dbuser");
props.setProperty("password", "secret");
props.setProperty("useSSL", "false");
props.setProperty("serverTimezone", "UTC");
props.setProperty("characterEncoding", "UTF-8");
props.setProperty("autoReconnect", "true");

Connection conn = DriverManager.getConnection(
    "jdbc:mysql://localhost:3306/mydb", props);
```

**After (MariaDB Connector/J 3.x):**
```java
Properties props = new Properties();
props.setProperty("user", "dbuser");
props.setProperty("password", "secret");
props.setProperty("sslMode", "disable");
props.setProperty("timezone", "UTC");
props.setProperty("charset", "utf8mb4");
// Remove autoReconnect — use connection pooling (HikariCP, DBCP) instead

Connection conn = DriverManager.getConnection(
    "jdbc:mariadb://localhost:3306/mydb", props);
```

---

## 6. SSL / TLS Configuration Migration

### 6a. SSL Properties Summary

MariaDB Connector/J 3.x replaced the boolean `useSSL`/`requireSSL`/`verifyServerCertificate` properties with a single `sslMode` property that maps to standard TLS verification levels.

**SSL Mode Values (MariaDB Connector/J 3.x):**

| `sslMode` Value | Description | MySQL C/J 5.1 Equivalent |
|---|---|---|
| `disable` | No SSL — all traffic unencrypted | `useSSL=false` |
| `trust` | SSL enabled, server certificate NOT verified | `useSSL=true&verifyServerCertificate=false` |
| `verify-ca` | SSL enabled, CA certificate verified | `requireSSL=true&verifyServerCertificate=true` (CA only) |
| `verify-full` | SSL enabled, CA and hostname verified | `requireSSL=true&verifyServerCertificate=true` (strictest) |

### 6b. SSL Migration Examples

**Before (disabled SSL):**
```properties
jdbc:mysql://host/db?useSSL=false
```
**After:**
```properties
jdbc:mariadb://host/db?sslMode=disable
```

**Before (SSL with no cert verification):**
```properties
jdbc:mysql://host/db?useSSL=true&verifyServerCertificate=false
```
**After:**
```properties
jdbc:mariadb://host/db?sslMode=trust
```

**Before (full SSL with certificate verification):**
```properties
jdbc:mysql://host/db?useSSL=true&requireSSL=true&verifyServerCertificate=true&trustCertificateKeyStoreUrl=file:/path/truststore.jks&trustCertificateKeyStorePassword=secret&clientCertificateKeyStoreUrl=file:/path/keystore.jks&clientCertificateKeyStorePassword=secret
```
**After:**
```properties
jdbc:mariadb://host/db?sslMode=verify-full&trustStore=file:/path/truststore.jks&trustStorePassword=secret&keyStore=file:/path/keystore.jks&keyStorePassword=secret
```

### 6c. MariaDB Connector/J 2.7.x SSL (if using the system RPM)

```properties
# MariaDB 2.7.x uses different property names from 3.x
jdbc:mariadb://host/db?useSsl=true&trustServerCertificate=false&keyStore=/path/keystore.jks&keyStorePassword=secret&trustStore=/path/truststore.jks&trustStorePassword=secret
```

---

## 7. Spring Framework Integration

### 7a. Spring XML Configuration

**Before (Spring XML — `applicationContext.xml` or `datasource-context.xml`):**
```xml
<bean id="dataSource"
      class="com.mysql.jdbc.jdbc2.optional.MysqlDataSource">
    <property name="serverName" value="localhost"/>
    <property name="port" value="3306"/>
    <property name="databaseName" value="mydb"/>
    <property name="user" value="dbuser"/>
    <property name="password" value="secret"/>
    <property name="useSSL" value="false"/>
    <property name="serverTimezone" value="UTC"/>
</bean>
```

**After:**
```xml
<bean id="dataSource"
      class="org.mariadb.jdbc.MariaDbDataSource">
    <property name="url" value="jdbc:mariadb://localhost:3306/mydb?sslMode=disable&amp;timezone=UTC"/>
    <property name="user" value="dbuser"/>
    <property name="password" value="secret"/>
</bean>
```

### 7b. Spring Boot `application.properties`

**Before:**
```properties
spring.datasource.driver-class-name=com.mysql.jdbc.Driver
spring.datasource.url=jdbc:mysql://localhost:3306/mydb?useSSL=false&serverTimezone=UTC
spring.datasource.username=dbuser
spring.datasource.password=secret
```

**After:**
```properties
spring.datasource.driver-class-name=org.mariadb.jdbc.Driver
spring.datasource.url=jdbc:mariadb://localhost:3306/mydb?sslMode=disable&timezone=UTC
spring.datasource.username=dbuser
spring.datasource.password=secret
```

### 7c. Spring Boot `application.yml`

**Before:**
```yaml
spring:
  datasource:
    driver-class-name: com.mysql.jdbc.Driver
    url: jdbc:mysql://localhost:3306/mydb?useSSL=false&serverTimezone=UTC
    username: dbuser
    password: secret
```

**After:**
```yaml
spring:
  datasource:
    driver-class-name: org.mariadb.jdbc.Driver
    url: jdbc:mariadb://localhost:3306/mydb?sslMode=disable&timezone=UTC
    username: dbuser
    password: secret
```

### 7d. Spring JNDI DataSource (`context.xml` in Tomcat)

**Before:**
```xml
<Resource name="jdbc/mydb"
          auth="Container"
          type="javax.sql.DataSource"
          driverClassName="com.mysql.jdbc.Driver"
          url="jdbc:mysql://localhost:3306/mydb?useSSL=false"
          username="dbuser"
          password="secret"
          maxTotal="20"
          maxIdle="10"
          maxWaitMillis="10000"/>
```

**After:**
```xml
<Resource name="jdbc/mydb"
          auth="Container"
          type="javax.sql.DataSource"
          driverClassName="org.mariadb.jdbc.Driver"
          url="jdbc:mariadb://localhost:3306/mydb?sslMode=disable"
          username="dbuser"
          password="secret"
          maxTotal="20"
          maxIdle="10"
          maxWaitMillis="10000"/>
```

---

## 8. Hibernate / JPA Integration

### 8a. Hibernate Dialect

**Before:**
```properties
# hibernate.properties or persistence.xml
hibernate.dialect=org.hibernate.dialect.MySQLDialect
# or
hibernate.dialect=org.hibernate.dialect.MySQL5InnoDBDialect
# or
hibernate.dialect=org.hibernate.dialect.MySQL5Dialect
```

**After (Hibernate 5.x):**
```properties
# Hibernate 5.4.x — use MariaDB-specific dialect
hibernate.dialect=org.hibernate.dialect.MariaDB103Dialect
# or for MariaDB 10.4+
hibernate.dialect=org.hibernate.dialect.MariaDB10Dialect
# or generic (least specific, always safe)
hibernate.dialect=org.hibernate.dialect.MariaDBDialect
```

**After (Hibernate 6.x):**
```properties
# Hibernate 6 auto-detects dialect; set explicitly as:
hibernate.dialect=org.hibernate.dialect.MariaDBDialect
```

> **Fallback:** If the `MariaDBDialect` class is not available in the Hibernate version in use, `MySQL5InnoDBDialect` or `MySQL5Dialect` will continue to work for basic queries, as MariaDB maintains SQL compatibility with MySQL 5.x.

### 8b. `persistence.xml` (JPA)

**Before:**
```xml
<persistence-unit name="myPU">
    <properties>
        <property name="javax.persistence.jdbc.driver"
                  value="com.mysql.jdbc.Driver"/>
        <property name="javax.persistence.jdbc.url"
                  value="jdbc:mysql://localhost:3306/mydb?useSSL=false"/>
        <property name="javax.persistence.jdbc.user" value="dbuser"/>
        <property name="javax.persistence.jdbc.password" value="secret"/>
        <property name="hibernate.dialect"
                  value="org.hibernate.dialect.MySQL5InnoDBDialect"/>
    </properties>
</persistence-unit>
```

**After:**
```xml
<persistence-unit name="myPU">
    <properties>
        <property name="javax.persistence.jdbc.driver"
                  value="org.mariadb.jdbc.Driver"/>
        <property name="javax.persistence.jdbc.url"
                  value="jdbc:mariadb://localhost:3306/mydb?sslMode=disable"/>
        <property name="javax.persistence.jdbc.user" value="dbuser"/>
        <property name="javax.persistence.jdbc.password" value="secret"/>
        <property name="hibernate.dialect"
                  value="org.hibernate.dialect.MariaDB103Dialect"/>
    </properties>
</persistence-unit>
```

---

## 9. Connection Pool Integration

### 9a. HikariCP (Recommended pool for Rocky Linux / Java 21 deployments)

**Before:**
```java
HikariConfig config = new HikariConfig();
config.setDriverClassName("com.mysql.jdbc.Driver");
config.setJdbcUrl("jdbc:mysql://localhost:3306/mydb?useSSL=false&serverTimezone=UTC");
config.setUsername("dbuser");
config.setPassword("secret");
config.setMaximumPoolSize(20);
config.setMinimumIdle(5);
config.setConnectionTimeout(30000);
config.setIdleTimeout(600000);
config.setMaxLifetime(1800000);
HikariDataSource ds = new HikariDataSource(config);
```

**After:**
```java
HikariConfig config = new HikariConfig();
config.setDriverClassName("org.mariadb.jdbc.Driver");  // Optional with JDBC 4+
config.setJdbcUrl("jdbc:mariadb://localhost:3306/mydb?sslMode=disable&timezone=UTC");
config.setUsername("dbuser");
config.setPassword("secret");
config.setMaximumPoolSize(20);
config.setMinimumIdle(5);
config.setConnectionTimeout(30000);
config.setIdleTimeout(600000);
config.setMaxLifetime(1800000);
// MariaDB Connector/J 3.x — use MariaDbDataSource as datasource class for best pool integration
config.setDataSourceClassName("org.mariadb.jdbc.MariaDbDataSource");
HikariDataSource ds = new HikariDataSource(config);
```

**HikariCP `application.properties` (Spring Boot):**
```properties
spring.datasource.type=com.zaxxer.hikari.HikariDataSource
spring.datasource.driver-class-name=org.mariadb.jdbc.Driver
spring.datasource.url=jdbc:mariadb://localhost:3306/mydb?sslMode=disable
spring.datasource.hikari.maximum-pool-size=20
spring.datasource.hikari.minimum-idle=5
spring.datasource.hikari.connection-timeout=30000
spring.datasource.hikari.idle-timeout=600000
spring.datasource.hikari.max-lifetime=1800000
```

> **Note on `autoReconnect`:** Do NOT use `autoReconnect=true` with connection pools. HikariCP handles connection validation and reconnection through `connectionTestQuery` or JDBC 4 `isValid()`. MariaDB Connector/J 3.x removed support for `autoReconnect` entirely. Configure pool-level health checks instead:
> ```properties
> spring.datasource.hikari.connection-test-query=SELECT 1
> spring.datasource.hikari.keepalive-time=60000
> ```

### 9b. Apache DBCP2

**Before:**
```java
BasicDataSource ds = new BasicDataSource();
ds.setDriverClassName("com.mysql.jdbc.Driver");
ds.setUrl("jdbc:mysql://localhost:3306/mydb?useSSL=false");
ds.setUsername("dbuser");
ds.setPassword("secret");
```

**After:**
```java
BasicDataSource ds = new BasicDataSource();
ds.setDriverClassName("org.mariadb.jdbc.Driver");
ds.setUrl("jdbc:mariadb://localhost:3306/mydb?sslMode=disable");
ds.setUsername("dbuser");
ds.setPassword("secret");
ds.setValidationQuery("SELECT 1");
```

### 9c. MariaDB Built-in Connection Pool (Connector/J 3.x)

MariaDB Connector/J 3.x includes a built-in connection pool via `MariaDbPoolDataSource`:

```java
MariaDbPoolDataSource poolDs = new MariaDbPoolDataSource(
    "jdbc:mariadb://localhost:3306/mydb?sslMode=disable&maxPoolSize=20&minPoolSize=5");
poolDs.setUser("dbuser");
poolDs.setPassword("secret");
Connection conn = poolDs.getConnection();
```

---

## 10. Exception Handling Changes

MySQL Connector/J 5.1.x exposed MySQL-specific exception classes. MariaDB Connector/J throws standard JDBC exceptions. Any code that catches MySQL-specific exceptions must be updated to use JDBC standard exceptions.

### 10a. Exception Class Migration

**Before:**
```java
import com.mysql.jdbc.exceptions.jdbc4.CommunicationsException;
import com.mysql.jdbc.exceptions.jdbc4.MySQLIntegrityConstraintViolationException;
import com.mysql.jdbc.exceptions.jdbc4.MySQLSyntaxErrorException;
import com.mysql.jdbc.exceptions.MySQLTimeoutException;

try {
    conn.createStatement().execute(sql);
} catch (CommunicationsException e) {
    // Connection lost
    logger.error("DB connection lost: " + e.getMessage());
} catch (MySQLIntegrityConstraintViolationException e) {
    // Duplicate key / constraint violation
    logger.error("Constraint violation: " + e.getMessage());
} catch (MySQLSyntaxErrorException e) {
    // SQL syntax error
    logger.error("SQL syntax error: " + e.getMessage());
}
```

**After:**
```java
// Use standard JDBC 4.x exception hierarchy — no MySQL-specific imports needed
try {
    conn.createStatement().execute(sql);
} catch (SQLNonTransientConnectionException e) {
    // Connection lost (replaces CommunicationsException)
    logger.error("DB connection lost: " + e.getMessage());
} catch (SQLIntegrityConstraintViolationException e) {
    // Duplicate key / constraint violation
    logger.error("Constraint violation: " + e.getMessage());
} catch (SQLSyntaxErrorException e) {
    // SQL syntax error
    logger.error("SQL syntax error: " + e.getMessage());
} catch (SQLException e) {
    // General fallback for all other SQL errors
    logger.error("SQL error [" + e.getSQLState() + "]: " + e.getMessage());
}
```

### 10b. Checking Error Codes

MySQL and MariaDB share many error codes. The `SQLException.getErrorCode()` and `getSQLState()` values for common errors are compatible:

| Error | MySQL Error Code | MariaDB Error Code | SQLState |
|---|---|---|---|
| Duplicate key | 1062 | 1062 | `23000` |
| Table not found | 1146 | 1146 | `42S02` |
| Access denied | 1045 | 1045 | `28000` |
| Connection refused | — | — | `08001` |
| Deadlock | 1213 | 1213 | `40001` |
| Constraint violation | 1452 | 1452 | `23000` |

---

## 11. SQL Compatibility Changes

MariaDB 10.11 and MySQL 5.5 are broadly SQL-compatible through the JDBC layer, but the following runtime differences may surface.

### 11a. Default `sql_mode`

**MySQL 5.5:** Permissive (effectively empty `sql_mode`)

**MariaDB 10.11:** `STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION`

**Fix — set `sql_mode` at connection time in application code:**
```java
// After obtaining the connection, set a compatible sql_mode
try (Statement st = conn.createStatement()) {
    st.execute("SET SESSION sql_mode = ''");
}
```

Or via connection URL parameter:
```
jdbc:mariadb://localhost:3306/mydb?sessionVariables=sql_mode=''
```

### 11b. Default Character Set

**MySQL 5.5:** Default charset is `latin1`

**MariaDB 10.11:** Default charset is `utf8mb4`

**Fix — set charset explicitly at connection:**
```java
// Preserve MySQL 5.5 behaviour
Properties props = new Properties();
props.setProperty("charset", "latin1");

// Or prefer utf8mb4 if application supports it
props.setProperty("charset", "utf8mb4");
```

Via URL:
```
jdbc:mariadb://localhost:3306/mydb?charset=latin1
```

### 11c. `ONLY_FULL_GROUP_BY`

If SQL queries use non-aggregated columns not in `GROUP BY`, set sql_mode to exclude `ONLY_FULL_GROUP_BY`:

```java
st.execute("SET SESSION sql_mode = 'NO_ENGINE_SUBSTITUTION'");
```

---

## 12. Common Compilation Errors and Fixes

### Error: `cannot find symbol: class com.mysql.jdbc.Driver`

```
[ERROR] cannot find symbol
  symbol:   class Driver
  location: package com.mysql.jdbc
```

**Fix:** The MySQL Connector/J JAR is not on the classpath. Replace the JAR and update the import/reference:
```java
// Before
Class.forName("com.mysql.jdbc.Driver");

// After
Class.forName("org.mariadb.jdbc.Driver");
// Or remove Class.forName() entirely (JDBC 4+ auto-detection)
```

### Error: `cannot find symbol: class MysqlDataSource`

```
[ERROR] cannot find symbol
  symbol:   class MysqlDataSource
  location: package com.mysql.jdbc.jdbc2.optional
```

**Fix:**
```java
// Before
import com.mysql.jdbc.jdbc2.optional.MysqlDataSource;
MysqlDataSource ds = new MysqlDataSource();

// After
import org.mariadb.jdbc.MariaDbDataSource;
MariaDbDataSource ds = new MariaDbDataSource();
```

### Error: `package com.mysql.jdbc does not exist`

```
[ERROR] package com.mysql.jdbc does not exist
[ERROR] package com.mysql.jdbc.jdbc2.optional does not exist
```

**Fix:** The `mysql-connector-java` JAR is missing from the classpath. Update the build classpath:
```bash
# In Makefile:
# Before
CLASSPATH = /usr/share/java/mysql-connector-java.jar

# After
CLASSPATH = /usr/share/java/mariadb-java-client.jar
```
Or update `pom.xml`/`build.gradle` dependency (see Section 1).

### Error: `ClassNotFoundException: com.mysql.jdbc.Driver` (Runtime)

```
java.lang.ClassNotFoundException: com.mysql.jdbc.Driver
```

**Fix:** The `mariadb-java-client` JAR is not on the runtime classpath, or the driver class name was not updated:
```java
// Update driver class name
Class.forName("org.mariadb.jdbc.Driver");
```
And ensure `mariadb-java-client.jar` is on the runtime classpath / in the RPM `Requires`.

### Error: `No suitable driver found for jdbc:mysql://...`

```
java.sql.SQLException: No suitable driver found for jdbc:mysql://localhost:3306/mydb
```

**Cause:** `mariadb-java-client` JAR is on the classpath but the URL uses `jdbc:mysql://`, and JDBC 4+ auto-detection did not register the driver (rare — usually the JAR is simply missing).

**Fix:**
1. Verify `mariadb-java-client.jar` is on the runtime classpath
2. Change URL to `jdbc:mariadb://...`
3. If 1 and 2 don't resolve it, explicitly register the driver:
   ```java
   Class.forName("org.mariadb.jdbc.Driver");
   ```

### Error: `Unknown property 'useSSL'` (Runtime Warning, MariaDB C/J 3.x)

```
WARN: Unknown properties: useSSL
```

**Fix:** Replace `useSSL=false` with `sslMode=disable` in the connection URL (see Section 6).

### Error: `Unknown property 'serverTimezone'` (Runtime Warning, MariaDB C/J 3.x)

```
WARN: Unknown properties: serverTimezone
```

**Fix:** Replace `serverTimezone=UTC` with `timezone=UTC` in the connection URL.

### Error: `Connection refused` after URL migration

```
java.sql.SQLException: Connection refused (ECONNREFUSED)
```

**Cause:** The URL was updated but the hostname, port, or database name is incorrect.

**Fix:** Verify the MariaDB server is running and accepting connections:
```bash
# Inside schroot on Rocky Linux
mysql -h localhost -u dbuser -p mydb -e "SELECT 1;"
```

---

## 13. Migration Checklist

Use this checklist for each TMOS Java module being migrated from MySQL Connector/J 5.1.x to MariaDB Connector/J:

### Build Configuration
- [ ] Replace `mysql:mysql-connector-java` dependency with `org.mariadb.jdbc:mariadb-java-client` in `pom.xml` / `build.gradle`
- [ ] Replace `mysql-connector-java.jar` with `mariadb-java-client.jar` in non-Maven classpath references
- [ ] Replace embedded `lib/mysql-connector-java-*.jar` with `lib/mariadb-java-client-*.jar` if the JAR is vendored in source tree

### RPM Spec File
- [ ] Replace `BuildRequires: mysql-connector-java` with `BuildRequires: mariadb-java-client`
- [ ] Replace `Requires: mysql-connector-java` with `Requires: mariadb-java-client`
- [ ] Update explicit JAR classpath references in `%build` and `%install` sections

### Java Source Code
- [ ] Replace `Class.forName("com.mysql.jdbc.Driver")` or `com.mysql.cj.jdbc.Driver` with `org.mariadb.jdbc.Driver` (or remove `Class.forName()` entirely)
- [ ] Replace `MysqlDataSource` / `MysqlConnectionPoolDataSource` / `MysqlXADataSource` with `MariaDbDataSource` / `MariaDbPoolDataSource`
- [ ] Update all `import com.mysql.*` statements to `import org.mariadb.jdbc.*` or JDBC standard interfaces
- [ ] Replace MySQL-specific exception imports (`CommunicationsException`, `MySQLSyntaxErrorException`, etc.) with standard JDBC exceptions

### Configuration Files
- [ ] Replace `jdbc:mysql://` with `jdbc:mariadb://` in all `.properties`, `.xml`, `.yml`, `.yaml`, `.conf` files
- [ ] Replace `com.mysql.jdbc.Driver` with `org.mariadb.jdbc.Driver` in all driver-class config entries
- [ ] Replace `com.mysql.jdbc.jdbc2.optional.MysqlDataSource` with `org.mariadb.jdbc.MariaDbDataSource` in Spring XML / context.xml
- [ ] Map SSL properties: `useSSL` → `sslMode`, `requireSSL` → `sslMode`, `verifyServerCertificate` → `sslMode` (see Section 6)
- [ ] Map `serverTimezone` → `timezone` (MariaDB C/J 3.x)
- [ ] Remove `autoReconnect=true` — configure connection pool keep-alive instead
- [ ] Remove `allowPublicKeyRetrieval=true` — not applicable to MariaDB
- [ ] Update Hibernate dialect: `MySQLDialect` / `MySQL5InnoDBDialect` → `MariaDB103Dialect` or `MariaDBDialect`

### Build Verification
- [ ] Module compiles without errors
- [ ] No `com.mysql` import references remain in source (`grep -r "com\.mysql" --include="*.java"`)
- [ ] RPM is generated successfully
- [ ] `mariadb-java-client` is listed in RPM `Requires`, not `mysql-connector-java`

### Runtime Verification
- [ ] Application connects successfully to MariaDB 10.11 server
- [ ] All SQL queries execute without `sql_mode` errors
- [ ] Connection pool initializes and health-checks pass
- [ ] No `ClassNotFoundException` or `NoSuitableDriverException` at startup
- [ ] SSL/TLS handshake succeeds (if SSL is used)

---

## 14. TMOS-Specific Patterns

### 14a. Finding MySQL Connector/J References in TMOS Modules

```bash
# Find all Java files importing com.mysql classes
grep -rn "import com\.mysql\." --include="*.java" .

# Find all JDBC URLs in Java source files
grep -rn "jdbc:mysql://" --include="*.java" .

# Find all Class.forName driver registrations
grep -rn "Class\.forName.*mysql\|forName.*com\.mysql" --include="*.java" .

# Find all MySQL DataSource class references in Java
grep -rn "MysqlDataSource\|MysqlConnectionPoolDataSource\|MysqlXADataSource" --include="*.java" .

# Find all configuration files referencing MySQL driver or JDBC URL
grep -rn "com\.mysql\.jdbc\.Driver\|jdbc:mysql://" \
    --include="*.properties" --include="*.xml" --include="*.yml" \
    --include="*.yaml" --include="*.conf" --include="*.cfg" .

# Find spec files with mysql-connector-java BuildRequires/Requires
grep -rn "mysql-connector-java\|mysql-enterprise-java" --include="*.spec" .

# Find Makefiles referencing mysql-connector-java JAR
grep -rn "mysql-connector-java\|mysql\.jar" --include="Makefile*" --include="*.mk" .
```

### 14b. Verifying MariaDB Java Client on Rocky Linux 8.10

```bash
# Check available MariaDB Java packages
dnf list mariadb-java-client 2>/dev/null

# Install (if needed during development/build)
sudo dnf install mariadb-java-client

# Verify installation
rpm -q mariadb-java-client
rpm -ql mariadb-java-client | grep "\.jar"

# Check JAR path
ls -lh /usr/share/java/mariadb-java-client.jar

# Verify JAR contains the MariaDB driver
jar -tf /usr/share/java/mariadb-java-client.jar | grep "Driver.class"
```

### 14c. Testing the Driver Connection Inside schroot

```bash
# Enter Rocky Linux schroot
schroot -c rocky8.1064

# Test MariaDB Java connection with a minimal test class
cat > /tmp/TestMariaDBConn.java << 'EOF'
import java.sql.*;

public class TestMariaDBConn {
    public static void main(String[] args) throws Exception {
        String url = "jdbc:mariadb://localhost:3306/testdb?sslMode=disable";
        try (Connection c = DriverManager.getConnection(url, "user", "pass");
             Statement s = c.createStatement();
             ResultSet rs = s.executeQuery("SELECT VERSION()")) {
            if (rs.next()) System.out.println("MariaDB version: " + rs.getString(1));
        }
    }
}
EOF

javac -cp /usr/share/java/mariadb-java-client.jar /tmp/TestMariaDBConn.java -d /tmp
java -cp /tmp:/usr/share/java/mariadb-java-client.jar TestMariaDBConn
```

### 14d. Module Definition Lookup for Java Modules

To identify TMOS Java modules that depend on MySQL Connector/J:

```bash
# Search for modules with mysql-connector-java or mysql-enterprise-java in depends
grep -l "mysql-connector-java\|mysql-enterprise-java" *.def.inc

# Extract module entry and check depends field
grep -A 30 "^entry <module_name>" *.def.inc | grep -i "dep\|mysql\|java"
```

### 14e. Checklist for Modules That Bundle the JDBC JAR in Source

Some TMOS modules embed the JDBC JAR directly in the source tree (e.g., under `lib/` or `3rdparty/`) rather than depending on a system package. For these modules:

1. **Identify the bundled JAR:**
   ```bash
   find . -name "mysql-connector-java*.jar" -o -name "mysql*.jar" 2>/dev/null
   ```

2. **Open for edit and replace:**
   ```bash
   p4 edit lib/mysql-connector-java-5.1.49.jar
   # Copy the new JAR from Maven cache or /usr/share/java/
   cp /usr/share/java/mariadb-java-client.jar lib/mariadb-java-client-3.3.3.jar
   p4 add lib/mariadb-java-client-3.3.3.jar
   ```

3. **Update all classpath references** in `Makefile`, build scripts, and spec file to point to the new JAR name.

4. **Mark the old JAR for deletion** only after the build succeeds and user confirms:
   ```bash
   # Only after successful build and user approval:
   p4 delete lib/mysql-connector-java-5.1.49.jar
   ```

---

## 15. References

- **MariaDB Connector/J 3.x Documentation:** https://mariadb.com/kb/en/mariadb-connector-j/
- **MariaDB Connector/J 2.7.x Release Notes:** https://mariadb.com/kb/en/mariadb-connector-j-2-7-release-notes/
- **MySQL Connector/J 5.1.x → MariaDB Migration:** https://mariadb.com/kb/en/migrating-to-mariadb-from-mysql/
- **Rocky Linux 8.10 AppStream packages:** `dnf info mariadb-java-client`
- **Related skill file:** `ai-agents/projects/centos2rocky/skills/mysql-mariadb-migration.SKILL.md` — covers C/C++ client migration
- **Related skill file:** `ai-agents/projects/centos2rocky/skills/java-migration-jdk21.SKILL.md` — covers Java JDK 21 migration
