from cspProblem import Variable, CSP, Constraint
from cspSLS import *
from costraints import *

class RoomProblem():
    def __init__(self, sub_dim, rooms) -> None:
        self.dim = sub_dim
        self.num_archs = self.dim + 2
        self.rooms_to_use = rooms
        pass
    
    def solve(self):
        vars = []

        arch_domain = []
        arch_domain.append((None, None, None, None))
        couples = []
        
        id_list = []
        for i in self.rooms_to_use:
            id_list.append(i.id)

        for i in id_list:
            for j in id_list:
                if i != j:# and ((i != 2 and j != 0) or (i != 0 and j != 2)):
                    temp = (i,j)
                    couples.append(temp)

        for c in couples:
            arch_domain.append((c[0], c[1], None, None))
            arch_domain.append((None, None, c[0], c[1]))

        n = self.num_archs
        for i in range(0,n):
            vars.append(Variable("A"+str(i), arch_domain))

        solution = None

        constraints = []

        constraints.append( Constraint(vars, not_equals, "non possono esserci 2 archi uguali") )
        constraints.append( Constraint(vars, not_mirrors, "non possono esserci archi con valori specchiati") ) 
        constraints.append( Constraint(vars, not_samecolumn, "non si può ripetere un unumero in una stessa posizione dell'arco")) 
        constraints.append( Constraint(vars, not_opposite, "non possono esserci archi orizzontali e verticali con gli stessi valori") ) 
        constraints.append( Constraint(vars, can_connect(self.rooms_to_use), "non ci può essere il collegamento se una stanza ha un ostacolo") )
        
        constraints.append( Constraint(vars, all_used(self.rooms_to_use), "verifica che usi tutte le stanze") )
        constraints.append( Constraint(vars, is_valid(self.rooms_to_use), "deve risultare un grafo collegato") )

        csp = CSP("stanze", vars, constraints)
        solution = any_conflict_solver(csp)
        
        return solution