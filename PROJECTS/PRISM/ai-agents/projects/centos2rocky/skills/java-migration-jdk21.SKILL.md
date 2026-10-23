---
name: java-migration-jdk21
description: Domain knowledge for migrating Java applications from JDK 1.8.0 to JDK 21.x. Covers module system, removed features, language enhancements, API changes, and migration best practices.
applyTo: ["**/*.java", "**/pom.xml", "**/build.gradle", "**/build.gradle.kts", "**/*.properties", "**/MANIFEST.MF"]
---

# Java Migration Guide: JDK 1.8.0 → JDK 21.x

This skill provides comprehensive guidance for migrating Java applications from JDK 1.8.0 (Java SE 8) to JDK 21.x (Java SE 21 LTS), covering major changes, removed features, new language constructs, and migration strategies.

## Overview of Java Version Changes

### Major Releases Covered (8 → 21)
- **Java 8 (LTS)** - March 2014 - Starting point
- **Java 9** - September 2017 - Module system, jshell
- **Java 10** - March 2018 - Local variable type inference (var)
- **Java 11 (LTS)** - September 2018 - HTTP Client API, removed Java EE
- **Java 12-16** - Non-LTS releases with incremental features
- **Java 17 (LTS)** - September 2021 - Sealed classes, pattern matching
- **Java 18-20** - Non-LTS releases
- **Java 21 (LTS)** - September 2023 - Virtual threads, pattern matching for switch

### Long Term Support (LTS) Versions
- Java 8 (2014) - Extended support until 2030
- Java 11 (2018) - LTS, widely adopted
- Java 17 (2021) - LTS, recommended migration target
- **Java 21 (2023)** - Latest LTS, target for this migration

## Critical Breaking Changes

### 1. Module System (Java 9+)

**Most Significant Change:** Introduction of Java Platform Module System (JPMS)

**Impact:**
```java
// Java 8 - No module system
// All classes accessible from classpath

// Java 9+ - Module system
// Requires module-info.java
module com.mycompany.myapp {
    requires java.sql;
    requires java.xml;
    exports com.mycompany.myapp.api;
    opens com.mycompany.myapp.internal to com.fasterxml.jackson.databind;
}
```

**Migration Options:**

**Option 1: Unnamed Module (easiest for migration)**
```bash
# Run as unnamed module (no module-info.java needed)
java -classpath app.jar:lib/* com.mycompany.Main

# Add exports if needed
java --add-exports java.base/sun.nio.ch=ALL-UNNAMED \
     -cp app.jar:lib/* com.mycompany.Main
```

**Option 2: Automatic Modules (JAR on module-path)**
```bash
# Place JARs on module-path instead of classpath
java --module-path lib --add-modules ALL-MODULE-PATH \
     -jar app.jar
```

**Option 3: Full Modularization (recommended for new development)**
```java
// src/main/java/module-info.java
module com.mycompany.myapp {
    requires java.logging;
    requires java.sql;
    requires com.fasterxml.jackson.databind;
    
    exports com.mycompany.myapp.api;
    opens com.mycompany.myapp.model to com.fasterxml.jackson.databind;
}
```

### 2. Removed Java EE and CORBA Modules (Java 11+)

**Removed from JDK (require separate dependencies):**

```xml
<!-- Java 8 - Included in JDK -->
import javax.xml.bind.*;        // JAXB
import javax.xml.ws.*;          // JAX-WS
import javax.activation.*;      // JAF
import javax.annotation.*;      // Common Annotations
import javax.transaction.*;     // JTA

<!-- Java 11+ - Must add as dependencies -->
<dependencies>
    <!-- JAXB -->
    <dependency>
        <groupId>javax.xml.bind</groupId>
        <artifactId>jaxb-api</artifactId>
        <version>2.3.1</version>
    </dependency>
    <dependency>
        <groupId>org.glassfish.jaxb</groupId>
        <artifactId>jaxb-runtime</artifactId>
        <version>2.3.1</version>
    </dependency>
    
    <!-- JAX-WS -->
    <dependency>
        <groupId>javax.xml.ws</groupId>
        <artifactId>jaxws-api</artifactId>
        <version>2.3.1</version>
    </dependency>
    
    <!-- Annotations -->
    <dependency>
        <groupId>javax.annotation</groupId>
        <artifactId>javax.annotation-api</artifactId>
        <version>1.3.2</version>
    </dependency>
</dependencies>
```

