---
name: openssl-migration
description: Domain knowledge for migrating applications from OpenSSL 1.0.1 to OpenSSL 1.1.1k. Covers API changes, deprecated functions, structure opaqueness, compilation fixes, and security improvements.
applyTo: ["**/*.c", "**/*.cpp", "**/*.h", "**/*.hpp", "**/Makefile", "**/*.mk", "**/*.spec"]
---

# OpenSSL Migration Guide: 1.0.1 → 1.1.1k

This skill provides comprehensive guidance for migrating applications from OpenSSL 1.0.1 to OpenSSL 1.1.1k, covering breaking changes, API updates, and best practices.

## Overview of Changes

OpenSSL 1.1.1k introduced significant architectural changes from 1.0.1:

1. **Opaque Structures**: Most internal structures are now opaque and require accessor functions
2. **Thread Safety**: Improved thread safety with automatic initialization
3. **TLS 1.3 Support**: Added support for TLS 1.3 protocol
4. **Deprecated APIs**: Many old functions deprecated or removed
5. **Simplified Initialization**: Automatic library initialization (no manual `SSL_library_init()` needed)
6. **Memory Management**: Changes to how objects are created and freed

## Critical Breaking Changes

### 1. Structure Opacity

**OpenSSL 1.0.1** exposed internal structure members directly:
```c
// OLD - Direct access (NO LONGER WORKS)
SSL_CTX *ctx = SSL_CTX_new(SSLv23_method());
ctx->options |= SSL_OP_NO_SSLv2;

EVP_MD_CTX md_ctx;
EVP_MD_CTX_init(&md_ctx);

HMAC_CTX hmac_ctx;
HMAC_CTX_init(&hmac_ctx);

X509 *cert = ...;
char *subject = cert->name;
```

**OpenSSL 1.1.1k** requires accessor functions:
```c
// NEW - Use accessor functions
SSL_CTX *ctx = SSL_CTX_new(TLS_method());
SSL_CTX_set_options(ctx, SSL_OP_NO_SSLv2);

EVP_MD_CTX *md_ctx = EVP_MD_CTX_new();
// Use md_ctx...
EVP_MD_CTX_free(md_ctx);

HMAC_CTX *hmac_ctx = HMAC_CTX_new();
// Use hmac_ctx...
HMAC_CTX_free(hmac_ctx);

X509 *cert = ...;
X509_NAME *subject_name = X509_get_subject_name(cert);
```

### 2. Initialization and Cleanup

**OpenSSL 1.0.1** required explicit initialization:
```c
// OLD - Manual initialization required
SSL_library_init();
SSL_load_error_strings();
OpenSSL_add_all_algorithms();
ERR_load_BIO_strings();
ERR_load_crypto_strings();

// Manual cleanup
EVP_cleanup();
ERR_free_strings();
```

**OpenSSL 1.1.1k** auto-initializes:
```c
// NEW - Automatic initialization (no code needed)
// Library initializes automatically on first use

// Manual initialization still available if needed:
OPENSSL_init_ssl(0, NULL);
OPENSSL_init_crypto(0, NULL);

// Cleanup (optional, automatic at exit)
// No explicit cleanup needed in most cases
```

### 3. Method Functions

**OpenSSL 1.0.1** had protocol-specific methods:
```c
// OLD - Protocol-specific methods
SSL_CTX *ctx = SSL_CTX_new(SSLv23_method());     // Flexible
SSL_CTX *ctx = SSL_CTX_new(SSLv3_method());      // SSLv3 only
SSL_CTX *ctx = SSL_CTX_new(TLSv1_method());      // TLS 1.0 only
SSL_CTX *ctx = SSL_CTX_new(TLSv1_2_method());    // TLS 1.2 only

// Server/client specific
SSL_CTX *ctx = SSL_CTX_new(SSLv23_server_method());
SSL_CTX *ctx = SSL_CTX_new(TLSv1_2_client_method());
```

