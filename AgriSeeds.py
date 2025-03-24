from gurobipy import Model, GRB
import gurobipy as gp

def solve_instance(l, m, n, prod_cost, capacity, bushels_per_bag, demand, trans_cost):
    try:
        model = Model("AgriSeeds Optimization")
        
        #introducing the decision variables
        x = model.addVars(l, m, n, name="x", lb=0, vtype=GRB.CONTINUOUS)
        
        #objective function: minimize total cost of production and transportation combines
        model.setObjective(
            gp.quicksum(
                (prod_cost[f][h] + trans_cost[f][h][r]) * x[f, h, r]
                for f in range(l) for h in range(m) for r in range(n)
            ),
            GRB.MINIMIZE
        )
        
        #demand constraint
        for h in range(m):
            for r in range(n):
                model.addConstr(
                    sum(x[f, h, r] for f in range(l)) == demand[h][r],
                    name=f"demand_satisfaction_{h}_{r}"
                )
        
        #production constraint
        for f in range(l):
            model.addConstr(
                sum(bushels_per_bag[h] * x[f, h, r] for h in range(m) for r in range(n)) <= capacity[f],
                name=f"capacity_limit_{f}"
            )
        
        model.optimize()
        
        if model.status == gp.GRB.OPTIMAL:
            solution = {(f, h, r): x[f, h, r].X for f in range(l) for h in range(m) for r in range(n) if x[f, h, r].X > 0}
            minimal_cost = model.objVal
            return solution, minimal_cost
        else:
            return None, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None


if __name__ == "__main__":
    #picked the example given in the pdf
    l = 2  # Number of facilities
    m = 2  # Number of crop types
    n = 2  # Number of regions
    prod_cost = {0: {0: 2.5, 1: 2.7}, 1: {0: 3.0, 1: 2.8}}
    capacity = {0: 500, 1: 600}
    bushels_per_bag = {0: 3, 1: 2}
    demand = {0: {0: 50, 1: 60}, 1: {0: 70, 1: 80}}
    trans_cost = {
        0: {0: {0: 0.5, 1: 0.6}, 1: {0: 0.7, 1: 0.8}},
        1: {0: {0: 0.6, 1: 0.5}, 1: {0: 0.8, 1: 0.7}}
    }

    solution, minimal_cost = solve_instance(l, m, n, prod_cost, capacity, bushels_per_bag, demand, trans_cost)

    if solution is not None:
        print("Optimal Solution:", solution)
        print("Minimal Cost:", minimal_cost)
    else:
        print("No feasible solution found.")

"""
Restricted license - for non-production use only - expires 2026-11-23
Gurobi Optimizer version 12.0.0 build v12.0.0rc1 (mac64[arm] - Darwin 23.0.0 23A344)

CPU model: Apple M2
Thread count: 8 physical cores, 8 logical processors, using up to 8 threads

Optimize a model with 6 rows, 8 columns and 16 nonzeros
Model fingerprint: 0x69da5ac4
Coefficient statistics:
  Matrix range     [1e+00, 3e+00]
  Objective range  [3e+00, 4e+00]
  Bounds range     [0e+00, 0e+00]
  RHS range        [5e+01, 6e+02]
Presolve removed 6 rows and 8 columns
Presolve time: 0.00s
Presolve: All rows and columns removed
Iteration    Objective       Primal Inf.    Dual Inf.      Time
       0    8.5400000e+02   0.000000e+00   0.000000e+00      0s

Solved in 0 iterations and 0.01 seconds (0.00 work units)
Optimal objective  8.540000000e+02
Optimal Solution: {(0, 0, 0): 50.0, (0, 0, 1): 60.0, (0, 1, 0): 70.0, (1, 1, 1): 80.0}
Minimal Cost: 854.0

"""