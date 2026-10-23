---
name: python-migration
description: Domain knowledge for migrating Python 2.x applications to Python 3.x. Covers syntax changes, Unicode handling, standard library reorganization, built-in function changes, and migration best practices. Also applies to extensionless scripts with python shebang lines.
applyTo: ["**/*.py", "**/requirements.txt", "**/setup.py", "**/setup.cfg", "**/tox.ini", "**/.python-version", "**/bin/*"]
---

# Python Migration Guide: Python 2.x → Python 3.x

This skill provides comprehensive guidance for migrating applications from Python 2.x to Python 3.x, covering breaking changes, syntax updates, and best practices.

## Overview of Major Changes

Python 3.x introduced significant breaking changes from Python 2.x:

1. **Print Function**: `print` statement → `print()` function
2. **Integer Division**: `/` always returns float, `//` for integer division
3. **Unicode by Default**: All strings are Unicode by default
4. **Text vs. Bytes**: Clear distinction between text (str) and binary (bytes)
5. **Iterators Everywhere**: `range()`, `map()`, `filter()`, `zip()`, `dict.keys()`, etc. return iterators
6. **Exception Syntax**: New exception handling syntax required
7. **Standard Library Reorganization**: Many modules renamed or restructured
8. **Removed Features**: Many deprecated Python 2 features removed

## Critical Breaking Changes

### 1. Print Statement → Print Function

**Python 2**:
```python
# OLD - Print statement
print "Hello, World!"
print "Value:", x
print "Result:",
print x, y
print >>sys.stderr, "Error message"

# Multiple items
print x, y, z
```

**Python 3**:
```python
# NEW - Print function
print("Hello, World!")
print("Value:", x)
print("Result:", end=' ')
print(x, y)
print("Error message", file=sys.stderr)

# Multiple items (same)
print(x, y, z)

# Custom separator and end
print(x, y, z, sep=', ', end='\n')
```

### 2. Integer Division

**Python 2**:
```python
# OLD - Integer division by default
result = 5 / 2      # Returns 2 (integer)
result = 5.0 / 2    # Returns 2.5 (float)
result = 5 // 2     # Returns 2 (floor division)

# Future import for Python 3 behavior
from __future__ import division
result = 5 / 2      # Returns 2.5 (float)
```

**Python 3**:
```python
# NEW - True division by default
result = 5 / 2      # Returns 2.5 (float)
result = 5 // 2     # Returns 2 (floor division)

# For backwards compatibility in Python 2:
# Use // for integer division explicitly
```

### 3. Unicode and Strings

**Python 2**:
```python
# OLD - str (bytes) and unicode types
text = "Hello"           # str (bytes in Python 2)
unicode_text = u"Hello"  # unicode
byte_string = b"Hello"   # str (same as "Hello")

# String type checking
if isinstance(text, basestring):  # Both str and unicode
    pass
if isinstance(text, unicode):
    pass
```

**Python 3**:
```python
# NEW - str (Unicode) and bytes types
text = "Hello"           # str (Unicode by default)
byte_string = b"Hello"   # bytes

# String type checking
if isinstance(text, str):      # Unicode string
    pass
if isinstance(text, bytes):    # Byte string
    pass

# No basestring - use str instead
# No unicode type - str is Unicode
```

### 4. String Encoding and Decoding

**Python 2**:
```python
# OLD - Implicit conversions
text = "Hello"
byte_data = text.encode('utf-8')  # str → str (confusing)

unicode_text = u"Hello"
byte_data = unicode_text.encode('utf-8')  # unicode → str

text = byte_data.decode('utf-8')  # str → unicode
```

**Python 3**:
```python
# NEW - Explicit conversions
text = "Hello"  # str (Unicode)
byte_data = text.encode('utf-8')  # str → bytes

# Decoding bytes to str
text = byte_data.decode('utf-8')  # bytes → str

# Can't mix bytes and str
result = "Hello" + b"World"  # TypeError!

# Must decode or encode explicitly
result = "Hello" + b"World".decode('utf-8')  # OK
result = "Hello".encode('utf-8') + b"World"  # OK (bytes result)
```

### 5. Iterator Changes

