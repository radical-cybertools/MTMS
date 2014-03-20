#!/usr/bin/env python

import mtms

###############################################################################
#
# Main
#
if __name__ == '__main__':

    dburl  = 'mongodb://localhost:27017'
    #dburl = 'mongodb://ec2-184-72-89-141.compute-1.amazonaws.com:27017'

    runs = 3
    host = 'localhost'
    stages = 10
    #cores_parameters = [1,2,4,8,16]
    #cores_parameters = [2]
    cores_parameters = [2,4]

    num_tasks_parameters = [1,2,4,8,16]
    #num_tasks_parameters = [1,2,4,8,16]
    #num_tasks_parameters = [1]

    task_length_parameters = [0]

    results = []

    for run in range(runs):

        for cores in cores_parameters:

            for num_tasks in num_tasks_parameters:

                for task_length in task_length_parameters:

                    resource_desc = mtms.Resource_Description()
                    resource_desc.resource = host
                    resource_desc.runtime = 240 # minutes
                    resource_desc.cores = cores
                    resource_desc.dburl = dburl

                    num_stages = stages

                    task_desc = mtms.Task_Description()
                    task_desc.tasks = range(num_tasks) # Could be any set of "items"
                    task_desc.num_stages = num_stages
                    task_desc.executable = '/bin/echo'
                    task_desc.arguments = task_length

                    io_desc = mtms.IO_Description()

                    engine = mtms.Engine()
                    print 'Executing run: %d, on host: %s, with %d cores, %d tasks, %d stages, with a %ss task length ...' % \
                          (run, host, cores, num_tasks, num_stages, task_length)
                    try:
                        engine.execute(resource_desc, task_desc, io_desc, verbose=False)
                    except Exception, e:
                        print 'Exception occurred: %s' % e.message
                        continue

                    result = {
                        'run': run,
                        'host': host,
                        'cores': cores,
                        'num_tasks': num_tasks,
                        'num_stages': num_stages,
                        'task_length': task_length,
                        'makespan': engine.makespan,
                        'cum_submission_2_submitted_2': engine.ting2ted,
                        'cum_submitted_2_running': engine.sub2run,
                        'cum_running_2_finished': engine.run2fin
                    }
                    results.append(result)
                    print result

    print results

#
###############################################################################
