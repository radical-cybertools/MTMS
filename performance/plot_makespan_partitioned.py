import datetime
from results import results
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
c = 8
p_sub = plt.bar(x,ting2ted_all_avg[core_counts.index(c)], width=0.8, color='blue', align='center')
p_run = plt.bar(x,sub2run_all_avg[core_counts.index(c)], bottom=ting2ted_all_avg[core_counts.index(c)], width=0.8, color='red', align='center')
p_fin = plt.bar(x,run2fin_all_avg[core_counts.index(c)], bottom=sub2run_all_avg[core_counts.index(c)], width=0.8, color='green', align='center')

plt.legend(reversed([p_sub, p_run, p_fin]), reversed(['Submitting - Submitted', 'Submitted - Running', 'Running - Finished']), title='Pilot core count', loc=2)

plt.xlabel('Number of tasks (pipelines)')
plt.ylabel('Cumulative time spend (seconds)')
plt.title('Makespan of MTMS execution on single pilot with varying number of (parallel) tasks and pilot sizes.\n'\
          'Execution on localhost with mongodb on localhost too.\n' \
          'Number of stages is fixed at 8. Zero second payload.'
        )
plt.xticks(x, task_counts)
plt.show()
