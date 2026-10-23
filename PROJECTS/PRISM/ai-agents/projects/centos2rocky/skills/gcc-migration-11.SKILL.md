---
name: gcc-migration-11
description: Domain knowledge for migrating C/C++ source code from GCC 4.8.5 to GCC 11.2.x. Covers compiler warnings, deprecated features, C++ standard changes, optimization differences, and build system updates.
applyTo: ["**/*.c", "**/*.cpp", "**/*.cc", "**/*.cxx", "**/*.h", "**/*.hpp", "**/Makefile*", "**/*.mk", "**/CMakeLists.txt", "**/*.cmake", "**/configure.ac", "**/*.spec"]
---

# GCC Migration Guide: GCC 4.8.5 → GCC 11.2.x

This skill provides comprehensive guidance for migrating C/C++ applications from GCC 4.8.5 to GCC 11.2.x, covering breaking changes, new warnings, deprecated features, C++ standard updates, and compiler flag modifications.

## Overview of GCC Version Changes

### Version Timeline (4.8.5 → 11.2.x)
- **GCC 4.8.5** (June 2015) - C++11 support, starting point
- **GCC 5.x** (April 2015) - C++14 default, ABI change, new warnings
- **GCC 6.x** (April 2016) - C++14 improvements, more diagnostics
- **GCC 7.x** (May 2017) - C++17 support, new optimizations
- **GCC 8.x** (May 2018) - C++17 improvements, stricter warnings
- **GCC 9.x** (May 2019) - C++17 complete, C++20 experimental
- **GCC 10.x** (May 2020) - C++20 support, default PIE
- **GCC 11.2.x** (July 2021) - C++20 improvements, new warnings

### Key Milestones
- **GCC 5+**: Major C++ ABI change (libstdc++ dual ABI)
- **GCC 7+**: Full C++17 support
- **GCC 10+**: Position Independent Executable (PIE) enabled by default
- **GCC 11+**: Improved C++20 support, stricter standard conformance

## Critical Breaking Changes

### 1. C++ ABI Change (GCC 5+)

**Most Significant Change:** libstdc++ dual ABI for std::string and std::list

**Impact:**
```cpp
// GCC 4.8.5 - Old ABI
std::string str = "hello";  // Uses COW (Copy-On-Write) implementation

// GCC 5+ - New ABI (default)
std::string str = "hello";  // Uses SSO (Small String Optimization)

// Binary incompatibility between old and new ABI!
```

**Migration Options:**

**Option 1: Use New ABI (Recommended)**
```makefile
# Default behavior in GCC 5+
CXXFLAGS += -std=c++14
# New ABI is used automatically
```

**Option 2: Force Old ABI (for compatibility)**
```makefile
# Define before including any standard headers
CXXFLAGS += -D_GLIBCXX_USE_CXX11_ABI=0
```

**Option 3: Mixed Environment**
```cpp
// In source code, before including <string> or <list>
#define _GLIBCXX_USE_CXX11_ABI 0
#include <string>
#include <list>
```

**Critical Rule:**
- All components in a binary must use the **same ABI**
- Mixing ABIs causes undefined behavior and linker errors
- Third-party libraries must be recompiled with matching ABI

### 2. Default C++ Standard Change

**GCC 4.8.5:**
```bash
# Default: GNU++98 (C++98 with GNU extensions)
g++ main.cpp  # Equivalent to -std=gnu++98
```

**GCC 11.2.x:**
```bash
# Default: GNU++17 (C++17 with GNU extensions)
g++ main.cpp  # Equivalent to -std=gnu++17
```

**Migration Impact:**
```cpp
// Code that compiled in GCC 4.8.5 with implicit C++98
auto x = 10;        // Error in C++98, OK in C++11+
nullptr;            // Error in C++98, OK in C++11+
for (auto& item : vec) {}  // Error in C++98, OK in C++11+

// Some C++98 code may break in C++17
std::auto_ptr<int> ptr;  // Removed in C++17, use std::unique_ptr
register int x;          // Deprecated in C++17, removed in C++20
```

**Solution - Explicit Standard:**
```makefile
# Specify exact standard
CXXFLAGS += -std=c++11   # Use C++11
CXXFLAGS += -std=c++14   # Use C++14
CXXFLAGS += -std=c++17   # Use C++17
CXXFLAGS += -std=gnu++11 # C++11 with GNU extensions
```

### 3. Position Independent Executable (PIE) Default (GCC 10+)

**GCC 4.8.5:**
```bash
# PIE not enabled by default
gcc main.c -o main  # Produces non-PIE executable
```

**GCC 10+:**
```bash
# PIE enabled by default on many platforms
gcc main.c -o main  # Produces PIE executable
```

**Impact:**
```c
// Code with absolute addressing may break
extern int global_var;
int *ptr = &global_var;  // Works differently with PIE

// Assembly code with absolute jumps may need updates
asm("jmp *%0" : : "r" (function_ptr));  // May need PIC register
```

**Solutions:**

**Option 1: Keep PIE (Recommended for security)**
```makefile
# Ensure all code is position-independent
CFLAGS += -fPIC
LDFLAGS += -pie
```

**Option 2: Disable PIE (if incompatible)**
```makefile
CFLAGS += -fno-pie
LDFLAGS += -no-pie
```

**Option 3: Fix Assembly Code**
```c
// Use PIC-compatible assembly
asm("call *%0" : : "r" (function_ptr));
```

### 4. Stricter Type Checking and Warnings

**New Errors/Warnings in GCC 11:**

```c
// 1. Narrowing conversions (C++11 onwards)
int x = 1000;
char c = {x};  // GCC 4.8.5: warning, GCC 11: error in C++11

// 2. Missing return statements
int foo() {
    printf("hello");
    // GCC 4.8.5: warning, GCC 11: error with -Werror
}

// 3. Array bounds checking (improved)
int arr[5];
arr[10] = 1;  // GCC 11: better detection, warning/error

// 4. Invalid pointer comparisons
void *p1 = malloc(10);
void *p2 = malloc(10);
if (p1 < p2) {}  // GCC 11: warning about undefined behavior

// 5. Misleading indentation
if (condition)
    statement1();
    statement2();  // GCC 11: warning, looks like in if-block but isn't
```

### 5. Removed/Deprecated Features

**Completely Removed:**

