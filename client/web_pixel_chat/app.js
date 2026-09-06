const logEl = document.getElementById("log");
const partyEl = document.getElementById("party");
const form = document.getElementById("form");
const input = document.getElementById("input");

function renderParty() {
  partyEl.innerHTML = "";
  AGENTS.forEach((a) => {
    const card = document.createElement("div");
    card.className = "agent-card";
    card.dataset.id = a.id;
    card.innerHTML = `<div class="swatch" style="background:${a.color}"></div>
      <div class="name">${a.name}</div>
      <div class="role">${a.role}</div>`;
    partyEl.appendChild(card);
  });
}

function append(who, text, color, system = false) {
  const div = document.createElement("div");
  div.className = "msg" + (system ? " system" : "");
  if (system) {
    div.textContent = text;
  } else {
    div.innerHTML = `<div class="who" style="color:${color}">${who}</div><div>${escapeHtml(text)}</div>`;
  }
  logEl.appendChild(div);
  logEl.scrollTop = logEl.scrollHeight;
}

function escapeHtml(s) {
  return s.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

function pulse(id) {
  const card = partyEl.querySelector(`[data-id="${id}"]`);
  if (!card) return;
  card.classList.add("pulse");
  setTimeout(() => card.classList.remove("pulse"), 280);
}

function speak(id, text) {
  return new Promise((resolve) => {
    setTimeout(() => {
      const a = AGENTS.find((x) => x.id === id);
      append(a.name, text, a.color);
      pulse(id);
      resolve();
    }, 320);
  });
}

async function handleUser(text) {
  append("You", text, "#a8c7ff");
  const lower = text.toLowerCase();

  const mention = AGENTS.find((a) => lower.startsWith("@" + a.id));
  if (mention) {
    const rest = text.slice(mention.id.length + 1).trim();
    await speak(mention.id, compose(mention, rest || text));
    return;
  }

  if (lower.includes("party debate") || lower.startsWith("debate")) {
    let topic = text.replace(/party debate/i, "").replace(/debate/i, "").trim() || "the mission";
    append("", "Party debate: " + topic, "", true);
    await speak("manager", "We debate: " + topic + ". Researcher first.");
    await speak("researcher", researchTake(topic));
    await speak("analyst", compose(AGENTS.find((a) => a.id === "analyst"), topic));
    await speak("tester", "I need a falsifiable check before we lock any claim.");
    await speak("engineer", "If we implement, local-first and claim-capped.");
    await speak("writer", "Summary: open questions stay open until evidence lands.");
    await speak("manager", "Decision: log hypothesis; no claim inflation.");
    return;
  }

  await speak("manager", compose(AGENTS.find((a) => a.id === "manager"), text));
  const target = route(text);
  await speak(target, compose(AGENTS.find((a) => a.id === target), text));
  if (Math.random() < 0.45) {
    await speak("tester", "Challenge: how do we verify that?");
    await speak(target, "Verification: unit test + offline smoke + claim status unchanged unless gates pass.");
  }
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;
  input.value = "";
  handleUser(text);
});

renderParty();
append("", "Welcome. Try: @researcher SPARC residual  |  party debate Ware Constant", "", true);
