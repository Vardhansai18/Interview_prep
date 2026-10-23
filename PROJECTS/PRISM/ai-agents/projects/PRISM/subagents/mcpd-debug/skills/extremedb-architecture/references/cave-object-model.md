# CAVE Object Model Reference

CAVE class hierarchy, object handles, OIDs, cursors, type system, and source file map.

## Class Hierarchy

```
Cave::CompositeObj           — Attribute get/set interface
  └─ Cave::CfgObj            — Configuration object (create, save, remove)
      └─ Cave::EdbCfgObj     — eXtremeDB implementation

Cave::DbConnection           — Transaction management interface
  └─ Cave::EdbDbConnection   — eXtremeDB implementation

Cave::QueryEngine            — Query interface
  └─ Cave::EdbQueryEngine    — eXtremeDB SQL implementation

Cave::CfgSchema              — Schema management
Cave::CfgClass               — Class metadata (fields, indexes, keys)
Cave::CfgAttribute           — Attribute metadata
Cave::TransactionLog         — Per-transaction change tracking
```

## Initialization

```cpp
Cave::initialize(DbConnection*)
    ├─ SchemaRepository::initialize()
    ├─ CfgSchema::initialize(dbc)
    ├─ QueryEngine::initialize(dbc)
    └─ CfgObj::initialize(dbc)
```

## CfgObj Operations

```cpp
CfgObj* obj = CfgObj::create(cid_some_class);   // Create
obj->set(cid_some_field, value);                  // Set attribute
obj->save();                                       // Update indexes (make visible)
obj->get(cid_some_field, &value);                 // Read attribute
obj->remove();                                     // Delete
```

**Note**: `save()` is actually `update_indexes()` — ensures object visible via indexes. The `save()` name is a deprecated wrapper.

## Object Handles

```c
typedef MCO_PUB_STRUCT_BASE MCO_Hf[mco_handle_size_w];
// mco_handle_size = 16 * sizeof(mco_offs_t)
```

A handle is a **pointer into shared memory** to the object's current physical location.

**Critical under MVCC**: When modified, eXtremeDB creates a **work copy** at a different location → **handle changes** even though it's the same object.

## OIDs (Object IDs)

```cpp
oid_t object_id() const;                 // Returns runtime OID
static oid_t get_and_incr_object_id();   // Assigns next OID
```

OIDs are **monotonically increasing** integers, the **stable** identifier across an object's lifetime.

## The Three Identifiers

```
┌──────────────────┬──────────────────────────────────────┐
│ Runtime handle   │ Physical location in shared memory.   │
│                  │ Changes when MVCC creates work copy.  │
├──────────────────┼──────────────────────────────────────┤
│ obj->object_id() │ CAVE runtime method. Stable, correct.│
│                  │ NOT from DB field.                    │
├──────────────────┼──────────────────────────────────────┤
│ obj->get(        │ Reads OID from eXtremeDB schema      │
│  cid_*_object_id │ FIELD. Under MVCC, may reference     │
│  , &oid)         │ stale version. ⚠️ CAN DIVERGE!      │
└──────────────────┴──────────────────────────────────────┘
```

**Rule**: Always `obj->object_id()`. Never `obj->get(cid_xxx_object_id, &oid)` for TransactionLog lookups.

## Cursors

```c
typedef struct mco_cursor_t_ {
    MCO_PUB_STRUCT_BASE c[mco_cursor_size_w];
} mco_cursor_t;
```

Cursors iterate index results. **Transaction-bound** — only valid in the creating transaction.

## Type System (cfg_type_t)

| Type | Description |
|------|-------------|
| `CFG_TYPE_INT8` – `CFG_TYPE_UINT64` | Integer types |
| `CFG_TYPE_DOUBLE` | Double precision float |
| `CFG_TYPE_STRING` | NULL-terminated, max 65520 bytes |
| `CFG_TYPE_BLOB` | Binary large object |
| `CFG_TYPE_VECTOR` | Ordered collection |
| `CFG_TYPE_REF` | Foreign key reference |
| `CFG_TYPE_STRUCT` | Embedded structure |
| `CFG_TYPE_IP_ADDRESS` | IP address |
| `CFG_TYPE_MAC_ADDRESS` | MAC address |
| `CFG_TYPE_DATE_TIME` | Wrapped `time_t` |

## Memory Architecture

### Shared Memory

```
/dev/shm/
├── mcp_db           # Main database segment
├── mcp_db_ext_1     # Extension segment (if grown)
├── mcp_db_ext_2     # Additional extension
└── ...
```

- Created via `mco_db_open_dev()` with `MCO_MEMORY_NAMED`
- Extended at runtime via `mco_db_extend_dev()`
- CAVE's `DbConnection::check_db_size()` auto-extends below watermark

### Page-Based Storage

```
┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐
│Page 0││Page 1││Page 2││Page 3││Page 4│
│(meta)││(data)││(data)││(idx) ││(free)│
└──────┘└──────┘└──────┘└──────┘└──────┘
```

### Key Parameters (mco_db_params_t)

| Parameter | Impact on Debugging |
|-----------|-------------------|
| `mem_page_size` | Allocation granularity |
| `db_max_connections` | MCO_E_SESLIMIT if exceeded |
| `min/max_conn_local_pages` | Per-thread memory; can cause MCO_E_NOMEM |
| `mvcc_objmap_max_child` | Version tracking capacity |
| `max_gc_versions` | Old versions reclaimed per GC |
| `trans_sched_policy` | FIFO, reader-favor, or writer-favor |

## Source File Map

```
Cave::CfgObj / EdbCfgObj         → f5lib/cave/lib/CfgObj.cpp, EdbCfgObj.cpp
Cave::DbConnection               → f5lib/cave/lib/DbConnection.h
Cave::EdbDbConnection             → f5lib/cave/lib/EdbDbConnection.cpp
Cave::TransactionLog              → f5lib/cave/lib/TransactionLog.cpp
Cave::QueryEngine                 → f5lib/cave/lib/QueryEngine.cpp
Cave::CfgSchema                   → f5lib/cave/lib/CfgSchema.cpp
Cave::SchemaRepository            → f5lib/cave/schema_parser/
eXtremeDB headers                 → ports/extremedb/v8.4/include/
mco_* implementation              → eXtremeDB library (external, no source)
```
