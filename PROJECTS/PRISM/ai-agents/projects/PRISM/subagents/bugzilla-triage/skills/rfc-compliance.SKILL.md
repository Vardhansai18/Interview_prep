---
name: rfc-compliance
description: "Domain knowledge for RFC and standards compliance analysis of BIG-IP bugs. USE FOR tasks involving determining whether reported BIG-IP behavior is a genuine defect or RFC-compliant expected behavior. Covers OCSP, LDAP, TLS/SSL, HTTP, X.509, BGP, OSPF, DNS, RADIUS, TACACS+, and other BIG-IP protocol stack areas. Provides protocol-to-RFC mapping, analysis framework, and verdict format."
---

## RFC COMPLIANCE ANALYSIS FRAMEWORK

This skill provides a structured approach to determining whether reported BIG-IP behavior is:
- A genuine software defect
- RFC-compliant / standards-compliant expected behavior
- An implementation choice (MAY/OPTIONAL)
- Third-party behavior (not BIG-IP's fault)

---

## STEP 1 — IDENTIFY GOVERNING STANDARD(S)

Map the reported bug area to the applicable RFC(s):

| Bug Area | Applicable RFC / Standard |
|----------|--------------------------|
| OCSP (certificate status) | RFC 6960 (OCSP v1), RFC 5019 (Lightweight OCSP), RFC 6961 (TLS Multiple Cert Status) |
| OCSP stapling in TLS | RFC 6066 §8 (TLS Certificate Status Request), RFC 8446 §4.4.2.1 (TLS 1.3 stapling) |
| OCSP response caching | RFC 6960 §4.2.2.1 (nextUpdate semantics), RFC 5019 §6 (caching guidelines) |
| LDAP protocol | RFC 4511 (LDAPv3 protocol), RFC 4512 (Directory Models), RFC 4513 (Auth Methods) |
| LDAP Abandon | RFC 4511 §4.11 (Abandon Operation) |
| TLS/SSL | RFC 5246 (TLS 1.2), RFC 8446 (TLS 1.3), RFC 6125 (cert hostname verification) |
| Client certificate auth | RFC 5246 §7.4.6, RFC 8446 §4.3.2 (CertificateRequest) |
| HTTP authentication | RFC 7235 (HTTP/1.1 Auth Framework), RFC 9110 §11 |
| HTTP session/cookies | RFC 6265 (HTTP State Management / Cookies) |
| X.509 certificates | RFC 5280 (X.509 PKI Certificate and CRL Profile) |
| SNMP | RFC 3411-3418 (SNMPv3 Framework), RFC 1157 (SNMPv1) |
| BGP | RFC 4271 |
| OSPF | RFC 2328 (OSPFv2), RFC 5340 (OSPFv3) |
| DNS / DNSSEC | RFC 1035 (DNS), RFC 4034 (DNSSEC) |
| RADIUS | RFC 2865, RFC 2866, RFC 5176 |
| TACACS+ | RFC 8907 |
| iRules / TCL | Not RFC-governed; refer to TCL/iRules documentation |
| tmsh configuration | Not RFC-governed; refer to F5 product documentation |

---

## STEP 2 — APPLY RFC REQUIREMENT LEVELS

RFC language defines the strength of requirements:

| RFC Keyword | Meaning | Compliance obligation |
|-------------|---------|----------------------|
| `MUST` / `SHALL` | Unconditional requirement | Non-compliance = **defect** |
| `MUST NOT` / `SHALL NOT` | Absolute prohibition | Violation = **defect** |
| `SHOULD` / `RECOMMENDED` | Best practice; deviations need justification | Non-compliance = **likely defect** unless justified |
| `SHOULD NOT` / `NOT RECOMMENDED` | Best practice to avoid; deviations need justification | Violation = **likely defect** unless justified |
| `MAY` / `OPTIONAL` | Implementation choice | Non-implementation = **NOT a defect** |

---

## STEP 3 — KEY RFC RULES FOR COMMON BIG-IP BUG AREAS

### OCSP (RFC 6960 / RFC 5019)

**RFC 6960 §4.2.2.1 — nextUpdate semantics:**
- `thisUpdate`: time the status is known to be correct
- `nextUpdate`: time at or before which newer information will be available
- A client **SHOULD NOT** cache a response past `nextUpdate`
- If `nextUpdate` is absent, the response is considered always current

**RFC 6960 §2.4 — Caching:**
- OCSP clients MAY cache responses
- Caching beyond `nextUpdate` makes a response stale and **MUST** trigger a new request

**RFC 5019 §6 — Caching guidelines:**
- Clients caching OCSP responses **SHOULD** use `nextUpdate` as cache expiry
- If `max-age` HTTP header is present: effective expiry = `min(max-age, nextUpdate)`
- If BIG-IP ignores `nextUpdate` and uses a fixed interval → **valid defect** (SHOULD violation)

**RFC 6066 §8 / RFC 8446 §4.4.2.1 — OCSP Stapling:**
- Server MUST include a valid OCSPResponse when stapling is requested
- Stapled response MUST be within validity period per RFC 6960 §4.2.2.1
- `AH02273: OCSP response outside validity period` = Apache/OpenSSL enforcing RFC 6960 correctly
  - Root cause: BIG-IP (or server) failed to refresh stapled response before `nextUpdate` expired

### LDAP (RFC 4511)

**RFC 4511 §4.11 — Abandon Operation:**
- "The Abandon operation does not have a response defined."
- Server **MAY** abandon the identified operation
- "If the server has already completed the operation, it ignores the Abandon request"
- → Abandon sent after SearchResponse = harmless, RFC-compliant server behavior. **Not a defect.**

**RFC 4511 §4.3 — BindResponse:**
- Server MUST send a BindResponse for every BindRequest
- A missing BindResponse = **defect**

**RFC 4511 §4.5 — SearchRequest:**
- `sizeLimit`: server MAY enforce a lower limit than requested
- `timeLimit`: server MAY enforce a shorter time than requested
- Both are OPTIONAL constraints; enforcing them is server-side behavior per RFC

### TLS/SSL (RFC 5246 / RFC 8446)

**RFC 5246 §7.4.6 / RFC 8446 §4.3.2 — Client Certificate:**
- `sslVerifyClient require` operates at TLS layer only
- TLS handshake completes once client presents a valid cert → TLS requirement met
- Application-layer policy (e.g., cert-only auth, no password fallback) is separate from TLS
- If POST-handshake app falls back to password → **application-layer defect**, not TLS violation

**RFC 8446 §4.2.1 — TLS 1.3 Supported Versions:**
- Clients MUST include both `supported_versions` extension AND legacy `ClientHello.legacy_version=0x0303`
- A server rejecting TLS 1.3 ClientHello for missing legacy field = **server defect**

**RFC 6125 — Hostname Verification:**
- Clients MUST verify server certificate hostname using SANs (prefer) or CN (fallback)
- Multiple wildcard patterns: `*.example.com` matches one label only
- Cert with `CN=*.example.com` does NOT match `foo.bar.example.com` → correct rejection, not a defect

### X.509 Certificates (RFC 5280)

**RFC 5280 §4.2.1.6 — Subject Alternative Name:**
- When SAN is present, CN MUST NOT be used for hostname matching
- If BIG-IP uses CN when SAN is present → **defect**

**RFC 5280 §6.1 — Certificate Path Validation:**
- `keyUsage` extension: cert MUST NOT be used for operations not permitted by `keyUsage`
- Missing intermediate CA in chain → path validation failure is correct behavior

### HTTP (RFC 7235 / RFC 9110 / RFC 6265)

**RFC 6265 §4.1.2 — Cookie attributes:**
- `Secure` flag: browser MUST NOT send cookie over non-HTTPS
- `HttpOnly` flag: browser MUST NOT allow JavaScript to access the cookie
- Missing `Secure`/`HttpOnly` = **potential security defect**, even if not strictly an RFC MUST

**RFC 7235 §3.1 — 401 Unauthorized:**
- Response MUST include `WWW-Authenticate` header
- Missing header = **defect**

**RFC 9110 §15.5.4 — 403 Forbidden:**
- Server understands the request but refuses authorization
- Returning 403 when auth is missing (should be 401) = potential **defect** (user-visible)

### SNMP (RFC 3411-3418)

**RFC 3412 — Message Processing:**
- SNMPv3 messages MUST be authenticated if `authFlag` is set in security model
- If BIG-IP accepts unauthenticated SNMPv3 messages when `authFlag` is set → **security defect**

---

## STEP 4 — CONSIDER THIRD-PARTY BEHAVIOR

Before concluding BIG-IP is at fault, check whether the behavior originates from:

| External System | What to check |
|-----------------|---------------|
| LDAP server | RFC 4511 server obligations; is the server responding per RFC? |
| OCSP responder | RFC 6960 §4.2.2 response format; is `nextUpdate` set? Is response valid? |
| CA / PKI | RFC 5280 certificate construction; are extensions correct? |
| Apache / mod_ssl | Apache docs + RFC 6066; is BIG-IP using Apache for OCSP stapling? |
| OpenSSL library | OpenSSL changelog; known behavior differences across versions |
| Client browser | Browser-specific TLS/cookie behavior; is this a browser quirk? |
| Network device | RFC-compliant routing protocol behavior |

**If a third-party system is acting per RFC**, conclude: 🔀 **Third-party behavior — BIG-IP is not at fault.**

---

## STEP 5 — VERDICT FORMAT

Always report one of these five verdicts with a specific RFC citation:

```
✅ Valid defect
   <Protocol> RFC <number> §<section> requires <behavior>;
   BIG-IP exhibits <different behavior>.
   This is a genuine defect.

⚠️ Expected behavior (per RFC)
   <Protocol> RFC <number> §<section> permits/requires exactly this behavior.
   The reporter may be misunderstanding the standard.
   Recommend closing as WORKSFORME with explanation.

🔄 Implementation choice
   RFC <number> permits multiple behaviors (MAY / OPTIONAL);
   BIG-IP chose <X>. This is not a defect.
   Consider filing an RFE if <Y> is desired.

🔀 Third-party behavior
   The observed behavior originates from <external system>
   acting per RFC <number> §<section>.
   BIG-IP is not at fault.
   Recommend routing to the <external system> vendor.

📄 No RFC applicable
   This bug does not involve a standardized protocol.
   RFC compliance analysis is not applicable.
   Proceeding with standard triage.
```

---

## COMMON VERDICTS BY SYMPTOM

| Reported Symptom | Likely Verdict |
|-----------------|----------------|
| OCSP response rejected after `nextUpdate` | ✅ Valid defect if BIG-IP didn't refresh before expiry |
| Apache `AH02273: OCSP response outside validity period` | 🔀 Third-party — Apache is enforcing RFC 6960 correctly |
| LDAP abandon logged after successful search | ⚠️ Expected behavior — RFC 4511 §4.11 permits this |
| TLS cert-only auth falls back to password form | ✅ Valid defect (application-layer policy violation) |
| SNMP v3 accepting no-auth messages | ✅ Security defect — RFC 3412 MUST authenticate |
| Session expires and redirects to login, not cert challenge | ⚠️ Expected behavior — RFC 6265 session cookie semantics |
| Certificate rejected — wrong CN vs SAN | ⚠️ Expected behavior — RFC 6125 SAN takes precedence |
