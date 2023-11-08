import random
from room import Room

def load_file(path, dim):
    file = open(path, 'r')
    arr = []
    for line in file:
        arr.append(Room(line))
    file.close()

    rooms_to_use = [ arr[0], arr[1], arr[2] ]
    arr = arr[3:]
    random.shuffle(arr)
    
    rooms_to_use = rooms_to_use + arr[:dim-3]
    for i in range(0,dim):
        rooms_to_use[i].id = i

    return rooms_to_use

def print_rooms(rooms):
    for i in rooms:
        print(i)