**Gradle equivalent:**
```groovy
dependencies {
    implementation 'javax.xml.bind:jaxb-api:2.3.1'
    implementation 'org.glassfish.jaxb:jaxb-runtime:2.3.1'
    implementation 'javax.xml.ws:jaxws-api:2.3.1'
    implementation 'javax.annotation:javax.annotation-api:1.3.2'
}
```

### 3. Removed Features

**Completely Removed:**

**Java 9+:**
- **Applets** - Java Plugin and Applet API removed
- **Java Web Start (JNLP)** - Removed entirely
- **JavaFX** - Separated from JDK (available as separate module)

**Java 11+:**
- **CORBA** - Common Object Request Broker Architecture
- **Java EE modules** - JAXB, JAX-WS, JAF, Common Annotations
- **Nashorn JavaScript Engine** - Deprecated in 11, removed in 15

**Java 14+:**
- **CMS Garbage Collector** - Removed
- **ParallelScavenge + SerialOld GC combination** - Removed

**What to do:**
```java
// If using removed features:
// 1. CORBA - Migrate to modern RPC (gRPC, REST)
// 2. Nashorn - Use GraalVM JavaScript or migrate to Node.js
// 3. JavaFX - Add as external dependency
// 4. Applets - Rewrite as web applications
```

### 4. Internal API Access Restrictions

**Java 8 - Unrestricted access:**
```java
// Could access internal APIs
import sun.misc.Unsafe;
import sun.nio.ch.DirectBuffer;
import com.sun.org.apache.xml.internal.*;

Unsafe unsafe = Unsafe.getUnsafe(); // Worked in Java 8
```

**Java 9+ - Restricted:**
```java
// Strongly encapsulated, generates warnings/errors
import sun.misc.Unsafe; // WARNING in 9-15, ERROR in 16+

// Must use --add-exports or --add-opens
java --add-exports java.base/sun.misc=ALL-UNNAMED \
     --add-opens java.base/java.lang=ALL-UNNAMED \
     -jar app.jar
```

**Better Solution - Use Standard APIs:**
```java
// Java 9+ - Use MethodHandles.Lookup
import java.lang.invoke.MethodHandles;
import java.lang.invoke.VarHandle;

// Use VarHandle instead of Unsafe for memory operations
VarHandle vh = MethodHandles.lookup()
    .findVarHandle(MyClass.class, "field", int.class);
```

### 5. Changed Default Garbage Collector

**Java 8:**
- Default: Parallel GC on server, Serial GC on client

**Java 9-13:**
- Default: G1GC (Garbage First)

**Java 14+:**
- Default: G1GC
- New options: ZGC (experimental in 11, production in 15)
- New options: Shenandoah GC (experimental in 12)

**Migration impact:**
```bash
# Java 8 tuning flags may not apply
# Old flags
-XX:+UseConcMarkSweepGC  # CMS removed in Java 14

# New GC options
-XX:+UseG1GC              # Default, explicit
-XX:+UseZGC               # Low latency GC (Java 15+)
-XX:+UseShenandoahGC      # Low pause GC (OpenJDK)
```

### 6. Runtime Parameter Changes

**Removed/Changed JVM Flags:**

```bash
# Removed in Java 9+
-XX:+UseGCLogFileRotation       # Use -Xlog instead
-XX:MaxPermSize                  # PermGen removed, use MetaSpace
-XX:PermSize                     # PermGen removed

# New Unified Logging (Java 9+)
# Old
-XX:+PrintGC -XX:+PrintGCDetails

# New
-Xlog:gc*:file=gc.log:time,level,tags

# G1GC tuning (Java 8 vs 9+)
# Java 8
-XX:+UseG1GC -XX:MaxGCPauseMillis=200

# Java 9+
-XX:+UseG1GC -XX:MaxGCPauseMillis=200 -XX:G1HeapRegionSize=16M
```

## Language Enhancements (Java 9-21)

### 1. Local Variable Type Inference - var (Java 10+)

