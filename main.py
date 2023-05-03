import pulp as pl

class Subproblem_node():
    sub: pl.LpProblem
    leftChild = None
    rightChild = None
    solution = False


def branch_and_bound(subproblem):
    # Define the queue of subproblems to be explored
    node: Subproblem_node = Subproblem_node()
    # Select the next subproblem from the queue
    
    # Solve the subproblem using PuLP solver
    subproblem.solve(pl.PULP_CBC_CMD(msg=0))
    node.sub = subproblem.copy()

    if subproblem.status == pl.LpStatusOptimal:
        # If the subproblem is feasible and optimal, print the solution and objective value
        vals = []
        for v in subproblem.variables():
            if pl.value(v) % 1 != 0:
                vals.append(v)
        
        if len(vals) == 0:
            print("Solution found")
            node.solution = True
            return node
        
        vals.sort()
        v = vals[0]
        sub1 = subproblem.copy()
        sub2 = subproblem.copy()
        sub1 += v <= pl.value(v) // 1
        sub2 += v >= pl.value(v) // 1 + 1

        resl = branch_and_bound(sub1)
        resr = branch_and_bound(sub2)

        node.leftChild = resl
        node.rightChild = resr
        return node
        
        
    elif subproblem.status == pl.LpStatusInfeasible:
        # If the subproblem is infeasible, print a message and move on to the next subproblem
        print("Subproblem is infeasible")
    else:
        # If the subproblem is unbounded or undefined, create two new subproblems by branching on a variable
        var = None
        for v in subproblem.variables():
            if v.varValue is None:
                var = v
                break
    
    return node
            
        

# Define the problem
problem = pl.LpProblem("Linear_Programming_Problem", pl.LpMinimize)

# Define the decision variables
x1 = pl.LpVariable("x1", lowBound=0)
x2 = pl.LpVariable("x2", lowBound=0)

# Define the objective function
problem += 6*x1 + 8*x2

# Define the constraints
problem += 6*x1 + 7*x2 >= 40
problem += x2 >= 2

# Solve the problem using Branch and Bound algorithm
sol = branch_and_bound(problem)

def printTree(t):
    if t is None:
        print("a")
        return
    
    for v in t.sub.variables():
        print(v.name, "=", v.varValue, "; ", end="")
    printTree(t.leftChild)
    printTree(t.rightChild)

printTree(sol)