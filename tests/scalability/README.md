#Scalability requirements and testing for MTMS

##Application introduction

The goal is to develop workflows for simulating arbitrary collections of mononucleosomes
in atomic detail as an online tool for comparative genomics that complements and extends
traditional bioinformatics tools or coarse grain models such as our Interactive
Chromatin Modeling (ICM) server at Louisiana Tech (www.latech.edu/b̃ishop).

In this study, we seek to localize and compare 5 potential nucleosome sites,
where we need to simulate 105 mononucleosome configurations for 20 nanoseconds.
This is a non-trivial undertaking and requires support for scalable, flexible and advanced execution modes.
Since the 105 configurations are independent, a properly implemented solution,
given sufficient resources, allows us to complete the study in as little as 1 day.

The information on this page about the application and computational experiments are taken from the following paper:
["Scalable online comparative genomics of mononucleosomes: a BigJob"](http://dl.acm.org/citation.cfm?id=2484819).

##Computational and data requirements

The workflow requires 105 chained sequences with each task in a chain being
dependent upon successful completion and output of the previous task.
There are 20 steps in every chain, which sums up to 2100 simulations.
Every simulation needs to run on ~240 cores for about 1 hour.
The application used is NAMD.

Initial input for for each task is ~40 MB.
The output of every step totals ~4GB, of which just ~7MB is required to be passed to the next step.
All other output is a combination of diagnostics and files for out-of-band analysis.


##Experiments

The 105 chained sequences are independent and can be run in parallel.
The number of 240 cores required for every simulation is taken from the paper and likely differs per compute resource.

I would like to explore the number of cores per simulation on the simulation duration.
In addition, the splicing and dicing will have influence on the number of data transfers.

"Feature requests"
- Transferred data volume


##Experimental data format and considerations

Currently, I have collected data in the following structure as python dicts:

```python
>>> results.keys()
# (Host, number of stages, number of cores, number of tasks, length)
[('localhost', 8, 1, 16, 0), ('localhost', 8, 4, 8, 0), ('localhost', 8, 2, 2, 0), ('localhost', 8, 1, 4, 0), ('localhost', 8, 2, 8, 0), ('localhost', 8, 4, 1, 0), ('localhost', 8, 8, 2, 0), ('localhost', 8, 8, 16, 0), ('localhost', 8, 2, 1, 0), ('localhost', 8, 2, 16, 0), ('localhost', 8, 2, 4, 0), ('localhost', 8, 8, 4, 0), ('localhost', 8, 4, 2, 0), ('localhost', 8, 4, 4, 0), ('localhost', 8, 8, 1, 0), ('localhost', 8, 4, 16, 0), ('localhost', 8, 1, 8, 0), ('localhost', 8, 1, 1, 0), ('localhost', 8, 1, 2, 0), ('localhost', 8, 8, 8, 0)]
```

```python
>>> results[('localhost', 8, 1, 16, 0)]
# (makespan, submitting2submitted, submitted2running, running2done)
[(datetime.timedelta(0, 259, 837489), datetime.timedelta(0, 0, 466942), datetime.timedelta(0, 3769, 765585), datetime.timedelta(0, 128, 630636)), (datetime.timedelta(0, 260, 792232), datetime.timedelta(0, 0, 445014), datetime.timedelta(0), datetime.timedelta(0)), (datetime.timedelta(0, 259, 753113), datetime.timedelta(0, 0, 431306), datetime.timedelta(0, 3769, 40693), datetime.timedelta(0, 128, 579386))]
```
