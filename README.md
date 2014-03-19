#Multi-Task Multi-Stage libary

## Introduction

This library supports the Multi-Task Multi-Stage pattern: a workflow of parallel Tasks (pipelines) with the same number of stages (steps).
All tasks execute the same application, although with (possibly) different configuration and parameters.
For the execution mtms relies on RADICAL-Pilot.


## Installation

TODO

## The core library

This is the generic Multi-Task Multi-Stage library

```python
import mtms

res = mtms.Resource_Description()
io = mtms.IO_Description()
tasks = mtms.Task_Description()
engine = mtms.Engine()

engine.execute(res, tasks, io)
```

## Example: NAMD workflow

namd_mtms_wf

This is the NAMD workflow specific example that makes use of the mtms library.