**OpenSSL 1.1.1k** uses unified methods:
```c
// NEW - Unified methods (recommended)
SSL_CTX *ctx = SSL_CTX_new(TLS_method());          // Auto-negotiates TLS version
SSL_CTX *ctx = SSL_CTX_new(TLS_server_method());   // Server-specific
SSL_CTX *ctx = SSL_CTX_new(TLS_client_method());   // Client-specific

// Set minimum/maximum protocol versions:
SSL_CTX_set_min_proto_version(ctx, TLS1_2_VERSION);
SSL_CTX_set_max_proto_version(ctx, TLS1_3_VERSION);

// Old methods still available but deprecated
SSL_CTX *ctx = SSL_CTX_new(TLS_method()); // Use this instead
```

## Common API Migrations

### 4. EVP_MD_CTX Changes

**OpenSSL 1.0.1**:
```c
// OLD - Stack allocation
EVP_MD_CTX md_ctx;
EVP_MD_CTX_init(&md_ctx);
EVP_DigestInit_ex(&md_ctx, EVP_sha256(), NULL);
// ... use md_ctx ...
EVP_MD_CTX_cleanup(&md_ctx);
```

**OpenSSL 1.1.1k**:
```c
// NEW - Heap allocation
EVP_MD_CTX *md_ctx = EVP_MD_CTX_new();
if (!md_ctx) {
    // Handle allocation error
}
EVP_DigestInit_ex(md_ctx, EVP_sha256(), NULL);
// ... use md_ctx ...
EVP_MD_CTX_free(md_ctx);
```

### 5. HMAC_CTX Changes

**OpenSSL 1.0.1**:
```c
// OLD - Stack allocation
HMAC_CTX hmac_ctx;
HMAC_CTX_init(&hmac_ctx);
HMAC_Init_ex(&hmac_ctx, key, key_len, EVP_sha256(), NULL);
HMAC_Update(&hmac_ctx, data, data_len);
HMAC_Final(&hmac_ctx, digest, &digest_len);
HMAC_CTX_cleanup(&hmac_ctx);
```

**OpenSSL 1.1.1k**:
```c
// NEW - Heap allocation
HMAC_CTX *hmac_ctx = HMAC_CTX_new();
if (!hmac_ctx) {
    // Handle allocation error
}
HMAC_Init_ex(hmac_ctx, key, key_len, EVP_sha256(), NULL);
HMAC_Update(hmac_ctx, data, data_len);
HMAC_Final(hmac_ctx, digest, &digest_len);
HMAC_CTX_free(hmac_ctx);
```

### 6. EVP_CIPHER_CTX Changes

**OpenSSL 1.0.1**:
```c
// OLD - Stack allocation
EVP_CIPHER_CTX cipher_ctx;
EVP_CIPHER_CTX_init(&cipher_ctx);
EVP_EncryptInit_ex(&cipher_ctx, EVP_aes_256_cbc(), NULL, key, iv);
// ... encryption ...
EVP_CIPHER_CTX_cleanup(&cipher_ctx);
```

**OpenSSL 1.1.1k**:
```c
// NEW - Heap allocation
EVP_CIPHER_CTX *cipher_ctx = EVP_CIPHER_CTX_new();
if (!cipher_ctx) {
    // Handle allocation error
}
EVP_EncryptInit_ex(cipher_ctx, EVP_aes_256_cbc(), NULL, key, iv);
// ... encryption ...
EVP_CIPHER_CTX_free(cipher_ctx);
```

### 7. RSA Key Generation

**OpenSSL 1.0.1**:
```c
// OLD - Direct RSA structure manipulation
RSA *rsa = RSA_generate_key(2048, RSA_F4, NULL, NULL);
if (!rsa) {
    // Handle error
}
// Access members directly
rsa->n = ...; // NO LONGER WORKS

RSA_free(rsa);
```

**OpenSSL 1.1.1k**:
```c
// NEW - Use accessor functions
RSA *rsa = RSA_new();
BIGNUM *bne = BN_new();
if (BN_set_word(bne, RSA_F4) != 1) {
    // Handle error
}
if (RSA_generate_key_ex(rsa, 2048, bne, NULL) != 1) {
    // Handle error
}

// Get components using accessors
const BIGNUM *n, *e, *d;
RSA_get0_key(rsa, &n, &e, &d);

BN_free(bne);
RSA_free(rsa);
```

### 8. DSA and DH Key Access

