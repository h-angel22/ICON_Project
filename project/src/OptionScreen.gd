extends CenterContainer

var selected_menu = 0
var pointer

func change_menu_color():
	_on_Resolution_mouse_exited()
	_on_Volume_mouse_exited()
	_on_Back_mouse_exited()
	
	match selected_menu:
		0:
			_on_Resolution_mouse_entered()
		1:
			_on_Volume_mouse_entered()
		2:
			_on_Back_mouse_entered()

func _ready():
	pointer = $Pointer
	remove_child(pointer)
	change_menu_color()

func _input(event):
	if Input.is_action_just_pressed("ui_down"):
		selected_menu = (selected_menu + 1) % 4;
		change_menu_color()
	elif Input.is_action_just_pressed("ui_up"):
		if selected_menu > 0:
			selected_menu = selected_menu - 1
		else:
			selected_menu = 2
		change_menu_color()
	elif Input.is_action_just_pressed("ui_accept"):
		match selected_menu:
			0:
				# Resolution
				_on_Resolution_pressed()
			1:
				# Volume
				_on_Volume_pressed()
			2:
				# Back
				_on_Back_pressed()


func _on_Resolution_pressed():
	get_tree().change_scene("res://scenes/menu/ResolutionPopup.tscn")


func _on_Resolution_mouse_entered():
	$Menu/Resolution.modulate = "ffffff"
	$Menu/Resolution.add_child(pointer)
	selected_menu = 0


func _on_Resolution_mouse_exited():
	$Menu/Resolution.modulate = "969696"
	if $Menu/Resolution.has_node(pointer.name):
		$Menu/Resolution.remove_child(pointer)

func _on_Volume_pressed():
	pass


func _on_Volume_mouse_entered():
	$Menu/Volume.modulate = "ffffff"
	$Menu/Volume.add_child(pointer)
	selected_menu = 1


func _on_Volume_mouse_exited():
	$Menu/Volume.modulate = "969696"
	if $Menu/Volume.has_node(pointer.name):
		$Menu/Volume.remove_child(pointer)


func _on_Back_pressed():
	get_tree().change_scene("res://scenes/menu/StartScreen.tscn")


func _on_Back_mouse_entered():
	$Menu/Back.modulate = "ffffff"
	$Menu/Back.add_child(pointer)
	selected_menu = 2


func _on_Back_mouse_exited():
	$Menu/Back.modulate = "969696"
	if $Menu/Back.has_node(pointer.name):
		$Menu/Back.remove_child(pointer)