**Python 2**:
```python
# OLD - Many functions return lists
items = range(10)              # list
keys = dict.keys()             # list
values = dict.values()         # list
items = dict.items()           # list
result = map(func, items)      # list
result = filter(func, items)   # list
result = zip(list1, list2)     # list

# Iterators available with iter* prefix
keys = dict.iterkeys()         # iterator
values = dict.itervalues()     # iterator
items = dict.iteritems()       # iterator
```

**Python 3**:
```python
# NEW - Most functions return iterators/views
items = range(10)              # range object (iterator)
keys = dict.keys()             # dict_keys view
values = dict.values()         # dict_values view
items = dict.items()           # dict_items view
result = map(func, items)      # iterator
result = filter(func, items)   # iterator
result = zip(list1, list2)     # iterator

# Convert to list explicitly if needed
items = list(range(10))        # list
keys = list(dict.keys())       # list

# No iter* methods
# dict.iterkeys() - REMOVED, use dict.keys()
# dict.itervalues() - REMOVED, use dict.values()
# dict.iteritems() - REMOVED, use dict.items()
```

### 6. Exception Handling Syntax

**Python 2**:
```python
# OLD - Multiple syntax styles
try:
    risky_operation()
except ValueError, e:          # Comma syntax (deprecated)
    print "Error:", e

try:
    risky_operation()
except ValueError as e:        # 'as' syntax (preferred, also works in Py3)
    print "Error:", e

# Raising exceptions
raise ValueError, "Error message"
raise ValueError("Error message")  # Also works
```

**Python 3**:
```python
# NEW - Only 'as' syntax
try:
    risky_operation()
except ValueError as e:        # Only this syntax works
    print("Error:", e)

# Raising exceptions
raise ValueError("Error message")  # Only this syntax

# Cannot use comma syntax
# raise ValueError, "Error message"  # SyntaxError!
```

### 7. Dictionary Methods

**Python 2**:
```python
# OLD - Multiple ways to iterate
d = {'a': 1, 'b': 2}

# Returns lists
keys = d.keys()        # ['a', 'b']
values = d.values()    # [1, 2]
items = d.items()      # [('a', 1), ('b', 2)]

# Returns iterators
for key in d.iterkeys():
    pass
for value in d.itervalues():
    pass
for key, value in d.iteritems():
    pass

# has_key method
if d.has_key('a'):
    pass
```

**Python 3**:
```python
# NEW - Views and iterators
d = {'a': 1, 'b': 2}

# Returns dictionary views (not lists)
keys = d.keys()        # dict_keys(['a', 'b'])
values = d.values()    # dict_values([1, 2])
items = d.items()      # dict_items([('a', 1), ('b', 2)])

# Views are iterable
for key in d.keys():
    pass
for value in d.values():
    pass
for key, value in d.items():
    pass

# No iter* methods - just use keys(), values(), items()
# d.iterkeys() - REMOVED
# d.itervalues() - REMOVED
# d.iteritems() - REMOVED

# has_key removed - use 'in' operator
if 'a' in d:
    pass
```

### 8. Input Function

**Python 2**:
```python
# OLD - Two input functions
name = raw_input("Enter name: ")  # Returns string
number = input("Enter number: ")  # Evaluates input as Python expression (DANGEROUS!)

# input() evaluates the input
x = input("Enter expression: ")  # User types: 2 + 3, x becomes 5
```

**Python 3**:
```python
# NEW - Only input() function
name = input("Enter name: ")     # Returns string (like raw_input)

# No raw_input
# raw_input() - REMOVED

# To evaluate input, use eval() explicitly (be careful!)
number = int(input("Enter number: "))
result = eval(input("Enter expression: "))  # Use with caution!
```

### 9. Comparison and Ordering

**Python 2**:
```python
# OLD - Can compare anything
result = "string" < 123          # Works, but nonsensical
result = [1, 2] < "test"         # Works

# sorted() and comparison functions
sorted_list = sorted(items, cmp=custom_compare)

# Custom comparison
def custom_compare(x, y):
    return x - y
```