```cpp
// C++17 removals (error in GCC 11 with -std=c++17)
std::auto_ptr<int> ptr;              // REMOVED: Use unique_ptr
std::random_shuffle(v.begin(), v.end());  // REMOVED: Use std::shuffle
std::bind1st, std::bind2nd;          // REMOVED: Use std::bind
register int x;                       // REMOVED in C++17
throw() exception specifications;     // REMOVED: Use noexcept

// Trigraphs removed (GCC 5.1+)
int array??(??) = ??< 1, 2, 3 ??>; // REMOVED
// Was equivalent to: int array[] = { 1, 2, 3 };
```

**Deprecated (warnings):**

```cpp
// Implicit conversions from string literals
char *str = "hello";  // GCC 11: warning, should be const char*

// Implicit fallthrough in switch
switch (x) {
    case 1:
        do_something();  // GCC 11: warning without [[fallthrough]]
    case 2:
        do_other();
}
```

### 6. Changes to Warning Flags

**GCC 4.8.5:**
```makefile
CFLAGS += -Wall -Wextra
# Enables common warnings
```

**GCC 11.2.x - New warnings to consider:**
```makefile
# Enhanced warnings
CFLAGS += -Wall -Wextra
CFLAGS += -Wmisleading-indentation      # New in GCC 6
CFLAGS += -Wduplicated-cond             # New in GCC 6
CFLAGS += -Wduplicated-branches         # New in GCC 7
CFLAGS += -Wlogical-op                  # Improved
CFLAGS += -Wrestrict                    # New in GCC 7
CFLAGS += -Wnull-dereference           # Improved
CFLAGS += -Wdouble-promotion           # Useful for floating point
CFLAGS += -Wshadow                      # Variable shadowing
CFLAGS += -Wformat=2                    # Strict format checking
CFLAGS += -Warray-bounds=2              # Enhanced bounds checking

# For C++ specifically
CXXFLAGS += -Woverloaded-virtual
CXXFLAGS += -Wnon-virtual-dtor
CXXFLAGS += -Wold-style-cast
CXXFLAGS += -Wuseless-cast
CXXFLAGS += -Wconversion
```

## Language Feature Changes

### 1. C++ Standard Library Updates

**std::auto_ptr Removed (C++17)**

**GCC 4.8.5 (C++11):**
```cpp
#include <memory>
std::auto_ptr<MyClass> ptr(new MyClass());
ptr->method();
```

**GCC 11.2.x (C++17):**
```cpp
#include <memory>
std::unique_ptr<MyClass> ptr(new MyClass());
// Or better:
auto ptr = std::make_unique<MyClass>();
ptr->method();
```

**std::random_shuffle Removed (C++17)**

**GCC 4.8.5:**
```cpp
#include <algorithm>
std::random_shuffle(vec.begin(), vec.end());
```

**GCC 11.2.x:**
```cpp
#include <algorithm>
#include <random>

std::random_device rd;
std::mt19937 g(rd());
std::shuffle(vec.begin(), vec.end(), g);
```

### 2. Exception Specifications

**GCC 4.8.5:**
```cpp
void foo() throw();              // Old style
void bar() throw(int, char);     // Old style
```

**GCC 11.2.x:**
```cpp
void foo() noexcept;             // Modern C++11
void bar() noexcept(false);      // Can throw

// Old throw() specifications removed in C++17
// Will cause error with -std=c++17
```

### 3. String Literal to char* Conversion

**GCC 4.8.5:**
```cpp
// Deprecated but allowed
char *msg = "Hello";
msg[0] = 'h';  // Undefined behavior but may compile
```

**GCC 11.2.x:**
```cpp
// Produces warning or error
const char *msg = "Hello";  // Correct
// msg[0] = 'h';  // Compile error - const

// For mutable strings
char msg[] = "Hello";  // Copy into array
msg[0] = 'h';  // OK
```

### 4. Implicit Fallthrough in Switch

**GCC 4.8.5:**
```cpp
switch (value) {
    case 1:
        process1();
        // Falls through
    case 2:
        process2();
        break;
}
```

**GCC 11.2.x:**
```cpp
switch (value) {
    case 1:
        process1();
        [[fallthrough]];  // C++17 attribute
    case 2:
        process2();
        break;
}

// Or use GCC attribute for C++11/14
switch (value) {
    case 1:
        process1();
        __attribute__((fallthrough));
    case 2:
        process2();
        break;
}
```

### 5. Register Keyword

**GCC 4.8.5:**
```c
register int counter = 0;  // Hint to compiler
```

**GCC 11.2.x:**
```c
// Deprecated in C++11, removed in C++17
int counter = 0;  // Just remove 'register'
// Modern compilers ignore or optimize better anyway
```

## Optimization Changes

### 1. Aggressive Optimization Warnings

**GCC 11 has better optimization analysis:**

```c
// GCC 4.8.5: May compile without warning
void foo() {
    int x;
    printf("%d", x);  // Uninitialized variable
}

// GCC 11.2.x with -O2: Warning about uninitialized read
```

**Solution:**
```c
void foo() {
    int x = 0;  // Always initialize
    printf("%d", x);
}
```

### 2. Strict Aliasing Rules

**GCC 11 enforces stricter aliasing:**

```c
// GCC 4.8.5: May work
int foo() {
    float f = 1.5f;
    return *(int*)&f;  // Type punning via cast
}

// GCC 11.2.x: Undefined behavior, may optimize incorrectly
```

**Correct Solutions:**

```c
// Option 1: Use memcpy (compiler optimizes to no-op)
int foo() {
    float f = 1.5f;
    int result;
    memcpy(&result, &f, sizeof(result));
    return result;
}

// Option 2: Use union (GCC extension)
union FloatInt {
    float f;
    int i;
};

int foo() {
    union FloatInt fi;
    fi.f = 1.5f;
    return fi.i;
}

// Option 3: Disable strict aliasing (not recommended)
// CFLAGS += -fno-strict-aliasing
```

### 3. Link-Time Optimization (LTO)

**GCC 4.8.5:**
```makefile
# LTO available but immature
CFLAGS += -flto
LDFLAGS += -flto
```

**GCC 11.2.x:**
```makefile
# LTO much more mature and usable
CFLAGS += -flto=auto     # Automatic parallelization
LDFLAGS += -flto=auto
# Or specify threads
CFLAGS += -flto=8        # Use 8 threads
```

**Benefits:**
- Better cross-module optimization
- Smaller binaries
- Better performance

**Considerations:**
- Increases build time
- Requires more memory during linking
- May expose previously hidden bugs

## Architecture-Specific Changes

### 1. x86_64 Instruction Sets

**GCC 4.8.5:**
```makefile
# Limited vectorization
CFLAGS += -march=native
```

