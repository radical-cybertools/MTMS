import sys
import os
from string import Template

import bigjobasync

glob_num_stages = None
glob_task_executable = None
glob_task_arguments = None

# ----------------------------------------------------------------------------
#
def resource_cb(origin, old_state, new_state):
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
def task_cb(origin, old_state, new_state):
    """Task callback function: writes task state changes to STDERR
"""
    msg = " * Task %s state changed from '%s' to '%s'.\n" % \
          (str(origin), old_state, new_state)
    sys.stderr.write(msg)

    if new_state == bigjobasync.FAILED:
        # Print the log entry if task has failed to run
        for entry in origin.log:
            print " LOG: %s" % entry






def execute_wf(
        # Resource configuration
        resource=None,
        # Task execution description
        task_executable=None,
        task_arguments=None,
        # Task "shape" definition
        tasks=None,
        num_stages=1,
        # Task I/O specification in the form of { 'label': 'pattern' }
        input_per_task_first_stage={},
        input_all_tasks_per_stage={},
        input_per_task_all_stages={},
        output_per_task_per_stage={},
        intermediate_output_per_task_per_stage=[], # in the form of [{input_label, output_label, pattern}]
        output_per_task_final_stage={}):

    global glob_num_stages, glob_task_executable, glob_task_arguments, glob_input_per_task_first_stage,\
        glob_input_all_tasks_per_stage, glob_input_per_task_all_stages, glob_output_per_task_per_stage,\
        glob_intermediate_output_per_task_per_stage, glob_output_per_task_final_stage

    glob_num_stages= num_stages
    glob_task_executable = task_executable
    glob_task_arguments = task_arguments
    glob_input_per_task_first_stage =  input_per_task_first_stage
    glob_input_all_tasks_per_stage =  input_all_tasks_per_stage
    glob_input_per_task_all_stages = input_per_task_all_stages
    glob_output_per_task_per_stage = output_per_task_per_stage
    glob_intermediate_output_per_task_per_stage = intermediate_output_per_task_per_stage
    glob_output_per_task_final_stage = output_per_task_final_stage

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
    resource.register_callbacks(resource_cb)
    # If terminate_on_empty_queue=True, the resource will be shut down as soon
    # as the last task has finished.
    resource.allocate(terminate_on_empty_queue=True)

    stage0_tasks = []
    stage = 0

    for task in tasks:
        print '\n##### Performing initial stage for task %s' % task

        mtms_task = construct_bja_task(task, stage)

        # Register a callback function with each task. This function will get
        # called every time the task changes its state.
        mtms_task.register_callbacks(task_cb)

        # Put it on the list of initial tasks to execute
        stage0_tasks.append(mtms_task)

    # Submit all tasks to the resource
    resource.schedule_tasks(stage0_tasks)

    # Wait for the execution of the workflow
    resource.wait()


def construct_bja_task(task=None, stage=None):

    print '### Constructing BJA task for task %s stage %s' % (task, stage)

    # The __TASK__ and __STAGE__ substitutions are arguably not
    # required from an application perspective, # but are
    # certainly useful for development/debugging purposes.
    task_substitutions = {'__TASK__': task, '__STAGE__': stage}

    for label, pattern in glob_input_per_task_first_stage.items():
        tmp = Template(pattern)
        filename = tmp.substitute(TASK=task, STAGE=stage)
        print '### Using initial input file %s as %s' % (filename, label)
        task_substitutions[label] = filename

    for label, pattern in glob_input_all_tasks_per_stage.items():
        tmp = Template(pattern)
        filename = tmp.substitute(TASK=task, STAGE=stage)
        print '### Using all task per stage input file %s as %s' % (filename, label)
        task_substitutions[label] = filename

    if stage != glob_num_stages-1:
        for entry in glob_intermediate_output_per_task_per_stage:
            tmp = Template(entry['pattern'])
            filename = tmp.substitute(TASK=task, STAGE=stage-1)
            label = entry['input_label']
            print '### Using intermediate per task per stage input file %s as %s' % (filename, label)
            task_substitutions[label] = filename

    for label, pattern in glob_input_per_task_all_stages.items():
        tmp = Template(pattern)
        filename = tmp.substitute(TASK=task, STAGE=stage)
        print '### Using per task all stage input file %s as %s' % (filename, label)
        task_substitutions[label] = filename

    for label, pattern in glob_output_per_task_per_stage.items():
        tmp = Template(pattern)
        filename = tmp.substitute(TASK=task, STAGE=stage)
        print '### Using per task per stage ouput file %s as %s' % (filename, label)
        task_substitutions[label] = filename

    if stage != glob_num_stages-1: # If not the latest stage
        for entry in glob_intermediate_output_per_task_per_stage:
            tmp = Template(entry['pattern'])
            filename = tmp.substitute(TASK=task, STAGE=stage)
            label = entry['output_label']
            print '### Using intermediate per task per stage output file %s as %s' % (filename, label)
            task_substitutions[label] = filename

    if stage == glob_num_stages-1: # If this is the (first and) last step
        for label, pattern in glob_output_per_task_final_stage.items():
            tmp = Template(pattern)
            filename = tmp.substitute(TASK=task, STAGE=stage)
            print '### Using per task final stage output file %s as %s' % (filename, label)
            task_substitutions[label] = filename

    if glob_task_executable:
        if not glob_task_arguments:
            print '### Will execute "%s"' % glob_task_executable
            arguments = None
        else:
            tmp = Template(glob_task_arguments)
            arguments = tmp.substitute(task_substitutions)
            print '### Will execute "%s %s"' % (glob_task_executable, arguments)
    else:
        print '### ERROR: Executable not specified!!'

    #
    # The meaning of the arguments are as follows:
    #
    # * name: a name for easier identification in the task's executable environment
    # * executable: the executable represented by the task
    # * arguments: a list of arguments passed to the executable
    # * environment: a dictionary of environment variables to set
    # * input: a list of input file transfer directives (dicts)
    # * output: a list of output file transfer directives (dicts)
    # * cores: the number of cores required by this task (the default is 1)

    # Name
    bja_name = "mtms-task-%s-%s" % (task, stage)

    # Executable
    bja_executable = glob_task_executable

    # Arguments
    if arguments:
        bja_arguments = arguments
    else:
        bja_arguments = []

    # Environment
    bja_environment = {}

    # Input
    bja_input = []

    # Output
    bja_output = []

    # Cores
    bja_cores = 1

    mtms_task = bigjobasync.Task(
        name = bja_name,
        executable = bja_executable,
        arguments = bja_arguments,
        environment=bja_environment,
        input = bja_input,
        output = bja_output,
        cores = bja_cores
    )

    return mtms_task

