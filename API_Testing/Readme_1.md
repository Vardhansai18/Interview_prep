# API Testing Interview Prep

## Table of Contents
1. [What is API?](#what-is-api)


---

## 1) What is API?

An **API** (Application Programming Interface) is a contract that allows one software system to communicate with another in a structured way.

Think of it like this:

- **You (client)** → send a request
- **Server** → processes it
- **Server** → sends back a response

You don't need to know how the server works internally—only what to send and what you'll get back.

---

## Real-Life Analogy

🔧 **A restaurant:**

- **You** = client
- **Waiter** = API
- **Kitchen** = server

You don't go into the kitchen. You tell the waiter what you want → waiter brings your food.

---

## Technical Example (HTTP API)

💻 **Request:**
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

## Types of APIs

📦 **Common API Types:**

### 1. REST API (Most used)
Uses HTTP methods: `GET`, `POST`, `PUT`, `DELETE`

**Example:**
```http
GET /products
POST /orders
```

### 2. SOAP API
- Uses XML
- More strict, used in enterprise systems

### 3. GraphQL API
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

## Real-World API Examples

🌍 **Examples in Production:**

### 1. Google Maps API
Used in apps like Uber, Zomato

**Example:**
```http
GET /maps/api/directions?from=A&to=B
```

### 2. Payment API (e.g., Stripe)
Used for online payments

```http
POST /payments
```

### 3. Weather API
Fetch weather data

```http
GET /weather?city=Hyderabad
```

### 4. Authentication API
Login systems (JWT, OAuth)

```http
POST /login
```

---

## Why APIs are Important

🧠 **Key Benefits:**

- ✅ Decouples frontend & backend
- ✅ Enables microservices
- ✅ Allows third-party integrations
- ✅ Used everywhere (mobile apps, web apps, cloud services)

---

## Simple Python Example

⚡ **Making an API call with Python:**

```python
import requests

response = requests.get("https://api.github.com/users/octocat")
print(response.json())
```
