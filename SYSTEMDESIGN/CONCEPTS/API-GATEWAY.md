# API Gateway - System Design Concept

## Overview

An **API Gateway** is a server that acts as a single entry point for all client requests in a microservices architecture. Instead of clients communicating directly with multiple backend services, they interact with the API Gateway, which routes requests to the appropriate services.

**Definition:** An API Gateway is a reverse proxy that provides a unified interface to a collection of microservices, handling cross-cutting concerns like authentication, rate limiting, load balancing, and request aggregation.

---

## Real-World Analogy: Restaurant Waiter

Imagine you're at a restaurant:

**Without a Waiter (No API Gateway):**
- You (the customer) would need to:
  - Go to the kitchen to order food
  - Walk to the billing counter to pay
  - Visit the inventory room to check availability

**With a Waiter (API Gateway):**
- You simply talk to the waiter who:
  - Takes your request
  - Routes it to the correct department
  - Collects responses from multiple departments
  - Returns the consolidated result to you

```
       Customer
           |
           v
        Waiter
     (API Gateway)
           |
           +-------> Kitchen (Food Service)
           |
           +-------> Billing (Payment Service)
           |
           +-------> Inventory (Stock Service)
```

---

## Software Example: E-Commerce Application

**Scenario:** A user opens a product page in an e-commerce app.

**Required Data:**
- Product details → Product Service
- Customer reviews → Review Service
- Stock availability → Inventory Service
- Related products → Recommendation Service

### Without API Gateway

The mobile app must know the address and make separate calls to every service:

```
    Mobile App
        |
        +---------> Product Service (http://product.api:8001)
        |
        +---------> Review Service (http://review.api:8002)
        |
        +---------> Inventory Service (http://inventory.api:8003)
        |
        +---------> Recommendation Service (http://recommend.api:8004)
```

**Problems:**
- Client needs to know all service endpoints
- Multiple network calls increase latency
- Authentication logic duplicated across services
- Difficult to manage service discovery
- Exposes internal architecture to clients

### With API Gateway

The mobile app makes a single call to the gateway:

```
    Mobile App
        |
        v
   API Gateway (https://api.company.com)
        |
        +---------> Product Service
        |
        +---------> Review Service
        |
        +---------> Inventory Service
        |
        +---------> Recommendation Service
```

**Benefits:**
- Single entry point for clients
- Simplified client code
- Centralized cross-cutting concerns
- Internal architecture hidden from clients
- Easy to refactor backend services

---

## Core Responsibilities of an API Gateway

### 1. Request Routing

Routes incoming requests to the appropriate backend service based on the request path.

**Example:**
```
GET /api/products/123       → Product Service
GET /api/orders/456         → Order Service
POST /api/payments          → Payment Service
GET /api/users/789/profile  → User Service
```

**Benefits:**
- Clients don't need to know individual service URLs
- Easy to add/remove services without affecting clients
- Supports service versioning (e.g., `/v1/products`, `/v2/products`)

---

### 2. Authentication & Authorization

Validates user credentials and permissions before forwarding requests to backend services.

**Flow:**
```
User Request → API Gateway → Validate JWT Token → Forward to Service
                    |
                    v
              [If Invalid: Return 401]
```

**Benefits:**
- Centralized authentication logic
- Backend services don't need to implement auth
- Supports multiple auth mechanisms (JWT, OAuth, API Keys)
- Single point for security enforcement

---

### 3. Rate Limiting

Prevents abuse by limiting the number of requests a user/IP can make within a time window.

**Example Rules:**
```
Free Tier Users:    100 requests/minute
Premium Users:      1,000 requests/minute
API Key (Internal): 10,000 requests/minute
```

**Implementation:**
```
Request → API Gateway → Check Rate Limit
                           |
                           +---> [Within Limit] → Forward to Service
                           |
                           +---> [Exceeded] → Return 429 (Too Many Requests)
```

**Benefits:**
- Protects backend services from overload
- Prevents DDoS attacks
- Ensures fair resource usage
- Enforces usage tiers

---

### 4. Load Balancing

Distributes incoming traffic across multiple instances of a service.

**Scenario:** Product Service has 3 instances running:

```
API Gateway
     |
     +---------> Product Service Instance 1 (Load: 30%)
     |
     +---------> Product Service Instance 2 (Load: 35%)
     |
     +---------> Product Service Instance 3 (Load: 35%)
```