**Java 8:**
```java
List<String> list = new ArrayList<>();
Map<String, List<Integer>> map = new HashMap<>();
```

**Java 10+:**
```java
var list = new ArrayList<String>();  // Type inferred
var map = new HashMap<String, List<Integer>>();

// Works in loops
for (var entry : map.entrySet()) {
    var key = entry.getKey();
    var value = entry.getValue();
}

// Cannot use for fields, parameters, or return types
// var field = "test";  // ERROR
```

### 2. Switch Expressions (Java 14+)

**Java 8:**
```java
String result;
switch (day) {
    case MONDAY:
    case FRIDAY:
    case SUNDAY:
        result = "6 letters";
        break;
    case TUESDAY:
        result = "7 letters";
        break;
    default:
        result = "Other";
        break;
}
```

**Java 14+:**
```java
// Switch expression with arrow syntax
String result = switch (day) {
    case MONDAY, FRIDAY, SUNDAY -> "6 letters";
    case TUESDAY -> "7 letters";
    default -> "Other";
};

// With yield for complex cases
String result = switch (day) {
    case MONDAY, FRIDAY, SUNDAY -> {
        System.out.println("Weekend or start of week");
        yield "6 letters";
    }
    case TUESDAY -> "7 letters";
    default -> "Other";
};
```

### 3. Text Blocks (Java 15+)

**Java 8:**
```java
String json = "{\n" +
              "  \"name\": \"John\",\n" +
              "  \"age\": 30\n" +
              "}";

String html = "<html>\n" +
              "  <body>\n" +
              "    <p>Hello</p>\n" +
              "  </body>\n" +
              "</html>";
```

**Java 15+:**
```java
String json = """
    {
      "name": "John",
      "age": 30
    }
    """;

String html = """
    <html>
      <body>
        <p>Hello</p>
      </body>
    </html>
    """;
```

### 4. Records (Java 16+)

**Java 8:**
```java
public final class Point {
    private final int x;
    private final int y;
    
    public Point(int x, int y) {
        this.x = x;
        this.y = y;
    }
    
    public int x() { return x; }
    public int y() { return y; }
    
    @Override
    public boolean equals(Object obj) {
        if (!(obj instanceof Point)) return false;
        Point other = (Point) obj;
        return x == other.x && y == other.y;
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(x, y);
    }
    
    @Override
    public String toString() {
        return "Point[x=" + x + ", y=" + y + "]";
    }
}
```

**Java 16+:**
```java
// Equivalent record - much shorter!
public record Point(int x, int y) {
    // Automatically generates:
    // - Constructor
    // - Getters (x(), y())
    // - equals(), hashCode(), toString()
}

// Can add custom methods and validation
public record Point(int x, int y) {
    public Point {  // Compact constructor
        if (x < 0 || y < 0) {
            throw new IllegalArgumentException("Negative coordinates");
        }
    }
    
    public double distance() {
        return Math.sqrt(x * x + y * y);
    }
}
```

### 5. Sealed Classes (Java 17+)

**Java 8:**
```java
// No way to restrict subclasses except final
public abstract class Shape {
    // Any class can extend
}
```

**Java 17+:**
```java
// Restrict which classes can extend
public sealed class Shape 
    permits Circle, Rectangle, Triangle {
    // Only these three can extend Shape
}

public final class Circle extends Shape {
    // Must be final, sealed, or non-sealed
}

public final class Rectangle extends Shape {
}

public non-sealed class Triangle extends Shape {
    // Allows further extension
}
```

### 6. Pattern Matching for instanceof (Java 16+)

**Java 8:**
```java
if (obj instanceof String) {
    String str = (String) obj;
    System.out.println(str.length());
}
```

**Java 16+:**
```java
// Pattern matching with type pattern
if (obj instanceof String str) {
    System.out.println(str.length());  // str already cast
}

// In complex conditions
if (obj instanceof String str && str.length() > 5) {
    System.out.println(str.toUpperCase());
}
```

### 7. Pattern Matching for switch (Java 21+)

**Java 8:**
```java
String formatted;
if (obj instanceof Integer) {
    formatted = String.format("int %d", (Integer) obj);
} else if (obj instanceof Long) {
    formatted = String.format("long %d", (Long) obj);
} else if (obj instanceof Double) {
    formatted = String.format("double %f", (Double) obj);
} else {
    formatted = obj.toString();
}
```

