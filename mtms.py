import sys
import os
from string import Template


import datetime

import sagapilot

verbose = False

# DBURL points to a MongoDB server. For installation of a MongoDB server, please
# refer to the MongoDB website: http://docs.mongodb.org/manual/installation/
#DBURL  = "mongodb://ec2-184-72-89-141.compute-1.amazonaws.com:27017"
DBURL  = "mongodb://localhost:27017"

glob_task_repo = {}
glob_umgr = None
glob_io_desc = None
glob_task_desc = None
glob_tasks_complete = 0

start = None

def log(msg):
    now = datetime.datetime.now()
    cum = now - start
    print '### %s ### %s' % (cum, msg)


class Task_Description():
    def __init__(self):

        # Task execution description
        self.executable = None
        self.arguments = None
        self.num_cores = 1
        self.environment = {}

        # Task "shape" definition
        self.tasks = None # List of elements / TODO: NEED A BETTER NAME!!
        self.num_stages = 1

class IO_Description():
    def __init__(self):
        # Task I/O specification in the form of { 'label': 'pattern' }
        self.input_per_task_first_stage={}
        self.input_all_tasks_per_stage={}
        self.input_per_task_all_stages={}

        self.output_per_task_per_stage={}
        self.output_per_task_final_stage={}

        # Intermediate in the form of [{input_label, output_label, pattern}]
        self.intermediate_output_per_task_per_stage=[]

def pilot_state_change_cb(pilot, state):
    """pilot_state_change_cb is a callback function. It handles ComputePilot
    state changes.
    """
    print "[Callback]: ComputePilot '{0}' state changed to {1}.".format(pilot.uid, state)

def unit_state_change_cb(unit, state):
    """ Callback for units.
    """
    #print "[Callback]: Unit '{0}' state changed to {1}.".format(unit.uid, state)

    determine_next_step(unit.uid, state)



def determine_next_step(cu_uid, state):
    entry = glob_task_repo[cu_uid]
    task_name = entry['desc'].name
    task = entry['task']
    stage = entry['stage']

    if state == sagapilot.states.DONE:
        log('Task %s is finished.' % task_name)
        glob_task_repo[cu_uid]['ts_done'] = datetime.datetime.now()

        #cu = glob_umgr.get_units(cu_uid)[0]
        #print 'cu:', cu
        # # print 'Details: ', cu.execution_details()
        #print 'Log:', cu.log

        if stage == glob_task_desc.num_stages - 1:
            log('Last stage (%d) reached for task %s ...' % (stage, task_name))
            global glob_tasks_complete
            glob_tasks_complete += 1
        else:
            next_stage = int(stage) + 1
            log('Launching task %s next stage: %d' % (task, next_stage))
            launch_task(task, next_stage, glob_task_desc, glob_io_desc)

    elif state == sagapilot.states.RUNNING:
        log('Task %s started running.' % task_name)
        glob_task_repo[cu_uid]['ts_running'] = datetime.datetime.now()

    elif state == sagapilot.states.FAILED:
        log('Task %s is failed.' % task_name)

    elif state == sagapilot.states.PENDING or \
         state == sagapilot.states.PENDING_EXECUTION or \
         state == sagapilot.states.PENDING_INPUT_TRANSFER or \
         state == sagapilot.states.PENDING_OUTPUT_TRANSFER:

        log('Task %s is %s.' % (task_name, state))

    else:
        print 'ERROR: uncatched state: %s' % state


def launch_initial_tasks(task_desc, io_desc):
    stage = 0
    for task in task_desc.tasks:
        log('Performing initial stage for task %s' % task)
        launch_task(task, stage, task_desc, io_desc)


def launch_task(task, stage, task_desc, io_desc):

    mtms_cud = construct_cud(task, stage, task_desc, io_desc)

    # Submit the previously created ComputeUnit descriptions to the
    # PilotManager. This will trigger the selected scheduler to start
    # assigning ComputeUnits to the ComputePilots.
    log('Submitting task %s stage %d' % (task, stage))
    ting = datetime.datetime.now()
    cu = glob_umgr.submit_units(mtms_cud)
    ted = datetime.datetime.now()
    log('Submitted task %s stage %d' % (task, stage))

    # Add to repo
    glob_task_repo[cu.uid] = {'task': task, 'stage': stage, 'desc': mtms_cud}

    glob_task_repo[cu.uid]['ts_submitting'] = ting
    glob_task_repo[cu.uid]['ts_submitted'] = ted



