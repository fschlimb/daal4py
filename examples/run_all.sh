#!/bin/sh

for ex in *_batch.py; do
    echo "Running $ex"
    python $ex || exit
done

for ex in *_dspv.py *_spmd.py ; do
    echo "Running $ex"
    (mpirun -genv DIST_CNC=MPI -n 4 python $ex -- 2>&1 | grep -viE 'cnc|communicator') || exit
done
