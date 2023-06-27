import random
import sys
from room import Room

def load_file(path, dim):
    file = open(path, 'r')
    arr = []
    for line in file:
        arr.append(Room(line))
    file.close()

    rooms_to_use = [ arr[0], arr[1], arr[2] ]
    random.shuffle(arr)

    #rooms_to_use = [Room("CheckpointRoom.tscn -1 -1 -1 -1"), Room("NewBossRoom.tscn -2 -2 -1 -1")]
    rooms_to_use = rooms_to_use + arr[:dim-3]
    for i in range(0,dim):
        rooms_to_use[i].id = i

    #print(rooms_to_use)

    return rooms_to_use

def save_file(path, rooms):
    #riginal_stdout = sys.stdout 

    #with open(path, 'w') as f:
        #sys.stdout = f # Change the standard output to the file we created.
        
    for i in rooms:
        print(i)

        #sys.stdout = original_stdout # Reset the standard output to its original value