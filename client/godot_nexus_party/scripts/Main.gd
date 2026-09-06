extends Control
## Nexus Party main chat — multi-agent interactive dialogue.

@onready var chat_log: RichTextLabel = $VBox/ChatLog
@onready var user_input: LineEdit = $VBox/InputRow/UserInput
@onready var send_button: Button = $VBox/InputRow/SendButton
@onready var party_bar: HBoxContainer = $VBox/PartyBar
@onready var status_label: Label = $VBox/Status

var bus: Node

func _ready() -> void:
	bus = preload("res://scripts/AgentBus.gd").new()
	add_child(bus)
	bus.name = "AgentBus"
	bus.setup_default_party()
	party_bar.setup(bus.get_agents())
	send_button.pressed.connect(_on_send)
	user_input.text_submitted.connect(func(_t): _on_send())
	_system("Welcome to ADL Nexus Party. Agents can hear you and each other.")
	_system("Tip: @engineer / @researcher / @manager or say 'party debate <topic>'")
	bus.agent_spoke.connect(_on_agent_spoke)
	bus.party_event.connect(_on_party_event)

func _on_send() -> void:
	var text := user_input.text.strip_edges()
	if text.is_empty():
		return
	user_input.text = ""
	_append("You", text, Color(0.7, 0.85, 1.0))
	bus.handle_user_message(text)

func _on_agent_spoke(agent_id: String, line: String) -> void:
	var a = bus.get_agent(agent_id)
	var col: Color = a.color if a else Color.WHITE
	_append(a.display_name if a else agent_id, line, col)
	party_bar.pulse(agent_id)

func _on_party_event(msg: String) -> void:
	_system(msg)

func _append(who: String, text: String, color: Color) -> void:
	var hex := color.to_html(false)
	chat_log.append_text("[color=#%s][b]%s[/b][/color]\n%s\n\n" % [hex, who, text])

func _system(text: String) -> void:
	chat_log.append_text("[color=#888888][i]%s[/i][/color]\n\n" % text)
