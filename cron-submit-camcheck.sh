#!/bin/bash
JOB_COUNT=$(qstat --header User:Command | grep thiruvat | grep cam_check | wc -l)
JOB_LIMIT=0
date
if [ "$JOB_COUNT" -gt "$JOB_LIMIT" ]; then
   echo "$JOB_COUNT running cam_check jobs; limit is $JOB_LIMIT. Not submitting"
else
   echo "$JOB_COUNT running cam_check jobs; limit is $JOB_LIMIT. Submitting."
   cd Work/Image_Archiever && qsub -A SE_HPC -t 30 -n 1 -q pubnet ./cam_check.sh
fi

