""" Application kernel configuration file.
"""

KERNEL = {

    "NAMD" :
    {
        "description" : "NAMD is a molecular dynamics simulation package.",
        "resources" :
        {
            "XSEDE.STAMPEDE" :
            {
                "pre_execution" : "module load namd",
                "executable" : "/opt/apps/intel13/mvapich2_1_9/namd/2.9/bin/namd2",
            }
        }
    },

    'DUMMY' :
    {
        "description" : "A dummy NAMD that does NOTHING.",
        "resources" :
        {
            "XSEDE.STAMPEDE" :
            {
                "pre_execution" : "/bin/true",
                "executable" : "/bin/sleep 10"
            }
        }
    }
}
