extends Resource
class_name Level

export(int) var lvl_num

export(int) var start_room setget ,get_first_room
export(int) var boss_room setget ,get_boss_room

export(Array, PackedScene) var rooms

const original_path = "res://scenes/Rooms/newRooms/"
const rooms_path = "user://"

var officialRooms = []
class tempRoom:
	var id: int
	var left: int
	var right: int
	var top: int
	var bottom: int
	var done: bool
	var position
	
	func _init(id, l, r, t, b):
		self.id = id
		left = int(l)
		right = int(r)
		top = int(t)
		bottom = int(b)
		done = false
		position = null


func initialize(description: String):
	var rooms_str = description.split("\n", false)

	var i = 0
	for rs in rooms_str:
		var r_str = rs.split(" ", false)
		officialRooms.append(tempRoom.new(i, r_str[1], r_str[2], r_str[3], r_str[4]))
		i+=1

	officialRooms[0].position = Vector2(0,0)
	_developLevel()

	_save_rooms(rooms_str)

	for r in officialRooms:
		print("id: ", r.id, ", pos: ", r.position)

	start_room = 0
	boss_room = 8 #TODO da sistemare perché funziona solo se generiamo 11 stanze


func _developLevel():
	var finito = false
	
	while not finito:
		finito = true
		for r in officialRooms:
			if r.position != null and not r.done:
				_developRoom(r)
			if r.position == null:
				finito = false

func _developRoom(r: tempRoom):
	var c = r.position
	r.done = true
	_addRoom(officialRooms[r.id].left, c.x-1, c.y)
	_addRoom(officialRooms[r.id].right, c.x+1, c.y)
	_addRoom(officialRooms[r.id].top, c.x, c.y-1)
	_addRoom(officialRooms[r.id].bottom, c.x, c.y+1)

func _addRoom(r, x, y):
	if (r < 0):
		return
	if (officialRooms[r].position == null):
		officialRooms[r].position = Vector2(x,y)

func _save_rooms(rooms_str):
	var r_str
	var r_load

	var r_inst
	var i = 0
	for rs in rooms_str:
		r_str = rs.split(" ", false)
		r_load = load(original_path + r_str[0])
		r_inst = r_load.instance()
		r_inst.set_directions(r_str[1], r_str[2], r_str[3], r_str[4])
		r_inst.set_id(i)
		r_inst.set_map_position(officialRooms[i].position)
		var save = PackedScene.new()
		save.pack(r_inst)
		ResourceSaver.save(rooms_path + r_str[0], save)
		i+= 1
		rooms.append(load(rooms_path + r_str[0]))
	

func get_rooms():
	return rooms

func get_first_room() -> int:
	return start_room

func get_boss_room() -> int:
	return boss_room
