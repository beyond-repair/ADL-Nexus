extends HBoxContainer
## Pixel-party strip: one portrait slot per agent.

var _slots: Dictionary = {}

func setup(agents: Array) -> void:
	for c in get_children():
		c.queue_free()
	_slots.clear()
	for a in agents:
		var panel := PanelContainer.new()
		panel.custom_minimum_size = Vector2(120, 88)
		var vb := VBoxContainer.new()
		var portrait := ColorRect.new()
		portrait.custom_minimum_size = Vector2(112, 48)
		portrait.color = a.color.darkened(0.35)
		var name_l := Label.new()
		name_l.text = a.display_name
		name_l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		name_l.add_theme_font_size_override("font_size", 11)
		var role_l := Label.new()
		role_l.text = a.role
		role_l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		role_l.add_theme_font_size_override("font_size", 9)
		vb.add_child(portrait)
		vb.add_child(name_l)
		vb.add_child(role_l)
		panel.add_child(vb)
		add_child(panel)
		_slots[a.id] = portrait

func pulse(agent_id: String) -> void:
	if not _slots.has(agent_id):
		return
	var r: ColorRect = _slots[agent_id]
	var base := r.color
	r.color = Color(1, 1, 0.6, 1)
	await get_tree().create_timer(0.15).timeout
	r.color = base
