#!/usr/bin/env python3
"""Revision diagrams for the IPsec notes. Labels match the written answers."""

import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
W, H = 1440, 810

NAVY = (15, 35, 64)
INK = (30, 41, 59)
MUTED = (71, 85, 105)
WHITE = (255, 255, 255)
BG = (239, 244, 250)
LINE = (203, 213, 225)
BLUE = (29, 78, 216)
BLUE_SOFT = (219, 234, 254)
TEAL = (14, 116, 144)
TEAL_SOFT = (204, 251, 241)
GREEN = (6, 95, 70)
GREEN_SOFT = (209, 250, 229)
AMBER = (146, 64, 14)
AMBER_SOFT = (255, 237, 213)
RED = (153, 27, 27)
RED_SOFT = (254, 226, 226)
GOLD = (202, 138, 4)
SLATE = (51, 65, 85)
SLATE_SOFT = (241, 245, 249)

REGULAR = "/System/Library/Fonts/Supplemental/Arial.ttf"
BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

F_Q = ImageFont.truetype(BOLD, 28)
F_TITLE = ImageFont.truetype(BOLD, 34)
F_SUB = ImageFont.truetype(REGULAR, 20)
F_H = ImageFont.truetype(BOLD, 24)
F_B = ImageFont.truetype(BOLD, 20)
F_P = ImageFont.truetype(REGULAR, 18)
F_S = ImageFont.truetype(REGULAR, 16)
F_XS = ImageFont.truetype(REGULAR, 15)


def new(qnum, title, subtitle):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W, 108), fill=NAVY)
    d.rounded_rectangle((32, 30, 118, 78), 16, fill=GOLD)
    d.text((75, 54), qnum, font=F_Q, fill=NAVY, anchor="mm")
    d.text((140, 36), title, font=F_TITLE, fill=WHITE, anchor="lt")
    d.text((140, 76), subtitle, font=F_SUB, fill=(191, 219, 254), anchor="lt")
    return im, d


def panel(d, x, y, w, h, fill, outline, width=3):
    d.rounded_rectangle((x, y, x + w, y + h), 18, fill=fill, outline=outline, width=width)


def center(d, cx, cy, lines, font, fill, gap=5):
    heights = []
    for line in lines:
        box = d.textbbox((0, 0), line, font=font)
        heights.append(box[3] - box[1])
    total = sum(heights) + gap * (len(lines) - 1)
    y = cy - total / 2
    for line, h in zip(lines, heights):
        d.text((cx, y), line, font=font, fill=fill, anchor="mt")
        y += h + gap


def wrap_text(d, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def footer(d, text="Say the labels out loud. Then answer without looking."):
    d.text((W / 2, H - 22), text, font=F_S, fill=MUTED, anchor="mm")


def arrow(d, x1, y1, x2, y2, fill=BLUE, width=5):
    d.line((x1, y1, x2, y2), fill=fill, width=width)
    import math

    ang = math.atan2(y2 - y1, x2 - x1)
    length = 16
    p1 = (x2 - length * math.cos(ang - 0.4), y2 - length * math.sin(ang - 0.4))
    p2 = (x2 - length * math.cos(ang + 0.4), y2 - length * math.sin(ang + 0.4))
    d.polygon([(x2, y2), p1, p2], fill=fill)


def badge(d, x, y, text, fill, ink=WHITE):
    tw = d.textlength(text, font=F_S)
    d.rounded_rectangle((x, y, x + tw + 22, y + 28), 14, fill=fill)
    d.text((x + 11, y + 14), text, font=F_S, fill=ink, anchor="lm")


def columns(n, y, h, pad=36, gap=22):
    w = (W - 2 * pad - gap * (n - 1)) / n
    return [(pad + i * (w + gap), y, w, h) for i in range(n)]


def save_png(im, stem):
    im.save(ROOT / f"{stem}.png", optimize=True)


def save_gif(frames, stem):
    tmp = ROOT / "_tmp" / stem
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True)
    for i, im in enumerate(frames):
        im.convert("RGB").save(tmp / f"f{i:02d}.png")
    out = ROOT / f"{stem}.gif"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-framerate",
            "0.45",
            "-i",
            str(tmp / "f%02d.png"),
            "-vf",
            "split[s0][s1];[s0]palettegen=reserve_transparent=0:stats_mode=diff[p];[s1][p]paletteuse=dither=bayer:bayer_scale=3",
            "-loop",
            "0",
            str(out),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    shutil.rmtree(tmp)


def dim_note(d, text):
    d.text((W - 36, 128), text, font=F_S, fill=MUTED, anchor="rt")


# --- questions -------------------------------------------------------------

def q01(step):
    im, d = new("Q1", "What is IPsec?", "A clear IP packet goes into a locked box.")
    specs = [
        (0, "1  Open postcard", SLATE, SLATE_SOFT, ["Anyone on café Wi-Fi", "can read the HR request.", "Source, destination,", "and the data are visible."]),
        (1, "2  IPsec wraps it", BLUE, BLUE_SOFT, ["ESP encrypts the packet", "and adds an integrity tag.", "Only the two ends", "have the key."]),
        (2, "3  Locked box", GREEN, GREEN_SOFT, ["Café sees addresses of", "the VPN gateway only.", "The HR request is hidden.", "Apps do not change."]),
    ]
    boxes = columns(3, 168, 250)
    for i, ((x, y, w, h), spec) in enumerate(zip(boxes, specs)):
        active = i <= step
        title, outline, fill, lines = spec[1], spec[2], spec[3], spec[4]
        panel(d, x, y, w, h, fill if active else (248, 250, 252), outline if active else LINE)
        d.text((x + w / 2, y + 36), title, font=F_H, fill=outline if active else MUTED, anchor="mt")
        center(d, x + w / 2, y + 155, lines if active else ["next frame"], F_P, INK if active else MUTED, gap=6)
    if step >= 0:
        arrow(d, boxes[0][0] + boxes[0][2] + 2, 290, boxes[1][0] - 2, 290)
    if step >= 1:
        arrow(d, boxes[1][0] + boxes[1][2] + 2, 290, boxes[2][0] - 2, 290, fill=GREEN)
    props = [("Confidentiality", "cannot read it"), ("Integrity", "cannot edit it"), ("Authentication", "it is really them"), ("Anti-replay", "cannot resend it")]
    row = columns(4, 460, 250)
    for i, ((x, y, w, h), (name, meaning)) in enumerate(zip(row, props)):
        on = step == 2
        panel(d, x, y, w, h, GREEN_SOFT if on else SLATE_SOFT, GREEN if on else LINE)
        center(d, x + w / 2, y + 90, [name, "", meaning], F_B, GREEN if on else MUTED, gap=8)
    footer(d, "Four things to say: confidentiality, integrity, authentication, anti-replay.")
    return im


