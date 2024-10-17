#!/usr/bin/env python3

'''dpll_kdamian.py - this program implements a 2SAT solver using the DPLL algorithm'''

import sys
import csv
import copy

from typing import List, Dict

def unit_propogation(clauses: List[List[int]], assignments: List[bool]) -> bool:
    '''unit propogation function'''
    units = [clause[0] for clause in clauses if len(clause) == 1]

    if not units:
        return False

    for unit in units:
        var = abs(unit) - 1
        truth_val = unit > 0
        assignments[var] = truth_val
        clauses[:] = [clause for clause in clauses if unit not in clause]
        for clause in range(len(clauses)):
            if -unit in clauses[clause]:
                clauses[clause].remove(-unit) 

    return True

def pure_literal_elimination(clauses: List[List[int]], assignments: List[bool]):
    '''pure literal elimination function'''
    variables = {}
    pure_literals = set()
    for clause in clauses:
        for literal in clause:
            if literal not in variables:
                variables[literal] = 0
            variables[literal] += 1

    for literal in variables:
        if -literal not in variables:
            if variables[literal] > 1:
                pure_literals.add(literal)

    if not pure_literals: 
        return False

    for literal in pure_literals:
        if literal > 0:
            assignments[literal - 1] = True
        else:
            assignments[-literal - 1] = False
        clauses[:] = [clause for clause in clauses if literal not in clause]

    return True

def dpll_algorithm(clauses: List[List[int]], assignments: List[bool]) -> bool:
    '''dpll algorithm'''

    found_unit = True
    while found_unit:
        found_unit = unit_propogation(clauses, assignments)
    print("clauses after unit prop while:")
    print(clauses)
    pure_literal_elimination(clauses, assignments)
    if not clauses:
        return True
    if any(len(c) == 0 for c in clauses):
        return False
    l = clauses[0][0]
    return dpll_algorithm(clauses + [[l]], assignments) or dpll_algorithm(clauses + [[-l]], assignments)

def main(arguments=sys.argv[1:], stream=sys.stdin) -> None:
    '''main function'''
    file = "2satless.csv"
    with open(file, mode = 'r') as file:
        csv_file = csv.reader(file)
        for line in csv_file:
            if line[0] == 'c':
                problem = int(line[1])
                clause = 0
                clauses = []
                print(f'Problem {problem}')
            elif line[0] == 'p':
                n_vars = int(line[2])
                n_clauses = int(line[3])
                assignments = [None] * n_vars
            else:
                clauses.append([])
                for literal in line[:-1]:
                    if int(literal) == 0:
                        clause += 1
                        continue
                    clauses[clause].append(int(literal))
                if clause > n_clauses - 1:
                    print("original clauses:")
                    print(clauses)
                    sat = dpll_algorithm(clauses, assignments)
                    if sat:
                        print("SATISFIABLE")
                    else:
                        print("UNSATISFIABLE")
                    continue
    
if __name__ == '__main__':
    main()