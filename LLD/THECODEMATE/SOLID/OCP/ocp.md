# SOLID Principles

---

## Open/Closed Principle (OCP)

### 📌 Definition

> **"Open for extension, closed for modification."**

### 🧠 Intuition

You should be able to **add new behavior** WITHOUT modifying existing code.

### 🌍 Real-life Example

**Payment System:** Adding new payment methods like:
- UPI
- Credit Card
- PayPal

You **shouldn't modify** old payment logic every time you add a new payment method.

---

## 💳 Payment System Example

### ❌ Bad Design (Violation of OCP)

Every time you add a new payment method, you **modify** the existing class:

```cpp
class Payment {
public:
    void pay(string type) {
        if(type == "card") { 
            // Card payment logic 
        }
        else if(type == "upi") { 
            // UPI payment logic 
        }
        // Adding PayPal? Modify this class again!
    }
};
```

#### 🚨 Problem

- Adding new payment method = **modifying existing code**
- Violates "closed for modification"
- Risk of breaking existing functionality
- Growing if-else chains

---

### ✅ Good Design (Applying OCP with Polymorphism)

Use **inheritance and polymorphism** to extend behavior:

#### Base Payment Interface

```cpp
class Payment {
public:
    virtual void pay() = 0;  // Pure virtual function
    virtual ~Payment() {}
};
```

#### Card Payment Implementation

```cpp
class CardPayment : public Payment {
public:
    void pay() override {
        cout << "Processing card payment\n";
        // Card-specific logic
    }
};
```

#### UPI Payment Implementation

```cpp
class UPIPayment : public Payment {
public:
    void pay() override {
        cout << "Processing UPI payment\n";
        // UPI-specific logic
    }
};
```

#### Adding PayPal (Extension without Modification)

```cpp
class PayPalPayment : public Payment {
public:
    void pay() override {
        cout << "Processing PayPal payment\n";
        // PayPal-specific logic
    }
};
```

#### 🧠 Usage

```cpp
void processPayment(Payment* payment) {
    payment->pay();  // Polymorphic call
}

int main() {
    Payment* cardPay = new CardPayment();
    Payment* upiPay = new UPIPayment();
    Payment* paypalPay = new PayPalPayment();
    
    processPayment(cardPay);    // Card payment
    processPayment(upiPay);     // UPI payment
    processPayment(paypalPay);  // PayPal payment
    
    delete cardPay;
    delete upiPay;
    delete paypalPay;
    
    return 0;
}
```

---

## 🎯 How to Achieve OCP

### ✅ Use:

- **Interfaces / Abstract Classes** - Define contracts
- **Polymorphism** - Runtime behavior selection
- **Inheritance** - Extend functionality
- **Strategy Pattern** - Encapsulate algorithms

### ❌ Avoid:

- **Large if-else chains** - Hard to maintain
- **Large switch statements** - Rigid and brittle
- **Type checking** - Defeats polymorphism
- **Modifying existing classes** - Risk breaking existing code

---

## 💡 Real Interview Insight

**If interviewer asks:**

> "How would you add a new discount system without changing existing code?"

### With OCP ✅

Create a new discount class that extends the base:

```cpp
class CryptoPayment : public Payment {
public:
    void pay() override {
        cout << "Processing cryptocurrency payment\n";
    }
};
```

**No existing code modified!** Just add the new class.

### Without OCP ❌

Modify the original `Payment` class with another `if-else` → risky!

---

## 🔍 Benefits of OCP

| Benefit | Description |
|---------|-------------|
| **Maintainability** | Existing code remains untouched |
| **Testability** | Test new features independently |
| **Flexibility** | Easy to add new behaviors |
| **Reduced Risk** | No chance of breaking existing functionality |

---

## 🚀 Key Takeaway

**OCP ensures:**
- ✅ **Open for extension** - Add new functionality easily
- ✅ **Closed for modification** - Don't touch working code

**Think:** "Can I add new features by writing new code, not modifying old code?"
