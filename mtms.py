import sys
import os
from string import Template

import bigjobasync


class MultiTaskMultiStage():

    # ----------------------------------------------------------------------------
    #
    def resource_cb(self, origin, old_state, new_state):
        """Resource callback function: writes resource allocation state
    changes to STDERR.

    It aborts the script script with exit code '-1' if the resource
    allocation state is 'FAILED'.

    (Obviously, more logic can be built into the callback function, for
    example fault tolerance.)
    """
        msg = " * Resource '%s' state changed from '%s' to '%s'.\n" % \
              (str(origin), old_state, new_state)
        sys.stderr.write(msg)

        if new_state == bigjobasync.FAILED:
            # Print the log and exit if big job has failed
            for entry in origin.log:
                print " * LOG: %s" % entry
            sys.stderr.write(" * EXITING.\n")
            sys.exit(-1)

    # ----------------------------------------------------------------------------
    #
    def task_cb(self, origin, old_state, new_state):
        """Task callback function: writes task state changes to STDERR
    """
        msg = " * Task %s state changed from '%s' to '%s'.\n" % \
              (str(origin), old_state, new_state)
        sys.stderr.write(msg)

        if new_state == bigjobasync.FAILED:
            # Print the log entry if task has failed to run
            for entry in origin.log:
                print " LOG: %s" % entry

    def __init__(self, resource):

        self.tasks = []
        self.stages = []

        self.task_executable = None
        self.task_arguments = None

        # In the form of { 'label': 'pattern' }
        self.input_per_task_first_stage = {}
        self.input_all_tasks_per_stage = {}
        self.input_per_task_all_stages = {}
        self.output_per_task_per_stage = {}
        self.intermediate_output_per_task_per_stage = []
        self.output_per_task_final_stage = {}

        # Register a callback function with the resource allocation. This function
        # will get called every time the big job changes its state. Possible states
        # of a resource allocation are:
        #
        # * NEW (just created)
        # * PENDING (pilot waiting to get scheduled by the system)
        # * RUNNING (pilot executing on the resource)
        # * DONE (pilot successfully finished execution)
        # * FAILED (an error occurred during pilot execution)
        #
        resource.register_callbacks(self.resource_cb)
        # If terminate_on_empty_queue=True, the resource will be shut down as soon
        # as the last task has finished.
        resource.allocate(terminate_on_empty_queue=True)

    def execute(self):

        for t in self.tasks:
                print '\n##### Performing initial stage for task %s' % t

                # Input
                for f in self.input_per_task_first_stage:
                    tmp = Template(f)
                    f = tmp.substitute(TASK=t, STAGE=0)
                    print '### Using initial input file %s' % f

                for f in self.input_all_tasks_per_stage:
                    tmp = Template(f)
                    f = tmp.substitute(TASK=t, STAGE=0)
                    print '### Using input all task per stage file %s' % f

                for f in self.input_per_task_all_stages:
                    tmp = Template(f)
                    f = tmp.substitute(TASK=t, STAGE=0)
                    print '### Using input per task all stage file %s' % f

                def construct_task():
                    print '### Will execute %s' % self.task_executable

                    # A 'combinator' tasks takes two input files and appends one to the
                    # other. The first input file 'loreipsum_pt1.txt' is copied from the
                    # local machine to the executing cluster. The second file is already
                    # one the remote cluster and is copied locally into the task's
                    # working directory. The resulting output file is copied back to the
                    # local machine. The meaning of the arguments are as follows:
                    #
                    # * name a name for easier identification
                    # * cores the number of cores required by this task
                    # (the default is 1)
                    # * environment a dictionary of environment variables to set
                    # in the task's executable environment
                    # * executable the executable represented by the task
                    # * arguments a list of arguments passed to the executable
                    # * input a list of input file transfer directives (dicts)
                    # * output a list of output file transfer directives (dicts)
                    #
                    mtms_task = bigjobasync.Task(
                        name = "mtms-task-%s" % i,
                        cores = 1,
                        executable = os.path.join(WD_PREFIX, 'mtmswf', 'namd-mockup.sh'),
                        arguments = [
                            # general
                            chr,
                            loc,
                            stage,
                            # i_conf_du
                            os.path.basename(i_conf),
                            # i_param_du
                            os.path.basename(i_pdb),
                            os.path.basename(i_crd),
                            os.path.basename(i_parm),
                            # i_stage_du
                            os.path.basename(i_coor),
                            os.path.basename(i_vel),
                            os.path.basename(i_xsc),
                            # o_stage_du
                            os.path.basename(o_coor),
                            os.path.basename(o_vel),
                            os.path.basename(o_xsc),
                            # o_log_du
                            os.path.basename(o_out),
                            os.path.basename(o_err),
                            # o_ana_du
                            os.path.basename(o_dcd),
                            os.path.basename(o_cvd),
                            os.path.basename(o_xst)
                            ],
                        # transfer input files from the local machine (i.e., the machine
                        # where this script runs) into the task's workspace on the
                        # remote machine.
                        input = [
                            {
                                "mode" : bigjobasync.COPY,
                                "origin" : bigjobasync.LOCAL,
                                "origin_path" : "/%s/loreipsum_pt1.txt" % os.getcwd(),
                            },
                            {
                                "mode" : bigjobasync.COPY,
                                "origin" : bigjobasync.LOCAL,
                                "origin_path" : "/%s/loreipsum_pt2.txt" % os.getcwd(),
                            }
                        ],
                        output = [
                            {
                                # transfer the task's output file ('STDOUT') back to the local machine
                                # (i.e., the machine where this script runs).
                                "mode" : bigjobasync.COPY,
                                "origin_path" : "loreipsum-complete-%s.txt" % i,
                                "destination" : bigjobasync.LOCAL,
                                "destination_path" : "."
                            }
                        ]
                    )

                      # Register a callback function with each task. This function will get
        # called everytime the task changes its state. Possible states of a
        # task are:
        #
        # * NEW (task just created)
        # * TRANSFERRING_INPUT (task transferring input data)
        # * WAITING_FOR_EXECUTION (task waiting to get submitted)
        # * PENDING (task submitted, waiting to get executed)
        # * RUNNING (task executing on the resource)
        # * TRANSFERRING_OUTPUT (task transferring output data)
        # * DONE (task successfully finished execution)
        # * FAILED (error during transfer or execution)
        #

        #combinator_task.register_callbacks(self.task_cb)
        #all_tasks.append(combinator_task)

        # Submit all tasks to stampede
        #stampede.schedule_tasks(all_tasks)

                for f in self.output_per_task_per_stage:
                    tmp = Template(f)
                    f = tmp.substitute(TASK=t, STAGE=s)
                    print '### Using output per task per stage file %s' % f

                if s != self.stages[-1]:
                    for f in self.intermediate_output_per_task_per_stage:
                        tmp = Template(f)
                        f = tmp.substitute(TASK=t, STAGE=s)
                        print '### Using intermediate output per task per stage file %s' % f

                if s == self.stages[-1]:
                    for f in self.output_per_task_final_stage:
                        tmp = Template(f)
                        f = tmp.substitute(TASK=t, STAGE=s)
                        print '### Using output per task final stage file %s' % f

        # For intermediate stages
        #if s != self.stages[0]:
        #    for f in self.intermediate_per_task_per_stage:
        #        tmp = Template(f)
        #        f = tmp.substitute(TASK=t, STAGE=s-1)
        #        print '### Reading intermediate per task per stage file %s' % f

    def emulate(self):

        for t in self.tasks:
            for s in self.stages:
                print '\n##### Performing stage %s for task %s' % (s, t)

                # The __TASK__ and __STAGE__ substitutions are arguably not
                # required from an application perspective, # but are
                # certainly useful for development/debugging purposes.
                task_substitutions = {'__TASK__': t, '__STAGE__': s}

                # Input
                if s == self.stages[0]:
                    for label, pattern in self.input_per_task_first_stage.items():
                        tmp = Template(pattern)
                        filename = tmp.substitute(TASK=t, STAGE=s)
                        print '### Using initial input file %s as %s' % (filename, label)
                        task_substitutions[label] = filename

                for label, pattern in self.input_all_tasks_per_stage.items():
                    tmp = Template(pattern)
                    filename = tmp.substitute(TASK=t, STAGE=s)
                    print '### Using all task per stage input file %s as %s' % (filename, label)
                    task_substitutions[label] = filename

                if s != self.stages[0]:
                    for entry in self.intermediate_output_per_task_per_stage:
                        tmp = Template(entry['pattern'])
                        filename = tmp.substitute(TASK=t, STAGE=s-1)
                        label = entry['input_label']
                        print '### Using intermediate per task per stage input file %s as %s' % (filename, label)
                        task_substitutions[label] = filename

                for label, pattern in self.input_per_task_all_stages.items():
                    tmp = Template(pattern)
                    filename = tmp.substitute(TASK=t, STAGE=s)
                    print '### Using per task all stage input file %s as %s' % (filename, label)
                    task_substitutions[label] = filename

                for label, pattern in self.output_per_task_per_stage.items():
                    tmp = Template(pattern)
                    filename = tmp.substitute(TASK=t, STAGE=s)
                    print '### Using per task per stage ouput file %s as %s' % (filename, label)
                    task_substitutions[label] = filename

                if s != self.stages[-1]:
                    for entry in self.intermediate_output_per_task_per_stage:
                        tmp = Template(entry['pattern'])
                        filename = tmp.substitute(TASK=t, STAGE=s)
                        label = entry['output_label']
                        print '### Using intermediate per task per stage output file %s as %s' % (filename, label)
                        task_substitutions[label] = filename

                if s == self.stages[-1]:
                    for label, pattern in self.output_per_task_final_stage.items():
                        tmp = Template(pattern)
                        filename = tmp.substitute(TASK=t, STAGE=s)
                        print '### Using per task final stage output file %s as %s' % (filename, label)
                        task_substitutions[label] = filename

                if self.task_executable:
                    if not self.task_arguments:
                        print '### Will execute "%s"' % self.task_executable
                    else:
                        tmp = Template(self.task_arguments)
                        arguments = tmp.substitute(task_substitutions)
                        print '### Will execute "%s %s"' % (self.task_executable, arguments)
                else:
                    print '### ERROR: Executable not specified!!'

