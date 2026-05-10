# Mutex in C++ Threading

## Overview

**Mutex** = **Mut**ual **Ex**clusion  

A mutex is a synchronization primitive used to protect shared data from being simultaneously accessed by multiple threads, preventing **race conditions**.

---

## 🚨 Race Condition

### What is a Race Condition?

A **race condition** occurs when:
- Two or more threads/processes access shared data **simultaneously**
- At least one thread **modifies** the data
- The final result depends on the **timing/order** of thread execution
- Results become **unpredictable** and **incorrect**

### Critical Section

The **protected section** of code that accesses shared resources is called the **critical section** or **critical region**.

---

## ❌ Problem: Race Condition Example

### Code Without Mutex:

```cpp
#include <iostream>
#include <thread>
using namespace std;

int myAmount = 0;

void addMoney() {
    for(int i = 0; i < 1000000; i++) {
        ++myAmount;  // ⚠️ Unsafe! Multiple threads accessing shared data
    }
}

int main() {
    thread t1(addMoney);
    thread t2(addMoney);

    t1.join();
    t2.join();

    cout << "Final Amount: " << myAmount << endl;
    cout << "Expected: 2000000" << endl;
    
    return 0;
}
```

### Output:
```
Final Amount: 1534689
Expected: 2000000
```

### The Problem:

**Why is the result incorrect?**

```
Thread 1: Read myAmount (0)
Thread 2: Read myAmount (0)
Thread 1: Increment (0 + 1 = 1)
Thread 2: Increment (0 + 1 = 1)
Thread 1: Write back (1)
Thread 2: Write back (1)

❌ Result: myAmount = 1 (Should be 2!)
```

- Both threads read the same value simultaneously
- Both increment independently
- Both write back, **losing one increment**
- Data corruption occurs!

---

## ✅ Solution: Using Mutex

### What is a Mutex?

A mutex ensures:
- 🔒 Only **one thread** can access the critical section at a time
- 🚦 Other threads **wait** until the mutex is unlocked
- ✅ **Thread-safe** access to shared data

### How Mutex Works:

1. Thread calls `lock()` - acquires the mutex
2. If already locked, thread waits
3. Thread executes critical section
4. Thread calls `unlock()` - releases the mutex
5. Waiting threads can now acquire the lock

---

## 📝 Basic Mutex Example

```cpp
#include <iostream>
#include <thread>
#include <mutex>
using namespace std;

int myAmount = 0;
mutex m;  // Declare mutex

void addMoney() {
    m.lock();      // 🔒 Acquire lock
    ++myAmount;    // ✅ Critical section (safe)
    m.unlock();    // 🔓 Release lock
}

int main() {
    thread t1(addMoney);
    thread t2(addMoney);

    t1.join();
    t2.join();

    cout << myAmount << endl;  // Output: 2 ✅
    return 0;
}
```

### Output:
```
2
```

**Analysis:**
- ✅ Both threads safely increment `myAmount`
- ✅ No data corruption
- ✅ Predictable result

---

## 🔄 Complete Example with Multiple Increments

```cpp
#include <iostream>
#include <thread>
#include <mutex>
using namespace std;

int myAmount = 0;
mutex m;

void addMoney() {
    for(int i = 0; i < 1000000; i++) {
        m.lock();
        ++myAmount;
        m.unlock();
    }
}

int main() {
    thread t1(addMoney);
    thread t2(addMoney);

    t1.join();
    t2.join();

    cout << "Final Amount: " << myAmount << endl;
    cout << "Expected: 2000000" << endl;
    
    return 0;
}
```

### Output:
```
Final Amount: 2000000
Expected: 2000000
```

**Perfect!** ✅ The result is now correct and consistent.

---

## 🛡️ lock_guard - RAII Approach (Recommended)

### Problem with Manual lock()/unlock():

```cpp
m.lock();
// If exception occurs here, unlock() never called!
++myAmount;
m.unlock();  // May never execute ❌
```

### Solution: Use lock_guard

```cpp
#include <iostream>
#include <thread>
#include <mutex>
using namespace std;

int myAmount = 0;
mutex m;

void addMoney() {
    lock_guard<mutex> lock(m);  // 🔒 Auto lock
    ++myAmount;
    // 🔓 Auto unlock when lock goes out of scope
}

int main() {
    thread t1(addMoney);
    thread t2(addMoney);

    t1.join();
    t2.join();

    cout << myAmount << endl;
    return 0;
}
```

### Benefits of lock_guard:
- ✅ **Automatic** lock on construction
- ✅ **Automatic** unlock on destruction
- ✅ **Exception-safe** (RAII principle)
- ✅ **Cannot forget** to unlock
- ✅ **Cleaner code**

