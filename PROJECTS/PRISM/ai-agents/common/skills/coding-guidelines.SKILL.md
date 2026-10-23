---
name: coding-guidelines
description: Coding standards and best practices for code review across multiple programming languages including C/C++, Python, JavaScript, Shell scripts, and configuration files.
applyTo: ["**/*"]
---

# Coding Guidelines for Code Review

This skill provides coding standards and best practices to be used during code review processes.

## General Principles

1. **Readability First**: Code should be written for humans to read and understand
2. **Consistency**: Follow established patterns within the codebase
3. **Simplicity**: Prefer simple solutions over complex ones (KISS principle)
4. **DRY**: Don't Repeat Yourself - avoid code duplication
5. **Single Responsibility**: Each function/class should have one clear purpose
6. **Error Handling**: Always handle errors explicitly and gracefully
7. **Security**: Never trust user input; validate and sanitize all external data
8. **Performance**: Write efficient code, but prioritize correctness first

## C/C++ Guidelines

### Memory Management
- Always pair `malloc()` with `free()`, `new` with `delete`, `new[]` with `delete[]`
- Initialize pointers to `NULL`/`nullptr` after freeing
- Check return values from memory allocation functions
- Use RAII (Resource Acquisition Is Initialization) in C++
- Avoid manual memory management where smart pointers can be used

### Pointer Safety
- Always check pointers for `NULL`/`nullptr` before dereferencing
- Use `const` pointers when the pointed-to data should not be modified
- Avoid pointer arithmetic unless absolutely necessary
- Prefer references over pointers in C++ when possible

### Type Safety
- Avoid C-style casts in C++; use `static_cast`, `dynamic_cast`, `const_cast`, `reinterpret_cast`
- Use appropriate integer types for 64-bit compatibility: `size_t`, `intptr_t`, `uintptr_t`
- Avoid mixing signed and unsigned types in comparisons
- Use explicit type conversions to show intent

### 64-bit Architecture Compatibility
- Never cast pointers to `int` or `long`; use `intptr_t` or `uintptr_t`
- Use `size_t` for sizes and array indices
- Use `PRId64`, `PRIu64` format specifiers for 64-bit integers
- Be aware of structure padding and alignment
- Use `sizeof()` rather than hardcoded sizes

### Header Files
- Use include guards: `#ifndef FILE_H` / `#define FILE_H` / `#endif` or `#pragma once`
- Minimize includes in headers; use forward declarations where possible
- Keep public API in headers, implementation details in source files
- Order includes: standard library, third-party, local headers

### Code Style
- Maximum line length: 100-120 characters
- Consistent indentation (typically 4 spaces or 1 tab)
- Braces on same line (K&R) or next line (Allman) - be consistent
- Use meaningful variable names - avoid single-letter except for loop counters
- Function names should be verbs (e.g., `calculate_total()`)

## Python Guidelines

### PEP 8 Compliance
- Maximum line length: 79 characters for code, 72 for docstrings
- 4 spaces per indentation level (never tabs)
- Two blank lines between top-level functions and classes
- One blank line between methods
- Use snake_case for functions and variables, PascalCase for classes
- Constants in UPPER_CASE

### Code Organization
- Imports order: standard library, third-party, local application/library
- One import per line for `import` statements
- Group imports: stdlib, third-party, local, with blank line between groups
- Avoid wildcard imports (`from module import *`)

### Best Practices
- Use list comprehensions for simple transformations
- Use context managers (`with` statement) for resource management
- Prefer `f-strings` for string formatting (Python 3.6+)
- Use `enumerate()` instead of manual counter in loops
- Use `zip()` to iterate over multiple sequences
- Add type hints for function parameters and return values

### Error Handling
- Catch specific exceptions, not bare `except:`
- Use `finally` or context managers for cleanup
- Don't silently ignore exceptions
- Provide meaningful error messages

### Documentation
- Docstrings for all public modules, functions, classes, and methods
- Use triple double-quotes for docstrings
- First line should be a brief summary
- Follow Google, NumPy, or reStructuredText style

## JavaScript/TypeScript Guidelines

### Modern JavaScript (ES6+)
- Use `const` by default, `let` when reassignment needed, never `var`
- Use arrow functions for callbacks and short functions
- Use template literals for string interpolation
- Use destructuring for object/array access
- Use async/await for asynchronous operations

### TypeScript-Specific
- Add type annotations for function parameters and return types
- Use interfaces for object shapes
- Avoid `any` type; use `unknown` if type is truly unknown
- Use strict mode (`"strict": true` in tsconfig.json)
- Leverage type inference where it improves readability

### Code Style
- Maximum line length: 100-120 characters
- 2 spaces for indentation
- Use semicolons consistently (or omit consistently with ASI rules)
- Use single quotes for strings (or double quotes - be consistent)
- Use camelCase for variables and functions, PascalCase for classes

