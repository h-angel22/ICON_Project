extends "res://src/boss/Pong.gd"

var original_speed: int
export var dash_speed: int = 30000
export var rotation_speed: float = 0.3

func _ready():
	._ready()
	original_speed = speed
	$Sensors.set_target(player)

const py_path = "./python/DecisionTree/learnDT.py"

func _do_action(actions: Dictionary):
	var action = actions[ actions.keys().max() ]
	match action:
		"shoot_left":
			_shoot_left()
		"shoot_right":
			_shoot_right()
		"jump":
			_start_jump()
		"dash_left":
			_dash_left()
		"dash_right":
			_dash_right()

func _input_ml():
	var action_str = []
	var read = $Sensors.read()
	var exit_code = OS.execute("python", [py_path] + read, true, action_str)
	if exit_code != 0:
		exit_code = OS.execute("python3", [py_path] + read, true, action_str)
	
	var actions_temp = action_str[0].split("\n", false)
	var actions = {}
	for a in actions_temp:
		var pair = a.split(" ", false)
		actions[float(pair[1])] = pair[0]
	print(actions)
	_do_action(actions)

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
		jumping_state = normal
		$Cooldown.wait_time = 0.5
		$Cooldown.start()

	elif $AnimatedSprite.animation == "spit":
		$AnimatedSprite.animation = "idle"

func _on_Cooldown_timeout():
	match jumping_state:
		normal: 
			_input_ml()
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
