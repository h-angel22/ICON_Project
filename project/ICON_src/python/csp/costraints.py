from collections import deque

def confront_quadruplet(quad):
    return tuple((float('inf') if x is None else x for x in quad))

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
        graph = {}

        for r in rooms:
            graph[r.id] = []

        for a in archs:
            if (a[0] != None):
                graph[a[0]] = graph[a[0]] + [a[1]]
                graph[a[1]] = graph[a[1]] + [a[0]]
            elif (a[2] != None):
                graph[a[2]] = graph[a[2]] + [a[3]]
                graph[a[3]] = graph[a[3]] + [a[2]]

        return is_connected(graph)

    connected.__name__ = "rooms_connected"
    return connected

def can_connect(rooms):
    def check_bool_rooms(*archs):
        valid = True
        for a in archs:
            if (a[0] != None):
                valid = rooms[a[0]].can_right
            elif (a[1] != None):
                valid = rooms[a[1]].can_left
            elif (a[2] != None):
                valid = rooms[a[2]].can_bottom
            elif (a[3] != None):
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
            if (i == 1):
                cont+=1
        if cont > 1:
            break
    return cont == 1

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