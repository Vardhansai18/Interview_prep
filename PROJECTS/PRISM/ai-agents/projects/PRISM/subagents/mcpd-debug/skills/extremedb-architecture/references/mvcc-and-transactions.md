# MVCC and Transactions Reference

Deep dive into eXtremeDB MVCC, transaction API, TransactionLog, and the OID mismatch bug pattern.

## MURSIW vs MVCC

### MURSIW (pre-8.4)
```
Readers → shared read lock (concurrent reads OK)
Writer  → exclusive lock (blocks ALL readers + writers)
- Objects updated IN-PLACE — no versioning
- Schema field values ≡ runtime handles (always identical)
- Simpler, no GC needed
```

### MVCC (v8.4, current)
```
Readers → snapshot isolation (point-in-time view)
Writer  → creates new versions (old retained for active readers)
- Objects NOT updated in-place — new version created
- Old versions retained until referencing transactions complete
- Requires garbage collection
- Schema field values CAN diverge from runtime handles ⚠️
```

**Why F5 migrated**: Worker threads (20.x+) need concurrent reads while main thread writes. MURSIW blocks all readers during writes — defeats the purpose.

## How MVCC Versioning Works

```
T1: Writer starts transaction
    ┌───────────────┐
    │ Object V1     │  ← Original version
    │ OID=100       │
    │ handle=0xAAA  │
    └───────────────┘

T2: Writer modifies → eXtremeDB creates WORK COPY
    ┌───────────────┐     ┌───────────────┐
    │ Object V1     │     │ Work Copy     │
    │ handle=0xAAA  │     │ handle=0xBBB  │  ← NEW handle!
    └───────────────┘     └───────────────┘

T3: Reader starts → gets snapshot of V1 (handle=0xAAA)
    Writer still sees handle=0xBBB

T4: Writer commits → Work Copy becomes V2
    V1 → old (awaiting GC)
    V2 → committed (handle=0xBBB)

T5: Reader finishes → V1 eligible for garbage collection
```

## Isolation Levels

| Level | Enum | Behavior |
|-------|------|----------|
| Read Committed | `MCO_READ_COMMITTED` | Sees committed data at time of each read |
| Repeatable Read | `MCO_REPEATABLE_READ` | Snapshot at tx start. **Default for MVCC.** |
| Serializable | `MCO_SERIALIZABLE` | Serial execution emulation. Can cause MCO_E_CONFLICT |

MCPD uses:
- Read-only: `begin_read_only_tx()` → `MCO_READ_ONLY`, Repeatable Read
- Read-committed: `begin_read_committed_tx()` → `MCO_READ_WRITE`

## MVCC Conflicts

```
Writer A: modifies Object X → creates work copy
Writer B: modifies Object X → MCO_E_CONFLICT (87)
```

In MCPD, writes are serialized on main thread → conflicts should be rare. Can occur if worker thread writes (bug) or during HA sync.

## MVCC Internal Locking

Even under MVCC, fine-grained internal locks exist:

```
MCO_WAIT_EVENT_MVCC_CS_LOCK          — Critical section
MCO_WAIT_EVENT_MVCC_TM_LOCK          — Transaction manager
MCO_WAIT_EVENT_MVCC_PM_MUTEX         — Page manager
MCO_WAIT_EVENT_MVCC_EXCLUSIVE_LOCK   — Exclusive tx
MCO_WAIT_EVENT_MVCC_TREE_*_LOCK      — B-Tree locks
MCO_WAIT_EVENT_MVCC_HASH_*_LOCK      — Hash index locks
MCO_WAIT_EVENT_MVCC_DB_MUTEX         — Database mutex
MCO_WAIT_EVENT_MVCC_PAGE_LATCH       — Page latch
```

If threads blocked on these → possible deadlock/contention within eXtremeDB.

## MVCC Mode Flags

| Flag | Value | Purpose |
|------|-------|---------|
| `MCO_DB_MODE_MVCC_AUTO_VACUUM` | 0x01 | Auto-reclaim old version pages |
| `MCO_DB_MVCC_COMPATIBILITY_MODE` | 0x40000 | Compatibility with pre-MVCC code |
| `MCO_DB_MVCC_TABLE_LEVEL_LOCKING` | 0x8000000 | Table-level locks (default: fine-grain) |

## Auto-Vacuum and Garbage Collection

MVCC accumulates old versions. Cleanup policies:

| Policy | Behavior |
|--------|----------|
| `MCO_GC_DISABLED` | No automatic GC |
| `MCO_GC_SELF_VERSIONS` | Each connection cleans own old versions |
| `MCO_GC_ON_MODIFICATION` | GC triggered on modifications |
| `MCO_GC_ALWAYS` | GC runs every transaction |

**GC too aggressive** → reclaims versions active readers still reference.
**GC too lazy** → shared memory fills → MCO_E_NOMEM.

---

## Transaction API

### Native eXtremeDB (C)

