extends Resource
class_name Level

export(int) var lvl_num

export(int) var start_room setget ,get_first_room
export(int) var boss_room setget ,get_boss_room

export(Array, PackedScene) var rooms


func initialize(description: String):
	var rooms_str = description.split("\n", false)
	print(rooms_str)

	var r_str
	var r_load
	var r_inst
	for rs in rooms_str:
		r_str = rs.split(" ", false)
		r_load = load(r_str[0])
		r_inst = r_load.instance()
		r_inst.set_directions(r_str[1], r_str[2], r_str[3], r_str[4])
		
		var save = PackedScene.new()
		save.pack(r_inst)
		ResourceSaver.save(r_str[0], save)
		
		rooms.append(r_load)

	start_room = 0
	boss_room = 1

func get_rooms():
	return rooms

func get_first_room() -> int:
	return start_room

func get_boss_room() -> int:
	return boss_room
