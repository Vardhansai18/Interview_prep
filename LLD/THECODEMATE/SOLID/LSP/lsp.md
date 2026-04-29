# SOLID Principles

---

## Liskov Substitution Principle (LSP)

### 📌 Definition

> **"Derived class should be replaceable for base class."**

### 🧠 Intuition

**Child class should NOT break parent behavior.**

In LSP, you typically have:
- **Base class** (abstraction) → `Vehicle`
- **Derived classes** → `Car`, `Bicycle`

**Key idea:** You should be able to replace `Vehicle` with `Car` or `Bicycle` without breaking behavior.

---

## 🚗 Vehicle Example

### 🔴 Bad Design (Violates LSP)

Let's assume **all vehicles** can:
- Start engine
- Drive

```cpp
#include <iostream>
using namespace std;

class Vehicle {
public:
    virtual void startEngine() {
        cout << "Starting engine\n";
    }

    virtual void drive() {
        cout << "Driving vehicle\n";
    }
};

class Car : public Vehicle {
public:
    void startEngine() override {
        cout << "Car engine started\n";
    }
};

class Bicycle : public Vehicle {
public:
    void startEngine() override {
        throw "Bicycle has no engine!";  // 💥 Problem!
    }
};
```

#### 🚨 Problem

**Bicycle breaks expected behavior!**

If client code does:

```cpp
void test(Vehicle* v) {
    v->startEngine();  // 💥 breaks for Bicycle
}
```

👉 **Substitution fails** → LSP violated

#### 🧠 Why This is Wrong

**LSP says:**
> Derived class should behave like base class without surprises

**But:**
- Base class **promises** `startEngine()`
- Bicycle **cannot fulfill** it

---

### 🟢 Good Design (Applying LSP)

👉 **Split abstraction properly**

```cpp
#include <iostream>
using namespace std;

// Base abstraction - common for ALL vehicles
class Vehicle {
public:
    virtual void move() = 0;
    virtual ~Vehicle() {}
};

// Only for engine-based vehicles
class EngineVehicle : public Vehicle {
public:
    virtual void startEngine() = 0;
};

// ------------------ Car ------------------
class Car : public EngineVehicle {
public:
    void startEngine() override {
        cout << "Car engine started\n";
    }

    void move() override {
        cout << "Car is driving\n";
    }
};

// ------------------ Bicycle ------------------
class Bicycle : public Vehicle {
public:
    void move() override {
        cout << "Bicycle is pedaling\n";
    }
};
```

#### 🧪 Client Code (Now Safe)

```cpp
void travel(Vehicle* v) {
    v->move();   // ✅ Works for ALL vehicles
}

int main() {
    Vehicle* car = new Car();
    Vehicle* bike = new Bicycle();
    
    travel(car);   // ✅ Car is driving
    travel(bike);  // ✅ Bicycle is pedaling
    
    // Engine-specific operations
    EngineVehicle* engineCar = new Car();
    engineCar->startEngine();  // ✅ Only for engine vehicles
    
    delete car;
    delete bike;
    delete engineCar;
    
    return 0;
}
```

---

### 🔍 Why This Works

| Class            | Responsibility          |
|------------------|-------------------------|
| `Vehicle`        | Movement (all vehicles) |
| `EngineVehicle`  | Engine behavior         |
| `Car`            | Engine + movement       |
| `Bicycle`        | Only movement           |

✅ **No broken expectations**  
✅ **Substitution works perfectly**

---

## ⚡ Key Insight (Interview Gold)

**Say this in interviews:**

> "I avoided forcing all vehicles to support engine-related behavior by introducing a refined abstraction (`EngineVehicle`). This ensures that subclasses don't violate expected contracts."

---

## 🚀 Real-Life Mapping

| Concept    | Example        |
|------------|----------------|
| `Vehicle`  | Transport      |
| `Car`      | Engine-based   |
| `Bicycle`  | Human-powered  |

---

## ❌ Common Mistake (Very Important)

**Many candidates do:**

```cpp
class Vehicle {
    virtual void startEngine();
};
```

👉 This is **WRONG design**  
👉 **Not all vehicles have engines**

---

## 🧠 Mental Model for LSP

**Ask yourself:**

> "Can I replace parent with child without breaking code?"

- **If YES** ✅ → LSP satisfied
- **If NO** ❌ → Redesign abstraction

---

## 🔥 Advanced Insight

### LSP violations often come from:

1. **Wrong inheritance hierarchy**
2. **Over-generalized base classes**
3. **Forcing common interface on incompatible types**

### Better approach:

✅ **Use capability-based design**
- `EngineVehicle` for vehicles with engines
- `ElectricVehicle` for electric vehicles
- `ManualVehicle` for human-powered vehicles

---

## 💡 Real Interview Questions

### Q: "How does LSP differ from basic inheritance?"

**Answer:**
> "Inheritance is about code reuse. LSP is about **behavioral compatibility**. A child class must not only inherit from parent, but must be **substitutable** for it without breaking functionality."

### Q: "What happens if you violate LSP?"

**Answer:**
> "You get:
> - Runtime errors
> - Need for `instanceof` or type checking
> - Fragile code that breaks when adding new types
> - Violated OCP (Open/Closed Principle)"

---

## 🚀 Key Takeaway

**LSP ensures:**
- ✅ **Behavioral substitutability** - Child can replace parent
- ✅ **Contract compliance** - Child honors parent's promises
- ✅ **No surprises** - Client code works with any subtype

**Think:** "Every subclass should enhance, not break, the parent's contract."
