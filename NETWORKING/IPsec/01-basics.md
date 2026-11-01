# Part 1 — Basics

Start here. If these answers are shaky, the resume stories will sound memorised.

---

## Q1. What is IPsec?

**Short answer**

IPsec is a suite of protocols that protects IP packets. It encrypts them so nobody on the path can read them, and it authenticates them so the receiver knows they came from the real peer and were not modified.

**Explain it**

A normal IP packet is like a postcard. Anyone who handles it can read it. IPsec puts that postcard in a locked box. The box is the ESP header plus encryption. Only the two ends have the key.

It works at the IP layer, so it can protect any application. The user does not change the app. Outlook, SSH, and an internal website all ride inside the same tunnel.

IPsec gives you four things:

| Goal | What it means in practice | How IPsec does it |
| --- | --- | --- |
| Confidentiality | A stranger on café Wi-Fi cannot read the packet | Encryption, usually AES-GCM inside ESP |
| Integrity | Nobody can flip bits in the packet unnoticed | An authentication tag. If the tag does not match, the packet is dropped |
| Authentication | The packet really came from the peer you trust | The handshake proves identity with a certificate, a pre-shared key, or a username and password |
| Anti-replay | An attacker cannot record a packet and send it again later | A sequence number. A number already seen is rejected |

**Real-life example**

You are in a Hyderabad café and you open an internal HR site that lives only on the company network. Without IPsec, that request is readable on the café network, and the café cannot route you to a private `10.x` address anyway. With IPsec, your laptop wraps the request, sends it to the company VPN gateway, and the gateway unwraps it and delivers it inside the office. The café sees only encrypted packets toward the gateway.

**Follow-up: Is a VPN the same thing as IPsec?**

No. VPN is the idea: a private path over a public network. IPsec is one way to build it. SSL VPN is another way. WireGuard is another. On a resume, “IPsec VPN” means the private path was built with IPsec.

**Follow-up: Where does IPsec sit if they mention OSI?**

At the network layer. That is why it protects every application above it. TLS protects one application connection, such as HTTPS to one website. IPsec protects the IP packets themselves.

---

## Q2. Why do companies use IPsec at all?

**Short answer**

To let remote users and branch offices use private company systems over the internet, without making those systems public and without sending the traffic in clear text.

**Explain it**

Private addresses such as `10.0.0.0/8` are not routable on the internet. Even if they were, you would not want payroll traffic crossing the internet in the clear. IPsec solves both problems. The private packet is encrypted and placed inside a new packet whose public addresses the internet does understand. The VPN gateway is the only public door.

Two patterns cover almost every interview:

| Pattern | Who connects | Everyday picture |
| --- | --- | --- |
| Remote access | One laptop to the company | You work from home or from a hotel |
| Site-to-site | One office network to another | Hyderabad office talks to the Mumbai data center all day, with no VPN client on each PC |

Your resume is the remote-access pattern on BIG-IP APM.

**Real-life example**

A 200-person office in Hyderabad and a data center in Mumbai. Buying a dedicated line between them is expensive. Each site has a firewall with a public IP. An IPsec tunnel between those two firewalls carries the office subnets. PCs in Hyderabad just send packets to `10.2.0.0/16`. They never know a tunnel exists. The firewalls do.

**Follow-up: Why not just expose the HR site on the public internet with HTTPS?**

HTTPS protects the login to that one site. It does not give the laptop an address inside the company, and it does not cover SSH, file shares, or every internal app. You would be publishing each app and managing each login page. A tunnel gives the laptop a presence on the internal network, and company firewall rules still decide what that user may reach.

---

## Q3. What is the difference between ESP and AH?

**Short answer**

ESP encrypts the packet and can also authenticate it. AH only authenticates the packet. Production VPNs use ESP.

**Explain it**

Both are IPsec protocols. They are headers added to the IP packet.

- **ESP** (Encapsulating Security Payload) is IP protocol **50**. The payload is encrypted. Someone sniffing the wire sees the outer IP addresses and an unreadable blob. With modern AES-GCM, encryption and the integrity check are one operation.
- **AH** (Authentication Header) is IP protocol **51**. It adds a checksum over the packet so tampering is detected. The data stays readable. AH also covers the IP header, so if a NAT router changes the source address, the checksum fails and the packet is dropped.

