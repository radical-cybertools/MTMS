import datetime
from results import results
import numpy

print results

#measurement = (host, num_stages, cores, num_tasks, task_length)
#result = (engine.makespan, engine.ting2ted, engine.sub2run, engine.run2fin)

#runs = max([x[0] for x in results.keys])+1
#print 'Total number of runs: %d' % runs


hosts = set([x[0] for x in results.keys()])
print 'Hosts used for experiments: %s' % [x for x in hosts]

stage_counts = sorted(list(set([x[1] for x in results.keys()])))
print 'Number of stages used for experiments: %s' % stage_counts

core_counts = sorted(list(set([x[2] for x in results.keys()])))
print 'Number of cores used for experiments: %s' % core_counts

task_counts = sorted(list(set([x[3] for x in results.keys()])))
print 'Number of tasks used for experiments: %s' % task_counts

task_lengths = sorted(list(set([x[4] for x in results.keys()])))
print 'Length of tasks used for experiments: %s' % task_lengths

for h in hosts:
    for s in stage_counts:
        for c in core_counts:
            for t in task_counts:
                for l in task_lengths:
                    result = results[(h,s,c,t,l)]
                    #self.sub2run = sum( [x['ts_running'] - x['ts_submitted'] for x in self.task_repo.values()], datetime.timedelta())
                    #print 'host:%s,stages:%d,cores:%s,tasks:%d,length:%d = ' % (h,s,c,t,l),

                    makespan_avg = numpy.average([x[0].total_seconds() for x in result])
                    makespan_std = numpy.std([x[0].total_seconds() for x in result])

                    ting2ted_avg = numpy.average([x[1].total_seconds() for x in result])
                    ting2ted_std = numpy.std([x[1].total_seconds() for x in result])

                    sub2run_avg = numpy.average([x[2].total_seconds() for x in result])
                    sub2run_std = numpy.std([x[2].total_seconds() for x in result])

                    run2fin_avg = numpy.average([x[3].total_seconds() for x in result])
                    run2f_std = numpy.std([x[3].total_seconds() for x in result])

                    print 'makespan:%s, sub:%s, sub2run:%s, run2fin:%s' % (makespan_avg, ting2ted_avg, sub2run_avg, run2fin_avg)




