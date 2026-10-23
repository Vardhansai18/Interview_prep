---
name: 32bit-to-64bit-migration
description: Domain knowledge for migrating applications from 32-bit to 64-bit architecture. Covers data type changes, pointer size issues, memory alignment, calling conventions, and platform-specific considerations for x86/x86_64 and ARM/AArch64 migrations.
applyTo: ["**/*.c", "**/*.cpp", "**/*.cc", "**/*.cxx", "**/*.h", "**/*.hpp", "**/Makefile*", "**/*.mk", "**/*.spec", "**/configure.ac", "**/CMakeLists.txt"]
---

# 32-bit to 64-bit Migration Guide

This skill provides comprehensive guidance for migrating applications from 32-bit to 64-bit architecture, covering critical data type changes, pointer handling, memory alignment, and platform-specific considerations.

## Overview of 32-bit vs 64-bit Differences

### Key Architectural Changes

**32-bit Architecture:**
- **Pointer size**: 4 bytes (32 bits)
- **Address space**: 4 GB maximum (2^32)
- **Register size**: 32-bit general-purpose registers
- **int size**: Typically 4 bytes
- **long size**: 4 bytes on most platforms

**64-bit Architecture:**
- **Pointer size**: 8 bytes (64 bits)
- **Address space**: 16 EB theoretical (2^64), practically much less
- **Register size**: 64-bit general-purpose registers
- **int size**: Still 4 bytes (unchanged)
- **long size**: 8 bytes on Unix/Linux, 4 bytes on Windows (LLP64)

### Data Model Differences

**ILP32 (32-bit)**: int, long, and pointer are 32-bit
```
int:      4 bytes
long:     4 bytes
pointer:  4 bytes
size_t:   4 bytes
```

**LP64 (64-bit Unix/Linux)**: long and pointer are 64-bit
```
int:      4 bytes
long:     8 bytes
pointer:  8 bytes
size_t:   8 bytes
```

**LLP64 (64-bit Windows)**: long-long and pointer are 64-bit
```
int:      4 bytes
long:     4 bytes (differs from LP64!)
long long: 8 bytes
pointer:  8 bytes
size_t:   8 bytes
```

## Critical Breaking Changes

### 1. Pointer and Integer Size Mismatch

**Most Critical Issue**: Pointers are 8 bytes in 64-bit, but `int` remains 4 bytes.

**Problem Code (32-bit):**
```c
// BAD - Assumes pointer fits in int
void *ptr = malloc(100);
int ptr_as_int = (int)ptr;           // TRUNCATION on 64-bit!
void *restored = (void *)ptr_as_int; // WRONG pointer!

// BAD - Pointer arithmetic with int
int offset = calculate_offset();
char *new_ptr = base_ptr + offset;   // May overflow if offset > 2GB

// BAD - Storing pointer in int array
int handles[10];
handles[0] = (int)malloc(100);       // TRUNCATION!
```

**Correct Code (64-bit compatible):**
```c
// GOOD - Use intptr_t/uintptr_t for pointer storage
void *ptr = malloc(100);
intptr_t ptr_as_int = (intptr_t)ptr;     // Safe conversion
void *restored = (void *)ptr_as_int;      // Correct restoration

// GOOD - Use ptrdiff_t for pointer arithmetic
ptrdiff_t offset = calculate_offset();
char *new_ptr = base_ptr + offset;

// GOOD - Use pointer array or intptr_t
intptr_t handles[10];
handles[0] = (intptr_t)malloc(100);

// Or better - use proper pointer array
void *ptr_handles[10];
ptr_handles[0] = malloc(100);
```

### 2. size_t and Integer Conversions

**Problem: size_t is 8 bytes on 64-bit, can overflow int**

**Problem Code:**
```c
// BAD - size_t truncated to int
size_t large_size = 5000000000ULL;  // 5 GB
int size_int = large_size;           // OVERFLOW! Negative value
char *buffer = malloc(size_int);     // Wrong allocation size!

// BAD - Loop with int for size_t
size_t count = get_large_count();
for (int i = 0; i < count; i++) {    // OVERFLOW if count > INT_MAX
    process(array[i]);
}

// BAD - Unsigned/signed mismatch
size_t size = strlen(str);
int result = size - 10;              // Can be negative, but size_t is unsigned
if (result < 0) {                    // Comparison never true if result is size_t!
    // ...
}
```

