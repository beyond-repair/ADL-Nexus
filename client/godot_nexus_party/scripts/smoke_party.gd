extends SceneTree
## Headless smoke: @mention, party debate, manager-route specialist.
## Run: godot --headless --path . --script res://scripts/smoke_party.gd

var _failures: PackedStringArray = []
var _spoke: PackedStringArray = []
var _events: PackedStringArray = []

func _initialize() -> void:
	call_deferred("_run")

func _run() -> void:
	var bus_script = load("res://scripts/AgentBus.gd")
	if bus_script == null:
		_fail("load AgentBus.gd")
		_finish(1)
		return
	var bus: Node = bus_script.new()
	root.add_child(bus)
	bus.reply_delay = 0.0
	bus.setup_default_party()
	bus.agent_spoke.connect(func(id: String, _line: String): _spoke.append(id))
	bus.party_event.connect(func(msg: String): _events.append(msg))

	var agents: Array = bus.get_agents()
	_assert(agents.size() == 7, "party size == 7 (got %s)" % agents.size())
	_assert(bus.get_agent("engineer") != null, "engineer present")
	_assert(bus.get_agent("manager").display_name == "Zidane", "manager is Zidane")

	# PartyBar setup / pulse without Main scene
	var bar_script = load("res://scripts/PartyBar.gd")
	var bar: HBoxContainer = bar_script.new()
	root.add_child(bar)
	bar.setup(agents)
	_assert(bar.slot_count() == 7, "PartyBar slots == 7")
	bar.pulse("engineer")
	# Re-setup must not leak children
	bar.setup(agents)
	_assert(bar.get_child_count() == 7, "PartyBar child_count after re-setup == 7")
	_assert(bar.slot_count() == 7, "PartyBar slots after re-setup == 7")

	# @mention exact
	_spoke.clear()
	await bus.handle_user_message("@engineer")
	_assert(_spoke == PackedStringArray(["engineer"]), "@engineer → engineer only (got %s)" % ",".join(_spoke))

	# @mention with comma rest
	_spoke.clear()
	await bus.handle_user_message("@researcher, check SPARC residual")
	_assert(_spoke == PackedStringArray(["researcher"]), "@researcher, … → researcher (got %s)" % ",".join(_spoke))

	# @mention with space rest
	_spoke.clear()
	await bus.handle_user_message("@tester verify acceptance")
	_assert(_spoke == PackedStringArray(["tester"]), "@tester … → tester (got %s)" % ",".join(_spoke))

	# Party debate
	_spoke.clear()
	_events.clear()
	await bus.handle_user_message("party debate SPARC residual")
	_assert(_events.size() == 1 and "SPARC residual" in _events[0], "debate party_event topic")
	var expected := PackedStringArray([
		"manager", "researcher", "analyst", "tester", "engineer", "writer", "manager"
	])
	_assert(_spoke == expected, "debate speakers (got %s)" % ",".join(_spoke))

	# Default route: manager then engineer for apk/godot wording
	_spoke.clear()
	await bus.handle_user_message("refactor the godot apk build")
	_assert(_spoke.size() >= 2, "route at least manager+specialist")
	_assert(_spoke[0] == "manager", "route first speaker manager")
	_assert(_spoke[1] == "engineer", "route specialist engineer for apk/godot")

	# Route researcher
	_spoke.clear()
	await bus.handle_user_message("research the SPARC hypothesis")
	_assert(_spoke.size() >= 2, "research route length")
	_assert(_spoke[0] == "manager" and _spoke[1] == "researcher", "route researcher")

	if _failures.is_empty():
		print("SMOKE_PARTY PASS")
		_finish(0)
	else:
		for f in _failures:
			printerr("FAIL: ", f)
		print("SMOKE_PARTY FAIL count=", _failures.size())
		_finish(1)

func _assert(cond: bool, label: String) -> void:
	if not cond:
		_failures.append(label)

func _fail(label: String) -> void:
	_failures.append(label)

func _finish(code: int) -> void:
	quit(code)