def q01b():
    im, d = new("Q1b", "What is the ESP header?", "The label on the locked box. The key is not written on it.")
    rows = [
        ("Outer IP header", "Café public IP  →  gateway public IP", "Visible to the café. This is not the ESP header.", SLATE, SLATE_SOFT),
        ("ESP header", "SPI = locker 42      Sequence = parcel 18", "Picks the key. Drops a replayed packet.", BLUE, BLUE_SOFT),
        ("Encrypted payload", "10.50.1.20  →  10.1.1.50   is hidden", "The original IP packet sits in here.", GREEN, GREEN_SOFT),
        ("Integrity check", "Tamper sticker", "If it does not match, the gateway throws the packet away.", AMBER, AMBER_SOFT),
    ]
    y = 145
    for title, value, why, ink, fill in rows:
        panel(d, 36, y, 1368, 140, fill, ink)
        d.text((60, y + 28), title, font=F_H, fill=ink)
        d.text((60, y + 68), value, font=F_B, fill=NAVY)
        d.text((60, y + 104), why, font=F_P, fill=INK)
        y += 152
    footer(d, "Protocol 50. The café sees the locker number and the packet size, not the HR letter.")
    return im


def q02():
    im, d = new("Q2", "Why companies use IPsec", "Private addresses and private data, over the public internet.")
    panel(d, 36, 150, 670, 560, WHITE, BLUE)
    d.text((70, 175), "Remote access  ·  your resume", font=F_H, fill=BLUE)
    center(d, 370, 390, ["Laptop on hotel Wi-Fi", "10.20.30.5", "↓", "encrypted tunnel", "↓", "BIG-IP gateway", "↓", "Internal HR app  10.1.1.50"], F_P, INK, gap=6)
    badge(d, 70, 640, "One user  →  company network", BLUE)

    panel(d, 734, 150, 670, 560, WHITE, TEAL)
    d.text((768, 175), "Site-to-site", font=F_H, fill=TEAL)
    center(d, 1068, 390, ["Hyderabad office firewall", "↓", "IPsec tunnel", "no client on each PC", "↓", "Mumbai firewall", "↓", "PCs send to 10.2.0.0/16"], F_P, INK, gap=6)
    badge(d, 768, 640, "Network  →  network", TEAL)
    footer(d)
    return im


def q03():
    im, d = new("Q3", "ESP versus AH", "Production VPNs use ESP. AH does not hide the data.")
    panel(d, 36, 150, 670, 560, WHITE, GREEN)
    d.text((70, 175), "ESP   ·   IP protocol 50", font=F_H, fill=GREEN)
    panel(d, 90, 240, 560, 120, GREEN_SOFT, GREEN)
    center(d, 370, 300, ["Outer IP: café  →  gateway", "Payload: unreadable blob"], F_B, GREEN)
    center(d, 370, 430, ["Sealed courier bag.", "The courier sees the address", "and cannot read the document.", "This is the one you deploy."], F_P, INK, gap=8)
    badge(d, 90, 620, "Encrypts + integrity check", GREEN)

    panel(d, 734, 150, 670, 560, WHITE, RED)
    d.text((768, 175), "AH   ·   IP protocol 51", font=F_H, fill=RED)
    panel(d, 788, 240, 560, 120, RED_SOFT, RED)
    center(d, 1068, 300, ["Checksum covers the IP header", "Payload stays readable"], F_B, RED)
    center(d, 1068, 430, ["Clear envelope with a wax seal.", "NAT rewrites the address,", "the seal breaks, packet dropped.", "Rare on an internet VPN."], F_P, INK, gap=8)
    badge(d, 788, 620, "Authenticates only. No encryption.", RED)
    footer(d, "If they ask what you used: ESP in tunnel mode.")
    return im


def q04():
    im, d = new("Q4", "Tunnel mode versus transport mode", "A remote user needs a second envelope.")
    panel(d, 36, 150, 880, 580, WHITE, BLUE)
    d.text((60, 172), "Tunnel mode  ·  the office VPN", font=F_H, fill=BLUE)
    panel(d, 70, 240, 800, 200, BLUE_SOFT, BLUE)
    center(d, 470, 300, ["OUTER header   café public IP  →  gateway public IP"], F_B, BLUE)
    panel(d, 120, 340, 700, 70, WHITE, NAVY)
    center(d, 470, 375, ["INNER packet   10.50.1.20  →  10.1.1.50   HR request"], F_B, NAVY)
    center(d, 470, 520, ["Internet routers only see the outer header.", "The gateway opens it and walks the inner letter to the desk.", "Your feature uses this mode."], F_P, INK, gap=8)
    badge(d, 70, 650, "Hides internal IP addresses", BLUE)

    panel(d, 940, 150, 464, 580, WHITE, AMBER)
    d.text((964, 172), "Transport mode", font=F_H, fill=AMBER)
    panel(d, 970, 250, 404, 140, AMBER_SOFT, AMBER)
    center(d, 1172, 320, ["Original IP header stays", "Only the payload is locked", "Both hosts are the endpoints"], F_P, AMBER, gap=8)
    center(d, 1172, 500, ["Host-to-host.", "Not a typical", "office VPN.", "Internal IPs stay visible."], F_P, INK, gap=8)
    footer(d)
    return im


