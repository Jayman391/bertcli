#!/bin/sh

#example configuration
save_dir="output"
data="tests/test_data/usa-vaccine-comments.csv"
num_samples=5000
#example sweep over LLMs, Dim Red algos, and Clustering algos with default sklearn parameters
for i in $(seq 1 6); do
    for j in $(seq 1 3); do
        for k in $(seq 1 3); do
            sequence="1,1${i},2${j},3${k},9"
            sbatch -N1 -n1 run.sh $save_dir"/${sequence}" $data $num_samples $sequence &
        done
    done
done