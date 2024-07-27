#!/bin/bash

# Function to run the program with given options and input file
run_test() {
    echo "Running with options: $1" >> "$2.metricas"
    echo "Input file: $2" >> "$2.metricas"
    (./comissao.py $1 < $2 2>&1) | tee -a "$2.metricas"
    echo "----------------------------------------" >> "$2.metricas"
}

# Run tests for each example
for i in {1..3}
do
    echo "Example $i:" > "ex$i.txt.metricas"
    
    # No pruning
    run_test "-f -o -a" "ex$i.txt"
    
    # Feasibility pruning only
    run_test "-o -a" "ex$i.txt"
    
    # Feasibility and original optimality pruning
    run_test "-a" "ex$i.txt"
    
    # Feasibility and improved optimality pruning
    run_test "" "ex$i.txt"
    
    echo "========================================" >> "ex$i.txt.metricas"
done