#!/usr/bin/env python

#from mtms import emulate_wf # , execute_wf
import mtms
#import bigjobasync

###############################################################################
#
# Main
#
if __name__ == '__main__':

    #
    # Resource configuration
    #
    #resource = bigjobasync.Resource(
    #    name = "india",
    #    resource = bigjobasync.RESOURCES['FUTUREGRID.INDIA'],
    #    username = 'marksant',
    #    runtime = 5,
    #    cores = 8,
    #    workdir = '/N/u/marksant/bja'
    #)
    resource = {}

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
    # Executable to run for every task
    #EXECUTABLE = 'namd-mockup.sh'
    EXECUTABLE = '/bin/echo'


    #
    # !!! No user-servicable parts below !!!
    # (Not completely true, but true enough!)
    #

    # The number of dynamic steps per system
    NUM_STEPS = SIM_TRAJ_TIME / TASK_SIM_TIME
    # Total number of systems to model, paper uses 105
    NUM_SYSTEMS = NUM_CHRS * NUM_LOCS

    tasks = range(NUM_SYSTEMS) # Could be any set of "items"
    num_stages = NUM_STEPS
    task_executable = EXECUTABLE
    task_arguments = '${__TASK__} ${__STAGE__} ${i_conf} ${i_pdb} ${i_crd} ${i_parm} ${i_coor} ${i_vel} ${i_xsc} ${o_coor} ${o_vel} ${o_xsc} ${o_out} ${o_err} ${o_dcd} ${o_cvd} ${o_xst}'

    #
    # INPUTS PER SYSTEM(S), FIRST DYNAMIC STEP(D) ONLY
    # (mineq_coor, mineq_vel, mineq_xsc)
    #     - mineq_coor[S]
    #     - mineq_vel[S]
    #     - mineq_xsc[S]
    #
    #
    input_per_task_first_stage = {
        'i_coor': 'mineq-${TASK}.coor',
        'i_vel': 'mineq-${TASK}.vel',
        'i_xsc': 'mineq-${TASK}.xsc'
    }

    #
    # INPUTS PER DYNAMIC STEP(D) FOR ALL SYSTEMS(S) (conf)
    #     - conf_1 .. conf_D
    #
    input_all_tasks_per_stage = {
        'i_conf': 'dyn-${STAGE}.conf'
    }

    #
    # INPUTS PER SYSTEM(S) FOR ALL DYNAMIC STEPS(D)
    # (sys.pdb, sys.parm, sys.crd)
    #     - pdb[S]
    #     - parm[S]
    #     - crc[S]
    #
    input_per_task_all_stages = {
        'i_pdb': 'sys-${TASK}.pdb',
        'i_parm': 'sys-${TASK}.parm',
        'i_crd': 'sys-${TASK}.crd'
    }

    #
    # SINKS PER SYSTEM(S) PER DYNAMIC STEP(D)
    # (dcd, cvd, xst, out, err)
    #     - dcd_1[S] .. dcd_D[S]
    #     - cvd_1[S] .. cvd_D[S]
    #     - xst_1[S] .. xst_D[S]
    #     - out_1[S] .. out_D[S]
    #     - err_1[S] .. err_D[S]
    #
    output_per_task_per_stage = {
        'o_dcd': 'dyn-${TASK}-${STAGE}.dcd',
        'o_cvd': 'dyn-${TASK}-${STAGE}.cvd',
        'o_xst': 'dyn-${TASK}-${STAGE}.xst',
        'o_out': 'dyn-${TASK}-${STAGE}.out',
        'o_err': 'dyn-${TASK}-${STAGE}.err'
    }

    #
    # INTERMEDIATE PER SYSTEM(S) PER DYNAMIC STEP(D)
    # (coor, vel, xsc)
    #     - coor_1[S] .. coor_D[S]
    #     - vel_1[S] .. vel_D[S]
    #     - xsc_1[S] .. xsc_D[S]
    #
    # TODO: rename to intermediate without "output" ?
    intermediate_output_per_task_per_stage = [
        {'input_label': 'i_coor', 'output_label': 'o_coor', 'pattern': 'dyn-${TASK}-${STAGE}.coor'},
        {'input_label': 'i_vel', 'output_label': 'o_vel', 'pattern': 'dyn-${TASK}-${STAGE}.vel'},
        {'input_label': 'i_xsc', 'output_label': 'o_xsc', 'pattern': 'dyn-${TASK}-${STAGE}.xsc'}
    ]

    #
    # OUTPUTS PER SYSTEM(S) FOR FINAL DYNAMIC STEP(D) ONLY
    # (coor, vel, xsc)
    #     - coor[S]
    #     - vel[S]
    #     - xsc[S]
    #
    output_per_task_final_stage = {
        'o_coor': 'dyn-${TASK}-${STAGE}.coor',
        'o_vel': 'dyn-${TASK}-${STAGE}.vel',
        'o_xsc': 'dyn-${TASK}-${STAGE}.xsc'
    }

    # mtms.emulate_wf(
    #     # Task execution description
    #     EXECUTABLE,
    #     task_arguments,
    #     # Task "shape" definition
    #     tasks,
    #     num_stages,
    #     # Task I/O specification in the form of { 'label': 'pattern' }
    #     input_per_task_first_stage,
    #     input_all_tasks_per_stage,
    #     input_per_task_all_stages,
    #     output_per_task_per_stage,
    #     intermediate_output_per_task_per_stage, # in the form of [{input_label, output_label, pattern}]
    #     output_per_task_final_stage
    # )
    mtms.execute_wf(
        resource,
        # Task execution description
        EXECUTABLE,
        task_arguments,
        # Task "shape" definition
        tasks,
        num_stages,
        # Task I/O specification in the form of { 'label': 'pattern' }
        input_per_task_first_stage,
        input_all_tasks_per_stage,
        input_per_task_all_stages,
        output_per_task_per_stage,
        intermediate_output_per_task_per_stage, # in the form of [{input_label, output_label, pattern}]
        output_per_task_final_stage
    )

#
###############################################################################
