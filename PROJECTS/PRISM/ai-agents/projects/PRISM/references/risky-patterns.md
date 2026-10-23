# Risky Coding Patterns Audit

Load this file during Phase 4 when the fix introduces any loop, blocking I/O, static variables, or cites an existing code pattern as justification.

## Pattern Table

| Pattern | Risk | Mandatory Check |
|---|---|---|
| `while(true)` or unbounded loop | **Zombie state**: 3rd-party permanently alive-but-slow → loop runs forever. Heartbeat alone prevents sod kill but blocks event loop permanently. mcpd appears alive to sod but is dead to clients. | Prove a **deadline** exists in the wait branch. `if (condition && time(NULL) >= deadline) throw` MUST be present. A loop that only exits on connection error is NOT bounded. |
| Blocking I/O on main event loop | Even with heartbeat, permanent block = no requests processed. | MUST have finite deadline, not just heartbeat. Both are required: heartbeat prevents sod kill during wait; deadline prevents zombie state. |
| Citing existing pattern as justification | Pattern acceptable in one context may be dangerous in another. | Verify **call-site context parity**: check if cited function runs in same lifecycle phase (init vs request-processing) and same thread. |
| `static` local variable in new code | Non-obvious shared state. | Confirm single-thread only, OR proper synchronization exists. |
| `usleep()` / `sleep()` in event loop | Blocks entire event loop. | Never acceptable on main thread during request processing. Use select/poll with timeout instead. |
| Raw pointer returned from function | Use-after-free if caller outlives owner. | Verify lifetime: who owns the memory? Does caller store it beyond the call? |

## Zombie State: Full Explanation

A zombie mcpd occurs when:
1. A blocking operation (loop, I/O) runs on the main event loop
2. The heartbeat is serviced (so sod doesn't kill mcpd)
3. But the event loop never returns to process new requests

Result: mcpd passes health checks but cannot serve any traffic. This is **worse** than a clean sod kill + restart because:
- No core dump is generated (no visibility into the problem)
- sod never triggers a restart
- All TMSH/iControl clients hang indefinitely
- The only recovery is manual `bigstart restart mcpd`

## Deadline Pattern (Correct Implementation)

```cpp
const time_t deadline = ::time(NULL) + TIMEOUT_SECS;
while (true) {
    service_heartbeat();          // prevents sod kill during wait
    if (!consume_input(conn)) {
        throw error;              // connection error → immediate exit
    }
    if (is_busy(conn)) {
        if (::time(NULL) >= deadline) {
            throw timeout_error;  // ← THIS is the zombie-state prevention
        }
        poll_with_1s_timeout();
        continue;
    }
    process_result();             // normal completion path
}
```

The deadline check MUST be inside the `is_busy` branch — that's the branch that executes when the 3rd party is alive but not responding with data.

## Call-Site Context Parity: How to Verify

When someone says "this matches the pattern in function X":

1. Find function X: `grep -rn "X" tm_daemon/mcp/`
2. Find X's caller: who calls X? In what phase?
3. Check lifecycle:
   - **Init phase** (called from `main()`, `PostgresClient::push_config_to_pg()`, startup sequences): unbounded loops are more acceptable — system isn't serving traffic yet
   - **Request processing** (called from `MCPProcessor::process_request()`, `replicate_tx()`, any event loop handler): MUST have deadlines

If X runs at init but the fix runs during request processing → the pattern does NOT transfer. Apply the stricter requirement.
