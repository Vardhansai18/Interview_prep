# Part 5 — Follow-ups, failures, and a mock round

Use this after Parts 1–4. These are the questions that arrive once the interviewer believes you have actually been near a tunnel.

---

## Q24. The tunnel shows up. The application still fails. How do you debug it?

**Short answer**

Decide whether the handshake is down, the data path is down, or only large packets are down. Those three have different fixes. Then check one direction at a time.

**Explain it**

Work top to bottom. Stop at the first layer that is wrong.

**1. Is the path even open?**

From the client network, can UDP 500 and UDP 4500 reach the gateway? Can TCP 443? A timeout on 500 and 4500 with 443 open is the fallback case, not a bug in the cipher suite.

**2. Did IKE succeed?**

Read the gateway log before you touch a packet capture.

| Log hint | Meaning | Fix |
| --- | --- | --- |
| No proposal chosen | No common algorithm bundle | Align IKE and IPsec proposals. Look for a stale 3DES or SHA-1 entry |
| Authentication failed | Password, MFA, certificate, or clock | Stay on this path. Do not fall back. Check the access policy result and the certificate name and dates |
| Traffic selector mismatch | The two sides disagree on subnets | Make the selectors mirrors |
| NAT-T disabled, peer is behind NAT | One side is speaking raw ESP | Turn NAT-T on for remote access |

**3. Is the child SA up in both directions?**

There are two SAs. Confirm both have packets, not just one. If the outbound count grows and the inbound count stays at zero, the return path is the problem.

**4. Is the inner network correct?**

- Did the client get a virtual IP?
- Does the company route that pool back to this gateway?
- Did DNS return an internal address?
- Does the firewall policy after decryption allow this user to this server?

A missing return route is the classic “connected, zero applications” ticket.

**5. Only big packets fail?**

Ping with a 64-byte payload works. Ping with 1400 bytes fails. That is MTU. Lower the tunnel MTU or clamp TCP MSS. ESP plus a UDP 4500 header often pushes you to about 1350–1400 bytes.

**Real-life example**

A parcel service says the shipment is “handed to the airline” (IKE is up). The box never arrives. You check the airway bill (the SA), then whether the destination warehouse knows your flat number (the virtual IP and the return route), then whether they refused the box for being too big (MTU). You do not start by repainting the van.

**Follow-up: What do you look for in a packet capture?**

- UDP 500, then a move to UDP 4500: NAT-T is working.
- Protocol 50 on the public side: NAT-T is off. Expect home users to fail.
- IKE retries with no answer: the network is dropping it. Fallback territory, if 443 is open.
- ESP packets only in one direction: routing or a firewall on the return path.
- Lots of small ESP packets and stalled TCP: suspect MTU and look at TCP retransmissions inside a decrypted capture.

You do not need to decode ESP by hand. You need to say which of those patterns you would look for, and what each one means.

---

## Q25. What is MOBIKE, and when would a laptop use it?

**Short answer**

MOBIKE lets IKEv2 update the client’s address when the laptop moves from Wi-Fi to mobile data, without tearing down the login and starting EAP again.

**Explain it**

A phone switches from office Wi-Fi to LTE and its public IP changes. Without MOBIKE the old NAT mapping is dead, DPD eventually kills the SA, and the user goes through the full handshake again. With MOBIKE the client sends an update from the new address, proves it still owns the existing IKE SA, and the gateway sends future ESP packets to the new address.

This is a remote-access feature. A site-to-site tunnel between two data centers has stable addresses and does not need it.

**Real-life example**

You are on a customer-support call and you walk out of the building. Your phone number stays the same from the agent’s point of view if the call can be updated to the new tower. Hanging up and passing the security questions again is the full IKE restart. MOBIKE is the network handing the same call to the new tower.

**Follow-up: What fails if the client roams and MOBIKE is not there?**

The tunnel looks up for a while, then DPD expires it, then the client reconnects. Users describe this as random disconnects on a commute. Check whether the client changed IP at the same moment. That correlation is the diagnosis.

---

## Q26. What is the difference between policy-based and route-based VPN?

**Short answer**

Policy-based VPN encrypts whatever matches a traffic selector. Route-based VPN creates a virtual interface and encrypts whatever the routing table sends into that interface.

**Explain it**

**Policy-based.** The SPD says “packets from `10.1.0.0/16` to `10.2.0.0/16` get encrypted to peer X.” There is no interface in the routing table. Adding a new subnet means editing selectors on both ends. Dynamic routing protocols do not have an interface to sit on. Selectors that are not perfect mirrors fail in confusing ways. This is the traditional IPsec model, and it is what the traffic-selector object in your schema represents.

**Route-based.** The tunnel is a virtual interface (often called a VTI). Routes, static or BGP, point company prefixes at that interface. Whatever is routed in gets encrypted. Adding a subnet is a routing change, which network teams already know how to review. This is the model most new site-to-site designs want.

