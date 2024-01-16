import os
import sys
from LevelConverter import *
from room import *
from RoomProblemCSP import RoomProblem
from Block import *

level_dim = 7
sub_dim = 4


absolute_path = os.path.dirname(__file__)
relative_path = "../../rooms.txt"
full_path = os.path.join(absolute_path, relative_path)


blocks_solution = None
while blocks_solution == None:
    dim = level_dim
    final_rooms = []

    i = 0
    start = True
    end = False
    delta = 0
    blocks = []
    while dim > 0:
        if dim < sub_dim:
            sub_dim = dim
            end = True
        dim -= sub_dim
        
        if start:
            rooms_to_use = load_file_start(full_path, sub_dim)
            start = False
        elif end:
            rooms_to_use = load_file_end(full_path, sub_dim)
        else:
            rooms_to_use = load_file_mid(full_path, sub_dim)

        solver = RoomProblem(sub_dim, rooms_to_use)
        solution = solver.solve()
        if solution == None:
            print('Fallito tentativo', file=sys.stderr)
        else:
            archs_to_rooms(rooms_to_use, solution, delta)
            delta += sub_dim

            final_rooms = final_rooms + rooms_to_use
            b = Block(rooms_to_use, i)
            blocks.append(b)
            rooms_to_use.clear()
            i+=1
    
    solver = RoomProblem(len(blocks), blocks)
    blocks_solution = solver.solve()
    
    if blocks_solution == None:
        print('Fallito tentativo', file=sys.stderr)
        final_rooms.clear()
        blocks.clear()
    else:
        archs_to_blocks(blocks, blocks_solution)

print_rooms(final_rooms)