**GCC 11.2.x:**
```makefile
# Better auto-vectorization and modern CPU support
CFLAGS += -march=native           # Use all CPU features
CFLAGS += -march=x86-64-v2        # Baseline + SSE3/4, SSSE3
CFLAGS += -march=x86-64-v3        # + AVX, AVX2
CFLAGS += -march=x86-64-v4        # + AVX512

# For compatibility with older CPUs
CFLAGS += -march=x86-64           # Baseline only
```

### 2. ARM/AArch64 Support

**GCC 11 has significantly better ARM support:**

```makefile
# ARM32
CFLAGS += -march=armv7-a -mfpu=neon -mfloat-abi=hard

# ARM64/AArch64
CFLAGS += -march=armv8-a+crypto   # With crypto extensions
CFLAGS += -march=armv8.2-a        # ARMv8.2
```

## Compiler Flag Changes

### 1. Removed/Changed Flags

**No longer supported or behavior changed:**

```makefile
# GCC 4.8.5 flags that changed
-fno-default-inline     # Ignored in modern GCC
-fexternal-templates    # Removed (obsolete)
-falt-external-templates # Removed (obsolete)

# Debug flags
-ggdb3 vs -ggdb         # More debug levels available
```

### 2. New Useful Flags

**GCC 11.2.x new flags:**

```makefile
# Security hardening
CFLAGS += -fstack-protector-strong   # Better than -fstack-protector
CFLAGS += -fstack-clash-protection   # Prevent stack clash attacks
CFLAGS += -fcf-protection=full       # Control flow protection (x86)
CFLAGS += -D_FORTIFY_SOURCE=2        # Runtime checks
CFLAGS += -D_GLIBCXX_ASSERTIONS      # C++ assertions

# Performance
CFLAGS += -fno-semantic-interposition  # Better optimization for shared libs
CFLAGS += -fipa-pta                    # Interprocedural pointer analysis

# Diagnostics
CFLAGS += -fdiagnostics-color=always   # Colored diagnostics
CFLAGS += -fanalyzer                   # Static analysis (GCC 10+)
```

### 3. Standard Compliance Flags

```makefile
# Strict standard compliance
CFLAGS += -pedantic              # Strict ISO C/C++
CFLAGS += -pedantic-errors       # Make warnings errors

# Disable GNU extensions
CFLAGS += -std=c11 -pedantic     # Pure C11
CXXFLAGS += -std=c++17 -pedantic # Pure C++17
```

## Common Migration Patterns

### Pattern 1: Fix Narrowing Conversions

**Before (GCC 4.8.5):**
```cpp
int x = 1000;
char arr[] = {1, 2, x};  // Warning in C++98, error in C++11
```

**After (GCC 11.2.x):**
```cpp
int x = 1000;
char arr[] = {1, 2, static_cast<char>(x)};  // Explicit cast

// Or use std::array for type safety
std::array<int, 3> arr = {1, 2, x};
```

### Pattern 2: Initialize Variables

**Before:**
```c
int process() {
    int result;
    if (condition) {
        result = compute();
    }
    return result;  // GCC 11: warning if condition false
}
```

**After:**
```c
int process() {
    int result = 0;  // Always initialize
    if (condition) {
        result = compute();
    }
    return result;
}
```

### Pattern 3: Fix Missing Returns

**Before:**
```cpp
int calculate(int x) {
    if (x > 0) {
        return x * 2;
    }
    // GCC 11: error, no return in all paths
}
```

**After:**
```cpp
int calculate(int x) {
    if (x > 0) {
        return x * 2;
    }
    return 0;  // Explicit return for all paths
}
```

### Pattern 4: Update deprecated std::bind

**Before:**
```cpp
#include <functional>
std::bind1st(std::plus<int>(), 10);  // Removed in C++17
```

**After:**
```cpp
#include <functional>
auto add_ten = std::bind(std::plus<int>(), 10, std::placeholders::_1);

// Or better, use lambda (C++11)
auto add_ten = [](int x) { return x + 10; };
```

### Pattern 5: Fix Misleading Indentation

**Before:**
```c
if (condition)
    printf("condition true\n");
    printf("always printed\n");  // GCC 11: warning
```

**After:**
```c
if (condition) {
    printf("condition true\n");
}
printf("always printed\n");  // Clear intent

// Or if both should be in if:
if (condition) {
    printf("condition true\n");
    printf("still in if\n");
}
```

### Pattern 6: Replace register Keyword

**Before:**
```c
void process() {
    register int i;
    for (i = 0; i < 1000; i++) {
        // process
    }
}
```

**After:**
```c
void process() {
    int i;  // Just remove 'register'
    for (i = 0; i < 1000; i++) {
        // process
    }
}
```

## Build System Updates

### 1. Makefile Updates

**GCC 4.8.5 Makefile:**
```makefile
CC = gcc
CXX = g++
CFLAGS = -Wall -O2
CXXFLAGS = -Wall -O2

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@
```

**GCC 11.2.x Makefile:**
```makefile
CC = gcc-11
CXX = g++-11
CFLAGS = -Wall -Wextra -O2 -std=c11 -D_FORTIFY_SOURCE=2
CXXFLAGS = -Wall -Wextra -O2 -std=c++17 -D_GLIBCXX_ASSERTIONS

# Security hardening
CFLAGS += -fstack-protector-strong -fstack-clash-protection
LDFLAGS += -Wl,-z,relro -Wl,-z,now

# Position independent code
CFLAGS += -fPIC
LDFLAGS += -pie

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@
```

### 2. CMake Updates

**GCC 4.8.5 CMakeLists.txt:**
```cmake
cmake_minimum_required(VERSION 2.8)
project(MyProject)

add_executable(myapp main.cpp)
```

**GCC 11.2.x CMakeLists.txt:**
```cmake
cmake_minimum_required(VERSION 3.10)
project(MyProject)

# Require C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Enable more warnings
add_compile_options(-Wall -Wextra -Wpedantic)

# Security flags
add_compile_options(
    -fstack-protector-strong
    -D_FORTIFY_SOURCE=2
)

# For PIE
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

add_executable(myapp main.cpp)
```

### 3. Autotools Updates

**configure.ac updates:**
```autoconf
# GCC 4.8.5
AC_INIT([myproject], [1.0])
AC_PROG_CC

# GCC 11.2.x
AC_INIT([myproject], [1.0])
AC_PROG_CC
AC_PROG_CXX

# Check GCC version
GCC_VERSION=$($CC -dumpversion)
AC_MSG_CHECKING([GCC version])
AC_MSG_RESULT([$GCC_VERSION])

# Require minimum GCC 11
AX_COMPARE_VERSION([$GCC_VERSION], [ge], [11.0],
    [AC_MSG_RESULT([yes])],
    [AC_MSG_ERROR([GCC 11+ required])])

# Add C++17 support
AX_CXX_COMPILE_STDCXX([17], [noext], [mandatory])
```

