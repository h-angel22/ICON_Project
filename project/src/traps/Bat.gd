extends "res://src/Shot.gd"

export(PackedScene) var POOF
var effect

func _on_Bat_area_entered(area):
	._on_hit(area)
	if not area.is_in_group("Portal"):
		speed = 0
		_spawn_death_effect()

func _on_Bat_body_entered(body):
	_on_Bat_area_entered(body)

func _spawn_death_effect():
	if effect.get_parent() != self:
		add_child(effect)
		effect.scale = Vector2(0.4, 0.4)
		effect.play()

func _end_effect():
	effect.queue_free()
	self.queue_free()

func _ready():
	effect = POOF.instance()
	effect.connect("animation_finished", self, "_end_effect")