**Python 3**:
```python
# NEW - Cannot compare incompatible types
result = "string" < 123          # TypeError!
result = [1, 2] < "test"         # TypeError!

# No cmp parameter in sorted()
# sorted_list = sorted(items, cmp=custom_compare)  # TypeError!

# Use key parameter instead
sorted_list = sorted(items, key=lambda x: x.some_attribute)

# For complex sorting, use functools.cmp_to_key
from functools import cmp_to_key

def custom_compare(x, y):
    return (x > y) - (x < y)

sorted_list = sorted(items, key=cmp_to_key(custom_compare))
```

### 10. Standard Library Reorganization

**Python 2**:
```python
# OLD - Module names and locations
import ConfigParser
import Queue
import SocketServer
import repr
import HTMLParser
import urlparse
import urllib2
import httplib
import cPickle as pickle  # C implementation

from itertools import izip, imap, ifilter
```

**Python 3**:
```python
# NEW - Renamed and reorganized modules
import configparser      # ConfigParser → configparser
import queue            # Queue → queue
import socketserver     # SocketServer → socketserver
import reprlib          # repr → reprlib
import html.parser      # HTMLParser → html.parser
import urllib.parse     # urlparse → urllib.parse
import urllib.request   # urllib2 → urllib.request
import http.client      # httplib → http.client
import pickle           # cPickle merged into pickle

# No need for separate iter* functions from itertools
# Use built-in zip, map, filter instead
# izip → zip
# imap → map
# ifilter → filter
```

## Standard Library Module Mapping

| Python 2 Module | Python 3 Module | Notes |
|-----------------|-----------------|-------|
| `__builtin__` | `builtins` | Built-in functions |
| `ConfigParser` | `configparser` | INI file parser |
| `copy_reg` | `copyreg` | Pickle support |
| `Queue` | `queue` | Thread-safe queue |
| `SocketServer` | `socketserver` | Network servers |
| `markupbase` | `_markupbase` | HTML/XML parser base |
| `repr` | `reprlib` | Alternate repr() implementation |
| `test.test_support` | `test.support` | Test utilities |
| `Tkinter` | `tkinter` | GUI toolkit |
| `tkFileDialog` | `tkinter.filedialog` | Tkinter file dialogs |
| `tkMessageBox` | `tkinter.messagebox` | Tkinter message boxes |
| `tkColorChooser` | `tkinter.colorchooser` | Tkinter color picker |
| `Dialog` | `tkinter.dialog` | Tkinter dialogs |
| `FileDialog` | `tkinter.filedialog` | File selection dialogs |
| `ScrolledText` | `tkinter.scrolledtext` | Scrolled text widget |
| `SimpleDialog` | `tkinter.simpledialog` | Simple dialogs |
| `Tix` | `tkinter.tix` | Tk extension widgets |
| `tkCommonDialog` | `tkinter.commondialog` | Common dialog infrastructure |
| `tkFont` | `tkinter.font` | Font utilities |
| `tkSimpleDialog` | `tkinter.simpledialog` | Simple input dialogs |
| `_winreg` | `winreg` | Windows registry access |
| `htmllib` | `html.parser` | HTML parser (deprecated) |
| `HTMLParser` | `html.parser` | HTML parser |
| `htmlentitydefs` | `html.entities` | HTML entity definitions |
| `Cookie` | `http.cookies` | HTTP cookies |
| `cookielib` | `http.cookiejar` | Cookie handling |
| `httplib` | `http.client` | HTTP client |
| `BaseHTTPServer` | `http.server` | HTTP server base |
| `SimpleHTTPServer` | `http.server` | Simple HTTP server |
| `CGIHTTPServer` | `http.server` | CGI HTTP server |
| `urllib` | `urllib.parse`, `urllib.request`, `urllib.error` | URL handling |
| `urllib2` | `urllib.request`, `urllib.error` | URL opening |
| `urlparse` | `urllib.parse` | URL parsing |
| `robotparser` | `urllib.robotparser` | robots.txt parser |
| `anydbm` | `dbm` | Generic DBM interface |
| `whichdb` | `dbm` | DBM type identifier |
| `dbm` | `dbm.ndbm` | Unix DBM interface |
| `dumbdbm` | `dbm.dumb` | Portable DBM implementation |
| `gdbm` | `dbm.gnu` | GNU DBM interface |
| `xmlrpclib` | `xmlrpc.client` | XML-RPC client |
| `DocXMLRPCServer` | `xmlrpc.server` | XML-RPC server with docs |
| `SimpleXMLRPCServer` | `xmlrpc.server` | Simple XML-RPC server |

