#!/usr/bin/env python3

'''dpll_kdamian.py'''

import sys
import csv

from typing import List, Dict

def unit_propogation(clauses: List[List[int]], assignments: List[bool], queue: List[List[List[int]]]) -> bool:
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

    queue.append([clause[:] for clause in clauses])
    print("ran unit prop")
    print(clauses)
    print(assignments)
    return True
     
def backtrack(clauses: List[Dict[int, bool]], assignments: List[bool], queue: List[List[List[int]]]) -> None:
    '''backtracking function'''

def pure_literal_elimination(clauses: List[Dict[int, bool]], assignments: List[bool], queue: List[List[List[int]]]) -> None:
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

    for literal in pure_literals:
        if literal > 0:
            assignments[literal - 1] = True
        else:
            assignments[-literal - 1] = False
        clauses[:] = [clause for clause in clauses if literal not in clause]
        
    print(variables)
    print(pure_literals)
    print(assignments)
    print(clauses)

def dpll_algorithm(clauses: List[Dict[int, bool]], assignments: List[bool], queue: List[List[List[int]]]) -> None:
    '''dpll algorithm'''
    run = True
    while run:
        run = unit_propogation(clauses, assignments, queue)
        if not clauses:
            print(f"satisfiable: variable assignments = {assignments}")
            print(f"queue after = {assignments}")
            print()
            return
        continue
    print(f"unsatisfied after unit prop: variable assignments = {assignments}")
    print(f"queue after = {assignments}")
    run = True
    while run:
        run = pure_literal_elimination(clauses, assignments, queue)
        if not clauses:
            print(f"satisfiable: variable assignments = {assignments}")
            print(f"queue after = {assignments}")
            print()
            return
        continue 
    print(f"unsatisfied after pure literal elimination: variable assignments = {assignments}")
    print(f"queue after = {assignments}")
    print()
    return

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
                queue = []
                print(f'Problem {problem}')
            elif line[0] == 'p':
                n_vars = int(line[2])
                n_clauses = int(line[3])
                assignments = [None] * n_vars
            else:
                clauses.append([])
                i = 0
                for literal in line[:-1]:
                    if int(literal) == 0:
                        clause += 1
                        continue
                    clauses[clause].append(int(literal))
                if clause > n_clauses - 1:
                    print(clauses)
                    queue.append([clause[:] for clause in clauses])
                    print("original queue")
                    print(queue)
                    dpll_algorithm(clauses, assignments, queue)
                    continue
    
if __name__ == '__main__':
    main()