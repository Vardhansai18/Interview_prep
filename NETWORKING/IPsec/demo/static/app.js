const NODES = {
  laptop: { x: 160, y: 300, title: "Laptop", addr: "10.20.30.5" },
  hotel: { x: 470, y: 200, title: "Hotel NAT", addr: "49.37.10.8" },
  gateway: { x: 900, y: 220, title: "BIG-IP", addr: "203.0.113.10" },
  hr: { x: 1040, y: 430, title: "HR server", addr: "10.1.1.50" },
};

const stage = document.querySelector("#stage");
const caption = document.querySelector("#caption");
const sceneNav = document.querySelector("#scenes");
const form = document.querySelector("#scenario");

let scenes = [];
let sceneId = "vpn";
let runToken = 0;

function quad(a, control, b, reverse, steps = 28) {
  const points = [];
  for (let i = 0; i <= steps; i += 1) {
    const t = reverse ? 1 - i / steps : i / steps;
    const u = 1 - t;
    points.push({
      x: u * u * a.x + 2 * u * t * control.x + t * t * b.x,
      y: u * u * a.y + 2 * u * t * control.y + t * t * b.y,
    });
  }
  return points;
}

function tunnelPoints(reverse) {
  return quad(NODES.laptop, { x: 530, y: 70 }, NODES.gateway, reverse);
}

function hopPoints(a, b, viaTunnel) {
  const tunnelHop = (a === "laptop" && b === "gateway") || (a === "gateway" && b === "laptop");
  if (viaTunnel && tunnelHop) return tunnelPoints(a === "gateway");
  return [NODES[a], NODES[b]];
}

function ridePoints(phase) {
  if (phase.ride === "bounce") {
    const over = tunnelPoints(false);
    const back = tunnelPoints(true);
    return over.concat(back).concat(over);
  }
  const viaTunnel = Boolean(phase.tunnel) && !phase.block;
  const ids = phase.ride;
  let points = [NODES[ids[0]]];
  for (let i = 0; i < ids.length - 1; i += 1) {
    const segment = hopPoints(ids[i], ids[i + 1], viaTunnel);
    points = points.concat(segment.slice(1));
  }
  return points;
}

function packetFace(style) {
  if (style === "open") return { fill: "#fff", stroke: "#b91c1c", text: "HR", ink: "#b91c1c" };
  if (style === "tls") return { fill: "#ea580c", stroke: "#9a3412", text: "443", ink: "#fff" };
  if (style === "key") return { fill: "#1d4ed8", stroke: "#1e3a8a", text: "IKE", ink: "#fff" };
  if (style === "inner") return { fill: "#047857", stroke: "#064e3b", text: "10.50", ink: "#fff" };
  if (style === "plain") return { fill: "#1d4ed8", stroke: "#1e3a8a", text: "VPN", ink: "#fff" };
  return { fill: "#1d4ed8", stroke: "#1e3a8a", text: "ESP", ink: "#fff" };
}

function drawMap(phase) {
  const tunnel = phase.tunnel;
  const block = phase.block;
  const face = packetFace(phase.style);
  stage.innerHTML = `
    <svg class="map" viewBox="0 0 1200 560" role="img" aria-label="Network path from the café laptop to the HR server">
      <rect class="zone cafe" x="30" y="80" width="250" height="430" rx="24"></rect>
      <rect class="zone net" x="310" y="80" width="360" height="220" rx="80"></rect>
      <rect class="zone office" x="760" y="80" width="400" height="430" rx="24"></rect>
      <text class="zone-label" x="52" y="110">CAFÉ</text>
      <text class="zone-label" x="430" y="118">INTERNET</text>
      <text class="zone-label" x="782" y="110">OFFICE</text>

      <path class="link ${block ? "blocked" : "hot"}" d="M160 270 Q300 210 470 210"></path>
      <path class="link ${block ? "blocked" : ""}" d="M520 190 Q700 150 860 210"></path>
      <path class="link" d="M940 260 L1020 400"></path>
      ${tunnel ? `<path class="tunnel ${tunnel.kind}" d="M160 250 Q530 55 900 170"></path>` : ""}
      ${tunnel ? `<text class="tunnel-label" x="500" y="58" text-anchor="middle">${tunnel.label}</text>` : ""}

      ${node("laptop")}
      ${node("hotel")}
      ${node("gateway")}
      ${node("hr")}
      <g id="packet" transform="translate(160 300)">
        <rect x="-28" y="-18" width="56" height="36" rx="8" fill="${face.fill}" stroke="${face.stroke}" stroke-width="2"></rect>
        <text class="packet-label" text-anchor="middle" y="5" fill="${face.ink}">${face.text}</text>
      </g>
      <text id="drop" class="drop-x" text-anchor="middle" visibility="hidden">×</text>
    </svg>
  `;
}