**Load Balancing Algorithms:**
- **Round Robin** - Distributes requests sequentially
- **Least Connections** - Routes to instance with fewest active connections
- **Weighted Round Robin** - Distributes based on instance capacity
- **IP Hash** - Routes same client to same instance (sticky sessions)

**Benefits:**
- Improved availability and reliability
- Better resource utilization
- Horizontal scalability
- No single point of failure

---

### 5. Response Aggregation (Backend for Frontend Pattern)

Combines data from multiple services into a single response.

**Example:** User Dashboard Request

**Single Client Request:**
```
GET /api/user-dashboard
```

**Gateway Internal Calls:**
```
API Gateway
     |
     +---------> User Service (Get user profile)
     |
     +---------> Order Service (Get recent orders)
     |
     +---------> Notification Service (Get unread notifications)
     |
     +---------> Recommendation Service (Get personalized suggestions)
```

**Aggregated Response:**
```json
{
  "user": {
    "name": "John Doe",
    "email": "john@example.com"
  },
  "recentOrders": [...],
  "notifications": [...],
  "recommendations": [...]
}
```

**Benefits:**
- Reduces number of client requests (from N to 1)
- Decreases network latency
- Simplifies client-side logic
- Optimizes mobile/bandwidth-constrained clients

---

### 6. Protocol Translation

Converts between different protocols (HTTP, gRPC, WebSockets, etc.).

**Example:**
```
Mobile App (HTTP/REST) → API Gateway → Backend Services (gRPC)
```

**Benefits:**
- Clients use simple, standard protocols
- Backend can use optimized protocols internally
- Enables gradual migration between protocols

---

### 7. Request/Response Transformation

Modifies request or response data to match client/service requirements.

**Use Cases:**
- Convert XML to JSON or vice versa
- Add/remove headers
- Modify request payloads
- Filter sensitive data from responses
- API versioning transformations

---

### 8. Caching

Caches frequently requested data to reduce backend load and improve response times.

**Example:**
```
Request → API Gateway → Check Cache
                           |
                           +---> [Cache Hit] → Return Cached Response
                           |
                           +---> [Cache Miss] → Forward to Service → Cache Response
```

**Benefits:**
- Reduced latency for clients
- Lower backend service load
- Cost savings (fewer service calls)

---

### 9. Monitoring & Logging

Centralizes logging, metrics, and monitoring for all API traffic.

**Tracked Metrics:**
- Request count and rate
- Response times (latency)
- Error rates (4xx, 5xx)
- Service availability
- Authentication failures
- Rate limit violations

**Benefits:**
- Single place to monitor all API traffic
- Early detection of issues
- Performance optimization insights
- Security audit trail

---

### 10. Circuit Breaking

Prevents cascading failures by stopping requests to failing services.

**States:**
```
Closed (Normal) → [Failures exceed threshold] → Open (Block requests)
                                                      |
                                                      v
                                              Half-Open (Test recovery)
                                                      |
                                                      v
                                                [Success] → Closed
                                                [Failure] → Open
```

**Benefits:**
- Prevents resource exhaustion
- Faster failure response to clients
- Automatic recovery detection
- System resilience

---

## Real-World Usage

### Companies Using API Gateways

**Netflix:**
- Handles billions of requests daily
- Uses Zuul (their open-source API Gateway)
- Routes traffic to 500+ microservices

**Amazon:**
- AWS API Gateway for serverless architectures
- Manages millions of API calls per second

**Uber:**
- Routes requests across 2000+ microservices
- Handles location, payments, rides, and more

**Airbnb:**
- Manages search, booking, payment, and messaging services
- Centralizes authentication and rate limiting

---

## Why Companies Use API Gateways

### Without API Gateway

**Problems:**
- Clients must know every service address
- Authentication logic duplicated in each service
- Difficult to implement rate limiting consistently
- No centralized monitoring or logging
- Tight coupling between clients and services
- Complex client-side orchestration

### With API Gateway

**Benefits:**
- ✅ **Single Entry Point** - Simplified client architecture
- ✅ **Centralized Authentication** - Security enforced in one place
- ✅ **Consistent Rate Limiting** - Fair resource distribution
- ✅ **Unified Monitoring** - Complete visibility of API traffic
- ✅ **Service Isolation** - Backend changes don't affect clients
- ✅ **Easy Debugging** - Centralized logging and tracing
- ✅ **Better Performance** - Caching and response aggregation
- ✅ **Scalability** - Load balancing and circuit breaking

