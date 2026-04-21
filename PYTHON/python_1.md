1) what is the difference between list and tuple?

Core Difference
List → mutable (can change)
Tuple → immutable (cannot change)
🔹 1. Syntax
# List
my_list = [1, 2, 3]

# Tuple
my_tuple = (1, 2, 3)
🔹 2. Mutability (Main Difference)
List (Mutable)
my_list = [1, 2, 3]
my_list[0] = 10
print(my_list)

👉 Output:

[10, 2, 3]
Tuple (Immutable)
my_tuple = (1, 2, 3)
my_tuple[0] = 10   # ❌ Error

👉 Error:

TypeError: 'tuple' object does not support item assignment
🔹 3. Performance
Tuple → faster (fixed size, optimized)
List → slightly slower (dynamic)
🔹 4. Methods Available
List methods (many)
my_list = [1, 2, 3]
my_list.append(4)
my_list.remove(2)
print(my_list)
Tuple methods (very few)
my_tuple = (1, 2, 3, 1)
print(my_tuple.count(1))
print(my_tuple.index(2))
🔹 5. Use Cases
Use List when:
Data changes frequently
You need insert/delete/update
Use Tuple when:
Data is fixed (constants, config)
You want better performance
You need safe (read-only) data
🔹 6. Example in Real Automation
List (dynamic data)
links = ["url1", "url2", "url3"]
links.append("url4")
Tuple (fixed config)
credentials = ("admin", "password123")
🔹 7. Tuple Packing & Unpacking
# Packing
data = (1, 2, 3)

# Unpacking
a, b, c = data
print(a, b, c)
🔹 8. Nested Example
my_list = [1, (2, 3), 4]   # tuple inside list
🔥 Interview Comparison Table
Feature	List	Tuple
Mutability	Mutable	Immutable
Syntax	[]	()
Performance	Slower	Faster
Methods	Many	Few
Use Case	Dynamic data	Fixed data
🔥 Interview Answer (Perfect)

A list is mutable, meaning its elements can be modified, added, or removed, while a tuple is immutable and cannot be changed after creation. Lists are used for dynamic data, whereas tuples are used for fixed data and offer better performance.


2) What is self in Python?

In Python, self refers to the current instance (object) of the class.
It is used to access instance variables and methods inside the class.

🔹 Why do we need self?

Without self, Python cannot distinguish:

instance variables vs local variables
which object’s data you’re working with
🔹 Example
class Person:
    def __init__(self, name, age):
        self.name = name   # instance variable
        self.age = age

    def greet(self):
        print(f"Hello, my name is {self.name} and I am {self.age}")
Usage
p1 = Person("Alice", 25)
p1.greet()

👉 Internally, Python does:

Person.greet(p1)
🔹 Key Points (Important)

✔ self is not a keyword, just a convention
✔ Must be the first parameter in instance methods
✔ Automatically passed by Python
✔ Used to access:

instance variables → self.name
methods → self.method()
🔹 What happens without self?
class Test:
    def show():
        print("Hello")

👉 Calling:

obj = Test()
obj.show()

❌ Error:

TypeError: show() takes 0 positional arguments but 1 was given
🔹 self vs local variable
class Demo:
    def __init__(self, x):
        self.x = x   # instance
        x = 10       # local (ignored outside)
🔹 Interview-Level Answer (Perfect)

👉 “self represents the current instance of the class in Python. It is used to access instance variables and methods and is automatically passed when an object calls a method.”

🔥 Pro Tip (Very Important)

If interviewer pushes deeper:

👉 “Why explicitly write self in Python but not in Java/C++?”

Answer:

Python makes it explicit for readability and flexibility
In Java/C++, this is implicit
🔹 Related Concepts (they may ask next)
self vs cls
@classmethod
@staticmethod


3) What are *args and **kwargs?
✅ *args
Allows a function to accept any number of positional arguments
Stored as a tuple
✅ **kwargs
Allows a function to accept any number of keyword arguments
Stored as a dictionary
🔹 Example: *args
def add(*args):
    return sum(args)

print(add(1, 2, 3))      # 6
print(add(10, 20))       # 30

👉 Internally:

args = (1, 2, 3)
🔹 Example: **kwargs
def print_details(**kwargs):
    for key, value in kwargs.items():
        print(key, value)

print_details(name="Alice", age=25)

👉 Internally:

kwargs = {"name": "Alice", "age": 25}
🔹 Using Both Together
def demo(*args, **kwargs):
    print("Args:", args)
    print("Kwargs:", kwargs)

demo(1, 2, 3, name="John", age=30)
🔹 Order Rule (VERY IMPORTANT)
def func(a, b, *args, **kwargs):
    pass

👉 Correct order:

Normal arguments
*args
**kwargs
🔹 Real-World Example (Very Useful for You)
Selenium / Pytest style config
def launch_browser(browser="chrome", **options):
    print(browser)
    print(options)

launch_browser(headless=True, window_size="1920x1080")
🔹 Argument Unpacking (Advanced 🔥)
def add(a, b, c):
    return a + b + c

nums = [1, 2, 3]
print(add(*nums))   # unpack list
def greet(name, age):
    print(name, age)

data = {"name": "Alice", "age": 25}
greet(**data)   # unpack dict
🔹 Why do we use them?
Flexible APIs
Unknown number of inputs
Passing dynamic configs
Wrapper/decorator functions
🔥 Interview Answer (Perfect)

👉 “*args allows passing a variable number of positional arguments as a tuple, and **kwargs allows passing a variable number of keyword arguments as a dictionary.”

🔥 Common Follow-up Questions
❓ Can we use different names instead of args / kwargs?

✔ Yes (they are just conventions)

def test(*numbers, **data):
    pass
❓ Difference between * and **?
Symbol	Meaning
*	tuple (positional)
**	dict (keyword)