**OpenSSL 1.0.1**:
```c
// OLD - Direct member access
DSA *dsa = ...;
BIGNUM *p = dsa->p;
BIGNUM *q = dsa->q;
BIGNUM *g = dsa->g;

DH *dh = ...;
BIGNUM *dh_p = dh->p;
```

**OpenSSL 1.1.1k**:
```c
// NEW - Use getter functions
DSA *dsa = ...;
const BIGNUM *p, *q, *g;
DSA_get0_pqg(dsa, &p, &q, &g);

const BIGNUM *pub_key, *priv_key;
DSA_get0_key(dsa, &pub_key, &priv_key);

DH *dh = ...;
const BIGNUM *dh_p, *dh_q, *dh_g;
DH_get0_pqg(dh, &dh_p, &dh_q, &dh_g);
```

### 9. X.509 Certificate Access

**OpenSSL 1.0.1**:
```c
// OLD - Direct structure access
X509 *cert = ...;
ASN1_INTEGER *serial = cert->cert_info->serialNumber;
X509_NAME *issuer = cert->cert_info->issuer;
X509_NAME *subject = cert->cert_info->subject;
```

**OpenSSL 1.1.1k**:
```c
// NEW - Use accessor functions
X509 *cert = ...;
ASN1_INTEGER *serial = X509_get_serialNumber(cert);
X509_NAME *issuer = X509_get_issuer_name(cert);
X509_NAME *subject = X509_get_subject_name(cert);
long version = X509_get_version(cert);
```

### 10. BIO Changes

**OpenSSL 1.0.1**:
```c
// OLD - Some BIO functions had different names
BIO *bio = BIO_new(BIO_s_mem());
// Direct member access was sometimes used
```

**OpenSSL 1.1.1k**:
```c
// NEW - More consistent API
BIO *bio = BIO_new(BIO_s_mem());
// Use BIO accessor functions
long len = BIO_get_mem_data(bio, &data);
BIO_free(bio);
```

## Deprecated and Removed Functions

### Functions to Replace:

| Old Function (1.0.1) | New Function (1.1.1k) | Notes |
|----------------------|------------------------|-------|
| `RSA_generate_key()` | `RSA_generate_key_ex()` | New function requires pre-allocated RSA structure |
| `EVP_MD_CTX_init()` | `EVP_MD_CTX_new()` | Allocates on heap instead of stack |
| `EVP_MD_CTX_cleanup()` | `EVP_MD_CTX_free()` | Matches new allocation pattern |
| `EVP_CIPHER_CTX_init()` | `EVP_CIPHER_CTX_new()` | Allocates on heap |
| `EVP_CIPHER_CTX_cleanup()` | `EVP_CIPHER_CTX_free()` | Matches new allocation pattern |
| `HMAC_CTX_init()` | `HMAC_CTX_new()` | Allocates on heap |
| `HMAC_CTX_cleanup()` | `HMAC_CTX_free()` | Matches new allocation pattern |
| `SSL_library_init()` | Automatic (no call needed) | Or use `OPENSSL_init_ssl()` |
| `OpenSSL_add_all_algorithms()` | Automatic (no call needed) | Or use `OPENSSL_init_crypto()` |
| `ERR_load_crypto_strings()` | Automatic (no call needed) | Error strings load automatically |
| `SSLv23_method()` | `TLS_method()` | Use unified TLS method |
| `TLSv1_2_method()` | `TLS_method()` + version setting | More flexible |

### Removed/Unavailable in 1.1.1k:

- `SSLv2_method()` - SSLv2 is completely removed (insecure)
- `SSLv3_method()` - SSLv3 should not be used (insecure)
- Direct structure member access (e.g., `ctx->options`, `rsa->n`, `x509->name`)
- `CRYPTO_num_locks()`, `CRYPTO_set_locking_callback()` - Thread locking is automatic

## Compilation and Build Changes

### Compiler Flags and Defines

**For backward compatibility during transition:**
```makefile
# Define this to use deprecated APIs during migration
CFLAGS += -DOPENSSL_API_COMPAT=0x10100000L

# After full migration, define this to ensure no deprecated API usage
CFLAGS += -DOPENSSL_API_COMPAT=0x10101000L
```

### Library Linking

**OpenSSL 1.0.1**:
```makefile
LDFLAGS += -lssl -lcrypto
```

