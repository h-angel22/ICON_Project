def to_bool(n) -> bool:
    return n != -2

class Room(object):
    def __init__(self, string) -> None:
        splits = str.split(string)
        self.nums = [int(splits[1]),int(splits[2]),int(splits[3]),int(splits[4])]
        
        self.name = splits[0]
        self.can_left = to_bool(self.nums[0])
        self.can_right = to_bool(self.nums[1])
        self.can_top = to_bool(self.nums[2])
        self.can_bottom = to_bool(self.nums[3])

        self.left = self.nums[0]
        self.right = self.nums[1]
        self.top = self.nums[2]
        self.bottom = self.nums[3]
        
        self.id = -1

    def reset_doors(self):
        self.left = self.nums[0]
        self.right = self.nums[1]
        self.top = self.nums[2]
        self.bottom = self.nums[3]
    
    #def set_coordinates(self, coor):
    #    self.x = coor[0]
    #    self.y = coor[1]
    
    def set_coordinates(self, x, y):
        print("ciao")
        self.x = x
        self.y = y

    # stampa quando richiamo il singolo elemento
    def __str__(self) -> str:
        return f"{self.name} {self.left} {self.right} {self.top} {self.bottom}"
    
    # stampa quando richiamo la lista degli elementi Room
    def __repr__(self) -> str:
        return f"\n<{self.name} - id {self.id}:\t{self.can_left}\t{self.can_right}\t{self.can_top}\t{self.can_bottom}>"

def archs_to_rooms(rooms: 'list[Room]', archs: dict):
    archs = archs.values()
#   archs_list = archs.values()
#   archs_to_rooms(rooms, archs_list)

#def archs_to_rooms(rooms: 'list[Room]', archs: list):
    for r in rooms:
        r.reset_doors()
    
    ar_hor = []
    ar_ver = []
    for a in archs:
        if (a[0] != None):
            ar_hor.append(a)
        elif (a[2] != None):
            ar_ver.append(a)

    for a in ar_hor:
        rooms[a[0]].right = a[1]
        rooms[a[1]].left = a[0]

    for a in ar_ver:
        rooms[a[2]].bottom = a[3]
        rooms[a[3]].top = a[2]

"""
class Arch(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.top = None
        self.bottom = None
"""
