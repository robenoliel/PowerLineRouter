# PowerLineRouter

## Introduction

## Implementation

To install this module, its code must be acquired from the repository page. That can be done by forking or downloading the project. Once the user has the project on his computer, he should make sure his Python environment has all requirements for the module. The Python version should be compatible with `3.9.9` or above. To install any missing dependencies, open the command prompt at the project root folder and run:

```
pip install -r requirements
```

The road routing routines will be expecting input data organized in a folder as follows:

```
case
├───basemap
│   ├───height
│   └───slope
├───candidates
├───corridor
├───costmap
├───enviromental
├───environmental
├───facilities
├───hydrology
├───limits
├───railways
├───results
├───routes
├───social
├───temporary
├───transmission
├───transportation
├───urban
├─candidates.csv
├─constraints.csv
├─maps.csv
└─parameters.csv
```

Each case folder may contain several studies with different parameters, each of which should be described at the study files `candidates.csv`, `constraints.csv`, `maps.csv` and `parameters.csv`. Those same files should point to the data that will be used at each study. All data must be available at the case directories according to their meaning.

Once the environment and data are appropriately set, the user may run the program by, at the project root folder, running:

```
python .\src\main.py --path [PATH_TO_CASE]
```

Additional arguments are:
* `-v`, `--verbose`: verbose mode, defaults to false.
* `-s`, `--studies`: the list of studies to run, formatted as the study ids separated by comma. If not given, all studies at the case will be ran. 

## Methodology
