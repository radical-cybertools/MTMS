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

ting2ted_all_avg = []
ting2ted_all_std = []

sub2run_all_avg = []
sub2run_all_std = []

run2fin_all_avg = []
run2fin_all_std = []

for h in hosts:
    for s in stage_counts:
        for c in core_counts:
            ting2ted_all_avg.append([])
            ting2ted_all_std.append([])

            sub2run_all_avg.append([])
            sub2run_all_std.append([])

            run2fin_all_avg.append([])
            run2fin_all_std.append([])

            for t in task_counts:
                for l in task_lengths:
                    result = results[(h,s,c,t,l)]
                    #self.sub2run = sum( [x['ts_running'] - x['ts_submitted'] for x in self.task_repo.values()], datetime.timedelta())
                    #print 'host:%s,stages:%d,cores:%s,tasks:%d,length:%d = ' % (h,s,c,t,l),

                    makespan_avg = numpy.average([x[0].total_seconds() for x in result])
                    makespan_std = numpy.std([x[0].total_seconds() for x in result])

                    ting2ted_avg = numpy.average([x[1].total_seconds() for x in result])
                    ting2ted_std = numpy.std([x[1].total_seconds() for x in result])

                    ting2ted_all_avg[core_counts.index(c)].append(ting2ted_avg)
                    ting2ted_all_std[core_counts.index(c)].append(ting2ted_std)

                    sub2run_avg = numpy.average([x[2].total_seconds() for x in result])
                    sub2run_std = numpy.std([x[2].total_seconds() for x in result])

                    sub2run_all_avg[core_counts.index(c)].append(sub2run_avg)
                    sub2run_all_std[core_counts.index(c)].append(sub2run_std)

                    run2fin_avg = numpy.average([x[3].total_seconds() for x in result])
                    run2fin_std = numpy.std([x[3].total_seconds() for x in result])

                    run2fin_all_avg[core_counts.index(c)].append(run2fin_avg)
                    run2fin_all_std[core_counts.index(c)].append(run2fin_std)

                    print 'makespan:%f(%f), sub:%f(%f), sub2run:%f(%f), run2fin:%f(%f)' % \
                          (makespan_avg, makespan_std, ting2ted_avg, ting2ted_std, \
                           sub2run_avg, sub2run_std, run2fin_avg, run2fin_std)


x = range(len(task_counts))
#x = task_counts
print 'x: %s' % x

print 'ting2ted_all_avg: %s' % ting2ted_all_avg
print 'sub2run_all_avg: %s' % sub2run_all_avg
print 'run2fin_all_avg: %s' % run2fin_all_avg

p = []
c = core_counts.index(8)

width = 0.8

p = []

#xloc = [xx+width*c for xx in x]
xloc = x
p.append(plt.bar(xloc, ting2ted_all_avg[c], width=width, color='blue', align='center'))
p.append(plt.bar(xloc, sub2run_all_avg[c], bottom=ting2ted_all_avg[c], width=width, color='red', align='center'))
p.append(plt.bar(xloc, run2fin_all_avg[c], bottom=sub2run_all_avg[c], width=width, color='green', align='center'))

plt.legend(p, reversed(['Submitting - Submitted', 'Submitted - Running', 'Running - Finished']), title='Phase', loc=2)

plt.xlabel('Number of tasks (pipelines)')
plt.ylabel('Cumulative time spend (seconds)')
plt.title('Cumulative time spent on MTMS execution on single pilot with varying number of (parallel) tasks.\n'\
          'Execution on localhost with mongodb on localhost too.\n' \
          'Number of stages is fixed at 8 and core count fixed at 8. Zero second payload.'
        )
plt.xticks(x, task_counts)
plt.show()
