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
    host_parameters = ['localhost']
    num_stages_parameters = [1,2,4,8,16]

    num_cores_parameters = [1,2,4,8]
    num_tasks_parameters = [1,2,4,8,16]

    #task_length_parameters = [0,1,4,8,16,32,64]
    task_length_parameters = [0]

    results = {}

    host = host_parameters[0]
    num_stages = num_stages_parameters[0]

    for run in range(runs):

        for cores in num_cores_parameters:

            for num_tasks in num_tasks_parameters:

                for task_length in task_length_parameters:

                    resource_desc = mtms.Resource_Description()
                    resource_desc.resource = host
                    resource_desc.runtime = 240 # minutes
                    resource_desc.cores = cores
                    resource_desc.dburl = dburl

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
                        print 'Exception occurred: %s' % e
                        continue

                    result = (engine.makespan, engine.ting2ted, engine.sub2run, engine.run2fin)

                    measurement = (host, num_stages, cores, num_tasks, task_length)
                    if (measurement) not in results:
                        results[measurement] = []
                    results[measurement].append(result)

                    print result

    print results

#
###############################################################################
