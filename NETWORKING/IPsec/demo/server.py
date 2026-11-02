#!/usr/bin/env python3
"""Teaching demo. It does not create a real VPN. It only decides how a sample packet would look."""

import json
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent / "static"

CAST = [
    {"id": "laptop", "name": "Laptop", "addr": "10.20.30.5", "note": "Café Wi-Fi"},
    {"id": "hotel", "name": "Hotel NAT", "addr": "49.37.10.8", "note": "One public IP"},
    {"id": "gateway", "name": "BIG-IP", "addr": "203.0.113.10", "note": "VPN gateway"},
    {"id": "hr", "name": "HR server", "addr": "10.1.1.50", "note": "Inside the office"},
]

GLOSSARY = [
    {"term": "VPN", "say": "The result you want: a private path into the office over a public network."},
    {"term": "IPsec", "say": "The lock for IP packets. IKE agrees the keys. ESP hides the packet. Layer 3."},
    {"term": "IPsec VPN", "say": "A VPN built with IPsec. Same desk, IPsec lock. SSL on 443 is only the backup door."},
    {"term": "SSL VPN", "say": "The same private desk, with the inner packet carried inside TLS on TCP 443."},
    {"term": "Tunnel mode", "say": "The whole original IP packet goes inside a new IP packet. This is the office VPN."},
    {"term": "Transport mode", "say": "Only the payload is locked. The original IP header stays visible. Not a typical office VPN."},
    {"term": "ESP", "say": "Encapsulating Security Payload, IP protocol 50. Encrypts the packet and checks it was not edited."},
    {"term": "AH", "say": "Authenticates only. The data stays readable, and NAT breaks it. Production VPNs use ESP."},
    {"term": "SPI", "say": "The locker number in the ESP header. It picks the key. It is not the key."},
    {"term": "Sequence number", "say": "Parcel number. A repeat of an old number is dropped."},
    {"term": "Integrity check", "say": "The tamper sticker. If it does not match, the gateway throws the packet away."},
    {"term": "IKE", "say": "The handshake before user data. It runs on UDP 500."},
    {"term": "IKE_SA_INIT", "say": "Agree algorithms and do Diffie-Hellman. The handshake becomes encrypted. No login yet."},
    {"term": "IKE_AUTH", "say": "Gateway shows its certificate. The user proves identity, here with EAP-MSCHAPv2."},
    {"term": "Child SA", "say": "The data tunnel. ESP keys, traffic selectors, and the virtual IP. User packets start here."},
    {"term": "Diffie-Hellman", "say": "Both sides build a shared secret. The private numbers never cross the network. It does not prove who the other side is."},
    {"term": "SA", "say": "A one-way agreement: this peer, this key, this SPI. A tunnel needs two."},
    {"term": "Virtual IP", "say": "10.50.1.20, an office address given to the laptop. HR replies to this address."},
    {"term": "NAT", "say": "The hotel rewrites the laptop's private address to one public address."},
    {"term": "NAT-T", "say": "Wrap ESP inside UDP 4500 so the hotel has a port number to deliver replies."},
    {"term": "UDP 500", "say": "IKE, before NAT is detected."},
    {"term": "UDP 4500", "say": "IKE and ESP after NAT-T."},
    {"term": "Protocol 50", "say": "Raw ESP, used when there is no NAT."},
    {"term": "TCP 443", "say": "SSL VPN. Looks like HTTPS, so guest Wi-Fi usually allows it."},
    {"term": "EAP-MSCHAPv2", "say": "Username and a challenge-response. The password itself is never sent. It runs inside encrypted IKE."},
    {"term": "PFS", "say": "The child SA does its own Diffie-Hellman, so a stolen certificate later cannot open yesterday's packets."},
    {"term": "Traffic selector", "say": "Which subnets must enter the tunnel. The two sides must mirror each other."},
]


def layer(name, tone, lines, note):
    return {"name": name, "tone": tone, "lines": lines, "note": note}


