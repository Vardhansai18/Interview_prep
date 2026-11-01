# Part 4 — Authentication and EAP-MSCHAPv2

This is the resume bullet:

> Designed and implemented EAP-MSCHAPv2 authentication for IPsec VPN tunnel establishment on F5 BIG-IP APM, eliminating per-client PKI certificate provisioning.

The interviewer is checking two things. Do you know where the password sits in the handshake, and can you say the security tradeoff out loud without being pushed into it.

---

## Q19. Why not just put a certificate on every laptop?

**Short answer**

A certificate per laptop is strong, and it is operationally expensive. Every new hire, re-image, contractor, and lost laptop needs issuance, install, renewal, and revocation. EAP-MSCHAPv2 lets the user sign in with the directory account they already have. The gateway still uses a certificate. The laptop does not need its own.

**Explain it**

There are three common ways for an IPsec peer to prove identity. Name the tradeoff, or the answer sounds like you picked a password because it was easy.

| Method | How it feels | Where it hurts |
| --- | --- | --- |
| Pre-shared key | One secret configured on both sides | A remote-access group key lives on every laptop. One leaked laptop exposes everyone. You cannot revoke one user. Fine for a site-to-site link between two firewalls you control. Poor for thousands of users |
| Certificate on the client | Each laptop has a unique keypair. Stealing one password is not enough | IT runs a PKI. Certificates expire, images get rebuilt, users work offline on the day of enrollment, and a lost laptop needs revocation before the cert expires |
| EAP username and password | The person signs in with their company account. Disable the account and the laptop loses access | Weaker than a device certificate if the password can be phished. You pair it with MFA. The password exchange has to sit inside an encrypted channel, and the client has to trust the gateway certificate first |

The resume claim is the middle column of that last row. You removed the per-client PKI step. You did not remove cryptography, and you did not remove the gateway certificate.

APM matters in this answer. The access policy is the place that already knew how to talk to Active Directory, check group membership, and demand a second factor. EAP-MSCHAPv2 is how IKEv2 hands the user’s identity to that policy. The IPsec tunnel and the SSL VPN can share it, which is also why the fallback in Part 3 does not invent a second login system.

**Real-life example**

A client certificate is a metal office key cut for one person. It is excellent until they lose it, change cities, or get a new laptop. Security then has to collect the old key and cut a new one. That is PKI provisioning.

EAP-MSCHAPv2 is the ID-badge plus the reception desk. The building (the gateway) has a certificate the badge reader can verify, so you know you are at the real office and not a fake door. The person types the same employee credentials they use every morning. When they resign, HR disables the account. You do not tour the country collecting metal keys.

**Follow-up: Is a password as strong as a client certificate?**

No, and you should say that before the interviewer does. A certificate proves the device holds a private key. A password proves a human knows a secret, and humans reuse secrets and type them into lookalike prompts. The compensating controls are:

- The gateway authenticates with a certificate the client actually validates.
- The EAP exchange is inside the encrypted IKE SA, so the café cannot see the challenge or the response.
- The access policy adds MFA.
- Account lockout and disable already exist in the directory.

For a high-security device, client certificates or certificates plus EAP are still the stronger design. For a large workforce, EAP-MSCHAPv2 plus MFA is the design that ships and stays operable. Your job in the interview is to show you chose it with that tradeoff open, not that you think passwords are magic.

---

## Q20. What is EAP, and what is MSCHAPv2?

**Short answer**

EAP is a framework for “ask the user to prove who they are,” with room for many methods. MSCHAPv2 is one method: a challenge and a response based on the password. The password itself is never sent.

**Explain it**

**EAP** (Extensible Authentication Protocol) does not hash anything by itself. It carries a method. IKEv2 knows how to carry EAP inside IKE_AUTH. The VPN gateway can then run EAP-MSCHAPv2, EAP-TLS, or another method without changing IKE.

**MSCHAPv2** (Microsoft Challenge-Handshake Authentication Protocol version 2) is a username-and-password method that Active Directory environments already understand.

The exchange, said in plain language:

1. The gateway sends a random challenge.
2. The client combines that challenge with its own random value and with a hash of the user’s password, and sends a response plus the username. The password does not travel.
3. The gateway checks that response with the directory (directly, or through RADIUS to something like NPS).
4. The gateway sends back its own proof, so the client knows the gateway knows the same password. This is the “mutual” part of MSCHAPv2.
5. Both sides derive keying material. IKEv2 uses that material to finish authenticating the IKE SA.

A capture of this exchange, if it were ever visible, can be attacked offline. That weakness is old and real. Inside this design it is not visible on the café wire, because it happens after IKE_SA_INIT. The Diffie-Hellman keys already encrypt the IKE channel. Say the weakness anyway. It shows you did not treat MSCHAPv2 as modern cryptography. You treated it as a directory-compatible proof, protected by the tunnel setup around it.

**Real-life example**

The door guard does not ask you to shout your PIN across the lobby. He slides a random number across the counter (the challenge). You do a calculation only someone who knows the PIN can do, and you slide the result back. He checks the result against what the office has on file. A person listening in the lobby sees two numbers and still does not have the PIN. That lobby is safe only because you already confirmed the guard works for your company. On the VPN, that confirmation is the gateway certificate, checked before EAP starts.

**Follow-up: Why MSCHAPv2 and not “just send the password inside the encrypted IKE channel”?**

Because the directory stores a hash, and RADIUS servers in a Windows environment expect the MSCHAPv2 challenge-response. Sending the raw password would mean the gateway sees it and you would no longer fit the AAA servers companies already run. MSCHAPv2 is the method those servers already accept. EAP is the slot IKEv2 provides to plug that method in.

---

## Q21. Where exactly does EAP sit in the IKEv2 handshake?

**Short answer**

After Diffie-Hellman, inside IKE_AUTH. The gateway proves itself with a certificate first. Then EAP runs. Then a child SA is created. User packets wait until all of that succeeds.

**Explain it**

Say this sequence slowly. It is the most common place people bluff and get caught.

1. **IKE_SA_INIT.** Algorithm agreement and Diffie-Hellman. Both sides can encrypt the rest of the handshake. The user has not logged in.
2. **First IKE_AUTH from the client.** The client sends its identity and the child-SA proposal. It does not send a finished password proof yet.
3. **Gateway replies.** The gateway sends its certificate and proves it holds the matching private key. It starts EAP.
4. **EAP rides inside further IKE_AUTH messages.** Challenge, response, success or failure. APM’s access policy is what checks the user against the directory and can insert MFA here.
5. **Client sends a final AUTH payload** built from the EAP keying material. This binds the login to this handshake, so the messages cannot be replayed into another session.
6. **Gateway sends the child SA answer.** Traffic selectors and ESP keys are now live. The virtual IP is assigned. Applications can flow.

If step 3 is skipped, the user is doing EAP with whoever answered the IKE packet. An attacker on the path can finish Diffie-Hellman with the laptop, collect the MSCHAPv2 response, and crack it offline. Certificate validation is the control that closes that hole. The client checks the name (`vpn.company.com`), the expiry, and the chain up to a CA it trusts.

**Real-life example**

You call your bank. The call is on a private line first (IKE_SA_INIT). The bank officer quotes a known branch ID and you recognise it (server certificate). Only then do they ask the security question (EAP). You would not answer the security question on a call you placed to a number you have not verified. The VPN client has the same rule, and the UI and schema enforce it: choosing EAP requires a server certificate on the gateway.

**Follow-up: What does the client check on that certificate?**

- The chain ends at a CA in the client’s trust store. Company devices are given that CA. A random public CA is not automatically the right trust anchor if you want only your gateway.
- The name in the certificate matches the gateway hostname the user connected to.
- The certificate is inside its validity dates. Large clock skew on a laptop looks like an expired or not-yet-valid certificate and fails the tunnel in a way that confuses everyone.
- Revocation, if the deployment has a CRL or OCSP that clients can actually reach. A revocation check that needs the VPN to be up before it can download the CRL is a circular trap. Mention it if they push on PKI. It is one more reason device-wide client certificates are operationally heavy.

---

## Q22. How does this remove work for the admin?

**Short answer**

Joiner, mover, and leaver events stay in the directory. Nobody cuts a certificate for a laptop, pushes it, tracks its expiry, or revokes it on a Friday night when a laptop is stolen.