**OpenSSL 1.1.1k** (same, but verify library paths):
```makefile
# May need to specify library path if multiple versions installed
LDFLAGS += -L/usr/local/lib -lssl -lcrypto

# Or use pkg-config
CFLAGS += $(shell pkg-config --cflags openssl)
LDFLAGS += $(shell pkg-config --libs openssl)
```

### Include Path Changes

Generally no changes needed, but verify:
```c
#include <openssl/ssl.h>
#include <openssl/err.h>
#include <openssl/evp.h>
#include <openssl/hmac.h>
#include <openssl/rsa.h>
#include <openssl/x509.h>
```

### Version Detection in Code

```c
// Check OpenSSL version at compile time
#if OPENSSL_VERSION_NUMBER >= 0x10101000L
    // OpenSSL 1.1.1 or later code
    EVP_MD_CTX *ctx = EVP_MD_CTX_new();
#else
    // OpenSSL 1.0.x code
    EVP_MD_CTX ctx;
    EVP_MD_CTX_init(&ctx);
#endif

// Check version at runtime
printf("OpenSSL version: %s\n", OpenSSL_version(OPENSSL_VERSION));
```

## Migration Strategy

### Step 1: Identify All OpenSSL Usage

Search for all OpenSSL includes and function calls:
```bash
grep -r "#include <openssl/" .
grep -r "SSL_\|EVP_\|HMAC_\|RSA_\|X509_\|BIO_\|DH_\|DSA_" . --include="*.c" --include="*.cpp" --include="*.h"
```

### Step 2: Structure Access Patterns

Find all direct structure member access (this will break):
```bash
grep -r "->options\|->n\|->e\|->d\|->p\|->q\|->g\|->name\|->cert_info" . --include="*.c" --include="*.cpp"
```

### Step 3: Context Initialization Patterns

Find old initialization patterns:
```bash
grep -r "EVP_MD_CTX_init\|EVP_CIPHER_CTX_init\|HMAC_CTX_init" . --include="*.c" --include="*.cpp"
grep -r "EVP_MD_CTX_cleanup\|EVP_CIPHER_CTX_cleanup\|HMAC_CTX_cleanup" . --include="*.c" --include="*.cpp"
```

### Step 4: Old Method Calls

Find deprecated method calls:
```bash
grep -r "SSLv23_method\|SSLv3_method\|TLSv1_method\|TLSv1_2_method" . --include="*.c" --include="*.cpp"
```

### Step 5: Initialization Code

Find manual initialization:
```bash
grep -r "SSL_library_init\|OpenSSL_add_all_algorithms\|ERR_load_crypto_strings" . --include="*.c" --include="*.cpp"
```

## Common Migration Patterns

### Pattern 1: Convert Stack-Allocated Contexts to Heap

**Before:**
```c
void hash_data(const unsigned char *data, size_t len, unsigned char *output) {
    EVP_MD_CTX ctx;
    EVP_MD_CTX_init(&ctx);
    
    EVP_DigestInit_ex(&ctx, EVP_sha256(), NULL);
    EVP_DigestUpdate(&ctx, data, len);
    EVP_DigestFinal_ex(&ctx, output, NULL);
    
    EVP_MD_CTX_cleanup(&ctx);
}
```

**After:**
```c
int hash_data(const unsigned char *data, size_t len, unsigned char *output) {
    EVP_MD_CTX *ctx = EVP_MD_CTX_new();
    if (!ctx) {
        return 0; // Error: allocation failed
    }
    
    int ret = 0;
    if (EVP_DigestInit_ex(ctx, EVP_sha256(), NULL) != 1)
        goto cleanup;
    if (EVP_DigestUpdate(ctx, data, len) != 1)
        goto cleanup;
    if (EVP_DigestFinal_ex(ctx, output, NULL) != 1)
        goto cleanup;
    
    ret = 1; // Success
    
cleanup:
    EVP_MD_CTX_free(ctx);
    return ret;
}
```

### Pattern 2: Replace Direct Structure Access

**Before:**
```c
void print_rsa_key(RSA *rsa) {
    printf("n = ");
    BN_print_fp(stdout, rsa->n);
    printf("\ne = ");
    BN_print_fp(stdout, rsa->e);
    printf("\n");
}
```