STORY = [
    {
        "id": "cast",
        "part": "Start here",
        "title": "One café, one HR site",
        "say": "Every mode in this demo uses the same people. Only the wrapper around the HR request changes.",
        "visual": "cast",
        "cafe": "The café can see whatever is written on the outside of the packet.",
        "gateway": "The gateway can open a wrapper only when it has the matching key.",
        "terms": ["VPN", "IPsec", "IPsec VPN", "SSL VPN"],
    },
    {
        "id": "no-vpn",
        "part": "1 · How a VPN becomes necessary",
        "title": "No tunnel. The request is a postcard.",
        "say": "The laptop sends the HR request directly. The address 10.1.1.50 is private, so the internet cannot deliver it. Anyone on the café Wi-Fi can also read the request.",
        "visual": "packet",
        "layers": [
            layer("IP header", "slate", ["Source 10.20.30.5", "Destination 10.1.1.50"], "Both addresses are visible."),
            layer("HTTP", "red", ["GET /hr/salary", "Cookie: session=open"], "The letter is readable."),
        ],
        "cafe": "Reads the HR URL and the cookie.",
        "gateway": "Never receives the packet. The public internet has no route to 10.1.1.50.",
        "terms": ["VPN"],
    },
    {
        "id": "vpn-idea",
        "part": "1 · What VPN means",
        "title": "VPN is the desk, not the lock.",
        "say": "A VPN is the result: from the café, you still get a desk inside the office. The word does not say whether the lock is IPsec, TLS, or something else.",
        "visual": "compare",
        "cards": [
            {"name": "VPN", "tone": "blue", "lines": ["The result", "A private desk in the office", "HR thinks you are inside"]},
            {"name": "Not chosen yet", "tone": "amber", "lines": ["The lock", "IPsec is one lock", "TLS is another lock"]},
        ],
        "cafe": "Will see only the outside of whatever lock you choose later.",
        "gateway": "Will unwrap that lock and forward the inner letter to HR.",
        "terms": ["VPN", "IPsec", "SSL VPN"],
    },
    {
        "id": "vpn-shape",
        "part": "1 · How a VPN works",
        "title": "Two envelopes. The tool is still unnamed.",
        "say": "Any office VPN does this shape. The inner envelope is the real request, from an office address. The outer envelope uses public addresses the internet can deliver. The gateway opens the outer envelope.",
        "visual": "packet",
        "layers": [
            layer("Outer IP header", "slate", ["49.37.10.8  →  203.0.113.10"], "Public addresses. The hotel and the internet can read this."),
            layer("Wrapper", "amber", ["The lock goes here", "IPsec or TLS, not chosen yet"], "This is the only part that changes between the modes."),
            layer("Inner IP packet", "green", ["10.50.1.20  →  10.1.1.50", "GET /hr/salary"], "Virtual IP to the HR server. Hidden from the café."),
        ],
        "cafe": "Sees the hotel's public IP talking to the gateway. Does not see 10.50.1.20 or the HR URL.",
        "gateway": "Removes the wrapper, reads the inner packet, and forwards it to 10.1.1.50. Replies come back to 10.50.1.20, so the office must route that pool to this gateway.",
        "terms": ["VPN", "Virtual IP", "Tunnel mode"],
    },
    {
        "id": "handshake",
        "part": "3 · How IPsec works",
        "title": "IKE first. No HR data yet.",
        "say": "IPsec does not start by encrypting the HR page. It starts with a handshake on UDP 500. Three beats, then user packets.",
        "visual": "compare",
        "cards": [
            {"name": "1 · IKE_SA_INIT", "tone": "blue", "lines": ["UDP 500", "Agree AES-GCM and DH group 19", "Diffie-Hellman", "No user data yet"]},
            {"name": "2 · IKE_AUTH", "tone": "green", "lines": ["Gateway certificate first", "Then EAP-MSCHAPv2", "Password is never sent", "A wrong password stops here"]},
            {"name": "3 · Child SA", "tone": "amber", "lines": ["ESP keys", "Traffic selectors", "Virtual IP 10.50.1.20", "Now the HR request may flow"]},
        ],
        "cafe": "Sees UDP 500 toward 203.0.113.10. After the first beat, the handshake itself is encrypted.",
        "gateway": "Proves who it is with a certificate, checks the user, then builds the data tunnel. Diffie-Hellman made a secret. The certificate proves the other end is the real gateway.",
        "terms": ["IKE", "IKE_SA_INIT", "IKE_AUTH", "Child SA", "Diffie-Hellman", "EAP-MSCHAPv2", "SA", "UDP 500"],
    },
    {
        "id": "esp",
        "part": "3 · How IPsec works",
        "title": "The HR request rides inside ESP.",
        "say": "This is tunnel mode. The inner IP packet is encrypted. The ESP header is the sticker on the bag: a locker number, a parcel number, and a tamper check. The key is not written on the sticker.",
        "visual": "packet",
        "layers": [
            layer("Outer IP header", "slate", ["49.37.10.8  →  203.0.113.10"], "Not part of the ESP header."),
            layer("ESP header", "blue", ["SPI = locker 42", "Sequence = parcel 18"], "Visible. SPI picks the key. A repeated sequence number is dropped."),
            layer("Encrypted payload", "green", ["10.50.1.20  →  10.1.1.50", "GET /hr/salary"], "The original IP packet. The café cannot read it."),
            layer("Integrity check", "amber", ["Tamper sticker"], "If it fails, the packet is thrown away."),
        ],
        "cafe": "Sees the gateway address, locker 42, and the packet size. Does not see the HR URL.",
        "gateway": "Uses SPI 42 to find the key, checks the sequence number and the sticker, decrypts, and forwards the inner packet to HR.",
        "terms": ["ESP", "SPI", "Sequence number", "Integrity check", "Tunnel mode", "AH", "Protocol 50", "PFS", "Traffic selector"],
    },
    {
        "id": "natt",
        "part": "3 · How IPsec works behind a hotel",
        "title": "NAT-T gives the bag a flat number.",
        "say": "The hotel rewrites 10.20.30.5 to 49.37.10.8. Plain ESP has no port, so many hotels drop it or mix up two laptops. NAT-T wraps ESP in UDP 4500. IKE moves there too.",
        "visual": "packet",
        "layers": [
            layer("Outer IP header", "slate", ["49.37.10.8  →  203.0.113.10"], "The hotel is allowed to rewrite the source address."),
            layer("UDP 4500", "teal", ["Source port 51000"], "The flat number. Two laptops can share one public IP."),
            layer("ESP header", "blue", ["SPI = locker 42", "Sequence = parcel 18"], "Same sticker as before, now inside UDP."),
            layer("Encrypted payload", "green", ["10.50.1.20  →  10.1.1.50"], "Still hidden."),
        ],
        "cafe": "Sees UDP 4500, not IP protocol 50.",
        "gateway": "During IKE, address hashes did not match, so NAT was detected. Data now arrives on UDP 4500.",
        "terms": ["NAT", "NAT-T", "UDP 4500", "ESP"],
    },
    {
        "id": "ssl",
        "part": "2 · How SSL VPN works",
        "title": "Same inner letter. TLS is the outer bag.",
        "say": "SSL VPN still gives the laptop a virtual IP and still hides the HR request. The wrapper is TLS on TCP 443, so the hotel treats it like ordinary HTTPS. The handshake is TLS, not IKE.",
        "visual": "packet",
        "layers": [
            layer("Outer IP header", "slate", ["49.37.10.8  →  203.0.113.10"], "Public addresses, same as before."),
            layer("TCP 443 · TLS", "amber", ["Looks like HTTPS"], "Guest Wi-Fi usually allows this door."),
            layer("Inner IP packet", "green", ["10.50.1.20  →  10.1.1.50", "GET /hr/salary"], "Same private letter as the IPsec path."),
        ],
        "cafe": "Sees a normal HTTPS connection to the gateway.",
        "gateway": "Terminates TLS, checks the same access policy, and forwards the inner packet to HR.",
        "terms": ["SSL VPN", "TCP 443", "Virtual IP", "VPN"],
    },
    {
        "id": "together",
        "part": "4 · IPsec and VPN together",
        "title": "IPsec VPN is the desk built with the IPsec lock.",
        "say": "VPN is the private desk. IPsec is the lock. IPsec VPN means that desk was reached with IKE and ESP. SSL VPN is the same desk reached with TLS. Your resume line is the IPsec VPN: try the IPsec lock first.",
        "visual": "compare",
        "cards": [
            {"name": "VPN", "tone": "blue", "lines": ["The desk", "Private access to HR", "Tool not implied"]},
            {"name": "IPsec", "tone": "green", "lines": ["The lock", "IKE then ESP", "Layer 3"]},
            {"name": "IPsec VPN", "tone": "teal", "lines": ["Desk + IPsec lock", "Tunnel mode", "SSL only if UDP is blocked"]},
            {"name": "SSL VPN", "tone": "amber", "lines": ["Desk + TLS lock", "TCP 443", "Same virtual IP"]},
        ],
        "cafe": "For an IPsec VPN it sees UDP 4500. For an SSL VPN it sees TCP 443. The HR letter stays hidden either way.",
        "gateway": "After either wrapper is removed, the inner packet is 10.50.1.20 → 10.1.1.50.",
        "terms": ["VPN", "IPsec", "IPsec VPN", "SSL VPN"],
    },
    {
        "id": "choice",
        "part": "4 · What the client decides",
        "title": "Fall back only when the road is blocked.",
        "say": "An IPsec VPN client tries IPsec first because UDP avoids TCP-inside-TCP and is lighter on the gateway. If the hotel drops UDP 500 and 4500, it uses SSL VPN on 443. A wrong password is not a blocked road. The client shows the error and does not switch locks to hide it.",
        "visual": "compare",
        "cards": [
            {"name": "UDP works", "tone": "green", "lines": ["Stay on IPsec", "NAT-T uses UDP 4500", "This is the preferred path"]},
            {"name": "UDP is blocked", "tone": "amber", "lines": ["IPsec VPN falls back", "TLS on TCP 443", "Same desk, other lock"]},
            {"name": "Wrong password", "tone": "red", "lines": ["Stop", "Do not fall back", "The user must see the error"]},
        ],
        "cafe": "A hotel that allows only web traffic never sees a finished IPsec tunnel.",
        "gateway": "The access policy is the same on both doors. Fallback does not grant a wider network.",
        "terms": ["IPsec VPN", "SSL VPN", "NAT-T", "TCP 443"],
    },
]


