from room import Room, Direction

class Block(Room):
    def __init__(self, rooms, id):
        string = f"Block{id} "
        self.rooms = {}
        for r in rooms:
            self.rooms[r.id] = r
        
        found = -1
        i = 0
        while found == -1 and i < len(rooms):
            if rooms[i].left == -1:
                found = i
            i += 1
        self.room_left = found
        
        found = -1
        i = 0
        while found == -1  and i < len(rooms):
            if rooms[i].right == -1:
                found = i
            i += 1
        self.room_right = found
        
        found = -1
        i = 0
        while found == -1  and i < len(rooms):
            if rooms[i].top == -1:
                found = i
            i += 1
        self.room_top = found
        
        found = -1
        i = 0
        while found == -1  and i < len(rooms):
            if rooms[i].bottom == -1:
                found = i
            i += 1
        self.room_bottom = found
        
        
        if self.room_left != -1:
            string += "-1 "
            self.room_left = rooms[self.room_left].id
        else:
            string += "-2 "
        if self.room_right != -1:
            string += "-1 "
            self.room_right = rooms[self.room_right].id
        else:
            string += "-2 "
        if self.room_top != -1:
            string += "-1 "
            self.room_top = rooms[self.room_top].id
        else:
            string += "-2 "
        if self.room_bottom != -1:
            string += "-1 "
            self.room_bottom = rooms[self.room_bottom].id
        else:
            string += "-2 "

        Room.__init__(self, string)
        self.id = id


def archs_to_blocks(blocks: 'list[Block]', archs: dict):
    archs = archs.values()

    ar_hor = []
    ar_ver = []
    for a in archs:
        if (a[0] != None):
            ar_hor.append(a)
        elif (a[2] != None):
            ar_ver.append(a)
    
    for a in ar_hor:
        left_block = blocks[a[0]]
        right_block = blocks[a[1]]
        right_r =  left_block.rooms[ left_block.room_right ]
        left_r = right_block.rooms[ right_block.room_left ]
        right_r.right = left_r.id
        left_r.left = right_r.id
    
    for a in ar_ver:
        top_block = blocks[a[2]]
        bottom_block = blocks[a[3]]
        bottom_r =  top_block.rooms[ top_block.room_bottom ]
        top_r = bottom_block.rooms[ bottom_block.room_top ]
        bottom_r.bottom = top_r.id
        top_r.top = bottom_r.id