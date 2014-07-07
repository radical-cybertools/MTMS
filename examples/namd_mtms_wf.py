#!/usr/bin/env python

from radical.ensemblemd import mtms
import os

###############################################################################
#
# Main
#
if __name__ == '__main__':

    #
    # Resource configuration
    #
    resource_desc = mtms.Resource_Description()
    resource_desc.runtime = 30 # minutes
    #
    # Localhost
    #resource_desc.resource = 'localhost'
    #resource_desc.cores = 4
    #resource_desc.dburl = 'mongodb://localhost:27017'
    #DATA_PREFIX = os.getcwd()
    #
    # Stampede
    resource_desc.resource = 'stampede.tacc.utexas.edu'
    resource_desc.cores = 16
    resource_desc.project = "TG-MCB090174"
    DATA_PREFIX = "sftp://stampede.tacc.utexas.edu/work/01740/marksant/demo/data"
    #DATA_PREFIX = 'file://localhost' + os.getcwd() + '/data'
    #
    # India
    #resource_desc.resource = 'india.futuregrid.org'
    #
    # Archer
    #resource_desc.resource = 'archer.ac.uk'
    #resource_desc.project = 'e290'
    #resource_desc.cores = 24
    #DATA_PREFIX = 'file://localhost' + os.getcwd() + '/data'
    #DATA_PREFIX= "sftp://login.archer.ac.uk/fs4/e290/e290/marksant/demo/data"
    #
    # SuperMUC
    #resource_desc.resource = 'supermuc.lrz.de'

    #
    # Application specific runtime characteristics
    #
    # Number of chromosomes
    NUM_CHRS = 1 # exp:5
    # Number of locations per chromosome
    NUM_LOCS = 2 # exp:21
    # The time of simulation per system
    SIM_TRAJ_TIME = 3 # exp:20
    # The simulation time per dynamic step
    TASK_SIM_TIME = 1
    # Executable kernel to run for every task
    KERNEL = 'NAMD'
    CORES = 8
    VERBOSE=True

    ######################################################################
    #
    # !!! No user-servicable parts below !!!
    #

    # The number of dynamic steps per system
    NUM_STEPS = SIM_TRAJ_TIME / TASK_SIM_TIME

    task_desc = mtms.Task_Description()
    task_desc.tasks = ['%d/%d' % (i,j) for i in range(NUM_CHRS) for j in range(NUM_LOCS)]
    task_desc.num_stages = NUM_STEPS
    task_desc.kernel = KERNEL
    task_desc.arguments = '${i_conf}'
    task_desc.cores = CORES

    io_desc = mtms.IO_Description()
    #
    # INPUTS PER SYSTEM(S), FIRST DYNAMIC STEP(D) ONLY
    # (mineq_coor, mineq_vel, mineq_xsc)
    #     - mineq_coor[S]
    #     - mineq_vel[S]
    #     - mineq_xsc[S]
    #
    #
    io_desc.input_per_task_first_stage = {
        'i_coor': '%s/${TASK}/min-eq.coor' % DATA_PREFIX,
        'i_vel': '%s/${TASK}/min-eq.vel' % DATA_PREFIX,
        'i_xsc': '%s/${TASK}/min-eq.xsc' % DATA_PREFIX
    }

    #
    # INPUTS PER DYNAMIC STEP(D) FOR ALL SYSTEMS(S) (conf)
    #     - conf_1 .. conf_D
    #
    io_desc.input_all_tasks_per_stage = {
        'i_conf': '%s/dyn-conf-files/dyn${STAGE}.conf' % (DATA_PREFIX),
    }

    #
    # INPUTS PER SYSTEM(S) FOR ALL DYNAMIC STEPS(D)
    # (sys.pdb, sys.parm, sys.crd)
    #     - pdb[S]
    #     - parm[S]
    #     - crc[S]
    #
    io_desc.input_per_task_all_stages = {
        'i_pdb': '%s/${TASK}/sys.pdb' % DATA_PREFIX,
        'i_parm': '%s/${TASK}/sys.parm' % DATA_PREFIX,
        'i_crd': '%s/${TASK}/sys.crd' % DATA_PREFIX
    }

    #
    # SINKS PER SYSTEM(S) PER DYNAMIC STEP(D)
    # (dcd, dvd, xst, out, err)
    #     - dcd_1[S] .. dcd_D[S]
    #     - dvd_1[S] .. dvd_D[S]
    #     - xst_1[S] .. xst_D[S]
    #     - out_1[S] .. out_D[S] # get from stdout
    #     - err_1[S] .. err_D[S] # get from stderr
    #
    io_desc.output_per_task_per_stage = {
        'o_dcd': '%s/${TASK}/dyn${STAGE}.dcd' % DATA_PREFIX,
        'o_dvd': '%s/${TASK}/dyn${STAGE}.dvd' % DATA_PREFIX,
        'o_xst': '%s/${TASK}/dyn${STAGE}.xst' % DATA_PREFIX,
        'STDOUT': '%s/${TASK}/dyn${STAGE}.out' % DATA_PREFIX, # STDOUT is special value
        'STDERR': '%s/${TASK}/dyn${STAGE}.err' % DATA_PREFIX  # STDERR is special value
    }

    #
    # INTERMEDIATE PER SYSTEM(S) PER DYNAMIC STEP(D)
    # (coor, vel, xsc)
    #     - coor_1[S] .. coor_D[S]
    #     - vel_1[S] .. vel_D[S]
    #     - xsc_1[S] .. xsc_D[S]
    #
    # TODO: rename to intermediate without "output" ?
    io_desc.intermediate_output_per_task_per_stage = [
        {'input_label': 'i_coor', 'output_label': 'o_coor', 'pattern': '%s/${TASK}/dyn${STAGE}.coor' % DATA_PREFIX},
        {'input_label': 'i_vel', 'output_label': 'o_vel', 'pattern': '%s/${TASK}/dyn${STAGE}.vel' % DATA_PREFIX},
        {'input_label': 'i_xsc', 'output_label': 'o_xsc', 'pattern': '%s/${TASK}/dyn${STAGE}.xsc' % DATA_PREFIX}
    ]

    #
    # OUTPUTS PER SYSTEM(S) FOR FINAL DYNAMIC STEP(D) ONLY
    # (coor, vel, xsc)
    #     - coor[S]
    #     - vel[S]
    #     - xsc[S]
    #
    io_desc.output_per_task_final_stage = {
        'o_coor': '%s/${TASK}/dyn${STAGE}.coor' % DATA_PREFIX,
        'o_vel': '%s/${TASK}/dyn${STAGE}.vel' % DATA_PREFIX,
        'o_xsc': '%s/${TASK}/dyn${STAGE}.xsc' % DATA_PREFIX
    }

    engine = mtms.Engine()
    engine.execute(resource_desc, task_desc, io_desc, verbose=VERBOSE)

    print 'Done!'

#
###############################################################################
