# Third-Party Library Upstream Check Reference

Load this file when the backtrace contains frames from a 3rd-party library (libpq, libssl, libcurl, libxml2, boost, etc.).

## P4 Access for Skill Files — Known Issue

**Important:** Skill files only exist for modules that have a `.spec` file. Not all modules have skill files.

**Lookup procedure:**
1. Try module-specific skill file: `//depot/tmos-rocky/tm_daemon/mcp/<module_name>_knowledge.SKILL.md`
2. If not found, try: `//depot/tmos-rocky/tm_daemon/mcp/mcp_knowledge.SKILL.md`
3. If neither exists, proceed with local source analysis

**Command to test access:**
```bash
export P4CONFIG=.p4config
p4 login  # If prompted, enter password

# Try module-specific first
p4 print -q "//depot/tmos-rocky/tm_daemon/mcp/<module_name>_knowledge.SKILL.md"
# Example: p4 print -q "//depot/tmos-rocky/tm_daemon/mcp/postgres_knowledge.SKILL.md"

# If "no such file", try mcp-level fallback
p4 print -q "//depot/tmos-rocky/tm_daemon/mcp/mcp_knowledge.SKILL.md"
```

**Error handling:**
- "no such file" (both attempts) → neither skill file exists, proceed with local analysis
- "protected namespace - access denied" → skill file exists but you lack permission, ask user for manual provision or proceed with local analysis

## Identify Library and Version

```bash
# Find bundled version
strings /usr/lib/lib<name>.so.* 2>/dev/null | grep -i "<library>" | head -5
rpm -qa | grep -i <library>
```

## Upstream Changelog Locations

| Library | Check location |
|---|---|
| libpq (PostgreSQL) | https://www.postgresql.org/docs/release/ |
| libssl / openssl | https://www.openssl.org/news/changelog.html |
| libcurl | https://curl.se/changes.html |
| libxml2 | https://gitlab.gnome.org/GNOME/libxml2/-/blob/master/NEWS |
| boost | https://www.boost.org/users/history/ |

Search for: the crashing function name, the symptom description, and the CVE if applicable.

## Configuration Mitigations

Check BEFORE writing workaround code. Many libraries expose parameters that address the symptom without code changes:

| Symptom | Library | Config mitigation |
|---|---|---|
| Blocking `poll(timeout=-1)` on dead socket | libpq | `keepalives=1 keepalives_idle=10 keepalives_interval=2 keepalives_count=5` in DSN |
| TLS handshake hangs | libssl | `SSL_CTX_set_timeout()`, non-blocking mode |
| DNS resolution hangs | libcurl | `CURLOPT_CONNECTTIMEOUT`, `CURLOPT_TIMEOUT` |
| XML parsing OOM | libxml2 | `XML_PARSE_HUGE` flag removal, size limits via `xmlCtxtSetMaxAmplification()` |

A configuration mitigation is **complementary** to a code fix — apply both when available:
- Config fix → handles dead-connection / crash scenarios (OS-level detection)
- Code fix → handles alive-but-slow scenarios (application-level timeout)

## Decision Matrix

| Upstream fix exists | Applicable | Action |
|---|---|---|
| Via config param | Yes (param available in bundled version) | Apply config param + add code fix as defense-in-depth |
| Via library upgrade | Small isolated patch | Backport upstream fix instead of workaround |
| Via library upgrade | Large delta / risky | Write BIG-IP workaround; note upstream fix in bug comments |
| No upstream fix | — | Write BIG-IP workaround using upstream-recommended pattern |

## libpq-Specific Patterns (Most Common)

libpq's synchronous API (`PQexec`) uses `poll(timeout=-1)` **by design**. This is not a bug upstream. The upstream-recommended solution for timeout control is the async model:

```
PQsendQuery() → PQconsumeInput() + PQisBusy() + manual select/poll with timeout
```

PostgreSQL has never introduced `PQexecWithTimeout()` — the async model IS the intended solution.

TCP keepalives (available since libpq 8.0) handle the **dead socket** case:
```
keepalives=1 keepalives_idle=10 keepalives_interval=2 keepalives_count=5
```
- idle=10: first probe after 10s silence
- interval=2: probe every 2s
- count=5: declare dead after 5 missed probes (~20s total detection)