Remote access is closer to a pool plus a set of routes pushed to the client. You can explain it without insisting on the phrase VTI. The client installs routes for the split-tunnel list, and those routes point at the virtual adapter.

**Real-life example**

Policy-based is a courier rule: “envelopes addressed to Mumbai go in the red bag.” If you open a new office in Pune, you must rewrite the rule on both ends.

Route-based is a road. You put up a sign that says “Pune, turn here.” The trucks (routes) follow the sign. The road does not need a new rule for every destination. It needs a sign.

**Follow-up: Why did GRE show up next to IPsec in older designs?**

Routing protocols and multicast needed an interface, and classic policy-based IPsec did not give them one. Engineers wrapped the traffic in GRE, which is a virtual interface, and then encrypted the GRE packets with IPsec. Route-based VTI removed the reason for that extra layer in many designs. If you see GRE over IPsec in a network, it is usually that history, or a multicast requirement.

---

## Q27. How do anti-replay and SA lifetimes limit the damage of a stolen key?

**Short answer**

Anti-replay stops an attacker from re-sending a packet you already accepted. Lifetimes throw the keys away on a schedule, so a stolen data key opens only a window, not the permanent history of the tunnel.

**Explain it**

Every ESP packet carries a sequence number. The receiver remembers a window of recent numbers. A repeat of an old number is dropped. That stops “capture a ‘create user’ packet and send it again.” It does not stop an attacker who has the key and can build a fresh packet with a new sequence number. That is why lifetimes and PFS exist.

An IKE SA might live for hours. A child SA might live for less, or for a byte count. When the child lifetime hits, the peers build new data keys, ideally with a new Diffie-Hellman (PFS). The old key cannot open the new hour, and the new key cannot open the old hour.

Say a concrete pair if they ask for numbers: IKE lifetime 8 hours, child SA 1 hour, PFS group 19. The exact numbers are local policy. The relationship is the point. The child SA expires sooner than the IKE SA, and the user does not log in again at every rekey.

**Real-life example**

A cinema ticket has a seat, a date, and a hologram sticker. Anti-replay is the door scanner rejecting a photo of a ticket that already went through. The lifetime is the date printed on the ticket. Tomorrow the sticker is worthless even if someone photographs it perfectly. PFS is printing tomorrow’s tickets from a new plate, so stealing today’s plate does not print yesterday’s tickets either.

**Follow-up: What is a rekey storm?**

All tunnels were configured with the same lifetime and came up together, for example after a gateway reboot at 9 am. They all try to rekey at 10 am. CPU spikes and some handshakes time out. Jitter the lifetimes, or let them be based on traffic as well as time, so they do not synchronise. Worth mentioning if they ask what goes wrong at scale.

---

## Q28. What would you monitor in production?

**Short answer**

Whether tunnels come up, which path they used, why they fail, and whether the gateway is about to run out of CPU or addresses. A green “IKE is running” check is not monitoring.

**Explain it**

| Signal | Why you care |
| --- | --- |
| IKE failures by reason | Tells you if you are looking at bad passwords, proposal mismatch, or timeouts. These are different bugs |
| Fallback rate to SSL | A sudden jump means a network path started dropping UDP, or a middlebox change. A slow jump means more users on hostile networks |
| Active SAs and setup rate | Capacity. A rekey storm shows up here |
| Address-pool usage | When the pool is exhausted, authentication succeeds and the session still fails. Users say “VPN is broken” |
| Certificate expiry on the gateway | One expired gateway certificate fails every EAP user at once |
| Decrypt failures and anti-replay drops | Can be attack traffic, or a peer with a broken SA after failover |
| CPU during ESP | IPsec is CPU-heavy if you are not using hardware crypto. AES-GCM is the algorithm you wanted partly for this reason |

**Real-life example**

A toll plaza does not only check that the gates exist. It watches which gate people use (IPsec versus SSL fallback), how often a card is declined and why, whether the car-park is full (address pool), and whether booth 4 is about to have its card reader certificate expire. The fallback rate is your early warning that a carrier or a guest-Wi-Fi vendor changed a firewall.

**Follow-up: Users say it is slow only on SSL fallback. Is that expected?**

It can be. They are on TCP 443, often on a lossy guest network, with TCP inside TCP. Confirm they really fell back, then look at loss and retransmissions before you resize the gateway. If IPsec users are slow too, look at gateway CPU and MTU instead. The path label you log at connect time is what makes this a five-minute diagnosis instead of a guess.

---

## Q29. How does failover work if the gateway reboots?

**Short answer**

The SAs live in memory. A reboot deletes them. Clients detect the dead peer and build a new tunnel to the same virtual address, or to a second gateway. Users may notice a short reconnect. They should not need a new account or a new configuration.

