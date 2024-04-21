#!/bin/sh
#SBATCH --partition=dggpu
#SBATCH --nodes=1
#SBATCH --ntasks=5
#SBATCH --mem=60G
#SBATCH --gres=gpu:4
#SBATCH --time=12:00:00
#SBATCH --job-name=finetune

python main.py "$@"