## Testing Strategy

### 1. Compilation Testing

**Step-by-step approach:**

```bash
# Step 1: Test basic compilation
gcc-11 -c main.c -o main.o

# Step 2: Add warnings
gcc-11 -Wall -Wextra -c main.c -o main.o

# Step 3: Add strict standards
gcc-11 -Wall -Wextra -std=c11 -pedantic -c main.c

# Step 4: Enable all warnings as errors
gcc-11 -Wall -Wextra -Werror -std=c11 -c main.c

# Step 5: Test with optimizations
gcc-11 -Wall -Wextra -std=c11 -O2 -c main.c
gcc-11 -Wall -Wextra -std=c11 -O3 -c main.c
```

### 2. Runtime Testing

```bash
# Build with sanitizers for testing
gcc-11 -fsanitize=address -g main.c -o main    # Address sanitizer
gcc-11 -fsanitize=undefined -g main.c -o main  # UB sanitizer
gcc-11 -fsanitize=thread -g main.c -o main     # Thread sanitizer

# Run tests
./main
```

### 3. Static Analysis

```bash
# Use GCC's built-in analyzer (GCC 10+)
gcc-11 -fanalyzer main.c -o main

# Check for issues
gcc-11 -Wall -Wextra -Wconversion main.c -o main 2>&1 | grep warning
```

## Common Pitfalls

### Pitfall 1: ABI Mismatch

**Problem:**
```bash
# Linking fails with undefined references
g++-11 -c module1.cpp -D_GLIBCXX_USE_CXX11_ABI=1
g++-11 -c module2.cpp -D_GLIBCXX_USE_CXX11_ABI=0
g++-11 module1.o module2.o -o app  # LINKER ERROR
```

**Solution:**
Use consistent ABI across all modules.

### Pitfall 2: Optimization Breaks Code

**Problem:**
```c
int flag = 0;

void signal_handler(int sig) {
    flag = 1;
}

int main() {
    signal(SIGINT, signal_handler);
    while (!flag) {  // GCC 11 -O2 may optimize away check
        // wait
    }
}
```

**Solution:**
```c
volatile int flag = 0;  // Use volatile for shared variables
```

### Pitfall 3: Assuming Compilation Order

**Problem:**
```c
// GCC 11 may reorder operations more aggressively
x = compute_expensive();
y = x + 1;
z = y * 2;
// GCC 11 may combine or reorder these
```

**Solution:**
Use memory barriers or volatile if order matters.

## Migration Checklist

### Phase 1: Preparation
- [ ] Audit current GCC 4.8.5 build configuration
- [ ] Document all compiler flags in use
- [ ] Check third-party library compatibility with GCC 11
- [ ] Set up GCC 11 development environment
- [ ] Create test builds in isolated environment

### Phase 2: Code Updates
- [ ] Remove `register` keyword usage
- [ ] Replace `std::auto_ptr` with `std::unique_ptr`
- [ ] Replace `std::random_shuffle` with `std::shuffle`
- [ ] Update exception specifications (`throw()` → `noexcept`)
- [ ] Fix string literal to `char*` conversions
- [ ] Add `[[fallthrough]]` to intentional switch fallthroughs
- [ ] Initialize all variables
- [ ] Ensure all code paths return values
- [ ] Fix misleading indentation

### Phase 3: Build System Updates
- [ ] Update Makefile with GCC 11 compiler
- [ ] Add new warning flags
- [ ] Add security hardening flags
- [ ] Update C++ standard flag (-std=c++17 or higher)
- [ ] Decide on ABI (old vs new)
- [ ] Update CMake/Autotools configuration
- [ ] Test with PIE enabled

### Phase 4: Testing
- [ ] Compile with `-Wall -Wextra -Werror`
- [ ] Test with `-O2` optimization
- [ ] Run with AddressSanitizer
- [ ] Run with UndefinedBehaviorSanitizer
- [ ] Perform regression testing
- [ ] Performance benchmarking
- [ ] Memory leak testing

### Phase 5: Deployment
- [ ] Update deployment documentation
- [ ] Update package dependencies (libgcc, libstdc++)
- [ ] Test in production-like environment
- [ ] Plan rollback procedure
- [ ] Monitor for runtime issues

## Useful GCC 11 Tools

### 1. Compiler Exploratory Tools

```bash
# Show default compiler flags
gcc-11 -dM -E - < /dev/null

# Show include paths
gcc-11 -xc++ -E -v -

# Show library search paths
gcc-11 -print-search-dirs

# Check ABI in use
echo | gcc-11 -xc++ -dM -E - | grep GLIBCXX_USE_CXX11_ABI
```

### 2. Analysis Tools

```bash
# Static analysis
gcc-11 -fanalyzer source.c

# Preprocessing only (check macros)
gcc-11 -E source.c > source.i

# Assembly output (check optimization)
gcc-11 -S -fverbose-asm source.c

# Dependency checking
gcc-11 -MM source.c
```

### 3. Debugging Tools

```bash
# Preprocessor trace
gcc-11 -H source.c

# Show warnings about unused
gcc-11 -Wunused source.c

# Check for undefined behavior
gcc-11 -fsanitize=undefined source.c
```

## Performance Considerations

### 1. Optimization Levels

```makefile
# Development: Fast compilation
CFLAGS += -O0 -g

# Testing: Some optimization, good debugging
CFLAGS += -Og -g

# Production: Balanced
CFLAGS += -O2

# Maximum performance
CFLAGS += -O3 -march=native

# Size optimization
CFLAGS += -Os
```

### 2. Profile-Guided Optimization (PGO)

```bash
# Step 1: Build instrumented binary
gcc-11 -fprofile-generate source.c -o app

# Step 2: Run typical workload
./app < typical_input

# Step 3: Build optimized binary with profile data
gcc-11 -fprofile-use source.c -o app_optimized
```

### 3. Link-Time Optimization

```bash
# Enable LTO
gcc-11 -flto=auto -O3 source.c -o app

# For large projects
gcc-11 -flto=8 -O3 *.c -o app  # Use 8 threads
```

## Platform-Specific Considerations

### Rocky Linux 8.10

**GCC versions available:**
- Default: GCC 8.5 (gcc, g++)
- Toolset: GCC 9, 10, 11 (gcc-toolset-11)

