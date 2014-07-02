#!/bin/sh

M1=1048576

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

echo "INFO: Creating output files ..."
# Create output files
# o_stage_du = ~7M
dd if=/dev/urandom of=$o_coor bs=$M1 count=1
ret=$?
if [ $ret -gt 0 ]; then
    echo "Writing output coor failed ...."
    exit $ret
fi
dd if=/dev/urandom of=$o_vel bs=$M1 count=1
ret=$?
if [ $ret -gt 0 ]; then
    echo "Writing output vel failed ...."
    exit $ret
fi
dd if=/dev/urandom of=$o_xsc bs=$M1 count=1
ret=$?
if [ $ret -gt 0 ]; then
    echo "Writing output xsc failed ...."
    exit $ret
fi
# o_log_du = 167M
#dd if=/dev/urandom of=$o_out bs=$M1 count=1
dd if=/dev/urandom bs=$M1 count=1
ret=$?
if [ $ret -gt 0 ]; then
    echo "Writing output out failed ...."
    exit $ret
fi
dd if=/dev/urandom bs=$M1 count=1 >&2
ret=$?
if [ $ret -gt 0 ]; then
    echo "Writing output err failed ...."
    exit $ret
fi
# o_ana_du = 3.6G
dd if=/dev/urandom of=$o_dcd bs=$M1 count=1
ret=$?
if [ $ret -gt 0 ]; then
    echo "Writing output dcd failed ...."
    exit $ret
fi
dd if=/dev/urandom of=$o_cvd bs=$M1 count=1
ret=$?
if [ $ret -gt 0 ]; then
    echo "Writing output cvd failed ...."
    exit $ret
fi
dd if=/dev/urandom of=$o_xst bs=$M1 count=1
ret=$?
if [ $ret -gt 0 ]; then
    echo "Writing output xst failed ...."
    exit $ret
fi

exit 0
