import random
import sys
from room import Room

def load_file(path, dim):
    file = open(path, 'r')
    arr = []
    for line in file:
        arr.append(Room(line))
    file.close()

    random.shuffle(arr)

    #TODO da generalizzare
    rooms_to_use = arr[:dim]
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