#Multi-Task Multi-Stage libary

## Introduction

This library supports the Multi-Task Multi-Stage pattern: a workflow of parallel Tasks (pipelines) with the same number of stages (steps).
All tasks execute the same application, although with (possibly) different configuration and parameters.
For the execution mtms relies on RADICAL-Pilot.


## Installation

First we create a python virtual environment to safely play around:
```bash
virtualenv /tmp/mtms-ve
source /tmp/mtms-ve/bin/activate
```
As MTMS depends on non-released versions of RADICAL-Pilot, SAGA-Python and MD-Kernels, we install those first.
```bash
mkdir /tmp/mtms-src
cd /tmp/mtms-src
git clone https://github.com/radical-cybertools/saga-python.git
cd saga-python
git checkout devel
python setup.py install
cd ..
git clone https://github.com/radical-cybertools/radical.pilot.git
cd radical.pilot
git checkout feature/staging
python setup.py install
cd ..
git clone https://github.com/radical-cybertools/radical.ensemblemd.mdkernels.git
cd radical.ensemblemd.mdkernels
git checkout release
python setup.py install
cd ..
```
Currently MTMS is only installable from source:
```bash
git clone https://github.com/radical-cybertools/MTMS.git
cd MTMS
git checkout staging
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
To run the supplied example, you can need to perform the described steps (from
the /tmp/MTMS directory created earlier).

The experiment configuration is based on the paper
["Scalable online comparative genomics of mononucleosomes: a BigJob"](http://dl.acm.org/citation.cfm?id=2484819).
The script uses the hierarchical directory layout for the input data as in the paper;
the first tier represents 5 chromosome sites, and the second tier represents 21 locations along the DNA sequence representing the start of the nucleosome.
You can see how that is used in the script at line 59 of examples/namd_mtms_wf.py.
For every location 20 simulations of 1ns are performed.

To cut execution time of this example, the number of chromosomes is 2, with each just 1 location and the number of simulations per location is 3.
This leads to 6 MD simulations instead of 2100.
Of course you are free to change these numbers, you can do that starting at line 34 of examples/namd_mtms_wf.py.

The current script assumes you have an account on the TACC XSEDE Stampede cluster.
If not, you can configure to run on another cluster or on your localhost by changing
the code at line 22 of examples/namd_mtms_wf.py.

Note that for demonstration purposes and saving you from the hassle of installing NAMD, this workflow doesn't run the real NAMD binary, but
other than that the workflow is completely genuine.

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
Depending on network speed and queueing times, this should take around 5
minutes to execute.

All with all this should give you the output of a verbose run of an MTMS application.
Please look at the example code to get a feeling for how to use MTMS for your own application.
