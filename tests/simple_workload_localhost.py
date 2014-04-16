#!/usr/bin/env python

from radical.ensemblemd import mtms

import unittest

class Test(unittest.TestCase):

    def test__allways_succeed(self):
        return

    def test__simple_workload(self):
        NUM_TASKS = 3
        NUM_STAGES = 2

        #
        # Resource configuration
        #
        resource_desc = mtms.Resource_Description()
        resource_desc.runtime = 42 # minutes
        resource_desc.cores = 1
        resource_desc.resource = 'localhost'

        task_desc = mtms.Task_Description()
        task_desc.tasks = ['task-%d' % i for i in range(NUM_TASKS)]
        task_desc.num_stages = NUM_STAGES
        task_desc.executable = '/bin/echo'
        task_desc.arguments = 'Hello, I am task ${__TASK__} at stage ${__STAGE__}.'

        io_desc = mtms.IO_Description()

        engine = mtms.Engine()
        engine.execute(resource_desc, task_desc, io_desc, verbose=False)