**After:**
```c
void print_rsa_key(RSA *rsa) {
    const BIGNUM *n, *e, *d;
    RSA_get0_key(rsa, &n, &e, &d);
    
    printf("n = ");
    BN_print_fp(stdout, n);
    printf("\ne = ");
    BN_print_fp(stdout, e);
    printf("\n");
}
```

### Pattern 3: Update Initialization Code

**Before:**
```c
int init_ssl_library(void) {
    SSL_library_init();
    SSL_load_error_strings();
    OpenSSL_add_all_algorithms();
    return 1;
}
```

**After:**
```c
int init_ssl_library(void) {
    // Automatic initialization - no code needed
    // Or explicitly:
    OPENSSL_init_ssl(OPENSSL_INIT_LOAD_SSL_STRINGS | 
                     OPENSSL_INIT_LOAD_CRYPTO_STRINGS, NULL);
    return 1;
}
```

### Pattern 4: Update SSL Method Calls

**Before:**
```c
SSL_CTX *create_ssl_context(void) {
    SSL_CTX *ctx = SSL_CTX_new(SSLv23_server_method());
    if (!ctx) {
        return NULL;
    }
    
    // Disable old protocols
    SSL_CTX_set_options(ctx, SSL_OP_NO_SSLv2 | SSL_OP_NO_SSLv3);
    
    return ctx;
}
```

**After:**
```c
SSL_CTX *create_ssl_context(void) {
    SSL_CTX *ctx = SSL_CTX_new(TLS_server_method());
    if (!ctx) {
        return NULL;
    }
    
    // Set minimum TLS version (TLS 1.2 or higher recommended)
    SSL_CTX_set_min_proto_version(ctx, TLS1_2_VERSION);
    
    return ctx;
}
```

## Testing Recommendations

### 1. Compile-Time Testing

Compile with warnings enabled:
```bash
gcc -Wall -Wextra -Werror -c your_code.c -I/usr/include/openssl
```

Test with different API compatibility levels:
```bash
# Allow deprecated APIs
gcc -DOPENSSL_API_COMPAT=0x10100000L -c your_code.c

# Disallow deprecated APIs
gcc -DOPENSSL_API_COMPAT=0x10101000L -c your_code.c
```

### 2. Runtime Testing

- Test all SSL/TLS connection scenarios
- Verify certificate validation works correctly
- Test different protocol versions (TLS 1.2, TLS 1.3)
- Test encryption/decryption operations
- Test key generation and signing operations
- Check for memory leaks using valgrind:
  ```bash
  valgrind --leak-check=full ./your_application
  ```

### 3. Protocol Testing

Test protocol negotiation:
```bash
# Test TLS 1.2
openssl s_client -connect yourserver:443 -tls1_2

# Test TLS 1.3
openssl s_client -connect yourserver:443 -tls1_3

# Check supported ciphers
openssl s_client -connect yourserver:443 -cipher 'ALL'
```

## Security Improvements in 1.1.1k

### 1. TLS 1.3 Support

TLS 1.3 is automatically supported and negotiated:
```c
SSL_CTX *ctx = SSL_CTX_new(TLS_method());
// TLS 1.3 will be used if both client and server support it
```

### 2. Stronger Default Ciphers

OpenSSL 1.1.1k has better default cipher suites. Explicitly set secure ciphers:
```c
SSL_CTX_set_cipher_list(ctx, "HIGH:!aNULL:!MD5:!RC4");
SSL_CTX_set_ciphersuites(ctx, "TLS_AES_256_GCM_SHA384:TLS_AES_128_GCM_SHA256");
```

### 3. Automatic Security Defaults

Many insecure options are disabled by default:
- SSLv2 is completely removed
- SSLv3 is disabled by default
- Weak ciphers are not included in default cipher list

### 4. Better Random Number Generation

RAND subsystem improvements provide better entropy:
```c
// Seeding is automatic; manual seeding usually not needed
// But you can still seed if needed:
RAND_add(seed_data, seed_len, entropy_estimate);

// Check if PRNG is seeded
if (RAND_status() != 1) {
    // Not enough entropy
}
```

## Common Pitfalls and Solutions

### Pitfall 1: Memory Leaks from Changed Allocation

