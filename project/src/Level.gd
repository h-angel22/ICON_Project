extends Resource
class_name Level

class rValues:
	var left: int
	var right: int
	var top: int
	var bottom: int
	
	func _init(description: String):
		var r_str = description.split(" ", false)
		left = int(r_str[1])
		right = int(r_str[2])
		top = int(r_str[3])
		bottom = int(r_str[4])

export(int) var lvl_num

export(int) var start_room setget ,get_first_room
export(int) var boss_room setget ,get_boss_room

export(Array, PackedScene) var rooms


var rooms_values = []


func initialize(description: String):
	var rooms_str = description.split("\n", false)
	print(rooms_str)

	for rs in rooms_str:
		#TODO sitema sto scempio del doppio split
		var r_str = rs.split(" ", false)
		rooms.append(load(r_str[0])) 
		rooms_values.append(rValues.new(rs))
	
	start_room = 0
	boss_room = -1

func get_rooms():
	return rooms

func get_first_room() -> int:
	return start_room

func get_boss_room() -> int:
	return boss_room
