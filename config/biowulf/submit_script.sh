#!/usr/bin/env bash
#SBATCH --job-name="charlie"
#SBATCH --mem=40g
#SBATCH --partition="$PARTITION"
#SBATCH --time=48:00:00
#SBATCH --cpus-per-task=2
#SBATCH --mail-type=BEGIN,END,FAIL

cd $SLURM_SUBMIT_DIR
$MODULE_LOAD
$EXPORT_SING_CACHE_DIR_CMD

snakemake -s $SNAKEFILE \
    --directory $WORKDIR \
    --use-singularity \
    --singularity-args "$SINGULARITY_BINDS" \
    --use-envmodules \
    --printshellcmds \
    --latency-wait 300 \
    --configfile $CONFIGFILE \
    --profile $CLUSTER_PROFILE \
    -j 500 \
    --rerun-incomplete \
    --rerun-triggers $trigger \
    --retries 2 \
    --keep-going \
    --stats ${WORKDIR}/snakemake.stats \
    2>&1 | tee ${WORKDIR}/snakemake.log

if [ "$?" -eq "0" ];then
  snakemake -s $SNAKEFILE \
  --directory $WORKDIR \
  --report ${WORKDIR}/runslurm_snakemake_report.html \
  --configfile $CONFIGFILE
fi
