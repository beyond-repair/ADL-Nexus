extends Node
## Multi-agent message bus. Agents hear the user and can reply to each other.

signal agent_spoke(agent_id: String, line: String)
signal party_event(msg: String)

class Agent:
	var id: String
	var display_name: String
	var role: String
	var color: Color
	var personality: String
	func _init(p_id: String, p_name: String, p_role: String, p_color: Color, p_personality: String) -> void:
		id = p_id
		display_name = p_name
		role = p_role
		color = p_color
		personality = p_personality

var agents: Dictionary = {}

func setup_default_party() -> void:
	_add(Agent.new("engineer", "Cid", "Engineer", Color(0.35, 0.75, 1.0), "pragmatic builder"))
	_add(Agent.new("researcher", "Vivi", "Researcher", Color(0.7, 0.45, 1.0), "curious theorist"))
	_add(Agent.new("writer", "Garnet", "Writer", Color(1.0, 0.55, 0.75), "clear narrator"))
	_add(Agent.new("analyst", "Quina", "Analyst", Color(0.4, 0.9, 0.55), "metrics minded"))
	_add(Agent.new("tester", "Steiner", "Tester", Color(0.95, 0.7, 0.3), "fail-closed skeptic"))
	_add(Agent.new("operator", "Freya", "Operator", Color(0.55, 0.7, 0.95), "keeps systems up"))
	_add(Agent.new("manager", "Zidane", "Manager", Color(1.0, 0.85, 0.35), "prioritizes and routes"))

func _add(a: Agent) -> void:
	agents[a.id] = a

func get_agents() -> Array:
	return agents.values()

func get_agent(id: String) -> Agent:
	return agents.get(id)

func handle_user_message(text: String) -> void:
	var lower := text.to_lower()
	# Direct @mention
	for id in agents.keys():
		if lower.begins_with("{0} ".format(["@" + id])) or lower.begins_with("{0},".format(["@" + id])):
			var rest := text.substr(id.length() + 1).strip_edges()
			await _agent_reply(id, rest, true)
			return
	# Party debate mode — agents respond to each other
	if "party debate" in lower or "debate" in lower:
		var topic := text
		for key in ["party debate", "debate"]:
			var idx := lower.find(key)
			if idx >= 0:
				topic = text.substr(idx + key.length()).strip_edges()
				break
		if topic.is_empty():
			topic = "the current mission"
		party_event.emit("Party debate: %s" % topic)
		await _debate(topic)
		return
	# Default: manager routes, then one specialist answers, tester may challenge
	await _agent_reply("manager", text, false)
	var target := _route(text)
	await _agent_reply(target, text, false)
	if randf() < 0.45:
		await _agent_reply("tester", "Challenge to %s: how do we verify that?" % agents[target].display_name, false)
		await _agent_reply(target, _verify_line(target), false)

func _route(text: String) -> String:
	var l := text.to_lower()
	if "test" in l or "bug" in l or "fail" in l:
		return "tester"
	if "research" in l or "hypothesis" in l or "cft" in l or "sparc" in l or "physics" in l:
		return "researcher"
	if "metric" in l or "number" in l or "χ" in l or "chi" in l:
		return "analyst"
	if "write" in l or "doc" in l or "readme" in l:
		return "writer"
	if "deploy" in l or "ops" in l or "uptime" in l:
		return "operator"
	if "code" in l or "build" in l or "refactor" in l or "apk" in l or "godot" in l:
		return "engineer"
	return "engineer"

func _debate(topic: String) -> void:
	await _agent_reply("manager", "We debate: %s. Researcher first." % topic, false)
	await _agent_reply("researcher", _research_take(topic), false)
	await _agent_reply("analyst", _analyst_take(topic), false)
	await _agent_reply("tester", "I need a falsifiable check before we lock any claim.", false)
	await _agent_reply("engineer", "If we implement, we keep it local-first and claim-capped.", false)
	await _agent_reply("writer", "Summary: open questions stay open until evidence lands.", false)
	await _agent_reply("manager", "Decision: log hypothesis in Research Fabric; no claim inflation.", false)

func _agent_reply(id: String, user_text: String, direct: bool) -> void:
	if not agents.has(id):
		return
	var a: Agent = agents[id]
	var line := _compose(a, user_text, direct)
	# Small delay so multi-agent turns feel conversational
	await get_tree().create_timer(0.35).timeout
	agent_spoke.emit(id, line)

func _compose(a: Agent, user_text: String, direct: bool) -> String:
	match a.id:
		"manager":
			return "Routing under governance. Focus: %s" % (user_text if user_text.length() < 80 else user_text.substr(0, 77) + "...")
		"engineer":
			return "I'll treat that as an engineering task. Local-first, tests before merge. %s" % ("On it." if direct else "")
		"researcher":
			return _research_take(user_text)
		"writer":
			return "I can draft a clear note for the log: goal, constraints, next evidence."
		"analyst":
			return _analyst_take(user_text)
		"tester":
			return "Fail-closed: what is the acceptance test, and what would falsify success?"
		"operator":
			return "Ops view: keep offline path green; no new network dependency without audit."
		_:
			return "Acknowledged."

func _research_take(topic: String) -> String:
	var t := topic.to_lower()
	if "sparc" in t or "chi" in t or "χ" in t:
		return "SPARC median χ²_red ~9.1 is still open; macro r0(Mb) must stay locked while we hunt residual structure."
	if "bullet" in t:
		return "Bullet simple r0/c fails; Model D (ξ cluster scale) is the open candidate that preserves the galactic lock."
	if "ware" in t or "w_star" in t or "cft" in t:
		return "W★ = 1/(4π) under Option A is the locked phenomenological anchor; M2 stays geometric-only."
	return "Hypothesis logged. Evidence before claim-level advance — Research Fabric discipline."

func _analyst_take(topic: String) -> String:
	return "Numbers first: separate locked constants from free parameters. If χ² stays high, report it; don't hide it."

func _verify_line(target_id: String) -> String:
	return "Verification plan: unit test + offline smoke + claim status unchanged unless gates pass."