def q05():
    im, d = new("Q5", "What the laptop receives", "Apps keep using normal IP. The client hides the encryption.")
    items = [
        ("Virtual IP", "10.50.1.20", "Internal servers reply here. The office must route this pool back to the gateway."),
        ("Internal DNS", "hr.corp.example", "Resolves to a private address. Without it, names fail or hit the public internet."),
        ("Routes", "company subnets", "Split tunnel sends only those subnets in. Full tunnel sends every packet in."),
    ]
    boxes = columns(3, 150, 300)
    colors = [(BLUE, BLUE_SOFT), (TEAL, TEAL_SOFT), (GREEN, GREEN_SOFT)]
    for (x, y, w, h), (title, value, body), (ink, fill) in zip(boxes, items, colors):
        panel(d, x, y, w, h, WHITE, ink)
        d.rectangle((x, y, x + w, y + 64), fill=fill)
        d.text((x + w / 2, y + 32), title, font=F_H, fill=ink, anchor="mm")
        d.text((x + w / 2, y + 120), value, font=F_B, fill=NAVY, anchor="mm")
        lines = wrap_text(d, body, F_P, w - 40)
        center(d, x + w / 2, y + 210, lines, F_P, INK, gap=4)

    panel(d, 36, 480, 668, 250, WHITE, GREEN)
    d.text((60, 505), "Split tunnel", font=F_H, fill=GREEN)
    center(d, 370, 600, ["Company apps use the tunnel.", "YouTube stays on the café network.", "Faster. The laptop is a bridge."], F_P, INK, gap=8)

    panel(d, 736, 480, 668, 250, WHITE, AMBER)
    d.text((760, 505), "Full tunnel", font=F_H, fill=AMBER)
    center(d, 1070, 600, ["Every packet enters the office.", "Safer for a company laptop.", "Costs bandwidth. Local printer needs an exclude."], F_P, INK, gap=8)
    footer(d, "Connected + every app times out → check the return route for the virtual-IP pool.")
    return im


def q06():
    im, d = new("Q6", "IPsec versus SSL VPN", "Same inner network. Different outer door.")
    panel(d, 36, 148, 670, 500, WHITE, BLUE)
    d.text((60, 170), "IPsec   preferred path", font=F_H, fill=BLUE)
    rows = [("Handshake", "IKE"), ("Firewall sees", "UDP 500 and UDP 4500"), ("Strength", "Fast. No TCP inside TCP."), ("Weakness", "Guest Wi-Fi often blocks UDP.")]
    y = 230
    for k, v in rows:
        d.text((70, y), k, font=F_B, fill=MUTED)
        d.text((280, y), v, font=F_P, fill=INK)
        y += 70
    badge(d, 70, 560, "Try this first", BLUE)

    panel(d, 734, 148, 670, 500, WHITE, AMBER)
    d.text((758, 170), "SSL VPN   escape hatch", font=F_H, fill=AMBER)
    rows = [("Handshake", "TLS"), ("Firewall sees", "TCP 443, same as HTTPS"), ("Strength", "Passes web-only networks."), ("Weakness", "TCP meltdown on lossy Wi-Fi.")]
    y = 230
    for k, v in rows:
        d.text((768, y), k, font=F_B, fill=MUTED)
        d.text((980, y), v, font=F_P, fill=INK)
        y += 70
    badge(d, 768, 560, "Fall back here", AMBER)
    footer(d, "Both can still give the laptop a virtual adapter and an internal IP.")
    return im


def q07():
    im, d = new("Q7", "Four words before the handshake", "Use these and you sound like you have configured it.")
    tiles = [
        ("ESP", "Carries user data", "Protocol 50"),
        ("IKE", "Agrees keys first", "UDP 500"),
        ("SA", "One-way agreement", "Need two"),
        ("Policy", "What to encrypt", "Selectors"),
    ]
    boxes = columns(4, 150, 280)
    inks = [GREEN, BLUE, TEAL, AMBER]
    fills = [GREEN_SOFT, BLUE_SOFT, TEAL_SOFT, AMBER_SOFT]
    for (x, y, w, h), (name, line, chip), ink, fill in zip(boxes, tiles, inks, fills):
        panel(d, x, y, w, h, fill, ink)
        center(d, x + w / 2, y + h / 2, [name, "", line, chip], F_H, ink, gap=10)

    panel(d, 36, 470, 1368, 250, WHITE, NAVY)
    d.text((60, 495), "SPI is a locker number, not a secret.", font=F_H, fill=NAVY)
    center(d, 720, 600, ["The ESP header carries an SPI. The gateway uses it to pick which key decrypts this packet.", "A traffic selector says which subnets must enter the tunnel. If the two sides disagree, IKE can succeed and data still fails."], F_P, INK, gap=12)
    footer(d)
    return im


def q08(step):
    im, d = new("Q8", "How the tunnel comes up", "Three beats. Old names: Phase 1, then Phase 2.")
    beats = [
        ("1", "IKE_SA_INIT", "Phase 1", ["Agree algorithms", "Diffie-Hellman", "Handshake becomes encrypted", "No user data yet"]),
        ("2", "IKE_AUTH", "still Phase 1", ["Gateway shows certificate", "User does EAP-MSCHAPv2", "Bad password stops here", "Do not fall back to SSL"]),
        ("3", "Child SA", "Phase 2", ["ESP algorithms", "Traffic selectors", "Optional fresh DH (PFS)", "Now user packets flow"]),
    ]
    boxes = columns(3, 160, 520)
    for i, ((x, y, w, h), beat) in enumerate(zip(boxes, beats)):
        on = i == step
        done = i < step
        ink = GREEN if done else BLUE if on else MUTED
        fill = GREEN_SOFT if done else BLUE_SOFT if on else WHITE
        panel(d, x, y, w, h, fill, ink, width=4 if on else 3)
        d.text((x + 28, y + 28), beat[0], font=F_TITLE, fill=ink)
        d.text((x + 78, y + 36), beat[1], font=F_H, fill=ink)
        d.text((x + 28, y + 90), beat[2], font=F_B, fill=MUTED)
        center(d, x + w / 2, y + 300, beat[3], F_P, INK if on or done else MUTED, gap=16)
        if done:
            badge(d, x + 28, y + h - 56, "done", GREEN)
        elif on:
            badge(d, x + 28, y + h - 56, "now", BLUE)
    footer(d, "First key protects the conversation. The child SA is a separate key for the documents.")
    return im


