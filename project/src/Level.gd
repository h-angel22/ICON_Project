extends Resource
class_name Level

export(int) var lvl_num

export(int) var start_room setget ,get_first_room
export(int) var boss_room setget ,get_boss_room

export(Array, PackedScene) var rooms

const original_path = "res://scenes/Rooms/newRooms/"
const rooms_path = "user://rooms/"

var officialRooms = []
class tempRoom:
	var left: int
	var right: int
	var top: int
	var bottom: int
	var position: Vector2
	
	func _init(l, r, t, b):
		left = int(l)
		right = int(r)
		top = int(t)
		bottom = int(b)


func initialize(description: String):
	var rooms_str = description.split("\n", false)

	var r_str
	var r_load
	for rs in rooms_str:
		r_str = rs.split(" ", false)
		officialRooms.append(tempRoom.new(r_str[1], r_str[2], r_str[3], r_str[4]))

	officialRooms[0].position = Vector2(0,0)
	print(officialRooms)

	var r_inst
	var i = 0
	for rs in rooms_str:
		r_str = rs.split(" ", false)
		r_load = load(original_path + r_str[0])
		r_inst = r_load.instance()
		r_inst.set_directions(r_str[1], r_str[2], r_str[3], r_str[4])
		r_inst.id_room = i
		var save = PackedScene.new()
		save.pack(r_inst)
		ResourceSaver.save(rooms_path + r_str[0], save)
		i+= 1
		rooms.append(load(rooms_path + r_str[0]))
		#rooms.append(r_inst)

	start_room = 0
	boss_room = 2

func get_rooms():
	return rooms

func get_first_room() -> int:
	return start_room

func get_boss_room() -> int:
	return boss_room
