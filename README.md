# EdgeX Foundry Paper Study Tool
This Python script pulls stats from github.com and pkg.go.docs on Go modules/packages used in EdgeX.  It creates a CSV file which can easily be uploaded into Excel.

## Usage
1. Replace or update the 3rd party packages / modules used by EdgeX in modules.txt.  This can be obtained from go.mod files of the EdgeX repositories.
2. Replace the AUTH_TOKEN to use your personal GitHub token in moddata.py
3. Run the Python script:  `python3 moddata.py`

## Results
If there are no errors, it creates a file called paper-study.csv in the directory where it is run.  For each 3rd party package, the following is collected:

- Forks Count
- Watchers Count
- Stars Count
- Number of Contributors
- Number of Tags
- Number of Releases
- Last Release Date
- Last Commit Date
- License Type
- Number of projects using (import) the module
- Number of module imports the module makes (number of dependencies)
	
## Options
The DEBUG global in moddata.py can be set to False (its True by default) to run quietly.