That NAT problem is why AH is almost never chosen for a VPN that has to cross the internet.

**Real-life example**

ESP is a sealed courier bag. The courier can see the from and to addresses on the bag, and cannot see the document inside.

AH is a clear plastic envelope with a wax seal. The courier can still read the document. If anyone rewrites the address, the seal breaks. Hotel Wi-Fi rewrites addresses all the time, so AH fails there.

**Follow-up: Why does almost nobody deploy AH today?**

Because the usual requirement is “hide the data,” and AH does not hide it. ESP already provides integrity. Running AH plus ESP costs extra and still breaks behind NAT. AH can make sense on a private backbone where you only need to prove packets were not modified and encryption is handled somewhere else. That case is rare in an enterprise VPN interview.

---

## Q4. What is tunnel mode, and what is transport mode?

**Short answer**

Tunnel mode wraps the entire original IP packet in a new IP packet. Transport mode encrypts the payload and keeps the original IP header. Remote-access and site-to-site VPNs use tunnel mode.

**Explain it**

In **tunnel mode** the original packet, including its private addresses (`10.50.1.20` → `10.1.1.50`), becomes the payload. A new IP header is added with public addresses (your café’s public IP → the VPN gateway’s public IP). Internet routers only look at the outer header. The gateway strips it, decrypts, and forwards the original packet inside the company.

In **transport mode** there is no second IP header. The original source and destination stay visible, and only the next layer up (TCP, UDP, or another payload) is protected. Both hosts must be the IPsec endpoints themselves. This fits “server A talks securely to server B,” not “send me into the office network.”

| | Tunnel mode | Transport mode |
| --- | --- | --- |
| What is protected | The whole original IP packet | The payload after the original IP header |
| Outer addresses | Gateway to gateway, or client to gateway | The real hosts |
| Typical use | Office VPN, branch VPN | Host-to-host on a network you already route |
| Hides internal IPs | Yes | No |

**Real-life example**

Tunnel mode is putting a letter inside a second envelope. The inner envelope says “Desk 20, Finance floor.” The outer envelope says “F5 office, Hyderabad” because the post office cannot deliver to a desk number. The receptionist (VPN gateway) opens the outer envelope and walks the inner letter to the desk.

Transport mode is locking the letter and still writing the desk address on the outside. That only works if the post office already knows how to reach that desk.

**Follow-up: Which mode did your feature use?**

Remote access uses tunnel mode. The laptop is given an internal virtual IP. Packets from that virtual IP to internal servers are encrypted and wrapped toward the BIG-IP public address. The café never sees the internal addresses.

---

## Q5. What does the laptop actually get when the VPN connects?

**Short answer**

An internal IP address, internal DNS, and a route that sends company traffic into the tunnel. The apps keep using normal IP. The VPN client and the gateway hide the encryption.

**Explain it**

After the tunnel is up, the gateway assigns the client an address from a pool, for example `10.50.1.20`. Internal servers reply to that address, and the company network routes the `10.50.1.0/24` pool back to the VPN gateway. If that return route is missing, the tunnel shows “connected” and every app times out. That is one of the first things you check.

The client also receives DNS servers and search domains, so `hr.corp.example` resolves to an internal IP instead of failing or hitting a public address.

**Split tunnel and full tunnel** come up here:

| | Split tunnel | Full tunnel |
| --- | --- | --- |
| What enters the VPN | Only company subnets | Every packet, including YouTube |
| What the user feels | Local internet stays fast | All browsing hairpins through the office |
| What security feels | The laptop can still talk to the internet and the office at the same time | The company can inspect all traffic, and the laptop is not a side door onto the internet |

**Real-life example**

Split tunnel is a company bus lane. The bus (company apps) uses the private lane. Your evening Google Maps traffic stays on the normal road.

Full tunnel is “all vehicles must enter the company gate and leave from there.” Safer for the company, slower for the user, and the office internet link carries everyone’s YouTube.

**Follow-up: Which one would you pick?**

For a company laptop that is managed and holds customer data, full tunnel is the safer default, because the machine cannot be used as a bridge from a café into the office. For a contractor who only needs one subnet, split tunnel is reasonable and much kinder on the gateway. The choice is a risk decision, and the product has to support both. The remote-access profile includes an include-list or exclude-list for this reason.

---

## Q6. How is IPsec different from SSL VPN?