**Explain it**

Tell the operational story in three scenes. Interviewers who have run a VPN recognise these scenes immediately.

**New hire.** IT enables the account and adds them to the VPN group. They install the client, type their username and password, pass MFA, and get a tunnel. No ticket to the PKI team.

**Lost laptop.** The account is disabled, or the password is reset. The next IKE_AUTH fails. You do not depend on a revocation list reaching every gateway before the thief connects.

**Re-image.** A laptop is rebuilt from a standard image that has the VPN client and the company CA. There is no unique certificate to back up and restore.

What the admin still does:

- One certificate on the gateway, monitored for expiry. This one is worth paging on.
- The CA that signed it, installed on company laptops once, as part of the image.
- The access policy: which group may connect, whether MFA is required, which networks each group gets.
- NAT-T left on, and SSL fallback left on, so the auth work is not wasted when the user’s network is hostile.

**Real-life example**

A courier company can issue a unique metal key to every driver and keep a board of 10,000 keys. Every lost key is a locksmith visit. Or it can give every driver the same style of staff login at the gate, backed by the HR list that already exists. Firing a driver is an HR update. EAP-MSCHAPv2 is that gate. The building’s own certificate is the one locksmith job you keep.

**Follow-up: What did the access policy decide, beyond the password?**

The password check is only the front door. The policy also decides:

- Is MFA required for this group?
- Is this user in the group allowed to use VPN?
- Which address pool do they get?
- Which split-tunnel subnets do they get? Finance and engineering should not automatically receive the same routes.
- Is the device posture acceptable, if you have a check for disk encryption or a minimum OS version?

Those decisions belong to APM either way. EAP is the handoff from IKE into that policy. When you describe the schema, the remote-access profile points at an access policy name. It does not hard-code a password check inside the IPsec object.

---

## Q23. What attacks should you bring up yourself?

**Short answer**

A fake gateway, a stolen password, a shared pre-shared key, and a downgrade to weak algorithms. Each one has a control you can name.

**Explain it**

Volunteer this table. It turns “we used passwords” into “we knew the risks.”

| Attack | What happens | What you say you did |
| --- | --- | --- |
| Fake gateway | Attacker runs IKE, completes Diffie-Hellman, and collects the EAP exchange | Client validates the gateway certificate before EAP. EAP is mandatory with a server certificate in the schema |
| Stolen or phished password | Attacker logs in as the user | MFA in the access policy. Disable the directory account. Passwords are not a shared VPN-wide secret, so one user is not every user |
| Group pre-shared key | One laptop image leaks the key that connects anyone | Remote access uses EAP, not a group PSK. PSK remains a site-to-site option between two firewalls |
| Weak crypto downgrade | Peer offers 3DES or DH group 2 and someone accepts it | The default proposal is AES-GCM and DH group 19 or 20. Legacy algorithms are not in the default set |
| Replay of an old ESP packet | Attacker resends a captured packet to repeat an action | ESP sequence numbers. The gateway drops a sequence it has already accepted |
| Recording today’s traffic and stealing the certificate next year | Attacker decrypts the archive | PFS on the child SA. The certificate only proved identity. It was not the data key |

**Real-life example**

A fake gateway is a person in a rented uniform standing in front of a copied door. Checking the building certificate is asking to see the company ID on the door before you answer the security question. MFA is a second lock on your own flat, so a stolen PIN is not enough. PFS is shredding yesterday’s meeting-room keys so a copied master badge next year cannot open last year’s rooms.

**Follow-up: Could you have used EAP-TLS instead?**

Yes. EAP-TLS is certificate authentication carried inside EAP. It is the right upgrade when the company is ready to run device certificates, and the schema can allow it as another EAP method beside MSCHAPv2. You still keep the server certificate and the access policy. The resume work was the method that removed the need for those device certificates. Knowing EAP-TLS by name shows the password method was a choice.

---

### Checkpoint

1. Why is a group pre-shared key a bad fit for 10,000 laptops?
2. When does EAP run, relative to Diffie-Hellman and the child SA?
3. Why is the gateway certificate still required?
4. What does disabling a directory account do that certificate revocation also tries to do?
5. Name three attacks and the control for each, without looking at the table.
