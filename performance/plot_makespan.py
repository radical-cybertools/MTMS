import datetime
#from results_local_mongo import results
from results_remote_mongo import results
import numpy
import matplotlib.pyplot as plt

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

avg = []
std = []
for h in hosts:
    for s in stage_counts:
        for c in core_counts:
            avg.append([])
            std.append([])
            for t in task_counts:
                for l in task_lengths:
                    result = results[(h,s,c,t,l)]
                    #self.sub2run = sum( [x['ts_running'] - x['ts_submitted'] for x in self.task_repo.values()], datetime.timedelta())
                    #print 'host:%s,stages:%d,cores:%s,tasks:%d,length:%d = ' % (h,s,c,t,l),

                    makespan_avg = numpy.average([x[0].total_seconds() for x in result])
                    makespan_std = numpy.std([x[0].total_seconds() for x in result])

                    avg[core_counts.index(c)].append(makespan_avg)
                    std[core_counts.index(c)].append(makespan_std)
                    ting2ted_avg = numpy.average([x[1].total_seconds() for x in result])
                    ting2ted_std = numpy.std([x[1].total_seconds() for x in result])

                    sub2run_avg = numpy.average([x[2].total_seconds() for x in result])
                    sub2run_std = numpy.std([x[2].total_seconds() for x in result])

                    run2fin_avg = numpy.average([x[3].total_seconds() for x in result])
                    run2fin_std = numpy.std([x[3].total_seconds() for x in result])

                    print 'makespan:%f(%f), sub:%f(%f), sub2run:%f(%f), run2fin:%f(%f)' % \
                          (makespan_avg, makespan_std, ting2ted_avg, ting2ted_std, \
                           sub2run_avg, sub2run_std, run2fin_avg, run2fin_std)


x = task_counts

p = []
for c in core_counts:
    #plt.plot(x,avg[core_counts.index(c)])
    p.append(plt.errorbar(x,avg[core_counts.index(c)], std[core_counts.index(c)]))

plt.legend(p, core_counts, title='Pilot core count')

plt.xlabel('Number of tasks (pipelines)')
plt.ylabel('Makespan (seconds)')
plt.title('Makespan of MTMS execution on single pilot with varying number of (parallel) tasks and pilot sizes.\n'\
          'Execution on localhost with remote mongodb.\n' \
          'Number of stages is fixed at 8. Zero second payload.'
        )
plt.show()