**Installation:**
```bash
# Install GCC 11 on Rocky Linux 8
sudo dnf install gcc-toolset-11

# Enable for current shell
scl enable gcc-toolset-11 bash

# Or use directly
/opt/rh/gcc-toolset-11/root/usr/bin/gcc
```

**Library paths:**
```bash
# Ensure GCC 11 libraries in path
export LD_LIBRARY_PATH=/opt/rh/gcc-toolset-11/root/usr/lib64:$LD_LIBRARY_PATH
```

### RHEL/CentOS

Similar to Rocky Linux, use Software Collections (SCL).

### Ubuntu/Debian

```bash
# Install GCC 11
sudo apt install gcc-11 g++-11

# Set as default
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-11 110
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-11 110
```

## Additional Resources

- GCC 11 Release Notes: https://gcc.gnu.org/gcc-11/changes.html
- GCC 11 Manual: https://gcc.gnu.org/onlinedocs/gcc-11.2.0/gcc/
- Porting to GCC 11: https://gcc.gnu.org/gcc-11/porting_to.html
- C++17 Changes: https://en.cppreference.com/w/cpp/17
- libstdc++ ABI Policy: https://gcc.gnu.org/onlinedocs/libstdc++/manual/abi.html

## Summary

Key migration points for GCC 4.8.5 → GCC 11.2.x:

1. **ABI Change**: Decide on libstdc++ ABI (new recommended, old for compatibility)
2. **C++ Standard**: Update from C++98/11 to C++17+ (default is gnu++17)
3. **PIE Default**: Position Independent Executables enabled by default
4. **Removed Features**: `std::auto_ptr`, `register`, `throw()` specifications
5. **Stricter Warnings**: Initialize variables, return from all paths, fix indentation
6. **New Flags**: Security hardening, better optimization, improved diagnostics
7. **Better Analysis**: Use `-fanalyzer`, sanitizers for finding bugs
8. **Architecture Support**: Better x86_64 levels, improved ARM/AArch64
9. **Testing**: Comprehensive testing with warnings as errors
10. **Dependencies**: Ensure all libraries compiled with same ABI and GCC version

Migration from GCC 4.8.5 to 11.2.x requires careful attention to ABI compatibility, language standard updates, and stricter compiler warnings. The benefits include better performance, security, standards compliance, and bug detection. Plan for incremental migration with thorough testing at each stage.

---

## TMOS-Specific GCC 11 Migration Patterns

> Patterns discovered during TMOS module migrations to Rocky Linux 8.10 / GCC 11.

### CxxTest Test Framework: GCC 11 Warning Suppressions

**Problem:** GCC 11 `-Wall` enables `-Wcatch-value` (warn when exceptions are caught by value rather than by reference). CxxTest's auto-generated test harness catches exceptions by value in its internal macros. Additionally, GCC 11 is stricter about `-Wundef` (undefined macros in `#if`), `-Wparentheses` (suggested parenthesization), and `-Wnonnull` (null passed to non-null parameter) — all triggered by CxxTest-generated code, not by the module's own logic.

**Resolution:** Two separate fixes are needed — one for CxxTest headers (in devfs, uneditable), one for the auto-generated runner:

1. **Use `-isystem` for the CxxTest include directory** — this tells GCC to treat CxxTest headers as system headers, suppressing `-Wundef`, `-Wparentheses`, and `-Wnonnull` from them without masking the same warning classes in the module's own code:
```makefile
# Change -I to -isystem for the CxxTest headers path (typically in devfs):
# Before:
CXXFLAGS += -I $(CXXTEST_HOME)
# After:
CXXFLAGS += -isystem $(CXXTEST_HOME)
```

   > **Superset path caveat:** If `CFLAGS`/`CXXFLAGS` already include a broader path such as `-I $(DEVFS)/usr/include` that covers the CxxTest headers, changing only `$(CXXTEST_HOME)` to `-isystem` will **not** suppress the warnings — GCC still finds the headers via the superset `-I` path first. In that case, **also** change the superset path to `-isystem`:
   > ```makefile
   > # Both the superset AND the specific path must use -isystem:
   > CXXFLAGS += -isystem $(DEVFS)/usr/include
   > CXXFLAGS += -isystem $(CXXTEST_HOME)
   > # (remove the corresponding -I entries for both)
   > ```
   > Check for superset paths: `grep -n '\-I.*DEVFS\|\-I.*devfs' <module>/Makefile <module>/*.mk 2>/dev/null`

2. **Keep only `-Wno-catch-value`** for the auto-generated CxxTest runner (the runner is generated code that catches exceptions by value — this cannot be fixed via `-isystem`):
```makefile
CXXFLAGS += -Wno-catch-value
```

> ⚠️ **Do NOT use `-Wno-undef -Wno-parentheses -Wno-nonnull` in `CXXFLAGS`** — these are global suppressions that mask the same warning classes in the module's own source code.

**Detection:**
```bash
# Check if module uses CxxTest:
grep -rn "cxxtest\|CxxTest\|CXXTEST" <module>/Makefile <module>/tests/ 2>/dev/null
# If CxxTest is used, check build output for these warning types:
grep "catch-value\|Wundef\|Wparentheses\|Wnonnull" build_log.txt
```

**Modules affected:** Any module using CxxTest with GCC 11

---

### GCOV Tool Version Mismatch with gcc-toolset-11

**Problem:** When a module includes `ng_mk/gcov.mk` (TMOS coverage build infrastructure) and its objects are compiled with gcc-toolset-11 (GCC 11), the `GCOV_EXE` variable in `ng_mk/gcov.mk` defaults to the system `gcov` binary (from an older GCC). This older gcov cannot process coverage notes generated by GCC 11, causing coverage build or test failures.

**Resolution:** Set `GCOV_EXE` to the gcc-toolset-11 gcov binary **before** the `include ng_mk/gcov.mk` line in the module's Makefile:
```makefile
# REQUIRED when compiling with gcc-toolset-11:
GCOV_EXE := /opt/rh/gcc-toolset-11/root/usr/bin/gcov
include ng_mk/gcov.mk
```

**Detection:**
```bash
# Check if module includes gcov.mk:
grep -n "ng_mk/gcov.mk" <module>/Makefile
# If yes, verify GCOV_EXE is set before the include:
grep -B5 "ng_mk/gcov.mk" <module>/Makefile | grep GCOV_EXE
```
If `GCOV_EXE` is not set (or set to a non-toolset-11 path), add the assignment before the `include` line.

**Modules affected:** Any module using ng_mk/gcov.mk under gcc-toolset-11

---

### Golden Test Data Must Be Regenerated After OpenSSL Library Upgrade

