# Thread Management: join(), detach() and joinable() (C++11)

## Overview

Every thread object must be either **joined** or **detached** before it is destroyed. Failure to do so will cause the program to terminate in the thread's destructor.

### Critical Rules

⚠️ **Must call either `join()` or `detach()` on every thread**  
⚠️ **Cannot call `join()` or `detach()` twice**  
⚠️ **Check `joinable()` before calling `join()` or `detach()`**

---

## 📌 join() - Wait for Thread Completion

### Key Points

✅ Once a thread is started, we wait for it to finish by calling `join()`  
✅ Blocks the calling thread until the target thread completes  
✅ Double join will result in program termination  
✅ Use `joinable()` to check if a thread can be joined

---

## 📌 detach() - Separate Thread from Parent

### Key Points

✅ Detaches the newly created thread from the parent thread  
✅ Detached threads run independently in the background  
✅ Always check `joinable()` before detaching to avoid double detach  
✅ If main() returns while a detached thread is running, the detached thread may be terminated

---


## Example 1: Basic join() Usage ✅

**Code:**
```cpp
#include <iostream>
#include <thread>
#include <chrono>

using namespace std;

void run(int count)
{
    while(count--)
    {
        cout << "count: " << count << endl;
    }
    this_thread::sleep_for(chrono::seconds(4)); 
}

int main() {
    cout << "main()" << endl;
    int count = 10;
    
    thread t1(run, count);
    t1.join();  // Wait for thread to finish
    
    cout << "main() after" << endl;
    return 0;
}
```

**Output:**
```
main()
count: 9
count: 8
count: 7
count: 6
count: 5
count: 4
count: 3
count: 2
count: 1
count: 0
main() after
```

**Analysis:**
- The main thread waits for `t1` to complete
- "main() after" is printed only after the thread finishes
- Thread sleeps for 4 seconds before completion




---

## Example 2: Double join() - ❌ ERROR

**Code:**
```cpp
#include <iostream>
#include <thread>
#include <chrono>

using namespace std;

void run(int count)
{
    while(count--)
    {
        cout << "count: " << count << endl;
    }
    this_thread::sleep_for(chrono::seconds(4)); 
}

int main() {
    cout << "main()" << endl;
    int count = 10;
    
    thread t1(run, count);
    t1.join();  // First join - OK
    t1.join();  // Second join - CRASH!
    
    cout << "main() after" << endl;
    return 0;
}
```

**Output:**
```
main()
count: 9
count: 8
count: 7
count: 6
count: 5
count: 4
count: 3
count: 2
count: 1
count: 0
terminate called after throwing an instance of 'std::system_error'
  what():  Invalid argument
Aborted (core dumped)
```

**Problem:**
- ❌ Calling `join()` twice on the same thread causes program termination
- After the first `join()`, the thread is no longer joinable
- Second `join()` throws `std::system_error`


---

## Example 3: Using joinable() - ✅ SAFE

**Code:**
```cpp
#include <iostream>
#include <thread>
#include <chrono>

using namespace std;

void run(int count)
{
    while(count--)
    {
        cout << "count: " << count << endl;
    }
    this_thread::sleep_for(chrono::seconds(4)); 
}

int main() {
    cout << "main()" << endl;
    int count = 10;
    
    thread t1(run, count);

    // Check before first join
    if(t1.joinable())
    {
        t1.join();
    }

    // Check before second join - will be false
    if(t1.joinable())
    {
        t1.join();  // This won't execute
    }
    
    cout << "main() after" << endl;
    return 0;
}
```

**Output:**
```
main()
count: 9
count: 8
count: 7
count: 6
count: 5
count: 4
count: 3
count: 2
count: 1
count: 0
main() after
```

**Analysis:**
- ✅ `joinable()` returns `true` before first `join()`
- ✅ `joinable()` returns `false` after first `join()`
- ✅ Second `join()` is skipped, preventing crash
- **Best Practice:** Always check `joinable()` before calling `join()`