def _step(name, status, detail):
    return {"name": name, "status": status, "detail": detail}


def trace(body):
    place = body.get("place", "home")
    product = body.get("product", "ipsec-vpn")
    password = body.get("password", "ok")
    places = {
        "home": {"label": "Home router", "nat": True, "udp": True},
        "hotel": {"label": "Hotel Wi-Fi", "nat": True, "udp": False},
        "office": {"label": "Office network", "nat": False, "udp": True},
    }
    if place not in places or product not in {"none", "ipsec-only", "ssl", "ipsec-vpn"} or password not in {"ok", "bad"}:
        raise ValueError("unknown scenario")
    here = places[place]
    steps = []

    if product == "none":
        steps.append(_step("Plain IP packet", "fail", "Source 10.20.30.5, destination 10.1.1.50, GET /hr/salary in the clear."))
        return _result(
            connected=False,
            fell_back=False,
            wrapper="none",
            headline="No VPN. The HR request never arrives.",
            lesson="VPN is the missing result. There is no lock, and the private address is not routable.",
            steps=steps,
            layers=[
                layer("IP header", "slate", ["10.20.30.5  →  10.1.1.50"], "Visible."),
                layer("HTTP", "red", ["GET /hr/salary"], "Readable on the café Wi-Fi."),
            ],
        )

    if product == "ssl":
        steps.append(_step("TLS handshake", "ok", "TCP 443 to 203.0.113.10. The hotel allows it because it looks like HTTPS."))
        if password == "bad":
            steps.append(_step("Access policy", "fail", "The directory rejects the password. The tunnel is not built."))
            return _result(False, False, "tls", "SSL VPN reached the gateway. The password was wrong.", "A wrong password stops on this door too. There is no third lock to try.", steps, [
                layer("TCP 443 · TLS", "amber", ["Handshake completed"], "The road was open."),
                layer("Login", "red", ["Password rejected"], "No virtual IP is assigned."),
            ])
        steps.append(_step("Virtual IP", "ok", "Access policy passes. Laptop receives 10.50.1.20."))
        return _result(True, False, "tls", "Connected with SSL VPN on TCP 443.", "This is the TLS lock on the private desk. IPsec was not used.", steps, [
            layer("Outer IP", "slate", ["Public IP  →  203.0.113.10"], "Visible."),
            layer("TCP 443 · TLS", "amber", ["HTTPS-shaped door"], "The wrapper."),
            layer("Inner packet", "green", ["10.50.1.20  →  10.1.1.50"], "Hidden HR request."),
        ])

    # IPsec attempt for ipsec-only and ipsec-vpn
    if not here["udp"]:
        steps.append(_step("IKE_SA_INIT", "fail", f"{here['label']} drops UDP 500 and UDP 4500."))
        if product == "ipsec-only":
            return _result(False, False, "esp", "IPsec failed because UDP is blocked.", "IPsec the protocol has no TCP 443 of its own. Fallback is a decision of the IPsec VPN client, and this client does not have it.", steps, [
                layer("UDP 500", "red", ["No reply"], "The handshake never starts."),
            ])
        steps.append(_step("SSL fallback", "ok", "Path failure, so the IPsec VPN client opens TLS on TCP 443."))
        if password == "bad":
            steps.append(_step("Access policy", "fail", "The fallback door opened, then the password was rejected."))
            return _result(False, True, "tls", "Fell back to SSL VPN, then the login failed.", "Fallback is allowed for a blocked road. It does not hide a bad password.", steps, [
                layer("UDP 500 / 4500", "red", ["Blocked by the hotel"], "IPsec could not start."),
                layer("TCP 443", "amber", ["Fallback door opened"], "Login still has to pass."),
                layer("Login", "red", ["Password rejected"], "No tunnel."),
            ])
        steps.append(_step("Virtual IP", "ok", "Same access policy, same pool. Laptop receives 10.50.1.20."))
        return _result(True, True, "tls", "Connected over SSL VPN because the network blocked IPsec.", "IPsec VPN preferred the IPsec lock. The hotel refused it, so the same desk was reached with TLS.", steps, [
            layer("Outer IP", "slate", ["49.37.10.8  →  203.0.113.10"], "Hotel public address."),
            layer("TCP 443 · TLS", "amber", ["Fallback wrapper"], "Looks like HTTPS."),
            layer("Inner packet", "green", ["10.50.1.20  →  10.1.1.50"], "Same letter IPsec would have carried."),
        ])

    steps.append(_step("IKE_SA_INIT", "ok", "UDP 500. Algorithms agreed and Diffie-Hellman finished."))
    if here["nat"]:
        steps.append(_step("NAT-T", "ok", "NAT detected. IKE and ESP move to UDP 4500."))
        wrapper_name = "ESP inside UDP 4500"
        outer = layer("UDP 4500", "teal", ["NAT-T flat number"], "Home router can deliver replies.")
    else:
        steps.append(_step("NAT detection", "ok", "No NAT. ESP stays IP protocol 50. IKE stays on UDP 500."))
        wrapper_name = "ESP protocol 50"
        outer = layer("ESP protocol 50", "blue", ["No UDP wrapper"], "The office path does not need a port.")

    if password == "bad":
        steps.append(_step("IKE_AUTH", "fail", "Gateway certificate was valid. EAP-MSCHAPv2 rejected the password."))
        return _result(False, False, "esp", "IPsec reached the gateway. The password was wrong.", "Do not fall back to SSL. The road is fine. The user must see the authentication error.", steps, [
            layer("IKE_SA_INIT", "blue", ["UDP 500 completed"], "The road is open."),
            layer("IKE_AUTH", "red", ["Password rejected"], "Child SA is not built."),
        ])

    steps.append(_step("IKE_AUTH", "ok", "Certificate checked, then EAP-MSCHAPv2 succeeded inside the encrypted handshake."))
    steps.append(_step("Child SA", "ok", f"Virtual IP 10.50.1.20. Data uses {wrapper_name}."))
    return _result(True, False, "esp", f"Connected with IPsec. {wrapper_name}.", "This is an IPsec VPN: the private desk, built with the IPsec lock.", steps, [
        layer("Outer IP", "slate", ["Public source  →  203.0.113.10"], "Visible."),
        outer,
        layer("ESP header", "blue", ["SPI = locker 42", "Sequence number"], "The sticker. Not the key."),
        layer("Inner packet", "green", ["10.50.1.20  →  10.1.1.50"], "Hidden HR request."),
    ])


