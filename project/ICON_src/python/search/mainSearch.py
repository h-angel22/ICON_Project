import sys
from searchProblem import Search_problem_from_explicit_graph, Arc
from searchGeneric import AStarSearcher


if __name__ == "__main__":
    #arcs_str = "4 5 2 - 5 2 1 - 0 3 1 - 6 4 2 - 1 7 1 - 7 2 1 - 4 7 1 - 3 6 2 - 1 0 1 - 5 4 2 - 2 5 2 - 3 0 1 - 4 6 2 - 7 1 2 - 2 7 1 - 7 4 2 - 6 3 1 - 0 1 2"

    #print(sys.argv)
    
    archs_str = sys.argv[1]
    start_room = int(sys.argv[2])
    rooms = {0, 1, 2, 3, 4, 5, 6, 7}

    archs_str_arr = archs_str.split(" - ")
    #print(archs_str_arr)

    archs = []
    for i in archs_str_arr:
        if i != "":
            inner_arr = i.split(" ")
            archs.append(Arc(int(inner_arr[0]), int(inner_arr[1]), int(inner_arr[2])))

    problem = Search_problem_from_explicit_graph(rooms, archs, start = start_room, goals = {2})

    msearcher = AStarSearcher(problem)
    print(msearcher.search())