**Explain it**

IKE state is not something you want to pretend survived a crash unless you have a sync mechanism between two gateways. In an active/standby pair, the honest design is:

- Both gateways can present the same virtual IP, or clients have a list.
- When the active gateway dies, DPD on the client fails.
- The client starts a new IKE_SA_INIT to the address that now answers.
- The user authenticates again if the access-policy session was only on the dead gateway. Session sync, if the product has it, saves them from typing the password twice.
- The virtual IP they get might change unless the pool state is shared. If it changes, existing TCP connections inside the tunnel break, and new ones work. Say that limitation plainly. It is normal.

**Real-life example**

The reception desk loses power. Your meeting does not continue at the empty desk. You walk to the second desk (the standby), show your badge again, and get a new visitor sticker. Appointments already in progress may need to be redialed. New ones work. Promising that a TCP download survives the power loss is how you get caught in the interview. Say the tunnel is rebuilt and new connections succeed.

**Follow-up: What breaks if both gateways think they are active?**

Split brain. Two gateways answer IKE, or the return route for the virtual-IP pool points at the wrong one. Clients flap, or they connect and receive no replies. The fix is a real failover protocol with one owner of the virtual IP, not two boxes configured identically and left to chance.

---

## Q30. Mock round — say these out loud in one sitting

Time box: 20 minutes. Cover the short answer only. Then pick two follow-ups you stumbled on and redo them with the example.

**Basics**

1. What is IPsec, in four properties?
2. ESP or AH for a laptop in a hotel, and why?
3. Tunnel mode or transport mode, and why?
4. What does the client get once it is connected?
5. Why is IPsec preferred and SSL VPN still required?

**Handshake**

6. Walk IKE_SA_INIT, IKE_AUTH, and the child SA.
7. What does Diffie-Hellman fail to prove?
8. What is PFS?
9. Name the objects in the configuration model.

**Resume**

10. Why does ESP suffer behind NAT, and what does NAT-T change?
11. When do you fall back to TCP 443, and when must you refuse to?
12. Tell the hotel packet story.
13. Why EAP-MSCHAPv2 instead of a certificate on every laptop?
14. Where in the handshake does EAP run, and why is the gateway certificate mandatory?

**Debug**

15. Connected, and no application works. What do you check?
16. Small ping works, large ping fails. What is that?
17. What would a jump in SSL-fallback rate tell you?

---

## Likely rapid-fire follow-ups

Keep these to two or three sentences. Long answers here sound rehearsed.

**Why UDP and not TCP for IKE?**
IKE is a short exchange, and the user’s own TCP already provides retransmission for applications. UDP avoids nesting TCP inside TCP. The cost is that UDP is easy for a guest network to block, which is why TCP 443 exists as the fallback.

**What is an SPI? Is it secret?**
It is a 32-bit index in the ESP header that selects the SA. It is a locker number. The key is the secret. The SPI is how you find the key.

**Can one IKE SA have multiple child SAs?**
Yes. One login can protect several selector pairs, or you rekey the child SA and briefly have the old and the new. The IKE SA is the management channel. Child SAs carry data.

**What is split tunneling’s real risk?**
The laptop is on the company network and on the internet at the same time. Malware on the laptop can use that. Full tunnel removes the direct internet path. It costs gateway bandwidth and breaks the local printer unless you exclude it.

**Why AES-GCM?**
It encrypts and authenticates in one pass, and CPUs have hardware support for it. It is the default you offer in the UI. You do not offer 3DES or MD5 in that default.

**What does the café attacker see?**
The gateway’s public IP, the hotel’s public IP, UDP 4500, packet sizes, and timing. They do not see the internal addresses, the URL, or the EAP username. Those are inside the encrypted handshake or the ESP payload. Traffic analysis is still possible: they can see that you use a VPN, and roughly how much you send.

**Site-to-site in one minute, so they know you can separate it from your project.**
Two firewalls, stable public IPs, a pre-shared key or a certificate, mirrored traffic selectors, tunnel mode, no user login, no SSL fallback, no EAP. NAT-T still matters if either firewall is behind NAT. Your resume is the other design: many laptops, EAP, NAT-T, and a 443 fallback.

**What would you improve next?**
EAP-TLS as an option for teams that are ready for device certificates. MFA already in the access policy for everyone else. MOBIKE so roaming does not force a full login. Stricter UI defaults so a new tunnel cannot be saved with DH group 2. Alerting on gateway certificate expiry and on a sudden rise in SSL fallback.

---

### Checkpoint

If you can do the mock round in Q30 once without opening the other files, you are ready to put IPsec on the table in an interview. If a follow-up in the rapid-fire section takes more than a minute, reopen the matching part and practise only that story.