## Removed Features in Python 3

### Syntax and Keywords
- `print` statement → `print()` function
- Backticks for `repr()`: `` `x` `` → `repr(x)`
- `<>` operator → use `!=`
- `exec` statement → `exec()` function
- `long` type → `int` (unified)
- `unicode` type → `str` (unified)

### Built-in Functions
- `apply()` → use `func(*args, **kwargs)`
- `buffer()` → use `memoryview()`
- `coerce()` → removed
- `execfile()` → use `exec(open(file).read())`
- `file()` → use `open()`
- `input()` (evaluating) → use `eval(input())`
- `raw_input()` → renamed to `input()`
- `reduce()` → moved to `functools.reduce()`
- `reload()` → moved to `importlib.reload()`
- `xrange()` → renamed to `range()`
- `StandardError` → removed
- `basestring` → use `str`
- `.has_key()` → use `in` operator

### Module-Level Changes
- `cPickle` → merged into `pickle`
- `cStringIO` → merged into `io`
- `itertools.izip()` → use `zip()`
- `itertools.imap()` → use `map()`
- `itertools.ifilter()` → use `filter()`

## Migration Patterns

### Pattern 1: Print Statement to Function

**Before:**
```python
def log_message(msg, level="INFO"):
    print "[%s]" % level, msg
    print >>sys.stderr, "Error occurred"
```

**After:**
```python
def log_message(msg, level="INFO"):
    print("[%s]" % level, msg)
    print("Error occurred", file=sys.stderr)
```

### Pattern 2: Unicode Handling

**Before:**
```python
def process_text(data):
    # Python 2 - handle both str and unicode
    if isinstance(data, unicode):
        data = data.encode('utf-8')
    
    # Process as bytes
    result = data.upper()
    
    # Return unicode
    return result.decode('utf-8')
```

**After:**
```python
def process_text(data):
    # Python 3 - str is already Unicode
    if isinstance(data, bytes):
        data = data.decode('utf-8')
    
    # Process as string
    result = data.upper()
    
    # Return str (Unicode)
    return result
```

### Pattern 3: Dictionary Iteration

**Before:**
```python
def process_dict(d):
    # Python 2 - use iteritems() for efficiency
    for key, value in d.iteritems():
        process(key, value)
    
    # Get all keys as list
    all_keys = d.keys()
    
    # Check key existence
    if d.has_key('key'):
        return d['key']
```

**After:**
```python
def process_dict(d):
    # Python 3 - items() returns view (efficient)
    for key, value in d.items():
        process(key, value)
    
    # Get all keys as list
    all_keys = list(d.keys())
    
    # Check key existence
    if 'key' in d:
        return d['key']
```

### Pattern 4: Exception Handling

**Before:**
```python
def handle_errors():
    try:
        risky_operation()
    except (ValueError, TypeError), e:
        print "Error:", e
        raise Exception, "Failed: %s" % e
```

**After:**
```python
def handle_errors():
    try:
        risky_operation()
    except (ValueError, TypeError) as e:
        print("Error:", e)
        raise Exception("Failed: %s" % e)
```

### Pattern 5: Integer Division

**Before:**
```python
def calculate_average(total, count):
    # Python 2 - integer division
    return total / count  # Returns int if both are int
    
def get_half(value):
    # Force float division
    return float(value) / 2
```

**After:**
```python
def calculate_average(total, count):
    # Python 3 - true division
    return total / count  # Always returns float
    
def get_half(value):
    # No need to cast
    return value / 2
    
def get_int_division(total, count):
    # Use // for integer division
    return total // count
```

### Pattern 6: Import Reorganization

**Before:**
```python
# Python 2 imports
import urllib2
import urlparse
import HTMLParser
import ConfigParser
import Queue
import cPickle as pickle

from itertools import izip, imap, ifilter

# URL operations
request = urllib2.Request(url)
response = urllib2.urlopen(request)
parsed = urlparse.urlparse(url)
```