def q09(step):
    im, d = new("Q9", "Diffie-Hellman, as an analogy", "The private ingredient never crosses the network. Eve still cannot plate the dish.")
    # three people
    people = [("You", "private: red"), ("Gateway", "private: blue"), ("Eve on the path", "sees only mixtures")]
    boxes = columns(3, 155, 130)
    for (x, y, w, h), (name, secret) in zip(boxes, people):
        panel(d, x, y, w, h, WHITE, NAVY)
        center(d, x + w / 2, y + h / 2, [name, secret], F_B, NAVY, gap=6)

    stages = [
        "Both start with the same public paint, plus a private colour they never send.",
        "Each mixes public + private and sends only that mixture.",
        "Each adds their own private colour to the mixture they received.",
        "Both now hold the same secret colour. Eve has both mixtures and still cannot make it.",
    ]
    panel(d, 36, 320, 1368, 180, BLUE_SOFT if step < 3 else GREEN_SOFT, BLUE if step < 3 else GREEN)
    center(d, 720, 410, wrap_text(d, stages[step], F_H, 1200), F_H, NAVY, gap=8)

    panel(d, 36, 530, 1368, 200, AMBER_SOFT, AMBER)
    center(d, 720, 610, ["This creates a secret with whoever is on the other end.", "It does not prove that end is your gateway. The certificate check does that.", "Say this when you explain why EAP needs the server certificate first."], F_P, INK, gap=10)
    footer(d, "Analogy only. The real exchange is numbers, and the private numbers stay local.")
    return im


def q10():
    im, d = new("Q10", "Proposal mismatch", "Both sides showed up. They still share no language.")
    panel(d, 36, 150, 560, 420, GREEN_SOFT, GREEN)
    d.text((60, 175), "Your gateway offers", font=F_H, fill=GREEN)
    center(d, 316, 340, ["AES-GCM 256", "DH group 19", "SHA-256", "", "One complete bundle"], F_B, GREEN, gap=12)

    panel(d, 844, 150, 560, 420, RED_SOFT, RED)
    d.text((868, 175), "The peer offers", font=F_H, fill=RED)
    center(d, 1124, 340, ["3DES", "DH group 2", "SHA-1", "", "A different bundle"], F_B, RED, gap=12)

    d.text((720, 340), "≠", font=ImageFont.truetype(BOLD, 64), fill=RED, anchor="mm")

    panel(d, 36, 600, 1368, 140, WHITE, RED)
    center(d, 720, 670, ["Log: no proposal chosen. This is a config bug, not a network block. Do not fall back to SSL."], F_B, RED)
    footer(d)
    return im


def q11():
    im, d = new("Q11", "IKEv1 versus IKEv2", "Prefer IKEv2 for remote access.")
    cols = [
        ("IKEv1 main mode", BLUE, ["6 messages", "Identity hidden", "after DH", "Safer of the two", "IKEv1 options"]),
        ("IKEv1 aggressive", RED, ["3 messages", "Identity in the clear", "PSK can be cracked", "offline", "Avoid for users"]),
        ("IKEv2  ·  use this", GREEN, ["Fewer round trips", "NAT detection built in", "EAP for passwords", "Liveness built in", "MOBIKE for roaming"]),
    ]
    boxes = columns(3, 155, 520)
    for (x, y, w, h), (title, ink, lines) in zip(boxes, cols):
        fill = GREEN_SOFT if ink == GREEN else RED_SOFT if ink == RED else BLUE_SOFT
        panel(d, x, y, w, h, fill, ink)
        d.text((x + w / 2, y + 40), title, font=F_H, fill=ink, anchor="mt")
        center(d, x + w / 2, y + 280, lines, F_P, INK, gap=16)
    footer(d, "You can say you prefer IKEv2 even if the interviewer learned Phase 1 and Phase 2.")
    return im


def q12():
    im, d = new("Q12", "Perfect forward secrecy", "A stolen badge next week does not open yesterday’s meeting room.")
    panel(d, 36, 155, 430, 540, WHITE, NAVY)
    center(d, 251, 300, ["Long-term key", "", "Gateway certificate", "or pre-shared key", "", "Proves identity", "at the door"], F_P, NAVY, gap=8)
    badge(d, 80, 600, "Not the data key", NAVY)

    arrow(d, 480, 400, 560, 400, fill=NAVY)

    panel(d, 580, 155, 824, 250, GREEN_SOFT, GREEN)
    center(d, 992, 280, ["Child SA does its own Diffie-Hellman", "Today’s data key is thrown away at rekey", "A recording from yesterday stays unreadable"], F_P, GREEN, gap=14)

    panel(d, 580, 430, 824, 265, AMBER_SOFT, AMBER)
    center(d, 992, 545, ["Turn PFS on in the IPsec / child proposal,", "not only in the IKE policy.", "A solid answer: DH group 19 or 20.", "“None” means a future key theft decrypts old captures."], F_P, INK, gap=10)
    footer(d)
    return im


def q13():
    im, d = new("Q13", "Configuration objects", "The UI schema was the blueprint for the backend.")
    tiles = [
        ("IKE proposal", "Handshake crypto, DH group, lifetime"),
        ("IPsec proposal", "ESP cipher, PFS group, lifetime"),
        ("Traffic selector", "Local subnet and remote subnet"),
        ("Peer", "Address, IKEv2, PSK or cert or EAP"),
        ("Tunnel binding", "Which peer + selectors + proposals"),
        ("Remote-access profile", "Pool, DNS, split tunnel, NAT-T, fallback, access policy"),
    ]
    for i, (name, body) in enumerate(tiles):
        col, row = i % 3, i // 3
        x = 36 + col * 460
        y = 150 + row * 250
        panel(d, x, y, 440, 220, WHITE, BLUE if row == 0 else GREEN)
        d.text((x + 24, y + 28), f"{i+1}   {name}", font=F_B, fill=NAVY)
        lines = wrap_text(d, body, F_P, 390)
        center(d, x + 220, y + 130, lines, F_P, INK, gap=6)
    footer(d, "Rule to say: EAP selected means a server certificate is required.")
    return im


