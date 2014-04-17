#!/bin/bash

NUM_CHRS=5 # 5
NUM_LOCS=21 #21
NUM_STAGES=20 #20
INPUT_FILES="min-eq.coor min-eq.vel min-eq.xsc sys.pdb sys.crd sys.parm"
PREFIX=$PWD/../../data

SOURCE_DIR=$PWD

conf_dir="$PREFIX/dyn-conf-files"
mkdir -p $conf_dir
cat ${SOURCE_DIR}/template.conf |sed 's/IN_PLACEHOLDER/set IN		min-eq/; s/OUT_PLACEHOLDER/set OUT		dyn1/' > ${conf_dir}/dyn1.conf
for conf in `seq 2 \`expr $NUM_STAGES\``; do
    cat ${SOURCE_DIR}/template.conf |sed "s/IN_PLACEHOLDER/set IN		dyn`expr ${conf} - 1`/; s/OUT_PLACEHOLDER/set OUT		dyn${conf}/" > ${conf_dir}/dyn${conf}.conf
done

for chr in `seq 0 \`expr $NUM_CHRS - 1\``; do
	for loc in `seq 0 \`expr $NUM_LOCS - 1\``; do
		dir="$PREFIX/$chr/$loc"
		mkdir -p $dir

        for name in $INPUT_FILES; do

            file=$dir/$name
			if [ $chr -eq 0 -a $loc -eq 0 ]; then
				cp ${SOURCE_DIR}/${name} ${file}
			else
				ln -s $PREFIX/0/0/$name $file
			fi
        done;

	done
done