```c
mco_trans_start(db, MCO_READ_WRITE, MCO_TRANS_FOREGROUND, &t);
mco_trans_commit(t);       // May fail with MCO_E_CONFLICT
mco_trans_rollback(t);     // Always succeeds
mco_trans_upgrade(t);      // Read→write (may fail MCO_E_UPGRADE_FAILED)

// Transaction types
MCO_READ_ONLY  = 0
MCO_UPDATE     = 1
MCO_READ_WRITE = 2
MCO_EXCLUSIVE  = 3
```

### CAVE (C++)

```cpp
DbConnection::begin_read_only_tx();
DbConnection::begin_read_committed_tx(bool exclusive = false);
DbConnection::commit();
DbConnection::rollback();
DbConnection::active_transaction();
```

### Transaction Lifecycle in MCPD

```
Main Thread (write):
  begin_read_committed_tx()
    └─ mco_trans_start(db, MCO_READ_WRITE, ...)
  ... CfgObj::create() / save() / remove() ...
  ... TransactionLog tracks all changes ...
  commit()
    └─ mco_trans_commit(t)
    └─ TransactionLog::close_tx_log()

Worker Thread (read):
  begin_read_only_tx()
    └─ mco_trans_start(db, MCO_READ_ONLY, ...)
  ... query ...
  commit() or rollback()
```

### Thread-Local DbConnection

```cpp
static __thread DbConnection* c_db_connection;  // From DbConnection.h
static __thread TransactionLog *c_tx_log;         // From TransactionLog.h
```

Each thread has its own connection + transaction. Required by eXtremeDB.

---

## TransactionLog

Tracks all modifications within a single database transaction. Bridge between DB operations and post-transaction actions.

### Structure

```cpp
class TransactionLog {
    map<oid_t, ModifiedObj*> m_modified_objects;  // Created or modified
    map<oid_t, SchemaObj*>   m_deleted_objects;   // Deleted
    vector<oid_t>            m_phantom_objects;    // Created-then-deleted
};
```

Key: `m_modified_objects` is keyed by **runtime** `object_id()`, NOT schema field.

### API

```cpp
// Record
void object_created(oid_t, CfgObj*);
void object_modified(oid_t, CfgObj*);
void object_deleted(CfgObj*);

// Query
bool get_log_entry(oid_t, const ModifiedObj*&);   // Lookup by OID
bool object_is_new(CfgObj*);
bool object_was_deleted(oid_t);

// Change detection
bool value_has_changed(const CfgObj*, const CFG_ID&, T&);

// Lifecycle
static void open_tx_log();    // Start
static void close_tx_log();   // Clear
```

### Usage in Pipeline

```
1. Checkpoint: CfgObj::create/set → TransactionLog::object_created/modified
2. Commit: Validators call get_log_entry() to check changes
3. Post-tx: PostTransMgr reads log for kernel ops; PubSub reads for notifications
4. After commit: close_tx_log() clears everything
```

---

## The MVCC OID Mismatch Bug Pattern

### The Problem

Schema field OID can diverge from runtime `object_id()` under MVCC. Using the wrong one for TransactionLog lookup → silent failure.

### Mechanism

```
Step 1: Checkpoint phase
  obj created → TransactionLog records {key: obj->object_id()=100}
  obj->save() → eXtremeDB creates work copy

Step 2: Validation
  Code re-queries from DB → may get different handle
  obj->get(cid_xxx_object_id, &oid) → reads schema field → STALE OID
  TransactionLog::get_log_entry(stale_oid) → FAILS (NULL)
  Post-transaction kernel op SILENTLY SKIPPED

Step 3: Commit
  DB thinks object exists. Kernel never created device/route.
  SILENT FAILURE → later crash when code assumes kernel matches DB.
```

### Fix Pattern

```cpp
// ❌ WRONG:
oid_t oid;
obj->get(cid_tunnel_object_id, &oid);
TransactionLog::get()->get_log_entry(oid, entry);

// ✅ CORRECT:
TransactionLog::get()->get_log_entry(obj->object_id(), entry);
```

### Known Affected Files

| File | Object Type | Status |
|------|-------------|--------|
| `net/validation/Tunnel.cpp` | Tunnel | Known bug, ~line 2368 |
| `net/validation/Vlan.cpp` | VLAN | Known bug |
| `net/validation/Vlangroup.cpp` | VLAN Group | Known bug |
| `sys/validation/DbVariableFile.cpp` | DB Variable | Fixed (lines 789-793) |
| **Any validator using `cid_*_object_id` + `get_log_entry()`** | Any | Potential |

### Search Commands

```bash
grep -rn "get_log_entry" tm_daemon/mcp/ | grep -v "object_id()"
grep -rn "cid_.*object_id.*&oid" tm_daemon/mcp/
grep -rn "get(cid_.*object_id" tm_daemon/mcp/
```

### Why Intermittent

Most of the time eXtremeDB keeps work copies at same location → handles match → works. Occasionally memory pressure/GC/concurrent tx causes relocation → divergence. ~1 in 100, timing-dependent, load-dependent.
