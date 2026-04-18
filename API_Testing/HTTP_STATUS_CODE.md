# HTTP Status Codes - Interview Guide

HTTP status codes are standardized responses from a server indicating the outcome of a client's request. In interviews—especially for backend, API testing, and system design—you're expected to know both categories and practical usage patterns.

---

## Table of Contents
1. [Status Code Categories](#status-code-categories)
2. [2xx - Success Codes](#2xx---success-codes)
3. [3xx - Redirection Codes](#3xx---redirection-codes)
4. [4xx - Client Error Codes](#4xx---client-error-codes)
5. [5xx - Server Error Codes](#5xx---server-error-codes)
6. [Interview-Focused Summary](#interview-focused-summary)
7. [Real API Testing Insights](#real-api-testing-insights)

---

## Status Code Categories

Overview of HTTP status code ranges and their meanings:

| Category | Range | Meaning |
|----------|-------|---------|
| **Informational** | `1xx` | Request received, continuing |
| **Success** | `2xx` | Request successfully processed |
| **Redirection** | `3xx` | Further action needed |
| **Client Errors** | `4xx` | Problem in client request |
| **Server Errors** | `5xx` | Problem on server side |

---

## 2xx - Success Codes

✅ **Success responses indicate the request was successfully received, understood, and accepted.**

### Common 2xx Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| **200** OK | Successful GET/PUT/PATCH | `GET /users/1 → 200` |
| **201** Created | Resource created | `POST /users → 201` |
| **202** Accepted | Accepted but not completed processing | Async operations |
| **204** No Content | Success but no response body | `DELETE /users/1 → 204` |

---

### 201 Created Example

👉 **Example:**

```http
POST /api/users
```

**Response: 201 Created**
```json
{
  "id": 101,
  "name": "Sai"
}
```

---

### 202 Accepted - When to Use?

Use it for **asynchronous operations** where:

- Processing takes time
- The result is not immediately available
- Work is delegated to a background job / queue

#### 🧠 Real-World Example: File Upload Processing

**Request:**
```http
POST /upload
```

**Response: 202 Accepted**
```json
{
  "message": "File received, processing started"
}
```

---

## 3xx - Redirection Codes

🔁 **Redirection responses indicate the client must take additional action to complete the request.**

### Common 3xx Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| **301** Moved Permanently | Resource moved permanently | HTTP → HTTPS redirect |
| **302** Found | Temporary redirect | Login redirect |
| **304** Not Modified | Cached version valid | Browser caching |

---

### 301 Moved Permanently Example

👉 **Example:**

**Request:**
```http
GET /old-url
```

**Response: 301 Moved Permanently**
```http
Location: /new-url
```

---

## 4xx - Client Error Codes

❌ **Client error responses indicate the request contains bad syntax or cannot be fulfilled.**

### Common 4xx Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| **400** Bad Request | Invalid request format | Missing JSON field |
| **401** Unauthorized | Authentication required | Missing token |
| **403** Forbidden | Access denied | No permission |
| **404** Not Found | Resource doesn't exist | `/users/999` |
| **405** Method Not Allowed | Wrong HTTP method | POST on GET endpoint |
| **409** Conflict | Conflict in request | Duplicate user |
| **415** Unsupported Media Type | Wrong content-type | Sending XML instead of JSON |
| **422** Unprocessable Entity | Validation failed | Invalid email format |
| **429** Too Many Requests | Rate limiting | API limit exceeded |

---

### 404 Not Found Example

👉 **Example:**

**Request:**
```http
GET /api/users/999
```

**Response: 404 Not Found**
```json
{
  "error": "User not found"
}
```

---

## 5xx - Server Error Codes

💥 **Server error responses indicate the server failed to fulfill a valid request.**

### Common 5xx Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| **500** Internal Server Error | Generic server failure | Null pointer exception |
| **502** Bad Gateway | Invalid upstream response | Microservice failure |
| **503** Service Unavailable | Server overloaded/down | Maintenance |
| **504** Gateway Timeout | Upstream timeout | Slow backend |

---

### 500 Internal Server Error Example

👉 **Example:**

**Request:**
```http
GET /api/data
```

**Response: 500 Internal Server Error**
```json
{
  "error": "Something went wrong"
}
```

---

## Interview-Focused Summary

🔹 **Quick revision table for interviews:**

| Code | Category | When to Use |
|------|----------|-------------|
| **200** | Success | GET success |
| **201** | Success | Resource created (POST) |
| **204** | Success | Delete/update without body |
| **301** | Redirect | Permanent redirect |
| **302** | Redirect | Temporary redirect |
| **400** | Client Error | Bad input |
| **401** | Client Error | Not authenticated |
| **403** | Client Error | Not authorized |
| **404** | Client Error | Resource not found |
| **409** | Client Error | Conflict (duplicate) |
| **422** | Client Error | Validation error |
| **429** | Client Error | Rate limit |
| **500** | Server Error | Generic failure |
| **502** | Server Error | Upstream issue |
| **503** | Server Error | Service unavailable |
| **504** | Server Error | Timeout |

---

## Real API Testing Insights

🔹 **Important for API automation and testing:**

Since you work with APIs + automation, always follow these practices:

### 1. Always validate status codes in tests

```python
assert response.status_code == 200
```

### 2. Combine with response validation

```python
assert response.json()["id"] is not None
```

### 3. Negative testing

```python
assert response.status_code == 400
```

### 4. Best Practices

- **Test all happy paths** - Verify 2xx codes
- **Test error scenarios** - Verify 4xx and 5xx codes
- **Check response body** - Don't just rely on status codes
- **Validate headers** - Content-Type, Location, etc.
- **Test edge cases** - Rate limits (429), timeouts (504)

---

### Example Test Case

```python
def test_create_user():
    # Test successful creation
    response = requests.post("/api/users", json={"name": "John"})
    assert response.status_code == 201
    assert response.json()["name"] == "John"
    
def test_invalid_user():
    # Test validation error
    response = requests.post("/api/users", json={})
    assert response.status_code == 400
    assert "error" in response.json()
    
def test_user_not_found():
    # Test not found
    response = requests.get("/api/users/99999")
    assert response.status_code == 404
```