**Problem:** Forgetting to convert cleanup calls when converting from stack to heap allocation.

**Solution:** Always pair `_new()` with `_free()`:
```c
// WRONG - Memory leak
EVP_MD_CTX *ctx = EVP_MD_CTX_new();
EVP_MD_CTX_cleanup(ctx); // Wrong function!

// CORRECT
EVP_MD_CTX *ctx = EVP_MD_CTX_new();
EVP_MD_CTX_free(ctx); // Correct
```

### Pitfall 2: NULL Pointer Dereference

**Problem:** Not checking return values from `_new()` functions.

**Solution:** Always check for NULL:
```c
HMAC_CTX *ctx = HMAC_CTX_new();
if (!ctx) {
    // Handle allocation failure
    return ERROR_CODE;
}
// Use ctx...
HMAC_CTX_free(ctx);
```

### Pitfall 3: Using Deprecated Methods

**Problem:** Using old method functions that may be removed.

**Solution:** Use `TLS_method()` family:
```c
// AVOID
SSL_CTX *ctx = SSL_CTX_new(TLSv1_2_method());

// PREFER
SSL_CTX *ctx = SSL_CTX_new(TLS_method());
SSL_CTX_set_min_proto_version(ctx, TLS1_2_VERSION);
```

### Pitfall 4: Incomplete Error Handling

**Problem:** Not checking return values from OpenSSL functions.

**Solution:** Check all return values and handle errors:
```c
if (EVP_DigestInit_ex(ctx, EVP_sha256(), NULL) != 1) {
    ERR_print_errors_fp(stderr);
    // Handle error
}
```

## Backward Compatibility Approach

For code that needs to work with both versions:

```c
#include <openssl/opensslv.h>

#if OPENSSL_VERSION_NUMBER < 0x10100000L

// Compatibility wrappers for OpenSSL 1.0.x
static inline EVP_MD_CTX *EVP_MD_CTX_new(void) {
    EVP_MD_CTX *ctx = OPENSSL_malloc(sizeof(*ctx));
    if (ctx) {
        EVP_MD_CTX_init(ctx);
    }
    return ctx;
}

static inline void EVP_MD_CTX_free(EVP_MD_CTX *ctx) {
    if (ctx) {
        EVP_MD_CTX_cleanup(ctx);
        OPENSSL_free(ctx);
    }
}

static inline HMAC_CTX *HMAC_CTX_new(void) {
    HMAC_CTX *ctx = OPENSSL_malloc(sizeof(*ctx));
    if (ctx) {
        HMAC_CTX_init(ctx);
    }
    return ctx;
}

static inline void HMAC_CTX_free(HMAC_CTX *ctx) {
    if (ctx) {
        HMAC_CTX_cleanup(ctx);
        OPENSSL_free(ctx);
    }
}

// Add more compatibility wrappers as needed...

#endif // OPENSSL_VERSION_NUMBER < 0x10100000L
```

## Additional Resources

- OpenSSL 1.1.1 Manual: https://www.openssl.org/docs/man1.1.1/
- OpenSSL 1.1.0 Migration Guide: https://wiki.openssl.org/index.php/OpenSSL_1.1.0_Changes
- OpenSSL Security Advisories: https://www.openssl.org/news/secadv/
- TLS 1.3 RFC: https://tools.ietf.org/html/rfc8446

## Summary Checklist

- [ ] Replace all stack-allocated contexts with heap-allocated versions
- [ ] Update all `_init()` calls to `_new()` and `_cleanup()` to `_free()`
- [ ] Replace direct structure member access with accessor functions
- [ ] Update SSL method calls to use `TLS_method()`
- [ ] Remove manual initialization code (SSL_library_init, etc.)
- [ ] Add NULL checks after all `_new()` calls
- [ ] Update error handling for all OpenSSL function calls
- [ ] Update Makefile/build scripts with correct library paths
- [ ] Test with both TLS 1.2 and TLS 1.3
- [ ] Run memory leak detection tools
- [ ] Verify all deprecated API usage is eliminated
- [ ] Update documentation to reflect API changes

---

## TMOS-Specific OpenSSL 1.1.1k Migration Patterns

> Patterns discovered during TMOS module migrations that are not covered in standard OpenSSL migration guides.