**Correct Code:**
```c
// GOOD - Use size_t throughout
size_t large_size = 5000000000ULL;
char *buffer = malloc(large_size);

// GOOD - Use size_t for loop index
size_t count = get_large_count();
for (size_t i = 0; i < count; i++) {
    process(array[i]);
}

// GOOD - Proper signed arithmetic
size_t size = strlen(str);
ptrdiff_t result = (ptrdiff_t)size - 10;
if (result < 0) {
    // Correctly handles negative values
}

// Or check before subtraction
if (size >= 10) {
    size_t result = size - 10;
}
```

### 3. Structure Packing and Alignment

**64-bit has stricter alignment requirements**

**Problem Code (32-bit):**
```c
// Naturally aligned in 32-bit
struct BadAlign32 {
    char c;        // 1 byte
    int i;         // 4 bytes, aligned to 4-byte boundary
    char c2;       // 1 byte
    void *ptr;     // 4 bytes in 32-bit
};
// Size in 32-bit: 16 bytes (with padding)

// But in 64-bit:
// Size in 64-bit: 24 bytes! (8-byte pointer alignment)
```

**Correct Approach:**
```c
// GOOD - Explicit packing awareness
struct GoodAlign {
    char c;        // 1 byte
    char c2;       // 1 byte
    // 2 bytes padding
    int i;         // 4 bytes
    void *ptr;     // 8 bytes in 64-bit
};
// Size in 64-bit: 16 bytes (optimized layout)

// If exact layout needed, use explicit packing
#pragma pack(push, 1)
struct Packed {
    char c;
    int i;
    char c2;
    void *ptr;
};
#pragma pack(pop)
// But be aware: unaligned access is slower!

// Check size at compile time
_Static_assert(sizeof(struct GoodAlign) == 16, "Size mismatch");
```

### 4. printf/scanf Format Specifiers

**Problem: Wrong format specifiers cause undefined behavior**

**Problem Code:**
```c
// BAD - Wrong format for size_t and pointers
size_t size = 1000;
printf("Size: %d\n", size);          // WRONG! Should be %zu

void *ptr = malloc(100);
printf("Pointer: %x\n", ptr);        // WRONG! Truncates on 64-bit

long value = 123456789;
printf("Value: %d\n", value);        // WRONG! %d is for int

// BAD - scanf with wrong types
int size;
scanf("%zu", &size);                 // WRONG! %zu expects size_t*
```

**Correct Code:**
```c
// GOOD - Correct format specifiers
size_t size = 1000;
printf("Size: %zu\n", size);         // %zu for size_t

void *ptr = malloc(100);
printf("Pointer: %p\n", ptr);        // %p for pointers

long value = 123456789;
printf("Value: %ld\n", value);       // %ld for long

// GOOD - Matching types
size_t size;
scanf("%zu", &size);                 // %zu with size_t*

// For fixed-width types
uint64_t big_num = 123456789ULL;
printf("Big: %" PRIu64 "\n", big_num);  // Use PRIu64 from <inttypes.h>

int64_t signed_num = -123456789LL;
printf("Signed: %" PRId64 "\n", signed_num);
```

**Format Specifier Reference:**

| Type | 32-bit | 64-bit | Correct Format |
|------|--------|--------|----------------|
| `int` | 4 bytes | 4 bytes | `%d` (signed), `%u` (unsigned) |
| `long` | 4 bytes | 8 bytes (Unix) | `%ld` (signed), `%lu` (unsigned) |
| `long long` | 8 bytes | 8 bytes | `%lld` (signed), `%llu` (unsigned) |
| `size_t` | 4 bytes | 8 bytes | `%zu` |
| `ssize_t` | 4 bytes | 8 bytes | `%zd` |
| `ptrdiff_t` | 4 bytes | 8 bytes | `%td` |
| `void*` | 4 bytes | 8 bytes | `%p` |
| `intptr_t` | 4 bytes | 8 bytes | `%"PRIdPTR` (from `<inttypes.h>`) |
| `uint64_t` | 8 bytes | 8 bytes | `%"PRIu64` (from `<inttypes.h>`) |

### 5. Bit Shift Operations

**Problem: Shifting beyond type width causes undefined behavior**