**Problem:** Unit tests that compare X.509 certificate, CSR, or other crypto output against a hardcoded "golden" string value will fail after upgrading from OpenSSL 1.0.x to OpenSSL 1.1.x, even when the logical content of the certificate is identical. OpenSSL 1.1.x changed the default ASN.1 encoding for subject attribute strings from `PrintableString` to `UTF8String`, altering the DER byte sequence and its base64 representation.

**Example:** In a TMOS module, `TestCrypto.h` contained a hardcoded expected CSR value with `CN=US` encoded as PrintableString (base64 substring `EwJ`). OpenSSL 1.1.x produces the same CN=US encoded as UTF8String (base64 substring `DAJ`), causing the golden comparison to fail.

**Resolution:**
1. Identify the test file containing the hardcoded golden value. The test directory may not always be named `tests/` — search recursively from the module root:
   ```bash
   find <module_source_path>/ -name "*.h" -o -name "*.cpp" | xargs grep -l "EwJ\|MFox\|BEGIN CERTIFICATE REQUEST" 2>/dev/null
   ```
2. Inside the Rocky Linux 8 schroot (where OpenSSL 1.1.x is active), run the CSR/certificate generating code to produce the new output.
3. Update the hardcoded golden string in the test file.
4. Add a comment: `// Golden regenerated for OpenSSL 1.1.x (UTF8String encoding) - YYYY-MM-DD`

**To generate the new golden value, run the CSR-generating test code under OpenSSL 1.1 in the Rocky Linux 8 schroot:**
```bash
schroot -c rocky8.1064
cd <module_source_path>
# Build and run just the CSR-generating code:
./build --override BLD_ENV_BRANCH_NAME:tmos-rocky -arch=x86_64 <module> -j4
# Run the test binary and capture the CSR output:
./<module_test_binary> 2>&1 | grep -A2 "BEGIN CERTIFICATE REQUEST\|base64\|golden"
# Copy the new base64 value into the test header
```

**Detection:**
```bash
# Look for hardcoded base64 or PEM strings in test files:
grep -rn "EwJ\|MFox\|BEGIN CERTIFICATE REQUEST\|BEGIN CERTIFICATE" <module>/tests/ 2>/dev/null
```

**Modules affected:** Any module generating or comparing X.509/CSR output in tests

---

### std::auto_ptr / boost::auto_ptr → std::unique_ptr (TMOS Modules)

**Problem:** `std::auto_ptr` was deprecated in C++11 and **removed in C++17**. GCC 11 compiles with `-std=gnu++17` by default. Any TMOS module still using `std::auto_ptr` or `boost::auto_ptr` will fail to compile with `error: 'auto_ptr' is not a member of 'std'`.

**Resolution:** Replace every occurrence with `std::unique_ptr`. `auto_ptr` copy-construction transferred ownership, so callers using copy must be updated to `std::move`.

```cpp
// BEFORE (fails with GCC 11 / C++17):
std::auto_ptr<MyClass> ptr(new MyClass());
std::auto_ptr<MyClass> ptr2 = ptr;  // transferred ownership

// AFTER:
std::unique_ptr<MyClass> ptr(new MyClass());
std::unique_ptr<MyClass> ptr2 = std::move(ptr);  // explicit move
```

**Detection:**
```bash
grep -RIn --include="*.cpp" --include="*.cc" --include="*.cxx" --include="*.hpp" --include="*.h" \
    'std::auto_ptr\|boost::auto_ptr\|auto_ptr<' <module_source_path>/
```
Any match is a compile-time error under C++17 — fix all before attempting the build.

**Modules affected:** Any TMOS module with C++ code predating C++11 migration.

---

### throw() Exception Specification → noexcept

**Problem:** Dynamic exception specifications (`throw()`, `throw(SomeException)`) were deprecated in C++11 and **removed in C++17**. GCC 11 emits `error: ISO C++17 does not allow dynamic exception specifications`. The empty-spec `throw()` is most common in TMOS headers declaring virtual methods.

**Resolution:** Replace `throw()` with `noexcept`. Non-empty specs like `throw(std::exception)` should have the spec removed (add a comment noting what is thrown).

```cpp
// BEFORE (fails with GCC 11 / C++17):
virtual void reset() throw();
int computeValue() throw(std::runtime_error);

// AFTER:
virtual void reset() noexcept;
int computeValue();  // throws std::runtime_error
```

**Bulk fix for empty `throw()`:**
```bash
# Detect:
grep -RIn --include="*.cpp" --include="*.cc" --include="*.cxx" --include="*.hpp" --include="*.h" \
    'throw\s*()' <module_source_path>/

# Bulk replace (review result before committing):
find <module_source_path>/ \( -name "*.cpp" -o -name "*.h" -o -name "*.hpp" \) \
    -exec sed -i 's/throw\s*()/noexcept/g' {} +
```

**Modules affected:** Any TMOS module with C++ interfaces/virtual methods written before C++11 (extremely common in older TMOS daemons).

---

### register Keyword Removal

**Problem:** The `register` storage-class keyword was deprecated in C++11 and **removed in C++17**. GCC 11 / C++17 emits `error: ISO C++17 does not allow 'register' storage class specifier`. Common in older TMOS C/C++ inner loops originally written in C style.

**Resolution:** Simply remove the `register` keyword. Modern compilers ignore register hints; the variable behaves identically.

```cpp
// BEFORE (fails with GCC 11 / C++17):
register int i;
register unsigned char *p = buf;

// AFTER:
int i;
unsigned char *p = buf;
```

**Detection and bulk fix:**
```bash
# Detect:
grep -RIn --include="*.cpp" --include="*.cc" --include="*.cxx" --include="*.hpp" --include="*.h" --include="*.c" \
    '\bregister\b' <module_source_path>/

# Bulk remove keyword (review result):
find <module_source_path>/ \( -name "*.cpp" -o -name "*.c" -o -name "*.h" -o -name "*.hpp" \) \
    -exec sed -i 's/\bregister\b //g' {} +
```

**Note:** Do not remove `register` from inline assembly (`asm` blocks) — those use different syntax.

**Modules affected:** Any TMOS module with C/C++ code written before C++11, especially those with tight inner loops.

---

### std::iterator Base Class Deprecated (C++17)

**Problem:** Deriving from `std::iterator<...>` to define custom iterators was deprecated in C++17. GCC 11 emits `warning: 'struct std::iterator<...>' is deprecated [-Wdeprecated-declarations]`. With `-Werror` this becomes a build failure.

**Resolution:** Remove the `std::iterator<>` base class and declare the five iterator typedef members directly in the class body.

