const canvas = document.getElementById("c");
const ctx = canvas.getContext("2d");

function resize() {
  canvas.width = window.innerWidth + 50;
  canvas.height = window.innerHeight + 50;
}
resize();
window.addEventListener("resize", resize);

const TOTAL = 500;
const radius = 300;
const particles = [];
const mouse = { x: null, y: null };

window.addEventListener("mousemove", e => {
  mouse.x = e.clientX;
  mouse.y = e.clientY;
});

for (let i = 0; i < TOTAL; i++) {
  const homeX = Math.random() * canvas.width;
  const homeY = Math.random() * canvas.height;
  particles.push({
    x: homeX,
    y: homeY,
    homeX,
    homeY,
    vx: (Math.random() - 0.5) * 0.2,
    vy: (Math.random() - 0.5) * 0.2,
    s: Math.random() * 3 + 1,
    offsetX: Math.random() * 1000,
    offsetY: Math.random() * 1000
  });
}

function lerp(a, b, t) {
  return a + (b - a) * t;
}

function draw() {
  ctx.fillStyle = "rgba(0,0,0,0.2)";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  const time = Date.now() * 0.002;

  particles.forEach(p => {
    const driftX = Math.sin(time + p.offsetX) * 0.2;
    const driftY = Math.cos(time + p.offsetY) * 0.2;

    if (mouse.x !== null) {
      const dx = mouse.x - p.x;
      const dy = mouse.y - p.y;
      const dist = Math.sqrt(dx*dx + dy*dy);

      if (dist < radius) {
        p.x = lerp(p.x, mouse.x, 0.001) + driftX;
        p.y = lerp(p.y, mouse.y, 0.001) + driftY;
      } else {
        p.x = lerp(p.x, p.homeX, 0.02) + driftX;
        p.y = lerp(p.y, p.homeY, 0.02) + driftY;
      }
    } else {
      p.x = lerp(p.x, p.homeX, 0.02) + driftX;
      p.y = lerp(p.y, p.homeY, 0.02) + driftY;
    }

    p.x += p.vx;
    p.y += p.vy;

    p.vx *= 0.98;
    p.vy *= 0.98;

    ctx.fillStyle = "white";
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.s, 0, Math.PI * 2);
    ctx.fill();
  });

  requestAnimationFrame(draw);
}

draw();
