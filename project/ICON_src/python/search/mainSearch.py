import sys
from searchProblem import Search_problem_from_explicit_graph, Arc
from searchGeneric import AStarSearcher


if __name__ == "__main__":
    archs_str = sys.argv[1]
    start_room = int(sys.argv[2])
    rooms = {0, 1, 2, 3, 4, 5, 6, 7}

    archs_str_arr = archs_str.split(" - ")
    

    archs = []
    for i in archs_str_arr:
        if i != "":
            inner_arr = i.split(" ")
            archs.append(Arc(int(inner_arr[0]), int(inner_arr[1]), int(inner_arr[2])))

    problem = Search_problem_from_explicit_graph(rooms, archs, start = start_room, goals = {2})

    msearcher = AStarSearcher(problem)
    print(msearcher.search())

