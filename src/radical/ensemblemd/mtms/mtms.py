import sys
import os
from string import Template
import datetime
import radical.pilot as rp
from radical.ensemblemd.mdkernels import MDTaskDescription


class Resource_Description():
    def __init__(self):
        # defaults
        self.resource = "localhost"
        self.project = None
        self.runtime = 42 # minutes
        self.cores = 1
        self.dburl = 'mongodb://ec2-184-72-89-141.compute-1.amazonaws.com:27017'


class Task_Description():
    def __init__(self):

        # Task execution description
        self.kernel = None
        self.arguments = None
        self.cores = 1

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


class Engine(object):

    def __init__(self):
        self.task_repo = {}
        self.tasks_complete = 0

    def pilot_state_change_cb(self, pilot, state):
        """pilot_state_change_cb is a callback function. It handles ComputePilot
        state changes.
        """
        if self.verbose:
            print "[Callback]: ComputePilot '{0}' state changed to {1}.".format(pilot.uid, state)

    def unit_state_change_cb(self, unit, state):
        """ Callback for units.
        """
        #print "[Callback]: Unit '{0}' state changed to {1}.".format(unit.uid, state)

        self.determine_next_step(unit.uid, state)

    def determine_next_step(self, cu_uid, state):

        entry = self.task_repo[cu_uid]
        task_name = entry['desc'].name
        task = entry['task']
        stage = entry['stage']

        if state == rp.states.DONE:
            self.log('Task %s is finished.' % task_name)
            self.task_repo[cu_uid]['ts_done'] = datetime.datetime.now()

            #cu = self.umgr.get_units(cu_uid)[0]
            #print 'cu:', cu
            # # print 'Details: ', cu.execution_details()
            #print 'Log:', cu.log

            if stage == self.task_desc.num_stages:
                self.log('Last stage (%d) reached for task %s ...' % (stage, task_name))
                self.tasks_complete += 1
            else:
                next_stage = int(stage) + 1
                self.log('Launching task %s next stage: %d' % (task, next_stage))
                self.launch_task(task, next_stage)

        elif state == rp.states.EXECUTING:
            self.log('Task %s started running.' % task_name)
            self.task_repo[cu_uid]['ts_running'] = datetime.datetime.now()

        elif state == rp.states.FAILED:
            self.log('Task %s is failed.' % task_name)
            self.log('Not launching next stage for task %s' % task)
            self.tasks_complete += 1

        elif state in [rp.states.NEW,
                       rp.states.PENDING_INPUT_STAGING,
                       rp.states.STAGING_INPUT,
                       rp.states.PENDING_EXECUTION,
                       rp.states.SCHEDULING,
                       rp.states.PENDING_OUTPUT_STAGING,
                       rp.states.STAGING_OUTPUT]:
            self.log('Task %s is %s.' % (task_name, state))

        else:
            print 'ERROR: uncaught state: %s' % state


    def launch_initial_tasks(self):
        stage = 1
        for task in self.task_desc.tasks:
            self.log('Performing initial stage for task %s' % task)
            self.launch_task(task, stage)

    def launch_task(self, task, stage):

        mtms_cud = self.construct_cud(task, stage)

        # Submit the previously created ComputeUnit descriptions to the
        # PilotManager. This will trigger the selected scheduler to start
        # assigning ComputeUnits to the ComputePilots.
        self.log('Submitting task %s stage %d' % (task, stage))
        ting = datetime.datetime.now()
        cu = self.umgr.submit_units(mtms_cud)
        ted = datetime.datetime.now()

        # Add to repo
        self.task_repo[cu.uid] = {
            'task': task,
            'stage': stage,
            'desc': mtms_cud,
            'ts_submitting': ting,
            'ts_submitted': ted
        }

        self.log('Submitted task %s stage %d' % (task, stage))

        # Register the callback for unit state changes
        cu.register_callback(self.unit_state_change_cb)

    def log(self, msg):
        now = datetime.datetime.now()
        cum = now - self.start
        if self.verbose:
            print '### %s ### %s' % (cum, msg)

    def execute(self, resource_desc, task_desc, io_desc, verbose=False, pm_timeout=None):

        self.verbose = verbose

        self.io_desc = io_desc
        self.task_desc = task_desc
        self.resource_desc = resource_desc

        # Create a new session. A session is a set of Pilot Managers
        # and Unit Managers (with associated Pilots and ComputeUnits).
        session = rp.Session(database_url=resource_desc.dburl)
        if self.verbose:
            print "Session UID      : {0} ".format(session.uid)

        # Find remote fs endpoint
        rc = session.get_resource_config(resource_desc.resource)
        self.remote_fs = rp.Url(rc['filesystem_endpoint'])

        # Add a Pilot Manager
        pmgr = rp.PilotManager(session=session)
        if self.verbose:
            print "PilotManager UID : {0} ".format( pmgr.uid )

        pilot_desc = rp.ComputePilotDescription()
        pilot_desc.resource  = resource_desc.resource
        pilot_desc.runtime   = resource_desc.runtime
        pilot_desc.cores     = resource_desc.cores

        if resource_desc.project:
            pilot_desc.project = resource_desc.project

        # Launch the pilot.
        pilot = pmgr.submit_pilots(pilot_desc)
        if self.verbose:
            print "Pilot UID        : {0} ".format( pilot.uid )

        # Register callbacks for pilot state changes
        pmgr.register_callback(self.pilot_state_change_cb)

        # Combine the ComputePilot, the workload and a scheduler via # a UnitManager object.
        self.umgr = rp.UnitManager( session=session, scheduler=rp.SCHED_DIRECT_SUBMISSION)
        if self.verbose:
            print "UnitManager UID  : {0} ".format(self.umgr.uid)

         # Add the previously created ComputePilot to the UnitManager.
        self.umgr.add_pilots(pilot)

        # Wait until the pilots are either running or failed
        pilot_states = pmgr.wait_pilots(pilot_ids=None,
                         state=[rp.states.ACTIVE,
                                rp.states.FAILED,
                                rp.states.CANCELED], timeout=pm_timeout)
        # Check whether there are other states than 'running'
        if list(set(pilot_states)) != [rp.states.ACTIVE]:
            raise Exception('ERROR: Not all pilots are running: %s' % pilot_states)

        # Now that the pilots started, begin the timing
        # TODO: This is useful for experiments, but not necessarily for normal running
        self.start = datetime.datetime.now()
        self.launch_initial_tasks()

        # TODO: Need a better estimate for when its "done"
        # Wait for all compute units to finish.
        while self.tasks_complete < len(self.task_desc.tasks):
            self.umgr.wait_units()
        stop = datetime.datetime.now()

        # Cancel all pilots.
        pmgr.cancel_pilots()

        # Remove session from database
        session.close(delete=False)

        self.ting2ted = sum( [x['ts_submitted'] - x['ts_submitting'] for x in self.task_repo.values()], datetime.timedelta())
        try:
            self.sub2run = sum( [x['ts_running'] - x['ts_submitted'] for x in self.task_repo.values()], datetime.timedelta())
        except KeyError:
            self.sub2run = datetime.timedelta(0)

        try:
            self.run2fin = sum( [x['ts_done'] - x['ts_running'] for x in self.task_repo.values()], datetime.timedelta())
        except KeyError:
            self.run2fin = datetime.timedelta(0)

        self.makespan = stop - self.start

    #########################################
    #
    # Create a Compute Unit Description
    #
    def construct_cud(self, task, stage):

        self.log('Constructing CUD for task %s stage %s' % (task, stage))
        cud = rp.ComputeUnitDescription()

        # Initialize input and output staging as list so that we can later just append.
        # TODO: Could this be an issue if there are no later appends?
        cud.input_staging = []
        cud.output_staging = []

        # The __TASK__ and __STAGE__ substitutions are arguably not
        # required from an application perspective, # but are
        # certainly useful for development/debugging purposes.
        task_substitutions = {'__TASK__': task, '__STAGE__': stage}

        if stage == 1:
            for label, pattern in self.io_desc.input_per_task_first_stage.items():
                tmp = Template(pattern)
                filename = tmp.substitute(TASK=task, STAGE=stage)
                if self.verbose:
                    print '### Using initial input file %s as %s' % (filename, label)
                task_substitutions[label] = os.path.basename(filename)

                url = rp.Url(filename)
                sd = {
                    'source': url.path,
                    'target': os.path.basename(filename)
                }

                if url.host == 'localhost' or url.host is None:
                    sd['action'] = rp.TRANSFER
                elif url.host == self.remote_fs.host:
                    sd['action'] = rp.LINK
                else:
                    print "### ERROR: Host not supported for this pilot!"

                cud.input_staging.append(sd)

        for label, pattern in self.io_desc.input_all_tasks_per_stage.items():
            tmp = Template(pattern)
            filename = tmp.substitute(TASK=task, STAGE=stage)
            if self.verbose:
                print '### Using all task per stage input file %s as %s' % (filename, label)
            task_substitutions[label] = os.path.basename(filename)

            url = rp.Url(filename)
            sd = {
                'source': url.path,
                'target': os.path.basename(filename)
            }

            if url.host == 'localhost' or url.host is None:
                sd['action'] = rp.TRANSFER
            elif url.host == self.remote_fs.host:
                sd['action'] = rp.LINK
            else:
                print "### ERROR: Host not supported for this pilot!"

            cud.input_staging.append(sd)

        if stage != 1:
            for entry in self.io_desc.intermediate_output_per_task_per_stage:
                tmp = Template(entry['pattern'])
                filename = tmp.substitute(TASK=task, STAGE=stage-1)
                label = entry['input_label']
                if self.verbose:
                    print '### Using intermediate per task per stage input file %s as %s' % (filename, label)
                task_substitutions[label] = os.path.basename(filename)

                url = rp.Url(filename)
                sd = {
                    'source': url.path,
                    'target': os.path.basename(filename)
                }

                if url.host == 'localhost' or url.host is None:
                    sd['action'] = rp.TRANSFER
                elif url.host == self.remote_fs.host:
                    sd['action'] = rp.LINK
                else:
                    print "### ERROR: Host not supported for this pilot!"

                cud.input_staging.append(sd)

        for label, pattern in self.io_desc.input_per_task_all_stages.items():
            tmp = Template(pattern)
            filename = tmp.substitute(TASK=task, STAGE=stage)
            if self.verbose:
                print '### Using per task all stage input file %s as %s' % (filename, label)
            task_substitutions[label] = os.path.basename(filename)

            url = rp.Url(filename)
            sd = {
                'source': url.path,
                'target': os.path.basename(filename)
            }

            if url.host == 'localhost' or url.host is None:
                sd['action'] = rp.TRANSFER
            elif url.host == self.remote_fs.host:
                sd['action'] = rp.LINK
            else:
                print "### ERROR: Host not supported for this pilot!"

            cud.input_staging.append(sd)

        for label, pattern in self.io_desc.output_per_task_per_stage.items():
            tmp = Template(pattern)
            filename = tmp.substitute(TASK=task, STAGE=stage)
            if label == 'STDOUT':
                if self.verbose:
                    print '### Using per task per stage STDOUT file as %s' % (filename)

                url = rp.Url(filename)
                sd = {
                    'source': 'STDOUT',
                    'target': url.path
                }

                if url.host == 'localhost' or url.host is None:
                    sd['action'] = rp.TRANSFER
                elif url.host == self.remote_fs.host:
                    sd['action'] = rp.COPY
                else:
                    print "### ERROR: Host not supported for this pilot!"

                cud.output_staging.append(sd)

            elif label == 'STDERR':
                if self.verbose:
                    print '### Using per task per stage STDERR file as %s' % (filename)

                url = rp.Url(filename)
                sd = {
                    'source': 'STDERR',
                    'target': url.path
                }

                if url.host == 'localhost' or url.host is None:
                    sd['action'] = rp.TRANSFER
                elif url.host == self.remote_fs.host:
                    sd['action'] = rp.COPY
                else:
                    print "### ERROR: Host not supported for this pilot!"

                cud.output_staging.append(sd)

            else:
                if self.verbose:
                    print '### Using per task per stage output file %s as %s' % (filename, label)
                basename = os.path.basename(filename)
                task_substitutions[label] = basename

                url = rp.Url(filename)
                sd = {
                    'source': basename,
                    'target': url.path
                }

                if url.host == 'localhost' or url.host is None:
                    sd['action'] = rp.TRANSFER
                elif url.host == self.remote_fs.host:
                    sd['action'] = rp.COPY
                else:
                    print "### ERROR: Host not supported for this pilot!"

                cud.output_staging.append(sd)

        if stage != self.task_desc.num_stages: # If not the latest stage
            for entry in self.io_desc.intermediate_output_per_task_per_stage:
                tmp = Template(entry['pattern'])
                filename = tmp.substitute(TASK=task, STAGE=stage)
                label = entry['output_label']
                if self.verbose:
                    print '### Using intermediate per task per stage output file %s as %s' % (filename, label)
                basename = os.path.basename(filename)
                task_substitutions[label] = basename

                url = rp.Url(filename)
                sd = {
                    'source': basename,
                    'target': url.path
                }

                if url.host == 'localhost' or url.host is None:
                    sd['action'] = rp.TRANSFER
                elif url.host == self.remote_fs.host:
                    sd['action'] = rp.COPY
                else:
                    print "### ERROR: Host not supported for this pilot!"

                cud.output_staging.append(sd)

        if stage == self.task_desc.num_stages: # If this is the last step
            for label, pattern in self.io_desc.output_per_task_final_stage.items():
                tmp = Template(pattern)
                filename = tmp.substitute(TASK=task, STAGE=stage)
                if self.verbose:
                    print '### Using per task final stage output file %s as %s' % (filename, label)
                basename = os.path.basename(filename)
                task_substitutions[label] = basename

                url = rp.Url(filename)
                sd = {
                    'source': basename,
                    'target': url.path
                }

                if url.host == 'localhost' or url.host is None:
                    sd['action'] = rp.TRANSFER
                elif url.host == self.remote_fs.host:
                    sd['action'] = rp.COPY
                else:
                    print "### ERROR: Host not supported for this pilot!"

                cud.output_staging.append(sd)


        # Name
        cud.name = "mtms-task-%s-%s" % (task, stage)

        # Cores
        cud.cores  =  self.task_desc.cores

        # Build MDTaskDescription from kernel name
        mdtd = MDTaskDescription()

        if not self.task_desc.kernel:
            raise Exception('Kernel not specified.')
        mdtd.kernel = self.task_desc.kernel

        # Bind to resource
        mdtd_bound = mdtd.bind(resource=self.resource_desc.resource)

        # Fill in CUD
        cud.environment = mdtd_bound.environment
        cud.pre_exec = mdtd_bound.pre_exec
        cud.executable = mdtd_bound.executable
        cud.mpi = mdtd_bound.mpi

        if not self.task_desc.arguments:
            if self.verbose:
                print '### Will execute "%s"' % cud.executable
            arguments = None
        else:
            tmp = Template(self.task_desc.arguments)
            arguments = tmp.substitute(task_substitutions)
            if self.verbose:
                print '### Will execute "%s %s"' % (cud.executable, arguments)

        # Arguments
        if arguments:
            cud.arguments = arguments

        return cud
