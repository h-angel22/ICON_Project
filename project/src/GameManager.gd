extends Node

const py_path = "./python/csp/mainDividiEtImpera.py"

export(PackedScene) var player_scene
export(PackedScene) var assistant_scene
var player
var assistant

var is_in_pause: bool = false
var in_respawn_phase: bool = false
var pause_screen: Node

onready var health_bar = get_node("HUD/HealthBar")
onready var mana_bar = get_node("HUD/ManaBar")

var levels: Array
var currentLevel
var boss_room

export var loadlvl = 0

var rooms: Array
var coordinates: Array
var current_room: int
var current_level: int

var saved_state: GameState = GameState.new()

signal loaded

func _init():
	pass
	#levels.append("res://levels/LvTutorial.tres")
	#levels.append("res://levels/Lv1SciFi.tres")
	#levels.append("res://levels/LvBonus1.tres")

func _generate_level():
	var level_str = [""]
	while level_str[0] == "":
		var exit_code = OS.execute("python", [py_path], true, level_str)
		if exit_code != 0:
			exit_code = OS.execute("python3", [py_path], true, level_str)
		print(level_str)
	var l = Level.new()
	l.initialize(level_str[0])
	ResourceSaver.save("user://lvl.tres", l)
	levels.append("user://lvl.tres")
	emit_signal("loaded")
	call_deferred("_load_level",loadlvl)

func _ready():
	var thread = Thread.new()
	thread.start(self, "_generate_level")
	#_generate_level()
	player = player_scene.instance()
	player.connect("is_dead", self, "_respawn")
	assistant = assistant_scene.instance()
	assistant.action_bar = $HUD/ActionBar
	health_bar.set_player(player)
	mana_bar.set_player(assistant)

	if get_node("/root/DefaultLoad").load_mode:
		load_savings()
	else:
		player.set_hp(player.max_hp)
		assistant.set_mana(assistant.max_mana)
	$Camera2D.set_process_input(false)

func _input(event):
	if Input.is_action_just_pressed("pause_toggle"):
		if not is_in_pause:
			is_in_pause = true
			var volume = get_node("/root/AudioManager").actual_volume
			get_node("/root/AudioManager").set_volume_music(volume - 10)
			get_tree().paused = true
			pause_screen = load("res://scenes/menu/PauseScreen.tscn").instance()
			$HUD.add_child(pause_screen)
		else:
			resume()
			var volume = get_node("/root/AudioManager").previous_volume
			get_node("/root/AudioManager").set_volume_music(volume)

func resume():
	is_in_pause = false
	get_tree().paused = false
	pause_screen.queue_free()

func _hide_main(parent):
	is_in_pause = not is_in_pause
	
	parent.add_child(load("res://scenes/menu/PauseScreen.tscn").instance())
	
	rooms[current_room].get_node("Objects").remove_child(player)
	rooms[current_room].get_node("Objects").remove_child(assistant)
	remove_child(rooms[current_room])
	
	health_bar.visible = false
	mana_bar.visible = false
	$HUD/ActionBar.visible = false
	
	$Camera2D.anchor_mode = 0

func _show_main():
	is_in_pause = not is_in_pause
	
	rooms[current_room].get_node("Objects").add_child(player)
	rooms[current_room].get_node("Objects").add_child(assistant)
	add_child(rooms[current_room])
	
	health_bar.visible = true
	mana_bar.visible = true
	$HUD/ActionBar.visible = true
	
	$Camera2D.anchor_mode = 1

func _load_level(l: int):
	currentLevel = load(levels[l])
	current_level = l

	var room_scenes = currentLevel.get_rooms()
	for rs in room_scenes:
		var temp: Room2D = rs.instance()
		rooms.append(temp)
		coordinates.append(temp.map_position)
	#for i in rooms.size():
	#	rooms[i].pos = MapPosition.new(l, i, Vector2(0,0))

	var start = currentLevel.get_first_room()
	boss_room = currentLevel.get_boss_room()
	if get_node("/root/DefaultLoad").load_mode:
		get_node("/root/DefaultLoad").load_mode = false
		_load_room(player.checkpoint_room, null)
	else:
		_load_room(start, null)

func _set_music(l: int):
	if l == 0:
		get_node("/root/AudioManager").change_music("res://assets/audio/Destroyed Sanctuary.mp3", -10.0, 1.0)
	elif l == 1:
		get_node("/root/AudioManager").change_music("res://assets/audio/echelon.mp3", -10.0, 1.0)
	elif l == 2:
		get_node("/root/AudioManager").change_music("res://assets/audio/Cleyton RX - Underwater.mp3", 0.0, 1.0)
	# da aggiungere altre colonne sonore

func _set_boss_music(l: int):
	if l == 0:
		get_node("/root/AudioManager").change_music("res://assets/audio/hold the line.ogg", -5.0, 1.0)
	elif l == 1:
		get_node("/root/AudioManager").change_music("res://assets/audio/Hojoj theme (OST wav version long).wav", -5.0, 1.0)
	# da aggiungere altre musiche per i boss

