import os
from LevelConverter import *
from room import *
from cspProblem import Variable, CSP, Constraint
from cspSLS import *
from costraints import *

dim = 11

absolute_path = os.path.dirname(__file__)
relative_path = "../../rooms.txt"
full_path = os.path.join(absolute_path, relative_path)

rooms_to_use = load_file(full_path, dim)
used_rooms = []
completed_rooms = []

random.shuffle(rooms_to_use)

used_rooms.append( rooms_to_use.pop() )

while len(rooms_to_use) != 0:
    random.shuffle(used_rooms)
    r = used_rooms[0]
    
    dir = r.get_direction()
    
    match dir:
        case Direction.LEFT: 
            dir_to_find = Direction.RIGHT
        case Direction.RIGHT: 
            dir_to_find = Direction.LEFT
        case Direction.TOP: 
            dir_to_find = Direction.BOTTOM
        case Direction.BOTTOM: 
            dir_to_find = Direction.TOP
    
    for r_index in rooms_to_use:
        if r_index.can(dir_to_find):
            rooms_to_use.remove(r_index)
            attach_rooms(r, r_index, dir)

            if r.is_completed():
                used_rooms.remove(r)
                completed_rooms.append(r)

            if r_index.is_completed():
                completed_rooms.append()
            else:
                used_rooms.append(r_index)
            break


final_rooms = used_rooms + completed_rooms
final_rooms.sort(key=lambda x: x.id)

print_rooms(final_rooms)
