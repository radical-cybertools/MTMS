#!/bin/sh

# general
task=$1
stage=$2
# i_conf_du
i_conf=$3 #
# i_param_du
i_pdb=$4
i_crd=$5
i_parm=$6
# i_stage_du
i_coor=$7
i_vel=$8
i_xsc=${9}
# o_stage_du = ~7M
o_coor=${10}
o_vel=${11}
o_xsc=${12}
# o_log_du = 167M
#o_out=${13}
#o_err=${14}
# o_ana_du = 3.6G
o_dcd=${13}
o_cvd=${14}
o_xst=${15}

# Check input file sizes
if [[ `stat --dereference --format=%s $i_conf` -eq 1024 ]]; then
    echo "INFO: config file $i_conf has correct size!"
else
    echo "ERROR: config file $i_conf is missing or has wrong size!"
    exit 1
fi
if [[ `stat --dereference --format=%s $i_pdb` -eq 1048576 ]]; then
    echo "INFO: pdb file $i_pdb has correct size!"
else
    echo "ERROR: pdb file $i_pdb is missing or has wrong size!"
    exit 1
fi
if [[ `stat --dereference --format=%s $i_crd` -eq 1048576 ]]; then
    echo "INFO: crd file $i_crd has correct size!"
else
    echo "ERROR: crd file $i_crd is missing or has wrong size!"
    exit 1
fi
if [[ `stat --dereference --format=%s $i_parm` -eq 1048576 ]]; then
    echo "INFO: parm file $i_parm has correct size!"
else
    echo "ERROR: parm file $i_parm is missing or has wrong size!"
    exit 1
fi
if [[ `stat --dereference --format=%s $i_coor` -eq 1048576 ]]; then
    echo "INFO: coor file $i_coor has correct size!"
else
    echo "ERROR: coor file $i_coor is missing or has wrong size!"
    exit 1
fi
if [[ `stat --dereference --format=%s $i_vel` -eq 1048576 ]]; then
    echo "INFO: vel file $i_vel has correct size!"
else
    echo "ERROR: vel file $i_vel is missing or has wrong size!"
    exit 1
fi
if [[ `stat --dereference --format=%s $i_xsc` -eq 1048576 ]]; then
    echo "INFO: xsc file $i_xsc has correct size!"
else
    echo "ERROR: xsc file $i_xsc is missing has wrong size!"
    exit 1
fi

echo "INFO: Creating output files ..."
# Create output files
# o_stage_du = ~7M
dd if=/dev/urandom of=$o_coor bs=1M count=1
ret=$?
if [ $ret -gt 0 ]; then
    echo "Writing output coor failed ...."
    exit $ret
fi
dd if=/dev/urandom of=$o_vel bs=1M count=1
ret=$?
if [ $ret -gt 0 ]; then
    echo "Writing output vel failed ...."
    exit $ret
fi
dd if=/dev/urandom of=$o_xsc bs=1M count=1
ret=$?
if [ $ret -gt 0 ]; then
    echo "Writing output xsc failed ...."
    exit $ret
fi
# o_log_du = 167M
dd if=/dev/urandom bs=1M count=1
ret=$?
if [ $ret -gt 0 ]; then
    echo "Writing output out failed ...."
    exit $ret
fi
dd if=/dev/urandom bs=1M count=1 >&2
ret=$?
if [ $ret -gt 0 ]; then
    echo "Writing output err failed ...."
    exit $ret
fi
# o_ana_du = 3.6G
dd if=/dev/urandom of=$o_dcd bs=1M count=1
ret=$?
if [ $ret -gt 0 ]; then
    echo "Writing output dcd failed ...."
    exit $ret
fi
dd if=/dev/urandom of=$o_cvd bs=1M count=1
ret=$?
if [ $ret -gt 0 ]; then
    echo "Writing output cvd failed ...."
    exit $ret
fi
dd if=/dev/urandom of=$o_xst bs=1M count=1
ret=$?
if [ $ret -gt 0 ]; then
    echo "Writing output xst failed ...."
    exit $ret
fi

exit 0