**After:**
```python
# Python 3 imports
import urllib.request
import urllib.parse
from html.parser import HTMLParser
import configparser
import queue
import pickle

# No need for separate iter functions
# izip → zip, imap → map, ifilter → filter

# URL operations
request = urllib.request.Request(url)
response = urllib.request.urlopen(request)
parsed = urllib.parse.urlparse(url)
```

### Pattern 7: File I/O with Encoding

**Before:**
```python
# Python 2 - binary mode by default
with open('file.txt', 'r') as f:
    data = f.read()  # Returns str (bytes)

# Explicit unicode handling
import codecs
with codecs.open('file.txt', 'r', encoding='utf-8') as f:
    data = f.read()  # Returns unicode
```

**After:**
```python
# Python 3 - text mode with encoding by default
with open('file.txt', 'r', encoding='utf-8') as f:
    data = f.read()  # Returns str (Unicode)

# Binary mode when needed
with open('file.bin', 'rb') as f:
    data = f.read()  # Returns bytes

# codecs.open still works but open() is preferred
```

### Pattern 8: Range and Iterators

**Before:**
```python
# Python 2 - xrange for efficiency, range for lists
for i in xrange(1000000):  # Iterator
    process(i)

indices = range(10)  # List [0, 1, 2, ..., 9]

# Map returns list
doubled = map(lambda x: x * 2, [1, 2, 3])  # [2, 4, 6]
```

**After:**
```python
# Python 3 - range is always efficient
for i in range(1000000):  # Iterator
    process(i)

indices = list(range(10))  # Convert to list if needed

# Map returns iterator
doubled = list(map(lambda x: x * 2, [1, 2, 3]))  # [2, 4, 6]
# Or use list comprehension
doubled = [x * 2 for x in [1, 2, 3]]
```

## Migration Tools and Strategies

### Using 2to3 Tool

Python provides the `2to3` tool for automated conversion:

```bash
# Check what changes would be made
2to3 -d your_module.py

# Apply changes to file
2to3 -w your_module.py

# Process entire directory
2to3 -w myproject/

# Output to different location
2to3 -w --output-dir=py3-version py2-version/

# Apply specific fixers
2to3 -f print -f except your_module.py

# List all available fixers
2to3 -l
```

### Common 2to3 Fixers:
- `print` - Convert print statements to print() function
- `unicode` - Handle unicode literals
- `except` - Fix exception syntax
- `raise` - Fix raise statement syntax
- `has_key` - Convert dict.has_key() to 'in' operator
- `itertools` - Update itertools imports
- `import` - Fix renamed/reorganized imports
- `xrange` - Convert xrange() to range()
- `raw_input` - Convert raw_input() to input()

### Using six Library for Compatibility

For code that needs to work on both Python 2 and 3:

```python
import six

# String types
if six.PY2:
    text_type = unicode
    binary_type = str
else:
    text_type = str
    binary_type = bytes

# Check string types
if isinstance(data, six.string_types):
    pass

# Integer types
if isinstance(value, six.integer_types):
    pass

# Dictionary iteration
for key, value in six.iteritems(d):
    pass

# URL imports
from six.moves import urllib
from six.moves import configparser
from six.moves import queue

# Print function (works in both)
from __future__ import print_function
print("Hello", file=sys.stderr)
```

### Using __future__ Imports

Make Python 2 code more compatible with Python 3:

```python
# At the top of the file
from __future__ import print_function      # Enable print()
from __future__ import division            # True division
from __future__ import absolute_import     # Absolute imports by default
from __future__ import unicode_literals    # Strings are unicode

# Now code behaves more like Python 3
print("Hello", end=' ')  # Works in Python 2
result = 5 / 2           # Returns 2.5 in Python 2
text = "Hello"           # unicode in Python 2
```

## Testing Strategy

### 1. Unit Tests

Ensure you have comprehensive unit tests before migration:

```python
# Use unittest or pytest
import unittest

class TestMyModule(unittest.TestCase):
    def test_functionality(self):
        result = my_function(input_data)
        self.assertEqual(result, expected_output)
```

### 2. Test Both Versions

Use tox to test against multiple Python versions:

```ini
# tox.ini
[tox]
envlist = py27,py36,py37,py38,py39

[testenv]
deps = pytest
commands = pytest tests/
```

