extends Node2D

var target: Character

func set_target(t):
	target = t

func _process(delta):
	$TargetPosition.position = target.position
	if Input.is_action_just_pressed("read_sensors"):
		read(true)

func _print_read(reading: Array):
	var str_read = ""
	for i in reading:
		if str(i) == "False":
			str_read += "0, "
		elif str(i) == "True":
			str_read += "1, "
		else:
			str_read += str(i) + ", "

	print(str_read)

func read(to_print=false):
	var pos = get_parent().position
	
	var reading = [0, 0, 0, 0, 0, 0, 0, 0]
	
	reading[0] = $RayCastLeft.get_collision_point().distance_to(pos)
	reading[1] = $RayCastRight.get_collision_point().distance_to(pos)
	reading[2] = $RayCastTop.get_collision_point().distance_to(pos)
	reading[3] = $RayCastBottom.get_collision_point().distance_to(pos)
	
	var dir = position.direction_to($TargetPosition.position)
	
	reading[4] = dir.x
	reading[5] = dir.y
	
	reading[6] = $TargetPosition.position.distance_to(pos)
	
	var at_risk = false
	var areas: Array = $Detector.get_overlapping_areas()
	for a in areas:
		if a.is_in_group("Projectile"):
			at_risk = true
			break

	reading[7] = 1 if at_risk else 0

	if to_print:
		_print_read(reading)

	return reading
