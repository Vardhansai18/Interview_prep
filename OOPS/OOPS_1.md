# OOPS (Object-Oriented Programming)

## 📑 Table of Contents

1. [What is OOPS?](#what-is-oops)
2. [Class](#class)
3. [Object](#object)
4. [Benefits of OOPS](#benefits-of-oops)
5. [Coding Example for Classes and Objects](#coding-example-for-classes-and-objects)
6. [What is a Constructor?](#what-is-a-constructor)
7. [What is a Destructor?](#what-is-a-destructor)

---

## What is OOPS?

**Definition:**  
A programming paradigm that structures code using objects and classes, focusing on modeling real-world entities and their interactions.

---

## Class

**Definition:**  
A blueprint/template used to create objects. It defines attributes (data) and methods (functions).

**👉 Example:**

```cpp
class Vehicle {
public:
    string color;
    int speed;

    void drive() {
        cout << "Driving..." << endl;
    }
};
```

---

## Object

**Definition:**  
An instance of a class. It represents a real-world entity and holds actual values.

**👉 Example:**

```cpp
Vehicle v1;
v1.color = "Red";
v1.speed = 100;
v1.drive();
```

---

## Benefits of OOPS

### 1. Code Reusability (Inheritance)
Using inheritance, you reuse existing code instead of rewriting.

### 2. Data Security (Encapsulation)
Data can be hidden using private and accessed via methods.

### 3. Flexibility (Polymorphism)
Same function behaves differently depending on the object.

### 4. Data Hiding (Abstraction)
Abstraction reduces complexity by exposing only relevant interfaces and hiding internal implementation details.

### 5. Modularity
Code is divided into small, manageable classes.

### 6. Easy Maintenance
Changes in one class don't affect the entire system.

### 7. Real-world Mapping
Models real-world entities (Car, User, BankAccount) → easier to design.

---

## Coding Example for Classes and Objects

```cpp
#include <iostream>
using namespace std;

class Vechile{
public:
    int number;
    string color;
    int price;

    // Constructor
    Vechile(string color , int number , int price )
    {
        this->number = number;
        this->color = color;
        this->price = price;
        cout << "Constructor called" << endl;
    }

    // Destructor
    ~Vechile()
    {
        cout << "Destructor called for Vehicle with number: " << number << endl;
    }

    void display()
    {
        cout << "Number: " << number << endl;
        cout << "Color: " << color << endl;
        cout << "Price: " << price << endl;
    }
};

int main() {
    Vechile v1("Red", 12, 25000);
    v1.display();

    v1.number = 1999;
    v1.color = "Blue";
    v1.price = 25;

    v1.display();

    return 0;
}
```

**Output:**

```
Constructor called
Number: 12
Color: Red
Price: 25000
Number: 1999
Color: Blue
Price: 25
Destructor called for Vehicle with number: 1999
```

---

## What is a Constructor?

**🔹 Constructor (C++)**

**Definition:**  
A constructor is a special member function of a class that is automatically called when an object is created. Its main purpose is to initialize the object's data members.

### 🔧 Key Properties

- Same name as the class
- No return type (not even void)
- Called automatically when object is created
- Can be overloaded (multiple constructors)

### ✅ Simple Example

```cpp
#include <iostream>
using namespace std;

class Vehicle {
public:
    string color;
    int speed;

    // Constructor
    Vehicle(string c, int s) {
        color = c;
        speed = s;
    }

    void display() {
        cout << color << " " << speed << endl;
    }
};

int main() {
    Vehicle v1("Red", 100);   // constructor called automatically
    v1.display();
}
```

### ⚙️ Types of Constructors

#### 1. Default Constructor

No parameters

```cpp
Vehicle() {
    color = "Black";
    speed = 0;
}
```

#### 2. Parameterized Constructor

Takes inputs to initialize values

```cpp
Vehicle(string c, int s) {
    color = c;
    speed = s;
}
```

#### 3. Copy Constructor

Creates object from another object

```cpp
Vehicle(const Vehicle &v) {
    color = v.color;
    speed = v.speed;
}
```

---

## What is a Destructor?

**Definition:**  
A destructor is a special member function that is automatically called when an object goes out of scope or is destroyed.

**Syntax:**

```cpp
~ClassName() {
    // cleanup code
}
```

### ⚙️ When is it Called?

In your case:

- `v1` is a stack object
- Destructor is called automatically at the end of `main()`

### 🧠 Output Flow

```
Constructor called
Number: 12
Color: Red
Price: 25000

Number: 1999
Color: Blue
Price: 25

Destructor called for Vehicle with number: 1999
```
