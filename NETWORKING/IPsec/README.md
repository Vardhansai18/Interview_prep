# IPsec VPN — Interview Questions

Practice these out loud. Each question has a short answer you can start with, a fuller explanation, a real-life example, and the follow-up an interviewer usually asks next.

Your resume stories sit in parts 3 and 4. Parts 1 and 2 are what they ask before they let you reach those stories.

To see the same story as a clickable packet, run the [demo](demo/README.md).

| Part | What it covers | File |
| --- | --- | --- |
| 1 | What IPsec is, and what problem it solves | [Basics](01-basics.md) |
| 2 | How a tunnel is actually built | [Building the tunnel](02-building-the-tunnel.md) |
| 3 | NAT-T, and why you fall back to SSL VPN on 443 | [NAT-T and SSL fallback](03-nat-t-and-ssl-fallback.md) |
| 4 | EAP-MSCHAPv2, and why you skipped per-laptop certificates | [Authentication](04-authentication-eap.md) |
| 5 | Extra follow-ups, failures, and a mock round | [Follow-ups](05-follow-ups-troubleshooting.md) |

---

## How to use this before an interview

1. Look at the picture under the question and name every label before you read the answer. Eight pictures are short animations. Each frame stays up for about two seconds.
2. Answer the short version without looking.
3. Then tell the real-life example in your own words. Interviewers remember the example.
4. Only after that, check the follow-up. If you can answer the follow-up, you own the topic.
5. On the day, re-read only the [60-second resume pitch](#60-second-resume-pitch) and the [one-page card](#one-page-card) at the bottom of this file.

---

## 60-second resume pitch

Say this when they ask “Walk me through the IPsec work on your resume.”

> I worked on remote-access IPsec for F5 BIG-IP APM. IPsec encrypts IP packets so a laptop on hotel Wi-Fi can reach internal apps as if it were in the office. I owned the configuration UI and the backend schema that the rest of the feature was built on: IKE settings, traffic selectors, proposals, and the remote-access profile.
>
> Two user problems sat on top of that. First, a lot of networks block IPsec. Guest Wi-Fi often allows only TCP 443, and some routers cannot do NAT traversal, so UDP 4500 never gets through. The client tries IPsec first, and if the path is blocked it falls back to SSL VPN on 443, which looks like normal HTTPS. The user still gets a tunnel.
>
> Second, giving every laptop its own certificate does not scale. I added EAP-MSCHAPv2 so the gateway proves itself with a certificate, and the user signs in with their directory username and password inside the already encrypted IKE channel. IT stops shipping certificates to every laptop, and one lost laptop is a disabled account, not a revoked certificate.

If they nod, they will ask one of these next. Know which file answers it.

| They say | You open |
| --- | --- |
| “What is IPsec in one minute?” | [Q1](01-basics.md#q1-what-is-ipsec) |
| “How is the tunnel created?” | [Q8](02-building-the-tunnel.md#q8-walk-me-through-how-an-ipsec-tunnel-comes-up) |
| “Why would IPsec fail on hotel Wi-Fi?” | [Q14](03-nat-t-and-ssl-fallback.md#q14-why-does-ipsec-break-behind-nat) |
| “Why fall back to SSL instead of fixing IPsec?” | [Q17](03-nat-t-and-ssl-fallback.md#q17-why-fall-back-to-ssl-vpn-on-port-443) |
| “Why not client certificates?” | [Q19](04-authentication-eap.md#q19-why-not-just-put-a-certificate-on-every-laptop) |

---

## One-page card

| Term | One line you can say |
| --- | --- |
| IPsec | A set of protocols that encrypts and authenticates IP packets. |
| ESP | The protocol that encrypts the packet. Protocol number 50. This is what production VPNs use. |
| AH | Authenticates the packet and does not encrypt it. Protocol 51. Rare today. |
| Tunnel mode | Wraps the whole original packet in a new IP header. This is the VPN. |
| Transport mode | Encrypts the payload and keeps the original IP header. Host-to-host, not a typical office VPN. |
| IKE | The handshake that agrees algorithms, exchanges keys, and proves identity. UDP port 500. |
| IKEv2 | The current version. Fewer messages, works better with NAT, built-in liveness checks, supports EAP. |
| SA | A one-way agreement: this peer, this key, this algorithm. A tunnel needs two, one each way. |
| SPI | A number in the ESP header that tells the receiver which key to use. |
| Child SA / Phase 2 | The actual data tunnel, built after the handshake is secure. |
| NAT-T | Wraps ESP inside UDP 4500 so a NAT router can pass it. |
| SSL VPN fallback | If UDP 500 and 4500 are blocked, carry the same remote-access session over TLS on TCP 443. |
| EAP-MSCHAPv2 | Username and password proof inside IKEv2, so each laptop does not need its own certificate. |
| PFS | The data tunnel uses its own Diffie-Hellman secret, so a stolen long-term key does not reveal old traffic. |

Ports and numbers interviewers expect you to know:

- IKE: UDP **500**
- NAT-T: UDP **4500**
- ESP: IP protocol **50**
- AH: IP protocol **51**
- SSL VPN fallback: TCP **443**
