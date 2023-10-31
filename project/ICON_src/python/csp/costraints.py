from collections import deque

from room import archs_to_rooms

def confront_quadruplet(quad):
    return tuple((float('inf') if x is None else x for x in quad))

def generate_graph(nodes, archs):
    graph = {}

    for r in nodes:
        graph[r.id] = []

    for a in archs:
        if (a[0] != None):
            graph[a[0]] += [a[1]]
            graph[a[1]] += [a[0]]
        elif (a[2] != None):
            graph[a[2]] += [a[3]]
            graph[a[3]] += [a[2]]
            
    return graph

#"non possono esserci 2 archi uguali"
def not_equals(*archs) -> bool:
    list_archs = list(archs)
    list_archs = sorted(list_archs, key=confront_quadruplet) #.sort(key=confront_quadruplet)

    valid = True
    i = 0
    while (i < len(list_archs) -1 and valid):
        if list_archs[i] == list_archs[i+1] and list_archs[i] != (None, None, None, None):
            valid = False
        i+=1

    return valid

#non si può ripetere un unumero in una stessa posizione dell'arco
def not_samecolumn(*archs) -> bool:
    ar_hor = []
    ar_ver = []
    for a in archs:
        if (a[0] != None):
            ar_hor.append(a)
        elif (a[2] != None):
            ar_ver.append(a)
    
    #colonne 0 e 2
    ar_hor = sorted(ar_hor, key=lambda a: a[0])
    ar_ver = sorted(ar_ver, key=lambda a: a[2])

    valid = True
    i = 0
    while (i < len(ar_hor) -1 and valid):
        if (ar_hor[i][0] == ar_hor[i+1][0]):
            valid = False
        i = i+1

    i = 0
    while (i < len(ar_ver) -1 and valid):
        if (ar_ver[i][2] == ar_ver[i+1][2]):
            valid = False
        i = i+1

    #colonne 1 e 3
    if (valid):
        ar_hor = sorted(ar_hor, key=lambda a: a[1])
        ar_ver = sorted(ar_ver, key=lambda a: a[3])

        i = 0
        while (i < len(ar_hor) -1 and valid):
            if (ar_hor[i][1] == ar_hor[i+1][1]):
                valid = False
            i = i+1

        i = 0
        while (i < len(ar_ver) -1 and valid):
            if (ar_ver[i][3] == ar_ver[i+1][3]):
                valid = False
            i = i+1

    return valid

#non possono esserci archi con valori specchiati
def not_mirrors(*archs) -> bool:
    ar_hor = []
    ar_ver = []
    for a in archs:
        if (a[0] != None):
            if(a[0] > a[1]):
                ar_hor.append((a[1],a[0], None, None))
            else:
                ar_hor.append(a)
        elif (a[2] != None):
            if(a[2] > a[3]):
                ar_ver.append((None, None,a[3],a[2]))
            else:
                ar_ver.append(a)

    valid = not_equals(*ar_hor) and not_equals(*ar_ver)

    return valid

#non possono esserci archi orizzontali e verticali con gli stessi valori
def not_opposite(*archs) -> bool:
    list_archs = []
    for a in archs:
        if (a[0] != None):
            if(a[0] > a[1]):
                list_archs.append((a[1],a[0], None, None))
            else:
                list_archs.append(a)
        elif (a[2] != None):
            if(a[2] > a[3]):
                list_archs.append((a[3],a[2],None,None))
            else:
                list_archs.append((a[2],a[3],None,None))

    valid = not_equals(*list_archs)

    return valid

#verifica che usi tutte le stanze
def all_used(rooms):

    def used(*archs) -> bool:
        rooms_dictionary = {}

        for r in rooms:
            rooms_dictionary[r.id] = False

        for i in archs:
            for j in i:
                if j in rooms_dictionary:
                    rooms_dictionary[j] = True
        valid = True 
        if False in rooms_dictionary.values():
            valid = False

        return valid
    
    used.__name__ = "rooms_used"
    return used


def is_connected(graph):
    if not graph:
        # The graph is empty, so it is not connected
        return False

    visited = set()
    queue = deque()

    # Choose a starting node
    initial_node = next(iter(graph))

    queue.append(initial_node)
    visited.add(initial_node)

    while queue:
        node = queue.popleft()

        for neighbor in graph[node]:
            if neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)

    return len(visited) == len(graph)

#deve risultare un grafo collegato
def is_valid(rooms) -> bool:
    
    def connected(*archs):
        graph = generate_graph(rooms, archs)

        return is_connected(graph)

    connected.__name__ = "rooms_connected"
    return connected