**Java 21+:**
```java
String formatted = switch (obj) {
    case Integer i -> String.format("int %d", i);
    case Long l    -> String.format("long %d", l);
    case Double d  -> String.format("double %f", d);
    case String s  -> String.format("String %s", s);
    case null      -> "null";
    default        -> obj.toString();
};

// With guards
String result = switch (obj) {
    case String s when s.length() > 5 -> "Long string";
    case String s -> "Short string";
    default -> "Not a string";
};
```

### 8. Virtual Threads (Java 21+)

**Java 8 - Platform Threads:**
```java
// Expensive platform threads
ExecutorService executor = Executors.newFixedThreadPool(100);
for (int i = 0; i < 10000; i++) {
    executor.submit(() -> {
        // Task
    });
}
```

**Java 21+ - Virtual Threads:**
```java
// Lightweight virtual threads
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 1_000_000; i++) {  // Can create millions!
        executor.submit(() -> {
            // Task
        });
    }
}

// Start virtual thread directly
Thread.startVirtualThread(() -> {
    System.out.println("Running in virtual thread");
});

// Thread builder
Thread thread = Thread.ofVirtual()
    .name("my-virtual-thread")
    .start(() -> System.out.println("Hello"));
```

## API Changes and Enhancements

### 1. Stream API Enhancements

**Java 9+ additions:**
```java
// takeWhile, dropWhile (Java 9)
List<Integer> numbers = List.of(1, 2, 3, 4, 5, 6);
numbers.stream()
    .takeWhile(n -> n < 4)
    .forEach(System.out::println);  // 1, 2, 3

// iterate with predicate (Java 9)
Stream.iterate(1, n -> n < 100, n -> n * 2)
    .forEach(System.out::println);  // 1, 2, 4, 8, 16, 32, 64

// ofNullable (Java 9)
Stream.ofNullable(getValue())  // Empty stream if null
    .forEach(System.out::println);

// toList() (Java 16)
List<String> list = stream.toList();  // Immutable list

// mapMulti (Java 16)
Stream.of(1, 2, 3)
    .mapMulti((num, consumer) -> {
        consumer.accept(num);
        consumer.accept(num * 2);
    })
    .forEach(System.out::println);  // 1, 2, 2, 4, 3, 6
```

### 2. Collection Factory Methods (Java 9+)

**Java 8:**
```java
List<String> list = Arrays.asList("a", "b", "c");
Set<String> set = new HashSet<>(Arrays.asList("a", "b"));
Map<String, Integer> map = new HashMap<>();
map.put("a", 1);
map.put("b", 2);
```

**Java 9+:**
```java
// Immutable collections
List<String> list = List.of("a", "b", "c");
Set<String> set = Set.of("a", "b", "c");
Map<String, Integer> map = Map.of("a", 1, "b", 2, "c", 3);

// Map with more entries
Map<String, Integer> map = Map.ofEntries(
    Map.entry("a", 1),
    Map.entry("b", 2),
    Map.entry("c", 3)
);
```

### 3. Optional Enhancements

**Java 9+ additions:**
```java
Optional<String> opt = Optional.of("value");

// ifPresentOrElse (Java 9)
opt.ifPresentOrElse(
    value -> System.out.println(value),
    () -> System.out.println("Empty")
);

// or (Java 9)
Optional<String> result = opt.or(() -> Optional.of("default"));

// stream (Java 9)
opt.stream()
    .map(String::toUpperCase)
    .forEach(System.out::println);

// isEmpty (Java 11)
if (opt.isEmpty()) {
    System.out.println("Empty");
}
```

### 4. String Methods

**Java 11+ additions:**
```java
String str = "  Hello World  ";

// isBlank (Java 11)
boolean blank = str.isBlank();  // false
"   ".isBlank();  // true

// lines (Java 11)
"Line1\nLine2\nLine3".lines()
    .forEach(System.out::println);

// strip, stripLeading, stripTrailing (Java 11)
// Better than trim() - handles Unicode whitespace
String stripped = str.strip();

// repeat (Java 11)
String repeated = "-".repeat(10);  // "----------"

// indent (Java 12)
String indented = "Hello".indent(4);  // "    Hello\n"

// transform (Java 12)
String result = "hello".transform(String::toUpperCase);

// formatted (Java 15)
String msg = "Hello %s".formatted("World");
```

