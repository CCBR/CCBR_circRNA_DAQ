#!usr/bin/env bash
# do not submit this script with qsub
# as worker nodes cannot submit additional jobs themselves

. /etc/profile.d/modules.sh
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