def q14(step):
    im, d = new("Q14", "Why IPsec breaks behind NAT", "The receptionist can deliver a parcel only if it has a flat number.")
    titles = [
        "Plain ESP has no port",
        "Two laptops, one public IP",
        "NAT-T writes a flat number",
    ]
    bodies = [
        ["Laptop 192.168.1.20", "sends IP protocol 50.", "Home router expects TCP or UDP.", "Protocol 50 is dropped."],
        ["Two hotel guests share 49.37.10.8.", "ESP has an SPI, not a port.", "The router keeps one mapping.", "The second user breaks the first."],
        ["IKE detects NAT (address hashes differ).", "ESP is wrapped in UDP 4500.", "The router rewrites the source port.", "Each laptop stays distinct."],
    ]
    boxes = columns(3, 170, 460)
    for i, ((x, y, w, h), title, lines) in enumerate(zip(boxes, titles, bodies)):
        on = i == step
        ink = RED if i < 2 else GREEN
        fill = RED_SOFT if i < 2 else GREEN_SOFT
        panel(d, x, y, w, h, fill if on else WHITE, ink if on else LINE, width=5 if on else 2)
        d.text((x + 24, y + 30), title, font=F_H, fill=ink if on else MUTED)
        center(d, x + w / 2, y + 250, lines if on else [" "], F_P, INK, gap=14)
        badge(d, x + 24, y + h - 60, "problem" if i < 2 else "NAT-T fix", ink if on else LINE, WHITE if on else MUTED)
    footer(d, "AH is worse: its checksum covers the IP address, so NAT breaks the seal.")
    return im


def q15():
    im, d = new("Q15", "Ports you should know cold", "Healthy remote access: a short UDP 500 exchange, then UDP 4500.")
    rows = [
        ("UDP 500", "IKE", "Start of the handshake, before NAT is detected", BLUE),
        ("UDP 4500", "NAT-T", "IKE and ESP after NAT is detected", TEAL),
        ("IP protocol 50", "ESP", "Raw encrypted data when NAT-T is off", GREEN),
        ("IP protocol 51", "AH", "Almost never in this design", MUTED),
        ("TCP 443", "SSL VPN", "Fallback. Looks like HTTPS", AMBER),
    ]
    y = 145
    for port, name, when, ink in rows:
        panel(d, 36, y, 1368, 110, WHITE, ink)
        d.text((60, y + 55), port, font=F_H, fill=ink, anchor="lm")
        d.text((380, y + 55), name, font=F_B, fill=NAVY, anchor="lm")
        d.text((620, y + 55), when, font=F_P, fill=INK, anchor="lm")
        y += 122
    footer(d, "Protocol 50 on the public internet means NAT-T is off. Expect home users to fail.")
    return im


def q16():
    im, d = new("Q16", "When “no NAT-T” is the network’s fault", "Fall back only for a blocked path.")
    panel(d, 36, 145, 880, 580, WHITE, RED)
    d.text((60, 170), "Path is blocked  ·  fallback is fair", font=F_H, fill=RED)
    lines = [
        "No reply to UDP 500",
        "Replies die when you move to UDP 4500",
        "Hotel allows only TCP 80 and 443",
        "Peer has NAT-T disabled, so it waits for raw ESP",
    ]
    y = 240
    for line in lines:
        d.ellipse((70, y, 96, y + 26), fill=RED)
        d.text((116, y + 13), line, font=F_P, fill=INK, anchor="lm")
        y += 80

    panel(d, 940, 145, 464, 580, GREEN_SOFT, GREEN)
    d.text((964, 170), "Do not call these NAT-T", font=F_H, fill=GREEN)
    center(d, 1172, 400, ["Authentication failed", "", "No proposal chosen", "", "Small ping works,", "large ping fails (MTU)"], F_P, GREEN, gap=6)
    footer(d)
    return im


def q17(step):
    im, d = new("Q17", "Fallback to TCP 443", "Switch vehicles only when the gate is the problem.")
    steps = [
        ("1", "User clicks Connect", "Start IKEv2"),
        ("2", "Wait a few seconds", "Not a full minute"),
        ("3", "If the SA comes up", "Stay on IPsec"),
        ("4", "If UDP 500/4500 dies", "Switch to TLS on 443"),
    ]
    boxes = columns(4, 150, 250)
    for i, ((x, y, w, h), item) in enumerate(zip(boxes, steps)):
        on = i == step
        ink = GREEN if i == 2 else AMBER if i == 3 else BLUE
        panel(d, x, y, w, h, (GREEN_SOFT if i == 2 else AMBER_SOFT if i == 3 else BLUE_SOFT) if on else WHITE, ink if on else LINE, width=4 if on else 2)
        center(d, x + w / 2, y + h / 2, [item[0], item[1], item[2]], F_P, INK if on else MUTED, gap=12)

    panel(d, 36, 430, 668, 290, GREEN_SOFT, GREEN)
    center(d, 370, 560, ["Same access policy", "Same address pool and DNS", "Same group routes", "Log which path was used"], F_P, GREEN, gap=12)
    d.text((60, 450), "Keep these the same", font=F_B, fill=GREEN)

    panel(d, 736, 430, 668, 290, RED_SOFT, RED)
    center(d, 1070, 575, ["Bad password", "Bad certificate", "Proposal mismatch", "MTU black hole"], F_P, RED, gap=12)
    d.text((760, 450), "Never fall back for these", font=F_B, fill=RED)
    footer(d, "IPsec first because it avoids TCP-inside-TCP. SSL because 443 is the door that opens.")
    return im