### 5. Files API Improvements

**Java 11+ additions:**
```java
// readString, writeString (Java 11)
String content = Files.readString(Path.of("file.txt"));
Files.writeString(Path.of("file.txt"), "Hello World");

// mismatch (Java 12)
long pos = Files.mismatch(path1, path2);  // First different byte position
```

### 6. HTTP Client (Java 11+)

**Java 8 - HttpURLConnection:**
```java
URL url = new URL("https://api.example.com/data");
HttpURLConnection conn = (HttpURLConnection) url.openConnection();
conn.setRequestMethod("GET");

BufferedReader in = new BufferedReader(
    new InputStreamReader(conn.getInputStream()));
String inputLine;
StringBuilder response = new StringBuilder();
while ((inputLine = in.readLine()) != null) {
    response.append(inputLine);
}
in.close();
```

**Java 11+ - HttpClient:**
```java
HttpClient client = HttpClient.newHttpClient();
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/data"))
    .GET()
    .build();

// Synchronous
HttpResponse<String> response = client.send(request, 
    HttpResponse.BodyHandlers.ofString());
System.out.println(response.body());

// Asynchronous
client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
    .thenApply(HttpResponse::body)
    .thenAccept(System.out::println)
    .join();
```

## Migration Strategy

### Phase 1: Assessment

**Step 1: Identify Java 8 Dependencies**
```bash
# Check for removed Java EE dependencies
grep -r "javax.xml.bind\|javax.xml.ws\|javax.activation" src/

# Check for internal API usage
grep -r "sun\.\|com\.sun\." src/

# Check for removed features
grep -r "Applet\|CORBA\|Nashorn" src/
```

**Step 2: Build Tool Compatibility**
```xml
<!-- Maven - Update to support Java 21 -->
<properties>
    <maven.compiler.source>21</maven.compiler.source>
    <maven.compiler.target>21</maven.compiler.target>
    <maven.compiler.release>21</maven.compiler.release>
</properties>

<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.11.0</version>
        </plugin>
    </plugins>
</build>
```

```groovy
// Gradle - Update to support Java 21
plugins {
    id 'java'
}

java {
    sourceCompatibility = JavaVersion.VERSION_21
    targetCompatibility = JavaVersion.VERSION_21
}

// Or using toolchain
java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}
```

### Phase 2: Incremental Migration Approach

**Option 1: Compile with Java 21, Target Java 8 Bytecode**
```xml
<!-- Compile with Java 21, produce Java 8 bytecode -->
<properties>
    <maven.compiler.source>8</maven.compiler.source>
    <maven.compiler.target>8</maven.compiler.target>
</properties>
```

**Option 2: Multi-Release JAR (Java 9+)**
```
myapp.jar
├── META-INF
│   ├── MANIFEST.MF (Multi-Release: true)
│   └── versions
│       ├── 9
│       │   └── com/myapp/JavaSpecificClass.class
│       ├── 11
│       │   └── com/myapp/JavaSpecificClass.class
│       └── 21
│           └── com/myapp/JavaSpecificClass.class
└── com
    └── myapp
        └── Main.class
```

### Phase 3: Dependency Updates

**Common dependencies needing updates:**

```xml
<dependencies>
    <!-- Add Java EE dependencies if removed -->
    <dependency>
        <groupId>jakarta.xml.bind</groupId>
        <artifactId>jakarta.xml.bind-api</artifactId>
        <version>4.0.0</version>
    </dependency>
    
    <!-- Update testing frameworks -->
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter</artifactId>
        <version>5.10.0</version>
        <scope>test</scope>
    </dependency>
    
    <!-- Update logging -->
    <dependency>
        <groupId>org.slf4j</groupId>
        <artifactId>slf4j-api</artifactId>
        <version>2.0.9</version>
    </dependency>
    
    <!-- Update frameworks -->
    <!-- Spring Boot 3.x requires Java 17+ -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter</artifactId>
        <version>3.1.5</version>
    </dependency>
</dependencies>
```