---

## 🆚 Comparison: With vs Without Mutex

| Aspect | Without Mutex | With Mutex |
|--------|---------------|------------|
| **Thread Safety** | ❌ Unsafe | ✅ Safe |
| **Race Condition** | ❌ Possible | ✅ Prevented |
| **Result** | ❌ Unpredictable | ✅ Consistent |
| **Data Integrity** | ❌ Corrupted | ✅ Protected |
| **Performance** | ⚡ Fast (but wrong) | 🐢 Slower (but correct) |

---

## 🎯 When to Use Mutex?

### ✅ Use Mutex When:

- Multiple threads **read and write** shared data
- Need to protect **critical sections**
- Need **data consistency** and integrity
- Accessing shared resources like files, network, etc.

### ❌ Don't Need Mutex When:

- Threads only **read** data (no writes)
- Each thread works on **independent data**
- Using **atomic operations** (`std::atomic`)
- Already using higher-level synchronization (e.g., channels, queues)

---

## 📚 Key Concepts

### Critical Section:
```cpp
m.lock();
// ⚠️ CRITICAL SECTION
// Only one thread at a time
// Keep this section as SMALL as possible
++sharedVariable;
m.unlock();
```

### Mutex Operations:

| Operation | Description |
|-----------|-------------|
| `m.lock()` | Acquire lock (blocks if already locked) |
| `m.unlock()` | Release lock |
| `m.try_lock()` | Try to acquire lock (returns immediately) |

### RAII Wrappers:

| Type | Description |
|------|-------------|
| `lock_guard` | Basic RAII lock (lock on construction, unlock on destruction) |
| `unique_lock` | More flexible, can unlock manually |
| `scoped_lock` | Can lock multiple mutexes (C++17) |

---

## ⚠️ Common Mistakes

### ❌ Forgetting to Unlock:
```cpp
m.lock();
if(condition) {
    return;  // ❌ Forgot to unlock! Deadlock!
}
m.unlock();
```

### ✅ Solution: Use lock_guard
```cpp
lock_guard<mutex> lock(m);
if(condition) {
    return;  // ✅ Automatically unlocks
}
```

### ❌ Deadlock:
```cpp
mutex m1, m2;

// Thread 1
m1.lock();
m2.lock();  // Waits for m2

// Thread 2
m2.lock();
m1.lock();  // Waits for m1
// ❌ DEADLOCK!
```

### ✅ Solution: Lock in Same Order
```cpp
// Both threads lock in same order
m1.lock();
m2.lock();
// ✅ No deadlock
```

---

## 💡 Best Practices

1. ✅ **Use `lock_guard`** instead of manual `lock()`/`unlock()`
2. ✅ **Keep critical sections small** - minimize locked time
3. ✅ **Lock in the same order** to avoid deadlocks
4. ✅ **Don't call external functions** while holding a lock
5. ✅ **Use `std::atomic`** for simple counters when possible
6. ✅ **Test with multiple threads** to catch race conditions
7. ✅ **Prefer higher-level abstractions** when available

---

## 🔍 Visual Representation

### Without Mutex:
```
Thread 1: [Read][Modify][Write]
                [Read][Modify][Write] Thread 2
❌ Overlap = Race Condition!
```

### With Mutex:
```
Thread 1: 🔒[Read][Modify][Write]🔓
                                  🔒[Read][Modify][Write]🔓 Thread 2
✅ Sequential = Safe!
```

---

## 🎓 Key Takeaways

1. 🚨 **Race conditions** occur when multiple threads access shared data
2. 🔒 **Mutex** provides mutual exclusion (only one thread at a time)
3. ✅ **Always protect critical sections** with mutex
4. 🛡️ **Use `lock_guard`** for exception-safe locking
5. ⚡ **Keep critical sections small** for better performance
6. 🔄 **Lock in same order** to prevent deadlocks
7. 📊 **Test thoroughly** with multiple threads

---

## Compilation

```bash
g++ -std=c++11 -pthread filename.cpp -o output
./output
```

---

## Summary Table

| Concept | Description |
|---------|-------------|
| **Race Condition** | Multiple threads modify shared data simultaneously |
| **Critical Section** | Code section that accesses shared resources |
| **Mutex** | Lock mechanism for mutual exclusion |
| **lock()** | Acquire mutex (blocks if locked) |
| **unlock()** | Release mutex |
| **lock_guard** | RAII wrapper for automatic lock/unlock |
| **Deadlock** | Circular wait for locks |






