# SOLID Principles

---

## Dependency Inversion Principle (DIP)

### 📌 Definition

> **"High-level modules should not depend on low-level modules. Both should depend on abstractions."**

### 🧠 Intuition

- **Don't depend on concrete implementations**
- **Depend on abstractions (interfaces/abstract classes)**
- **Invert the dependency direction**

### 🌍 Real-life Example: Switch & Devices

A **Switch** (high-level) controls devices:
- Light
- Fan
- AC

👉 **Switch should NOT depend on Light directly**  
✅ **Switch should depend on a Device abstraction**

---

## 💡 Switch & Device Example

### 🔴 Bad Design (Violates DIP)

The high-level module (**Switch**) depends directly on the low-level module (**Light**):

```cpp
#include <iostream>
using namespace std;

class Light {
public:
    void turnOn() {
        cout << "Light ON\n";
    }
};

class Switch {
    Light light;  // ❌ Tightly coupled to Light
public:
    void operate() {
        light.turnOn();
    }
};

int main() {
    Switch s;
    s.operate();
    return 0;
}
```

#### 🚨 Problems

- `Switch` depends **directly** on `Light`
- Cannot reuse `Switch` for:
  - Fan
  - AC
  - Any other device
- 👉 **Not flexible, tightly coupled**
- Hard to test (can't mock Light)

---

### 🟢 Good Design (Applying DIP)

👉 **Create a common abstraction: `Device` interface**

```cpp
#include <iostream>
using namespace std;

// -------------------- Abstraction --------------------
class Device {
public:
    virtual void turnOn() = 0;
    virtual ~Device() {}
};

// -------------------- Low-Level Modules --------------------
class Light : public Device {
public:
    void turnOn() override {
        cout << "Light is ON\n";
    }
};

class Fan : public Device {
public:
    void turnOn() override {
        cout << "Fan is ON\n";
    }
};

class AC : public Device {
public:
    void turnOn() override {
        cout << "AC is ON\n";
    }
};

// -------------------- High-Level Module --------------------
class Switch {
private:
    Device* device;  // ✅ Depends on abstraction

public:
    // Dependency Injection via constructor
    Switch(Device* d) : device(d) {}

    void operate() {
        device->turnOn();
    }
};

// -------------------- Main --------------------
int main() {
    Light light;
    Fan fan;
    AC ac;

    cout << "Using Light:\n";
    Switch s1(&light);
    s1.operate();

    cout << "\nUsing Fan:\n";
    Switch s2(&fan);
    s2.operate();

    cout << "\nUsing AC:\n";
    Switch s3(&ac);
    s3.operate();

    return 0;
}
```

#### 📤 Output

```
Using Light:
Light is ON

Using Fan:
Fan is ON

Using AC:
AC is ON
```

---

### 🔍 Why This Follows DIP

| Component        | Depends On          |
|------------------|---------------------|
| `Switch`         | `Device` (abstraction) |
| `Light`/`Fan`/`AC` | `Device` (abstraction) |

✅ **No direct dependency between:**
- ❌ `Switch` → `Light`
- ❌ `Switch` → `Fan`

✅ **Both depend on abstraction:**
- ✅ `Switch` → `Device`
- ✅ `Light`/`Fan`/`AC` → `Device`

---

## 🧠 Key Interview Explanation

**Say this in interviews:**

> "I inverted the dependency by introducing a `Device` abstraction. The high-level module (`Switch`) depends on the abstraction instead of concrete implementations. This allows us to plug in any device without modifying the `Switch`."

---

## ⚡ Key Concept: Dependency Injection

```cpp
Switch s(&light);  // Injecting dependency from outside
```

👉 **We inject the dependency from outside** (not created inside Switch)

### Types of Dependency Injection:

| Type | Description | Example |
|------|-------------|---------|
| **Constructor Injection** | Pass via constructor | `Switch(Device* d)` |
| **Setter Injection** | Pass via setter method | `setDevice(Device* d)` |
| **Interface Injection** | Pass via interface method | Less common in C++ |

---

## 🚀 What Happens If Requirements Change?

**Scenario:** Need to add a new device (Heater)

### ✅ With DIP

Just add the new device:

```cpp
class Heater : public Device {
public:
    void turnOn() override {
        cout << "Heater is ON\n";
    }
};

// Usage
Heater heater;
Switch s4(&heater);
s4.operate();  // ✅ Works immediately!
```

**✅ No changes needed in `Switch` class!**

### ❌ Without DIP

You would need to:
1. Modify the `Switch` class
2. Add if-else or switch statements
3. Recompile and retest everything

---

## 🧩 Mental Model

### Without DIP (Tight Coupling)

```
Switch → Light (direct dependency)
```

### With DIP (Loose Coupling)

```
       Device (abstraction)
         ↗     ↖
    Switch     Light/Fan/AC
```

Both Switch and concrete devices depend on the abstraction.

---

## 🔥 Advanced Insight

### DIP + OCP = Powerful Design

When you combine **DIP** with **OCP (Open/Closed Principle)**:

- ✅ **Plug-and-play design**
- ✅ **Highly extensible systems**
- ✅ **Easy to test** (mock dependencies)
- ✅ **Decoupled architecture**

👉 **This is the foundation of:**
- Spring Boot (Dependency Injection)
- Dependency Injection frameworks
- Microservices architecture
- Testable code

---

## 💡 Real-World Examples

### Example 1: Database Layer

#### ❌ Bad Design

```cpp
class UserService {
    MySQLDatabase db;  // ❌ Tied to MySQL
public:
    void saveUser() {
        db.insert();
    }
};
```

#### ✅ Good Design

```cpp
class Database {
public:
    virtual void insert() = 0;
};

class MySQLDatabase : public Database { /* ... */ };
class PostgreSQLDatabase : public Database { /* ... */ };

class UserService {
    Database* db;  // ✅ Depends on abstraction
public:
    UserService(Database* database) : db(database) {}
    void saveUser() {
        db->insert();
    }
};
```

---

### Example 2: Notification System

#### ❌ Bad Design

```cpp
class OrderService {
    EmailService email;  // ❌ Tied to email
public:
    void processOrder() {
        email.send();
    }
};
```

#### ✅ Good Design

```cpp
class Notifier {
public:
    virtual void notify() = 0;
};

class EmailNotifier : public Notifier { /* ... */ };
class SMSNotifier : public Notifier { /* ... */ };
class PushNotifier : public Notifier { /* ... */ };

class OrderService {
    Notifier* notifier;  // ✅ Flexible
public:
    OrderService(Notifier* n) : notifier(n) {}
    void processOrder() {
        notifier->notify();
    }
};
```

---

## 🎯 Benefits of DIP

| Benefit | Description |
|---------|-------------|
| **Flexibility** | Easy to swap implementations |
| **Testability** | Mock dependencies in unit tests |
| **Maintainability** | Changes localized to specific modules |
| **Reusability** | High-level modules can be reused |
| **Decoupling** | Modules are independent |

---

## 🧪 Testing Benefits

With DIP, testing becomes easy:

```cpp
class MockDevice : public Device {
public:
    bool wasCalled = false;
    
    void turnOn() override {
        wasCalled = true;
    }
};

// In test
MockDevice mock;
Switch s(&mock);
s.operate();
assert(mock.wasCalled);  // ✅ Easy to verify
```

---

## 🚀 Key Takeaway

**DIP ensures:**
- ✅ **High-level modules** don't depend on low-level modules
- ✅ **Both depend on abstractions**
- ✅ **Easy to extend** without modifying existing code
- ✅ **Highly testable** and maintainable

**Think:** "Depend on what things do (abstraction), not on how they do it (implementation)."
