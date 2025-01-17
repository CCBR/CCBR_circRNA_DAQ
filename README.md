# CHARLIE

**C**ircrnas in **H**ost **A**nd vi**R**uses ana**L**ysis p**I**p**E**line

[![build](https://github.com/CCBR/CHARLIE/actions/workflows/build.yml/badge.svg)](https://github.com/CCBR/CHARLIE/actions/workflows/build.yml)
[![docs](https://github.com/CCBR/CHARLIE/actions/workflows/docs-mkdocs.yml/badge.svg)](https://ccbr.github.io/CHARLIE)
[![license](https://img.shields.io/github/license/CCBR/CHARLIE)](https://github.com/CCBR/CHARLIE/blob/main/LICENSE)
[![issues](https://img.shields.io/github/issues/CCBR/CHARLIE)](https://github.com/CCBR/CHARLIE/issues)
[![PRs](https://img.shields.io/github/issues-pr/CCBR/CHARLIE)](https://github.com/CCBR/CHARLIE/pulls)
![forks](https://img.shields.io/github/forks/CCBR/CHARLIE)
![stars](https://img.shields.io/github/stars/CCBR/CHARLIE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.13770166.svg)](https://doi.org/10.5281/zenodo.13770166)

See the website for detailed information, documentation, and examples:
<https://ccbr.github.io/CHARLIE/>

### Table of Contents

- [CHARLIE](#charlie)
  - [Table of Contents](#table-of-contents)
  - [1. Introduction](#1-introduction)
  - [2. Flowchart](#2-flowchart)
  - [3. Software Dependencies](#3-software-dependencies)
  - [4. Usage](#4-usage)
  - [5. License](#5-license)
  - [6. Testing](#6-testing)
    - [6.1 Test data](#61-test-data)
    - [6.2 Expected output](#62-expected-output)

### 1. Introduction

**C**ircrnas in **H**ost **A**nd vi**R**uses ana**L**ysis p**I**p**E**line

Things to know about CHARLIE:

- Snakemake workflow to detect, annotate and quantify (DAQ) host and viral circular RNAs.
- Primirarily developed to run on [BIOWULF](https://hpc.nih.gov/)
- Reach out to [Vishal Koparde](mailto:vishal.koparde@nihgov) for questions/comments/requests.

This circularRNA detection pipeline uses CIRCExplorer2, CIRI2 and many other tools in parallel to detect, quantify and annotate circRNAs. Here is a list of tools that can be run using CHARLIE:

| circRNA Detection Tool                                      | Aligner(s)       | Run by default |
| ----------------------------------------------------------- | ---------------- | -------------- |
| [CIRCExplorer2](https://github.com/YangLab/CIRCexplorer2)   | STAR<sup>1</sup> | Yes            |
| [CIRI2](https://sourceforge.net/projects/ciri/files/CIRI2/) | BWA<sup>1</sup>  | Yes            |
| [CIRCExplorer2](https://github.com/YangLab/CIRCexplorer2)   | BWA<sup>1</sup>  | Yes            |
| [CLEAR](https://github.com/YangLab/CLEAR)                   | STAR<sup>1</sup> | Yes            |
| [DCC](https://github.com/dieterich-lab/DCC)                 | STAR<sup>2</sup> | Yes            |
| [circRNAFinder](https://github.com/bioxfu/circRNAFinder)    | STAR<sup>3</sup> | Yes            |
| [find_circ](https://github.com/marvin-jens/find_circ)       | Bowtie2          | Yes            |
| [MapSplice](https://github.com/merckey/MapSplice2)          | BWA<sup>2</sup>  | No             |
| [NCLScan](https://github.com/TreesLab/NCLscan)              | NovoAlign        | No             |

> Note: STAR<sup>1</sup>, STAR<sup>2</sup>, STAR<sup>3</sup> denote 3 different sets of alignment parameters, etc.

> Note: BWA<sup>1</sup>, BWA<sup>2</sup> denote 2 different alignment parameters, etc.

### 2. Flowchart

![flowchart](https://raw.githubusercontent.com/CCBR/CHARLIE/main/docs/images/CHARLIE_v0.8.x.png)

For complete documentation, view the website <https://CCBR.github.io/CHARLIE/>.

> ⚠️ DISCLAIMER: New circRNA tools have been added CHARLIE and the documentation is currently out of date!

### 3. Software Dependencies

CHARLIE is already installed on biowulf.
It is included in the ccbrpipeliner module from release 7 onward.
To load the module run:

```bash
module load ccbrpipeliner/7
```

The following version of various bioinformatics tools are using within CHARLIE:

| tool          | version  |
| ------------- | -------- |
| blat          | 3.5      |
| bedtools      | 2.30.0   |
| bowtie        | 2-2.5.1  |
| bowtie        | 1.3.1    |
| bwa           | 0.7.17   |
| circexplorer2 | 2.3.8    |
| cufflinks     | 2.2.1    |
| cutadapt      | 4.4      |
| fastqc        | 0.11.9   |
| hisat         | 2.2.2.1  |
| java          | 18.0.1.1 |
| multiqc       | 1.9      |
| parallel      | 20231122 |
| perl          | 5.34     |
| picard        | 2.27.3   |
| python        | 2.7      |
| python        | 3.8      |
| sambamba      | 0.8.2    |
| samtools      | 1.16.1   |
| STAR          | 2.7.6a   |
| stringtie     | 2.2.1    |
| ucsc          | 450      |
| R             | 4.0.5    |
| novocraft     | 4.03.05  |

### 4. Usage

```bash
charlie


##########################################################################################

Welcome to
 _______  __   __  _______  ______    ___      ___   _______
|       ||  | |  ||   _   ||    _ |  |   |    |   | |       |
|       ||  |_|  ||  |_|  ||   | ||  |   |    |   | |    ___|
|       ||       ||       ||   |_||_ |   |    |   | |   |___
|      _||       ||       ||    __  ||   |___ |   | |    ___|
|     |_ |   _   ||   _   ||   |  | ||       ||   | |   |___
|_______||__| |__||__| |__||___|  |_||_______||___| |_______|

C_ircrnas in H_ost A_nd vi_R_uses ana_L_ysis p_I_p_E_line

##########################################################################################

This pipeline was built by CCBR (https://bioinformatics.ccr.cancer.gov/ccbr)
Please contact Vishal Koparde for comments/questions (vishal.koparde@nih.gov)

##########################################################################################

CHARLIE can be used to DAQ(Detect/Annotate/Quantify) circRNAs in hosts and viruses.

Here is the list of hosts and viruses that are currently supported:

HOSTS:
  * hg38          [Human]
  * mm39          [Mouse]

ADDITIVES:
  * ERCC          [External RNA Control Consortium sequences]
  * BAC16Insert   [insert from rKSHV.219-derived BAC clone of the full-length KSHV genome]

VIRUSES:
  * NC_007605.1   [Human gammaherpesvirus 4 (Epstein-Barr virus)]
  * NC_006273.2   [Human betaherpesvirus 5 (Cytomegalovirus )]
  * NC_001664.4   [Human betaherpesvirus 6A (HHV-6A)]
  * NC_000898.1   [Human betaherpesvirus 6B (HHV-6B)]
  * NC_001716.2   [Human betaherpesvirus 7 (HHV-7)]
  * NC_009333.1   [Human gammaherpesvirus 8 (KSHV)]
  * NC_045512.2   [Severe acute respiratory syndrome(SARS)-related coronavirus]
  * MN485971.1    [HIV from Belgium]
  * NC_001806.2   [Human alphaherpesvirus 1 (Herpes simplex virus type 1)](strain 17) (HSV-1)]
  * KT899744.1    [HSV-1 strain KOS]
  * MH636806.1    [MHV68 (Murine herpesvirus 68 strain WUMS)]

##########################################################################################

USAGE:
  charlie -w/--workdir=<WORKDIR> -m/--runmode=<RUNMODE>

Required Arguments:
1.  WORKDIR     : [Type: String]: Absolute or relative path to the output folder with write permissions.

2.  RUNMODE     : [Type: String] Valid options:
    * init      : initialize workdir
    * dryrun    : dry run snakemake to generate DAG
    * run       : run by submitting the job with slurm
    * qsub      : run by submitting the job with qsub
    * runlocal  : run without submitting to sbatch
    ADVANCED RUNMODES (use with caution!!)
    * unlock    : unlock WORKDIR if locked by snakemake NEVER UNLOCK WORKDIR WHERE PIPELINE IS CURRENTLY RUNNING!
    * reconfig  : recreate config file in WORKDIR (debugging option) EDITS TO config.yaml WILL BE LOST!
    * reset     : DELETE workdir dir and re-init it (debugging option) EDITS TO ALL FILES IN WORKDIR WILL BE LOST!
    * printbinds: print singularity binds (paths)
    * local     : same as runlocal
    * slurm     : same as run (run with slurm)

Optional Arguments:

--singcache|-c  : singularity cache directory. Default is `/data/${USER}/.singularity` if available, or falls back to `${WORKDIR}/.singularity`. Use this flag to specify a different singularity cache directory.
--host|-g       : supply host at command line. hg38 or mm39.                                            (--runmode=init only)
--additives|-a  : supply comma-separated list of additives at command line. ERCC or BAC16Insert or both (--runmode=init only)
--viruses|-v    : supply comma-separated list of viruses at command line                                (--runmode=init only)
--manifest|-s   : absolute path to samples.tsv. This will be copied to output folder                    (--runmode=init only)
--changegrp|-z  : change group to "Ziegelbauer_lab" before running anything. Biowulf-only. Useful for correctly setting permissions.
--platform      : set the HPC platform (biowulf, fnlcr, eddie). If not set, CHARLIE will try to detect the platform with `scontrol`.
--help|-h       : print this help


Example commands:
  charlie -w=/my/output/folder -m=init
  charlie -w=/my/output/folder -m=dryrun
  charlie -w=/my/output/folder -m=run

##########################################################################################

VersionInfo:
  python          : 3
  snakemake       : 7
  pipeline_home   : /gpfs/gsfs10/users/CCBR_Pipeliner/Pipelines/CHARLIE/.v0.11.1
  git commit/tag  : 613fb617f1ed426fb8900f98e599ca0497a67cc0    v0.11.0-49-g613fb61

##########################################################################################
```

### 5. License

MIT License

Copyright (c) 2021 Vishal Koparde

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

### 6. Testing

#### Init

Run init mode:

```bash
bash <path to charlie> -w=<path to output dir> -m=init
```

This will create the folder provided by `-w=`. The user should have write permission to this folder.

#### Dry-run

Test data (1 paired-end subsample and 1 single-end subsample) have been including under the `/data/CCBR_Pipeliner/testdata/circRNA/human` folder. After running in `-m=init`, `samples.tsv` should be edited to point the copies of the above mentioned samples with the column headers:

- sampleName
- path_to_R1_fastq
- path_to_R2_fastq

Column `path_to_R2_fastq` will be blank in case of single-end samples.

After editing `samples.tsv`, dry run should be run:

```bash
bash <path to charlie> -w=<path to output dir> -m=dryrun
```

This will create the reference fasta and gtf file based on the selections made in the `config.yaml`.

#### Run

If `-m=dryrun` was successful, then simply do `-m=run`. The output will look something like this

```
... ... skipping ~1000 lines
...
...
Job stats:
job                                              count    min threads    max threads
---------------------------------------------  -------  ----------
all                                                  1              1              1
annotate_clear_output                                2              1              1
circExplorer                                         2              2              2
circExplorer_bwa                                     2              2              2
circrnafinder                                        2              1              1
ciri                                                 2             56             56
clear                                                2              2              2
create_bowtie2_index                                 1              1              1
create_bwa_index                                     1              1              1
create_circExplorer_BSJ_bam                          2              4              4
create_circExplorer_linear_spliced_bams              2             56             56
create_circExplorer_merged_found_counts_table        2              1              1
create_hq_bams                                       2              1              1
create_index                                         1             56             56
create_master_counts_file                            1              1              1
cutadapt                                             2             56             56
dcc                                                  2              4              4
dcc_create_samplesheets                              2              1              1
estimate_duplication                                 2              1              1
fastqc                                               2              4              4
find_circ                                            2             56             56
find_circ_align                                      2             56             56
merge_SJ_tabs                                        1              2              2
merge_alignment_stats                                1              1              1
merge_genecounts                                     1              1              1
merge_per_sample                                     2              1              1
star1p                                               2             56             56
star2p                                               2             56             56
star_circrnafinder                                   2             56             56
total                                               52              1             56

Reasons:
    (check individual jobs above for details)
    input files updated by another job:
        alignment_stats, all, annotate_clear_output, circExplorer, circExplorer_bwa, circrnafinder, ciri, clear, create_circExplorer_BSJ_bam, create_circExplorer_linear_spliced_bams, create_circExplorer_merged_found_counts_table, create_hq_bams, create_master_counts_file, dcc, dcc_create_samplesheets, estimate_duplication, fastqc, find_circ, find_circ_align, merge_SJ_tabs, merge_alignment_stats, merge_genecounts, merge_per_sample, star1p, star2p, star_circrnafinder
    missing output files:
        alignment_stats, annotate_clear_output, circExplorer, circExplorer_bwa, circrnafinder, ciri, clear, create_bowtie2_index, create_bwa_index, create_circExplorer_BSJ_bam, create_circExplorer_linear_spliced_bams, create_circExplorer_merged_found_counts_table, create_hq_bams, create_index, create_master_counts_file, cutadapt, dcc, dcc_create_samplesheets, estimate_duplication, fastqc, find_circ, find_circ_align, merge_SJ_tabs, merge_alignment_stats, merge_genecounts, merge_per_sample, star1p, star2p, star_circrnafinder

This was a dry-run (flag -n). The order of jobs does not reflect the order of execution.
Running...
14743440
```

##### 6.1 Test Data

The `/data/CCBR_Pipeliner/testdata/circRNA/human` folder in the repo has test dataset:

```bash
tree /data/CCBR_Pipeliner/testdata/circRNA/human
/data/CCBR_Pipeliner/testdata/circRNA/human
├── GI1_N_ss.R1.fastq.gz
├── GI1_N_ss.R2.fastq.gz
├── GI1_T_ss.R1.fastq.gz
└── samples.tsv
```

`GI1_N` is a PE sample while `GI1_T` is a SE sample.

##### 6.2 Expected Output

Expected output from the sample data is stored under `.tests/expected_output`.

More details about running test data can be found [here](https://ccbr.github.io/CHARLIE/tutorial).

> DISCLAIMER:
>
> CHARLIE is built to be run only on [BIOWULF](https://hpc.nih.gov). A newer HPC-agnostic version of CHARLIE is planned for 2024.
