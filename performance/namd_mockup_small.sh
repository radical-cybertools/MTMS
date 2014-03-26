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
o_out=${13}
o_err=${14}
# o_ana_du = 3.6G
o_dcd=${15}
o_cvd=${16}
o_xst=${17}

# Check input file sizes
if [[ -f $i_conf && `stat --dereference --format=%s $i_conf` -ne 1024 ]]; then
    echo "ERROR: config file has wrong size!"
    exit 1
else
    echo "INFO: config file has correct size!"
fi
if [[ -f $i_pdb &&`stat --dereference --format=%s $i_pdb` -ne 1048576 ]]; then
    echo "ERROR: pdb file has wrong size!"
    exit 1
else
    echo "INFO: pdb file has correct size!"
fi
if [[ -f $i_crd && `stat --dereference --format=%s $i_crd` -ne 1048576 ]]; then
    echo "ERROR: crd file has wrong size!"
    exit 1
else
    echo "INFO: crd file has correct size!"
fi
if [[ -f $i_parm && `stat --dereference --format=%s $i_parm` -ne 1048576 ]]; then
    echo "ERROR: parm file has wrong size!"
    exit 1
else
    echo "INFO: parm file has correct size!"
fi
if [[ -f $i_coor && `stat --dereference --format=%s $i_coor` -ne 1048576 ]]; then
    echo "ERROR: coor file has wrong size!"
    exit 1
else
    echo "INFO: coor file has correct size!"
fi
if [[ -f $i_vel && `stat --dereference --format=%s $i_vel` -ne 1048576 ]]; then
    echo "ERROR: vel file has wrong size!"
    exit 1
else
    echo "INFO: vel file has correct size!"
fi
if [[ -f $i_xsc && `stat --dereference --format=%s $i_xsc` -ne 1048576 ]]; then
    echo "ERROR: xsc file has wrong size!"
    exit 1
else
    echo "INFO: xsc file has correct size!"
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
dd if=/dev/urandom of=$o_out bs=1M count=1
ret=$?
if [ $ret -gt 0 ]; then
    echo "Writing output out failed ...."
    exit $ret
fi
dd if=/dev/urandom of=$o_err bs=1M count=1
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