**Problem Code:**
```c
// BAD - Assumes 32-bit operations
unsigned long mask = 1 << 31;        // OK in 32-bit
mask = 1 << 32;                      // UNDEFINED! Shifts beyond int width

// BAD - Bit fields with assumptions
unsigned int flags = 0xFFFFFFFF;     // All bits set
unsigned long lflags = flags << 32;  // Shifts int, then extends - WRONG!

// BAD - Assumes long is 32-bit
long value = some_calculation();
int shifted = value >> 32;           // On 64-bit, this doesn't get upper bits!
```

**Correct Code:**
```c
// GOOD - Use explicit types and ULL suffix
uint64_t mask = 1ULL << 31;          // Explicit 64-bit
mask = 1ULL << 32;                   // OK, defined behavior

// GOOD - Cast before shifting
unsigned int flags = 0xFFFFFFFF;
uint64_t lflags = ((uint64_t)flags) << 32;  // Cast first, then shift

// GOOD - Use proper types
int64_t value = some_calculation();
int32_t upper = (int32_t)(value >> 32);     // Extract upper 32 bits

// GOOD - Use masks for bit operations
uint64_t full_value = 0x123456789ABCDEFULL;
uint32_t lower = (uint32_t)(full_value & 0xFFFFFFFFULL);
uint32_t upper = (uint32_t)((full_value >> 32) & 0xFFFFFFFFULL);
```

### 6. Array Indexing and Pointer Arithmetic

**Problem: Using int for array indices may overflow**

**Problem Code:**
```c
// BAD - int index for large arrays
char *huge_buffer = malloc(10000000000ULL);  // 10 GB
for (int i = 0; i < 10000000000; i++) {      // OVERFLOW! i wraps
    huge_buffer[i] = 0;
}

// BAD - Pointer arithmetic assumptions
struct Data {
    int x;
    void *ptr;  // 8 bytes on 64-bit
};
struct Data *array = malloc(1000 * sizeof(struct Data));
int offset = 100;
struct Data *item = (struct Data *)((char *)array + offset * 12);
// WRONG! sizeof(struct Data) is 16 on 64-bit, not 12!
```

**Correct Code:**
```c
// GOOD - Use size_t for indices
char *huge_buffer = malloc(10000000000ULL);
for (size_t i = 0; i < 10000000000ULL; i++) {
    huge_buffer[i] = 0;
}

// GOOD - Use sizeof, not hardcoded sizes
struct Data {
    int x;
    void *ptr;
};
struct Data *array = malloc(1000 * sizeof(struct Data));
size_t offset = 100;
struct Data *item = &array[offset];  // Let compiler handle arithmetic

// Or if manual calculation needed:
struct Data *item = (struct Data *)((char *)array + offset * sizeof(struct Data));
```

## Data Type Guidelines

### Use Fixed-Width Types (Best Practice)

**Instead of platform-dependent types, use fixed-width types:**

```c
#include <stdint.h>
#include <inttypes.h>

// AVOID platform-dependent types
long value;           // 4 bytes on Windows 64-bit, 8 bytes on Linux 64-bit
unsigned long flags;  // Size varies by platform

// PREFER fixed-width types
int32_t value32;      // Always 4 bytes
int64_t value64;      // Always 8 bytes
uint32_t flags32;     // Always 4 bytes unsigned
uint64_t flags64;     // Always 8 bytes unsigned

// For sizes and counts
size_t size;          // Unsigned integer type for object sizes
ssize_t ssize;        // Signed version of size_t
ptrdiff_t diff;       // Result of pointer subtraction

// For pointer storage
intptr_t ptr_int;     // Signed integer large enough for pointer
uintptr_t ptr_uint;   // Unsigned integer large enough for pointer
```

### Type Selection Guide

**For memory sizes and offsets:**
```c
size_t buffer_size = 1024;          // Use size_t
void *buffer = malloc(buffer_size);

ssize_t bytes_read = read(fd, buf, size);  // ssize_t can be negative
if (bytes_read < 0) {
    perror("read error");
}
```

**For array indices:**
```c
size_t count = get_array_count();
for (size_t i = 0; i < count; i++) {
    process(array[i]);
}
```

**For pointer differences:**
```c
char *start = buffer;
char *end = buffer + 1000;
ptrdiff_t distance = end - start;    // Use ptrdiff_t
```

