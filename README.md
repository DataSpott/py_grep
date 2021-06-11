# py_grep

Search excel-, csv- and tsv-files through arbitrary columns for one or multiple search terms.

Following file-formats are supported:
xls, xlsx, xlsm, xlsb, odf, ods, odt, csv & tsv

## Requirements
For the use of *py_grep* in your terminal there are two options.

### 1. Setup on your own system:
* clone this git-repository to your computer using the command
```bash
git clone https://github.com/DataSpott/SGT-Analysis.git
```
* if not already installed use the following command to install pip for python3 in your terminal
```bash
sudo apt install python3-pip
```
* use the following command to set up the necessary python-modules
```bash
pip3 install pandas
```
* to start *py_grep* use the following command in the repository directory
```bash
$PWD/py_grep.py --help
```

### 2. Use the docker-container:
* make sure docker is installed at your system as described under https://docs.docker.com/get-docker/
* locate your data to the git repository
* use following command in the repository directory to pull the docker-image to your system, mount all data in the current directory to the container-directory "/input"* and execute it
```bash
docker run --rm -it -v $PWD:/input dataspott/sgt_analyser:v0.9.1
```
* inside the docker a python3 environment is pre-installed and py_grep can be executed as follows
```bash
/input/py_grep.py --help
```

## Usage
*py_grep* offers support for xls-, tsv- and csv-files. Conversion is done automatically.

Following flags can be used to control the program:

**Necessary flags**

Flag|Description
-|-
**[-i]  [--input]**|Path to the input file to read the data from
**[-s]  [--search]**|One or multiple terms to search for

**Optional flags**

Flag|Description
-|-
**[-c]  [--columns]**|One or multiple columns of the table to search through. By default all columns will be searched [default: all].
**[-d]  [--deact_search_str]**|Deactivates the output of the information string (which terms were searched in which columns) in the first row of the result-file.
**[-n]  [--sheet]**|Number or name of the excel-sheet, which is taken as input. You can also specify a range of sheets without whitespaces, e.g. '1-4'. By default all sheets of the file are taken [default: None].
**[-o]  [--output]**|Output-directory where *py_grep* creates its result-directory. By default the output-directory is the current working directory [default: $PWD].
**[-r]  [--reverse]**|Reverses the search, so that *py_grep* searches for everything except the search-terms given via the [--search]-flag.
**[--md]**|Activates output of the result-file in .md-format.
**[--csv]**|Activates output of the result-file in .csv-format.
**[--tsv]**|Deactivates output of the result-file in .tsv-format.
**[--isnull]**|Searches for NaN (Overwrites [-s]).
**[--notnull]**|Searches for notNaN (Overwrites [-s]).
**[-h]  [--help]**|Shows the help-message.
