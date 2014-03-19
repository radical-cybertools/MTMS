#!/usr/bin/env python

import mtms

###############################################################################
#
# Main
#
if __name__ == '__main__':

    resource_desc = {}

    num_tasks = 2
    num_stages = 3
    duration = 0

    task_desc = mtms.Task_Description()
    task_desc.tasks = range(num_tasks) # Could be any set of "items"
    task_desc.num_stages = num_stages
    task_desc.executable = '/bin/echo'
    task_desc.arguments = duration

    io_desc = mtms.IO_Description()

    engine = mtms.Engine()
    engine.execute(resource_desc, task_desc, io_desc)

#
###############################################################################