**For file offsets:**
```c
off_t offset = lseek(fd, 0, SEEK_END);  // off_t is 64-bit safe
// Or use off64_t on 32-bit systems with large file support
```

**For flags and bit operations:**
```c
uint32_t flags = 0;                  // When 32 bits sufficient
uint64_t wideflags = 0;              // When need more than 32 bits
```

## Compiler Flags and Build Changes

### GCC/Clang Compilation Flags

**32-bit compilation:**
```makefile
# Compile for 32-bit
CFLAGS += -m32
LDFLAGS += -m32
```

**64-bit compilation:**
```makefile
# Compile for 64-bit (usually default on 64-bit systems)
CFLAGS += -m64
LDFLAGS += -m64

# Or just omit -m flag and use system default
```

**Enable warnings for 64-bit issues:**
```makefile
# Warn about conversions
CFLAGS += -Wconversion
CFLAGS += -Wsign-conversion

# Warn about pointer/integer conversions
CFLAGS += -Wpointer-to-int-cast
CFLAGS += -Wint-to-pointer-cast

# Warn about format strings
CFLAGS += -Wformat=2

# Warn about pointer sign
CFLAGS += -Wpointer-sign

# Additional useful warnings
CFLAGS += -Wcast-align          # Warn about alignment issues
CFLAGS += -Wstrict-overflow=2   # Warn about overflow assumptions
```

### Preprocessor Macros

**Detect 64-bit compilation:**
```c
// Portable 64-bit detection
#if defined(__LP64__) || defined(_LP64) || defined(__x86_64__) || defined(_WIN64)
    #define IS_64BIT 1
#else
    #define IS_64BIT 0
#endif

// GCC/Clang specific
#ifdef __x86_64__
    // x86-64 specific code
#endif

#ifdef __aarch64__
    // ARM 64-bit specific code
#endif

// Windows specific
#ifdef _WIN64
    // Windows 64-bit
#endif
```

**Conditional compilation example:**
```c
#if defined(__LP64__)
    // 64-bit code
    typedef uint64_t handle_t;
    #define HANDLE_FORMAT "%lu"
#else
    // 32-bit code
    typedef uint32_t handle_t;
    #define HANDLE_FORMAT "%u"
#endif
```

## Common Migration Patterns

### Pattern 1: Converting Handle/ID Storage

**Before (32-bit):**
```c
// Storing handles/IDs as int
typedef int handle_t;
handle_t file_handles[MAX_FILES];

int open_file(const char *path) {
    FILE *fp = fopen(path, "r");
    return (int)fp;  // BAD!
}

FILE *get_file(int handle) {
    return (FILE *)handle;  // BAD!
}
```

**After (64-bit compatible):**
```c
// Use pointer type or intptr_t
typedef intptr_t handle_t;
handle_t file_handles[MAX_FILES];

handle_t open_file(const char *path) {
    FILE *fp = fopen(path, "r");
    return (handle_t)fp;  // Safe conversion
}

FILE *get_file(handle_t handle) {
    return (FILE *)handle;  // Safe conversion
}

// Or better - use actual pointer type
typedef FILE* file_handle_t;
file_handle_t file_handles[MAX_FILES];
```

### Pattern 2: Converting Unions with Pointers

**Before (32-bit):**
```c
// Union assumes pointer and int are same size
union Value {
    int int_val;
    void *ptr_val;
};  // Size: 4 bytes in 32-bit, 8 bytes in 64-bit!

union Value v;
v.int_val = 42;
void *p = v.ptr_val;  // BROKEN in 64-bit!
```

**After (64-bit compatible):**
```c
// Use intptr_t or separate unions
union Value {
    intptr_t int_val;  // Now matches pointer size
    void *ptr_val;
};

// Or use tagged union
enum ValueType { TYPE_INT, TYPE_PTR };

struct Value {
    enum ValueType type;
    union {
        int int_val;
        void *ptr_val;
    } data;
};
```

### Pattern 3: Converting Packed Network Protocols

**Before (32-bit):**
```c
// Protocol assumes natural alignment
struct NetworkPacket {
    uint32_t magic;
    void *callback;  // 4 bytes in 32-bit, 8 in 64-bit!
    uint32_t size;
};
// Size varies between architectures!
```