func _unload_level():
	get_node("/root/AudioManager").end_effects()
	_unload_room()
	rooms.clear()

func _switch_to_level(l: int, r: int, d):
	call_deferred("_unload_level")
	call_deferred("_load_level", l)
	call_deferred("_switch_to_room", r, d)

func _load_room(r: int, d):
	current_room = r
	add_child(rooms[r])
	if d == null:
		player.position = player.checkpoint_position
		assistant.position = Vector2(-200,20)
	elif d == -1:
		player.position = Vector2(0, 0)
		assistant.position = Vector2(-200,20)
	else:
		rooms[r].set_player_position(player, assistant, d)
	if r == boss_room:  
		$Camera2D.current = false
		_set_boss_music(current_level)
		rooms[r].get_node("Camera2D").current = true
	else:
		$Camera2D.current = true
		_set_music(current_level)
	
	rooms[r].load_events(saved_state.events)
	rooms[r].get_node("TimeToCheck").start()
	rooms[r].get_node("Objects").add_child(player)
	rooms[r].get_node("Objects").add_child(assistant)
	rooms[r].start_events()
	rooms[r].connect("exited_room", self, "_going_trough_door")
	get_node("/root/AudioManager").reactivate_effects(current_room)

func _unload_room():
	player.destroy_portals()
	assistant.destroy_summons()
	rooms[current_room].close_doors()
	if rooms[current_room].get_node("Objects").has_node(player.name):
		rooms[current_room].get_node("Objects").remove_child(player)
	rooms[current_room].get_node("Objects").remove_child(assistant)
	rooms[current_room].disconnect("exited_room", self, "_going_trough_door")
	remove_child(rooms[current_room])
	get_node("/root/AudioManager").deactivate_effects()
	_update_events()

func _switch_to_room(r: int, d):
	player.destroy_portals()
	assistant.destroy_summons()
	call_deferred("_unload_room")
	call_deferred("_load_room", r, d)

var destination_room
var door_used

func _going_trough_door(room, door):
	$HUD/ColorRect.show()
	$AnimationPlayer.play("fast_Fadeout")
	destination_room = room
	door_used = door

func _respawn(room):
	in_respawn_phase = true
	get_node("Room/Objects").remove_child(player)
	$HUD/ColorRect.show()
	$AnimationPlayer.play("Fadeout")
	destination_room = room
	load_savings()
	health_bar.set_player(player)
	player.set_hp(player.max_hp)
	assistant.set_mana(assistant.max_mana)

func _on_AnimationPlayer_animation_finished(anim_name):
	$AnimationPlayer.stop()
	match anim_name:
		"Fadeout":
			_unload_level()
			_load_level(loadlvl)
			_switch_to_room(destination_room, null)
			$AnimationPlayer.play("Fadein")
		"fast_Fadeout":
			_switch_to_room(destination_room, door_used)
			$AnimationPlayer.play("fast_Fadein")
		_:
			$HUD/ColorRect.hide()

func load_summon(sum, cost):
	assistant.add_summon(sum, cost)

func get_cost() -> int:
	return assistant.get_current_cost()

func _update_events():
	var room_events: Dictionary = rooms[current_room].get_events()
	for e in room_events:
		saved_state.events[e] = room_events[e]

func save():
	if in_respawn_phase:
		in_respawn_phase = false
		return
	_update_events()
	saved_state.set_hp(player.hp, player.max_hp)
	saved_state.set_mp(assistant.mana, assistant.max_mana)
	saved_state.set_actionbar(assistant.slot_number, assistant.summons)
	saved_state.check_point = MapPosition.new(currentLevel.lvl_num, player.checkpoint_room, player.checkpoint_position)
	get_node("/root/DefaultLoad").save_game_state(saved_state)

func load_savings():
	saved_state = get_node("/root/DefaultLoad").load_game_state()
	loadlvl = saved_state.check_point.level
	player.checkpoint_room = saved_state.check_point.room
	player.checkpoint_position = saved_state.check_point.position
	player.set_max_hp(saved_state.max_hp) 
	player.set_hp(saved_state.hp)
	assistant.set_max_mana(saved_state.max_mp)
	assistant.set_mana(saved_state.mp)
	assistant.slot_number = saved_state.slot_num
	assistant.set_summons(saved_state.get_action_bar()) 
	assistant.update_grafics()

func fadein():
	$AnimationPlayer.play("Fadein")

var stacked_menu

func ask_name():
	var stacked_menu = load("res://scenes/menu/NamePopUp.tscn").instance()
	$HUD.add_child(stacked_menu)
	get_node("/root/DefaultLoad").is_blocked = true

func save_name(name: String):
	saved_state.name = name
	var file = preload("res://dialogues/TutorialDialogues.tres")
	DialogueManager.game_states = [$Room, $Room/Events/PresentationEvent, player, assistant]
	DialogueManager.show_example_dialogue_balloon("Quest", file)

func set_assistant_anim(animation: String):
	assistant.get_node("Sprite").animation = animation

func get_rooms() -> Array:
	return rooms

func validate_coordinate(coor: Vector2) -> bool:
	return coordinates.has(coor)
