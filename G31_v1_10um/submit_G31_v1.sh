#!/bin/sh
# Job Name:
#SBATCH -J G31_v1_test
# Standard output and error:
#SBATCH -o /u/gresi/radmc3d_code/G31_v1/G31_v1_10um/output.txt
# Initial working directory:
#SBATCH -D /u/gresi/radmc3d_code/G31_v1/G31_v1_10um
# Number of nodes and MPI tasks per node:
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
# Enable Hyperthreading:
#SBATCH --ntasks-per-core=2
# for OpenMP:
#SBATCH --cpus-per-task=40
# Request 180 GB of main memory per node in units of MB:
#SBATCH --mem=126000
#SBATCH --mail-type=end
#SBATCH --mail-user=gsiu@gapp.nthu.edu.tw
# Wall clock Limit:
#SBATCH --qos 28d
#SBATCH --time=672:00:00
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
# For pinning threads correctly
export OMP_PLACES=threads
export SLURM_HINT=multithread

radmc3d mctherm 
