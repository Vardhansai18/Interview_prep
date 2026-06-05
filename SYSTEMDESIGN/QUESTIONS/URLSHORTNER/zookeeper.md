# ZooKeeper: Persistent Nodes vs Ephemeral Nodes

Zoom is a great real-world analogy for understanding the difference between **Persistent Nodes** and **Ephemeral Nodes** in ZooKeeper.

---

## What is ZooKeeper?

ZooKeeper is a distributed coordination service. It stores data in a hierarchical tree structure (similar to a file system), where each node in the tree is called a **znode**.

There are two types of znodes:

| Node Type | Description |
|-----------|-------------|
| **Persistent Node** | Remains in ZooKeeper even after the client that created it disconnects |
| **Ephemeral Node** | Automatically deleted when the client session that created it ends |

---

## Zoom Meeting Example

Imagine Zoom uses ZooKeeper internally to manage meetings and participants.

### Creating a Meeting

Suppose you create a meeting:

- **Meeting ID:** 12345
- **Topic:** System Design Discussion
- **Time:** 10:00 AM

ZooKeeper stores it as:

```text
/
└── meetings
     └── 12345
          ├── topic = System Design Discussion
          └── host = Vardhan
```

This is a **Persistent Node** — the meeting details exist even if nobody is currently connected.

---

### Before Anyone Joins (9:50 AM)

No participants yet. The meeting node still exists:

```text
/meetings/12345
  topic = System Design Discussion
  host = Vardhan
```

The meeting configuration persists regardless of active connections.

---

### Participants Join

Vardhan, Rahul, and Priya join the meeting.

ZooKeeper creates **Ephemeral Nodes** for each active participant:

```text
/
└── meetings
     └── 12345
          └── participants
                ├── vardhan   (ephemeral)
                ├── rahul     (ephemeral)
                └── priya     (ephemeral)
```

These are ephemeral because they represent **live, active connections**.

---

### Rahul Leaves the Meeting

Rahul clicks "Leave". His session ends, and ZooKeeper **automatically removes** his node:

```text
/meetings/12345/participants/rahul  ← removed
```

The remaining participants:

```text
participants
├── vardhan
└── priya
```

- ✅ The meeting itself still exists (persistent)
- ❌ Rahul's participant entry is gone (ephemeral removed)

---

### Everyone Leaves

All participants disconnect. ZooKeeper automatically removes all ephemeral participant nodes:

```text
/participants/vardhan  ← removed
/participants/priya    ← removed
```

ZooKeeper now looks like:

```text
/
└── meetings
     └── 12345
          ├── topic = System Design Discussion
          └── host = Vardhan
```

The meeting configuration remains — because it's a **Persistent Node**.

---

## Real-Life Mapping: Conference Room

Think of a Zoom meeting as a physical conference room booking.

### Persistent Node → Room Booking

```
Room A
Booked for 10 AM
Topic: System Design
```

Even if the room is currently empty, the booking record still exists.

### Ephemeral Node → People in the Room

```
Vardhan  (present)
Rahul    (present)
Priya    (present)
```

- When Rahul walks out → Rahul's entry disappears
- When everyone leaves → The room is empty, but the booking remains

---

## Why ZooKeeper Uses This: Service Discovery

The same pattern is used for tracking live servers in a distributed system.

```text
/services
    /server1   (ephemeral)
    /server2   (ephemeral)
    /server3   (ephemeral)
```

Each server registers itself as an **Ephemeral Node** when it starts.

When a server crashes or goes offline:

```text
server2 disconnected → /servers/server2 removed automatically
```

Other services can watch `/services` and react instantly when a node disappears — exactly like Zoom detecting that a participant left.

---

## Summary

| Zoom Concept | ZooKeeper Node Type |
|---|---|
| Meeting details (ID, topic, host) | Persistent Node |
| Active participants in the meeting | Ephemeral Node |
| Participant disconnects | Ephemeral node removed automatically |
| Meeting configuration remains | Persistent node remains |

**Key Insight:**
- **Persistent nodes** describe the meeting itself — what exists regardless of who is connected.
- **Ephemeral nodes** describe who is currently connected — they live and die with the session.