## Common Migration Patterns

### Pattern 1: Replace Java EE Dependencies

**Before:**
```java
import javax.xml.bind.JAXBContext;
import javax.xml.bind.Marshaller;

JAXBContext context = JAXBContext.newInstance(MyClass.class);
Marshaller marshaller = context.createMarshaller();
```

**After (add Jakarta EE dependencies):**
```xml
<dependency>
    <groupId>jakarta.xml.bind</groupId>
    <artifactId>jakarta.xml.bind-api</artifactId>
    <version>4.0.0</version>
</dependency>
<dependency>
    <groupId>org.glassfish.jaxb</groupId>
    <artifactId>jaxb-runtime</artifactId>
    <version>4.0.0</version>
</dependency>
```

```java
// Code stays the same, but uses jakarta.xml.bind
import jakarta.xml.bind.JAXBContext;
import jakarta.xml.bind.Marshaller;
```

### Pattern 2: Handle Internal API Usage

**Before:**
```java
import sun.misc.BASE64Encoder;
import sun.misc.BASE64Decoder;

BASE64Encoder encoder = new BASE64Encoder();
String encoded = encoder.encode(bytes);
```

**After:**
```java
import java.util.Base64;

String encoded = Base64.getEncoder().encodeToString(bytes);
byte[] decoded = Base64.getDecoder().decode(encoded);
```

### Pattern 3: Update Date/Time Usage

**Before (Java 8 still supports but deprecated):**
```java
Date date = new Date();
SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
String formatted = sdf.format(date);
```

**After (use java.time):**
```java
LocalDate date = LocalDate.now();
String formatted = date.format(DateTimeFormatter.ISO_LOCAL_DATE);

// With time
LocalDateTime dateTime = LocalDateTime.now();
String formatted = dateTime.format(
    DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));
```

### Pattern 4: Modernize Loops and Streams

**Before:**
```java
List<String> filtered = new ArrayList<>();
for (String item : list) {
    if (item.startsWith("A")) {
        filtered.add(item.toUpperCase());
    }
}
```

**After:**
```java
List<String> filtered = list.stream()
    .filter(item -> item.startsWith("A"))
    .map(String::toUpperCase)
    .toList();  // Java 16+, or .collect(Collectors.toList())
```

### Pattern 5: Use Records for DTOs

**Before:**
```java
public class UserDTO {
    private final String username;
    private final String email;
    
    public UserDTO(String username, String email) {
        this.username = username;
        this.email = email;
    }
    
    // getters, equals, hashCode, toString...
}
```

**After (Java 16+):**
```java
public record UserDTO(String username, String email) {
    // Automatic constructor, getters, equals, hashCode, toString
}
```

## Testing Strategy

### 1. Compile-Time Testing

```bash
# Compile with Java 21
javac --release 21 *.java

# Run with specific module exports if needed
javac --add-exports java.base/sun.nio.ch=ALL-UNNAMED \
      --release 21 *.java
```

### 2. Runtime Testing

```bash
# Run application
java -jar myapp.jar

# With module system debugging
java --show-module-resolution -jar myapp.jar

# List dependencies
jdeps myapp.jar

# Check for removed/internal API usage
jdeps --jdk-internals myapp.jar
```

### 3. Performance Testing

```bash
# Profile with Flight Recorder
java -XX:StartFlightRecording=filename=recording.jfr \
     -jar myapp.jar

# Analyze GC performance
java -Xlog:gc*:file=gc.log -jar myapp.jar
```

## Common Pitfalls

### Pitfall 1: Reflection with Modules

**Problem:**
```java
// May fail with modules
Class<?> clazz = Class.forName("com.internal.MyClass");
Method method = clazz.getDeclaredMethod("privateMethod");
method.setAccessible(true);  // May throw exception
```

**Solution:**
```bash
# Add --add-opens if absolutely necessary
java --add-opens java.base/java.lang=ALL-UNNAMED \
     -jar myapp.jar
```

### Pitfall 2: ClassLoader Hierarchy Changes

**Problem:**
Extensions classloader removed, may affect custom classloading.

