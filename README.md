# Interview Revision Checklist

Tick a box after you can explain the topic out loud without opening the note. Change `[ ]` to `[x]` in this file, or click the box in Markdown preview if your editor writes it back.

Before an interview, revise only the sections that match the role. When you want a fresh pass, change the ticked boxes back to `[ ]`.

| Role | Start here |
| --- | --- |
| Backend / system design | [System design](#system-design), [LLD](#low-level-design), [Multithreading](#multithreading-c) |
| SDET / API automation | [API testing](#api-testing), [Pytest](#pytest), [Python](#python), [HTTP status codes](#http-status-codes) |
| DevOps | [Terraform](#terraform), [Git](#git), [Networking](#networking) |
| AI / LLM | [AI interview](#ai-interview) |

---

## OOP

Notes: [OOPS/OOPS_1.md](OOPS/OOPS_1.md)

- [ ] What is OOP
- [ ] Class and object
- [ ] Benefits of OOP
- [ ] Constructor and destructor
- [ ] Abstraction
- [ ] Encapsulation
- [ ] Inheritance and its types
- [ ] Diamond problem
- [ ] Polymorphism

## Low-level design

- [ ] What LLD is, and how it differs from HLD — [Introduction](LLD/THECODEMATE/Introduction.md)
- [ ] CERID approach (Clarify, Entities, Responsibilities, Interactions, Durability) — [LLD approach](LLD/CODENCODE/LLD_APPROACH/LLD_APPROACH.md)
- [ ] Class diagrams (association, aggregation, composition) — [Class diagrams](LLD/THECODEMATE/CLASSDIAGRAMS/CLASSDIAGRAMS.md)
- [ ] UML — [UML](LLD/THECODEMATE/UML/UML.md)

### SOLID

Summary: [SOLID summary](LLD/THECODEMATE/SOLID/SOLID_Summary.md)

- [ ] Single Responsibility — [SRP](LLD/THECODEMATE/SOLID/SRP/SRP.md)
- [ ] Open/Closed — [OCP](LLD/THECODEMATE/SOLID/OCP/ocp.md)
- [ ] Liskov Substitution — [LSP](LLD/THECODEMATE/SOLID/LSP/lsp.md)
- [ ] Interface Segregation — [ISP](LLD/THECODEMATE/SOLID/IS/IS.md)
- [ ] Dependency Inversion — [DIP](LLD/THECODEMATE/SOLID/DIP/DIP.md)

### Design patterns

- [ ] Factory — [Factory](LLD/THECODEMATE/PATTERNS/FACTORY_PATTERN.md)
- [ ] Observer — [Observer](LLD/THECODEMATE/PATTERNS/OBSERVER_PATTERN.md)
- [ ] Strategy — [Strategy](LLD/THECODEMATE/PATTERNS/STRATEGY_PATTEN.md)

### Problems with notes

- [ ] Parking lot — [design](LLD/CODENCODE/PROBLEMS/EASY/PARKING_LOT/parking_lot.md)
- [ ] Notification system — [design](LLD/CODENCODE/PROBLEMS/EASY/NOTIFICATION_SYSTEM/NOTIFICATION.md) · [C++ code](LLD/CODENCODE/PROBLEMS/EASY/NOTIFICATION_SYSTEM/CODE/README.md)
- [ ] Ride-sharing app — [story walkthrough](LLD/CODENCODE/PROBLEMS/HARD/RIDESHARINGAPP/RIDESHARINGAPP.MD)

### Problems still to write up

Full list also lives in [LLD intro](LLD/CODENCODE/INTRO/INTRO.md). Tick these when you have practised the design, even if the write-up is not in the repo yet.

**Easy**

- [ ] Logging framework
- [ ] Task management system
- [ ] Vending machine
- [ ] Traffic signal system
- [ ] Coffee machine
- [ ] Stack Overflow

**Medium**

- [ ] LRU cache
- [ ] ATM
- [ ] Elevator system
- [ ] Car rental system
- [ ] Library management system
- [ ] Hotel management system
- [ ] Restaurant management system
- [ ] Online auction system
- [ ] Pub-sub system
- [ ] Rate limiter
- [ ] File system
- [ ] Digital wallet
- [ ] Tic-tac-toe

**Hard**

- [ ] Splitwise
- [ ] Chess
- [ ] Snake and Ladder
- [ ] CricInfo
- [ ] Movie ticket booking
- [ ] Online shopping
- [ ] Food delivery
- [ ] Payment gateway
- [ ] Music streaming
- [ ] Stock brokerage
- [ ] Course registration
- [ ] Chat application

## System design

### Concepts

- [ ] What system design is, and horizontal vs vertical scaling — [Part 1](SYSTEMDESIGN/CONCEPTS/PART-1-INTRO.md)
- [ ] Client-server model — [Part 2](SYSTEMDESIGN/CONCEPTS/PART-2-CLIENT-SERVER.md)
- [ ] Load balancing and algorithms — [Part 3](SYSTEMDESIGN/CONCEPTS/PART-3-LOAD-BALANCING.md)
- [ ] Caching and eviction (Random, FIFO, LFU, LRU) — [Part 4](SYSTEMDESIGN/CONCEPTS/PART-4-CACHING.md)
- [ ] Databases, SQL vs NoSQL — [Part 5](SYSTEMDESIGN/CONCEPTS/PART-5-DATA-BASE.md)
- [ ] How to draw the diagram as you scale — [Part 6](SYSTEMDESIGN/CONCEPTS/PART-6-CREATING-DIAGRAMS.md)
- [ ] Database indexing — [Part 7](SYSTEMDESIGN/CONCEPTS/PART-7-DB-INDEXING.md)
- [ ] Forward proxy vs reverse proxy — [Part 8](SYSTEMDESIGN/CONCEPTS/PART-8-PROXY.md)
- [ ] Message queues — [notes](SYSTEMDESIGN/CONCEPTS/PART-9-CDN.md)
- [ ] CAP theorem (CP vs AP) — [Part 10](SYSTEMDESIGN/CONCEPTS/PART-10-CAP-THEOREM.md)
- [ ] API gateway — [API gateway](SYSTEMDESIGN/CONCEPTS/API-GATEWAY.md)
- [ ] Fault tolerance — [notes](SYSTEMDESIGN/CONCEPTS/FAULT-TOLERENT)

### Questions

- [ ] URL shortener (requirements, capacity, 301 vs 302, hashing) — [URL shortener](SYSTEMDESIGN/QUESTIONS/URLSHORTNER/URLSHORTNER.md)
- [ ] ZooKeeper persistent vs ephemeral nodes — [ZooKeeper](SYSTEMDESIGN/QUESTIONS/URLSHORTNER/zookeeper.md)
- [ ] Unique ID generator (UUID, ticket server, Snowflake) — [Unique ID](SYSTEMDESIGN/QUESTIONS/UNIQUE_ID_GENERATOR/UNIQUE_ID_GENERATOR.md)
- [ ] Rate limiter (token bucket, fixed window, sliding window) — [Rate limiter](SYSTEMDESIGN/QUESTIONS/RATELIMITER/RATELIMITER.md)
- [ ] Notification system (email, SMS, push, fan-out) — [Notification system](SYSTEMDESIGN/QUESTIONS/NOTIFICATIONSYSTEM/NOTIFICATIONSYSTEM.md)

## Multithreading (C++)

- [ ] What a thread is, and ways to create one in C++11 — [Thread intro](<MULTITHREADING/1)ThreadIntro.md>)
- [ ] `join()`, `detach()`, and `joinable()` — [Join and detach](<MULTITHREADING/2)Join_Detach.md>)
- [ ] Mutex, race conditions, and protecting shared data — [Mutex](<MULTITHREADING/3)Mutex.md>)
- [ ] Token-bucket scratch notes — [C++/temp](C++/temp)

## Python

Notes: [PYTHON/python_1.md](PYTHON/python_1.md)

- [ ] List vs tuple
- [ ] What `self` is
- [ ] `*args` and `**kwargs`

## Pytest

Notes: [PYTEST/Pytest.md](PYTEST/Pytest.md)

- [ ] Why Pytest instead of unittest
- [ ] Ordering
- [ ] Markers
- [ ] Fixtures
- [ ] Fixture scope
- [ ] Parametrization
- [ ] Running tests in parallel
- [ ] Logging
- [ ] Skipping tests
- [ ] Managing test data across environments
- [ ] ID vs XPath vs CSS selectors
- [ ] Headless Selenium
- [ ] Broken-link checks
- [ ] Common automation exceptions, including `ZeroDivisionError`

Practice files: [test_basic.py](PYTEST/test_basic.py), [test_fixture.py](PYTEST/test_fixture.py), [test_marker.py](PYTEST/test_marker.py), [test_order.py](PYTEST/test_order.py), [test_parametrize.py](PYTEST/test_parametrize.py), [test_scope.py](PYTEST/test_scope.py), [test_practise.py](PYTEST/test_practise.py)

## API testing

Notes: [API_Testing/Part-1.md](API_Testing/Part-1.md)

- [ ] What an API is
- [ ] API vs web service
- [ ] Usage limits
- [ ] Architectural styles
- [ ] Who can use a web API
- [ ] What API testing is, and why it helps
- [ ] Protocols used in API testing
- [ ] API test environment
- [ ] Principles of API test design
- [ ] Types of API testing
- [ ] API vs REST API
- [ ] Authentication vs authorization

### HTTP status codes

Notes: [API_Testing/HTTP_STATUS_CODE.md](API_Testing/HTTP_STATUS_CODE.md)

- [ ] Status code categories
- [ ] 2xx success, including 201 and 202
- [ ] 3xx redirection, including 301 vs 302
- [ ] 4xx client errors
- [ ] 5xx server errors
- [ ] How you assert status codes in a real test

## Networking

- [ ] What a network is — [Networks](NETWORKING/README_1.md)
- [ ] Private and special IP addresses
- [ ] NAT
- [ ] VPN types
- [ ] LAN, WLAN, and VLAN
- [ ] Subnetting
- [ ] OSI layers on a live-stream request — [OSI](NETWORKING/README_2.md)
- [ ] TCP vs UDP
- [ ] IPsec basics, tunnel setup, NAT-T, SSL fallback, EAP-MSCHAPv2 — [IPsec](NETWORKING/IPsec/README.md)

## Git

Notes: [GIT/GIT-1.md](GIT/GIT-1.md)

- [ ] What merge does
- [ ] What rebase does
- [ ] When you would choose merge, and when you would choose rebase

## Terraform

- [ ] What Terraform is for — [Questions](TERRAFORM/README_1.md)
- [ ] Declarative vs imperative infrastructure as code
- [ ] What the state file is, and why it matters — [State](TERRAFORM/README_2.md)
- [ ] How state is used to plan changes and detect drift
- [ ] Why state must be stored carefully

## AI interview

Notes: [AI_INTERVIEW/RAG_VECTOR_DB_HALLUCINATION.md](AI_INTERVIEW/RAG_VECTOR_DB_HALLUCINATION.md)

- [ ] What RAG is
- [ ] What a vector database is, and when to use one
- [ ] Problems you get without RAG, and problems that remain with RAG
- [ ] What hallucination is, and how you reduce it
- [ ] What temperature does to an answer

## DSA

- [ ] Two Sum — [NETWORKING/temp.md](NETWORKING/temp.md)