Run tests:
```bash
tox
```

### 3. Static Analysis

Use tools to detect Python 2/3 compatibility issues:

```bash
# pylint with Python 3 checking
pylint --py3k your_module.py

# modernize - like 2to3 but more conservative
python-modernize -w your_module.py

# futurize - adds __future__ imports
futurize -w your_module.py
```

### 4. Manual Testing

- Test with different input types (str, bytes, unicode)
- Test file I/O with various encodings
- Test exception handling
- Test numeric operations (division, comparisons)
- Test dictionary and iterator operations

## Common Pitfalls and Solutions

### Pitfall 1: Bytes vs. String Confusion

**Problem:**
```python
# Python 2 - works
data = b"Hello"
result = data + " World"

# Python 3 - TypeError!
data = b"Hello"
result = data + " World"  # Can't mix bytes and str
```

**Solution:**
```python
# Be explicit about types
data = b"Hello"
result = data + b" World"  # bytes + bytes = bytes
# OR
result = data.decode('utf-8') + " World"  # str + str = str
```

### Pitfall 2: Dictionary Ordering

**Problem:**
```python
# Python 2 - dict order is arbitrary
d = {'a': 1, 'b': 2, 'c': 3}
print(d.keys())  # Order may vary

# Python 3.7+ - dict preserves insertion order
d = {'a': 1, 'b': 2, 'c': 3}
print(d.keys())  # dict_keys(['a', 'b', 'c'])
```

**Solution:**
```python
# Use OrderedDict for explicit ordering in Python 2/3.6-
from collections import OrderedDict
d = OrderedDict([('a', 1), ('b', 2), ('c', 3)])

# Or don't rely on dict order in Python 2
# In Python 3.7+, regular dict is ordered
```

### Pitfall 3: map(), filter(), zip() Return Iterators

**Problem:**
```python
# Python 2 - returns list
numbers = [1, 2, 3, 4, 5]
doubled = map(lambda x: x * 2, numbers)
print(doubled)        # [2, 4, 6, 8, 10]
print(doubled[0])     # 2
print(len(doubled))   # 5

# Python 3 - returns iterator
numbers = [1, 2, 3, 4, 5]
doubled = map(lambda x: x * 2, numbers)
print(doubled)        # <map object at 0x...>
print(doubled[0])     # TypeError!
print(len(doubled))   # TypeError!
```

**Solution:**
```python
# Convert to list if needed
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)        # [2, 4, 6, 8, 10]

# Or use list comprehension (often better)
doubled = [x * 2 for x in numbers]
```

### Pitfall 4: Implicit Relative Imports

**Problem:**
```python
# Python 2 - implicit relative imports
# In package/submodule.py
import module  # Checks package first, then sys.path

# Python 3 - absolute imports by default
import module  # Checks sys.path first
```

**Solution:**
```python
# Use explicit relative imports
from . import module         # Import from current package
from .subpackage import mod  # Import from subpackage
from .. import module        # Import from parent package

# Or use absolute imports
from package import module
```

### Pitfall 5: Integer Overflow

**Problem:**
```python
# Python 2 - separate int and long types
x = 2147483647  # int
y = x + 1       # long (automatically promoted)
print(type(y))  # <type 'long'>

# Python 3 - only int type (unlimited precision)
x = 2147483647  # int
y = x + 1       # int
print(type(y))  # <class 'int'>
```

**Solution:**
```python
# No action needed - Python 3 handles this better
# Just be aware that there's no separate 'long' type

# Don't check for long type
# isinstance(x, long)  # NameError in Python 3!

# Use six for compatibility
import six
if isinstance(x, six.integer_types):
    pass
```

## Compatibility Decorators and Utilities

