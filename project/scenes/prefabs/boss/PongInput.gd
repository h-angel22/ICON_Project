extends "res://src/boss/Pong.gd"

var original_speed: int
export var dash_speed: int
export var rotation_speed: float

func _ready():
	._ready()
	original_speed = speed
	$Sensors.set_target(player)

func _process(delta):
	if Input.is_action_just_pressed("debug1"):
		_shoot_left()
	if Input.is_action_just_pressed("debug2"):
		_shoot_right()
	if Input.is_action_just_pressed("debug3"):
		_start_jump()
	if Input.is_action_just_pressed("debug4"):
		_dash_left()
	if Input.is_action_just_pressed("debug5"):
		_dash_right()

func _physics_process(delta):
	._physics_process(delta)
	match jumping_state:
		dashing_left:
			$AnimatedSprite.rotate(-rotation_speed)
		dashing_right:
			$AnimatedSprite.rotate(rotation_speed)

func get_direction() -> Vector2:
	if jumping_state == dashing_left:
		return Vector2.LEFT
	elif jumping_state == dashing_right:
		return Vector2.RIGHT
	else:
		return .get_direction()

func _dash_left():
	jumping_state = dashing_left
	speed = dash_speed
	$Cooldown.wait_time = 0.5
	$Cooldown.start()

func _dash_right():
	jumping_state = dashing_right
	speed = dash_speed
	$Cooldown.wait_time = 0.5
	$Cooldown.start()

func _start_jump():
	$Cooldown.wait_time = 3
	$AnimatedSprite.animation = "jump_up"

func _shoot_left():
	jumping_state = shooting_left
	_spit()
	$Cooldown.wait_time = 1
	$Cooldown.start()

func _shoot_right():
	jumping_state = shooting_right
	_spit()
	$Cooldown.wait_time = 1
	$Cooldown.start()

func _on_AnimatedSprite_animation_finished():
	if $AnimatedSprite.animation == "jump_up":
		jumping_state = jumping

	elif $AnimatedSprite.animation == "jump_down":
		start_earthquake()
		contact_damage = original_contact_damage
		$HitBox/Body.disabled = false
		$CollisionShape2D.disabled = false
		get_parent().crack_floor(position)
		$AnimatedSprite.animation = "sit_up"
		jumping_state = normal

	elif $AnimatedSprite.animation == "sit_up":
		$AnimatedSprite.animation = "idle"
		$Sensors.read()

	elif $AnimatedSprite.animation == "spit":
		$AnimatedSprite.animation = "idle"

func _on_Cooldown_timeout():
	match jumping_state:
		normal: 
			$Sensors.read()
		out_of_screen:
			jumping_state = landing
		shooting_left:
			jumping_state = normal
			$Cooldown.wait_time = 0.5
			$Cooldown.start()
		shooting_right:
			jumping_state = normal
			$Cooldown.wait_time = 0.5
			$Cooldown.start()
		dashing_left:
			$AnimatedSprite.rotation = 0
			speed = original_speed
			jumping_state = normal
			$Cooldown.wait_time = 0.5
			$Cooldown.start()
		dashing_right:
			$AnimatedSprite.rotation = 0
			speed = original_speed
			jumping_state = normal
			$Cooldown.wait_time = 0.5
			$Cooldown.start()
