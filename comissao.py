import sys

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
    if is_feasible(solution, candidates, l):
        if len(solution) < len(best_solution) or not best_solution:
            return solution
        return best_solution

    choices = compute_choices(solution, candidates, l, disable_pruning)
    
    # Apply bounding function
    if not disable_optimality_cuts:
        bounding_function = original_bounding_function if use_original_bounding else improved_bounding_function
        B = bounding_function(solution, choices, candidates, l)
        if best_solution and B >= len(best_solution):
            return best_solution

    for choice in choices:
        if choice not in solution:  # Avoid adding the same candidate twice
            new_solution = solution + [choice]
            result = backtrack(new_solution, candidates, l, best_solution, disable_pruning, disable_optimality_cuts, use_original_bounding)
            if result:
                if not best_solution or len(result) < len(best_solution):
                    best_solution = result

    return best_solution

def main():
    disable_pruning = '-f' in sys.argv
    disable_optimality_cuts = '-o' in sys.argv
    use_original_bounding = '-a' in sys.argv
    l, n, candidates = read_input()
    
    initial_solution = []
    best_solution = backtrack(initial_solution, candidates, l, None, disable_pruning, disable_optimality_cuts, use_original_bounding)

    if best_solution:
        print(' '.join(str(i+1) for i in best_solution))
    else:
        print("Inviavel")

if __name__ == "__main__":
    main()