**After (64-bit compatible):**
```c
// Use fixed-width types and explicit packing
#pragma pack(push, 1)
struct NetworkPacket {
    uint32_t magic;
    uint64_t callback_id;  // Use ID instead of pointer
    uint32_t size;
};
#pragma pack(pop)
// Size is now consistent

// Map callback IDs to actual function pointers
void *id_to_callback(uint64_t id) {
    // Lookup in callback registry
}
```

### Pattern 4: Converting Bit Field Structures

**Before (32-bit):**
```c
// Bit fields with assumptions
struct Flags {
    unsigned int flag1 : 1;
    unsigned int flag2 : 1;
    unsigned int reserved : 30;
    void *data;  // Alignment changes in 64-bit!
};
```

**After (64-bit compatible):**
```c
// Use explicit types and consider padding
struct Flags {
    uint32_t flag1 : 1;
    uint32_t flag2 : 1;
    uint32_t reserved : 30;
    uint32_t padding;  // Explicit padding for 8-byte alignment
    void *data;
};

// Or avoid bit fields with pointers
struct Flags {
    uint32_t flags;    // Store all flags in single field
    void *data;
};

#define FLAG1_BIT 0x00000001
#define FLAG2_BIT 0x00000002

// Access via macros
#define HAS_FLAG1(f) ((f)->flags & FLAG1_BIT)
#define SET_FLAG1(f) ((f)->flags |= FLAG1_BIT)
```

## Platform-Specific Considerations

### x86 vs x86_64 (Intel/AMD)

**Calling Convention Changes:**
- **32-bit (x86)**: Arguments passed on stack
- **64-bit (x86_64)**: First 6 arguments in registers (RDI, RSI, RDX, RCX, R8, R9)

**Assembly Language:**
```c
// If using inline assembly, update register names
#ifdef __x86_64__
    // 64-bit registers
    asm("movq %rax, %rbx");
#else
    // 32-bit registers
    asm("movl %eax, %ebx");
#endif
```

**SSE/AVX alignment:**
- 64-bit mode expects 16-byte stack alignment
- May need to align structures for SIMD operations

### ARM vs AArch64

**Register differences:**
- **32-bit ARM**: 32-bit registers (R0-R15)
- **64-bit AArch64**: 64-bit registers (X0-X30), can access lower 32-bits as W0-W30

**Pointer Authentication (AArch64):**
```c
// AArch64 may use pointer authentication
// Ensure crypto-secure pointers are handled correctly
#ifdef __aarch64__
    // Handle pointer authentication if enabled
#endif
```

## Testing and Validation

### Compile-Time Checks

**Use static assertions:**
```c
#include <assert.h>

// Verify size assumptions
_Static_assert(sizeof(void*) == 8, "Expect 64-bit pointers");
_Static_assert(sizeof(size_t) == 8, "Expect 64-bit size_t");
_Static_assert(sizeof(int) == 4, "Expect 32-bit int");

// Verify structure sizes
_Static_assert(sizeof(struct MyStruct) == 32, "Unexpected struct size");
```

### Runtime Checks

**Print type sizes:**
```c
void print_type_sizes(void) {
    printf("sizeof(char):      %zu\n", sizeof(char));
    printf("sizeof(short):     %zu\n", sizeof(short));
    printf("sizeof(int):       %zu\n", sizeof(int));
    printf("sizeof(long):      %zu\n", sizeof(long));
    printf("sizeof(long long): %zu\n", sizeof(long long));
    printf("sizeof(void*):     %zu\n", sizeof(void*));
    printf("sizeof(size_t):    %zu\n", sizeof(size_t));
    printf("sizeof(ptrdiff_t): %zu\n", sizeof(ptrdiff_t));
}
```

### Test Large Allocations

```c
// Test with > 4GB allocations
size_t large_size = 5ULL * 1024 * 1024 * 1024;  // 5 GB
void *buffer = malloc(large_size);
if (buffer) {
    printf("Successfully allocated %zu bytes\n", large_size);
    // Test access
    ((char*)buffer)[large_size - 1] = 'x';
    free(buffer);
}
```

### Address Sanitizer

**Enable sanitizers to catch issues:**
```makefile
CFLAGS += -fsanitize=address          # Memory errors
CFLAGS += -fsanitize=undefined        # Undefined behavior
CFLAGS += -fno-omit-frame-pointer     # Better stack traces
```