def q18(step):
    im, d = new("Q18", "Hotel user, packet by packet", "Same inner letter. Different gate pass.")
    nodes = [
        ("Laptop", "10.20.30.5"),
        ("Hotel NAT", "49.37.10.8"),
        ("BIG-IP", "203.0.113.10"),
        ("HR server", "10.1.1.50"),
    ]
    boxes = columns(4, 145, 120)
    for (x, y, w, h), (name, ip) in zip(boxes, nodes):
        panel(d, x, y, w, h, WHITE, NAVY)
        center(d, x + w / 2, y + h / 2, [name, ip], F_B, NAVY, gap=4)

    stories = [
        ["Memorise the four addresses.", "The virtual IP 10.50.1.20 appears only after login."],
        ["Attempt 1: IKE to UDP 500.", "Hotel rewrites the source to 49.37.10.8.", "The hotel firewall drops UDP 500 or 4500."],
        ["Attempt 2: TLS to TCP 443.", "The hotel allows it. It looks like HTTPS.", "The user signs in through the same access policy."],
        ["Inner packet: 10.50.1.20 → 10.1.1.50.", "Outer packet: 49.37.10.8 → 203.0.113.10.", "If IPsec had worked, the outer header would be UDP 4500 instead."],
    ]
    colors = [BLUE, RED, AMBER, GREEN]
    fills = [BLUE_SOFT, RED_SOFT, AMBER_SOFT, GREEN_SOFT]
    panel(d, 36, 300, 1368, 420, fills[step], colors[step])
    d.text((60, 325), f"Frame {step + 1} of 4", font=F_B, fill=colors[step])
    center(d, 720, 500, stories[step], F_H, NAVY, gap=18)
    footer(d)
    return im


def q19():
    im, d = new("Q19", "Three ways to prove identity", "You removed per-laptop certificates. You kept the gateway certificate.")
    cols = [
        ("Pre-shared key", AMBER, ["One secret on both ends", "", "Fine for two firewalls", "", "A group key on every laptop", "means one leak is everyone", "", "You cannot revoke one user"]),
        ("Client certificate", BLUE, ["Unique key on each laptop", "", "Strong device proof", "", "Issue, install, renew, revoke", "", "Painful at 10,000 laptops"]),
        ("EAP-MSCHAPv2", GREEN, ["Directory username + password", "", "Disable the account and", "access is gone", "", "Pair it with MFA", "Gateway still has a certificate"]),
    ]
    boxes = columns(3, 150, 560)
    for (x, y, w, h), (title, ink, lines) in zip(boxes, cols):
        panel(d, x, y, w, h, WHITE, ink)
        d.rectangle((x, y, x + w, y + 64), fill=ink)
        d.text((x + w / 2, y + 32), title, font=F_H, fill=WHITE, anchor="mm")
        center(d, x + w / 2, y + 320, lines, F_P, INK, gap=6)
    footer(d, "Say the tradeoff before the interviewer does: a password is weaker than a device certificate.")
    return im


def q20(step):
    im, d = new("Q20", "MSCHAPv2 challenge and response", "The password never travels. This runs inside encrypted IKE.")
    frames_title = ["Gateway sends a random challenge", "Laptop answers with a response, not the password", "Gateway proves it knows the password too"]
    left = [
        ["Challenge  →", "random number"],
        ["Check the response", "against the directory"],
        ["Success +", "gateway’s own proof"],
    ]
    right = [
        ["Password stays here", "Waiting"],
        ["Response + username", "Password still stays here"],
        ["Client checks the proof", "Both sides derive keys"],
    ]
    panel(d, 36, 160, 640, 500, BLUE_SOFT, BLUE)
    d.text((60, 185), "Gateway  /  APM", font=F_H, fill=BLUE)
    center(d, 356, 400, left[step], F_H, NAVY, gap=16)

    panel(d, 764, 160, 640, 500, GREEN_SOFT, GREEN)
    d.text((788, 185), "Laptop", font=F_H, fill=GREEN)
    center(d, 1084, 400, right[step], F_H, NAVY, gap=16)

    arrow(d, 690, 420, 750, 420, fill=NAVY)
    d.text((W / 2, 690), frames_title[step], font=F_B, fill=NAVY, anchor="mm")
    footer(d, "A café cannot see this. It is already inside the IKE SA. A fake gateway could, if the cert is not checked.")
    return im


def q21():
    im, d = new("Q21", "Where EAP sits", "Certificate first. Password second. User packets last.")
    steps = [
        ("1", "IKE_SA_INIT", "Diffie-Hellman. The rest of the handshake is encrypted. No login yet."),
        ("2", "Gateway certificate", "Client checks the name, the dates, and the CA. This closes the fake-gateway hole."),
        ("3", "EAP-MSCHAPv2", "Challenge and response inside IKE_AUTH. APM checks the directory and can demand MFA."),
        ("4", "Child SA", "Virtual IP is assigned. Only now do application packets flow."),
    ]
    y = 140
    colors = [BLUE, NAVY, GREEN, TEAL]
    for (num, title, body), ink in zip(steps, colors):
        panel(d, 36, y, 1368, 140, WHITE, ink)
        d.rounded_rectangle((56, y + 40, 120, y + 100), 12, fill=ink)
        d.text((88, y + 70), num, font=F_H, fill=WHITE, anchor="mm")
        d.text((146, y + 42), title, font=F_H, fill=ink)
        d.text((146, y + 86), body, font=F_P, fill=INK)
        y += 152
    footer(d)
    return im


