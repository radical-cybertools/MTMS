#Multi-Task Multi-Stage libary

## Introduction

This library supports the Multi-Task Multi-Stage pattern: a workflow of parallel Tasks (pipelines) with the same number of stages (steps).
All tasks execute the same application, although with (possibly) different configuration and parameters.
For the execution mtms relies on RADICAL-Pilot.


## Installation

First we create a python virtual environment to safely play around:
```bash
virtualenv /tmp/ve
source /tmp/ve/bin/activate
```
Currently MTMS is only installable from source:
```bash
cd /tmp
git clone git@github.com:radical-cybertools/MTMS.git
cd MTMS
python setup.py install
```

To verify quickly that the installation was successful you can run:
```bash
python -c 'import radical.ensemblemd.mtms as mtms; print mtms.version'
```
This should print a version number. If you get an import error, get in touch with us.

## Tests provided

For a more elaborate testing of the code a suite of tests is available.
These can be executed by:
```bash
python setup.py test
```

Please report any errors to us, as these should all succeed in theory.

## The core library

This is the generic Multi-Task Multi-Stage library.
The minimal structure of the API and its usage is displayed below.

```python
from radical.ensemblemd import mtms

res = mtms.Resource_Description()
io = mtms.IO_Description()
tasks = mtms.Task_Description()
engine = mtms.Engine()

engine.execute(res, tasks, io)
```

## Example: NAMD workflow

This is a NAMD workflow specific example that makes use of the mtms library.
To run the supplied example, you can need to perform the following steps (from
the /tmp/MTMS directory created earlier).

First to create a dummy set of input data files:
```bash
./performance/populate_data_directory_small.sh
```
This creates a /tmp/MTMS/data directory that will be used during the
experiment.

To start the experiment, run the following command from the same directory.
```bash
python examples/namd_mtms_wf.py
```

This assumes you have an account on the TACC XSEDE Stampede cluster. If not,
you can configure to run on another cluster or on your localhost by changing
the code at line #22.

This should give you the output of a verbose run of an MTMS application.
Please look at the example code to get a feeling for how to write your own.
Note that for "portability" this workflow doesn't run the real namd binary, but
other than that the workflow is representative.
Depending on network speed and queueing times, this should take around 5
minutes to execute.
