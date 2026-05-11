# SOLID Principles Summary

## Overview Table

| Principle | Abbreviation | Definition | Key Concept | Real-Life Example | Benefits |
|-----------|--------------|------------|-------------|-------------------|----------|
| **Single Responsibility Principle** | **SRP** | A class should have only ONE reason to change | Each class should have one job and one job only | Restaurant: Chef cooks, Waiter serves. Don't mix responsibilities. | • Easier to maintain<br>• Better code organization<br>• Reduced coupling<br>• Easier testing |
| **Open/Closed Principle** | **OCP** | Open for extension, closed for modification | Add new behavior WITHOUT modifying existing code | Payment System: Add new payment methods (UPI, Card, PayPal) without changing existing payment logic | • Flexible code<br>• Minimal risk when adding features<br>• Existing code remains stable<br>• Promotes inheritance/composition |
| **Liskov Substitution Principle** | **LSP** | Derived class should be replaceable for base class | Child class should NOT break parent behavior. Objects of a superclass should be replaceable with objects of subclass | Vehicle: Replace Vehicle with Car or Bicycle without breaking behavior | • Reliable inheritance<br>• Predictable behavior<br>• Better polymorphism<br>• Prevents unexpected bugs |
| **Interface Segregation Principle** | **ISP** | Clients should not be forced to depend on interfaces they do not use | Make fine-grained, client-specific interfaces instead of "fat interfaces" | Shape: 2D shapes (Square) should not implement 3D methods (calculateVolume). Split into 2D and 3D interfaces | • Cleaner interfaces<br>• No unnecessary dependencies<br>• Better code clarity<br>• Easier to implement |
| **Dependency Inversion Principle** | **DIP** | High-level modules should not depend on low-level modules. Both should depend on abstractions | Depend on abstractions/interfaces, not concrete implementations | Switch: Switch should depend on Device interface, not directly on Light, Fan, or AC | • Loose coupling<br>• Easy to swap implementations<br>• Better testability<br>• More flexible architecture |

---

## Quick Reference

### 🔴 SRP - Single Responsibility Principle
```
One class = One responsibility = One reason to change
```
**Violation:** A class that handles both cooking AND serving  
**Solution:** Separate Chef class and Waiter class

---

### 🟠 OCP - Open/Closed Principle
```
Open for extension, Closed for modification
```
**Violation:** Modifying existing payment class to add new payment method  
**Solution:** Create interface and extend with new payment implementations

---

### 🟡 LSP - Liskov Substitution Principle
```
Subtypes must be substitutable for their base types
```
**Violation:** Bicycle extends Vehicle but throws error on startEngine()  
**Solution:** Create proper abstractions where methods make sense for all derived classes

---

### 🟢 ISP - Interface Segregation Principle
```
Many specific interfaces > One general interface
```
**Violation:** Square forced to implement calculateVolume() from Shape interface  
**Solution:** Split into Shape2D and Shape3D interfaces

---

### 🔵 DIP - Dependency Inversion Principle
```
Depend on abstractions, not concretions
```
**Violation:** Switch class directly depends on Light class  
**Solution:** Switch depends on Device interface; Light implements Device interface

---

## Memory Aid: SOLID

| Letter | Principle | Remember As |
|--------|-----------|-------------|
| **S** | Single Responsibility | **S**ingle job |
| **O** | Open/Closed | **O**pen for extension |
| **L** | Liskov Substitution | **L**iskov = substitutable |
| **I** | Interface Segregation | **I**nterface = split it |
| **D** | Dependency Inversion | **D**epend on abstractions |

---

## Application Order (Recommended)

1. **Start with SRP** - Get your responsibilities right
2. **Apply OCP** - Make it extensible
3. **Check LSP** - Ensure inheritance is correct
4. **Apply ISP** - Split fat interfaces
5. **Apply DIP** - Invert dependencies to abstractions

---

## Common Violations to Watch For

| Principle | Red Flags |
|-----------|-----------|
| **SRP** | Class has multiple unrelated methods, uses "and" in class name (e.g., UserAndOrder) |
| **OCP** | Frequent if-else chains for types, modifying classes to add features |
| **LSP** | Derived class throws UnsupportedOperationException, empty overrides, type checking |
| **ISP** | Empty method implementations, NotImplementedException, large interfaces |
| **DIP** | Direct instantiation of concrete classes, new keyword everywhere, hard to test |

---

## Benefits of Following SOLID

✅ **Maintainability** - Easier to understand and modify  
✅ **Flexibility** - Easy to extend and adapt  
✅ **Testability** - Components can be tested in isolation  
✅ **Reusability** - Components can be reused across projects  
✅ **Scalability** - Architecture can grow without major refactoring  
✅ **Reduced Bugs** - Clear responsibilities reduce unexpected behavior  

---

## When to Apply SOLID?

- ✅ Building new systems
- ✅ Refactoring legacy code
- ✅ Adding new features
- ✅ When code becomes hard to maintain
- ⚠️ Not every small script needs SOLID (don't over-engineer)