def q22():
    im, d = new("Q22", "What the admin stops doing", "Joiners and leavers stay in the directory.")
    scenes = [
        ("New hire", GREEN, ["Enable the account", "Add the VPN group", "They type password + MFA", "No ticket to the PKI team"]),
        ("Lost laptop", RED, ["Disable the account", "Next IKE_AUTH fails", "You do not wait for a", "revocation list to propagate"]),
        ("Re-image", BLUE, ["Standard image has the client", "and the company CA", "No unique certificate", "to back up and restore"]),
    ]
    boxes = columns(3, 145, 360)
    for (x, y, w, h), (title, ink, lines) in zip(boxes, scenes):
        panel(d, x, y, w, h, WHITE, ink)
        d.text((x + 24, y + 24), title, font=F_H, fill=ink)
        center(d, x + w / 2, y + 210, lines, F_P, INK, gap=12)
    panel(d, 36, 530, 1368, 200, AMBER_SOFT, AMBER)
    center(d, 720, 630, ["Still required: one gateway certificate, the company CA on the image,", "the access policy, NAT-T on, and SSL fallback on."], F_B, AMBER, gap=12)
    footer(d)
    return im


def q23():
    im, d = new("Q23", "Attacks to volunteer", "Name the risk and the control in the same breath.")
    rows = [
        ("Fake gateway", "Attacker finishes DH and collects EAP", "Client checks the gateway certificate first"),
        ("Stolen password", "Attacker logs in as the user", "MFA, and disabling that one account"),
        ("Group pre-shared key", "One image leaks everyone’s key", "Remote access uses EAP, not a group PSK"),
        ("Weak algorithms", "Peer offers 3DES or DH group 2", "Default is AES-GCM and group 19 or 20"),
        ("Replayed ESP packet", "Old packet sent again", "ESP sequence numbers"),
        ("Record now, steal cert later", "Archive decrypted next year", "PFS on the child SA"),
    ]
    y = 132
    for attack, how, control in rows:
        panel(d, 28, y, 1384, 100, WHITE, LINE, width=2)
        d.text((48, y + 28), attack, font=F_B, fill=RED)
        d.text((48, y + 62), how, font=F_S, fill=MUTED)
        d.text((760, y + 50), control, font=F_B, fill=GREEN, anchor="lm")
        y += 108
    footer(d)
    return im


def q24():
    im, d = new("Q24", "Connected, but the app fails", "Stop at the first layer that is wrong.")
    steps = [
        ("1  Path", "UDP 500, UDP 4500, TCP 443. Timeout on UDP only → fallback case."),
        ("2  IKE log", "No proposal. Auth failed. Selector mismatch. NAT-T off."),
        ("3  Both SAs", "Two directions. Outbound growing, inbound stuck at zero → return path."),
        ("4  Inner network", "Virtual IP, return route, internal DNS, policy after decrypt."),
        ("5  Big packets only", "64-byte ping works, 1400-byte ping fails → MTU. Clamp TCP MSS."),
    ]
    y = 140
    for i, (title, body) in enumerate(steps):
        panel(d, 36, y, 1368, 112, WHITE, BLUE if i < 4 else AMBER)
        d.text((60, y + 30), title, font=F_H, fill=NAVY)
        d.text((60, y + 72), body, font=F_P, fill=INK)
        y += 124
    footer(d)
    return im


def q25(step):
    im, d = new("Q25", "MOBIKE", "The login survives a change of IP. A site-to-site tunnel does not need this.")
    places = [("Office Wi-Fi", "49.37.10.8"), ("Walk outside", "SA still valid"), ("LTE", "106.20.4.9")]
    boxes = columns(3, 160, 220)
    for i, ((x, y, w, h), (name, ip)) in enumerate(zip(boxes, places)):
        on = i <= step
        panel(d, x, y, w, h, GREEN_SOFT if on else WHITE, GREEN if on else LINE, width=4 if i == step else 2)
        center(d, x + w / 2, y + h / 2, [name, ip], F_H, GREEN if on else MUTED, gap=12)
    if step >= 1:
        arrow(d, boxes[0][0] + boxes[0][2] + 4, 270, boxes[1][0] - 4, 270, fill=GREEN)
    if step >= 2:
        arrow(d, boxes[1][0] + boxes[1][2] + 4, 270, boxes[2][0] - 4, 270, fill=GREEN)
    panel(d, 36, 430, 1368, 290, WHITE, NAVY)
    notes = [
        "The client is on Wi-Fi. IKE SA and child SA are up. EAP already finished.",
        "Without MOBIKE the old NAT mapping dies and DPD eventually kills the SA.",
        "The client proves it still owns this IKE SA and the gateway sends ESP to the new address.",
    ]
    center(d, 720, 575, wrap_text(d, notes[step], F_H, 1200), F_H, NAVY, gap=8)
    footer(d, "Users call the no-MOBIKE version “random disconnects on the commute.”")
    return im


def q26():
    im, d = new("Q26", "Policy-based versus route-based", "Selectors versus a road with signs.")
    panel(d, 36, 150, 670, 560, WHITE, AMBER)
    d.text((60, 175), "Policy-based", font=F_H, fill=AMBER)
    center(d, 370, 400, ["Encrypt whatever matches", "a traffic selector.", "", "“10.1.0.0/16 to 10.2.0.0/16", "goes to peer X.”", "", "A new subnet means editing", "selectors on both ends.", "They must be exact mirrors."], F_P, INK, gap=6)

    panel(d, 734, 150, 670, 560, WHITE, GREEN)
    d.text((758, 175), "Route-based", font=F_H, fill=GREEN)
    center(d, 1068, 400, ["A virtual tunnel interface.", "Routes point prefixes at it.", "", "Adding Pune is a route,", "which network teams already", "know how to review.", "", "BGP can sit on the interface.", "Remote access pushes routes", "to the client adapter."], F_P, INK, gap=6)
    footer(d, "GRE over IPsec was the older way to give routing an interface. VTI replaced a lot of it.")
    return im


