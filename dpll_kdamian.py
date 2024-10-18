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

    if not pure_literals:                                                   # if no pure literals are found, return                                  
        return

    for literal in pure_literals:                                           # for each pure literal we found
        if literal > 0:                                                     # if the literal is positive, assign it True
            assignments[literal - 1] = True
        else:                                                               # if the literal is negative, assign it False
            assignments[-literal - 1] = False                               # remove all the clauses that the literal appears in
        clauses[:] = [clause for clause in clauses if literal not in clause]

def dpll_algorithm(clauses: List[List[int]], assignments: List[bool]) -> bool:
    '''dpll algorithm'''

    while any(len(clause) == 1 for clause in clauses):                      # while there is a unit in clauses
        unit_propagation(clauses, assignments)                              # call unit_propagate on clauses and assignments
    pure_literal_elimination(clauses, assignments)                          # then call pure_literal_elimination on clauses and assignments
    if not clauses:                                                         # if there are no clauses left in clauses, return True since we know that clauses is satisfiable
        return True
    if any(len(c) == 0 for c in clauses):                                   # if any clause is empty, we know that clauses is unsatisfiable with that truth assignment, so return False
        return False
    lit_to_change = clauses[0][0]                                           # determine the next literal to change (default is the first literal that appears in clauses)
                                                                            # call dpll_algorithm on clauses AND literal or clauses AND -literal to force unit propagation
    return dpll_algorithm(clauses + [[lit_to_change]], assignments) or dpll_algorithm(clauses + [[-lit_to_change]], assignments)

def main() -> None:
    '''main function'''
    file = "check-kdamian.csv"                                              # initialize file name
    sat = 0                                                                 # initialize satisfiable counts                                                                 
    unsat = 0
    # x_sat = []                                                            # initialize x axis and y axis lists for both satisfiable and unsatisfiable problems for the graph
    # y_sat = []
    # x_unsat = []
    # y_unsat = []

    with open(file, mode = 'r') as file:
        csv_file = csv.reader(file)
        for line in csv_file:
            if line[0] == 'c':                                              # if the line starts with a c, we know it's a new problem
                clauses = []                                                # initialize clauses list and clause counter (n)
                n = 0
                problem = int(line[1])                                      # get the problem number and print it to the screen
                print(f'Problem {problem}')
            elif line[0] == 'p':                                            # if the line starts with p
                n_vars = int(line[2])                                       # get the number of variables and clauses
                n_clauses = int(line[3])
                assignments = [None] * n_vars                               # initialize the assignments list to None for all variables
            else:                                                           # if the line doesn't start with p or c, we know it's a clause
                clause = [int(v) for v in line[:-1] if v != '0']            # remove the ending comma, then add all the variables to the clause, not including the ending zero      
                clauses.append(clause)                                      # append that clause to the clauses list
                n += 1                                                      # increment the clause counter
                if n == n_clauses:                                          # if we have reached the last clause in the problem
                    start = time.time()                                     # run dpll_algorithm and retrieve the start and end times
                    result = dpll_algorithm(clauses, assignments)           
                    end = time.time()
                    if result is True:                                      # if dpll_algorithm returned True, print that it was satisfiable as well as the final assignments of each variable
                        print(f"satisfiable: final assignments = {assignments}\n")
                        sat += 1
                        # x_sat.append(n_clauses * 2)                       # append number of literals to the x_sat list
                        # y_sat.append(end - start)                         # append execution time to the y_sat list
                    else:                                                   # if dpll_algorithm returned False, print that it was unsatisfiable as well as the final assignments of each variable
                        print(f"unsatisfiable: final assignments = {assignments}\n")
                        unsat += 1
                        # x_unsat.append(n_clauses * 2)                     # append number of literals to the x_unsat list
                        # y_unsat.append(end - start)                       # append execution time to the y_unsat list
                    
    print(f"TOTAL SATISFIABLE: {sat}")                                      # print total satisfiable and unsatisfiable counts
    print(f"TOTAL UNSATISFIABLE: {unsat}")

    # with open('output_xsat_kdamian.txt', 'w') as f:                                     # print x and y axes to .txt files to copy and paste into Excel to graph
    #     f.writelines(f"{val}\n" for val in x_sat)
    # with open('output_ysat_kdamian.txt', 'w') as f:
    #     f.writelines(f"{val}\n" for val in y_sat)
    # with open('output_xunsat_kdamian.txt', 'w') as f:
    #     f.writelines(f"{val}\n" for val in x_unsat)
    # with open('output_yunsat_kdamian.txt', 'w') as f:
    #     f.writelines(f"{val}\n" for val in y_unsat)

if __name__ == '__main__':
    main()