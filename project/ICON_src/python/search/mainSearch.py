from searchProblem import *
from searchGeneric import AStarSearcher


if __name__ == "__main__":
    arcs_str = "4 5 2\n5 2 1\n0 3 1\n6 4 2\n1 7 1\n7 2 1\n4 7 1\n3 6 2\n1 0 1\n" + "5 4 2\n2 5 2\n3 0 1\n4 6 2\n7 1 2\n2 7 1\n7 4 2\n6 3 1\n0 1 2\n"
    rooms_str = "0 1 2 3 4 5 6 7"

    rooms = {0, 1, 2, 3, 4, 5, 6, 7}

    archs_str_arr = arcs_str.split("\n")
    print(archs_str_arr)

    archs = []
    for i in archs_str_arr:
        if i != "":
            inner_arr = i.split(" ")
            archs.append(Arc(int(inner_arr[0]), int(inner_arr[1]), int(inner_arr[2])))

    problem = Search_problem_from_explicit_graph(rooms, archs, start=0, goals = {5})

    msearcher = AStarSearcher(problem)
    print(msearcher.search())