def q27():
    im, d = new("Q27", "Anti-replay and lifetimes", "A stolen data key opens a window, not the whole history.")
    panel(d, 36, 150, 670, 400, WHITE, RED)
    d.text((60, 175), "Anti-replay", font=F_H, fill=RED)
    center(d, 370, 340, ["Each ESP packet has a sequence number.", "The receiver remembers a recent window.", "A repeat of an old number is dropped.", "", "This stops a resent packet.", "It does not stop a thief who has the key", "and can build a fresh number."], F_P, INK, gap=8)

    panel(d, 734, 150, 670, 400, WHITE, BLUE)
    d.text((758, 175), "Lifetimes + PFS", font=F_H, fill=BLUE)
    center(d, 1068, 340, ["Example you can say:", "IKE SA 8 hours.", "Child SA 1 hour.", "PFS group 19.", "", "The child expires first.", "The user does not log in again at rekey."], F_P, INK, gap=8)

    panel(d, 36, 575, 1368, 150, AMBER_SOFT, AMBER)
    center(d, 720, 650, ["Rekey storm: every tunnel came up at 09:00 and rekeys at 10:00. Jitter the lifetimes."], F_B, AMBER)
    footer(d)
    return im


def q28():
    im, d = new("Q28", "What to monitor", "“IKE is running” is not monitoring.")
    tiles = [
        ("IKE failures by reason", "Bad password, mismatch, or timeout"),
        ("SSL fallback rate", "A jump means UDP started dying"),
        ("Active SAs", "Capacity and rekey storms"),
        ("Address-pool usage", "Auth can succeed and still fail"),
        ("Gateway certificate expiry", "One expiry fails every EAP user"),
        ("Replay drops", "Attack, or a peer after failover"),
        ("Decrypt failures", "Wrong SA or broken peer"),
        ("CPU during ESP", "Why the default is AES-GCM"),
    ]
    for i, (title, body) in enumerate(tiles):
        col, row = i % 4, i // 4
        x = 28 + col * 352
        y = 145 + row * 280
        panel(d, x, y, 336, 250, WHITE, BLUE if row == 0 else TEAL)
        center(d, x + 168, y + 110, wrap_text(d, title, F_B, 290), F_B, NAVY, gap=4)
        center(d, x + 168, y + 185, wrap_text(d, body, F_P, 290), F_P, MUTED, gap=4)
    footer(d)
    return im


def q29():
    im, d = new("Q29", "Gateway reboot", "The tunnel is rebuilt. In-flight TCP does not have to survive.")
    steps = [
        ("1", "Active gateway reboots", "SAs lived in memory. They are gone."),
        ("2", "Client DPD fails", "The peer does not answer the liveness check."),
        ("3", "New IKE to the standby", "Same virtual IP, if failover moved it."),
        ("4", "New connections work", "Old downloads may break. Say that plainly."),
    ]
    boxes = columns(4, 160, 420)
    colors = [RED, AMBER, BLUE, GREEN]
    for (x, y, w, h), item, ink in zip(boxes, steps, colors):
        panel(d, x, y, w, h, WHITE, ink)
        d.text((x + w / 2, y + 50), item[0], font=F_TITLE, fill=ink, anchor="mt")
        center(d, x + w / 2, y + 220, wrap_text(d, item[1], F_H, w - 40) + [""] + wrap_text(d, item[2], F_P, w - 40), F_P, INK, gap=10)
    footer(d, "Two gateways both answering IKE is split brain. One owner of the virtual IP.")
    return im


def q30():
    im, d = new("Q30", "20-minute mock round", "Short answers only. Then redo the two you stumbled on.")
    groups = [
        ("Basics", "Q1–Q7", BLUE, ["Four properties", "ESP, not AH", "Tunnel mode", "What the client gets", "Why keep both VPNs"]),
        ("Handshake", "Q8–Q13", TEAL, ["Three beats", "DH does not prove identity", "PFS", "The six config objects"]),
        ("Resume", "Q14–Q23", GREEN, ["NAT and UDP 4500", "When not to fall back", "Hotel addresses", "Why EAP, where it sits"]),
        ("Debug", "Q24–Q29", AMBER, ["Five-layer debug", "MTU signature", "Fallback-rate jump", "Failover is honest"]),
    ]
    boxes = columns(4, 155, 540)
    for (x, y, w, h), (title, qs, ink, lines) in zip(boxes, groups):
        panel(d, x, y, w, h, WHITE, ink)
        d.rectangle((x, y, x + w, y + 90), fill=ink)
        center(d, x + w / 2, y + 45, [title, qs], F_B, WHITE, gap=4)
        center(d, x + w / 2, y + 320, lines, F_P, INK, gap=16)
    footer(d, "If a rapid-fire answer takes more than a minute, reopen only that story.")
    return im


def main():
    pngs = {
        "q01b-esp-header": q01b,
        "q02-why-ipsec": q02,
        "q03-esp-vs-ah": q03,
        "q04-tunnel-vs-transport": q04,
        "q05-what-the-laptop-gets": q05,
        "q06-ipsec-vs-ssl": q06,
        "q07-building-blocks": q07,
        "q10-proposal-mismatch": q10,
        "q11-ike-versions": q11,
        "q12-pfs": q12,
        "q13-config-objects": q13,
        "q15-ports": q15,
        "q16-path-versus-auth": q16,
        "q19-auth-methods": q19,
        "q21-where-eap-sits": q21,
        "q22-admin-work": q22,
        "q23-attacks": q23,
        "q24-debug-ladder": q24,
        "q26-policy-vs-route": q26,
        "q27-replay-and-lifetime": q27,
        "q28-monitoring": q28,
        "q29-failover": q29,
        "q30-mock-round": q30,
    }
    for stem, fn in pngs.items():
        save_png(fn(), stem)
        print("png", stem)

    gifs = {
        "q01-what-is-ipsec": [q01(i) for i in range(3)],
        "q08-handshake": [q08(i) for i in range(3)],
        "q09-diffie-hellman": [q09(i) for i in range(4)],
        "q14-nat": [q14(i) for i in range(3)],
        "q17-fallback": [q17(i) for i in range(4)],
        "q18-hotel-walkthrough": [q18(i) for i in range(4)],
        "q20-mschapv2": [q20(i) for i in range(3)],
        "q25-mobike": [q25(i) for i in range(3)],
    }
    for stem, frames in gifs.items():
        save_gif(frames, stem)
        print("gif", stem)

    tmp = ROOT / "_tmp"
    if tmp.exists():
        shutil.rmtree(tmp)


if __name__ == "__main__":
    main()