---

## Popular API Gateway Solutions

### Open Source
- **Kong** - Built on Nginx, highly extensible with plugins
- **Apache APISIX** - Cloud-native, high-performance gateway
- **Tyk** - Written in Go, RESTful API management
- **KrakenD** - Ultra-fast, stateless API Gateway

### Cloud-Managed
- **AWS API Gateway** - Fully managed, serverless-friendly
- **Azure API Management** - Enterprise-grade API management
- **Google Cloud API Gateway** - Integrated with GCP services
- **Apigee (Google)** - Enterprise API management platform

### Framework-Integrated
- **Spring Cloud Gateway** - For Spring Boot applications
- **Netflix Zuul** - Used by Netflix for microservices
- **Express Gateway** - Built on Node.js and Express
- **Ocelot** - .NET Core API Gateway

---

## API Gateway vs Other Patterns

### API Gateway vs Load Balancer

| Aspect | API Gateway | Load Balancer |
|--------|-------------|---------------|
| **Layer** | Application Layer (L7) | Transport/Network Layer (L4/L7) |
| **Intelligence** | Business logic aware | Traffic distribution only |
| **Features** | Routing, auth, transformation | Distribution only |
| **Use Case** | Microservices orchestration | Traffic distribution |

### API Gateway vs Service Mesh

| Aspect | API Gateway | Service Mesh |
|--------|-------------|--------------|
| **Location** | Edge (external traffic) | Internal (service-to-service) |
| **Purpose** | Client-facing entry point | Inter-service communication |
| **Examples** | Kong, AWS API Gateway | Istio, Linkerd, Consul |

### API Gateway vs Reverse Proxy

| Aspect | API Gateway | Reverse Proxy |
|--------|-------------|---------------|
| **Scope** | API-specific features | General web traffic |
| **Intelligence** | Request aggregation, transformation | Simple forwarding |
| **Use Case** | Microservices API management | Load distribution, SSL termination |

---

## Potential Drawbacks

### 1. Single Point of Failure
- **Risk:** If gateway goes down, entire system is unreachable
- **Solution:** Deploy multiple gateway instances with load balancing

### 2. Performance Bottleneck
- **Risk:** Gateway can become a bottleneck under high load
- **Solution:** Horizontal scaling, caching, async processing

### 3. Increased Latency
- **Risk:** Additional hop adds latency
- **Solution:** Keep gateway lightweight, use caching, optimize routing

### 4. Complexity
- **Risk:** Gateway configuration can become complex
- **Solution:** Use infrastructure as code, proper documentation, testing

---

## Best Practices

1. **Keep It Lightweight** - Don't add business logic to the gateway
2. **Use Caching** - Cache frequently accessed data
3. **Implement Circuit Breakers** - Prevent cascading failures
4. **Monitor Everything** - Track latency, errors, and throughput
5. **Version Your APIs** - Use `/v1`, `/v2` for backward compatibility
6. **Secure the Gateway** - Use HTTPS, validate input, implement WAF
7. **Scale Horizontally** - Deploy multiple gateway instances
8. **Use Async Where Possible** - Don't block on long-running operations
9. **Document APIs** - Use OpenAPI/Swagger for documentation
10. **Test Thoroughly** - Load testing, chaos engineering, failover scenarios

---

## Interview Talking Points

**Quick Definition:**
> "An API Gateway is a reverse proxy that acts as the single entry point for clients, handling routing, authentication, rate limiting, load balancing, and request aggregation before forwarding requests to backend microservices."

**Key Benefits:**
- Single entry point for all client requests
- Centralizes cross-cutting concerns (auth, rate limiting, logging)
- Enables request aggregation and protocol translation
- Improves security and simplifies client architecture

**Common Use Cases:**
- Microservices architecture with multiple backend services
- Mobile applications requiring optimized API calls
- Public APIs requiring rate limiting and authentication
- Systems needing centralized monitoring and logging

**Trade-offs:**
- Introduces single point of failure (mitigate with redundancy)
- Can become a bottleneck (mitigate with caching and scaling)
- Adds complexity to infrastructure (mitigate with good tooling)

---

## Summary

API Gateways are essential components in modern microservices architectures, providing a unified entry point that simplifies client interactions, centralizes common functionality, and improves system maintainability and security. While they introduce some complexity, the benefits of centralized management, improved security, and simplified client architecture make them invaluable for large-scale distributed systems.