def can_connect(rooms):
    def check_bool_rooms(*archs):
        valid = True
        for a in archs:
            if (a[0] != None and valid):
                valid = rooms[a[0]].can_right
            if (a[1] != None and valid):
                valid = rooms[a[1]].can_left
            if (a[2] != None and valid):
                valid = rooms[a[2]].can_bottom
            if (a[3] != None and valid):
                valid = rooms[a[3]].can_top
            if (not valid):
                break

        return valid
    
    check_bool_rooms.__name__ = "room_can_connect"
    return check_bool_rooms

def to_boss(*archs):
    cont = 0
    for a in archs:
        for i in a:
            if (i == 2):
                cont+=1
        if cont > 1:
            break
    return cont == 1

def to_compass(*archs):
    cont = 0
    for a in archs:
        for i in a:
            if (i == 1):
                cont+=1
        if cont > 1:
            break
    return cont == 1


#def not_overlay(rooms):
    
    #develop leve
    
#    develop_level.__name__ = "level_builder"
#    return develop_level
def develop_level(rooms): #(*archs):
    #func = is_valid(rooms)
    #all = func(*archs)
    #if not all:
    #    return False
    
    #archs_to_rooms(rooms, archs)

    officialRooms = []
    for r in rooms:
        officialRooms.append(None)
    #valid = True
    
    officialRooms[0] = (0, 0)
    #roomCounters[0]++; 
    #coorCounter[5][5]++; 
    addRoom(rooms[0].left, -1, 0, officialRooms)
    addRoom(rooms[0].right, 1, 0, officialRooms)
    addRoom(rooms[0].top, 0, -1, officialRooms) 
    addRoom(rooms[0].bottom, 0, 1, officialRooms) 
    
    stack = []
    for r in rooms[1:]:
        stack.append(r)
    
    developStack(stack, rooms, officialRooms)
    
    #if not (None in officialRooms):
        #print(officialRooms)
    #for i in range(0, len(rooms)):
        #if officialRooms[i] != None:
            #rooms[i].set_coordinates(officialRooms[i][0], officialRooms[i][1])
    
    #return valid

def addRoom(r, x, y, officialRooms):
    if (r < 0):
        return True
    if (officialRooms[r] == None):
        officialRooms[r] = (x,y)
        r.set_coordinates(x,y)
        return True
    #if (officialRooms[r][0] == x and officialRooms[r][1] == y):
    #    return True
    else:
        return False

def developStack(remains, rooms, officialRooms):
    #valid = True
    
    prev_len = len(remains) + 1
    while len(remains) != 0:
        if len(remains) == prev_len:
            return False

        i = 0
        while i < len(remains):
            prev_len = len(remains)
            r = remains[i]
            if (officialRooms[r.id] != None):
                developRoom(r, rooms, officialRooms)
                #print(valid)
                #if not valid:
                #    return False
                remains.remove(r)
            else:
                i = i + 1

    #todo = []
    
    #if len(ramains) == 0:
    #    return True

    #while len(ramains) != 0 and valid:
    #    r = ramains.pop()
    #    if (officialRooms[r.id] == None):
    #        todo.append(r)
    #    else:
    #        valid = developRoom(r, rooms, officialRooms)

    #if (valid):
    #    return developStack(todo, rooms, officialRooms)

    #print(valid)
    return True
    

def developRoom(r, rooms, officialRooms):
    #valid = True
    
    x = officialRooms[r.id][0]
    y = officialRooms[r.id][1]
    
    addRoom(rooms[r.id].left, x-1, y, officialRooms)
    addRoom(rooms[r.id].right, x+1, y, officialRooms)
    addRoom(rooms[r.id].top, x, y-1, officialRooms)
    addRoom(rooms[r.id].bottom, x, y+1, officialRooms)
    
    #return valid

#test
"""
graph = { "A" : ["B", "C"],
          "B" : ["D", "E", "A"],
          "C" : ["A"],
          "D" : ["B", "E"],
          "E" : ["B", "D"]
}

def edges(graph):
    edges = []
    for node in graph:
        for neighbour in graph[node]:
            edges.append((node, neighbour))

    return edges

print(edges(graph))
"""

"""
    archs = list(archs)

    archs[0] = (3,2,None,None)
    archs[1] = (1,4,None,None)
    archs[2] = (2,3,None,None)
    archs[3] = (None,None,1,5)
    archs[4] = (None,None,3,4)
    archs[5] = (None,None,4,3)
    archs[6] = (None,None,6,2)

    archs = list(archs)

        archs[5] = (None, None, 0, 1)
        archs[0] = (1,2,None,None)
        archs[1] = (3,4,None,None)
        archs[2] = (5,6,None,None)
        archs[3] = (None,None,2,3)
        archs[4] = (None,None,3,5)
"""