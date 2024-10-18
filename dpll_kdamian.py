#!/usr/bin/env python3

'''dpll_kdamian.py - this program implements a 2SAT solver using the DPLL algorithm'''

import csv
import time

from typing import List, Dict

def unit_propagation(clauses: List[List[int]], assignments: List[bool]):
    '''unit propagation function'''
    units = [clause[0] for clause in clauses if len(clause) == 1]           # collect all the units (clauses with only one literal)

    if not units:                                                           # if no units are found, return
        return

    for unit in units:                                                      # for every unit
        var = abs(unit) - 1                                                 # get the index of the unit
        truth_val = unit > 0                                                # check if the value of the unit should be true or false (true if unit > 0)
        assignments[var] = truth_val                                        # assign the unit its truth value that makes the clause true
        clauses[:] = [clause for clause in clauses if unit not in clause]   # delete all the clauses that the unit appears in
        for i, clause in enumerate(clauses):                                # delete all the appearances of the -unit in each clause
            if -unit in clause:
                clauses[i] = [v for v in clause if v != -(unit)]

def pure_literal_elimination(clauses: List[List[int]], assignments: List[bool]):
    '''pure literal elimination function'''
    variables = []                                                          # initialize list to hold all the variables (both positive and negative occurences)
    pure_literals = set()                                                   # initialize set to hold all pure literals
    
    for clause in clauses:                                                  # add all the instances of each literal (both positive and negative) to the variables list
        for literal in clause:
            if literal not in variables:
                variables.append(literal)

    for literal in variables:                                               # for each literal, if the -literal does not appear in the variables list, add it to the pure_literals set
        if -literal not in variables:                                       
            pure_literals.add(literal)

    if not pure_literals:                                                   
        return

    for literal in pure_literals:
        if literal > 0:
            assignments[literal - 1] = True
        else:
            assignments[-literal - 1] = False
        clauses[:] = [clause for clause in clauses if literal not in clause]

def dpll_algorithm(clauses: List[List[int]], assignments: List[bool]) -> bool:
    '''dpll algorithm'''

    while any(len(clause) == 1 for clause in clauses):
        unit_propagation(clauses, assignments)
    pure_literal_elimination(clauses, assignments)
    if not clauses:
        return True
    if any(len(c) == 0 for c in clauses):
        return False
    lit_to_change = clauses[0][0]
    return dpll_algorithm(clauses + [[lit_to_change]], assignments) or dpll_algorithm(clauses + [[-lit_to_change]], assignments)

def main() -> None:
    '''main function'''
    file = "check-kdamian.csv"                                                   # initialize variables
    sat = 0
    unsat = 0
    x_sat = []
    y_sat = []
    x_unsat = []
    y_unsat = []

    with open(file, mode = 'r') as file:
        csv_file = csv.reader(file)
        for line in csv_file:
            if line[0] == 'c':
                clauses = []
                n = 0
                problem = int(line[1])
                print(f'Problem {problem}')
            elif line[0] == 'p':
                n_vars = int(line[2])
                n_clauses = int(line[3])
                assignments = [None] * n_vars
            else:
                clause = [int(v) for v in line[:-1] if v != '0']
                clauses.append(clause)
                n += 1
                if n == n_clauses:
                    start = time.time()
                    result = dpll_algorithm(clauses, assignments)
                    end = time.time()
                    if result is True:
                        print(f"satisfiable")
                        sat += 1
                        x_sat.append(n_clauses * 2)                         # append number of literals to the x_sat list
                        y_sat.append(end - start)                           # append execution time to the y_sat list
                    else:
                        print(f"unsatisfiable")
                        unsat += 1
                        x_unsat.append(n_clauses * 2)                       # append number of literals to the x_unsat list
                        y_unsat.append(end - start)                         # append execution time to the y_unsat list
                    
    print(f"TOTAL SATISFIABLE: {sat}")
    print(f"TOTAL UNSATISFIABLE: {unsat}")

    # with open('x_sat.txt', 'w') as f:                                     # print x and y axes to 
    #     f.writelines(f"{val}\n" for val in x_sat)
    # with open('y_sat.txt', 'w') as f:
    #     f.writelines(f"{val}\n" for val in y_sat)
    # with open('x_unsat.txt', 'w') as f:
    #     f.writelines(f"{val}\n" for val in x_unsat)
    # with open('y_unsat.txt', 'w') as f:
    #     f.writelines(f"{val}\n" for val in y_unsat)

if __name__ == '__main__':
    main()