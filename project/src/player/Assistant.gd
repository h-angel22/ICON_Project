extends Node2D

var summons: Array = [null, null, null, null, null, null]
export var summons_number = 1

var action_bar setget set_actionbar

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	if Input.is_action_just_pressed("summon"):
		print("summon ", get_viewport().get_mouse_position())
		summons[action_bar.current()].position = get_viewport().get_mouse_position()
		get_parent().add_child(summons[action_bar.current()])

func set_actionbar(bar):
	action_bar = bar

func add_summon(sum):
	summons[action_bar.current()] = sum
	var t = sum.icon
	action_bar.set_slot(t)

func add_slot():
	pass
