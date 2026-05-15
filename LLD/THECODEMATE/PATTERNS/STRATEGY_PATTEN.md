# Strategy Pattern

## 📑 Table of Contents
- [📋 Overview](#-overview)
  - [🎨 UML Diagram](#-uml-diagram)
- [🎬 Real Life Example: Navigation App](#-real-life-example-navigation-app)
- [❌ Problem Without Strategy Pattern](#-problem-without-strategy-pattern)
- [⚠️ Problems in This Design](#️-problems-in-this-design)
- [✅ Strategy Pattern Solution](#-strategy-pattern-solution)
- [🏗️ Structure of Strategy Pattern](#️-structure-of-strategy-pattern)
- [💻 Code: AFTER Strategy Pattern](#-code-after-strategy-pattern)
- [📊 UML Structure](#-uml-structure)
- [🎓 When Should You Use Strategy Pattern?](#-when-should-you-use-strategy-pattern)
- [🌍 Real World Examples](#-real-world-examples)
- [✨ Advantages](#-advantages)
- [⚠️ Drawbacks](#️-drawbacks)
- [🔄 Strategy vs Factory Pattern](#-strategy-vs-factory-pattern)
- [💼 In Your JIRA / Task Management LLD](#-in-your-jira--task-management-lld)
- [📝 Key Interview Definition](#-key-interview-definition)

---

## 📋 Overview

The **Strategy Pattern** is a **Behavioral Design Pattern**.

### Definition
> Used when you have **multiple ways to perform the same behavior** and you want to **switch behavior dynamically at runtime** without writing large if-else or switch statements everywhere.

### 🎨 UML Diagram
> 📐 [**View Interactive UML Diagram on Excalidraw**](https://excalidraw.com/#room=5e13347d83844189f149,t00h0S-auu7a1wpzyLueAw)

---

## 🎬 Real Life Example: Navigation App

### Think about Google Maps 🗺️

A user can choose:
- 🚗 **Car route**
- 🚴 **Bike route**
- 🚶 **Walking route**

The app behavior changes based on the selected travel strategy.

### ❌ Without Strategy Pattern

```cpp
if(type == "car") { 
    // Car routing logic
}
else if(type == "bike") { 
    // Bike routing logic
}
else if(type == "walk") { 
    // Walking routing logic
}
```

### ✅ With Strategy Pattern

Each routing algorithm becomes a **separate strategy**.
- `CarRouteStrategy`
- `BikeRouteStrategy`
- `WalkRouteStrategy`

**Clean, extensible, and maintainable!**

---

## ❌ Problem Without Strategy Pattern

### Scenario: Building a Payment System

We support:
- 💳 **Credit Card**
- 📱 **UPI**
- 💰 **PayPal**

### Code BEFORE Strategy Pattern

```cpp
#include <iostream>
using namespace std;

class PaymentService {
public:
    void pay(string paymentType, int amount) {
        
        if(paymentType == "creditcard") {
            cout << "Paid " << amount
                 << " using Credit Card\n";
        }
        else if(paymentType == "upi") {
            cout << "Paid " << amount
                 << " using UPI\n";
        }
        else if(paymentType == "paypal") {
            cout << "Paid " << amount
                 << " using PayPal\n";
        }
    }
};

int main() {
    PaymentService payment;
    payment.pay("upi", 1000);
    
    return 0;
}
```

---

## ⚠️ Problems in This Design

### 1. Violates Open/Closed Principle ❌

Every time you add:
- 🍎 Apple Pay
- ₿ Crypto
- 🏦 Net Banking

**You must modify existing code!**

Bad for scalability.

### 2. Large if-else chain 🔗

As features grow:
```cpp
if(...)
else if(...)
else if(...)
else if(...)
else if(...) // Becomes messy!
```

### 3. Difficult Testing 🧪

Cannot test each algorithm independently.

### 4. Tight Coupling 🔒

`PaymentService` knows all payment algorithms.

| Problem | Impact |
|---------|--------|
| **Violates OCP** | Must modify existing code for new features |
| **if-else Hell** | Code becomes messy and unreadable |
| **No Isolation** | Can't test strategies independently |
| **Tight Coupling** | Context knows too much |

---

## ✅ Strategy Pattern Solution

**We separate each payment algorithm into its own class.**

---

## 🏗️ Structure of Strategy Pattern

### 1. Strategy Interface 📋

Common behavior contract.

```cpp
class PaymentStrategy {
public:
    virtual void pay(int amount) = 0;
};
```

### 2. Concrete Strategies 🛠️

Different implementations.

- `UPIPayment : public PaymentStrategy`
- `CreditCardPayment : public PaymentStrategy`
- `PaypalPayment : public PaymentStrategy`

### 3. Context Class 🎯

Uses strategy dynamically.

- `PaymentService` - holds and uses the strategy

---

## 💻 Code: AFTER Strategy Pattern

```cpp
#include <iostream>
using namespace std;

///////////////////////////////////////////////////////////
// STRATEGY INTERFACE (Abstraction)
///////////////////////////////////////////////////////////

class PaymentStrategy {
public:
    virtual void pay(int amount) = 0;
    virtual ~PaymentStrategy() {}
};

///////////////////////////////////////////////////////////
// CONCRETE STRATEGIES (Implementations)
///////////////////////////////////////////////////////////

class CreditCardPayment : public PaymentStrategy {
public:
    void pay(int amount) override {
        cout << "Paid " << amount 
             << " using Credit Card\n";
    }
};

class UPIPayment : public PaymentStrategy {
public:
    void pay(int amount) override {
        cout << "Paid " << amount 
             << " using UPI\n";
    }
};

class PaypalPayment : public PaymentStrategy {
public:
    void pay(int amount) override {
        cout << "Paid " << amount 
             << " using PayPal\n";
    }
};

///////////////////////////////////////////////////////////
// CONTEXT CLASS (Uses Strategy)
///////////////////////////////////////////////////////////

class PaymentService {
private:
    PaymentStrategy* strategy;

public:
    PaymentService(PaymentStrategy* strategy) {
        this->strategy = strategy;
    }

    // Switch strategy at runtime
    void setStrategy(PaymentStrategy* strategy) {
        this->strategy = strategy;
    }

    // Delegate to strategy
    void makePayment(int amount) {
        strategy->pay(amount);
    }
};

///////////////////////////////////////////////////////////
// MAIN (CLIENT)
///////////////////////////////////////////////////////////

int main() {
    // Create strategies
    UPIPayment upi;
    CreditCardPayment card;
    PaypalPayment paypal;

    // Start with UPI
    PaymentService paymentService(&upi);
    paymentService.makePayment(1000);

    // Switch to Credit Card
    paymentService.setStrategy(&card);
    paymentService.makePayment(2000);

    // Switch to PayPal
    paymentService.setStrategy(&paypal);
    paymentService.makePayment(3000);

    return 0;
}
```

**Output:**
```
Paid 1000 using UPI
Paid 2000 using Credit Card
Paid 3000 using PayPal
```

---

## 📊 UML Structure

### BEFORE Strategy Pattern 🔴

```
PaymentService
    |
    |-- if(type == UPI)     ❌
    |-- if(type == CARD)    ❌
    |-- if(type == PAYPAL)  ❌
```

**Everything tightly coupled!**

### AFTER Strategy Pattern 🟢

```
                +------------------+
                | PaymentStrategy  |  ← Interface
                +------------------+
                | + pay()          |
                +------------------+
                         ^
        ------------------------------------
        |                |                |
+----------------+ +----------------+ +----------------+
| UPIPayment     | | CreditCard     | | PaypalPayment  |
+----------------+ +----------------+ +----------------+
| + pay()        | | + pay()        | | + pay()        |
+----------------+ +----------------+ +----------------+

                         ^
                         |
                +------------------+
                | PaymentService   |  ← Context
                +------------------+
                | - strategy*      |
                +------------------+
                | + makePayment()  |
                | + setStrategy()  |
                +------------------+
```

**Clean architecture!** ✨

---

## 🎓 When Should You Use Strategy Pattern?

### ✅ Use When:

#### 1. Multiple Algorithms Exist

Examples:
- 🔄 Sorting algorithms (QuickSort, MergeSort, BubbleSort)
- 💳 Payment methods (UPI, Card, PayPal)
- 📦 Compression techniques (ZIP, RAR, 7ZIP)
- 📧 Notification channels (Email, SMS, Push)

#### 2. Behavior Changes at Runtime

```cpp
payment.setStrategy(new UPIPayment());
// Later...
payment.setStrategy(new CardPayment());
```

#### 3. Want to Avoid Large if-else Chains

Replace messy conditionals with clean strategy classes.

---

## 🌍 Real World Examples

| System | Strategies |
|--------|-----------|
| **Payment System** | UPI, Card, PayPal, ApplePay, Crypto |
| **Navigation App** | Car, Bike, Walk, Transit |
| **Compression Tool** | ZIP, RAR, 7ZIP, TAR |
| **Notification System** | Email, SMS, Push, Slack |
| **Authentication** | OAuth, SAML, JWT, Basic Auth |
| **Sorting Library** | QuickSort, MergeSort, HeapSort |
| **Image Processing** | PNG, JPEG, WebP converters |

---

## ✨ Advantages

| Advantage | Explanation |
|-----------|-------------|
| **Open/Closed Principle ✅** | Add new strategy without modifying existing code |
| **Removes if-else 🧹** | Cleaner, more maintainable code |
| **Runtime Flexibility 🔄** | Switch behavior dynamically |
| **Better Testing 🧪** | Test each strategy independently |
| **Loose Coupling 🔓** | Context depends only on interface |
| **Single Responsibility 📦** | Each strategy has one job |

### Example: Adding New Strategy

```cpp
// Just add new class - no existing code changes!
class CryptoPayment : public PaymentStrategy {
public:
    void pay(int amount) override {
        cout << "Paid " << amount << " using Crypto\n";
    }
};

// Usage
CryptoPayment crypto;
paymentService.setStrategy(&crypto);
paymentService.makePayment(5000);
```

**No changes to `PaymentService` or other strategies!** 🎉

---

## ⚠️ Drawbacks

| Drawback | Explanation |
|----------|-------------|
| **More Classes** | Each strategy becomes a separate class |
| **Slightly Complex** | For very small systems, may feel over-engineered |
| **Client Awareness** | Client must know and choose correct strategy |
| **Memory Overhead** | Multiple objects in memory |

### When to Avoid ❌

- Only 2-3 simple strategies with no growth expected
- Algorithm never changes at runtime
- Very simple conditional logic
- Performance is extremely critical

---

## 🔄 Strategy vs Factory Pattern

| Aspect | Strategy | Factory |
|--------|----------|---------|
| **Purpose** | Changes behavior | Creates objects |
| **Pattern Type** | Behavioral | Creational |
| **Focus** | Runtime algorithm selection | Object creation abstraction |
| **When Used** | Multiple ways to do same thing | Multiple types of objects to create |
| **Example** | Payment methods | Vehicle types |

### Can Be Used Together! 🤝

```cpp
// Factory creates strategies
PaymentStrategy* strategy = 
    PaymentFactory::createStrategy("upi");

// Context uses strategy
PaymentService service(strategy);
service.makePayment(1000);
```

---

## 💼 In Your JIRA / Task Management LLD

You can apply Strategy Pattern for:

### 1. Notification Strategy 📧

```cpp
class NotificationStrategy {
public:
    virtual void notify(User user, Message msg) = 0;
};

class EmailNotification : public NotificationStrategy { };
class SMSNotification : public NotificationStrategy { };
class SlackNotification : public NotificationStrategy { };
```

### 2. Authentication Strategy 🔐

```cpp
class AuthStrategy {
public:
    virtual bool authenticate(User user) = 0;
};

class OAuthStrategy : public AuthStrategy { };
class JWTStrategy : public AuthStrategy { };
class SAMLStrategy : public AuthStrategy { };
```

### 3. Task Assignment Strategy 📋

```cpp
class TaskAssignmentStrategy {
public:
    virtual User* assignTask(Task task, vector<User> users) = 0;
};

class RoundRobinStrategy : public TaskAssignmentStrategy { };
class LeastLoadedStrategy : public TaskAssignmentStrategy { };
class ManualAssignmentStrategy : public TaskAssignmentStrategy { };
```

---

## 📝 Key Interview Definition

> **Strategy Pattern** defines a **family of algorithms**, **encapsulates each one**, and makes them **interchangeable at runtime**.

### Key Points to Remember: 🎯

1. **Behavioral pattern** - focuses on algorithms/behaviors
2. **Runtime flexibility** - switch strategies dynamically
3. **Eliminates conditionals** - no if-else chains
4. **Follows OCP** - open for extension, closed for modification
5. **Delegation over inheritance** - composition-based design

---

## 🎯 Modern C++ Version (Best Practice)

### Using Smart Pointers

```cpp
#include <memory>
#include <iostream>
using namespace std;

class PaymentService {
private:
    unique_ptr<PaymentStrategy> strategy;

public:
    PaymentService(unique_ptr<PaymentStrategy> strat) 
        : strategy(move(strat)) {}

    void setStrategy(unique_ptr<PaymentStrategy> strat) {
        strategy = move(strat);
    }

    void makePayment(int amount) {
        strategy->pay(amount);
    }
};

// Usage
int main() {
    auto payment = make_unique<PaymentService>(
        make_unique<UPIPayment>()
    );
    
    payment->makePayment(1000);
    
    payment->setStrategy(make_unique<CardPayment>());
    payment->makePayment(2000);
    
    return 0;
}
```

**Benefits:**
- ✅ Automatic memory management
- ✅ No memory leaks
- ✅ Exception safe
- ✅ Modern C++ best practice

---

## 🔗 Related Patterns

- **State Pattern** - Similar structure, but state changes behavior based on internal state
- **Factory Pattern** - Can create strategy objects
- **Template Method** - Alternative using inheritance instead of composition
- **Command Pattern** - Encapsulates requests as objects

---

## 💡 Pro Tips

1. **Use Strategy with Factory** - Factory creates appropriate strategy
2. **Consider lambdas** - For simple strategies, use `std::function`
3. **Thread safety** - Use mutex if switching strategies in multi-threaded code
4. **Default strategy** - Always have a sensible default
5. **Strategy validation** - Validate input before delegating to strategy

---

## 🎬 Summary

```
WITHOUT Strategy:
  if (type == UPI) { ... }        ❌ Tight coupling
  else if (type == CARD) { ... }  ❌ Hard to extend
  else if (type == PAYPAL) { ... }❌ Violates OCP

WITH Strategy:
  Context → Strategy Interface     ✅ Loose coupling
              ↓                    ✅ Easy to extend
    [UPI, Card, PayPal, ...]       ✅ Follows OCP
```

**Remember:** Strategy Pattern = **Select algorithm at runtime!** 🚀