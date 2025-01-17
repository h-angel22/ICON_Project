import os
from LevelConverter import *
from room import *
from cspProblem import Variable, CSP, Constraint
from cspSLS import *
from costraints import *

dim = 11
num_archs = 12


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

n = num_archs
for i in range(0,n):
    vars.append(Variable("A"+str(i), arch_domain))

solution = None


while solution == None:

    constraints = []

    absolute_path = os.path.dirname(__file__)
    relative_path = "../../rooms.txt"
    full_path = os.path.join(absolute_path, relative_path)

    rooms_to_use = load_file(full_path, dim)

    constraints.append( Constraint(vars, not_equals, "non possono esserci 2 archi uguali") )
    constraints.append( Constraint(vars, to_boss, "può esserci solo un entrata alla stanza del boss") )
    constraints.append( Constraint(vars, not_mirrors, "non possono esserci archi con valori specchiati") ) # tutti gli archi
    constraints.append( Constraint(vars, not_samecolumn, "non si può ripetere un unumero in una stessa posizione dell'arco")) #tutti gli archi
    constraints.append( Constraint(vars, not_opposite, "non possono esserci archi orizzontali e verticali con gli stessi valori") ) # tutti gli archi
    constraints.append( Constraint(vars, can_connect(rooms_to_use), "non ci può essere il collegamento se una stanza ha un ostacolo") )
    
    constraints.append( Constraint(vars, all_used(rooms_to_use), "verifica che usi tutte le stanze") )
    constraints.append( Constraint(vars, is_valid(rooms_to_use), "deve risultare un grafo collegato") )

    csp = CSP("stanze", vars, constraints)
    solution = any_conflict_solver(csp)
    if solution == None:
        print('Fallito tentativo', file=sys.stderr)  



archs_to_rooms(rooms_to_use, solution)

print_rooms(rooms_to_use)