### X509_get0_signature() — Accessing the Certificate Signature Field

OpenSSL 1.1.0 made the `X509` structure opaque. The `cert->signature` field is no longer directly accessible. Use `X509_get0_signature()` instead.

**Before (OpenSSL 1.0.x):**
```cpp
const ASN1_BIT_STRING* sig = cert->signature;
int sig_len = sig->length;
const unsigned char* sig_data = sig->data;
```

**After (OpenSSL 1.1.x):**
```cpp
const ASN1_BIT_STRING* sig = nullptr;
const X509_ALGOR* alg = nullptr;
X509_get0_signature(&sig, &alg, cert);
// sig and alg are borrowed references — do NOT free them
int sig_len = sig ? (int)sig->length : 0;
const unsigned char* sig_data = sig ? sig->data : nullptr;
```

**Note:** `X509_get0_signature()` returns borrowed pointers owned by the X509 object — do not free `sig` or `alg`.

**Detection:**
```bash
grep -rn "->signature\b" <module>/ --include="*.cpp" --include="*.c" --include="*.h"
```

---

### shared_ptr With Borrowed OpenSSL Pointer — No-Op Deleter Required

OpenSSL "get" and "get0" accessor functions return non-owning ("borrowed") pointers. The returned object is owned by the parent OpenSSL structure and must not be freed by the caller. Wrapping such a pointer in `std::shared_ptr` without a custom deleter causes a double-free crash.

**Problem:**
```cpp
// X509_get_subject_name returns a borrowed pointer owned by cert:
std::shared_ptr<X509_NAME> name(X509_get_subject_name(cert));
// When name goes out of scope, shared_ptr calls X509_NAME_free() — double-free!
```

**Fix — use a no-op deleter:**
```cpp
// No-op lambda deleter: shared_ptr does not free the borrowed pointer
std::shared_ptr<X509_NAME> name(
    X509_get_subject_name(cert),
    [](X509_NAME*) {}   // no-op: cert still owns this
);
```

**Affected "get0" / borrowed-reference accessors (non-exhaustive):**
- `X509_get_subject_name()` → `X509_NAME*` (borrowed)
- `X509_get_issuer_name()` → `X509_NAME*` (borrowed)
- `X509_get0_pubkey()` → `EVP_PKEY*` (borrowed)
- `X509_get0_notBefore()` / `X509_get0_notAfter()` → `ASN1_TIME*` (borrowed)
- `X509_get0_signature()` → `ASN1_BIT_STRING*` and `X509_ALGOR*` (borrowed)
- `EVP_PKEY_get0_RSA()` → `RSA*` (borrowed)
- `EVP_PKEY_get0_EC_KEY()` → `EC_KEY*` (borrowed)

**Contrast with owning accessors (caller must free):**
- `X509_get_pubkey()` → `EVP_PKEY*` (caller owns; call `EVP_PKEY_free()`)
- `X509_get_serialNumber()` → `ASN1_INTEGER*` (borrowed, not to be freed)

**Detection:**
```bash
grep -rn "shared_ptr.*X509_get\|shared_ptr.*EVP_\|shared_ptr.*ASN1_" \
    <module>/ --include="*.cpp" --include="*.h"
```

---

### BIO_get_mem_data — Return Type is long, Not int

`BIO_get_mem_data(bio, &ptr)` is a macro that calls `BIO_ctrl(...)` and returns `long`. On LP64 Linux (x86_64), `long` is 8 bytes while `int` is 4 bytes. Storing the result in `int` silently truncates for buffers larger than 2GB and produces a `-Wconversion` warning under GCC 11.

**Before (incorrect on LP64):**
```cpp
int len = BIO_get_mem_data(bio, &ptr);
```

**After (correct):**
```cpp
long len = BIO_get_mem_data(bio, &ptr);
```

**Or for size-based operations:**
```cpp
BUF_MEM* bptr = nullptr;
BIO_get_mem_ptr(bio, &bptr);
size_t len = bptr ? bptr->length : 0;
const char* ptr = bptr ? bptr->data : nullptr;
```

**Detection:**
```bash
grep -rn "int\s\+[a-z_]\+\s*=\s*BIO_get_mem_data" <module>/ --include="*.cpp" --include="*.c"
```
