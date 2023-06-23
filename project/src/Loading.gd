extends Control


var loop_one = false

var loading_finished = false

func _on_AnimatedSprite_animation_finished():
	if loop_one and loading_finished:
		hide()
	loop_one = true

func _on_loaded():
	loading_finished = true

