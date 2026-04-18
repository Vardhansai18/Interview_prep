# API Testing Interview Prep

## Table of Contents
1. [What is API?](#what-is-api)
2. [What are the main differences between API and Web Services?](#what-are-the-main-differences-between-api-and-web-services)
3. [What are API Usage Limits?](#what-are-api-usage-limits)
4. [What are some architectural styles for creating a Web API?](#what-are-some-architectural-styles-for-creating-a-web-api)
5. [Who can use a Web API?](#who-can-use-a-web-api)
6. [What is API Testing?](#what-is-api-testing)
7. [What are the Advantages of API Testing?](#what-are-the-advantages-of-api-testing)
8. [What are Common Protocols Used in API Testing?](#what-are-common-protocols-used-in-api-testing)

---

## What is API?

An **API** (Application Programming Interface) is a contract that allows one software system to communicate with another in a structured way.

Think of it like this:

- **You (client)** → send a request
- **Server** → processes it
- **Server** → sends back a response

You don't need to know how the server works internally—only what to send and what you'll get back.

---

### 🔧 Real-Life Analogy

**A restaurant:**

- **You** = client
- **Waiter** = API
- **Kitchen** = server

You don't go into the kitchen. You tell the waiter what you want → waiter brings your food.

---

### 💻 Technical Example (HTTP API)

**Request:**
```http
GET /users/101
```

**Response:**
```json
{
  "id": 101,
  "name": "Vardhan",
  "role": "Engineer"
}
```

---

### 📦 Types of APIs

**Common API Types:**

#### 1. REST API (Most used)
Uses HTTP methods: `GET`, `POST`, `PUT`, `DELETE`

**Example:**
```http
GET /products
POST /orders
```

#### 2. SOAP API
- Uses XML
- More strict, used in enterprise systems

#### 3. GraphQL API
Client asks exactly what data it needs

**Example:**
```graphql
{
  user(id: 101) {
    name
    email
  }
}
```

---

### 🌍 Real-World API Examples

**Examples in Production:**

#### 1. Google Maps API
Used in apps like Uber, Zomato

**Example:**
```http
GET /maps/api/directions?from=A&to=B
```

#### 2. Payment API (e.g., Stripe)
Used for online payments

```http
POST /payments
```

#### 3. Weather API
Fetch weather data

```http
GET /weather?city=Hyderabad
```

#### 4. Authentication API
Login systems (JWT, OAuth)

```http
POST /login
```

---

### 🧠 Why APIs are Important

**Key Benefits:**

- ✅ Decouples frontend & backend
- ✅ Enables microservices
- ✅ Allows third-party integrations
- ✅ Used everywhere (mobile apps, web apps, cloud services)

---

### ⚡ Simple Python Example

**Making an API call with Python:**

```python
import requests

response = requests.get("https://api.github.com/users/octocat")
print(response.json())
```

---

## What are the main differences between API and Web Services?

### Core Difference (Simple View)

- **API** = Any interface that lets two pieces of software talk
- **Web Service** = An API that works over a network using web protocols (HTTP/HTTPS)

👉 **So yes:**  
All Web Services are APIs, but **not all APIs are Web Services**

---

### ⚖️ Key Differences

#### 1. Scope
- **API** → Broader concept (can be local, library-based, OS-level)
- **Web Service** → Always network-based

#### 2. Network Requirement
- **API** → May or may not need network
- **Web Service** → Always needs network (HTTP/HTTPS)

👉 **Key point:**  
APIs can work without a network, but Web Services always require one.

#### 3. Communication Protocols
- **API** → Any protocol (function calls, libraries, REST, etc.)
- **Web Service** → Typically:
  - REST
  - SOAP
  - XML-RPC

#### 4. Use Case Complexity
- **API** → Can be simple (e.g., calling a function)
- **Web Service** → Designed for distributed systems (client-server over network)

---

### 🧠 Real-Life Examples (Very Important for Interview)

#### 🍽️ Example 1: Restaurant vs Online Food App

**API (Local interaction)**

You go into a restaurant kitchen and directly ask the chef:
- No internet
- Direct communication

👉 This is like a local API call (e.g., Python function)

**Web Service (Network-based)**

You order food using **Zomato or Swiggy**

**Flow:**
1. App → sends request over internet
2. Server → processes order
3. Response → sent back

👉 This is a Web Service (REST API over HTTP)

---

#### 💻 Example 2: Programming vs Internet

**API Example (No Network)**
```python
import math
print(math.sqrt(16))
```
- You're using Python's math API
- No internet involved

**Web Service Example (With Network)**
```python
import requests
response = requests.get("https://api.openweathermap.org/data")
```
- Calling a remote server
- Uses HTTP
- Needs internet

👉 This is a Web Service

---

## What are API Usage Limits?

API usage limits (rate limits / quotas) are restrictions set by the provider on:

- How many requests you can make
- How fast you can make them
- How much data you can access

These limits protect the system from overload and control cost + fairness.

---

### ⚙️ Types of Limits

- **Rate limit** → e.g., 100 requests per minute
- **Quota limit** → e.g., 10,000 requests per day
- **Billing limit** → pay after free tier is exhausted

---

### 🧠 Real-Life Examples (Interview-ready)

#### 📍 Example 1: Maps API (Very Common)

**Apps like Google Maps**

Suppose you build a ride app (like Uber):
- Every time a user searches location → API call
- Directions, distance, ETA → multiple API calls

👉 **Limit scenario:**

- Free tier: 1000 requests/day
- Your app hits 1500 requests

❌ **Result:**

- API stops responding OR starts charging money
- Your app cannot show routes

👉 **Real-world impact:**

Users see "Unable to fetch directions"

---

### ✅ Best Practices (What interviewer expects)

- **Implement rate limiting handling** - Catch and handle 429 (Too Many Requests) errors
- **Use caching** - Reduce API calls by storing frequently accessed data
- **Monitor usage** - Set up alerts before hitting limits
- **Use retry with backoff** - Exponential backoff strategy for failed requests
- **Plan for scaling + billing** - Understand cost implications as your app grows

---

## What are some architectural styles for creating a Web API?

This is one of the fundamental Web API interview questions. Below are four common Web API architectural styles:

### 🏗️ Common Architectural Styles

1. **HTTP for client-server communication**
   - Uses standard HTTP protocols
   - Request-response model

2. **XML/JSON as formatting language**
   - Structured data exchange
   - JSON is more lightweight and popular
   - XML is more verbose but powerful

3. **Simple URI as the address for the services**
   - Clean and intuitive endpoints
   - Example: `/api/users`, `/api/orders`

4. **Stateless communication**
   - Each request is independent
   - Server doesn't store client state
   - Improves scalability

---

## Who can use a Web API?

Web API can be consumed by **any clients which support HTTP verbs** such as `GET`, `PUT`, `DELETE`, `POST`.

### 🔑 Key Points

- **No configuration required** - Web API services can be easily used by any client
- **Platform independent** - Works across different technologies and languages
- **Mobile-friendly** - Even portable devices such as mobile devices can easily use Web API
- **Biggest advantage** - Universal accessibility and ease of integration

### 💡 Examples of Clients that can consume Web API

- **Web browsers** - JavaScript/AJAX calls
- **Mobile apps** - iOS, Android
- **Desktop applications** - Any programming language (Python, Java, C#, etc.)
- **IoT devices** - Smart devices, sensors
- **Server-to-server** - Microservices communication

---
## What is API Testing?

API Testing is a type of software testing where we validate **Application Programming Interfaces (APIs)** directly to ensure they work correctly **without relying on UI**.

---

### 🔹 Key Points to Mention in Interview

#### 1. Focus on Business Logic (Not UI)

API testing validates the core functionality of the system. It bypasses UI and interacts directly with endpoints.

👉 **Example:**

In a food delivery app, instead of clicking "Place Order", API testing directly calls:

```http
POST /orders
```

and verifies if the order is created.

---

#### 2. Types of Checks in API Testing

You should explicitly mention these 4 areas:

##### ✅ Functional Testing
Checks if API returns correct response for valid input.

👉 **Example:**
```
Login API should return 200 OK + token for valid credentials.
```

##### ✅ Reliability Testing
Ensures API works consistently over time.

👉 **Example:**
```
Calling GET /get-user 100 times should always return correct data.
```

##### ✅ Performance Testing
Measures response time and scalability.

👉 **Example:**
```
Can the API handle 1000 concurrent users without slowing down?
```

##### ✅ Security Testing
Ensures API is protected from unauthorized access.

👉 **Example:**
```
Accessing GET /user/profile without token should return 401 Unauthorized.
```

---

## What are the Advantages of API Testing?

API testing offers numerous benefits over traditional UI testing, making it a critical part of modern software development.

---

### 🔹 Key Advantages

#### 1. Early Testing of Core Functionality

API testing validates business logic at the backend level before UI is ready. Helps catch defects early, reducing cost of fixing later.

👉 **Real-life example:**

In a banking app, before UI is built, you can test:

```http
POST /transfer-money
```

to ensure money transfer logic works correctly.

---

#### 2. Faster Execution (Time Efficient)

No UI rendering → faster response validation. Suitable for quick regression testing.

👉 **Real-life example:**

Testing login via API takes milliseconds, while UI testing requires loading pages, entering data, waiting for elements.

---

#### 3. Higher Test Coverage with Less Effort

Covers multiple scenarios (edge cases, negative cases) easily. Automation requires less code compared to UI automation.

👉 **Real-life example:**

You can test:
- valid login
- invalid login
- empty fields
- SQL injection cases

—all using API calls quickly.

---

#### 4. Language Independent

APIs use JSON/XML, so any programming language can be used.

👉 **Real-life example:**

You can test the same API using:
- Python (requests)
- Java (RestAssured)
- JavaScript (Axios)

---

#### 5. Better Debugging and Issue Isolation

Errors are easier to identify since testing is done at service layer.

👉 **Real-life example:**

If `/get-user` API fails, you know issue is backend—not UI or frontend JavaScript.

---

#### 6. Improved Automation and CI/CD Integration

APIs integrate easily into pipelines like Jenkins/GitLab CI/CD.

👉 **Real-life example:**

After every code commit, API tests run automatically to validate backend stability.

---

#### 7. No Dependency on UI Availability

Testing can start even if frontend is incomplete or unstable.

👉 **Real-life example:**

Frontend team is still designing screens, but backend APIs like `/register` can already be tested.

---

#### 8. Supports Load & Performance Testing

APIs are ideal for testing scalability and performance.

👉 **Real-life example:**

Simulate 1000 users hitting:

```http
GET /products
```

to check response time under load.

---

#### 9. Easy Integration with GUI Testing

APIs help prepare test data for UI tests.

👉 **Real-life example:**

Before running UI test for login, create a user via API:

```http
POST /create-user
```

Then use that user in UI automation.

---

#### 10. Cost Effective

Faster execution + early bug detection = reduced overall testing cost.

👉 **Real-life example:**

Fixing a bug in API stage is much cheaper than fixing it after full UI development.

---

### 🔹 One-Line Summary (for interview)

> "API testing is faster, more reliable, and cost-effective than UI testing because it validates core backend functionality early, independent of the user interface."

---

## What are Common Protocols Used in API Testing?


Understanding the protocols used in API testing is crucial for effective test automation and integration.

---

### 🌐 Common Protocols

#### 1. HTTP (HyperText Transfer Protocol)

**Foundation of most web APIs.** Works on request–response model.

👉 **Key Methods:**

```
GET, POST, PUT, PATCH, DELETE
```

👉 **Real-life example:**

When you open a website or app, it sends:

```http
GET /users
```

to fetch user data from server.

---

#### 2. REST (Representational State Transfer)

**Architectural style built on top of HTTP.** Uses JSON mostly for communication. Stateless and lightweight.

👉 **Real-life example:**

In an e-commerce app:

```http
GET /products
POST /orders
```

returns JSON responses.

---

#### 3. SOAP (Simple Object Access Protocol)

**Protocol that uses XML format only.** More secure and strict than REST. Common in enterprise systems (banking, telecom).

👉 **Real-life example:**

A banking system uses SOAP to securely transfer transaction details between systems.

---

#### 4. JMS (Java Message Service)

**Used for asynchronous communication.** Works with queues/topics (not direct request-response).

👉 **Real-life example:**

When you place an order:
- API sends message to queue
- Backend processes it later (order confirmation, invoice)

---

#### 5. UDDI (Universal Description, Discovery, and Integration)

**Acts like a directory for web services.** Helps applications discover APIs/services.

👉 **Real-life example:**

A company system searches UDDI registry to find available payment service APIs.



9)What is API Test Environment?

An API test environment is a setup of server, database, and required configurations where APIs are deployed and tested without a GUI.

🔹 Key Points to Mention in Interview
1. Backend-Focused Environment (No UI)
API testing happens without any frontend/UI.
Interaction is through tools like Postman or code.

👉 Real-life example:
Testing:

POST /login

directly via Postman instead of using a login webpage.

2. Includes Server Setup
APIs are hosted on servers (local, staging, or production-like).
You need proper endpoints (URLs) to test.

👉 Real-life example:

https://staging.myapp.com/api/login

This staging server is used for testing before production.

3. Database Configuration
API interacts with database → must be properly set up.
Test data should be available or seeded.

👉 Real-life example:
After calling:

POST /create-user

verify that the user is stored in the database.

4. Environment Variables & Parameters
Different environments use different configs:
URLs
Tokens
API keys

👉 Real-life example:

Dev → dev.api.com
QA → qa.api.com
Prod → api.com
5. Authentication & Authorization Setup
APIs often require tokens, API keys, OAuth, etc.

👉 Real-life example:

Authorization: Bearer <token>

Without this, API should return 401 Unauthorized.

6. Test Data Preparation
Need valid and invalid datasets for testing.

👉 Real-life example:

Valid user → success case
Invalid password → failure case
7. Dependency Handling (External Services)
APIs may depend on third-party services.
Use mocks/stubs if services are unavailable.

👉 Real-life example:
Payment API depends on Stripe → mock it during testing.

8. API Verification After Setup
Once environment is ready, validate:
Response correctness
Status codes
Performance

👉 Real-life example:

GET /users

Check:

Status → 200
Response time
Correct JSON data
9. Testing with Different Parameters
Same API is tested with multiple inputs.

👉 Real-life example:

GET /products?category=electronics
GET /products?category=clothing

Validate different responses.

10. Logging & Monitoring
Logs help debug failures in API environment.

👉 Real-life example:
If API fails, check server logs to identify root cause.

🔹 Real-Life End-to-End Scenario

👉 E-commerce API Testing Environment

Server → staging server deployed
Database → test DB with sample users/products
API → /login, /orders, /products
Tool → Postman / pytest
Auth → Bearer token
Flow:
Call login API → get token
Use token to create order
Verify order stored in DB
Test with invalid inputs

9)What is the test environment of API?
Setting up the API’s test environment is not an easy task, so you should have a
ready answer if your API testing interview is coming. The test environment of
API is a bit complete and requires the configuration of the database and server,
depending on the software requirements. No GUI (Graphical User Interface) is
available in this test form.
When the installation process is complete, API is verified for the proper
operation. Throughout the process, the API called from the original environment
is set up with different parameters to study the test results. 


API test environment is a backend setup with server, database, configurations, authentication, and dependencies where APIs are tested directly without a UI



9)  Principles of API Test Design
1. Setup (Pre-conditions)
Prepare everything required before executing the test:
Test data
Server readiness
Authentication tokens
Required objects/services

👉 Real-life example:
Before testing order creation:

POST /login

Get auth token and ensure user + products exist in DB.

2. Execution (Test Steps)
Perform the actual API call with required inputs.
Include request construction, headers, and logging.

👉 Real-life example:

POST /orders
Authorization: Bearer <token>
{
  "product_id": 101,
  "quantity": 2
}
3. Verification (Assertions)
Validate the API response against expected results:
Status codes
Response body
Business logic correctness

👉 Real-life example:

Status → 201 Created
Response contains order_id
Total price calculation is correct
4. Reporting (Result Status)
Capture and report test outcome:
Pass
Fail
Blocked

👉 Real-life example:

If status is 201 → Pass
If status is 500 → Fail
If API is down → Blocked

Reports are usually generated in tools like CI/CD dashboards.

5. Clean Up (Post-conditions)
Restore system to original state after test execution.
Remove test data to avoid conflicts.

👉 Real-life example:

DELETE /orders/{order_id}

Delete the test order created during execution.

🔹 End-to-End Example (Putting it all together)

👉 Scenario: Test Order API

Setup
Create user
Login → get token
Execution
Call POST /orders
Verification
Check 201 Created
Validate response data
Reporting
Mark test as Pass/Fail
Clean Up
Delete created order


11)Common API Testing Types
1. Validation Testing
Ensures API meets basic correctness and expected behavior.
Checks response structure, status codes, and data.

👉 Example:

GET /users/101

Verify:

Status → 200 OK
Response contains id, name
2. Functional Testing
Validates business logic of the API.

👉 Example:

POST /apply-discount

Check if correct discount is applied based on rules.

3. UI Testing (Indirect for APIs)
Ensures API works correctly when integrated with UI.

👉 Example:
Clicking “Login” button triggers:

POST /login

Verify API supports UI functionality.

4. Load Testing
Checks how API performs under heavy traffic.

👉 Example:
Simulate 1000 users calling:

GET /products

Verify response time and stability.

5. Runtime / Error Detection Testing
Identifies issues like:
Memory leaks
Crashes
Unexpected failures

👉 Example:
Repeatedly call an API 10,000 times → ensure it doesn’t crash.

6. Security Testing
Ensures API is protected from unauthorized access.

👉 Example:

GET /user/profile

Without token → expect 401 Unauthorized.

7. Penetration Testing
Simulates real-world attacks to find vulnerabilities.

👉 Example:
Try SQL Injection:

POST /login
{
  "username": "' OR 1=1 --",
  "password": "123"
}
8. Fuzz Testing
Sends random/invalid data to check robustness.

👉 Example:

POST /register
{
  "username": "@@@###$$$",
  "age": -999
}

API should handle gracefully (not crash).

9. Interoperability & WS Compliance Testing
Ensures API works across:
Different systems
Protocol standards (REST/SOAP)

👉 Example:
API should work correctly when accessed from:

Web app
Mobile app
Third-party client
🔹 Quick Summary Table
Type	Purpose	Example
Validation	Basic correctness	Check status & schema
Functional	Business logic	Discount calculation
UI	UI integration	Login button
Load	Performance	1000 users
Runtime	Stability	Repeated calls
Security	Access control	Token validation
Penetration	Attack simulation	SQL injection
Fuzz	Invalid inputs	Random data
Interoperability	Cross-system	Mobile + web