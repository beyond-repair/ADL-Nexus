const AGENTS = [
  { id: "engineer", name: "Cid", role: "Engineer", color: "#59bfff" },
  { id: "researcher", name: "Vivi", role: "Researcher", color: "#b36bff" },
  { id: "writer", name: "Garnet", role: "Writer", color: "#ff8cb8" },
  { id: "analyst", name: "Quina", role: "Analyst", color: "#6ee7a0" },
  { id: "tester", name: "Steiner", role: "Tester", color: "#f0b429" },
  { id: "operator", name: "Freya", role: "Operator", color: "#8cb4ff" },
  { id: "manager", name: "Zidane", role: "Manager", color: "#ffd85c" },
];

function route(text) {
  const l = text.toLowerCase();
  if (/test|bug|fail/.test(l)) return "tester";
  if (/research|hypothesis|cft|sparc|physics|ware/.test(l)) return "researcher";
  if (/metric|number|chi|χ/.test(l)) return "analyst";
  if (/write|doc|readme/.test(l)) return "writer";
  if (/deploy|ops|uptime/.test(l)) return "operator";
  if (/code|build|refactor|apk|godot/.test(l)) return "engineer";
  return "engineer";
}

function researchTake(topic) {
  const t = topic.toLowerCase();
  if (/sparc|chi|χ/.test(t))
    return "SPARC median χ²_red ~9.1 is still open; keep macro r0(Mb) locked.";
  if (/bullet/.test(t))
    return "Bullet simple r0/c fails; Model D (cluster ξ) stays the open candidate.";
  if (/ware|w_star|cft/.test(t))
    return "W★ = 1/(4π) under Option A is locked; M2 is geometric-only.";
  return "Hypothesis noted. Evidence before any claim-level advance.";
}

function compose(agent, userText) {
  switch (agent.id) {
    case "manager":
      return "Routing under governance. Focus: " + userText.slice(0, 80);
    case "engineer":
      return "Engineering frame: local-first, tests before merge.";
    case "researcher":
      return researchTake(userText);
    case "writer":
      return "I can draft a clear log: goal, constraints, next evidence.";
    case "analyst":
      return "Numbers first — separate locked constants from free parameters.";
    case "tester":
      return "Fail-closed: what is the acceptance test, and what falsifies success?";
    case "operator":
      return "Ops: keep offline path green; no silent network dependency.";
    default:
      return "Acknowledged.";
  }
}
