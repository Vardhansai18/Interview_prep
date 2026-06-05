# CAP Theorem

The CAP theorem states that a distributed system can only guarantee **two out of three** of the following properties at the same time:

---

## The Three Properties

- **Consistency:**
  The system should deliver the same results no matter how and from where we query.

- **Availability:**
  The system should always return some response or result.

- **Partition Tolerance:**
  The system should be functional even if one partition is disconnected.

![CAP Theorem Properties](IMAGES/PART-10-CAP-THEOREM/image.png)

---

## CAP Theorem

![CAP Theorem](IMAGES/PART-10-CAP-THEOREM/image-1.png)

## Example: Movie Ticket Booking

### Situation

There is only **one seat left: A1**.

Two ticket counters exist:
- Counter A
- Counter B

Both counters normally stay synchronized.

---

### Case 1: Consistency First (CP)

1. Customer 1 goes to Counter A.
2. Customer 1 asks to book seat A1.
3. Counter A confirms the booking.
4. Immediately after that, the network connection between the two counters breaks.

```text
Counter A  X  Counter B
```

5. Customer 2 goes to Counter B.
6. Counter B thinks seat A1 **might** still be available.
7. However, it cannot verify that information because the network is down.
8. To preserve correctness, Counter B rejects the request.

**Counter B response:**
> Sorry, booking is temporarily unavailable.

#### Result

- Customer 1 gets the ticket.
- Customer 2 is rejected.
- No double booking happens.

**Outcome:**
- Consistency is maintained.
- Availability is reduced.

This is a **CP system**.

---

### Case 2: Availability First (AP)

1. Customer 1 books seat A1 through Counter A.
2. The network connection breaks.

```text
Counter A  X  Counter B
```

3. Customer 2 comes to Counter B.
4. Counter B cannot contact Counter A, but it still responds immediately.
5. Counter B accepts the booking request.

**Counter B response:**
> No problem, I'll book it.

#### Result

- Customer 1 gets seat A1.
- Customer 2 also gets seat A1.

Now two people have been assigned the same seat.

Later, when the network recovers:
- Counter A and Counter B synchronize again.
- The system discovers the conflict.
- One customer must be refunded or reassigned.

**Outcome:**
- Availability is maintained.
- Consistency is violated.

This is an **AP system**.

---

## Why Waiting Reduces Availability

Imagine Counter B receives a booking request.

To guarantee consistency, it must ask Counter A:

> Has seat A1 already been booked?

But the network is broken, so Counter B has only two choices.

### Option 1: Wait

Counter B waits until it can contact Counter A.

- The customer keeps waiting.
- The wait may continue indefinitely.
- The service is effectively unavailable.

### Option 2: Respond Immediately

Counter B responds without verification.

- The customer gets a quick response.
- The service stays available.
- The answer may be incorrect.

---

## The Core Trade-Off

During a network partition:

### CP

- Cannot verify data
- Reject the request
- Keep data correct

### AP

- Cannot verify data
- Still serve the request
- Risk inconsistent data

---

## One-Line Summary

When servers cannot communicate with each other, you must choose between:

- **Consistency**: keep the data correct
- **Availability**: keep answering requests

That is the essence of the CAP theorem.

The movie ticket example is a strong interview explanation because it makes the trade-off easy to visualize.