### Best Practices
- Avoid callback hell; use promises or async/await
- Handle promise rejections with `.catch()` or try/catch
- Use strict equality operators (`===`, `!==`) instead of loose (`==`, `!=`)
- Validate function arguments
- Avoid modifying function arguments

## Shell Script Guidelines

### Bash Best Practices
- Start with shebang: `#!/bin/bash` or `#!/usr/bin/env bash`
- Use `set -e` to exit on error
- Use `set -u` to exit on undefined variable
- Use `set -o pipefail` to catch errors in pipelines
- Use `set -x` for debugging (or remove in production)

### Variable Handling
- Quote all variable expansions: `"$var"` not `$var`
- Use `${var}` for clarity when concatenating
- Use `readonly` or `declare -r` for constants
- Use `local` for function-local variables
- Use uppercase for environment/global variables, lowercase for local

### Conditionals and Tests
- Use `[[ ]]` instead of `[ ]` for tests (in bash)
- Quote variables in tests: `[[ "$var" == "value" ]]`
- Use `-z` for empty string checks, `-n` for non-empty
- Use `-f` for file existence, `-d` for directory existence

### Functions
- Define functions before use
- Use `function name() { }` or `name() { }` syntax consistently
- Return meaningful exit codes (0 for success, non-zero for errors)
- Use `local` for all function variables

### Error Handling
- Check exit codes: `if command; then ... fi` or `command || handle_error`
- Provide meaningful error messages to stderr: `echo "Error" >&2`
- Exit with appropriate error codes
- Clean up temporary files with `trap` on EXIT

## Makefile Guidelines

### Variables
- Use uppercase for standard variables: `CC`, `CFLAGS`, `LDFLAGS`
- Use `:=` for immediate assignment, `=` for recursive
- Use `?=` for conditional assignment (set only if not already set)
- Use `$(var)` syntax for variable expansion

### Targets
- Declare phony targets: `.PHONY: clean all install`
- Use pattern rules for similar targets
- Specify dependencies accurately
- Use automatic variables: `$@` (target), `$<` (first prerequisite), `$^` (all prerequisites)

### Best Practices
- Use tabs for recipe indentation (required by Make)
- One command per line, or use `;` and `\` for continuation
- Use `@` prefix to silence echoing of commands
- Check for required tools: `$(if $(shell which gcc),,$(error gcc not found))`
- Support parallel builds (`-j` flag)

### Path Handling
- Use variables for paths: `$(PREFIX)`, `$(DESTDIR)`
- Use `/` for path separators (works on Unix and Windows with proper Make)
- Quote paths that might contain spaces: `"$(PATH_VAR)"`

## Security Guidelines (All Languages)

### Input Validation
- Validate all user input at boundaries
- Sanitize data before use in commands, queries, or display
- Use parameterized queries/prepared statements for SQL
- Escape shell commands or avoid shell invocation
- Validate input length, type, format, and range

### Authentication & Authorization
- Never store passwords in plain text
- Use strong hashing algorithms (bcrypt, Argon2, PBKDF2)
- Implement rate limiting for authentication attempts
- Check permissions before granting access
- Use principle of least privilege

### Sensitive Data
- Never commit secrets, API keys, or passwords to version control
- Use environment variables or secrets management for sensitive configuration
- Mask sensitive data in logs
- Securely wipe sensitive data from memory when finished
- Use encrypted connections (TLS/SSL) for network communication

### Common Vulnerabilities
- Prevent SQL injection with parameterized queries
- Prevent XSS with proper output encoding
- Prevent CSRF with tokens
- Prevent path traversal with validation
- Avoid buffer overflows with bounds checking

## Code Review Checklist

### Functionality
- [ ] Does the code do what it's supposed to do?
- [ ] Are edge cases handled?
- [ ] Are error conditions handled properly?
- [ ] Is the logic correct and complete?

### Code Quality
- [ ] Is the code readable and understandable?
- [ ] Is the code properly documented?
- [ ] Is there duplicated code that should be refactored?
- [ ] Are functions/methods a reasonable size?
- [ ] Are names meaningful and follow conventions?

### Testing
- [ ] Are there unit tests for new functionality?
- [ ] Do tests cover edge cases and error conditions?
- [ ] Do all tests pass?
- [ ] Is test coverage adequate?

### Performance
- [ ] Are there obvious performance issues?
- [ ] Are algorithms efficient for expected data sizes?
- [ ] Are resources properly managed and released?
- [ ] Are there unnecessary operations or allocations?

### Security
- [ ] Is user input validated?
- [ ] Are there potential security vulnerabilities?
- [ ] Is sensitive data properly protected?
- [ ] Are authentication/authorization checks in place?

### Maintainability
- [ ] Is the code organized logically?
- [ ] Are changes backward compatible (if required)?
- [ ] Is the code consistent with existing codebase?
- [ ] Are there proper abstractions without over-engineering?