def _result(connected, fell_back, wrapper, headline, lesson, steps, layers):
    return {
        "connected": connected,
        "fell_back": fell_back,
        "wrapper": wrapper,
        "headline": headline,
        "lesson": lesson,
        "steps": steps,
        "layers": layers,
    }


def _phase(caption, tunnel, ride, style, drop=None, unwrap=False, block=False):
    return {
        "caption": caption,
        "tunnel": tunnel,
        "ride": ride,
        "style": style,
        "drop": drop,
        "unwrap": unwrap,
        "block": block,
    }


SCENES = [
    {
        "id": "vpn",
        "label": "How VPN works",
        "phases": [
            _phase("No tunnel. The open request dies at the hotel. 10.1.1.50 is not on the internet.", None, ["laptop", "hotel"], "open", drop="hotel", block=True),
            _phase("A VPN is a private pipe from the laptop to the office. The lock is not chosen yet.", {"kind": "vpn", "label": "VPN"}, ["laptop", "gateway"], "plain", unwrap=False),
            _phase("Inner packet 10.50.1.20 to HR. Outer packet is only the public path.", {"kind": "vpn", "label": "VPN"}, ["laptop", "gateway", "hr"], "plain", unwrap=True),
        ],
    },
    {
        "id": "ipsec",
        "label": "How IPsec works",
        "phases": [
            _phase("IKE on UDP 500. Keys and identity. No HR page yet.", {"kind": "ike", "label": "IKE · UDP 500"}, "bounce", "key"),
            _phase("ESP tunnel. SPI 42 picks the key. The HR letter is hidden.", {"kind": "ipsec", "label": "ESP · SPI 42"}, ["laptop", "gateway", "hr"], "esp", unwrap=True),
            _phase("Hotel NAT rewrites the address. UDP 4500 is the flat number that lets ESP through.", {"kind": "ipsec", "label": "NAT-T · UDP 4500"}, ["laptop", "gateway", "hr"], "esp", unwrap=True),
        ],
    },
    {
        "id": "ssl",
        "label": "How SSL VPN works",
        "phases": [
            _phase("Same inner letter. The pipe is TLS on TCP 443, so the hotel treats it like HTTPS.", {"kind": "ssl", "label": "TLS · TCP 443"}, ["laptop", "gateway", "hr"], "tls", unwrap=True),
        ],
    },
    {
        "id": "both",
        "label": "IPsec VPN",
        "phases": [
            _phase("IPsec VPN: the private desk, built with the IPsec lock.", {"kind": "ipsec", "label": "IPsec VPN"}, ["laptop", "gateway", "hr"], "esp", unwrap=True),
            _phase("Hotel blocks UDP 500 and 4500. The IPsec pipe stops.", {"kind": "ipsec", "label": "UDP blocked"}, ["laptop", "hotel"], "esp", drop="hotel", block=True),
            _phase("Same desk, TLS lock. A wrong password would stop here instead of switching pipes.", {"kind": "ssl", "label": "SSL fallback · 443"}, ["laptop", "gateway", "hr"], "tls", unwrap=True),
        ],
    },
]


