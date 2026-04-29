# SOLID Principles

---

## Interface Segregation Principle (ISP)

### 📌 Definition

> **"Clients should not be forced to depend on interfaces they do not use."**

### 🧠 Intuition

**Make fine-grained interfaces that are client-specific.**

Don't create "fat interfaces" that force classes to implement methods they don't need.

### 🌍 Real-life Example

A single `Shape` interface forces both `calculateArea()` and `calculateVolume()`:
- A **Square** is 2D, so it should **not** implement `calculateVolume()`
- A **Cuboid** is 3D, so it needs both methods

**Solution:** Split into separate interfaces based on dimensions.

---

## 📐 Shape Example

### ❌ Bad Design (Violation of ISP)

A single interface forces **all shapes** to implement both 2D and 3D methods:

```cpp
#include <iostream>
using namespace std;

class Shape {
public:
    virtual double calculateArea() = 0;
    virtual double calculateVolume() = 0;
};

class Square : public Shape {
public:
    double calculateArea() override {
        return 4 * 4;
    }

    double calculateVolume() override {
        // ❌ Not applicable, but FORCED to implement
        return 0;  // Dummy implementation
    }
};

class Cuboid : public Shape {
public:
    double calculateArea() override {
        return 2 * (2*3 + 3*4 + 2*4);
    }

    double calculateVolume() override {
        return 2 * 3 * 4;
    }
};
```

#### 🚨 Problem

- `Square` depends on `calculateVolume()` → **unnecessary dependency**
- Forces dummy implementations
- Violates ISP
- Confusing for clients: "Can a square have volume?"

---

### ✅ Good Design (Applying ISP)

👉 **Split interfaces based on responsibility**

#### Separate Interfaces

```cpp
#include <iostream>
using namespace std;

// Interface for 2D shapes
class TwoDimensionalShape {
public:
    virtual double calculateArea() = 0;
    virtual ~TwoDimensionalShape() {}
};

// Interface for 3D shapes
class ThreeDimensionalShape {
public:
    virtual double calculateVolume() = 0;
    virtual ~ThreeDimensionalShape() {}
};
```

#### ✅ Square (Only 2D behavior)

```cpp
class Square : public TwoDimensionalShape {
private:
    double side;

public:
    Square(double s) : side(s) {}

    double calculateArea() override {
        return side * side;
    }
};
```

#### ✅ Circle (Only 2D behavior)

```cpp
class Circle : public TwoDimensionalShape {
private:
    double radius;

public:
    Circle(double r) : radius(r) {}

    double calculateArea() override {
        return 3.14159 * radius * radius;
    }
};
```

#### ✅ Cuboid (Both 2D + 3D behavior)

```cpp
class Cuboid : public TwoDimensionalShape, public ThreeDimensionalShape {
private:
    double length, width, height;

public:
    Cuboid(double l, double w, double h)
        : length(l), width(w), height(h) {}

    double calculateArea() override {
        return 2 * (length*width + width*height + height*length);
    }

    double calculateVolume() override {
        return length * width * height;
    }
};
```

#### 🧠 Usage

```cpp
int main() {
    Square sq(4);
    cout << "Square Area: " << sq.calculateArea() << endl;

    Circle circle(5);
    cout << "Circle Area: " << circle.calculateArea() << endl;

    Cuboid cb(2, 3, 4);
    cout << "Cuboid Area: " << cb.calculateArea() << endl;
    cout << "Cuboid Volume: " << cb.calculateVolume() << endl;

    return 0;
}
```

---

### 🔍 Why This Works

| Class    | Implements              | Why |
|----------|-------------------------|-----|
| `Square` | `TwoDimensionalShape`   | Only needs area calculation |
| `Circle` | `TwoDimensionalShape`   | Only needs area calculation |
| `Cuboid` | Both interfaces         | Needs both area and volume |

✅ **No unnecessary dependencies**  
✅ **Each class implements only what it needs**  
✅ **Clear separation of concerns**

---

## 💡 Real Interview Insight

**If interviewer asks:**

> "Why not just leave dummy implementations in Square?"

**Answer:**
> "Dummy implementations are code smells. They:
> 1. Confuse other developers
> 2. Create maintenance burden
> 3. Violate the contract — if a method exists, it should be meaningful
> 4. Make testing harder — what do you test for dummy methods?"

---

## 🧠 Design Thinking Pattern

**Ask yourself:**

> "Does every implementer of this interface need ALL of its methods?"

- **If NO** ❌ → Split the interface
- **If YES** ✅ → Keep it as is

---

## 🎯 Benefits of ISP

| Benefit | Description |
|---------|-------------|
| **Decoupling** | Classes depend only on what they use |
| **Flexibility** | Easy to add new types without affecting existing code |
| **Clarity** | Interfaces clearly communicate their purpose |
| **Testability** | Smaller interfaces are easier to mock and test |

---

## 🚀 Real-World Examples

### Example 1: Printer Interface

#### ❌ Bad Design

```cpp
class Printer {
    virtual void print() = 0;
    virtual void scan() = 0;
    virtual void fax() = 0;
};
```

Problem: A simple printer doesn't scan or fax!

#### ✅ Good Design

```cpp
class Printable {
    virtual void print() = 0;
};

class Scannable {
    virtual void scan() = 0;
};

class Faxable {
    virtual void fax() = 0;
};

// Simple printer
class SimplePrinter : public Printable { /* ... */ };

// All-in-one printer
class AllInOnePrinter : public Printable, public Scannable, public Faxable { /* ... */ };
```

---

### Example 2: Worker Interface

#### ❌ Bad Design

```cpp
class Worker {
    virtual void work() = 0;
    virtual void eat() = 0;
};
```

Problem: Robot workers don't eat!

#### ✅ Good Design

```cpp
class Workable {
    virtual void work() = 0;
};

class Eatable {
    virtual void eat() = 0;
};

class HumanWorker : public Workable, public Eatable { /* ... */ };
class RobotWorker : public Workable { /* ... */ };
```

---

## 🔥 Advanced Insight

### ISP vs SRP

| Principle | Focus |
|-----------|-------|
| **SRP** | Single responsibility per **class** |
| **ISP** | Minimal dependencies per **interface** |

Both promote **focused, cohesive designs** but at different levels.

---

## ⚡ One-Line Summary

> **"Don't make classes implement methods they don't need."**

---

## 🚀 Key Takeaway

**ISP ensures:**
- ✅ **Minimal interfaces** - Only necessary methods
- ✅ **No fat interfaces** - Split large interfaces
- ✅ **Client-specific** - Tailored to actual needs

**Think:** "Every interface method should be relevant to every implementer."