def execute_wf(resource_desc, task_desc, io_desc):


    global glob_io_desc
    glob_io_desc = io_desc
    global glob_task_desc
    glob_task_desc = task_desc

    # Create a new session. A session is a set of Pilot Managers
    # and Unit Managers (with associated Pilots and ComputeUnits).
    session = sagapilot.Session(database_url=DBURL)
    print "Session UID      : {0} ".format(session.uid)

    # Add a Pilot Manager
    pmgr = sagapilot.PilotManager(session=session)
    print "PilotManager UID : {0} ".format( pmgr.uid )

    # Define a 2-core local pilot in /tmp/sagapilot.sandbox that runs  for 10 minutes.
    pdesc = sagapilot.ComputePilotDescription()
    pdesc.resource  = "localhost"
    pdesc.runtime   = 15 # minutes
    pdesc.cores     = 8

    # Launch the pilot.
    pilot = pmgr.submit_pilots(pdesc)
    print "Pilot UID        : {0} ".format( pilot.uid )

    # Register callbacks for pilot state changes
    pmgr.register_callback(pilot_state_change_cb)

    # Combine the ComputePilot, the workload and a scheduler via # a UnitManager object.
    global glob_umgr
    glob_umgr = sagapilot.UnitManager( session=session, scheduler=sagapilot.SCHED_DIRECT_SUBMISSION)
    print "UnitManager UID  : {0} ".format(glob_umgr.uid)

    # Register callbacks for unit state changes
    glob_umgr.register_callback(unit_state_change_cb)

     # Add the previously created ComputePilot to the UnitManager.
    glob_umgr.add_pilots(pilot)

    pmgr.wait_pilots(pilot_ids=None, state=sagapilot.states.RUNNING)
    global start
    start = datetime.datetime.now()
    launch_initial_tasks(task_desc, io_desc)

    # TODO: Need a better estimate for when its "done"
    # Wait for all compute units to finish.
    while glob_tasks_complete < len(glob_task_desc.tasks):
        glob_umgr.wait_units()

    # Cancel all pilots.
    pmgr.cancel_pilots()

    # Remove session from database
    session.destroy()

    ting2ted = sum( [x['ts_submitted'] - x['ts_submitting'] for x in glob_task_repo.values()], datetime.timedelta())
    sub2run = sum( [x['ts_running'] - x['ts_submitted'] for x in glob_task_repo.values()], datetime.timedelta())
    run2fin = sum( [x['ts_done'] - x['ts_running'] for x in glob_task_repo.values()], datetime.timedelta())
    print 'Cumulative time between submission and submitted: %s' % ting2ted
    print 'Cumulative time between submitted and running: %s' % sub2run
    print 'Cumulative time between running and finished: %s' % run2fin

#########################################
#
# Create a Compute Unit Description
#
def construct_cud(task, stage, task_desc, io_desc):

    log('Constructing CUD for task %s stage %s' % (task, stage))
    cud = sagapilot.ComputeUnitDescription()

    # The __TASK__ and __STAGE__ substitutions are arguably not
    # required from an application perspective, # but are
    # certainly useful for development/debugging purposes.
    task_substitutions = {'__TASK__': task, '__STAGE__': stage}

    for label, pattern in io_desc.input_per_task_first_stage.items():
        tmp = Template(pattern)
        filename = tmp.substitute(TASK=task, STAGE=stage)
        if verbose:
            print '### Using initial input file %s as %s' % (filename, label)
        task_substitutions[label] = filename

    for label, pattern in io_desc.input_all_tasks_per_stage.items():
        tmp = Template(pattern)
        filename = tmp.substitute(TASK=task, STAGE=stage)
        if verbose:
            print '### Using all task per stage input file %s as %s' % (filename, label)
        task_substitutions[label] = filename

    if stage != task_desc.num_stages-1:
        for entry in io_desc.intermediate_output_per_task_per_stage:
            tmp = Template(entry['pattern'])
            filename = tmp.substitute(TASK=task, STAGE=stage-1)
            label = entry['input_label']
            if verbose:
                print '### Using intermediate per task per stage input file %s as %s' % (filename, label)
            task_substitutions[label] = filename

    for label, pattern in io_desc.input_per_task_all_stages.items():
        tmp = Template(pattern)
        filename = tmp.substitute(TASK=task, STAGE=stage)
        if verbose:
            print '### Using per task all stage input file %s as %s' % (filename, label)
        task_substitutions[label] = filename

    for label, pattern in io_desc.output_per_task_per_stage.items():
        tmp = Template(pattern)
        filename = tmp.substitute(TASK=task, STAGE=stage)
        if verbose:
            print '### Using per task per stage output file %s as %s' % (filename, label)
        task_substitutions[label] = filename

    if stage != task_desc.num_stages-1: # If not the latest stage
        for entry in io_desc.intermediate_output_per_task_per_stage:
            tmp = Template(entry['pattern'])
            filename = tmp.substitute(TASK=task, STAGE=stage)
            label = entry['output_label']
            if verbose:
                print '### Using intermediate per task per stage output file %s as %s' % (filename, label)
            task_substitutions[label] = filename

    if stage == task_desc.num_stages-1: # If this is the (first and) last step
        for label, pattern in io_desc.output_per_task_final_stage.items():
            tmp = Template(pattern)
            filename = tmp.substitute(TASK=task, STAGE=stage)
            if verbose:
                print '### Using per task final stage output file %s as %s' % (filename, label)
            task_substitutions[label] = filename

    if task_desc.executable:
        if not task_desc.arguments:
            if verbose:
                print '### Will execute "%s"' % task_desc.executable
            arguments = None
        else:
            tmp = Template(task_desc.arguments)
            arguments = tmp.substitute(task_substitutions)
            if verbose:
                print '### Will execute "%s %s"' % (task_desc.executable, arguments)
    else:
        print '### ERROR: Executable not specified!!'


    # Name
    cud.name = "mtms-task-%s-%s" % (task, stage)

    # Executable
    cud.executable = task_desc.executable

    # Arguments
    if arguments:
        cud.arguments = arguments

    # Environment
    cud.environment =  task_desc.environment

    # Input
    #cud.input_data  = [ "./file1.dat   > file1.dat",
    #                "./file2.dat   > file2.dat" ]
    #input = bja_input

    # Output
    #cud.output_data = [ "result-%s.dat < STDOUT" % unit_count]
    #output = bja_output,

    # Cores
    cud.cores  =  task_desc.num_cores

    return cud