def phases_for(body, result):
    place = body.get("place", "home")
    product = body.get("product", "ipsec-vpn")
    password = body.get("password", "ok")
    nat_label = "ESP · protocol 50" if place == "office" else "ESP · UDP 4500"
    if product == "none":
        return [_phase(result["headline"], None, ["laptop", "hotel"], "open", drop="hotel", block=True)]
    if product == "ssl" and password == "bad":
        return [_phase(result["headline"], {"kind": "ssl", "label": "TLS · TCP 443"}, ["laptop", "gateway"], "tls", drop="gateway")]
    if product == "ssl":
        return [_phase(result["headline"], {"kind": "ssl", "label": "TLS · TCP 443"}, ["laptop", "gateway", "hr"], "tls", unwrap=True)]
    if place == "hotel" and product == "ipsec-only":
        return [_phase(result["headline"], {"kind": "ipsec", "label": "UDP blocked"}, ["laptop", "hotel"], "esp", drop="hotel", block=True)]
    if place == "hotel" and product == "ipsec-vpn" and password == "bad":
        return [
            _phase("Hotel blocks the IPsec pipe.", {"kind": "ipsec", "label": "UDP blocked"}, ["laptop", "hotel"], "esp", drop="hotel", block=True),
            _phase(result["headline"], {"kind": "ssl", "label": "TLS · TCP 443"}, ["laptop", "gateway"], "tls", drop="gateway"),
        ]
    if place == "hotel" and product == "ipsec-vpn":
        return [
            _phase("Hotel blocks UDP.", {"kind": "ipsec", "label": "UDP blocked"}, ["laptop", "hotel"], "esp", drop="hotel", block=True),
            _phase(result["headline"], {"kind": "ssl", "label": "SSL fallback · 443"}, ["laptop", "gateway", "hr"], "tls", unwrap=True),
        ]
    if password == "bad":
        return [_phase(result["headline"], {"kind": "ipsec", "label": "IKE · UDP 500"}, ["laptop", "gateway"], "key", drop="gateway")]
    return [
        _phase("IKE agrees the keys.", {"kind": "ike", "label": "IKE · UDP 500"}, "bounce", "key"),
        _phase(result["headline"], {"kind": "ipsec", "label": nat_label}, ["laptop", "gateway", "hr"], "esp", unwrap=True),
    ]


