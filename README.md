# MethylDot
This is a tool for extraction and Dot-plot-like visualization of methylation status of a defined genomic region across experimental samples. Input data type supports converage file (.cov) from methylation_extractor included in bismark (http://www.bioinformatics.babraham.ac.uk/projects/bismark/). The advantage of such plot type is that it is useful to see the methylation patterns in a defined genomic region (typically, promoters/enhancers/et al.) in different experimental samples. This small tool provides the function for any genomic region you are interested in. However, I would strongly suggest controlling the region size considering the aesthetics. Output of this tool will be a data file (already in long-format) as well as a R script (If `-r` is specifeid). Normally, there is no need to modify the R the script (meaning you can subject it to R and get a nice figure back directly), however, if your desired region contains too much CpG sites, the figure may look weird. You can open the R script and change the plot parameters if needed. The plot ultilized R package `ggplot2` for better look.  

# Installation
First of all, python 2.7 environment is required, you also can install R - If you are willing to run the generated R script on your computer - in that case, package `ggplot2` is required. 
To get ggplot2 in your R, please type:
```
install.packages('ggplot2')
```
in your R console.
Download the `MethylDot.py`.
Prepare your data file (So far, it only supports coverage file from bismark).
Then, everything is good to go.

# Usage
Like any other bioinformatics tools that work under Linux/Unix enviroment, `MethylDot.py` provides several options and arguments to be filled. 

## Basic Usage
```
python /script/where/you/store/MethylDot.py [Options] file [file1,file2,file3]
```
For the list of files you provide, all files should be joint by comma (e.g. `file1,file2,file3...`) with their full path provided, unless you are currently under THE directory of your data files. 
## Required Arguments
```
  -h, --help                        show this help message and exit
  -o OUTPUT, --output               FULL PATH of output file containing methylation information for the desired region.
  -c CHROMOSOME, --chromosome       Define your desired chromosome.
  -s START, --start                 Define the start position of your desired region.
  -e END, --end                     Define the end position of your desired region.
  -l METHYL_LVL, --level            Define the level of methylation to be consider as a methylated site. Range: 0 to 1.
```
## Optional arguments
```
  -r, --rscript                     Whether to call plotting function or not. (Default=OFF)
  -p PATH, --path                   Define the path for rscript and plot storing. Must be a directory ended with a "/".
```
For optional arguments, if `-r` is specified, then `-p` is required. Optional arguments provide function generating an R script that could be run directly to generate the plot. The reason I did not include calling R to run the script is due to differenct R environments installed different computer/high performance computer. Anyhoo, the generated R script is ready to go once you installed `ggplot2`.

# Example
The following script was used for a bovine genome project.
```
python MethylDot.py -o /your/path/test.txt \
-r \
-c Chr1 \
-s 1000 \
-e 5000 \
-l 0.1 \
-p /data/macee77aggie/ \
/your/path/sample1.cov,/your/path/sample2.cov/,your/path/sample3.cov,/your/path/sample4.cov,/your/path/sample5.cov
```
As a result, the reults are one `test.txt` and one `methyl_dot.R`. You can find them in this repository. The R script was run and the generated dot plot (`test.png`) is also under the same directory. 

For any further questions, please contact:
guosong.wang@tamu.edu or guosonwang@gmail.com
