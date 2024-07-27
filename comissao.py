#!/usr/bin/env python3
# coding=utf

import sys
import time

# Global counter for nodes
nodes_analyzed = 0

def read_input():
    l, n = map(int, input().split())
    candidates = []
    for _ in range(n):
        line = list(map(int, input().split()))
        candidates.append(set(line[1:]))
    return l, n, candidates

def is_feasible(solution, candidates, l):
    covered = set()
    for i in solution:
        covered.update(candidates[i])
    return len(covered) == l

def compute_choices(solution, candidates, l, disable_pruning):
    if disable_pruning:
        return set(range(len(candidates)))
    
    if len(solution) == 0:
        return set(range(len(candidates)))
    covered = set()
    for i in solution:
        covered.update(candidates[i])
    if len(covered) == l:
        return set()
    return set(range(solution[-1] + 1, len(candidates)))

def original_bounding_function(E, F, candidates, l):
    covered = set()
    for i in E:
        covered.update(candidates[i])
    return len(E) + (1 if len(covered) < l else 0)

def improved_bounding_function(E, F, candidates, l):
    # Compute covered elements
    covered = set()
    for i in E:
        covered.update(candidates[i])
    
    # Compute uncovered elements
    uncovered_elements = set(range(1, l+1)) - covered
    
    # Compute max_coverage
    max_coverage = 0
    for i in F:
        coverage = len(candidates[i] & uncovered_elements)
        max_coverage = max(max_coverage, coverage)
    
    # Avoid division by zero
    if max_coverage == 0:
        return len(E) + len(uncovered_elements)
    
    return len(E) + (len(uncovered_elements) + max_coverage - 1) // max_coverage

def backtrack(solution, candidates, l, best_solution, disable_pruning, disable_optimality_cuts, use_original_bounding):
    global nodes_analyzed
    nodes_analyzed += 1  # Increment node counter

    if is_feasible(solution, candidates, l):
        if best_solution is None or len(solution) < len(best_solution):
            return solution
        return best_solution

    choices = compute_choices(solution, candidates, l, disable_pruning)
    
    # Utiliza a função limitante, se cortes por otimalidade estiverem desabilitados
    if not disable_optimality_cuts:
        bounding_function = original_bounding_function if use_original_bounding else improved_bounding_function
        B = bounding_function(solution, choices, candidates, l)
        if best_solution is not None and B >= len(best_solution):
            return best_solution

    # Faz a busca em profundidade
    for choice in choices:
        if choice not in solution:
            new_solution = solution + [choice]
            result = backtrack(new_solution, candidates, l, best_solution, disable_pruning, disable_optimality_cuts, use_original_bounding)
            if result:
                if not best_solution or len(result) < len(best_solution):
                    best_solution = result

    return best_solution

def main():
    global nodes_analyzed
    disable_pruning = '-f' in sys.argv
    disable_optimality_cuts = '-o' in sys.argv
    use_original_bounding = '-a' in sys.argv
    l, n, candidates = read_input()
    
    initial_solution = []
    
    # Start timing
    start_time = time.time()
    
    best_solution = backtrack(initial_solution, candidates, l, None, disable_pruning, disable_optimality_cuts, use_original_bounding)
    
    # End timing
    end_time = time.time()
    execution_time = end_time - start_time

    if best_solution:
        print(' '.join(str(i+1) for i in best_solution))
    else:
        print("Inviavel")
    
    # Output metrics to stderr
    sys.stderr.write(f"Nós percorridos: {nodes_analyzed}\n")
    sys.stderr.write(f"Tempo de execução(s): {execution_time:.6f}\n")

if __name__ == "__main__":
    main()