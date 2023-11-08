extends Node

onready var parent_room: Room2D = get_parent().get_parent().get_parent()
onready var level: Array = parent_room.get_parent().get_rooms()
const py_path = "./python/search/mainSearch.py"

var current_room: int
var direction: int

var active = true

# Called when the node enters the scene tree for the first time.
func _ready():
	parent_room.connect("exited_room", self, "_room_changed")
	_update_path()

func _room_changed(next, door):
	parent_room.disconnect("exited_room", self, "_room_changed")
	parent_room = level[next]
	parent_room.connect("exited_room", self, "_room_changed")
	_update_path()

func _update_path():
	current_room = parent_room.id_room
	var path = _path_finder()
	var roomTo: int = -3
	var i : int = 0
	while(i < path.size() - 1):
		if int(path[i]) == current_room:
			roomTo = int(path[i+1])
			break
	parent_room.activatePathFinding(roomTo)

func _archs_str() -> String:
	var archs: String = ""
	for room in level:
		if room.top_room != -1 and room.top_room != -2:
			archs += str(room.id_room) + " " + str(room.top_room)
			if (level[room.top_room].closed):
				archs += " 2"
			else:
				archs += " 1"
			archs += " - "
		if room.bottom_room != -1 and room.bottom_room != -2:
			archs += str(room.id_room) + " " + str(room.bottom_room)
			if (level[room.bottom_room].closed):
				archs += " 2"
			else:
				archs += " 1"
			archs += " - "
		if room.left_room != -1 and room.left_room != -2:
			archs += str(room.id_room) + " " + str(room.left_room)
			if (level[room.left_room].closed):
				archs += " 2"
			else:
				archs += " 1"
			archs += " - "
		if room.right_room != -1 and room.right_room != -2:
			archs += str(room.id_room) + " " + str(room.right_room)
			if (level[room.right_room].closed):
				archs += " 2"
			else:
				archs += " 1"
			archs += " - "
	return archs

func _path_finder() -> Array:
	var path: Array
	var path_str = []
	OS.execute("python3", [py_path, _archs_str(), current_room], true, path_str)
	path = path_str[0].split(" --> ")
	print(path)
	return path

# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