def emulate_wf(
            # Task execution description
            task_executable=None,
            task_arguments=None,
            # Task "shape" definition
            tasks=None,
            num_stages=1,
            # Task I/O specification in the form of { 'label': 'pattern' }
            input_per_task_first_stage={},
            input_all_tasks_per_stage={},
            input_per_task_all_stages={},
            output_per_task_per_stage={},
            intermediate_output_per_task_per_stage=[], # in the form of [{input_label, output_label, pattern}]
            output_per_task_final_stage={}):

    global glob_num_stages, glob_task_executable, glob_task_arguments
    glob_num_stages= num_stages
    glob_task_executable = task_executable
    glob_task_arguments = task_arguments

    for t in tasks:
        for s in range(num_stages):
            print '\n##### Performing stage %s for task %s' % (s, t)

            # The __TASK__ and __STAGE__ substitutions are arguably not
            # required from an application perspective, # but are
            # certainly useful for development/debugging purposes.
            task_substitutions = {'__TASK__': t, '__STAGE__': s}

            # Input
            if s == 0:
                for label, pattern in input_per_task_first_stage.items():
                    tmp = Template(pattern)
                    filename = tmp.substitute(TASK=t, STAGE=s)
                    print '### Using initial input file %s as %s' % (filename, label)
                    task_substitutions[label] = filename

            for label, pattern in input_all_tasks_per_stage.items():
                tmp = Template(pattern)
                filename = tmp.substitute(TASK=t, STAGE=s)
                print '### Using all task per stage input file %s as %s' % (filename, label)
                task_substitutions[label] = filename

            if s != 0:
                for entry in intermediate_output_per_task_per_stage:
                    tmp = Template(entry['pattern'])
                    filename = tmp.substitute(TASK=t, STAGE=s-1)
                    label = entry['input_label']
                    print '### Using intermediate per task per stage input file %s as %s' % (filename, label)
                    task_substitutions[label] = filename

            for label, pattern in input_per_task_all_stages.items():
                tmp = Template(pattern)
                filename = tmp.substitute(TASK=t, STAGE=s)
                print '### Using per task all stage input file %s as %s' % (filename, label)
                task_substitutions[label] = filename

            for label, pattern in output_per_task_per_stage.items():
                tmp = Template(pattern)
                filename = tmp.substitute(TASK=t, STAGE=s)
                print '### Using per task per stage ouput file %s as %s' % (filename, label)
                task_substitutions[label] = filename

            if s != num_stages-1:
                for entry in intermediate_output_per_task_per_stage:
                    tmp = Template(entry['pattern'])
                    filename = tmp.substitute(TASK=t, STAGE=s)
                    label = entry['output_label']
                    print '### Using intermediate per task per stage output file %s as %s' % (filename, label)
                    task_substitutions[label] = filename

            if s == num_stages-1:
                for label, pattern in output_per_task_final_stage.items():
                    tmp = Template(pattern)
                    filename = tmp.substitute(TASK=t, STAGE=s)
                    print '### Using per task final stage output file %s as %s' % (filename, label)
                    task_substitutions[label] = filename

            if task_executable:
                if not glob_task_arguments:
                    print '### Will execute "%s"' % task_executable
                else:
                    tmp = Template(glob_task_arguments)
                    arguments = tmp.substitute(task_substitutions)
                    print '### Will execute "%s %s"' % (task_executable, arguments)
            else:
                print '### ERROR: Executable not specified!!'

