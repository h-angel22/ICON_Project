from LevelConverter import *
from room import *
from cspProblem import Variable, CSP, Constraint
from cspSLS import *
from costraints import *

dim = 8
num_archs = 10


#variabili
vars = []

arch_domain = []
arch_domain.append((None, None, None, None))
couples = []

for i in range(0,dim):
    for j in range(0,dim):
        if i != j and ((i != 2 and j != 0) or (i != 0 and j != 2)):
            temp = (i,j)
            couples.append(temp)

for c in couples:
    arch_domain.append((c[0], c[1], None, None))
    arch_domain.append((None, None, c[0], c[1]))

n = num_archs #9#int((dim*(dim-1))/2)
for i in range(0,n):
    vars.append(Variable("A"+str(i), arch_domain))

solution = None


while solution == None:

    constraints = []

    rooms_to_use = load_file("/run/media/carlo/1ADE0211322EE208/Progetti/Godot/ICON_Project/project/ICON_src/rooms.txt", dim)

    constraints.append( Constraint(vars, not_equals, "non possono esserci 2 archi uguali") )
    constraints.append( Constraint(vars, to_boss, "può esserci solo un entrata alla stanza del boss") )
    #constraints.append( Constraint(vars, to_compass, "può esserci solo un entrata alla stanza del tesoro") )
    constraints.append( Constraint(vars, not_mirrors, "non possono esserci archi con valori specchiati") ) # tutti gli archi
    constraints.append( Constraint(vars, not_samecolumn, "non si può ripetere un unumero in una stessa posizione dell'arco")) #tutti gli archi
    constraints.append( Constraint(vars, not_opposite, "non possono esserci archi orizzontali e verticali con gli stessi valori") ) # tutti gli archi
    constraints.append( Constraint(vars, can_connect(rooms_to_use), "non ci può essere il collegamento se una stanza ha un ostacolo") )
    
    constraints.append( Constraint(vars, all_used(rooms_to_use), "verifica che usi tutte le stanze") )
    constraints.append( Constraint(vars, is_valid(rooms_to_use), "deve risultare un grafo collegato") )
    #constraints.append( Constraint(vars, not_overlay(rooms_to_use), "le stanze non si possono sovrapporre") )

    csp = CSP("stanze", vars, constraints)
    #dfs_solve1(csp,vars)
    solution = any_conflict_solver(csp)
    if solution == None:
        print('Fallito tentativo', file=sys.stderr)  

#print(develop_level(rooms_to_use))


archs_to_rooms(rooms_to_use, solution)



save_file("out_rooms.txt", rooms_to_use)

#print(solution)


#print("CheckpointRoom.tscn -1 -1 -1 4\nCompassRoom.tscn 4 7 3 -1\nNewBossRoom.tscn -2 -2 5 -1\nNewRoom3.tscn -2 5 6 1\nNewRoom2.tscn 7 1 0 6\nNewRoom10.tscn 3 -1 -2 2\nNewRoom7.tscn -1 -1 4 3\nNewRoom8.tscn 1 4 -1 -1")