## Migration Checklist

### Phase 1: Code Audit
- [ ] Search for `int` variables storing pointers
- [ ] Search for casts between pointers and integers
- [ ] Search for hardcoded structure sizes
- [ ] Check all `printf`/`scanf` format strings
- [ ] Review array indexing with `int` variables
- [ ] Check unions containing pointers
- [ ] Review bit shift operations
- [ ] Check file I/O offset handling

### Phase 2: Type Conversion
- [ ] Replace pointer-to-int conversions with `intptr_t`/`uintptr_t`
- [ ] Replace `long` with fixed-width types where appropriate
- [ ] Use `size_t` for all size/count variables
- [ ] Use `ptrdiff_t` for pointer arithmetic
- [ ] Update format specifiers in printf/scanf
- [ ] Add explicit structure padding where needed

### Phase 3: Compilation
- [ ] Enable all 64-bit warnings (`-Wconversion`, `-Wformat=2`, etc.)
- [ ] Fix all compilation warnings
- [ ] Add static assertions for size assumptions
- [ ] Test compilation on both 32-bit and 64-bit (if supporting both)

### Phase 4: Testing
- [ ] Run existing unit tests
- [ ] Test with large memory allocations (> 4 GB)
- [ ] Test with large file operations
- [ ] Test with Address Sanitizer
- [ ] Test serialization/deserialization if applicable
- [ ] Verify network protocol compatibility
- [ ] Test on actual 64-bit hardware

### Phase 5: Performance
- [ ] Profile application on 64-bit
- [ ] Optimize memory usage (64-bit uses more memory)
- [ ] Consider cache effects (larger pointers = less cache efficiency)
- [ ] Test with realistic workloads

## Common Pitfalls Summary

1. **Pointer Truncation**: Casting pointer to `int` loses upper 32 bits
2. **Format Mismatch**: Using `%d` for `size_t` or `%x` for pointers
3. **Array Overflow**: Using `int` for large array indices
4. **Structure Size**: Assuming structure sizes remain the same
5. **Bit Operations**: Shifting beyond type width
6. **Signed/Unsigned**: Mixing `size_t` (unsigned) with signed integers
7. **Alignment**: Stricter alignment requirements in 64-bit
8. **Network Protocols**: Sending pointer values or size-dependent structures
9. **Serialization**: File formats assuming 32-bit sizes
10. **Third-Party Libraries**: Ensure all dependencies are 64-bit compatible

## Best Practices

1. **Use Standard Types**: Prefer `size_t`, `ptrdiff_t`, `intptr_t` over `int`/`long`
2. **Use Fixed-Width Types**: Use `int32_t`, `uint64_t` from `<stdint.h>`
3. **Check Format Strings**: Always use correct printf/scanf format specifiers
4. **Avoid Magic Numbers**: Use `sizeof()` instead of hardcoded structure sizes
5. **Static Assertions**: Add compile-time checks for size assumptions
6. **Enable Warnings**: Compile with `-Wall -Wextra -Wconversion`
7. **Test Early**: Test on 64-bit platform as soon as possible
8. **Document Assumptions**: Comment any remaining 32/64-bit specific code
9. **Use Sanitizers**: Enable ASan and UBSan during testing
10. **Review Assembly**: Check generated assembly for critical code paths

## Additional Resources

- **C99 Standard**: `<stdint.h>`, `<inttypes.h>` for portable types
- **POSIX**: `off_t`, `ssize_t` for system calls
- **GCC Documentation**: https://gcc.gnu.org/onlinedocs/
- **Intel 64 and IA-32 Architectures Software Developer's Manual**
- **ARM Architecture Reference Manual ARMv8**

## Conclusion

Migrating from 32-bit to 64-bit requires careful attention to:
- Pointer size changes (4 → 8 bytes)
- Data type assumptions (`long` varies by platform)
- Format specifier correctness
- Structure alignment and padding
- Array indexing with proper types

Follow this guide systematically, enable compiler warnings, and test thoroughly to ensure a successful migration.

---

## TMOS-Specific LP64 Migration Patterns

> Patterns discovered during TMOS module migrations from CentOS 6 (i686/ILP32) to Rocky Linux 8.10 (x86_64/LP64).

### abs() on time_t (LP64 Truncation)