---

## Example 4: Using detach() - ⚠️ Unpredictable Behavior

**Code:**
```cpp
#include <iostream>
#include <thread>
#include <chrono>

using namespace std;

void run(int count)
{
    while(count--)
    {
        cout << "count: " << count << endl;
    }
    this_thread::sleep_for(chrono::seconds(4)); 
}

int main() {
    cout << "main()" << endl;
    int count = 10;
    
    thread t1(run, count);
    t1.detach();  // Detach immediately
    
    cout << "main() after" << endl;
    return 0;  // main() exits before thread finishes
}
```

**Output:**
```
main()
main() after
```

**Analysis:**
- ⚠️ Thread is detached and runs independently
- ⚠️ main() completes immediately without waiting
- ⚠️ Detached thread may not execute fully (gets terminated when main() exits)
- ⚠️ No output from the thread because main() exits too quickly
- **Problem:** Detached threads lose execution context when parent exits 


---

## Example 5: Best Practice - ✅ Safe Thread Management

**Code:**
```cpp
#include <iostream>
#include <thread>
#include <chrono>

using namespace std;

void run(int count)
{
    while(count--)
    {
        cout << "count: " << count << endl;
    }
    this_thread::sleep_for(chrono::seconds(4)); 
}

int main() {
    cout << "main()" << endl;
    int count = 10;
    
    thread t1(run, count);

    // Always check before join
    if(t1.joinable())
    {
        t1.join();
    }

    // This won't execute (thread already joined)
    if(t1.joinable())
    {
        t1.detach();
    }

    cout << "main() after" << endl;
    return 0;
}
```

**Output:**
```
main()
count: 9
count: 8
count: 7
count: 6
count: 5
count: 4
count: 3
count: 2
count: 1
count: 0
main() after
```

---

## 📊 Comparison: join() vs detach()

| Feature | join() | detach() |
|---------|--------|----------|
| **Waits for completion** | ✅ Yes | ❌ No |
| **Thread independence** | ❌ Dependent on parent | ✅ Independent |
| **Resource cleanup** | ✅ Guaranteed | ⚠️ OS handles it |
| **Use case** | When you need results | Background tasks |
| **Risk** | Blocking | May terminate prematurely |

---

## 🎯 Best Practices

### ✅ DO:

```cpp
// Always check joinable before join/detach
if(t.joinable()) {
    t.join();
}

// Use join() when you need to wait for completion
thread t(func);
t.join();  // Safe and predictable

// For long-running background tasks, use detach carefully
thread t(backgroundTask);
t.detach();  // Make sure task won't crash if main exits
```

### ❌ DON'T:

```cpp
// Never double join
t.join();
t.join();  // CRASH!

// Never double detach
t.detach();
t.detach();  // CRASH!

// Never forget to join or detach
thread t(func);
// Missing t.join() or t.detach() - CRASH on destructor!
```

---

## 🔍 joinable() Function

**Returns `true` when:**
- Thread object represents an active thread of execution
- Thread has been created but not yet joined or detached

**Returns `false` when:**
- Thread has been joined
- Thread has been detached
- Thread is default-constructed (no function assigned)

**Usage:**
```cpp
thread t(func);
cout << t.joinable();  // true

t.join();
cout << t.joinable();  // false
```

---

## 💡 Key Takeaways

1. ⚠️ **Always call either `join()` or `detach()`** on every thread
2. ✅ **Use `joinable()` to check** before calling `join()` or `detach()`
3. 🔒 **Use `join()` for predictable behavior** and guaranteed completion
4. 🚀 **Use `detach()` sparingly** for truly independent background tasks
5. 💥 **Double join/detach causes termination** - always protect with `joinable()`
6. 🧹 **Thread destructor checks `joinable()`** - if true, program terminates

---

## Compilation

```bash
g++ -std=c++11 -pthread filename.cpp -o output
./output
```