def self_check():
    hotel_vpn = trace({"place": "hotel", "product": "ipsec-vpn", "password": "ok"})
    assert hotel_vpn["connected"] and hotel_vpn["fell_back"] and hotel_vpn["wrapper"] == "tls"
    hotel_raw = trace({"place": "hotel", "product": "ipsec-only", "password": "ok"})
    assert not hotel_raw["connected"] and not hotel_raw["fell_back"]
    home_bad = trace({"place": "home", "product": "ipsec-vpn", "password": "bad"})
    assert not home_bad["connected"] and not home_bad["fell_back"]
    office = trace({"place": "office", "product": "ipsec-vpn", "password": "ok"})
    assert office["connected"] and office["wrapper"] == "esp" and any("protocol 50" in s["detail"] for s in office["steps"])
    home = trace({"place": "home", "product": "ipsec-vpn", "password": "ok"})
    assert home["connected"] and any("4500" in s["detail"] for s in home["steps"])
    none = trace({"place": "home", "product": "none", "password": "ok"})
    assert not none["connected"] and none["wrapper"] == "none"
    hotel_bad = trace({"place": "hotel", "product": "ipsec-vpn", "password": "bad"})
    assert not hotel_bad["connected"] and hotel_bad["fell_back"]


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, fmt, *args):
        print("%s - %s" % (self.address_string(), fmt % args))

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/story":
            return self._json({"cast": CAST, "steps": STORY, "glossary": GLOSSARY, "scenes": SCENES})
        if path == "/":
            self.path = "/index.html"
        return super().do_GET()

    def do_POST(self):
        path = urlparse(self.path).path
        if path != "/api/trace":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b"{}"
        try:
            body = json.loads(raw.decode("utf-8"))
            payload = trace(body)
            payload["phases"] = phases_for(body, payload)
        except (json.JSONDecodeError, ValueError):
            self.send_error(400, "Send place, product, and password")
            return
        self._json(payload)

    def _json(self, payload):
        data = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def main():
    self_check()
    server = None
    port = None
    for candidate in range(8765, 8775):
        try:
            server = ThreadingHTTPServer(("127.0.0.1", candidate), Handler)
            port = candidate
            break
        except OSError:
            continue
    if server is None:
        raise SystemExit("No free port between 8765 and 8774")
    print(f"Open http://127.0.0.1:{port}", flush=True)
    print("This demo only draws packets. It does not open a real tunnel.", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
