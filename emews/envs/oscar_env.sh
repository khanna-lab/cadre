module load openmpi/4.1.2-s5wtoqb  
gcc -v #check that gcc/11 is loaded
module load r/4.3.1-lmofgb4
module load  python/3.11.0s-ixrhc3q

#module load gcc/10.2
#module load mpi/mvapich2-2.3.5_gcc_10.2_slurm22 cuda/11.7.1
#module load R/4.2.0
#module load python/3.9.0

export PATH=/gpfs/data/akhann16/sfw/tcl-8.6.12/bin:/gpfs/data/akhann16/sfw/apache-ant-1.10.12/bin:$PATH
export R_LIBS_USER=/gpfs/data/akhann16/sfw/rlibs/4.3.1
#export PATH=/gpfs/data/akhann16/sfw/swift-t/gcc-10.2/mvapich-2.3.5/12022022/stc/bin:$PATH

