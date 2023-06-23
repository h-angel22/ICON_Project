extends Node

# Declare member variables here. Examples:
# var a = 2
# var b = "text"

const rooms_path = "res://scenes/Rooms/newRooms/"
const out_path = "res://ICON_src/rooms.txt"
const py_path = "D:/Progetti/Godot/ICON_Project/project/ICON_src/python/mainTest.py"

# Called when the node enters the scene tree for the first time.
func _ready():
	var all_files = list_files_in_directory(rooms_path)
	
	var room: PackedScene
	var i
	var data = ""
	for r in all_files:
		room = load(rooms_path + r)
		i = room.instance()
		data += rooms_path + r + " " + str(i.left_room) + " "+ str(i.right_room) + " " + str(i.top_room) + " " + str(i.bottom_room) + "\n"
	
	data[-1] = ""
	var file = File.new()
	file.open(out_path, File.WRITE)
	file.store_line(data)
	file.close()

	var output = []
	var exit_code = OS.execute("python3", [py_path], true, output)
	var l = Level.new()
	l.initialize(output[0])
	ResourceSaver.save("user://lvl.tres", l)

func list_files_in_directory(path):
	var files = []
	var dir = Directory.new()
	dir.open(path)
	dir.list_dir_begin()

	while true:
		var file = dir.get_next()
		if file == "":
			break
		elif not file.begins_with("."):
			files.append(file)

	dir.list_dir_end()

	return files



# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