On LP64, `time_t` is `long` (8 bytes). The standard `abs()` function has an `int` overload that silently truncates `time_t` differences. Use `llabs()` instead.

```cpp
// WRONG — abs() selects int overload, truncates time_t (8 bytes) to int (4 bytes):
long delta = abs(time_now - ref_time);  // LP64 truncation!

// CORRECT — llabs() handles long long and time_t correctly:
long delta = llabs(time_now - ref_time);

// OR in C++ with <cstdlib>:
long delta = std::abs((long long)(time_now - ref_time));
```

**Detection:**
```bash
grep -rn "\babs\s*(.*time\b" <source_dir>/ --include="*.cpp" --include="*.c"
```

---

### ntohl()/htonl() With container.size() Argument

On LP64, `std::container::size()` returns `size_t` (8 bytes). `ntohl()`/`htonl()` expect `uint32_t` (4 bytes). The implicit narrowing conversion silently truncates.

```cpp
// WRONG — size_t (8 bytes) silently narrowed to uint32_t (4 bytes) argument:
uint32_t wire_len = ntohl(buf.size());

// CORRECT — explicit cast with range check:
if (buf.size() > UINT32_MAX) {
    throw std::overflow_error("buffer size exceeds wire format maximum");
}
uint32_t wire_len = ntohl(static_cast<uint32_t>(buf.size()));
```

**Detection:**
```bash
grep -rn "ntohl(.*\.size()\|htonl(.*\.size()\|ntohs(.*\.size()\|htons(.*\.size()" \
    <source_dir>/ --include="*.cpp" --include="*.c"
```

---

### xmlParseMemory() Length Argument Narrowing

`xmlParseMemory(const char *buffer, int size)` takes `int` for the length. On LP64, `std::string::size()` returns `size_t` (8 bytes). Implicit narrowing from `size_t` → `int` produces a GCC 11 warning and can truncate for strings > 2GB.

```cpp
// WRONG — size_t implicitly narrowed to int:
xmlDocPtr doc = xmlParseMemory(xml.c_str(), xml.size());

// CORRECT — explicit static_cast:
xmlDocPtr doc = xmlParseMemory(xml.c_str(), static_cast<int>(xml.size()));
```

**Detection:**
```bash
grep -rn "xmlParseMemory.*\.size()" <source_dir>/ --include="*.cpp" --include="*.c"
```

---

### BIO_get_mem_data() Return Type Mismatch

`BIO_get_mem_data(bio, &ptr)` is a macro returning `long` (8 bytes on LP64). Storing in `int` (4 bytes) silently truncates for data > 2GB.

```cpp
// WRONG — int truncates long return on LP64:
int len = BIO_get_mem_data(bio, &ptr);

// CORRECT — use long:
long len = BIO_get_mem_data(bio, &ptr);
```

See also: **openssl111k-migration.SKILL.md** for full OpenSSL-specific context.

---

### Signed Loop Counter With size() Comparison

Using `int i` with `i < container.size()` produces a signed/unsigned comparison warning (`-Wsign-compare`) because `size()` returns `size_t` (unsigned 8 bytes on LP64). On very large containers, a negative `int i` would compare as greater than `size()` due to unsigned promotion.

```cpp
// WRONG — signed/unsigned comparison, int may wrap before size() value:
for (int i = 0; i < s.size(); i++) { ... }

// CORRECT option 1 — use size_t:
for (size_t i = 0; i < s.size(); i++) { ... }

// CORRECT option 2 — range-based for (C++11):
for (const auto& elem : s) { ... }

// CORRECT option 3 — explicit cast (when i must stay int for legacy reasons):
for (int i = 0; i < static_cast<int>(s.size()); i++) { ... }
```

**Detection:**
```bash
grep -rn "for\s*(int\s\+[a-z_]\+\s*=\s*0\s*;\s*[a-z_]\+\s*<\s*[a-z_]\+\.size()" \
    <source_dir>/ --include="*.cpp" --include="*.c"
```

---

### TMOS Pre-Build LP64 Scan Checklist

Before building a TMOS C/C++ module on x86_64, run this quick scan to catch the most common LP64 issues in TMOS codebases:

