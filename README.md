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

To verify that the installation was successful you can run:
```bash
python -c 'import radical.ensemblemd.mtms as mtms; print mtms.version'
```
This should print a version number. If you get an import error, get in touch with us.

## The core library

This is the generic Multi-Task Multi-Stage library

```python
from radical.ensemblemd import mtms

res = mtms.Resource_Description()
io = mtms.IO_Description()
tasks = mtms.Task_Description()
engine = mtms.Engine()

engine.execute(res, tasks, io)
```

## Example: NAMD workflow

This is the NAMD workflow specific example that makes use of the mtms library.
To run the supplied example, you can run:

```bash
python examples/namd_mtms_wf.py
```
This should give you the output of a verbose run of an MTMS application.
Please look at the example to get a feeling for how to write your own.