```cpp
// BEFORE (deprecated in C++17):
#include <iterator>
class MyIterator : public std::iterator<std::forward_iterator_tag, int> {
    // iterator_category, value_type, etc. inherited from base
};

// AFTER:
class MyIterator {
public:
    using iterator_category = std::forward_iterator_tag;
    using value_type        = int;
    using difference_type   = std::ptrdiff_t;
    using pointer           = int*;
    using reference         = int&;
    // ... iterator methods unchanged
};
```

**Detection:**
```bash
grep -RIn --include="*.cpp" --include="*.cc" --include="*.cxx" --include="*.hpp" --include="*.h" \
    ': public std::iterator\|: protected std::iterator' <module_source_path>/
```

**Modules affected:** Any TMOS module implementing custom STL-compatible iterators (container wrappers, range adapters).

---

### readdir_r() Deprecated — Use readdir() Instead

**Problem:** `readdir_r()` was deprecated in glibc 2.24 (Rocky Linux 8 ships glibc 2.28). GCC 11 emits `-Wdeprecated-declarations` for custom code using it directly. This warning also appears from inside boost/filesystem internals (not fixable by the TMOS module author). Custom TMOS code using `readdir_r()` must be migrated.

**Background:** `readdir_r()` was designed for thread-safe directory traversal, but POSIX deprecated it because `readdir()` is itself thread-safe per-`DIR*` stream on glibc 2.24+ (each `DIR*` has its own internal lock).

**Resolution:**
```cpp
// BEFORE:
dirent entry, *result;
while (readdir_r(dir, &entry, &result) == 0 && result != nullptr) {
    // process entry
}

// AFTER:
dirent *entry;
while ((entry = readdir(dir)) != nullptr) {
    // readdir() is thread-safe per-DIR on glibc 2.24+
}
```

**Detection:**
```bash
grep -RIn --include="*.cpp" --include="*.cc" --include="*.cxx" --include="*.c" --include="*.h" --include="*.hpp" \
    '\breaddir_r\s*(' <module_source_path>/
```

**Note:** If warnings come from `boost/filesystem/src/operations.cpp`, they are not in TMOS source and cannot be directly fixed. Suppress `-Wdeprecated-declarations` scoped to that translation unit, or ignore as warnings if `-Werror` is not in effect for that path.

**Modules affected:** Any TMOS module doing custom directory scanning (plug-in loaders, config file scanners, log rotation utilities).


---

## Boost 1.66 Under GCC 11: Suppress Warnings via -isystem, Not -Wno-error

**Domain:** GCC 11 / Boost 1.66 (devfs headers)  
**Applies to:** Any TMOS module that includes Boost headers from `devfs_x86_64` and builds with `-Werror`

**Symptoms — two hard build failures:**
1. `boost/math/special_functions/fpclassify.hpp`: `error: "_GLIBCXX_USE_C99_FP_MACROS_DYNAMIC" is not defined [-Werror=undef]`  
   *GCC 11 removed this macro from libstdc++; Boost 1.66 uses a bare `#if` without `defined()`.*
2. `boost/concept/detail/general.hpp`: `error: 'this' pointer is null [-Werror=nonnull]`  
   *Boost 1.66 concept-checking uses `((Model*)0)->` pattern; GCC 11 flags this as nonnull.*

**Resolution:**  
Use `-isystem` instead of `-I` for the Boost devfs include path. GCC treats `-isystem` paths as system headers and suppresses all warnings from them — warnings in the module's own code remain fully active.

```makefile
# WRONG — suppresses these warning classes globally (masks real bugs in module code):
# CXXFLAGS += -Wno-error=undef -Wno-error=nonnull

# CORRECT — suppress warnings only from the Boost devfs headers:
CXXFLAGS += -isystem $(DEVFS)/usr/include/boost
# (remove any corresponding -I $(DEVFS)/usr/include/boost)
```

> **Superset path caveat:** If `CFLAGS`/`CXXFLAGS` include a superset path such as `-I $(DEVFS)/usr/include` that already covers `$(DEVFS)/usr/include/boost`, changing only the Boost-specific entry to `-isystem` will **not** suppress the warnings — GCC finds the headers via the broader `-I` path first. In that case, **also** change the superset path to `-isystem`:
> ```makefile
> # Both the superset AND the specific path must use -isystem:
> CXXFLAGS += -isystem $(DEVFS)/usr/include
> CXXFLAGS += -isystem $(DEVFS)/usr/include/boost
> # (remove the corresponding -I entries for both)
> ```
> Check for superset paths: `grep -n '\-I.*DEVFS\|\-I.*devfs' <module>/Makefile <module>/*.mk 2>/dev/null`

Also applies to any other uneditable third-party devfs include path (e.g., CxxTest — see CxxTest section).

**Detection:**
```bash
grep -rn "\-I.*devfs.*boost\|\-I.*DEVFS.*boost" <module>/Makefile <module>/*.mk 2>/dev/null
```

---

## C++17 Removed Features: auto_ptr, register, throw() in TMOS Modules

**Domain:** GCC 11 Migration / C++17  
**Applies to:** Any TMOS C++ module with code predating C++11

**Problem:** Three features removed in C++17 (which GCC 11 enforces by default) produce **hard compile errors**:
1. `std::auto_ptr` / `boost::auto_ptr` → `error: 'auto_ptr' is not a member of 'std'`
2. `throw()` dynamic exception specs → `error: ISO C++17 does not allow dynamic exception specifications`
3. `register` storage class → `error: ISO C++17 does not allow 'register' storage class specifier`

**Resolution:**
- `std::auto_ptr` → `std::unique_ptr`; update copy-construction to `std::move`
- `throw()` → `noexcept`; non-empty specs → remove and document in comment
- `register` → remove keyword entirely

**Pre-build detection (run before first build attempt):**
```bash
grep -RIn --include="*.cpp" --include="*.h" --include="*.hpp" 'auto_ptr<\|std::auto_ptr\|boost::auto_ptr' <src>/
grep -RIn --include="*.cpp" --include="*.h" --include="*.hpp" 'throw\s*()' <src>/
grep -RIn --include="*.c" --include="*.cpp" --include="*.h" '\bregister\b' <src>/
```
**Cross-module applicability:** YES — extremely common in older TMOS daemons.

---

## std::iterator Base Class Deprecated in C++17

**Domain:** GCC 11 Migration / C++17  
**Applies to:** Any TMOS module defining custom iterators by inheriting from `std::iterator`

**Problem:** Deriving from `std::iterator<Category, Type>` is deprecated in C++17. GCC 11 emits `-Wdeprecated-declarations`; with `-Werror` this causes a build failure.