```python
# encoding_helpers.py - Helper functions for Python 2/3 compatibility
import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY3:
    string_types = (str,)
    integer_types = (int,)
    text_type = str
    binary_type = bytes
else:
    string_types = (str, unicode)
    integer_types = (int, long)
    text_type = unicode
    binary_type = str

def ensure_str(s, encoding='utf-8'):
    """Ensure value is str (bytes in Py2, unicode in Py3)"""
    if PY2:
        if isinstance(s, unicode):
            return s.encode(encoding)
        return s
    else:
        if isinstance(s, bytes):
            return s.decode(encoding)
        return s

def ensure_binary(s, encoding='utf-8'):
    """Ensure value is bytes in both Py2 and Py3"""
    if isinstance(s, binary_type):
        return s
    if isinstance(s, text_type):
        return s.encode(encoding)
    raise TypeError("Expected string or bytes")

def ensure_text(s, encoding='utf-8'):
    """Ensure value is text (unicode in Py2, str in Py3)"""
    if isinstance(s, text_type):
        return s
    if isinstance(s, binary_type):
        return s.decode(encoding)
    raise TypeError("Expected string or bytes")
```

## Migration Checklist

### Phase 1: Preparation
- [ ] Ensure comprehensive unit test coverage
- [ ] Set up continuous integration for multiple Python versions
- [ ] Review codebase for Python 3 incompatibilities
- [ ] Document all third-party dependencies and check Python 3 support
- [ ] Create a Python 3 branch for migration work

### Phase 2: Initial Migration
- [ ] Run 2to3 tool and review suggested changes
- [ ] Replace print statements with print() function
- [ ] Update exception handling syntax (use 'as' keyword)
- [ ] Fix integer division (use // where needed)
- [ ] Update dictionary iteration (remove iterkeys/itervalues/iteritems)
- [ ] Replace has_key() with 'in' operator
- [ ] Update standard library imports
- [ ] Fix unicode/bytes handling
- [ ] Replace xrange with range
- [ ] Replace raw_input with input

### Phase 3: Testing
- [ ] Run all unit tests in Python 3
- [ ] Test file I/O with various encodings
- [ ] Test binary vs. text handling
- [ ] Test string operations
- [ ] Test numeric operations
- [ ] Perform integration testing
- [ ] Check performance (some operations may be faster/slower)

### Phase 4: Cleanup
- [ ] Remove Python 2 compatibility code (if no longer needed)
- [ ] Remove __future__ imports (if dropping Python 2 support)
- [ ] Update documentation
- [ ] Update requirements.txt and setup.py
- [ ] Update CI/CD configuration
- [ ] Update shebang lines (#!/usr/bin/env python3)

### Phase 5: Deployment
- [ ] Deploy to staging environment
- [ ] Monitor for errors/warnings
- [ ] Deploy to production
- [ ] Monitor performance and errors
- [ ] Update documentation and README

## Useful Tools

### Migration Tools
- `2to3` - Official Python tool for automated conversion
- `python-modernize` - Like 2to3 but more conservative
- `futurize` - Adds __future__ imports for gradual migration
- `six` - Compatibility library for Python 2 and 3
- `pylint --py3k` - Check for Python 3 compatibility issues

### Testing Tools
- `tox` - Test against multiple Python versions
- `pytest` - Modern testing framework
- `coverage` - Measure test coverage
- `mypy` - Static type checker (Python 3.5+)

### Code Quality Tools
- `black` - Code formatter (Python 3.6+)
- `flake8` - Style guide enforcement
- `isort` - Import statement organizer

## Additional Resources

- Python 3 Official Documentation: https://docs.python.org/3/
- What's New in Python 3: https://docs.python.org/3/whatsnew/3.0.html
- Python 2 to 3 Porting Guide: https://docs.python.org/3/howto/pyporting.html
- Six Documentation: https://six.readthedocs.io/
- 2to3 Documentation: https://docs.python.org/3/library/2to3.html
- Modernize Documentation: https://python-modernize.readthedocs.io/

## Summary

Key points for Python 2 to 3 migration:

1. **Syntax Changes**: Print function, exception handling, integer division
2. **String Handling**: Clear separation of text (str) and bytes
3. **Iterators**: Most functions return iterators instead of lists
4. **Standard Library**: Many modules renamed and reorganized
5. **Testing**: Essential to test thoroughly with both versions during transition
6. **Tools**: Use 2to3, six, and tox for smoother migration
7. **Gradual Migration**: Use __future__ imports for incremental changes
8. **Documentation**: Keep track of changes and update docs accordingly

The migration from Python 2 to 3 requires careful planning and testing, but the improved consistency and modern features of Python 3 make it worthwhile.
