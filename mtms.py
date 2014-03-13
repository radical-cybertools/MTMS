import sys
import os
from string import Template

import sagapilot

glob_num_stages = None
glob_task_executable = None
glob_task_arguments = None


# DBURL points to a MongoDB server. For installation of a MongoDB server, please
# refer to the MongoDB website: http://docs.mongodb.org/manual/installation/
DBURL  = "mongodb://ec2-184-72-89-141.compute-1.amazonaws.com:27017"

task_repo = {}

def pilot_state_change_cb(pilot, state):
    """pilot_state_change_cb is a callback function. It handles ComputePilot
    state changes.
    """
    print "[Callback]: ComputePilot '{0}' state changed to {1}.".format(pilot, state)

def unit_state_change_cb(unit, state):
    """ Callback for units.
    """
    print "[Callback]: Unit '{0}' state changed to {1}.".format(unit, state)

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

    global task_repo

    glob_num_stages= num_stages
    glob_task_executable = task_executable
    glob_task_arguments = task_arguments
    glob_input_per_task_first_stage =  input_per_task_first_stage
    glob_input_all_tasks_per_stage =  input_all_tasks_per_stage
    glob_input_per_task_all_stages = input_per_task_all_stages
    glob_output_per_task_per_stage = output_per_task_per_stage
    glob_intermediate_output_per_task_per_stage = intermediate_output_per_task_per_stage
    glob_output_per_task_final_stage = output_per_task_final_stage


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
    pdesc.cores     = 2

    # Launch the pilot.
    pilot = pmgr.submit_pilots(pdesc)
    print "Pilot UID        : {0} ".format( pilot.uid )

    # Register callbacks for pilot state changes
    #pilot.register_state_callback(pilot_state_change_cb)
    pmgr.register_callback(pilot_state_change_cb)

    # Combine the ComputePilot, the workload and a scheduler via # a UnitManager object.
    umgr = sagapilot.UnitManager( session=session, scheduler=sagapilot.SCHED_DIRECT_SUBMISSION)
    print "UnitManager UID  : {0} ".format( umgr.uid )

    # Register callbacks for unit state changes
    umgr.register_callback(unit_state_change_cb)

     # Add the previsouly created ComputePilot to the UnitManager.
    umgr.add_pilots(pilot)

    stage0_cus = []
    stage = 0

    for task in tasks:
        print '\n##### Performing initial stage for task %s' % task

        mtms_task = construct_cud(task, stage)

        #mtms_task.register_callback(unit_state_change_cb)

        # Put it on the list of initial tasks to execute
        stage0_cus.append(mtms_task)

        task_repo[mtms_task.name] = {'task': mtms_task, 'stage': stage}
        print 'task repo inside execute_wf:', task_repo

    # Submit the previously created ComputeUnit descriptions to the
    # PilotManager. This will trigger the selected scheduler to start
    # assigning ComputeUnits to the ComputePilots.
    umgr.submit_units(stage0_cus)

    # Wait for all compute units to finish.
    umgr.wait_units()

    for unit in umgr.get_units():
        # Print some information about the unit.
        print "{0}".format(str(unit))

        # Get the stdout and stderr streams of the ComputeUnit.
        print "  STDOUT: {0}".format(unit.stdout)
        print "  STDERR: {0}".format(unit.stderr)

    # Cancel all pilots.
    pmgr.cancel_pilots()

    # Remove session from database
    session.destroy()

#########################################
#
# Create a Compute Unit Description
#
def construct_cud(task=None, stage=None):

    print '### Constructing CUD for task %s stage %s' % (task, stage)
    cu = sagapilot.ComputeUnitDescription()

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


    # Name
    cu.name = "mtms-task-%s-%s" % (task, stage)

    # Executable
    cu.executable = glob_task_executable

    # Arguments
    if arguments:
        cu.arguments = arguments

    # Environment
    #cu.environment =  {}

    # Input
    #cu.input_data  = [ "./file1.dat   > file1.dat",
    #                "./file2.dat   > file2.dat" ]
    #input = bja_input

    # Output
    #cu.output_data = [ "result-%s.dat < STDOUT" % unit_count]
    #output = bja_output,

    # Cores
    cu.cores  =  1

    return cu