**Resolution:** Remove the base class and inline the five typedef members directly:
```cpp
// Before:  class MyIter : public std::iterator<std::forward_iterator_tag, int> { ...
// After:
using iterator_category = std::forward_iterator_tag;
using value_type        = int;
using difference_type   = std::ptrdiff_t;
using pointer           = int*;
using reference         = int&;
```

**Detection:**
```bash
grep -RIn --include="*.cpp" --include="*.h" --include="*.hpp" \
    ': public std::iterator\|: protected std::iterator' <src>/
```

---

## glibc 2.28 Removed/Deprecated APIs (CentOS 6/7 → Rocky Linux 8)

**Domain:** GCC 11 Migration / glibc 2.28  
**Applies to:** Any TMOS module with C/C++ code running on CentOS 6 (glibc 2.12) or CentOS 7 (glibc 2.17)

Rocky Linux 8 ships **glibc 2.28**. The following APIs were removed or deprecated and must be migrated.

### gets() Removed in glibc 2.28

**Problem:** `gets()` was **removed entirely** in glibc 2.28 → linker error `undefined reference to 'gets'`.

**Resolution:**
```c
// BEFORE:  gets(buf);
// AFTER:
if (fgets(buf, sizeof(buf), stdin) == NULL) { /* handle EOF/error */ }
buf[strcspn(buf, "\n")] = '\0';  // strip trailing newline
```
**Detection:** `grep -RIn '\bgets\s*(' <src>/ --include="*.c" --include="*.cpp"`

### mktemp() / tmpnam() — Use mkstemp()

**Problem:** Deprecated (TOCTOU race), glibc 2.28 warns `-Wdeprecated-declarations`.

**Resolution:**
```c
char tmpfile[] = "/tmp/myXXXXXX";
int fd = mkstemp(tmpfile);
// use fd; close and unlink when done
```
**Detection:** `grep -RIn '\bmktemp\s*(\|\btmpnam\s*(' <src>/`

### boost::filesystem::file_size() Returns uintmax_t

**Problem:** Returns 64-bit `uintmax_t`; storing in `int` truncates for files >2GB.

**Resolution:** Use `uintmax_t file_sz = boost::filesystem::file_size(path);`

**Detection:**
```bash
grep -RIn '=\s*boost::filesystem::file_size\|=\s*fs::file_size' <src>/ \
  | grep -v 'uintmax_t\|uint64_t\|size_t'
```

### strerror_r() GNU vs XSI Variant

**Problem:** glibc default builds use the **GNU variant** (returns `char*`). Code expecting the XSI variant (returns `int`) silently misbehaves when `_GNU_SOURCE` is defined.

**Resolution:**
```cpp
char errbuf[256];
char *msg = strerror_r(errno, errbuf, sizeof(errbuf));
// use msg (may point into errbuf or a static string), not errbuf directly
```
**Detection:** `grep -RIn '\bstrerror_r\s*(' <src>/ | grep -v 'char\s*\*\|const char'`

### Pre-Build glibc 2.28 Scan Checklist

```bash
MODULE_SRC=<module_source_path>
echo "=== glibc 2.28 API scan ==="
echo "[1] gets() REMOVED:"; grep -RIn --include="*.c" --include="*.cpp" '\bgets\s*(' ${MODULE_SRC}/
echo "[2] mktemp/tmpnam deprecated:"; grep -RIn --include="*.c" --include="*.cpp" '\bmktemp\s*(\|\btmpnam\s*(' ${MODULE_SRC}/
echo "[3] readdir_r deprecated:"; grep -RIn --include="*.c" --include="*.cpp" --include="*.h" '\breaddir_r\s*(' ${MODULE_SRC}/
echo "[4] file_size in int:"; grep -RIn --include="*.cpp" '=\s*boost::filesystem::file_size\|=\s*fs::file_size' ${MODULE_SRC}/ | grep -v 'uintmax_t\|uint64_t\|size_t'
echo "[5] strerror_r return ignored:"; grep -RIn --include="*.c" --include="*.cpp" '\bstrerror_r\s*(' ${MODULE_SRC}/ | grep -v 'char\s*\*\|const char'
echo "=== scan complete ==="
```

---

## boost::format() With %u/%d and uint64_t/int64_t — Use PRI* Macros

**Domain:** GCC 11 Migration / LP64  
**Applies to:** Any TMOS module using `boost::format()` with 64-bit integer arguments

**Problem:** `boost::format("%u") % uint64_val` silently truncates on LP64 because `%u` expects 32-bit `unsigned int`.

**Resolution:**
```cpp
#include <inttypes.h>
str = boost::format("%" PRIu64) % val;   // CORRECT
// Also: PRId64 for int64_t, PRIx64 for hex, PRIo64 for octal
```

**Detection:**
```bash
grep -RIn --include='*.cpp' --include='*.cc' --include='*.h' \
  'boost::format.*"%[duxo]"' <module>/
```

---

## int Buffer Cursor Compared Against ssize_t Length — Use ssize_t Throughout

**Domain:** GCC 11 Migration / LP64  
**Applies to:** Any TMOS module using `int pos`/`int offset` as a buffer cursor against a `ssize_t` length

**Pattern:**
```cpp
ssize_t len = read(fd, buf, sizeof(buf));
int pos = 0;              // WRONG — should be ssize_t
while (pos < len) { ... } // signed/unsigned compare + truncation risk
```
**Fix:** declare `ssize_t pos = 0;`

> Silent bug — no warning unless `-Wsign-compare` is active.

**Detection:**
```bash
grep -RIn --include='*.cpp' --include='*.c' \
  'int[[:space:]]\+pos[[:space:]]*=[[:space:]]*0\|int[[:space:]]\+offset[[:space:]]*=[[:space:]]*0' <module>/
```

---

## Signed Integer Shift 1<<N Should Be 1U<<N for Bitmask Expressions

**Domain:** GCC 11 Migration / LP64  
**Applies to:** Any TMOS module using bitmask expressions with bare integer literals

**Problem:** `1<<N` where N ≥ 31 shifts into the sign bit → undefined behaviour.

**Fix:**
```cpp
if (flags & (1U<<24)) { ... }              // CORRECT
static const unsigned int MASK = 1U<<24;  // CORRECT
static const uint64_t MASK64 = UINT64_C(1)<<48;  // 64-bit mask
```

**Detection:**
```bash
grep -RIn --include='*.cpp' --include='*.c' --include='*.h' '[^U](1<<[0-9]\+)' <module>/
```
