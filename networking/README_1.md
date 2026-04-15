# Computer Networks — Interview Preparation

📚 Quick, interview-friendly notes with real-life analogies and examples.

---

## 1. What is a Network? 🌐

A **network** is a system where multiple devices are interconnected to communicate and share data using standard protocols.

### Example
When you stream a match on JioHotstar, your device requests video from a server and receives data in packets — that client ↔ server ↔ network interaction is a real-world network example.

---

## 2. Key Points Interviewers Expect ✅

- Devices are connected (nodes)
- Communication happens via protocols (HTTP, TCP/IP)
- Data is transferred as packets
- There is always a sender, receiver, and medium

---

## 3. Real-Life Analogies 🔁

### Domino's Delivery (Simple Mapping) 🏪

1. You place an order → request sent
2. Store prepares pizza → server processes request
3. Delivery agent → data packets delivered

| Real Life | Network Equivalent |
|-----------|--------------------|
| Customer | Client (your device) |
| Domino's app | Application layer |
| Internet/mobile network | Communication channel |
| Store | Server |
| Delivery agent | Packets |
| Order tracking | Protocols |

**Takeaway:** Networks connect devices and services just like Domino's connects customers and stores.

---

### Video Streaming (Buffering & Bandwidth) 📺

| Action | Network Concept |
|--------|-----------------|
| Open app | HTTP(S) request |
| Network | Infrastructure / ISP |
| Video chunks | Packets |
| Buffering | Latency / jitter |
| Smooth playback | Good bandwidth |

---

## 4. Private & Special IP Addresses 🔐

### Private IPs (Used inside LANs)

- Not routable on the public internet
- Common ranges:

| Class | Range |
|-------|-------|
| A | 10.0.0.0 — 10.255.255.255 |
| B | 172.16.0.0 — 172.31.255.255 |
| C | 192.168.0.0 — 192.168.255.255 |

Example (home):

- Phone → `192.168.1.2`
- Laptop → `192.168.1.3`
- TV → `192.168.1.4`

Routers use DHCP to assign these addresses and NAT to share a public IP.

### Loopback / Localhost 🖥️

- `127.0.0.1` — talks to the same machine

Run a local server:

```bash
python app.py
```

Open:

```
http://127.0.0.1:5000
```

This traffic never leaves your host.

---

## 5. Network Address Translation (NAT) 🔁

NAT maps many private IPs to a single public IP so internal devices access the internet.

**Analogy:** Apartment building — flats = private IPs, building address = public IP, receptionist = NAT router.

Benefits:

- Conserves IPv4 addresses
- Provides basic isolation

---

## 6. VPN — Types & Use Cases 🔒

### a) Access VPN (Remote Access) 🧑‍💻
- One user connects to company network using a VPN client (e.g., AnyConnect).
- Use: Work from home.

### b) Site-to-Site VPN 🏢
- Connects two networks (office → office) over the internet.
- Use: Branch connectivity (Hyderabad ↔ Mumbai).

### c) Intranet VPN
- Connects multiple offices of the same org into a single virtual network.

### d) Extranet VPN
- Allows partners/suppliers limited access to specific internal resources.

| Feature | Access VPN | Site-to-Site VPN |
|--------:|:----------:|:----------------:|
| Connection | User → Network | Network → Network |
| Device | VPN client | Router / firewall |
| Authentication | Username / MFA | Pre-configured devices |
| Use case | Remote user access | Branch office connectivity |

### VPN Advantages ✅

## 6. VPN — Types & Use Cases 🔒

### a) Access VPN (Remote Access) 🧑‍💻
- Real-life: work from home using a VPN client (e.g., Cisco AnyConnect).
- One user → company network; device-level authentication (username/MFA).

### b) Site-to-Site VPN 🏢
- Real-life: secure link between branch offices (Hyderabad ↔ Mumbai).
- Network → Network; routers/firewalls handle tunnels and encryption.

### c) Intranet VPN 🏬
- Connects multiple offices of the same organization into a single virtual private network.

### d) Extranet VPN 🤝
- Provides limited, secure access for partners or suppliers to specific internal resources.

| Feature | Access VPN | Site-to-Site VPN |
|--------:|:----------:|:----------------:|
| Connection | User → Network | Network → Network |
| Who connects | Individual user | Entire office/branch |
| Device | VPN client software | Router / firewall |
| Authentication | Username/password, MFA | Pre-configured device credentials |
| Use case | Remote access | Branch-to-branch connectivity |

### VPN Advantages ✅

- Encrypts traffic and protects data in transit
- Hides real IP addresses (privacy)
- Enables safe remote access and branch connectivity
- Cost-effective vs private WANs

---

## 7. LAN & WLAN 📡

**LAN (Local Area Network):** connects devices in a limited area (home, office).

Types:
- Wired LAN — Ethernet (stable, low-latency)
- Wireless LAN (WLAN) — Wi‑Fi (flexible, mobile)

Use examples:
- Office desktops and printers (wired)
- Phones and laptops via Wi‑Fi (wireless)

---

## 8. VLAN (Virtual LAN) 🏷️

VLANs provide logical segmentation on switches so groups of devices behave as separate networks.

- Example: `VLAN 10 = HR`, `VLAN 20 = Finance`, `VLAN 30 = Engineering`
- Access (untagged) port: single VLAN for end devices
- Trunk (tagged) port: carries multiple VLANs between switches

Analogy: stickers on students identify classes (tagged) vs no sticker (untagged/default group).

---

## 9. Subnetting (Why network + host?) ✂️

Analogy: postal address — city/street (network) + house number (host).

IP example: `192.168.1.10` → `192.168.1` = network, `10` = host.

### Quick /26 example (HR subnet)

- Subnet: `192.168.1.0/26`
- `/26` → 26 bits network, 6 bits hosts → 2^6 = 64 addresses
- Network ID: `192.168.1.0`
- Broadcast: `192.168.1.63`
- Usable: `192.168.1.1` — `192.168.1.62`

| Type | Address |
|------|---------|
| Network ID | 192.168.1.0 |
| First usable | 192.168.1.1 |
| Last usable | 192.168.1.62 |
| Broadcast | 192.168.1.63 |

**Shortcut:** Network = first IP, Broadcast = last IP, usable = in between.

---

## 10. Real-Life Example: Postal Address Analogy 📬

Address: USA, Seattle, 5th Avenue, House No. 101

- Network part: USA → Seattle → 5th Avenue (helps route to area)
- Host part: House No. 101 (identifies exact device)

Mapping to IP:

| IP Part | Meaning |
|--------:|---------|
| `192.168.1` | Network (area) |
| `10` | Host (device) |

How data travels:

- Routers first determine the target **network**, then local delivery to the **host**.

Why separate network/host?

- Scales routing and groups devices logically.

---

## 11. Quick Revision Card (one-liners) 📝

- NAT: private → public IP translation
- Loopback: `127.0.0.1` (local host)
- VPN: secure encrypted tunnel
- VLAN: logical segmentation on switches
- Subnet: split network into smaller networks

---

If you'd like, I can now:

- add an `examples/` folder with `curl` and `python` snippets
- generate a printable one-page revision card (PDF or Markdown)

Which would you like next?

👉 With network + host:

Routing becomes fast and scalable
Devices can be grouped logically
🔷 Technical View (Simple)
Network part → Used by routers to forward packets
Host part → Used inside the network to deliver to exact device