function node(id) {
  const n = NODES[id];
  const shapes = {
    laptop: `<rect x="-34" y="-26" width="68" height="44" rx="6" fill="white" stroke="#0f2340" stroke-width="2"></rect><rect x="-22" y="20" width="44" height="6" rx="2" fill="#0f2340"></rect>`,
    hotel: `<rect x="-26" y="-30" width="52" height="56" rx="4" fill="white" stroke="#0f2340" stroke-width="2"></rect><path d="M-26 -8 H26 M-26 12 H26 M-8 -30 V26 M8 -30 V26" stroke="#94a3b8"></path>`,
    gateway: `<path d="M0 -34 L30 -16 V20 H-30 V-16 Z" fill="white" stroke="#0f2340" stroke-width="2"></path>`,
    hr: `<rect x="-28" y="-32" width="56" height="18" rx="3" fill="white" stroke="#0f2340"></rect><rect x="-28" y="-8" width="56" height="18" rx="3" fill="white" stroke="#0f2340"></rect><rect x="-28" y="16" width="56" height="18" rx="3" fill="white" stroke="#0f2340"></rect>`,
  };
  return `
    <g transform="translate(${n.x} ${n.y})">
      ${shapes[id]}
      <text class="node-title" text-anchor="middle" y="58">${n.title}</text>
      <text class="node-addr" text-anchor="middle" y="76">${n.addr}</text>
    </g>
  `;
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function glide(points, token) {
  const packet = document.querySelector("#packet");
  if (!packet || points.length < 2) return;
  const duration = 1400;
  const start = performance.now();
  await new Promise((resolve) => {
    function frame(now) {
      if (token !== runToken) return resolve();
      const t = Math.min(1, (now - start) / duration);
      const index = Math.min(points.length - 1, t * (points.length - 1));
      const i = Math.floor(index);
      const f = index - i;
      const a = points[i];
      const b = points[Math.min(points.length - 1, i + 1)];
      const x = a.x + (b.x - a.x) * f;
      const y = a.y + (b.y - a.y) * f;
      packet.setAttribute("transform", `translate(${x} ${y})`);
      if (t < 1) requestAnimationFrame(frame);
      else resolve();
    }
    requestAnimationFrame(frame);
  });
}

async function playPhase(phase, token) {
  if (token !== runToken) return;
  caption.textContent = phase.caption;
  drawMap(phase);
  const unwrap = phase.unwrap && Array.isArray(phase.ride) && phase.ride.includes("hr");
  const points = unwrap ? ridePoints({ ...phase, ride: phase.ride.filter((id) => id !== "hr") }) : ridePoints(phase);
  await glide(points, token);
  if (token !== runToken) return;
  if (unwrap) {
    const packet = document.querySelector("#packet text");
    const rect = document.querySelector("#packet rect");
    if (packet && rect) {
      packet.textContent = "10.50";
      packet.setAttribute("fill", "#fff");
      rect.setAttribute("fill", "#047857");
      rect.setAttribute("stroke", "#064e3b");
    }
    await glide([NODES.gateway, NODES.hr], token);
  }
  if (phase.drop) {
    const spot = NODES[phase.drop];
    const mark = document.querySelector("#drop");
    if (mark) {
      mark.setAttribute("x", spot.x);
      mark.setAttribute("y", spot.y - 48);
      mark.setAttribute("visibility", "visible");
    }
    await sleep(700);
  }
}

async function play(phases) {
  const token = ++runToken;
  while (token === runToken) {
    for (const phase of phases) {
      await playPhase(phase, token);
      if (token !== runToken) return;
      await sleep(500);
    }
    await sleep(600);
  }
}

function selectScene(id) {
  sceneId = id;
  sceneNav.querySelectorAll("button").forEach((button) => {
    const on = button.dataset.scene === id;
    button.classList.toggle("on", on);
    button.setAttribute("aria-pressed", String(on));
  });
  const scene = scenes.find((item) => item.id === id);
  play(scene.phases);
}

async function load() {
  const response = await fetch("/api/story");
  const data = await response.json();
  scenes = data.scenes;
  sceneNav.innerHTML = scenes.map((scene) => `
    <button type="button" data-scene="${scene.id}" aria-pressed="false">${scene.label}</button>
  `).join("");
  sceneNav.querySelectorAll("button").forEach((button) => {
    button.addEventListener("click", () => selectScene(button.dataset.scene));
  });
  selectScene("vpn");
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  sceneNav.querySelectorAll("button").forEach((button) => {
    button.classList.remove("on");
    button.setAttribute("aria-pressed", "false");
  });
  const body = Object.fromEntries(new FormData(form).entries());
  const response = await fetch("/api/trace", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const result = await response.json();
  play(result.phases);
});

load().catch(() => {
  caption.textContent = "Start the demo with python3 server.py, then refresh this page.";
});
