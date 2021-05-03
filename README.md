# py_grep

Search excel-, csv- and tsv-files through arbitrary columns for one or multiple search terms.

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