```bash
MODULE_SRC=<module_source_path>

echo "=== LP64 pre-build scan for ${MODULE_SRC} ==="

echo "[1] Pointer cast to int/unsigned int:"
grep -RIn "(unsigned int).*this\|(int).*this" ${MODULE_SRC}/ --include="*.cpp" --include="*.c" --include="*.h"

echo "[2] time_t with %d format:"
grep -RIn "printf.*\"%.*%d.*time\|snprintf.*\"%.*%d.*time" ${MODULE_SRC}/ --include="*.cpp" --include="*.c"

echo "[3] abs() on time_t:"
grep -RIn "\babs\s*(.*time" ${MODULE_SRC}/ --include="*.cpp" --include="*.c"

echo "[4] ssize_t from read/write stored in int:"
grep -RIn "int\s\+[a-z_]\+\s*=\s*read(\|int\s\+[a-z_]\+\s*=\s*write(" ${MODULE_SRC}/ --include="*.cpp" --include="*.c"

echo "[5] %d with .size():"
grep -RIn "printf.*%d.*\.size()\|\.size().*printf" ${MODULE_SRC}/ --include="*.cpp" --include="*.c"

echo "[6] ntohl/htonl with size():"
grep -RIn "ntohl(.*\.size()\|htonl(.*\.size()" ${MODULE_SRC}/ --include="*.cpp" --include="*.c"

echo "[7] xmlParseMemory with size():"
grep -RIn "xmlParseMemory.*\.size()" ${MODULE_SRC}/ --include="*.cpp" --include="*.c"

echo "[8] BIO_get_mem_data stored in int:"
grep -RIn "int\s\+[a-z_]\+\s*=\s*BIO_get_mem_data" ${MODULE_SRC}/ --include="*.cpp" --include="*.c"

echo "[9] signed loop counter with .size():"
grep -RIn "for\s*(int\s\+[a-z_]\+.*\.size()" ${MODULE_SRC}/ --include="*.cpp" --include="*.c"

echo "=== Scan complete ==="
```



---

## Hardcoded /usr/lib/ in Spec Files Must Use %{_lib} Macro on Rocky x86_64

**Domain:** 32-bit to 64-bit / RPM Packaging  
**Applies to:** Any TMOS module whose spec file hardcodes `/usr/lib/` in `%files`, `%install`, `%post`, or `%preun` sections

**Problem:** On Rocky Linux x86_64, `%{_lib}` expands to `lib64`. Installed files land in `/usr/lib64/` (from the Makefile) but the spec expects `/usr/lib/`, causing:
```
Installed (but unpackaged) file(s) found: /usr/lib64/<module>/...
File not found: /usr/lib/<module>/...
```

**Resolution:**

| Location | Before | After |
|---|---|---|
| Spec `%files`/`%install`/`%post`/`%preun` | `/usr/lib/<module>/` | `/usr/%{_lib}/<module>/` |
| Makefile install target | `$(DESTDIR)/usr/lib/<module>/` | `$(DESTDIR)/usr/lib64/<module>/` |

**Detection:**
```bash
grep -n "/usr/lib/" <module>.spec   # find hardcoded lib without %{_lib} macro
```
Apply to **ALL** occurrences in `%files`, `%install`, `%post`, `%preun`.

---

## readlink() and readlinkat() Return ssize_t — Do Not Store in int

**Domain:** 32-bit to 64-bit / LP64 Integer Width  
**Applies to:** Any TMOS module calling `readlink()` or `readlinkat()`

**Problem:** Both functions return `ssize_t` (8 bytes on LP64). Storing in `int` truncates large values and breaks error detection (`-1LL` truncated to `int` ≠ `-1` in all cases).

```cpp
int rc = readlink(path, buf, sizeof(buf));      // WRONG
int n  = readlinkat(fd, path, buf, sizeof(buf)); // WRONG
```

**Resolution:**
```cpp
ssize_t rc = readlink(path, buf, sizeof(buf));      // CORRECT
ssize_t n  = readlinkat(fd, path, buf, sizeof(buf)); // CORRECT
if (rc > 0) buf[rc] = '\0';
```

**Detection:**
```bash
grep -RIn --include='*.cpp' --include='*.c' --include='*.h' \
  'int[[:space:]]\+[a-z_]\+[[:space:]]*=[[:space:]]*readlink(\|int[[:space:]]\+[a-z_]\+[[:space:]]*=[[:space:]]*readlinkat(' \
  <module_source_path>/
```