**Short answer**

IPsec protects IP packets and usually runs over UDP 500 and UDP 4500. SSL VPN protects traffic inside TLS and runs over TCP 443, so it gets through networks that only allow web browsing. On BIG-IP both can present the user with a full network tunnel. The difference the user hits is whether the network lets the packets out.

**Explain it**

People mix these up because both are called “VPN” and both can end with a virtual network adapter on the laptop.

| | IPsec | SSL VPN (network-access style) |
| --- | --- | --- |
| What is encrypted | IP packets | A TLS session that carries those packets |
| What a firewall sees | UDP 500, UDP 4500, or IP protocol 50 | TCP 443, same as HTTPS |
| Handshake | IKE | TLS |
| Typical strength | Fast, often done in the kernel. UDP behaves well on lossy Wi-Fi | Passes guest networks and proxies that only allow web traffic |
| Typical weakness | Blocked by simple firewalls and by NAT that cannot handle ESP | TCP inside TCP. On a lossy network both layers retransmit and the session feels slow |

“TCP inside TCP” is worth saying carefully. The user’s HTTP connection is already TCP. SSL VPN puts that TCP inside another TCP (the TLS tunnel). When a hotel Wi-Fi link drops packets, both TCP stacks retransmit and slow down. That is called TCP meltdown. IPsec over UDP does not nest TCP, so it usually feels better once it is allowed through.

That is also why the client tries IPsec first and keeps SSL as the backup. You want the better path, and you need a path that works everywhere.

**Real-life example**

IPsec is a motorcycle courier. Fast, but some building gates only admit delivery trucks and refuse motorcycles.

SSL VPN on 443 is a delivery truck painted to look like every other web delivery. The gate lets it in. It is slower in traffic, and it gets the package there when the motorcycle is turned away.

**Follow-up: If SSL VPN works everywhere, why keep IPsec?**

Because on a normal home router IPsec is up, it uses less overhead, and it avoids TCP meltdown. Forcing every user through TLS on the gateway also costs more CPU. IPsec is the preferred path. SSL is the path that survives a locked-down network. That preference is the fallback feature on the resume.

---

## Q7. What are the building blocks I should name before I talk about the handshake?

**Short answer**

ESP to protect packets, IKE to agree how, a security association to remember the agreement, and a policy that says which traffic must enter the tunnel.

**Explain it**

Use these four words and you sound like you have configured it, not just read a definition.

1. **ESP** carries the user data.
2. **IKE** (Internet Key Exchange) runs first, on UDP 500. It agrees algorithms, does Diffie-Hellman, and checks identity. No user data moves during IKE.
3. **Security Association (SA)** is the result. It is one direction: “packets from this peer, with this SPI, are decrypted with this key.” The reverse direction is a second SA.
4. **Policy** decides what to do with a packet before any encryption: protect it in the tunnel, let it pass in the clear, or drop it. On paper this is the Security Policy Database. The live keys sit in the Security Association Database.

Two more words that show up the moment something breaks:

- **SPI** (Security Parameter Index) is a number in the ESP header. The gateway may have thousands of tunnels. The SPI tells it which key to use for this packet. Think of it as a locker number, not as a secret.
- **Traffic selector** is the definition of “interesting traffic”: source subnet, destination subnet, and sometimes protocol and port. If the two sides disagree on this, IKE can succeed and the data tunnel still never comes up.

**Real-life example**

Two offices agree to exchange mail.

- IKE is the phone call where they agree to use a particular lock and exchange key halves.
- The SA is the written note: “lock type, key, locker number 42, valid until 6 pm.”
- The traffic selector is the rule “only mail addressed to the other office goes in this bag.” A letter to a customer does not.
- The SPI is locker 42 painted on the bag, so the receiving mailroom opens it with the matching key.

**Follow-up: Why is an SA one-way?**

Because each direction has its own key and its own sequence numbers. In practice you always create them as a pair. When you debug, you check both directions. A tunnel can be up one way and black-hole the return traffic.

---

### Checkpoint

You should be able to answer these without notes before you move on:

1. What four security properties does IPsec give you?
2. Why ESP and not AH for a remote user?
3. Why tunnel mode for a laptop on hotel Wi-Fi?
4. Why try IPsec before SSL VPN?
5. What is an SA, and what is an SPI?
