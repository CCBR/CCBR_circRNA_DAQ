## CHARLIE development version

- Support Eddie (The University of Edinburgh's HPC cluster) with `--platform=eddie` and `--runmode=qsub`. (#136, @kelly-sovacool)

## CHARLIE 0.11.1

- CHARLIE was falsely throwing a file permissions error for tempdir values containing bash variables. (#118, @kelly-sovacool)
- Singularity bind paths were not being set properly. (#119, @kelly-sovacool)
- Update docker containers to set `$PYTHONPATH`. (#119, #125, @kelly-sovacool)
  - Otherwise, this environment variable can be carried over and cause package conflicts when singularity is not run with `-C`.
  - Also use `python -E` to ensure the `$PYTHONPATH` is not carried over. (#129, @kelly-sovacool)
- Fix `reconfig` to correctly replace variables in the config file. (#121, @kelly-sovacool)
- Prevent using excessive memory when copying reference files. (#126, @kelly-sovacool)
- Fix missing output files due to file system latency and use real (absolute) paths where possible. (#130, @kelly-sovacool)
- Update documentation to reflect biowulf usage and improved test dataset. (#132, @kelly-sovacool)

## CHARLIE 0.11.0

- Major updates to convert CHARLIE from a biowulf-specific to a platform-agnostic pipeline (#102, @kelly-sovacool):
  - All rules now use containers instead of envmodules.
  - Default config and cluster config files are provided for use on biowulf and FRCE.
  - New entry `TEMPDIR` in the config file sets the temporary directory location for rules that require transient storage.
  - New `--singcache` argument to provide a singularity cache dir location. The singularity cache dir is automatically set inside `/data/$USER/` or `$WORKDIR/` if `--singcache` is not provided.
- Minor documentation improvements. (#114, @kelly-sovacool)

## CHARLIE 0.10.1

- strand are reported together, strand from all callers are reported,
- both + and - flanking sites are reported,
- rev-comp function updated,
- updated versions of tools to match available tools on BIOWULF.

## CHARLIE 0.9.0

Significant upgrades since the last release:

- updates to wrapper script, many new arguments/options added
- new per-sample counts table format
- new all-sample master counts matrix with min-nreads filtering and ntools column to show number of tools supporting the circRNA call
- new version of Snakemake
- cluster_status script added for forced completion of pipeline upon TIMEOUTs
- updated flowchart from lucid charts
- added circRNAfinder, find_circ, circExplorer2_bwa and other tools
- optimized execution and resource requirements
- updated viral annotations (Thanks Sara!)
- new method to extract linear counts, create linear BAMs using circExplorer2 outputs
- new job reporting using jobby and its derivatives
- separated creation of BWA and BOWTIE2 index from creation of STAR index to speed things up
- parallelized find_circ
- better cleanup (eg. deleting \_STARgenome folders, etc.) for much smaller digital footprint
- multitude of comments throughout the snakefiles including listing of output file column descriptions
- preliminary GH actions added

## CHARLIE 0.7.0

- 5 circRNA callers
- all-sample counts matrix with annotations

## CHARLIE 0.6.9

- Optimized pysam scripts
- fixed premature completion of singularity rules

## CHARLIE 0.6.5

- updated config.yaml to use the latest HSV-1 annotations received from Sarah (050421)

## CHARLIE 0.6.4

- create linear reads BAM file
- create linear reads BigWigs for each region in the .regions file.

## CHARLIE 0.6.3

- QOS not working for Taka... removed from cluster.json
- recall rule requires python/3.7 ... env module updated

## CHARLIE 0.6.2

- BSJ files are in BSJ subfolder... bug fix for v0.6.1

## CHARLIE 0.6.1

- customBSJs recalled from STAR alignments
  - only for PE
  - removes erroneously called CircExplorer BSJs
- create sense and anti-sense BSJ BAMs and BW for each reference (host+viruses)
- find reads which contribute to CIRI BSJs but not on the STAR list of BSJ reads, see if they contribute to novel (not called by STAR) BSJs and append novel BSJs to customBSJ list

## CHARLIE 0.6.0

cutadapt_min_length to cutadapt rule... setting it to 15 in config (for miRNAs, Biot and short viral features)

## CHARLIE 0.5.0

- `run_clear` is now set to True (as default)
- `circ_quant` replaces `clear_quant` in the CLEAR rule. In order words, we are reusing the STAR alignment file and the circExplorer2 output file for running CLEAR. No need to run HISAT2 and TopHat (fusion-search with Bowtie1). This is much quicker.
- Using picard to estimate duplicates using[ _MarkDuplicates_](https://gatk.broadinstitute.org/hc/en-us/articles/360037052812-MarkDuplicates-Picard-)
- Generating a per-run [multiqc](https://multiqc.info/) HTML report
- Using [_eulerr_](https://www.rdocumentation.org/packages/eulerr/versions/6.1.0) R package to generate CIRI-CircExplorer circRNA Venn diagrams and include them in the mulitqc report
- Gather per job cluster metadata like queue time, run time, job state etc. Stats are compiled in **HPC_summary** file
- CLEAR pipeline _quant.txt_ file is annotated for known circRNAs
- `WORKDIR` can now be a relative path
- bam2bw conversion fix for BSJ and spliced_reads. [Issue](https://github.com/kopardev/circRNA/issues/17) closed!

## CHARLIE 0.4.0

- [CLEAR](https://github.com/YangLab/CLEAR) added.
- wrapper script (`run_circrna_daq.sh`) added for local and cluster execution.
- "spliced reads only" bam created and split by regions

## CHARLIE 0.3.0

- Lookup table for hg38 to hg19 circRNA annotations is updated... this eliminate one-to-many hits from the previous version
- BSJs extracted as different bam file.
- flowchart added
- adding slurmjobid to log/err file names
- v0.3.1 has significant (>10X) performance improvements at BSJ bam creation
- v0.3.3 splits BSJ bams into human and viral bams, and also converts them to bigwigs
- v0.3.4 adds hg38_rRNA_masked_plus_rRNA_plus_viruses_plus_ERCC reference (source:Sarah)

## CHARLIE 0.2.0

- SE support added .. PE/SE samples handled concurrently
- `envmodules` used in Snakemake in place of `module load` statements

## CHARLIE 0.1.0

- base version
- PE only support
