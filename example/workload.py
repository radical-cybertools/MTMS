""" (Sample) workload definition file for NAMD.
"""

WORKLOAD = []

# replace the paths with your input file paths on stampede

for stage in range(1, 5):

    task = {
        "cpus" : 16, # processors
        "conf"   : "/work/01740/marksant/bishop_sample/stage%s.conf" % stage
    }

    WORKLOAD.append(task)
