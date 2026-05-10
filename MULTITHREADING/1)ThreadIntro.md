# Introduction to Threads in C++ (C++11)

## What is a Thread?

**Definition:**
- A thread is also known as a **lightweight process**
- The idea is to achieve parallelism by dividing a process into multiple threads
- In every application, there is a default thread which is `main()`, inside this we create other threads

**Real-World Examples:**

1. **Browser:** Multiple tabs can be different threads
2. **MS Word:** 
   - One thread to format the text
   - Another thread to process inputs (spell checker)
3. **VS Code Editor:** 
   - Uses threading for auto-completing code (IntelliSense)

---

## Ways to Create Threads in C++11

1. **Function Pointers**
2. **Lambda Functions**
3. **Functors**
4. **Member Functions**
5. **Static Member Functions**

---

## Example: Sequential vs Parallel Execution

**Problem Statement:**
Find the sum of all odd numbers from 1 to 1,900,000,000 and all even numbers from 1 to 1,900,000,000

---

### Method 1: Sequential Execution (Without Threads)

```cpp
#include <iostream>
#include <chrono>

typedef unsigned long long ull;
using namespace std;
using namespace chrono;

void findOdd(ull start, ull end)
{
    ull oddSum = 0;

    for (ull i = start; i <= end; i++)
    {
        if ((i & 1) != 0)
        {
            oddSum += i;
        }
    }

    cout << "Odd Sum : " << oddSum << endl;
}

void findEven(ull start, ull end)
{
    ull evenSum = 0;

    for (ull i = start; i <= end; i++)
    {
        if ((i & 1) == 0)
        {
            evenSum += i;
        }
    }
    cout << "Even Sum : " << evenSum << endl;
}

int main()
{
    ull start = 0, end = 1900000000;

    auto totalStart = high_resolution_clock::now();

    // Sequential execution - one after another
    findOdd(start, end);
    findEven(start, end);

    auto totalEnd = high_resolution_clock::now();

    auto totalDuration =
        duration_cast<microseconds>(totalEnd - totalStart);

    cout << "Total Execution Time : "
         << totalDuration.count() / 1000000  << " s" << endl;
}
```

**Output:**
```
Odd Sum : 902500000000000000
Even Sum : 902500000950000000
Total Execution Time : 4 s
```

**Analysis:**
- ⏱️ Execution time: **4 seconds**
- Functions execute sequentially (one after another)
- CPU is not fully utilized

---

### Method 2: Parallel Execution (With Threads)

```cpp
#include <iostream>
#include <thread>
#include <chrono>

typedef unsigned long long ull;
using namespace std;
using namespace chrono;

void findOdd(ull start, ull end)
{
    ull oddSum = 0;

    for (ull i = start; i <= end; i++)
    {
        if ((i & 1) != 0)
        {
            oddSum += i;
        }
    }

    cout << "Odd Sum : " << oddSum << endl;
}

void findEven(ull start, ull end)
{
    ull evenSum = 0;

    for (ull i = start; i <= end; i++)
    {
        if ((i & 1) == 0)
        {
            evenSum += i;
        }
    }
    cout << "Even Sum : " << evenSum << endl;
}

int main()
{
    ull start = 0, end = 1900000000;

    auto totalStart = high_resolution_clock::now();

    // Create two threads for parallel execution
    thread Odd(findOdd, start, end);
    thread Even(findEven, start, end);

    // Wait for both threads to complete
    Odd.join();
    Even.join();

    auto totalEnd = high_resolution_clock::now();

    auto totalDuration =
        duration_cast<microseconds>(totalEnd - totalStart);

    cout << "Total Execution Time : "
         << totalDuration.count() / 1000000  << " s" << endl;
}
```

**Output:**
```
Odd Sum : 902500000000000000
Even Sum : 902500000950000000
Total Execution Time : 2 s
```

**Analysis:**
- ⚡ Execution time: **2 seconds** 
- **50% faster** than sequential execution!
- Both functions execute simultaneously on different CPU cores
- Better CPU utilization through parallelism

---

## Key Concepts

### Thread Creation
```cpp
thread threadName(functionName, arg1, arg2, ...);
```

### Thread Join
- `join()` blocks the calling thread until the thread completes
- Ensures the main thread waits for worker threads to finish
- **Must call `join()` or `detach()` on every thread**

---

## Compilation & Execution

**Compile:**
```bash
g++ -std=c++11 -pthread filename.cpp -o output
```

**Run:**
```bash
./output
```

---

## Performance Comparison

| Method | Execution Time | Speed Improvement |
|--------|---------------|-------------------|
| Sequential (No Threads) | 4 seconds | Baseline |
| Parallel (With Threads) | 2 seconds | **2x faster** |

---

## Key Takeaways

✅ Threads enable parallel execution of tasks  
✅ Can significantly reduce execution time for independent operations  
✅ Must use `join()` to wait for thread completion  
✅ Requires `-pthread` flag during compilation  
✅ Best used when tasks are CPU-intensive and independent