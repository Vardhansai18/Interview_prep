# SOLID Principles

![SOLID Principles Diagram](image-4.png)

---

## Single Responsibility Principle (SRP)

### 📌 Definition
UML: [Excalidraw - SRP UML](https://excalidraw.com/#json=PuI1yMIQUunzWiVKw99_Y,LpFQo36eKgJAm-AuRbpQWQ)

> **"A class should have only ONE reason to change."**

### 🧠 Intuition

Don't mix responsibilities. Each class should have **one job** and one job only.

### 🌍 Real-life Example

- A **Restaurant Chef** cooks
- A **Waiter** serves
- If the chef also serves → **messy responsibilities**

---

## 🍽️ Restaurant Example (Code-Level Design)

### ❌ Bad Design (Violation of SRP)

In this example, one class is handling **multiple responsibilities**:
- Cooking
- Serving

```cpp
#include <iostream>
using namespace std;

class RestaurantStaff {
public:
    void cookFood() {
        cout << "Cooking food...\n";
    }

    void serveFood() {
        cout << "Serving food to customer...\n";
    }
};
```

#### 🚨 Problem

- If **cooking logic** changes → class changes
- If **serving logic** changes → same class changes
- 👉 **Multiple reasons to change** → SRP violation

---

### ✅ Good Design (Applying SRP)

We **split responsibilities** into separate classes:

#### 👨‍🍳 Chef → Only cooks

```cpp
class Chef {
public:
    void cookFood() {
        cout << "Chef is cooking food\n";
    }
};
```

#### 🧑‍💼 Waiter → Only serves

```cpp
class Waiter {
public:
    void serveFood() {
        cout << "Waiter is serving food\n";
    }
};
```

#### 🧾 Order (Optional — for better design)

```cpp
class Order {
public:
    string item;
    Order(string item) : item(item) {}
};
```

#### 🧠 Usage (How the system works together)

```cpp
int main() {
    Chef chef;
    Waiter waiter;

    Order order("Pasta");

    chef.cookFood();      // Chef responsibility
    waiter.serveFood();   // Waiter responsibility

    return 0;
}
```

---

### 🔍 Why This is SRP Correct

| Class    | Responsibility |
|----------|----------------|
| `Chef`   | Cooking        |
| `Waiter` | Serving        |
| `Order`  | Data           |

👉 **Each class has only ONE reason to change**

---

## 💡 Real Interview Insight

**If interviewer asks:**

> "What if tomorrow we add home delivery?"

### With SRP ✅

You just add a new class:

```cpp
class DeliveryAgent {
public:
    void deliverFood() {
        cout << "Delivering food\n";
    }
};
```

### Without SRP ❌

You would need to **modify existing class** → risky + messy

---

## 🧠 Design Thinking Pattern

When designing, **ask yourself:**

> "Can I describe this class in ONE sentence?"

### Examples:

- `Chef` → cooks food ✅
- `Waiter` → serves food ✅
- `RestaurantStaff` → cooks + serves ❌ (bad abstraction)

---

## ⚡ Advanced Example (Better LLD Version)

A more realistic implementation with better integration:

```cpp
class Order {
public:
    string item;
    Order(string item) : item(item) {}
};

class Chef {
public:
    void prepareOrder(const Order& order) {
        cout << "Preparing " << order.item << endl;
    }
};

class Waiter {
public:
    void serveOrder(const Order& order) {
        cout << "Serving " << order.item << endl;
    }
};
```

---

## 🚀 Key Takeaway

**SRP is NOT about:**
- "One function per class"

**It's about:**
- ✅ One **responsibility** per class
- ✅ One **reason to change**