**Solution:**
Review and update custom classloader implementations.

### Pitfall 3: Removed Tools

**Problem:**
```bash
# These tools are removed
jhat    # Removed in Java 9
javah   # Removed in Java 10 (use javac -h)
```

**Solution:**
Use modern alternatives (jconsole, VisualVM, javac -h).

## Performance Considerations

### Garbage Collection

**G1GC Tuning (Java 21):**
```bash
-XX:+UseG1GC
-XX:MaxGCPauseMillis=200
-XX:G1HeapRegionSize=16M
-XX:InitiatingHeapOccupancyPercent=45
```

**ZGC (Low Latency):**
```bash
-XX:+UseZGC
-XX:ZAllocationSpikeTolerance=5
```

### Virtual Threads (Java 21)

Consider converting to virtual threads for I/O-bound applications:
```java
// Can handle millions of concurrent requests
Executors.newVirtualThreadPerTaskExecutor()
```

## Migration Checklist

### Phase 1: Preparation
- [ ] Audit current Java 8 codebase
- [ ] Identify removed Java EE dependencies
- [ ] Check for internal API usage (sun.*, com.sun.*)
- [ ] Review third-party library compatibility
- [ ] Update build tools (Maven 3.8+, Gradle 8+)
- [ ] Set up Java 21 development environment

### Phase 2: Code Updates
- [ ] Add Java EE dependencies if needed
- [ ] Replace internal API usage with standard APIs
- [ ] Update deprecated API calls
- [ ] Fix compilation errors
- [ ] Update JVM parameters
- [ ] Remove obsolete GC flags

### Phase 3: Modernization (Optional)
- [ ] Consider using records for data classes
- [ ] Convert switch statements to switch expressions
- [ ] Use text blocks for multi-line strings
- [ ] Apply pattern matching where appropriate
- [ ] Consider virtual threads for I/O-bound code

### Phase 4: Testing
- [ ] Run full test suite
- [ ] Performance testing with new GC
- [ ] Memory profiling
- [ ] Monitor for module-related issues
- [ ] Test reflection and serialization
- [ ] Integration testing

### Phase 5: Deployment
- [ ] Update deployment scripts for Java 21
- [ ] Configure JVM parameters for production
- [ ] Monitor application metrics
- [ ] Plan rollback procedure
- [ ] Document Java 21-specific configurations

## Useful Tools

### Analysis Tools
```bash
# Find internal API usage
jdeps --jdk-internals myapp.jar

# Analyze module dependencies
jdeps --module-path lib --analyze-module-path myapp.jar

# List suggested --add-modules
jdeps --suggest-providers 'java.sql.*' myapp.jar
```

### Migration Tools
```bash
# Compile with Java 21, target Java 8
javac --source 8 --target 8 --release 8 MyClass.java

# Show module resolution
java --show-module-resolution -jar myapp.jar

# Dry run module resolution
java --dry-run --class-path app.jar Main
```

## Additional Resources

- Java SE 21 Documentation: https://docs.oracle.com/en/java/javase/21/
- Java Version Almanac: https://javaalmanac.io/
- Migration Guide (Oracle): https://docs.oracle.com/en/java/javase/21/migrate/
- OpenJDK JEPs: https://openjdk.org/jeps/0
- Inside Java: https://inside.java/

## Summary

Key migration points for Java 8 → Java 21:

1. **Module System**: Understand JPMS, use unnamed module for gradual migration
2. **Removed Features**: Add Java EE dependencies separately, migrate from removed APIs
3. **Internal APIs**: Replace sun.* and com.sun.* usage with standard APIs
4. **Build Tools**: Update Maven/Gradle to support Java 21
5. **GC Changes**: Review and update GC configuration
6. **Language Features**: Optionally adopt records, switch expressions, text blocks
7. **Virtual Threads**: Consider for concurrent I/O-bound applications
8. **Testing**: Comprehensive testing with jdeps and runtime validation
9. **Dependencies**: Update all third-party libraries to Java 21-compatible versions
10. **Performance**: Take advantage of G1GC or ZGC improvements

Migration from Java 8 to Java 21 is substantial but provides significant benefits: better performance, modern language features, improved security, and long-term support. Plan for incremental migration and thorough testing.
